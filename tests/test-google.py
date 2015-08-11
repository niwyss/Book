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
from modules.model import *
from modules.googlebook import *

class TestGoogleBookDataParsere(unittest.TestCase):

	def test_parse_data_with_none(self):

		parser = GoogleBookDataParser()
		result = parser.parse(None)

		self.assert_(True)
		self.assertFalse(result)

	def test_parse_ko(self):

		with open('tests/data/googlebook-ko.json') as data_file:
			data = json.load(data_file)

		parser = GoogleBookDataParser()
		result = parser.parse(data)

		self.assert_(True)
		self.assertFalse(result)

	def test_parse_ok(self):

		with open('tests/data/googlebook-ok.json') as data_file:
			data = json.load(data_file)

		parser = GoogleBookDataParser()
		result = parser.parse(data)

		self.assert_(True)
		self.assertTrue(result)
		self.assertEqual(parser.title, "The title")
		self.assertEqual(parser.authors, [u"Author n°1", u"Author n°2"])
		self.assertEqual(parser.publishedYear, "2013")
		self.assertEqual(parser.description, "The long description")
		self.assertEqual(parser.pageCount, 55)
		self.assertEqual(parser.language, "en")
		self.assertEqual(parser.isbn10, "0123456789")
		self.assertEqual(parser.isbn13, "0123456789123")


if __name__ == '__main__':
	unittest.main()
