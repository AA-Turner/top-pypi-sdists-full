# copyright 2003-2013 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of logilab-common.
#
# logilab-common is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option) any
# later version.
#
# logilab-common is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with logilab-common.  If not, see <http://www.gnu.org/licenses/>.
"""
unit tests for module modutils (module manipulation utilities)
"""

import doctest
import sys
import warnings

try:
    __file__
except NameError:
    __file__ = sys.argv[0]

from logilab.common.testlib import TestCase, unittest_main
from logilab.common import modutils

from os import path
from logilab import common

warnings.simplefilter("default", DeprecationWarning)
sys.path.insert(0, path.dirname(__file__))
DATADIR = path.join(path.dirname(__file__), "data")


class ModutilsTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.__common_in_path = common.__path__[0] in sys.path
        if self.__common_in_path:
            sys.path.remove(common.__path__[0])

    def tearDown(self):
        if self.__common_in_path:
            sys.path.insert(0, common.__path__[0])
        super().tearDown()


class modpath_from_file_tc(ModutilsTestCase):
    """given an absolute file path return the python module's path as a list"""

    def test_knownValues_modpath_from_file_1(self):
        self.assertEqual(
            modutils.modpath_from_file(modutils.__file__), ["logilab", "common", "modutils"]
        )

    def test_knownValues_modpath_from_file_2(self):
        self.assertEqual(
            modutils.modpath_from_file(__file__, {path.split(__file__)[0]: "arbitrary.pkg"}),
            ["arbitrary", "pkg", "test_modutils"],
        )

    def test_raise_modpath_from_file_Exception(self):
        self.assertRaises(Exception, modutils.modpath_from_file, "/turlututu")


def load_tests(loader, tests, ignore):
    from logilab.common import modutils

    tests.addTests(doctest.DocTestSuite(modutils))
    return tests


if __name__ == "__main__":
    unittest_main()
