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
"""Test the Core Confogiration."""

from __future__ import absolute_import
import unittest
from mock import MagicMock as Mock
from ILCDIRAC.Core.Utilities import Configuration

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Core.Utilities.Configuration'


class TestCheckConf(unittest.TestCase):
  """Test the Configuration Utilities Module."""

  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_getOptionValue(self):
    ops = Mock()

    def getValueMock(path, defVal):
      return {"/base/myOp": "baseVal",
              "/base/foo/myOp": "fooVal",
              "/base/foo/bar/myOp": "barVal",
              "/base/foo/bar/baz/myOp": "bazVal",
             }.get(path, defVal)

    ops.getValue.side_effect = getValueMock

    value = Configuration.getOptionValue(ops, "/base", "myOp", "defVal", ['foo', 'bar', 'baz'])
    self.assertEqual(value, 'bazVal')

    value = Configuration.getOptionValue(ops, "/base", "myOp", "defVal", ['foo', 'bar', 'baz2'])
    self.assertEqual(value, 'barVal')

    value = Configuration.getOptionValue(ops, "/base", "myOp", "defVal", ['foo', 'bar2', 'baz'])
    self.assertEqual(value, 'fooVal')

    value = Configuration.getOptionValue(ops, "/base", "myOp", "defVal", ['args', '', 'kwargs'])
    self.assertEqual(value, 'baseVal')

    value = Configuration.getOptionValue(ops, "/base2", "myOp", "defVal", ['args', '', 'kwargs'])
    self.assertEqual(value, 'defVal')
