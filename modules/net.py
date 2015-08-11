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

import sys, urllib2

CHUNK = 16 * 1024

class Download(object):

    def __init__(self, url, file_path):
        self.url = url
        self.file_path = file_path
        self.status = False
        self.error_message = None

class Downloader(object):

    def __init__(self, download):
        self.download = download

    def run(self):

        try:

            # Request the file
            request = urllib2.Request(self.download.url)
            response = urllib2.urlopen(request)

            # Download the file
            if response.getcode() == 200:
                with open(self.download.file_path, 'wb') as file:
                    while True:
                        chunk = response.read(CHUNK)
                        if not chunk: break
                        file.write(chunk)

            # Download is Ok
            self.download.status = True

        except urllib2.URLError as e:
            self.download.error_message = e.reason

        return self.download
