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

import sys, os, json, logging, time
import database
from database import Common

PARAMETERS_FILE_NAME = 'parameters.json'

class Configuration(object):

    def __init__(self):

        try:

            parameters_path = self.__get_current_path() + PARAMETERS_FILE_NAME

            data = open(parameters_path, 'r')
            parameters = json.loads(data.read())
            data.close()

            self.googlebook_key = parameters["googlebook.key"]
            self.library_path = parameters["library.path"]
            self.database_path = parameters["database.path"]
            self.tmp_path = parameters["tmp.path"]
            self.log_path = parameters["log.path"]
            self.error_path = parameters["error.path"]

        except Exception, e:
            print "error: unabled to get the configuration from parameters file [{0}]".format(parameters_path)
            sys.exit(0)

    def __repr__(self):
        return (
            "<Configuration('{self.googlebook_key}', '{self.library_path}', "
            "'{self.database_path}', '{self.tmp_path}')>".format(self=self)
        )

    def __get_current_path(self):

        # Get the path to command from where she's called
        path = "."
        if os.path.islink(sys.argv[0]):
            path = os.readlink(sys.argv[0])[:-5]
        else:
            path =  sys.argv[0][:-5]
        path = os.path.abspath(path) + os.sep

        return path

# Init configuration
configuration = Configuration()

# Init logging
logger = logging.getLogger("book")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler(configuration.log_path)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Init the connection to the database
database.common = Common(configuration.database_path)


def clean_folder(folder_path):
    try:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    except Exception, e:
        print "book: unabled to clean folder []".format(folder_path)
        sys.exit(0)
