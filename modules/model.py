#!/usr/bin/python
# -*- coding: utf-8 -*-

# BOOK : More than a simple moneybox
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
# along with BOOK. If not, see <http://www.gnu.org/licenses/>.

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    books = relationship(
        'Book',
        secondary='book_author_link'
    )

    def __init__(self):
        self.name = None

    def __repr__(self):
        return (
            "<Author('{self.id}', '{self.name}')>".format(self=self)
        )

    def __eq__(self, other):
        return (isinstance(other, Author) and self.name == other.name)

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    isbn10 = Column(String(10), nullable=False)
    isbn13 = Column(String(13), nullable=False)
    title = Column(String(250), nullable=False)
    nb_pages = Column(Integer, nullable=False)
    language = Column(String(250), nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(String(250), nullable=False)
    authors = relationship(
        'Author',
        secondary='book_author_link'
    )

    def __init__(self):
        self.id = None
        self.isbn10 = None
        self.isbn13 = None
        self.title = None
        self.nb_pages = None
        self.language = None
        self.year = None
        self.description = None

    def __repr__(self):
        return (
            "<Book('{self.title}', '{self.authors}', "
            "'{self.year}', '{self.description}', "
            "'{self.nb_pages}', '{self.language}', "
            "'{self.isbn10}', '{self.isbn13}')>".format(self=self)
        )

    def __eq__(self, other):
        return (isinstance(other, Book) and
                self.id == other.id and
                self.isbn10 == other.isbn10 and
                self.isbn13 == other.isbn13 and
                self.title == other.title and
                self.nb_pages == other.nb_pages and
                self.language == other.language and
                self.year == other.year and
                self.authors == other.authors and
                self.description == other.description)

class BookAuthorLink(Base):
    __tablename__ = 'book_author_link'
    book_id = Column(Integer, ForeignKey('book.id'), primary_key=True)
    author_id = Column(Integer, ForeignKey('author.id'), primary_key=True)
    book = relationship(Book, backref=backref("author_assoc"))
    author = relationship(Author, backref=backref("book_assoc"))
