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
"""Test the Core Splitting Module."""

from __future__ import absolute_import
import unittest
from ILCDIRAC.Core.Utilities.Splitting import addJobIndexToFilename

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Core.Utilities.Splitting'


class Splittingtest(unittest.TestCase):
  """Test the Splitting."""

  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_Splitting(self):
    fileIn = "output_%n.slcio"
    jobIndex = 123
    self.assertEqual("output_123.slcio", addJobIndexToFilename(fileIn, jobIndex))

    fileIn = "output_%n.slcio"
    jobIndex = 0
    self.assertEqual("output_0.slcio", addJobIndexToFilename(fileIn, jobIndex))

    fileIn = "output.slcio"
    jobIndex = 123
    self.assertEqual("output_123.slcio", addJobIndexToFilename(fileIn, jobIndex))

    fileIn = "output"
    jobIndex = 123
    self.assertEqual("output_123", addJobIndexToFilename(fileIn, jobIndex))

    fileIn = "/ilc/user/t/tester/some/folder/output"
    jobIndex = 123
    self.assertEqual("/ilc/user/t/tester/some/folder/output_123", addJobIndexToFilename(fileIn, jobIndex))

    fileIn = "/ilc/user/t/tester/some/folder/%n/output"
    jobIndex = 123
    self.assertEqual("/ilc/user/t/tester/some/folder/123/output", addJobIndexToFilename(fileIn, jobIndex))
