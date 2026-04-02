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
"""Test Whizard2 module."""

from __future__ import print_function
from __future__ import absolute_import
import unittest
from mock import patch, MagicMock as Mock

from parameterized import parameterized
import six

from DIRAC import gLogger, S_OK, S_ERROR
from ILCDIRAC.Interfaces.API.NewInterface.Applications import Whizard2
from Tests.Utilities.FileUtils import mock_open_few
from Tests.Utilities.GeneralUtils import assertEqualsImproved, assertDiracFailsWith, \
    assertDiracSucceeds


__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Interfaces.API.NewInterface.Applications.Whizard2'
BUILTIN_NAME = 'builtins' if six.PY3 else '__builtin__'

gLogger.setLevel("DEBUG")
gLogger.showHeaders(True)

# pylint: disable=protected-access


class Whizard2TestCase(unittest.TestCase):
  """Base class for the Whizard2 test cases."""

  def setUp(self):
    """set up the objects."""
    self.whiz = Whizard2({})
    self.whiz._ops = Mock(name='OpsMock')

  def test_setrandomseed(self):
    self.assertFalse(self.whiz._errorDict)
    self.whiz.setRandomSeed(89421)
    self.assertFalse(self.whiz._errorDict)
    assertEqualsImproved(self.whiz.randomSeed, 89421, self)

  def test_setrandomseed_fails(self):
    self.assertFalse(self.whiz._errorDict)
    self.whiz.setRandomSeed(['abc'])
    self.assertIn('_checkArgs', self.whiz._errorDict)

  def test_setEvtType(self):
    self.assertFalse(self.whiz._errorDict)
    self.whiz.setEvtType('ee->ff')
    self.assertFalse(self.whiz._errorDict)
    assertEqualsImproved(self.whiz.eventType, 'ee->ff', self)

  @parameterized.expand([(15, False, '_checkArgs'),
                         ('tt', True, 'setEvtType'),
                         ])
  def test_setEvtType_fail(self, evtType, addedToJob, errorMessage):
    self.assertFalse(self.whiz._errorDict)
    self.whiz.addedtojob = addedToJob
    self.whiz.setEvtType(evtType)
    self.assertIn(errorMessage, self.whiz._errorDict)

  @parameterized.expand([(True,), (False,)])
  def test_setSinFile(self, raw):
    """Test setSinFile."""
    self.assertFalse(self.whiz._errorDict)
    with patch('os.path.isfile', new=Mock(return_value=True)), \
         patch('%s.open' % BUILTIN_NAME, mock_open_few({'/some/path': 'process decay_proc = "A", "A" => "b", "B"'})):
      if raw:
        self.whiz.setSinFile('/some/path', raw=True)
      else:
        self.whiz.setSinFile('/some/path', raw=False)
    self.assertFalse(self.whiz._errorDict)
    assertEqualsImproved(self.whiz.whizard2SinFile, 'process decay_proc = "A", "A" => "b", "B"', self)
    assertEqualsImproved(self.whiz.whizard2RawSin, raw, self)

  @parameterized.expand([(False, 'does not exist', ''),
                         (True, 'Do not set n_events', '\n n_events'),
                         (True, 'Do not set seed', '\n seed'),
                         (True, 'Do not call "simulate ()"', '\n simulate( decay_proc)'),
                         ])
  def test_setSinFile_fails2(self, exists, errorMessage, extra):
    with patch('os.path.isfile', new=Mock(return_value=exists)), \
        patch('%s.open' % BUILTIN_NAME,
              mock_open_few({'/some/path': 'process decay_proc = "A", "A" => "b", "B"' + extra})):
      assertDiracFailsWith(self.whiz.setSinFile('/some/path'), errorMessage, self)

  def test_checkworkflow_app_missing(self):
    self.whiz._inputapp = ['some_depdency', 'unavailable_dependency_fail_on_this']
    self.whiz._jobapps = ['myjobapp_1', 'some_dependency']
    assertDiracFailsWith(self.whiz._checkWorkflowConsistency(), 'job order not correct', self)

  def test_checkworkflow_empty(self):
    self.whiz._inputapp = []
    self.whiz._jobapps = []
    assertDiracSucceeds(self.whiz._checkWorkflowConsistency(), self)

  def test_userjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.whiz._userjobmodules(module_mock), self)

  def test_prodjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.whiz._prodjobmodules(module_mock), self)

  def test_userjobmodules_fails(self):
    with patch('%s._setUserJobFinalization' % MODULE_NAME, new=Mock(return_value=S_OK('something'))),\
        patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_test_err'))):
      assertDiracFailsWith(self.whiz._userjobmodules(None),
                            'userjobmodules failed', self)

  def test_prodjobmodules_fails(self):
    with patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_OK('something'))), \
        patch('%s._setOutputComputeDataList' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_other_test_err'))):
      assertDiracFailsWith(self.whiz._prodjobmodules(None),
                            'prodjobmodules failed', self)

  def test_checkconsistency(self):
    self.whiz.version = '2.3.1'
    self.whiz.whizard2SinFile = 'mymodel.sin \n decay_proc'
    self.whiz.outputFile = 'myoutput.stdhep'
    self.whiz._jobtype = 'User'
    self.whiz.numberOfEvents = 100
    assertDiracSucceeds(self.whiz._checkConsistency(Mock()), self)
    self.assertNotIn({'outputFile': '@{OutputFile}', 'outputPath': '@{OutputPath}',
                        'outputDataSE': '@{OutputSE}'}, self.whiz._listofoutput)
    self.assertNotIn('nbevts', self.whiz.prodparameters)
    self.assertNotIn('Process', self.whiz.prodparameters)
    self.assertNotIn('Model', self.whiz.prodparameters)
    self.assertNotIn('Energy', self.whiz.prodparameters)

  def test_checkconsistency_noVersion(self):
    self.whiz.version = None
    assertDiracFailsWith(self.whiz._checkConsistency(Mock()), 'No version found!', self)

  def test_checkconsistency_noSinFile(self):
    self.whiz.version = '2.3.1'
    self.whiz.whizard2SinFile = None
    assertDiracFailsWith(self.whiz._checkConsistency(Mock()), 'No sin file set!', self)

  def test_checkconsistency_noNumberOfEvents(self):
    self.whiz.version = '2.3.1'
    self.whiz.whizard2SinFile = 'mymodel.sin'
    self.whiz.numberOfEvents = None
    assertDiracFailsWith(self.whiz._checkConsistency(Mock()), 'Number of events not set!', self)

  def test_checkconsistency_nouserjob(self):
    self.whiz.version = '2.3.1'
    self.whiz.whizard2SinFile = 'sqrts=350 GeV\n model=SM \ndecay_proc'
    self.whiz.eventType = 'ee -> ff'
    self.whiz._jobtype = 'notUser'
    self.whiz.numberOfEvents = 100
    assertDiracSucceeds(self.whiz._checkConsistency(Mock()), self)
    self.assertIn({'outputFile': '@{OutputFile}', 'outputPath': '@{OutputPath}',
                     'outputDataSE': '@{OutputSE}'}, self.whiz._listofoutput)
    for keyword in ['Process', 'Energy', 'nbevts', 'Model']:
      self.assertIn(keyword, self.whiz.prodparameters)
    assertEqualsImproved(self.whiz.prodparameters['Energy'], '350', self)
    assertEqualsImproved(self.whiz.prodparameters['Process'], 'ee -> ff', self)
    assertEqualsImproved(self.whiz.prodparameters['Model'], 'SM', self)
    assertEqualsImproved(self.whiz.prodparameters['nbevts'], 100, self)

  def test_checkconsistency_nouserjob_2(self):
    self.whiz.version = '2.3.1'
    self.whiz.whizard2SinFile = '  sqrts  =   350.232   GeV\n model=SM \ndecay_proc'
    self.whiz.eventType = 'ee -> ff'
    self.whiz._jobtype = 'notUser'
    self.whiz.numberOfEvents = 100
    self.whiz.energy = 1337
    assertDiracSucceeds(self.whiz._checkConsistency(Mock()), self)
    self.assertIn({'outputFile': '@{OutputFile}', 'outputPath': '@{OutputPath}',
                   'outputDataSE': '@{OutputSE}'}, self.whiz._listofoutput)
    for keyword in ['Process', 'Energy', 'nbevts', 'Model']:
      self.assertIn(keyword, self.whiz.prodparameters)
    assertEqualsImproved(self.whiz.prodparameters['Energy'], '1337', self)
    assertEqualsImproved(self.whiz.prodparameters['Process'], 'ee -> ff', self)
    assertEqualsImproved(self.whiz.prodparameters['Model'], 'SM', self)
    assertEqualsImproved(self.whiz.prodparameters['nbevts'], 100, self)
    self.assertIn("sqrts = 1337 GeV", self.whiz.whizard2SinFile)

  def test_checkconsistency_nouserjob_fails(self):
    self.whiz.version = '2.3.1'
    self.whiz.whizard2SinFile = 'mymodel.sin \ndecay_proc'
    self.whiz.numberOfEvents = 100
    self.whiz._jobtype = 'notUser'
    assertDiracFailsWith(self.whiz._checkConsistency(Mock()), 'evttype not set, please set event type!', self)

  def test_checkconsistency_nouserjob_fails2(self):
    self.whiz.version = '2.3.1'
    self.whiz.whizard2SinFile = 'model=SM \ndecay_proc'
    self.whiz.eventType = 'ee -> ff'
    self.whiz._jobtype = 'notUser'
    self.whiz.numberOfEvents = 100
    assertDiracFailsWith(
        self.whiz._checkConsistency(
            Mock()),
        'No energy set in sin file, please set "sqrts=...GeV"',
        self)

  def test_checkconsistency_nouserjob_fails3(self):
    self.whiz.version = '2.3.1'
    self.whiz.whizard2SinFile = 'sqrts=350 GeV \ndecay_proc'
    self.whiz.eventType = 'ee -> ff'
    self.whiz._jobtype = 'notUser'
    self.whiz.numberOfEvents = 100
    assertDiracFailsWith(self.whiz._checkConsistency(Mock()), 'No model set in sin file, please set "model=..."', self)

  def test_checkconsistency_nouserjob_fails4(self):
    self.whiz.version = '2.3.1'
    self.whiz.whizard2SinFile = 'sqrts=350 GeV\n sqrts=550 GeV \ndecay_proc'
    self.whiz.eventType = 'ee -> ff'
    self.whiz._jobtype = 'notUser'
    self.whiz.numberOfEvents = 100
    assertDiracFailsWith(
        self.whiz._checkConsistency(
            Mock()),
        'Multiple instances of "sqrts=..GeV" detected, only one can be processed',
        self)

  def test_checkconsistency_nouserjob_fails5(self):
    self.whiz.version = '2.3.1'
    self.whiz.whizard2SinFile = 'sqrts=350 GeV\n model=SM\n model=Susy \ndecay_proc'
    self.whiz.eventType = 'ee -> ff'
    self.whiz._jobtype = 'notUser'
    self.whiz.numberOfEvents = 100
    assertDiracFailsWith(
        self.whiz._checkConsistency(
            Mock()),
        'Multiple instances of "model=..." detected, only one can be processed',
        self)

  def test_checkconsistency_nouserjob_fails6(self):
    self.whiz.version = '2.3.1'
    self.whiz.whizard2SinFile = 'sqrts=350 GeV\n model=SM\n model=Susy'
    self.whiz.eventType = 'ee -> ff'
    self.whiz._jobtype = 'notUser'
    self.whiz.numberOfEvents = 100
    assertDiracFailsWith(self.whiz._checkConsistency(Mock()), '"decay_proc" not found', self)

  def test_setProcessVariables(self):
    ret = self.whiz.setProcessVariables('  decay_proc  ')
    self.assertTrue(ret['OK'])
    self.assertEqual(self.whiz._decayProc, ['decay_proc'])

    ret = self.whiz.setProcessVariables(('  decay_proc  ', 'decay_another   '))
    self.assertTrue(ret['OK'])
    self.assertEqual(self.whiz._decayProc, ['decay_proc', 'decay_another'])

    ret = self.whiz.setProcessVariables({'  decay_proc  ': 'decay_another   '})
    self.assertFalse(ret['OK'])
    self.assertIn('Cannot handle', ret.get('Message'))

  def test_setIntegratedProcess_lfn(self):
    lfn = 'lfn:/vo/user/u/username/mytar.tar.gz'
    ret = self.whiz.setIntegratedProcess(lfn)
    self.assertTrue(ret['OK'])
    self.assertEqual('', self.whiz._integratedProcess)
    self.assertIn(lfn, self.whiz.inputSB)

  @parameterized.expand([(True, '3.1.4', S_OK({'tt': 'tt.tar.gz'})),
                         (False, '', None),  # no version defined
                         (False, '3.1.4', S_OK({'nottt': 'nottt.tar.gz'})),
                       ])
  def test_setIntegratedProcess_config(self, success, version, knownProc):
    proc = 'tt'
    self.whiz.version = version
    with patch.object(self.whiz._ops, 'getOptionsDict', new=Mock(return_value=knownProc)):
      ret = self.whiz.setIntegratedProcess(proc)
    self.assertEqual(ret['OK'], success)
    if success:
      self.assertEqual(proc, self.whiz._integratedProcess)


def runTests():
  """Runs our tests."""
  suite = unittest.defaultTestLoader.loadTestsFromTestCase(Whizard2TestCase)
  testResult = unittest.TextTestRunner(verbosity=2).run(suite)
  print(testResult)


if __name__ == '__main__':
  runTests()
