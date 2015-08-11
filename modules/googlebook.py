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

import json, sys, httplib

HOST = "www.googleapis.com"
HEADERS = {}
URL_FETCH_ID = "/books/v1/volumes?q=isbn:{0}&key={1}"
URL_FETCH_ALL = "/books/v1/volumes/{0}?key={1}"

class GoogleBookDataParser(object):

    def __init__(self):
        self.title = None
        self.authors = None
        self.isbn10 = None
        self.isbn13 = None
        self.thumbnail_url = None
        self.publishedDate = None
        self.description = None
        self.pageCount = None
        self.language = None

    def parse(self, data):

        if data and "volumeInfo" in data:

            if "title" in data["volumeInfo"] and data["volumeInfo"]["title"]:
                self.title = data["volumeInfo"]["title"]

            if "authors" in data["volumeInfo"] and data["volumeInfo"]["authors"]:
                self.authors = data["volumeInfo"]["authors"]

            if "publishedDate" in data["volumeInfo"] and data["volumeInfo"]["publishedDate"]:
                self.publishedYear = data["volumeInfo"]["publishedDate"][:4]

            if "description" in data["volumeInfo"] and data["volumeInfo"]["description"]:
                self.description = data["volumeInfo"]["description"]

            if "pageCount" in data["volumeInfo"] and data["volumeInfo"]["pageCount"]:
                self.pageCount = data["volumeInfo"]["pageCount"]

            if "language" in data["volumeInfo"] and data["volumeInfo"]["language"]:
                self.language = data["volumeInfo"]["language"]

            if "industryIdentifiers" in data["volumeInfo"] and data["volumeInfo"]["industryIdentifiers"]:
                for identifier in data["volumeInfo"]["industryIdentifiers"]:
                    if "type" in identifier and "identifier" in identifier:
                        if identifier["type"] == "ISBN_10":
                            self.isbn10 = identifier["identifier"]
                        elif identifier["type"] == "ISBN_13":
                            self.isbn13 = identifier["identifier"]

            if "imageLinks" in data["volumeInfo"] and data["volumeInfo"]["imageLinks"]:
                if "thumbnail" in data["volumeInfo"]["imageLinks"] and data["volumeInfo"]["imageLinks"]["thumbnail"]:
                    self.thumbnail_url = data["volumeInfo"]["imageLinks"]["thumbnail"]

            if not self.description:
                self.description = "No description"

            result = True
            result &= self.title is not None
            result &= self.authors is not None
            result &= self.isbn10 is not None
            result &= self.isbn13 is not None
            result &= self.thumbnail_url is not None
            result &= self.publishedYear is not None
            result &= self.description is not None
            result &= self.pageCount is not None
            result &= self.language is not None

            return result

        return False

    def __repr__(self):
        return (
            "<GoogleBookDataParser('{self.title}', '{self.authors}', '{self.isbn10}',"
            "'{self.isbn13}', '{self.thumbnail_url}', '{self.publishedYear}', '{self.description}',"
            "'{self.pageCount}', '{self.language}')>".format(self=self)
        )

class GoogleBookService(object):

    def __init__(self, key):
        self.key = key

    def __fetch_data_from_web(self, host, url, headers):
        try:
            conn = httplib.HTTPSConnection(host)
            conn.request("GET", url)
            response = conn.getresponse()
            data = response.read()
            conn.close()
            return json.loads(data)
        except:
            print "book: error: web service unreachable."
            sys.exit(0)

    def fetch_data(self, code_isbn):

        # Get data from "Fetch ID" service
        url = URL_FETCH_ID.format(code_isbn, self.key)
        data = self.__fetch_data_from_web(HOST, url, HEADERS)

        if data is not None and "error" not in data:

            # Extract Google ID
            id = ""
            if data["totalItems"] > 0:
                item = data["items"][0]
                id = item["id"]

            # Get data from "Fetch All" service
            url = URL_FETCH_ALL.format(id, self.key)
            data = self.__fetch_data_from_web(HOST, url, HEADERS)

            if data is not None and "error" not in data:
                return data

        return None
