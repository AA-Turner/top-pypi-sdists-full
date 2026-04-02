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
"""Test StdHepSplit module."""

from __future__ import absolute_import
import sys
import unittest
from mock import patch, MagicMock as Mock

from DIRAC import S_OK, S_ERROR
from Tests.Utilities.GeneralUtils import assertEqualsImproved, assertDiracFailsWith, \
    assertDiracSucceeds, assertInImproved

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Interfaces.API.NewInterface.Applications.StdHepSplit'

# pylint: disable=protected-access


class StdHepSplitTestCase(unittest.TestCase):
  """Base class for the StdHepSplit test cases."""

  def setUp(self):
    """set up the objects."""
    # Mock out modules that spawn other threads
    mocked_modules = {'DIRAC.DataManagementSystem.Client.DataManager': Mock()}
    self.module_patcher = patch.dict(sys.modules, mocked_modules)
    self.module_patcher.start()
    from ILCDIRAC.Interfaces.API.NewInterface.Applications import StdHepSplit
    self.shs = StdHepSplit({})

  def tearDown(self):
    self.module_patcher.stop()

  def test_userjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.shs._userjobmodules(module_mock), self)

  def test_prodjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.shs._prodjobmodules(module_mock), self)

  def test_userjobmodules_fails(self):
    with patch('%s._setUserJobFinalization' % MODULE_NAME, new=Mock(return_value=S_OK('something'))),\
        patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_test_err'))):
      assertDiracFailsWith(self.shs._userjobmodules(None),
                            'userjobmodules failed', self)

  def test_prodjobmodules_fails(self):
    with patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_OK('something'))), \
        patch('%s._setOutputComputeDataList' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_other_test_err'))):
      assertDiracFailsWith(self.shs._prodjobmodules(None),
                            'prodjobmodules failed', self)

  def test_checkproductionmeta(self):
    self.shs.numberOfEventsPerFile = 12348
    meta_dict = {'NumberOfEvents': True}
    assertDiracSucceeds(self.shs.checkProductionMetaData(meta_dict), self)
    assertEqualsImproved({'NumberOfEvents': 12348}, meta_dict, self)

  def test_checkproductionmeta_changenothing(self):
    meta_dict = {'myentry': True, 'other_entry': 81943, 'other': 'ae8fj', False: 1}
    assertDiracSucceeds(self.shs.checkProductionMetaData(meta_dict), self)
    assertEqualsImproved({'myentry': True, 'other_entry': 81943, 'other': 'ae8fj', False: 1},
                          meta_dict, self)

  def test_resolvelinkedstepparams(self):
    instance_mock = Mock()
    step_mock = Mock()
    step_mock.getType.return_value = 'abc'
    self.shs._inputappstep = None
    self.shs._jobsteps = ['', '', step_mock]
    self.shs._linkedidx = 2
    assertDiracSucceeds(self.shs._resolveLinkedStepParameters(instance_mock), self)
    instance_mock.setLink.assert_called_once_with('InputFile', 'abc', 'OutputFile')

  def test_resolvelinkedstepparams_nothing_happens(self):
    instance_mock = Mock()
    self.shs._inputappstep = None
    self.shs._jobsteps = None
    self.shs._linkedidx = ['abc']
    assertDiracSucceeds(self.shs._resolveLinkedStepParameters(instance_mock), self)
    self.assertFalse(instance_mock.setLink.called)

  def test_checkconsistency(self):
    self.shs._jobtype = 'notUser'
    self.shs.OutputFile = None
    assertDiracSucceeds(self.shs._checkConsistency(), self)
    assertInImproved({'outputFile': '@{OutputFile}', 'outputPath': '@{OutputPath}',
                        'outputDataSE': '@{OutputSE}'}, self.shs._listofoutput, self)

  def test_checkconsistency_userjob(self):
    job_mock = Mock()
    job_mock.datatype = 'testDatatype'
    self.shs._job = job_mock
    self.shs._jobtype = 'User'
    self.shs.OutputFile = None
    assertDiracSucceeds(self.shs._checkConsistency(), self)
    self.assertFalse(self.shs.outputFile)
    assertEqualsImproved(self.shs.datatype, 'testDatatype', self)
