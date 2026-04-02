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
"""Test SLCIOSplit module."""

from __future__ import absolute_import
import unittest
from mock import patch, MagicMock as Mock

from DIRAC import S_OK, S_ERROR
from ILCDIRAC.Interfaces.API.NewInterface.Applications import SLCIOSplit
from Tests.Utilities.GeneralUtils import assertEqualsImproved, assertDiracFailsWith, \
    assertDiracSucceeds, assertInImproved

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Interfaces.API.NewInterface.Applications.SLCIOSplit'

# pylint: disable=protected-access


class SLCIOSplitTestCase(unittest.TestCase):
  """Base class for the SLCIOSplit test cases."""

  def setUp(self):
    """set up the objects."""
    self.ssp = SLCIOSplit({})

  def test_setnumberevtsperfile(self):
    self.ssp.setNumberOfEventsPerFile(987124)
    assertEqualsImproved(self.ssp.numberOfEventsPerFile, 987124, self)
    self.assertFalse(self.ssp._errorDict)

  def test_setnumberevtsperfile_fails(self):
    self.ssp.setNumberOfEventsPerFile({'asf': True})
    assertInImproved('_checkArgs', self.ssp._errorDict, self)

  def test_userjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.ssp._userjobmodules(module_mock), self)

  def test_prodjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.ssp._prodjobmodules(module_mock), self)

  def test_userjobmodules_fails(self):
    with patch('%s._setUserJobFinalization' % MODULE_NAME, new=Mock(return_value=S_OK('something'))),\
        patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_test_err'))):
      assertDiracFailsWith(self.ssp._userjobmodules(None),
                            'userjobmodules failed', self)

  def test_prodjobmodules_fails(self):
    with patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_OK('something'))), \
        patch('%s._setOutputComputeDataList' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_other_test_err'))):
      assertDiracFailsWith(self.ssp._prodjobmodules(None),
                            'prodjobmodules failed', self)

  def test_checkworkflowconsistency(self):
    self.ssp._checkWorkflowConsistency()
    # pylint: disable=redundant-unittest-assert
    self.assertTrue(True)

  def test_resolvelinkedstepparams(self):
    instance_mock = Mock()
    step_mock = Mock()
    step_mock.getType.return_value = 'abc'
    self.ssp._inputappstep = None
    self.ssp._jobsteps = ['', '', step_mock]
    self.ssp._linkedidx = 2
    assertDiracSucceeds(self.ssp._resolveLinkedStepParameters(instance_mock), self)
    instance_mock.setLink.assert_called_once_with('InputFile', 'abc', 'OutputFile')

  def test_resolvelinkedstepparams_nothing_happens(self):
    instance_mock = Mock()
    self.ssp._inputappstep = None
    self.ssp._jobsteps = None
    self.ssp._linkedidx = ['abc']
    assertDiracSucceeds(self.ssp._resolveLinkedStepParameters(instance_mock), self)
    self.assertFalse(instance_mock.setLink.called)

  def test_checkconsistency(self):
    job_mock = Mock()
    job_mock.datatype = 'Mock_type_data'
    job_mock.detector = 'testdetector123'
    self.ssp._job = job_mock
    self.ssp._jobtype = 'notUser'
    self.ssp.OutputFile = None
    assertDiracSucceeds(self.ssp._checkConsistency(), self)
    assertInImproved({'outputFile': '@{OutputFile}', 'outputPath': '@{OutputPath}',
                        'outputDataSE': '@{OutputSE}'}, self.ssp._listofoutput, self)
    assertEqualsImproved((self.ssp.datatype, self.ssp.detectortype),
                          ('Mock_type_data', 'testdetector123'), self)

  def test_checkconsistency_userjob(self):
    self.ssp._jobtype = 'User'
    self.ssp.OutputFile = None
    assertDiracSucceeds(self.ssp._checkConsistency(), self)
    self.assertFalse(self.ssp.outputFile)
