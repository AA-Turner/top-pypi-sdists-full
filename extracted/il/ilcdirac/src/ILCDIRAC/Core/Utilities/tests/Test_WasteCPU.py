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
"""Test WasteCPU."""

from __future__ import absolute_import
import unittest
from mock import MagicMock as Mock, patch

from ILCDIRAC.Core.Utilities.WasteCPU import wasteCPUCycles

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Core.Utilities.WasteCPU'


class WasteCPUTest(unittest.TestCase):
  """Test the WasteCPU."""

  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_success(self):
    """wasteCPUCycles suceeeds to waste............................................................."""
    self.assertTrue(wasteCPUCycles(1)['OK'])

  def test_fail1(self):
    """wasteCPUCycles fails 1......................................................................."""
    with patch("%s.log" % MODULE_NAME, new=Mock(side_effect=ValueError("MockedValue"))):
      self.assertFalse(wasteCPUCycles(1)['OK'])
      self.assertIn("MockedValue", wasteCPUCycles(1)['Message'])

  def test_fail2(self):
    """wasteCPUCycles fails 2......................................................................."""
    with patch("%s.log" % MODULE_NAME, new=Mock(side_effect=RuntimeError("MockedError"))):
      self.assertFalse(wasteCPUCycles(1)['OK'])
      self.assertIn("OtherException", wasteCPUCycles(1)['Message'])
      self.assertIn("RuntimeError('MockedError'", wasteCPUCycles(1)['Message'])


if __name__ == "__main__":
  SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(WasteCPUTest)
  TESTRESULT = unittest.TextTestRunner(verbosity=2).run(SUITE)
