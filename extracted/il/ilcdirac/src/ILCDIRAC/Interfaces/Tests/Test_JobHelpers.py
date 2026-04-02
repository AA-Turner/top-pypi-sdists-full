#
# Copyright (c) 2009-2022 CERN. All rights nots expressly granted are
# reserved.
#
# This file is part of iLCDirac
# (see ilcdirac.cern.ch, contact: ilcdirac-support@cern.ch).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# In applying this licence, CERN does not waive the privileges and
# immunities granted to it by virtue of its status as an
# Intergovernmental Organization or submit itself to any jurisdiction.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""Tests for Interfaces.Utilities.JobHelpers."""

from __future__ import print_function
from __future__ import absolute_import
import unittest

from ILCDIRAC.Interfaces.Utilities import JobHelpers
import six

__RCSID__ = "$Id$"


class TestJobHelpers(unittest.TestCase):
  """tests for the JobHelper utilities."""

  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_getValue_list_int(self):
    value = ["2", 3]
    ret = JobHelpers.getValue(value, int, int)
    self.assertIsInstance(ret, int)
    self.assertEqual(ret, int(value[0]))

  def test_getValue_int(self):
    value = 2
    ret = JobHelpers.getValue(value, int, int)
    self.assertIsInstance(ret, int)
    self.assertEqual(ret, int(value))

  def test_getValue_int_none(self):
    value = "2"
    ret = JobHelpers.getValue(value, int, None)
    self.assertIsInstance(ret, int)
    self.assertEqual(ret, int(value))

  def test_getValue_string_none(self):
    value = ["someString", "someOther"]
    ret = JobHelpers.getValue(value, str, six.string_types)
    self.assertIsInstance(ret, six.string_types)
    self.assertEqual(ret, value[0])


def runTests():
  """Runs our tests."""
  suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestJobHelpers)
  testResult = unittest.TextTestRunner(verbosity=2).run(suite)
  print(testResult)


if __name__ == '__main__':
  runTests()

  # if isinstance( compatmeta['NumberOfEvents'], list ):
  #   self.nbevts = int(compatmeta['NumberOfEvents'][0])
  # else:
  #   #type(compatmeta['NumberOfEvents']) in types.StringTypes:
  #   self.nbevts = int(compatmeta['NumberOfEvents'])
