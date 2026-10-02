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
"""Test _Root module."""

from __future__ import absolute_import
import sys
import unittest
from mock import patch, MagicMock as Mock

from DIRAC import S_OK, S_ERROR
from Tests.Utilities.GeneralUtils import assertDiracFailsWith, assertDiracSucceeds

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Interfaces.API.NewInterface.Applications._Root'

# pylint: disable=protected-access


class RootTestCase(unittest.TestCase):
  """Base class for the _Root test cases."""

  def setUp(self):
    """set up the objects."""
    # Mock out modules that spawn other threads
    mocked_modules = {'DIRAC.DataManagementSystem.Client.DataManager': Mock()}
    self.module_patcher = patch.dict(sys.modules, mocked_modules)
    self.module_patcher.start()
    from ILCDIRAC.Interfaces.API.NewInterface.Applications import _Root
    self.root = _Root({})

  def tearDown(self):
    self.module_patcher.stop()

  def test_userjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.root._userjobmodules(module_mock), self)

  def test_prodjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.root._prodjobmodules(module_mock), self)

  def test_userjobmodules_fails(self):
    with patch('%s._setUserJobFinalization' % MODULE_NAME, new=Mock(return_value=S_OK('something'))),\
        patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_test_err'))):
      assertDiracFailsWith(self.root._userjobmodules(None),
                            'userjobmodules failed', self)

  def test_prodjobmodules_fails(self):
    with patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_OK('something'))), \
        patch('%s._setOutputComputeDataList' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_other_test_err'))):
      assertDiracFailsWith(self.root._prodjobmodules(None),
                            'prodjobmodules failed', self)

  def test_setmacro(self):
    assertDiracFailsWith(self.root.setMacro(None), 'not allowed here', self)

  def test_resolvelinkedstepparams(self):
    instance_mock = Mock()
    step_mock = Mock()
    step_mock.getType.return_value = 'abc'
    self.root._inputappstep = None
    self.root._jobsteps = ['', '', step_mock]
    self.root._linkedidx = 2
    assertDiracSucceeds(self.root._resolveLinkedStepParameters(instance_mock), self)
    instance_mock.setLink.assert_called_once_with('InputFile', 'abc', 'OutputFile')

  def test_resolvelinkedstepparams_nothing_happens(self):
    instance_mock = Mock()
    self.root._inputappstep = None
    self.root._jobsteps = None
    self.root._linkedidx = ['abc']
    assertDiracSucceeds(self.root._resolveLinkedStepParameters(instance_mock), self)
    self.assertFalse(instance_mock.setLink.called)

  def test_checkconsistency_noscript(self):
    self.root.script = None
    assertDiracFailsWith(self.root._checkConsistency(), 'script or macro not defined', self)

  def test_checkconsistency_noversion(self):
    self.root.script = 1
    self.root.version = None
    assertDiracFailsWith(self.root._checkConsistency(), 'you need to specify the root version', self)
