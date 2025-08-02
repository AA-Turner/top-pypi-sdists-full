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
"""Test GaudiApp module."""

from __future__ import print_function
from __future__ import absolute_import
import linecache
import unittest
from mock import patch, MagicMock as Mock
from mock import mock_open
from mock import mock as mock_module
import six
import os
import shutil
import tempfile

from DIRAC import gLogger, S_OK, S_ERROR
from ILCDIRAC.Interfaces.API.NewInterface.Applications import GaudiApp
from Tests.Utilities.GeneralUtils import assertEqualsImproved, assertDiracFailsWith, \
    assertDiracSucceeds

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Interfaces.API.NewInterface.Applications.GaudiApp'
BUILTIN_NAME = 'builtins' if six.PY3 else '__builtin__'

gLogger.setLevel("DEBUG")
gLogger.showHeaders(True)

# pylint: disable=protected-access
def cleanup(tempdir):
  """Remove files after run."""
  try:
    shutil.rmtree(tempdir)
  except OSError:
    pass

class GaudiAppTestCase(unittest.TestCase):
  """Base class for the GaudiApp test cases."""

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
    self.gaudi = GaudiApp({})
    self.gaudi._jobtype = 'User'
    self.gaudi._ops = Mock(name='OpsMock')
    self.curdir = os.getcwd()
    self.tempdir = tempfile.mkdtemp("", dir="./")
    os.chdir(self.tempdir)

  def tearDown(self):
    os.chdir(self.curdir)
    cleanup(self.tempdir)
    
  def test_setrandomseed(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setRandomSeed(89421)
    self.assertFalse(self.gaudi._errorDict)
    assertEqualsImproved(self.gaudi.randomSeed, 89421, self)

  def test_setrandomseed_fails(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setRandomSeed(['abc'])
    self.assertIn('_checkArgs', self.gaudi._errorDict)

  def test_setrandomseedflag(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setRandomSeedFlag("randomseedflag")
    self.assertFalse(self.gaudi._errorDict)
    assertEqualsImproved(self.gaudi.randomSeedFlag, "randomseedflag", self)

  def test_setrandomseedflag_fails(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setRandomSeedFlag(None)
    self.assertIn('_checkArgs', self.gaudi._errorDict)

  def test_setgaudiworkflow(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setGaudiWorkFlow("fullsim")
    self.assertFalse(self.gaudi._errorDict)
    assertEqualsImproved(self.gaudi.gaudiWorkFlow, "fullsim", self)

  def test_setgaudiworkflow_fails(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setGaudiWorkFlow(None)
    self.assertIn('_checkArgs', self.gaudi._errorDict)
    
  def test_setinputfileflag(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setInputFileFlag("inputfileflag")
    self.assertFalse(self.gaudi._errorDict)
    assertEqualsImproved(self.gaudi.inputFileFlag, "inputfileflag", self)

  def test_setinputfileflag_fails(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setInputFileFlag(None)
    self.assertIn('_checkArgs', self.gaudi._errorDict)

  def test_setoutputfileflag(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setOutputFileFlag("outputfileflag")
    self.assertFalse(self.gaudi._errorDict)
    assertEqualsImproved(self.gaudi.outputFileFlag, "outputfileflag", self)

  def test_setoutputfileflag_fails(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setOutputFileFlag(None)
    self.assertIn('_checkArgs', self.gaudi._errorDict)

  def test_setdetectormodelflag(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setDetectorModelFlag("detectormodelflag")
    self.assertFalse(self.gaudi._errorDict)
    assertEqualsImproved(self.gaudi.detectorModelFlag, "detectormodelflag", self)

  def test_setdetectormodelflag_fails(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setDetectorModelFlag(None)
    self.assertIn('_checkArgs', self.gaudi._errorDict)

  def test_setexecutable(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setExecutableName("executable")
    self.assertFalse(self.gaudi._errorDict)
    assertEqualsImproved(self.gaudi.executableName, "executable", self)

  def test_setexecutable_fails(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setExecutableName(None)
    self.assertIn('_checkArgs', self.gaudi._errorDict)

  def test_setstartfrom(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setStartFrom(89421)
    self.assertFalse(self.gaudi._errorDict)
    assertEqualsImproved(self.gaudi.startFrom, 89421, self)

  def test_setstartfrom_fails(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setStartFrom('adgiuj')
    self.assertIn('_checkArgs', self.gaudi._errorDict)

  def test_keeprecfile(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setKeepRecFile(True)
    self.assertFalse(self.gaudi._errorDict)
    assertEqualsImproved(self.gaudi.keepRecFile, True, self)

  def test_keeprecfile_fails(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setKeepRecFile(89421)
    self.assertIn('_checkArgs', self.gaudi._errorDict)

  def test_setPythia8Card(self):
    self.assertFalse(self.gaudi._errorDict)
    with patch("builtins.open", mock_open(read_data='content')), \
         patch('os.path.isfile', new=Mock(return_value=True)):
      res = self.gaudi.setPythia8Card("pythia8card.cmd")
      assertDiracSucceeds(res, self)
      assertEqualsImproved(self.gaudi.pythia8CardContent, 'content', self)

  def test_setPythiaLHEreader(self):
    self.assertFalse(self.gaudi._errorDict)
    res = self.gaudi.setPythia8Card("Pythia_LHEinput.cmd")
    assertDiracSucceeds(res, self)
    self.assertIn('! 2) Settings related to output in init(), next() and stat().', self.gaudi.pythia8CardContent)

  def test_setPythia8CardEOS(self):
    self.assertFalse(self.gaudi._errorDict)
    with patch("builtins.open", mock_open(read_data='content')), \
         patch("os.path.isfile", new=Mock(side_effect=[False, True])), \
         patch.object(self.gaudi._ops, 'getValue', return_value=['firstlocation']):
      res = self.gaudi.setPythia8Card("p8_ee_tt_ecm365.cmd")
      assertDiracSucceeds(res, self)
      assertEqualsImproved(self.gaudi.pythia8CardContent, 'content', self)

  def test_setPythia8Card_fails_file(self):
    self.assertFalse(self.gaudi._errorDict)
    res = self.gaudi.setPythia8Card("content")
    assertDiracFailsWith(res, 'Pythia8 configuration file does not exist!', self)

  def test_setPythia8Card_fails_argument(self):
    self.assertFalse(self.gaudi._errorDict)
    res = self.gaudi.setPythia8Card(1)
    self.assertIn('_checkArgs', self.gaudi._errorDict)

  def test_setPythia8CardEOS_fails(self):
    self.assertFalse(self.gaudi._errorDict)
    with patch("builtins.open", mock_open(read_data='content')), \
         patch("os.path.isfile", new=Mock(side_effect=[False, False])), \
         patch.object(self.gaudi._ops, 'getValue', return_value=['firstlocation']):
      res = self.gaudi.setPythia8Card("p8_ee_tt_ecm365.cmd")
      assertDiracFailsWith(res, 'Pythia8 configuration file does not exist!', self)

  def test_setarguments(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setArguments("arguments")
    self.assertFalse(self.gaudi._errorDict)
    assertEqualsImproved(self.gaudi.extraCLIArguments, "arguments", self)
    assertDiracSucceeds(self.gaudi.setArguments("arguments"), self)

  def test_setarguments_fails(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setArguments(None)
    self.assertIn('_checkArgs', self.gaudi._errorDict)

  def test_setrecfilepath(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setOutputRecFile("name", "path")
    self.assertFalse(self.gaudi._errorDict)
    assertEqualsImproved(self.gaudi.outputRecFile, "name", self)
    assertEqualsImproved(self.gaudi.outputRecPath, "path", self)

  def test_setrecfilepath_fails(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setOutputRecFile(89421)
    self.assertIn('_checkArgs', self.gaudi._errorDict)

  def test_setsimfilepath(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setOutputSimFile("name", "path")
    self.assertFalse(self.gaudi._errorDict)
    assertEqualsImproved(self.gaudi.outputSimFile, "name", self)
    assertEqualsImproved(self.gaudi.outputSimPath, "path", self)

  def test_setsimfilepath_fails(self):
    self.assertFalse(self.gaudi._errorDict)
    self.gaudi.setOutputSimFile(89421)
    self.assertIn('_checkArgs', self.gaudi._errorDict)
    
#--------------------------------------------------------------------------

  def test_resolvelinkedparams(self):
    step_mock = Mock()
    input_mock = Mock()
    input_mock.getType.return_value = {'abc': False}
    self.gaudi._linkedidx = 3
    self.gaudi._jobsteps = [None, None, None, input_mock]
    assertDiracSucceeds(self.gaudi._resolveLinkedStepParameters(step_mock), self)
    step_mock.setLink.assert_called_once_with('InputFile', {'abc': False}, 'OutputFile')

  def test_resolvelinkedparams_noinputstep(self):
    self.gaudi._linkedidx = None
    self.gaudi._inputappstep = []
    assertDiracSucceeds(self.gaudi._resolveLinkedStepParameters(None), self)

  def test_checkworkflow_app_missing(self):
    self.gaudi._inputapp = ['some_depdency', 'unavailable_dependency_fail_on_this']
    self.gaudi._jobapps = ['myjobapp_1', 'some_dependency']
    assertDiracFailsWith(self.gaudi._checkWorkflowConsistency(), 'job order not correct', self)

  def test_checkworkflow_empty(self):
    self.gaudi._inputapp = []
    self.gaudi._jobapps = []
    assertDiracSucceeds(self.gaudi._checkWorkflowConsistency(), self)

  def test_checkworkflow_success(self):
    self.gaudi._inputapp = ['some_dependency', 'other_dependencies', 'many_more']
    self.gaudi._jobapps = ['ignore_me', 'many_more', 'some_dependency', 'other_dependencies']
    assertDiracSucceeds(self.gaudi._checkWorkflowConsistency(), self)

  def test_userjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.gaudi._userjobmodules(module_mock), self)

  def test_prodjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.gaudi._prodjobmodules(module_mock), self)

  def test_userjobmodules_fails(self):
    with patch('%s._setUserJobFinalization' % MODULE_NAME, new=Mock(return_value=S_OK('something'))),\
            patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_test_err'))):
      assertDiracFailsWith(self.gaudi._userjobmodules(None),
                           'userjobmodules failed', self)

  def test_prodjobmodules_fails(self):
    with patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_OK('something'))), \
            patch('%s._setOutputComputeDataList' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_other_test_err'))):
      assertDiracFailsWith(self.gaudi._prodjobmodules(None),
                           'prodjobmodules failed', self)

#----------------------------------------------------------------------------

  def test_checkconsistency_notuserjobtype(self):
    self.gaudi.version = '134'
    self.gaudi.detectorModel = 'mymodel.det'
    self.gaudi.outputFile = 'myoutput.file'
    self.gaudi._jobtype = 'NotaUser'
    assertDiracSucceeds(self.gaudi._checkConsistency(Mock()), self)
    self.assertIn({'outputFile': '@{OutputFile}', 'outputPath': '@{OutputPath}',
                        'outputDataSE': '@{OutputSE}'}, self.gaudi._listofoutput)
    self.assertNotIn('nbevts', self.gaudi.prodparameters)
    self.assertNotIn('Process', self.gaudi.prodparameters)

  def test_checkconsistency_notStartFrom(self):
    self.gaudi.version = '134'
    self.gaudi.startFrom = True
    self.gaudi.detectorModel = 'mymodel.det'
    self.gaudi.outputFile = 'myoutput.file'
    self.gaudi._jobtype = 'User'
    assertDiracSucceeds(self.gaudi._checkConsistency(Mock()), self)
    self.assertNotIn({'outputFile': '@{OutputFile}', 'outputPath': '@{OutputPath}',
                        'outputDataSE': '@{OutputSE}'}, self.gaudi._listofoutput)
    self.assertNotIn('nbevts', self.gaudi.prodparameters)
    self.assertNotIn('Process', self.gaudi.prodparameters)

  def test_checkconsistency_noversion(self):
    self.gaudi.version = None
    assertDiracFailsWith(self.gaudi._checkConsistency(Mock()), 'no version found', self)

  def test_checkconsistency_lfn_steeringfile(self):
    self.gaudi.version = '134'
    self.gaudi.detectorModel = 'mymodel.det'
    self.gaudi.outputFile = 'myoutput.file'
    self.gaudi._jobtype = 'User'
    self.gaudi.steeringFile = 'lfn:steeringFile'
    assertDiracSucceeds(self.gaudi._checkConsistency(Mock()), self)
    self.assertNotIn({'outputFile': '@{OutputFile}', 'outputPath': '@{OutputPath}',
                        'outputDataSE': '@{OutputSE}'}, self.gaudi._listofoutput)
    self.assertNotIn('nbevts', self.gaudi.prodparameters)
    self.assertNotIn('Process', self.gaudi.prodparameters)

  def test_checkconsistency_okaysteeringfile(self):
    self.gaudi.version = '134'
    self.gaudi.detectorModel = 'mymodel.det'
    self.gaudi.outputFile = 'myoutput.file'
    self.gaudi._jobtype = 'User'
    self.gaudi.steeringFile = 'CLDReconstruction.py'
    assertDiracSucceeds(self.gaudi._checkConsistency(Mock()), self)
    self.assertNotIn({'outputFile': '@{OutputFile}', 'outputPath': '@{OutputPath}',
                        'outputDataSE': '@{OutputSE}'}, self.gaudi._listofoutput)
    self.assertNotIn('nbevts', self.gaudi.prodparameters)
    self.assertNotIn('Process', self.gaudi.prodparameters)

  @patch("DIRAC.Core.Workflow.Parameter.ParameterCollection.getParametersNames", new=Mock(return_value={"a":1, "b":2, "c":3}))
  def test_checkconsistency_badsteeringfile(self):
    self.gaudi.version = '134'
    self.gaudi.detectorModel = 'mymodel.det'
    self.gaudi.outputFile = 'myoutput.file'
    self.gaudi._jobtype = 'User'
    self.gaudi.steeringFile = 'badsteeringFile'
    self.assertIn('is not available locally nor in the software installation', \
                  str(self.gaudi._checkConsistency(Mock())))
    
  def test_checkconsistency_badpythia8card(self):
    self.gaudi.version = '134'
    self.gaudi.detectorModel = 'mymodel.det'
    self.gaudi.outputFile = 'myoutput.file'
    self.gaudi._jobtype = 'User'
    self.gaudi.steeringFile = 'lfn:steeringFile'
    self.gaudi.pythia8CardContent = 'poorcontent'
    self.gaudi.gaudiWorkFlow = 'fastsim'
    res = self.gaudi._checkConsistency(Mock())
    assertDiracFailsWith(self.gaudi._checkConsistency(Mock()), 'Pythia card with unusual content: neither `Beams:LHEF` nor `Beams:eCM` fields present. Please check the content of your card.', self)

    
  def test_checkconsistency_goodpythia8card(self):
    self.gaudi.version = '134'
    self.gaudi.detectorModel = 'mymodel.det'
    self.gaudi.outputFile = 'myoutput.file'
    self.gaudi._jobtype = 'User'
    self.gaudi.steeringFile = 'lfn:steeringFile'
    self.gaudi.pythia8CardContent = 'Beams:LHEF\nMain:numberOfEvents'
    assertDiracSucceeds(self.gaudi._checkConsistency(Mock()), self)


#----------------------------------------------------------------------------

def runTests():
  """Runs our tests."""
  suite = unittest.defaultTestLoader.loadTestsFromTestCase(GaudiAppTestCase)
  testResult = unittest.TextTestRunner(verbosity=2).run(suite)
  print(testResult)


if __name__ == '__main__':
  runTests()
