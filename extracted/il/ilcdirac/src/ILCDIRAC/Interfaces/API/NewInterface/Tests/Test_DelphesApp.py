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
"""Test DelphesApp module."""

from __future__ import print_function
from __future__ import absolute_import
import linecache
import unittest
from mock import patch, MagicMock as Mock
from mock import mock as mock_module
import six
import os
import shutil
import tempfile
import inspect

from DIRAC import gLogger, S_OK, S_ERROR
from ILCDIRAC.Interfaces.API.NewInterface.Applications import DelphesApp
from Tests.Utilities.GeneralUtils import assertEqualsImproved, assertDiracFailsWith, \
    assertDiracSucceeds

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Interfaces.API.NewInterface.Applications.DelphesApp'
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

class DelphesAppTestCase(unittest.TestCase):
  """Base class for the DelphesApp test cases."""

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
    self.delphes = DelphesApp({})
    self.delphes._jobtype = 'User'
    self.delphes._ops = Mock(name='OpsMock')
    self.curdir = os.getcwd()
    self.tempdir = tempfile.mkdtemp("", dir="./")
    os.chdir(self.tempdir)

  def tearDown(self):
    os.chdir(self.curdir)
    cleanup(self.tempdir)

  def test_setrandomseed(self):
    self.assertFalse(self.delphes._errorDict)
    self.delphes.setRandomSeed(89421)
    self.assertFalse(self.delphes._errorDict)
    assertEqualsImproved(self.delphes.randomSeed, 89421, self)

  def test_setrandomseed_fails(self):
    self.assertFalse(self.delphes._errorDict)
    self.delphes.setRandomSeed(['abc'])
    self.assertIn('_checkArgs', self.delphes._errorDict)

  def test_setexecutable(self):
    self.assertFalse(self.delphes._errorDict)
    self.delphes.setExecutableName("executable")
    self.assertFalse(self.delphes._errorDict)
    assertEqualsImproved(self.delphes.executableName, "executable", self)

  def test_setexecutable_fails(self):
    self.assertFalse(self.delphes._errorDict)
    self.delphes.setExecutableName(None)
    self.assertIn('_checkArgs', self.delphes._errorDict)

  def test_setdetectorcard(self):
    self.assertFalse(self.delphes._errorDict)
    self.delphes.setDetectorCard("detectorcard")
    self.assertFalse(self.delphes._errorDict)
    assertEqualsImproved(self.delphes.detectorCard, "detectorcard", self)
    self.assertFalse(self.delphes.inputSB)
    self.delphes.setDetectorCard("lfn:/mydir/detectorcard")
    assertEqualsImproved(self.delphes.inputSB, ['lfn:/mydir/detectorcard'], self)

  def test_setdetectorcard_fails(self):
    self.assertFalse(self.delphes._errorDict)
    self.delphes.setDetectorCard(1)
    self.assertIn('_checkArgs', self.delphes._errorDict)

  def test_setoutputcard(self):
    self.assertFalse(self.delphes._errorDict)
    self.delphes.setOutputCard("outputcard")
    self.assertFalse(self.delphes._errorDict)
    assertEqualsImproved(self.delphes.outputCard, "outputcard", self)
    self.assertFalse(self.delphes.inputSB)
    self.delphes.setOutputCard("lfn:/mydir/outputcard")
    assertEqualsImproved(self.delphes.inputSB, ['lfn:/mydir/outputcard'], self)

  def test_setoutputcard_fails(self):
    self.assertFalse(self.delphes._errorDict)
    self.delphes.setOutputCard(1)
    self.assertIn('_checkArgs', self.delphes._errorDict)

  def test_setevtgenparticlelist(self):
    self.assertFalse(self.delphes._errorDict)
    self.delphes.setEvtGenParticleList("evtGenParticleList")
    self.assertFalse(self.delphes._errorDict)
    assertEqualsImproved(self.delphes.evtGenParticleList, "evtGenParticleList", self)
    self.assertFalse(self.delphes.inputSB)
    self.delphes.setEvtGenParticleList("lfn:/mydir/evtGenParticleList")
    assertEqualsImproved(self.delphes.inputSB, ['lfn:/mydir/evtGenParticleList'], self)

  def test_setevtgenparticlelist_fails(self):
    self.assertFalse(self.delphes._errorDict)
    self.delphes.setEvtGenParticleList(1)
    self.assertIn('_checkArgs', self.delphes._errorDict)

  def test_setevtgenfulldecay(self):
    self.assertFalse(self.delphes._errorDict)
    self.delphes.setEvtGenFullDecay("evtGenFullDecay")
    self.assertFalse(self.delphes._errorDict)
    assertEqualsImproved(self.delphes.evtGenFullDecay, "evtGenFullDecay", self)
    self.assertFalse(self.delphes.inputSB)
    self.delphes.setEvtGenFullDecay("lfn:/mydir/evtGenFullDecay")
    assertEqualsImproved(self.delphes.inputSB, ['lfn:/mydir/evtGenFullDecay'], self)

  def test_setevtgenfulldecay_fails(self):
    self.assertFalse(self.delphes._errorDict)
    self.delphes.setEvtGenFullDecay(1)
    self.assertIn('_checkArgs', self.delphes._errorDict)

  def test_setevtgendeccard(self):
    with patch.object(inspect.getmodule(DelphesApp), 'cardFinder', new=Mock(return_value=S_OK('content'))):
      self.assertFalse(self.delphes._errorDict)
      self.delphes.setEvtGenDecCard("evtGenDecCard")
      self.assertFalse(self.delphes._errorDict)
      assertEqualsImproved(self.delphes.evtGenDecCardContent, "content", self)

  def test_setevtgendeccard_fails_argument(self):
    self.assertFalse(self.delphes._errorDict)
    try:
      res = self.delphes.setEvtGenDecCard(1)
    except:
      pass
    self.assertIn('_checkArgs', self.delphes._errorDict)

  def test_setevtgendeccardEOS_fails(self):
    with patch.object(inspect.getmodule(DelphesApp), 'cardFinder', new=Mock(return_value=S_ERROR('message'))):
      self.assertFalse(self.delphes._errorDict)
      res = self.delphes.setEvtGenDecCard("p8_ee_tt_ecm365.cmd")
      assertDiracFailsWith(res, 'message', self)

  def test_setPythiaLHEreader(self):
    self.assertFalse(self.delphes._errorDict)
    res = self.delphes.setPythia8Card("Pythia_LHEinput.cmd")
    assertDiracSucceeds(res, self)
    self.assertIn('! 2) Settings related to output in init(), next() and stat().', self.delphes.pythia8CardContent)

  def test_setPythia8CardEOS(self):
    with patch.object(inspect.getmodule(DelphesApp), 'cardFinder', new=Mock(return_value=S_OK('content'))):
      self.assertFalse(self.delphes._errorDict)
      res = self.delphes.setPythia8Card("p8_ee_tt_ecm365.cmd")
      assertDiracSucceeds(res, self)
      assertEqualsImproved(self.delphes.pythia8CardContent, 'content', self)

  def test_setPythia8Card_fails_argument(self):
    self.assertFalse(self.delphes._errorDict)
    res = self.delphes.setPythia8Card(1)
    self.assertIn('_checkArgs', self.delphes._errorDict)

  def test_setPythia8CardEOS_fails(self):
    with patch.object(inspect.getmodule(DelphesApp), 'cardFinder', new=Mock(return_value=S_ERROR('message'))):
      self.assertFalse(self.delphes._errorDict)
      res = self.delphes.setPythia8Card("p8_ee_tt_ecm365.cmd")
      assertDiracFailsWith(res, 'message', self)

  def test_setarguments(self):
    self.assertFalse(self.delphes._errorDict)
    self.delphes.setArguments("arguments")
    self.assertFalse(self.delphes._errorDict)
    assertEqualsImproved(self.delphes.extraCLIArguments, "arguments", self)
    assertDiracSucceeds(self.delphes.setArguments("arguments"), self)

  def test_setarguments_fails(self):
    self.assertFalse(self.delphes._errorDict)
    self.delphes.setArguments(None)
    self.assertIn('_checkArgs', self.delphes._errorDict)

#--------------------------------------------------------------------------

  def test_resolvelinkedparams(self):
    step_mock = Mock()
    input_mock = Mock()
    input_mock.getType.return_value = {'abc': False}
    self.delphes._linkedidx = 3
    self.delphes._jobsteps = [None, None, None, input_mock]
    assertDiracSucceeds(self.delphes._resolveLinkedStepParameters(step_mock), self)
    step_mock.setLink.assert_called_once_with('InputFile', {'abc': False}, 'OutputFile')

  def test_resolvelinkedparams_noinputstep(self):
    self.delphes._linkedidx = None
    self.delphes._inputappstep = []
    assertDiracSucceeds(self.delphes._resolveLinkedStepParameters(None), self)

  def test_checkworkflow_app_missing(self):
    self.delphes._inputapp = ['some_depdency', 'unavailable_dependency_fail_on_this']
    self.delphes._jobapps = ['myjobapp_1', 'some_dependency']
    assertDiracFailsWith(self.delphes._checkWorkflowConsistency(), 'job order not correct', self)

  def test_checkworkflow_empty(self):
    self.delphes._inputapp = []
    self.delphes._jobapps = []
    assertDiracSucceeds(self.delphes._checkWorkflowConsistency(), self)

  def test_checkworkflow_success(self):
    self.delphes._inputapp = ['some_dependency', 'other_dependencies', 'many_more']
    self.delphes._jobapps = ['ignore_me', 'many_more', 'some_dependency', 'other_dependencies']
    assertDiracSucceeds(self.delphes._checkWorkflowConsistency(), self)

  def test_userjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.delphes._userjobmodules(module_mock), self)

  def test_prodjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.delphes._prodjobmodules(module_mock), self)

  def test_userjobmodules_fails(self):
    with patch('%s._setUserJobFinalization' % MODULE_NAME, new=Mock(return_value=S_OK('something'))),\
            patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_test_err'))):
      assertDiracFailsWith(self.delphes._userjobmodules(None),
                           'userjobmodules failed', self)

  def test_prodjobmodules_fails(self):
    with patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_OK('something'))), \
            patch('%s._setOutputComputeDataList' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_other_test_err'))):
      assertDiracFailsWith(self.delphes._prodjobmodules(None),
                           'prodjobmodules failed', self)

#----------------------------------------------------------------------------
  def test_checkconsistency_noversion(self):
    self.delphes.version = None
    assertDiracFailsWith(self.delphes._checkConsistency(Mock()), 'no version found', self)

  def test_checkconsistency_badexecutable(self):
    self.delphes.version = '134'
    self.delphes.executableName = None
    assertDiracFailsWith(self.delphes._checkConsistency(Mock()), 'Executable not supported. Supported executables: DelphesPythia8_EDM4HEP, DelphesSTDHEP_EDM4HEP, DelphesROOT_EDM4HEP', self)

  def test_checkconsistency_badseed(self):
    self.delphes.version = '134'
    self.delphes.executableName = 'DelphesPythia8_EDM4HEP'
    self.delphes.randomSeed = -2
    assertDiracFailsWith(self.delphes._checkConsistency(Mock()), 'Random Seed has to be equal or greater than -1', self)

  def test_checkconsistency_nodetectorcard(self):
    self.delphes.version = '134'
    self.delphes.executableName = 'DelphesPythia8_EDM4HEP'
    self.delphes.randomSeed = -1
    assertDiracFailsWith(self.delphes._checkConsistency(Mock()), 'Missing detector config-file.', self)

  def test_checkconsistency_nooutputcard(self):
    self.delphes.version = '134'
    self.delphes.executableName = 'DelphesPythia8_EDM4HEP'
    self.delphes.randomSeed = -1
    self.delphes.detectorCard = 'card_IDEA.tcl'
    assertDiracFailsWith(self.delphes._checkConsistency(Mock()), 'Missing output-config-file.', self)

  def test_checkconsistency_nopythia8card(self):
    self.delphes.version = '134'
    self.delphes.executableName = 'DelphesPythia8_EDM4HEP'
    self.delphes.randomSeed = -1
    self.delphes.detectorCard = 'card_IDEA.tcl'
    self.delphes.outputCard = 'edm4hep_IDEA.tcl'
    assertDiracFailsWith(self.delphes._checkConsistency(Mock()), 'Missing Pythia 8 Card. The execution of Delphes would not succeed', self)

  def test_checkconsistency_baddetectorcard(self):
    self.delphes.version = '134'
    self.delphes.executableName = 'DelphesPythia8_EDM4HEP'
    self.delphes.randomSeed = -1
    self.delphes.detectorCard = 'badname'
    assertDiracFailsWith(self.delphes._checkConsistency(Mock()), 'Wrong name for the detector config file. Hint: they all end in ".tcl"', self)

  def test_checkconsistency_badoutputcard(self):
    self.delphes.version = '134'
    self.delphes.executableName = 'DelphesPythia8_EDM4HEP'
    self.delphes.randomSeed = -1
    self.delphes.detectorCard = 'card_IDEA.tcl'
    self.delphes.outputCard = 'badname'
    assertDiracFailsWith(self.delphes._checkConsistency(Mock()), 'Wrong name for the output config file. Hint: they all end in ".tcl"', self)

  def test_checkconsistency_detectorcardnotavailable(self):
    self.delphes.version = '134'
    self.delphes.executableName = 'DelphesPythia8_EDM4HEP'
    self.delphes.randomSeed = -1
    self.delphes.detectorCard = 'badname.tcl'
    res = self.delphes._checkConsistency(Mock())
    assertDiracFailsWith(res, 'badname.tcl is not available locally nor in the software installation', self)

  def test_checkconsistency_outputcardnotavailable(self):
    self.delphes.version = '134'
    self.delphes.executableName = 'DelphesPythia8_EDM4HEP'
    self.delphes.randomSeed = -1
    self.delphes.detectorCard = 'card_IDEA.tcl'
    self.delphes.outputCard = 'badname.tcl'
    res = self.delphes._checkConsistency(Mock())
    assertDiracFailsWith(res, 'badname.tcl is not available locally nor in the software installation', self)

  def test_checkconsistency_badpythia8card(self):
    self.delphes.version = '134'
    self.delphes.executableName = 'DelphesPythia8_EDM4HEP'
    self.delphes.randomSeed = -1
    self.delphes.detectorCard = 'card_IDEA.tcl'
    self.delphes.outputCard = 'edm4hep_IDEA.tcl'
    self.delphes.pythia8CardContent = 'poorcontent'
    res = self.delphes._checkConsistency(Mock())
    assertDiracFailsWith(res, 'Pythia card with unusual content: neither `Beams:LHEF` nor `Beams:eCM` fields present. Please check the content of your card.', self)

  def test_checkconsistency_evtgen(self):
    self.delphes.version = '134'
    self.delphes.executableName = 'DelphesPythia8EvtGen_EDM4HEP_k4Interface'
    self.delphes.randomSeed = -1
    self.delphes.detectorCard = 'card_IDEA.tcl'
    self.delphes.outputCard = 'edm4hep_IDEA.tcl'
    self.delphes.evtGenParticleList = 'evt.pdl'
    self.delphes.evtGenDecCardContent  = 'user.dec'
    self.delphes.evtGenFullDecay = 'DECAY.DEC'
    self.delphes.pythia8CardContent = 'Beams:LHEF\nMain:numberOfEvents'
    self.delphes.evtGenDecCardContent = 'poorcontent'
    self.delphes.evtGenBsignal = ''
    assertDiracSucceeds(self.delphes._checkConsistency(Mock()), self)
    self.assertNotIn({'outputFile': '@{OutputFile}', 'outputPath': '@{OutputPath}',
                        'outputDataSE': '@{OutputSE}'}, self.delphes._listofoutput)
    self.assertNotIn('nbevts', self.delphes.prodparameters)
    self.assertNotIn('Process', self.delphes.prodparameters)

  def test_checkconsistency_evtgen_failinputfiles(self):
    self.delphes.version = '134'
    self.delphes.executableName = 'DelphesPythia8EvtGen_EDM4HEP_k4Interface'
    self.delphes.randomSeed = -1
    self.delphes.detectorCard = 'card_IDEA.tcl'
    self.delphes.outputCard = 'edm4hep_IDEA.tcl'
    self.delphes.pythia8CardContent = 'Beams:LHEF\nMain:numberOfEvents'
    self.delphes.evtGenDecCardContent = 'poorcontent'
    self.delphes.evtGenBsignal = ''
    res = self.delphes._checkConsistency(Mock())
    assertDiracFailsWith(res, 'Missing some Evtgen input files: DECAY.DEC, evt.pdl or user.dec', self)

  def test_checkconsistency_evtgen_failevtgencardcontent(self):
    self.delphes.version = '134'
    self.delphes.executableName = 'DelphesPythia8EvtGen_EDM4HEP_k4Interface'
    self.delphes.randomSeed = -1
    self.delphes.detectorCard = 'card_IDEA.tcl'
    self.delphes.outputCard = 'edm4hep_IDEA.tcl'
    self.delphes.evtGenParticleList = 'evt.pdl'
    self.delphes.evtGenDecCardContent  = 'user.dec'
    self.delphes.evtGenFullDecay = 'DECAY.DEC'
    self.delphes.pythia8CardContent = 'Beams:LHEF\nMain:numberOfEvents'
    self.delphes.evtGenDecCardContent = 'poorcontent'
    self.delphes.evtGenBsignal = 'something'
    res = self.delphes._checkConsistency(Mock())
    assertDiracFailsWith(res, f'Can not find the correct evtGenBsignal ({self.delphes.evtGenBsignal}) in the evtGenDecCardContent that was selected.', self)

  def test_checkconsistency(self):
    self.delphes.version = '134'
    self.delphes.executableName = 'DelphesPythia8_EDM4HEP'
    self.delphes.detectorCard = 'card_IDEA.tcl'
    self.delphes.outputCard = 'edm4hep_IDEA.tcl'
    self.delphes.pythia8CardContent = 'Beams:LHEF\nMain:numberOfEvents'
    self.delphes.outputFile = 'myoutput.file'
    self.delphes._jobtype = 'User'
    assertDiracSucceeds(self.delphes._checkConsistency(Mock()), self)
    self.assertNotIn({'outputFile': '@{OutputFile}', 'outputPath': '@{OutputPath}',
                        'outputDataSE': '@{OutputSE}'}, self.delphes._listofoutput)
    self.assertNotIn('nbevts', self.delphes.prodparameters)
    self.assertNotIn('Process', self.delphes.prodparameters)

  def test_checkconsistency_longfilenames(self):
    self.delphes.version = '134'
    self.delphes.executableName = 'DelphesPythia8_EDM4HEP'
    self.delphes.detectorCard = 'lfn:card_IDEA.tcl'
    self.delphes.outputCard = 'lfn:edm4hep_IDEA.tcl'
    self.delphes.pythia8CardContent = 'Beams:LHEF\nMain:numberOfEvents'
    self.delphes.outputFile = 'myoutput.file'
    self.delphes._jobtype = 'User'
    assertDiracSucceeds(self.delphes._checkConsistency(Mock()), self)
    self.assertNotIn({'outputFile': '@{OutputFile}', 'outputPath': '@{OutputPath}',
                        'outputDataSE': '@{OutputSE}'}, self.delphes._listofoutput)
    self.assertNotIn('nbevts', self.delphes.prodparameters)
    self.assertNotIn('Process', self.delphes.prodparameters)

  def test_checkconsistency_notuserjobtype(self):
    self.delphes.version = '134'
    self.delphes.executableName = 'DelphesSTDHEP_EDM4HEP'
    self.delphes.detectorCard = 'card_IDEA.tcl'
    self.delphes.outputCard = 'edm4hep_IDEA.tcl'
    self.delphes.outputFile = 'myoutput.file'
    self.delphes._jobtype = 'NotaUser'
    assertDiracSucceeds(self.delphes._checkConsistency(Mock()), self)
    self.assertIn({'outputFile': '@{OutputFile}', 'outputPath': '@{OutputPath}',
                        'outputDataSE': '@{OutputSE}'}, self.delphes._listofoutput)
    self.assertNotIn('nbevts', self.delphes.prodparameters)
    self.assertNotIn('Process', self.delphes.prodparameters)

#----------------------------------------------------------------------------

def runTests():
  """Runs our tests."""
  suite = unittest.defaultTestLoader.loadTestsFromTestCase(DelphesAppTestCase)
  testResult = unittest.TextTestRunner(verbosity=2).run(suite)
  print(testResult)


if __name__ == '__main__':
  runTests()
