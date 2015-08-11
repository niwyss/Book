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

from string import maketrans
import string
import unicodedata
import sys
import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFSyntaxError
from cStringIO import StringIO
import isbnlib

class PDFScanner(object):

	def __init__(self, pdf):
		self.pdf = pdf
		self.isbn10 = None
		self.isbn13 = None

	# Scan the pdf
	def extractISBN(self):

		isbn = None;

		rsrcmgr = PDFResourceManager()
		retstr = StringIO()
		device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams())
		interpreter = PDFPageInterpreter(rsrcmgr, device)

		for page in PDFPage.get_pages(self.pdf, set(), maxpages=0, password="",caching=True, check_extractable=True):

			# Get the text from the page
			interpreter.process_page(page)
			text = retstr.getvalue()
			retstr.truncate(0)

			# Extract ISBN
			isbn = self.searchCodeInPage(text)

			if isbn:
				break

		device.close()
		retstr.close()

		# Convert to ISBN 10 and 13
		if isbnlib.is_isbn10(isbn):
			self.isbn10 = isbn
			self.isbn13 = isbnlib.to_isbn13(self.isbn10)
		elif isbnlib.is_isbn13(isbn):
			self.isbn13 = isbn
			self.isbn10 = isbnlib.to_isbn10(self.isbn13)

	# Search keyword in a page
	def searchCodeInPage(self, page):

		code = "";

		# Prepare the page
		page = page.upper()

		keys = ['ISBN-13', 'ISBN']

		# Try to find the key
		for key in keys:
			position = page.find(key)
			if position > 0:

				# Extract data
				code = page[position + len(key):position + 35]

				# Clean data
				code = code.strip()
				code = code.partition("\n")[0]
				code = self.clean(code)
				code = code[0:13]

				if code:
					break

		return code

	# Clean string from chars other than digits
	def clean(self, phrase):

		# Convert Unicode to String
		if isinstance(phrase, unicode):
			phrase = unicodedata.normalize('NFKD', phrase).encode('ascii','ignore')

		# Delete all chars but the digits
		allchars = ''.join(chr(i) for i in xrange(256))
		identity = string.maketrans('', '')
		nondigits = allchars.translate(identity, string.digits)
		phrase = phrase.translate(identity, nondigits)

		return phrase
