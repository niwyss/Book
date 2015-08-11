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
import database, utils
from database import Common

def work():

    utils.logger.info("start init command")

    # Create the base
    database.common.create()

    # Create the library
    os.makedirs(utils.configuration.library_path, mode=0777)

    # Create tmp folder
    os.makedirs(utils.configuration.tmp_path, mode=0777)

    # Create error folder
    os.makedirs(utils.configuration.error_path, mode=0777)
