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
"""Unit tests for the Calibration application."""

from __future__ import print_function
#  import unittest
#  import pytest
#  import os
#  import shutil
#  import time
#  from datetime import datetime
#  from datetime import timedelta
#  from xml.etree import ElementTree as et
#  from shutil import copyfile
#  from DIRAC import S_OK, S_ERROR
#  from mock import patch
#  from mock import MagicMock as Mock
from __future__ import absolute_import
from ILCDIRAC.Interfaces.API.NewInterface.Applications.Calibration import Calibration

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Interfaces.API.NewInterface.Applications.Calibration'


def test_init():
  """Test initialization."""
  calApp = Calibration()
  assert calApp._modulename == "Calibration"
  assert calApp.appname == "marlin"


def test_setCalibrationID():
  """Test setCalibrationID function."""
  calApp = Calibration()

  # correct input
  arg = 3
  assert not calApp._errorDict
  calApp.setCalibrationID(arg)
  assert not calApp._errorDict

  # wrong input
  arg = 'some string'
  calApp.setCalibrationID(arg)
  assert calApp._errorDict


def test_setWorkerID():
  """Test setCalibrationID function."""
  calApp = Calibration()

  # correct input
  arg = 3
  assert not calApp._errorDict
  calApp.setWorkerID(arg)
  assert not calApp._errorDict

  # wrong input
  arg = 'some string'
  calApp.setWorkerID(arg)
  assert calApp._errorDict
