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
"""Test Tomato module."""

from __future__ import absolute_import
import unittest
from mock import patch, MagicMock as Mock

from DIRAC import S_OK, S_ERROR
from ILCDIRAC.Interfaces.API.NewInterface.Applications import Tomato
from Tests.Utilities.GeneralUtils import assertEqualsImproved, assertDiracFailsWith, \
    assertDiracSucceeds

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Interfaces.API.NewInterface.Applications.Tomato'

# pylint: disable=protected-access


class TomatoTestCase(unittest.TestCase):
  """Base class for the Tomato test cases."""

  def setUp(self):
    """set up the objects."""
    self.tom = Tomato({})

  def test_setlib(self):
    self.assertFalse(self.tom._errorDict)
    self.tom.setLibTomato('some_lib.tomato')
    self.assertFalse(self.tom._errorDict)

  def test_setlib_wrongtype(self):
    self.assertFalse(self.tom._errorDict)
    self.tom.setLibTomato({'mydict': True, 'something': 139875})
    assertEqualsImproved(len(self.tom._errorDict['_checkArgs']), 1, self)

  def test_userjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.tom._userjobmodules(module_mock), self)

  def test_prodjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.tom._prodjobmodules(module_mock), self)

  def test_userjobmodules_fails(self):
    with patch('%s._setUserJobFinalization' % MODULE_NAME, new=Mock(return_value=S_OK('something'))),\
        patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_test_err'))):
      assertDiracFailsWith(self.tom._userjobmodules(None),
                            'userjobmodules failed', self)

  def test_prodjobmodules_fails(self):
    with patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_OK('something'))), \
        patch('%s._setOutputComputeDataList' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_other_test_err'))):
      assertDiracFailsWith(self.tom._prodjobmodules(None),
                            'prodjobmodules failed', self)

  def test_checkconsistency(self):
    self.tom.libTomato = None
    assertDiracSucceeds(self.tom._checkConsistency(), self)
    self.tom.libTomato = 'bla'
    assertDiracSucceeds(self.tom._checkConsistency(), self)

  def test_checkconsistency_noversion(self):
    self.tom.version = None
    assertDiracFailsWith(self.tom._checkConsistency(), 'specify which version of marlin to use', self)

  def test_resolvelinkedparams(self):
    step_mock = Mock()
    input_mock = Mock()
    input_mock.getType.return_value = {'abc': False}
    self.tom._linkedidx = 3
    self.tom._jobsteps = [None, None, None, input_mock]
    assertDiracSucceeds(self.tom._resolveLinkedStepParameters(step_mock), self)
    step_mock.setLink.assert_called_once_with('InputFile', {'abc': False}, 'OutputFile')

  def test_resolvelinkedparams_noinputstep(self):
    self.tom._linkedidx = None
    self.tom._inputappstep = []
    assertDiracSucceeds(self.tom._resolveLinkedStepParameters(None), self)

  def test_checkworkflow_app_missing(self):
    self.tom._inputapp = ['some_depdency', 'unavailable_dependency_fail_on_this']
    self.tom._jobapps = ['myjobapp_1', 'some_dependency']
    assertDiracFailsWith(self.tom._checkWorkflowConsistency(), 'job order not correct', self)

  def test_checkworkflow_empty(self):
    self.tom._inputapp = []
    self.tom._jobapps = []
    assertDiracSucceeds(self.tom._checkWorkflowConsistency(), self)

  def test_checkworkflow_success(self):
    self.tom._inputapp = ['some_dependency', 'other_dependencies', 'many_more']
    self.tom._jobapps = ['ignore_me', 'many_more', 'some_dependency', 'other_dependencies']
    assertDiracSucceeds(self.tom._checkWorkflowConsistency(), self)
