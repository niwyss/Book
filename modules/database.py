#!/usr/bin/python
# -*- coding:utf-8 -*-

# Copyright 2012 Nicolas Wyss
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

import sys, os
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy import or_
from modules.model import Base, Book, Author

class Common(object):

    def __init__(self, database_path=":memory:"):
        self.engine = create_engine("sqlite:///{0}".format(database_path))
        self.session = scoped_session(sessionmaker(bind=self.engine, autoflush=True, autocommit=False))

    def create(self):
        Base.metadata.create_all(self.engine)

    def drop(self):
        Base.metadata.drop_all(self.engine)

common = Common()

class BookFacade(object):

    def put(self, book):

        def sync_author(author_to_add):
            dao = AuthorDAO()
            author_in_base = dao.get(author_to_add.name)
            return author_in_base if author_in_base else author_to_add

        # Sync new authors with already presents one
        authors = map(sync_author, book.authors)
        book.authors = authors

        bookDAO = BookDAO()
        bookDAO.put(book)

        return book

    def get(self, isbn):
        dao = BookDAO()
        return dao.get(isbn)


class BookDAO(object):

    def put(self, book):
        session = common.session()
        session.add(book)
        session.commit()
        return book

    def get(self, isbn):
        session = common.session()
        books = session.query(Book).filter(or_(Book.isbn10 == isbn, Book.isbn13 == isbn)).all()
        session.commit()
        return books[0] if books else None

class AuthorDAO(object):

    def put(self, author):
        session = common.session()
        session.add(author)
        session.commit()
        return author

    def get(self, name):
        session = common.session()
        authors = session.query(Author).filter(Author.name == name).all()
        session.commit()
        return authors[0] if authors else None
