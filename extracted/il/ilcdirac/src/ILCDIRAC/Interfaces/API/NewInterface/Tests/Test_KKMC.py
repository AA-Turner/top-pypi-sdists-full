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
"""Test KKMC module."""

from __future__ import print_function
from __future__ import absolute_import
import linecache
import unittest
from mock import patch, MagicMock as Mock
from mock import mock_open
from mock import mock as mock_module
from parameterized import parameterized
import six

from DIRAC import gLogger, S_OK, S_ERROR
from ILCDIRAC.Interfaces.API.NewInterface.Applications import KKMC
from Tests.Utilities.GeneralUtils import assertEqualsImproved, assertDiracFailsWith, \
    assertDiracSucceeds

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Interfaces.API.NewInterface.Applications.KKMC'
BUILTIN_NAME = 'builtins' if six.PY3 else '__builtin__'

gLogger.setLevel("DEBUG")
gLogger.showHeaders(True)

# pylint: disable=protected-access


class KKMCTestCase(unittest.TestCase):
  """Base class for the KKMC test cases."""

  @classmethod
  def setUpClass(cls):
    """Load the Application file into the linecache to prevent exceptions when mocking the builtin open."""
    from ILCDIRAC.Interfaces.API.NewInterface import Application
    for fName in [Application.__file__, mock_module.__file__]:
      if fName.endswith(('.pyc', '.pyo')):
        fName = fName[:-1]
      linecache.getlines(fName)

  @classmethod
  def tearDownClass(cls):
    """Remove all entries from linecache because we mock builtin open."""
    linecache.clearcache()

  def setUp(self):
    """set up the objects."""
    self.kkmc = KKMC({})
    self.kkmc._jobtype = 'User'
    self.kkmc._ops = Mock(name='OpsMock')

  def test_setEvtType(self):
    self.assertFalse(self.kkmc._errorDict)
    self.kkmc.setEvtType('Mu')
    self.assertFalse(self.kkmc._errorDict)
    assertEqualsImproved(self.kkmc.eventType, 'Mu', self)

  @parameterized.expand([(15, False, '_checkArgs'),
                         ('Mu', True, 'setEvtType'),
                         ])
  def test_setEvtType_fail(self, evtType, addedToJob, errorMessage):
    self.assertFalse(self.kkmc._errorDict)
    self.kkmc.addedtojob = addedToJob
    self.kkmc.setEvtType(evtType)
    self.assertIn(errorMessage, self.kkmc._errorDict)

  @patch('os.path.isfile', new=Mock(return_value=True))
  @patch('%s.open' % BUILTIN_NAME, mock_open(read_data='configFile content'))
  def test_setConfigFile(self):
    """Test setConfigFile."""
    self.assertFalse(self.kkmc._errorDict)
    self.kkmc.setConfigFile('/some/path/configFile.input')
    self.assertFalse(self.kkmc._errorDict)
    assertEqualsImproved(self.kkmc.kkmcConfigFile, 'configFile content', self)

  @patch('os.path.isfile', new=Mock(return_value=False))
  def test_setConfigFile_fail(self):
    """Test setConfigFile."""
    self.assertFalse(self.kkmc._errorDict)
    assertDiracFailsWith(self.kkmc.setConfigFile('/some/path/configFile.input'), 'KKMC config file does not exist!', self)

  def test_checkworkflow_app_missing(self):
    self.kkmc._inputapp = ['some_depdency', 'unavailable_dependency_fail_on_this']
    self.kkmc._jobapps = ['myjobapp_1', 'some_dependency']
    assertDiracFailsWith(self.kkmc._checkWorkflowConsistency(), 'job order not correct', self)

  def test_checkworkflow_empty(self):
    self.kkmc._inputapp = []
    self.kkmc._jobapps = []
    assertDiracSucceeds(self.kkmc._checkWorkflowConsistency(), self)

  def test_setrandomseed(self):
    self.assertFalse(self.kkmc._errorDict)
    self.kkmc.setRandomSeed(89421)
    self.assertFalse(self.kkmc._errorDict)
    assertEqualsImproved(self.kkmc.randomSeed, 89421, self)

  def test_setrandomseed_fails(self):
    self.assertFalse(self.kkmc._errorDict)
    self.kkmc.setRandomSeed(['abc'])
    self.assertIn('_checkArgs', self.kkmc._errorDict)

  def test_userjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.kkmc._userjobmodules(module_mock), self)

  def test_prodjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.kkmc._prodjobmodules(module_mock), self)

  def test_userjobmodules_fails(self):
    with patch('%s._setUserJobFinalization' % MODULE_NAME, new=Mock(return_value=S_OK('something'))),\
            patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_test_err'))):
      assertDiracFailsWith(self.kkmc._userjobmodules(None),
                           'userjobmodules failed', self)

  def test_prodjobmodules_fails(self):
    with patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_OK('something'))), \
            patch('%s._setOutputComputeDataList' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_other_test_err'))):
      assertDiracFailsWith(self.kkmc._prodjobmodules(None),
                           'prodjobmodules failed', self)

  def test_checkconsistency_configFile(self):
    self.kkmc.version = 'LCG_97a_FCC_4'
    self.kkmc.kkmcConfigFile = 'kkmc_steer.input'
    assertDiracSucceeds(self.kkmc._checkConsistency(Mock()), self)

  def test_checkconsistency_parameters(self):
    self.kkmc.version = 'LCG_97a_FCC_4'
    self.kkmc.kkmcConfigFile = None
    self.kkmc.eventType = 'Mu'
    self.kkmc.energy = '91.2'
    self.kkmc.numberOfEvents = '1000'
    self.kkmc.outputFile = 'kkmu_1000.LHE'
    assertDiracSucceeds(self.kkmc._checkConsistency(Mock()), self)

  def test_checkconsistency_noVersion(self):
    self.kkmc.version = None
    assertDiracFailsWith(self.kkmc._checkConsistency(Mock()), 'No version found!', self)

  def test_checkconsistency_notuserjob(self):
    self.kkmc.version = 'LCG_97a_FCC_4'
    self.kkmc._jobtype = 'not a User'
    assertDiracSucceeds(self.kkmc._checkConsistency(Mock()), self)

  def test_checkconsistency_noConfigFile(self):
    self.kkmc.version = 'LCG_97a_FCC_4'
    self.kkmc.kkmcConfigFile = None
    assertDiracFailsWith(self.kkmc._checkConsistency(Mock()), 'No config file set!', self)

  def test_checkconsistency_noEventType(self):
    self.kkmc.version = 'LCG_97a_FCC_4'
    self.kkmc.kkmcConfigFile = None
    self.kkmc.eventType = None
    self.kkmc.energy = 91.2
    self.kkmc.numberOfEvents = 1000
    self.kkmc.outputFile = 'kkmu_1000.LHE'
    assertDiracFailsWith(self.kkmc._checkConsistency(Mock()), 'No event type set!', self)

  def test_checkconsistency_noEnergy(self):
    self.kkmc.version = 'LCG_97a_FCC_4'
    self.kkmc.kkmcConfigFile = None
    self.kkmc.eventType = 'Mu'
    self.kkmc.energy = None
    self.kkmc.numberOfEvents = 1000
    self.kkmc.outputFile = 'kkmu_1000.LHE'
    assertDiracFailsWith(self.kkmc._checkConsistency(Mock()), 'No energy set!', self)

  def test_checkconsistency_noNumberOfEvents(self):
    self.kkmc.version = 'LCG_97a_FCC_4'
    self.kkmc.kkmcConfigFile = None
    self.kkmc.eventType = 'Mu'
    self.kkmc.energy = 91.2
    self.kkmc.numberOfEvents = None
    self.kkmc.outputFile = 'kkmu_1000.LHE'
    assertDiracFailsWith(self.kkmc._checkConsistency(Mock()), 'No number of events set!', self)

  def test_checkconsistency_noOutputFile(self):
    self.kkmc.version = 'LCG_97a_FCC_4'
    self.kkmc.kkmcConfigFile = None
    self.kkmc.eventType = 'Mu'
    self.kkmc.energy = 91.2
    self.kkmc.numberOfEvents = 1000
    self.kkmc.outputFile = None
    assertDiracFailsWith(self.kkmc._checkConsistency(Mock()), 'No output file set!', self)

  def test_checkconsistency_badseed(self):
    self.kkmc.version = 'LCG_97a_FCC_4'
    self.kkmc.kkmcConfigFile = None
    self.kkmc.energy = 91.2
    self.kkmc.numberOfEvents = 1000
    self.kkmc.outputFile = 'kkmc_1000.LHE'
    self.kkmc.eventType = 'Mu'
    self.kkmc.randomSeed = -2
    assertDiracFailsWith(self.kkmc._checkConsistency(Mock()), 'Random Seed has to be equal or greater than -1', self)

    self.kkmc._jobtype = 'User'


def runTests():
  """Runs our tests."""
  suite = unittest.defaultTestLoader.loadTestsFromTestCase(KKMCTestCase)
  testResult = unittest.TextTestRunner(verbosity=2).run(suite)
  print(testResult)


if __name__ == '__main__':
  runTests()
