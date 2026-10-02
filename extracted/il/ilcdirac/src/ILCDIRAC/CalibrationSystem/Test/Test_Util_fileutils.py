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
"""Unit tests for the CalibrationAgent."""

from __future__ import absolute_import
import filecmp
import os
import unittest

from ILCDIRAC.CalibrationSystem.Utilities.fileutils import binaryFileToString, stringToBinaryFile


__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.CalibrationSystem.Agent.CalibrationAgent'


class TestsFileUtils(unittest.TestCase):
  """Test the utilities for the CalibrationSystem."""

  def setUp(self):
    """Set up the objects."""
    self.targetFile = "targetFile.root"

  def tearDown(self):
    """Tear down the objects."""
    try:
      os.remove(os.path.join(os.getcwd(), self.targetFile))
    except EnvironmentError:
      pass

  def test_binaryToString(self):
    """Test stringToBinaryFile function."""
    filename = os.path.join(os.environ['ILCDIRAC_BASE_FOLDER'], 'Tests', 'Files', 'input.root')
    content = binaryFileToString(filename)
    stringToBinaryFile(content, self.targetFile)
    self.assertTrue(filecmp.cmp(filename, self.targetFile), "Files are not the same any more")
