#!/usr/local/bin/python
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

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from multiprocessing.dummy import Pool as ThreadPool
from modules.model import Base, Book, Author
from modules.database import common, BookDAO, AuthorDAO, BookFacade
from threading import Thread

class TestQuery(unittest.TestCase):

    def setUp(self):
        common.create()

    def tearDown(self):
        common.drop()

    def test_dao_put_author(self):

        author = Author()
        author.name = "John Snow"

        dao = AuthorDAO()
        dao.put(author)

        session = common.session()

        expected = [author]
        result = session.query(Author).all()
        self.assertEqual(result, expected)

    def test_dao_get_author(self):

        author = Author()
        author.name = "John Snow"

        session = common.session()
        session.add(author)
        session.commit()

        dao = AuthorDAO()

        expected = author
        result = dao.get("John Snow")
        self.assertEqual(result, expected)

    def test_dao_put_book_add(self):

        author = Author()
        author.name = "John Snow"

        book = Book()
        book.isbn10 = "0123456789"
        book.isbn13 = "0123456789123"
        book.title = "A title"
        book.nb_pages = 5
        book.language = "fr"
        book.year = 2015
        book.description = "The long description"
        book.authors.append(author)

        dao = BookDAO()
        dao.put(book)

        session = common.session()

        expected = [book]
        result = session.query(Book).all()
        self.assertEqual(result, expected)

        expected = [author]
        result = session.query(Author).all()
        self.assertEqual(result, expected)

    def test_dao_get_book(self):

        author = Author()
        author.name = "John Snow"

        book = Book()
        book.isbn10 = "0123456789"
        book.isbn13 = "0123456789123"
        book.title = "A title"
        book.nb_pages = 5
        book.language = "fr"
        book.year = 2015
        book.description = "The long description"
        book.authors.append(author)

        session = common.session()
        session.add(book)
        session.commit()

        dao = BookDAO()

        expected = book
        result = dao.get(book.isbn10)
        self.assertEqual(result, expected)

    def test_dao_put_book_update(self):

        author = Author()
        author.name = "John Snow"

        book = Book()
        book.isbn10 = "0123456789"
        book.isbn13 = "0123456789123"
        book.title = "A title"
        book.nb_pages = 5
        book.language = "fr"
        book.year = 2015
        book.description = "The long description"
        book.authors.append(author)

        dao = BookDAO()
        dao.put(book)

        book.description = "Another description"
        book.title = "Another title"
        book.nb_pages = 10
        book.language = "en"
        book.year = 2014

        dao.put(book)

        session = common.session()

        expected = [book]
        result = session.query(Book).all()
        self.assertEqual(result, expected)

        expected = [author]
        result = session.query(Author).all()
        self.assertEqual(result, expected)

    def test_facade_put_book(self):

        authorA = Author()
        authorA.name = "John Snow"

        bookA = Book()
        bookA.isbn10 = "0123456789"
        bookA.isbn13 = "0123456789123"
        bookA.title = "A title"
        bookA.nb_pages = 5
        bookA.language = "fr"
        bookA.year = 2015
        bookA.description = "The long description"
        bookA.authors.append(authorA)

        authorB = Author()
        authorB.name = "John Snow"

        authorC = Author()
        authorC.name = "Bidule Chose"

        bookB = Book()
        bookB.isbn10 = "9876543210"
        bookB.isbn13 = "3219876543219"
        bookB.title = "Another title"
        bookB.nb_pages = 18
        bookB.language = "fr"
        bookB.year = 2014
        bookB.description = "The very long description"
        bookB.authors.append(authorB)
        bookB.authors.append(authorC)

        facade = BookFacade()
        facade.put(bookA)
        facade.put(bookB)

        session = common.session()

        self.assertEqual(session.query(Book).count(), 2)
        expected = [bookA, bookB]
        result = session.query(Book).all()
        self.assertEqual(result, expected)

        self.assertEqual(session.query(Author).count(), 2)
        result = session.query(Author).all()
        self.assertEqual(result, [authorA, authorC])
        self.assertEqual(result, [authorB, authorC])


if __name__ == '__main__':
	unittest.main()
