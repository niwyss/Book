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
from modules.pdf import PDFScanner

def read_file(file_path):
	data = open(file_path, 'r')
	try:
		text = data.read()
	finally:
		data.close()
	return text


class TestPDFScanner(unittest.TestCase):

	def test_clean(self):

		scanner = PDFScanner(None)

		phrase = "0a1§2!3à4k5L6P7&8é9a"
		phrase = scanner.clean(phrase)
		self.assertEqual(phrase, "0123456789")

	def test_searchCodeInPage(self):

		scanner = PDFScanner(None)

		# Test 1
		page = read_file("tests/data/test_no-isbn.txt")
		code = scanner.searchCodeInPage(page)
		self.assertEqual(code, "")

		# Test 2
		page = read_file("tests/data/test_isbn-1.txt")
		code = scanner.searchCodeInPage(page)
		self.assertEqual(code, "0123456789012")

		# Test 3
		page = read_file("tests/data/test_isbn-2.txt")
		code = scanner.searchCodeInPage(page)
		self.assertEqual(code, "0123456789012")

		# Test 4
		page = read_file("tests/data/test_isbn-3.txt")
		code = scanner.searchCodeInPage(page)
		self.assertEqual(code, "9876543212346")

		# Test 5
		page = read_file("tests/data/test_isbn-4.txt")
		code = scanner.searchCodeInPage(page)
		self.assertEqual(code, "0201633612")

	def test_extract_isbn(self):

		pdf = file("tests/data/test_book-1.pdf", 'rb')
		scanner = PDFScanner(pdf)

		scanner.extractISBN()

		isbn13 = scanner.isbn13
		self.assertEqual(isbn13, "9783161484100")

		isbn10 = scanner.isbn10
		self.assertEqual(isbn10, "316148410X")

if __name__ == '__main__':
	unittest.main()
