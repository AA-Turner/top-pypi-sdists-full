#!/usr/local/env python
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
"""Test CheckWNs module."""

from __future__ import absolute_import
import unittest
from mock import patch, MagicMock as Mock

from DIRAC import S_OK, S_ERROR
from ILCDIRAC.Interfaces.API.NewInterface.Applications import CheckWNs
from Tests.Utilities.GeneralUtils import assertDiracFailsWith, assertDiracSucceeds

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Interfaces.API.NewInterface.Applications.CheckWNs'

# pylint: disable=protected-access


class CheckWNsTestCase(unittest.TestCase):
  """Base class for the Pythia test cases."""

  def setUp(self):
    """set up the objects."""
    self.cwn = CheckWNs({})

  def test_userjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.cwn._userjobmodules(module_mock), self)

  def test_prodjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.cwn._prodjobmodules(module_mock), self)

  def test_userjobmodules_fails(self):
    with patch('%s._setUserJobFinalization' % MODULE_NAME, new=Mock(return_value=S_OK('something'))),\
        patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_test_err'))):
      assertDiracFailsWith(self.cwn._userjobmodules(None),
                            'userjobmodules failed', self)

  def test_prodjobmodules_fails(self):
    with patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_test_err'))):
      assertDiracFailsWith(self.cwn._prodjobmodules(None),
                            'prodjobmodules failed', self)

  def test_checkconsistency(self):
    assertDiracSucceeds(self.cwn._checkConsistency(), self)

  def test_checkconsistency_nojob(self):
    assertDiracSucceeds(self.cwn._checkConsistency(None), self)

  def test_checkconsistency_mock_job(self):
    assertDiracSucceeds(self.cwn._checkConsistency(Mock()), self)
