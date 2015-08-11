#!/usr/bin/python
# -*- coding:utf-8 -*-

# Copyright 2013 Nicolas Wyss
#
# This file is part of BOOK.
#
# BOOK is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BOOK is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BOOK.  If not, see <http://www.gnu.org/licenses/>.

import sqlite3, sys, os, shutil, json, urllib, imghdr
from datetime import datetime

import utils, database
from model import Book, Author
from database import BookFacade
from googlebook import GoogleBookService, GoogleBookDataParser
from pdf import PDFScanner
from net import Download, Downloader

def work(pdf_paths):

    products = []
    print "Found {0} file(s) to scan.".format(len(pdf_paths))

    for pdf_path in pdf_paths:

        try:

            utils.logger.info("Works on {0}".format(pdf_path))

            # Clean tmp folder
            utils.clean_folder(utils.configuration.tmp_path)

            # Build the treatment
            extractISBNFromPDF = ExtractISBNFromPDFTreatment()
            checkISBNInDatabase = CheckISBNInDatabaseTreatment()
            downloadDataFromGoogleBook = DownloadDataFromGoogleBookTreatment()
            store = StoreTreatment()

            # Chain the treatment
            firstTreatment = extractISBNFromPDF
            extractISBNFromPDF.next = checkISBNInDatabase
            checkISBNInDatabase.next = downloadDataFromGoogleBook
            downloadDataFromGoogleBook.next = store

            # Build the product
            product = Product()
            product.pdf_path = pdf_path;

            # Start
            products.append(firstTreatment.proceed(product))

            utils.logger.info("Process terminated with the status : {0}".format(['Still waiting', 'Done', 'Error', 'Already'][product.status]))

        except IOError as e:
            print "error({0}): {1}".format(e.errno, e.strerror)
        except OSError as e:
            print "error({0}): {1}".format(e.errno, e.strerror)

    done = filter(lambda x: Status.Done == x.status, products)
    error = filter(lambda x: Status.Error == x.status, products)
    already = filter(lambda x: Status.Already == x.status, products)
    waiting = filter(lambda x: Status.Waiting == x.status, products)

    print " {0} new book(s) stored, {1} book(s) already present, {2} files with error.".format(len(done), len(already), len(error))

    if error and len(error) > 0:
        print " files with errors :"
        for item in error:
            print " --> {0}".format(item.pdf_path)
            shutil.copy2(item.pdf_path, utils.configuration.error_path + "/" + datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3] + ".pdf")

class Status:
    Waiting, Done, Error, Already = range(0, 4)

class Product(object):

    def __init__(self):
        self.book = None
        self.pdf_path = None
        self.metadata_path = None
        self.thumbnail_path = None
        self.status = Status.Waiting

class Treatment(object):

    def __init__(self):
        self.next = None

    def proceed(self, product):
        return True

class ExtractISBNFromPDFTreatment(Treatment):

    def proceed(self, product):

        # Open the PDF file
        pdf = file(product.pdf_path, 'rb')

        # Extract the ISBN code
        scanner = PDFScanner(pdf)
        scanner.extractISBN()

        # Close the PDF file
        pdf.close()

        if scanner.isbn13 is not None:

            # Store ISBN
            product.book = Book()
            product.book.isbn13 = scanner.isbn13
            product.book.isbn10 = scanner.isbn10

            utils.logger.info("Found ISBN [13:{0}, 10:{1}]".format(product.book.isbn13, product.book.isbn10))

            if self.next:
                return self.next.proceed(product)

            product.status = Status.Done
            return product

        utils.logger.info("ISBN not Found")

        product.status = Status.Error
        return product

class CheckISBNInDatabaseTreatment(Treatment):

    def proceed(self, product):

        # Fetch Book from database
        facade = BookFacade()
        book = facade.get(product.book.isbn13)

        if book is None:

            utils.logger.info("This book is not in database")

            if self.next:
                return self.next.proceed(product)

            product.status = Status.Done
            return product

        utils.logger.info("This book is already in databse")

        product.status = Status.Already
        return product

class DownloadDataFromGoogleBookTreatment(Treatment):

    def proceed(self, product):

        # Fetch metadata from Google
        service = GoogleBookService(utils.configuration.googlebook_key)
        data = service.fetch_data(product.book.isbn13)

        if data is not None:

            # Parse the metadata
            parser = GoogleBookDataParser()

            if parser.parse(data):

                # Convert to book
                book = Book()
                book.title = parser.title
                book.isbn10 = parser.isbn10
                book.isbn13 = parser.isbn13
                book.year = parser.publishedYear
                book.description = parser.description
                book.nb_pages = parser.pageCount
                book.language = parser.language

                def convert_name_to_author(name):
                    author = Author()
                    author.name = name
                    return author

                book.authors = map(convert_name_to_author, parser.authors)

                if book is not None and book.isbn10 == product.book.isbn10 and book.isbn13 == product.book.isbn13:

                    # Store the book
                    product.book = book

                    # Save data from Googlebook
                    product.metadata_path = "{0}/{1}.json".format(utils.configuration.tmp_path, product.book.isbn13)
                    with open(product.metadata_path, 'w') as outfile:
                        json.dump(data, outfile)

                    # Download the thumbnail
                    product.thumbnail_path = "{0}/{1}.picture".format(utils.configuration.tmp_path, product.book.isbn13)
                    download = Download(parser.thumbnail_url, product.thumbnail_path)
                    downloader = Downloader(download)
                    downloader.run()

                    if download.status:

                        utils.logger.info("Match found in Google Book database [{0}]".format(book.title))

                        if self.next:
                            return self.next.proceed(product)

                        product.status = Status.Done
                        return product

        utils.logger.info("This book is unknow from Google Book database")

        product.status = Status.Error
        return product

class StoreTreatment(Treatment):

    def proceed(self, product):

        # Add book in database
        facade = BookFacade()
        book = facade.put(product.book)

        # Get path to the book
        book_path = utils.configuration.library_path + "/" + product.book.isbn13

        # Create book directory
        os.makedirs(book_path, mode=0777)

        # Copy PDF file to book directory
        shutil.copy2(product.pdf_path, book_path + "/" + product.book.isbn13  + ".pdf")
        shutil.move(product.metadata_path, book_path + "/" + product.book.isbn13  + ".json")
        shutil.move(product.thumbnail_path, book_path + "/" + product.book.isbn13  + "." + imghdr.what(product.thumbnail_path))

        utils.logger.info("Book stored")

        if self.next:
            return self.next.proceed(product)

        product.status = Status.Done
        return product
