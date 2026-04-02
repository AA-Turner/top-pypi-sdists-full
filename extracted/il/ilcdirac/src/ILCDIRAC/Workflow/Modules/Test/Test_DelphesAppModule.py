#!/usr/bin/env python
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
"""Test the DelphesApp WorkflowModule."""

from __future__ import print_function
from __future__ import absolute_import
import unittest
import os
import os.path
import shutil
import tempfile
from mock import patch, MagicMock as Mock


from DIRAC import gLogger, S_OK, S_ERROR
from ILCDIRAC.Workflow.Modules.DelphesAppModule import DelphesAppModule
from Tests.Utilities.GeneralUtils import assertDiracSucceeds, assertDiracFails
from ILCDIRAC.Core.Utilities.PrepareOptionFiles import PYTHIA_LHE_INPUT_CMD

__RCSID__ = "$Id$"


MODULE_NAME = 'ILCDIRAC.Workflow.Modules.DelphesAppModule'
MODULEBASE_NAME = 'ILCDIRAC.Workflow.Modules.ModuleBase'
PROXYINFO_NAME = 'DIRAC.Core.Security.ProxyInfo'
# pylint: disable=too-many-public-methods, protected-access

gLogger.setLevel("ERROR")
gLogger.showHeaders(True)


def cleanup(tempdir):
  """Remove files after run."""
  try:
    shutil.rmtree(tempdir)
  except OSError:
    pass


@patch("%s.getProxyInfoAsString" % MODULEBASE_NAME, new=Mock(return_value=S_OK()))
@patch("%s.getProxyInfoAsString" % PROXYINFO_NAME, new=Mock(return_value=S_OK()))
class TestDelphesAppModule(unittest.TestCase):
  """test DelphesAppModule."""

  def assertIn(self, *args, **kwargs):
    """make this existing to placate pylint."""
    return super(TestDelphesAppModule, self).assertIn(*args, **kwargs)

  @patch("%s.getProxyInfoAsString" % MODULEBASE_NAME, new=Mock(return_value=S_OK()))
  @patch("%s.getProxyInfoAsString" % PROXYINFO_NAME, new=Mock(return_value=S_OK()))
  def setUp(self):
    self.delphes = DelphesAppModule()
    self.curdir = os.getcwd()
    self.tempdir = tempfile.mkdtemp("", dir="./")
    os.chdir(self.tempdir)
    self.delphes.ops = Mock()

  def tearDown(self):
    os.chdir(self.curdir)
    cleanup(self.tempdir)

#---------------------------------------------------------------------------

class TestDelphesAppModuleRunit(TestDelphesAppModule):
  """test DelphesApp runtIt."""

  def setUp(self):
    super(TestDelphesAppModuleRunit, self).setUp()
    self.logFileName = "localEnv.log"
    self.executableName = "DelphesPythia8_EDM4HEP"
    self.detectorCard = "delphes_card_IDEA.tcl"
    self.outputCard = "edm4hep_output_config.tcl"
    self.pythia8CardContent = "Random:setSeed = on\nMain:numberOfEvents = 3000         ! number of events to generate"
    self.step_commons = {'STEP_NUMBER': 1}
    with open(self.logFileName, "w") as logF:
      logF.write("logged the logging logs")

#-------------------------- RUNIT

  def test_DelphesApp_runIt_failure_NoPlatform(self):
    """DelphesApp.runit failure with platform ........................................................."""
    self.delphes.applicationLog = self.logFileName
    self.delphes.executableName = self.executableName
    self.delphes.detectorCard = self.detectorCard
    self.delphes.outputCard = self.outputCard
    res = self.delphes.runIt()
    self.assertIn("No ILC platform selected", res['Message'])

  def test_DelphesApp_runIt_failure_NoLogFile(self):
    """delphes.runit failure with logfile................................................................"""
    self.delphes.platform = "Windows"
    self.delphes.executableName = self.executableName
    self.delphes.detectorCard = self.detectorCard
    self.delphes.outputCard = self.outputCard
    res = self.delphes.runIt()
    self.assertIn("No Log file provided", res['Message'])

  def test_DelphesApp_runIt_failure_NoExecutable(self):
    """delphes.runit failure with executable name................................................................"""
    self.delphes.platform = "Windows"
    self.delphes.applicationLog = self.logFileName
    self.delphes.detectorCard = self.detectorCard
    self.delphes.outputCard = self.outputCard
    res = self.delphes.runIt()
    self.assertIn("No executable name provided", res['Message'])

  def test_DelphesApp_runIt_failure_NodetectorCard(self):
    """delphes.runit failure with detectorCard name................................................................"""
    self.delphes.platform = "Windows"
    self.delphes.applicationLog = self.logFileName
    self.delphes.executableName = self.executableName
    self.delphes.outputCard = self.outputCard
    res = self.delphes.runIt()
    self.assertIn("No detectorCard name provided", res['Message'])

  def test_DelphesApp_runIt_failure_NooutputCard(self):
    """delphes.runit failure with outputCard name................................................................"""
    self.delphes.platform = "Windows"
    self.delphes.applicationLog = self.logFileName
    self.delphes.executableName = self.executableName
    self.delphes.detectorCard = self.detectorCard
    res = self.delphes.runIt()
    self.assertIn("No outputCard name provided", res['Message'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_ERROR("missing setup.sh")))
  def test_DelphesApp_runIt_failure_env(self):
    """delphes.runit failed to get env................................................................"""
    self.delphes.platform = "Windows"
    self.delphes.applicationLog = self.logFileName
    self.delphes.executableName = self.executableName
    self.delphes.detectorCard = self.detectorCard
    self.delphes.outputCard = self.outputCard
    res = self.delphes.runIt()
    self.assertEqual(res['Message'], "missing setup.sh")

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value={"OK": False, "Message": ""}))
  def test_DelphesApp_runIt_failure_wrong_env_res(self):
    """delphes.runit failed to obtain the environment script................................................................"""
    self.delphes.platform = "Windows"
    self.delphes.applicationLog = self.logFileName
    self.delphes.executableName = self.executableName
    res = self.delphes.runIt()
    assertDiracFails(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  def test_DelphesApp_runIt_success_workflowStatusOK(self):
    """delphes.runit success while having workflowStatus[OK] set as False................................................................"""
    self.delphes.platform = "Windows"
    self.delphes.applicationLog = self.logFileName
    self.delphes.executableName = self.executableName
    self.delphes.detectorCard = self.detectorCard
    self.delphes.outputCard = self.outputCard
    self.delphes.pythia8CardContent = self.pythia8CardContent
    self.delphes.workflowStatus['OK'] = False
    #NB: workflowStatus['OK'] = False will cause RunIt() to be interrupted earlier
    res = self.delphes.runIt()
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  @patch("%s.preparePythia8Card" % MODULE_NAME, new=Mock(return_value=S_ERROR("error")))
  def test_DelphesApp_runIt_failurepreparepythia8card(self):
    """DelphesApp.runit failure with preparepythia8card..........................................."""
    self.delphes.platform = "Windows"
    self.delphes.applicationLog = self.logFileName
    self.delphes.executableName = self.executableName
    self.delphes.ignoreapperrors = False
    self.delphes.detectorCard = self.detectorCard
    self.delphes.outputCard = self.outputCard
    self.delphes.pythia8CardContent = self.pythia8CardContent
    self.delphes.step_commons = self.step_commons
    # side effect for the os.path.exists in DelphesAppModule:
    # scriptName, "lib", self.applicationLog, self.applicationLog, self.pythia8Card
    with patch("os.path.exists", new=Mock(side_effect=[False, False, True, False, False])):
      res = self.delphes.runIt()
    self.assertIn("error", res['Message'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_DelphesApp_runIt_success_applog(self):
    """DelphesApp.runit success with applog..........................................."""
    self.delphes.platform = "Windows"
    self.delphes.applicationLog = self.logFileName
    self.delphes.executableName = "DelphesROOT_EDM4HEP"
    self.delphes.ignoreapperrors = False
    self.delphes.detectorCard = self.detectorCard
    self.delphes.outputCard = self.outputCard
    self.delphes.pythia8CardContent = self.pythia8CardContent
    self.delphes.step_commons = self.step_commons
    with open("p8_ee_ggqq_ecm91.cmd", "w") as scr:
      scr.write("Beams:LHEF\nMain:numberOfEvents")
    # side effect for the os.path.exists in DelphesAppModule:
    # scriptName, "lib", self.applicationLog, self.applicationLog, (self.pythia8Card)
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, True, True])):
      res = self.delphes.runIt()
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_DelphesApp_runIt_success_ignoreapperrors(self):
    """DelphesApp.runit success with ignoreappererrors..........................................."""
    self.delphes.platform = "Windows"
    self.delphes.applicationLog = self.logFileName
    self.delphes.executableName = "DelphesROOT_EDM4HEP"
    self.delphes.ignoreapperrors = True
    self.delphes.detectorCard = self.detectorCard
    self.delphes.outputCard = self.outputCard
    self.delphes.pythia8CardContent = self.pythia8CardContent
    self.delphes.step_commons = self.step_commons
    with open("p8_ee_ggqq_ecm91.cmd", "w") as scr:
      scr.write("content")
    # side effect for the os.path.exists in DelphesAppModule:
    # scriptName, "lib", self.applicationLog, self.applicationLog, (self.pythia8Card)
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False, True])):
      res = self.delphes.runIt()
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_DelphesApp_runIt_success_solveIFpaths(self):
    """DelphesApp.runit success with solveIFpaths..........................................."""
    self.delphes.platform = "Windows"
    self.delphes.applicationLog = self.logFileName
    self.delphes.executableName = "DelphesROOT_EDM4HEP"
    self.delphes.ignoreapperrors = True
    self.delphes.detectorCard = self.detectorCard
    self.delphes.outputCard = self.outputCard
    self.delphes.InputFile = 'some simulation'
    self.delphes.step_commons = self.step_commons
    with open("p8_ee_ggqq_ecm91.cmd", "w") as scr:
      scr.write("content")
    # side effect for the os.path.exists in DelphesAppModule:
    # scriptName, "lib", self.applicationLog, self.applicationLog, (self.pythia8Card)
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False, True])), \
      patch("%s.resolveIFpaths" % MODULE_NAME, new=Mock(return_value=S_OK('some simulation'))):
      res = self.delphes.runIt()
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_DelphesApp_runIt_success_solveIFpaths_notfound(self):
    """DelphesApp.runit fails with solveIFpaths not finding input files..........................................."""
    self.delphes.platform = "Windows"
    self.delphes.applicationLog = self.logFileName
    self.delphes.executableName = "DelphesROOT_EDM4HEP"
    self.delphes.ignoreapperrors = True
    self.delphes.detectorCard = self.detectorCard
    self.delphes.outputCard = self.outputCard
    self.delphes.pythia8CardContent = self.pythia8CardContent
    self.delphes.InputFile = 'some simulation'
    with patch("%s.resolveIFpaths" % MODULE_NAME, new=Mock(return_value=S_ERROR('resolveIFPath: Input file(s) not found locally'))):
      res = self.delphes.runIt()
    self.assertEqual(res['Message'], "resolveIFPath: Input file(s) not found locally")

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_DelphesApp_runIt_failure_LogFile(self):
    """DelphesApp.runit failure with logfile......................................................"""
    self.delphes.platform = "Windows"
    self.delphes.applicationLog = self.logFileName
    self.delphes.executableName = "DelphesSTDHEP_EDM4HEP"
    self.delphes.ignoreapperrors = False
    self.delphes.detectorCard = self.detectorCard
    self.delphes.outputCard = self.outputCard
    self.delphes.pythia8CardContent = self.pythia8CardContent
    self.delphes.step_commons = self.step_commons
    with open("p8_ee_ggqq_ecm91.cmd", "w") as scr:
      scr.write("content")
    # side effect for the os.path.exists in DelphesAppModule:
    # scriptName, "lib", self.applicationLog, self.applicationLog, (self.pythia8Card)
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False, True])):
      res = self.delphes.runIt()
    print(res)
    self.assertIn("did not produce the expected log", res['Message'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  @patch("%s.preparePythia8Card" % MODULE_NAME, new=Mock(return_value=S_OK("edited card")))
  def test_DelphesApp_runIt_success_LogAndScriptPresentEditingThePythiaFile(self):
    """DelphesApp.runit success log and script exist, also editing the number of events in the Pythia file..................................................."""
    self.delphes.platform = "Windows"
    self.delphes.applicationLog = self.logFileName
    self.delphes.ignoreapperrors = True
    self.delphes.executableName = self.executableName
    self.delphes.detectorCard = self.detectorCard
    self.delphes.outputCard = self.outputCard
    self.delphes.pythia8CardContent = "Beams:LHEF\nMain:numberOfEvents"
    self.delphes.step_commons = self.step_commons
    with open("DelphesApp__Run_.sh", "w") as scr:
      scr.write("content")
    with open(self.logFileName, "w") as scr:
      scr.write("content")
    # side effect for the os.path.exists in DelphesAppModule:
    # scriptName, "lib", self.applicationLog, self.pythia8Card, self.applicationLog
    with patch("os.path.exists", new=Mock(side_effect=[True, True, False, True, False])):    
      res = self.delphes.runIt()
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  @patch("%s.preparePythia8Card" % MODULE_NAME, new=Mock(return_value=S_OK("edited card")))
  def test_DelphesApp_runIt_success_LogAndScriptPresentEditingThePythiaFile2(self):
    """DelphesApp.runit success log and script exist, also editing the number of events in the Pythia file..................................................."""
    self.delphes.platform = "Windows"
    self.delphes.applicationLog = self.logFileName
    self.delphes.ignoreapperrors = True
    self.delphes.executableName = 'DelphesPythia8EvtGen_EDM4HEP_k4Interface'
    self.evtGenParticleList = ''
    self.evtGenFullDecay = ''
    self.evtGenDigit = ''
    self.evtGenPdgid = ''
    self.evtGenBsignal = ''
    self.evtGenCard = 'evtGenCard_1.dec'
    self.delphes.detectorCard = self.detectorCard
    self.delphes.outputCard = self.outputCard
    self.delphes.evtGenCardContent = "somecontent"
    self.delphes.evtPythia8CardContent = "Beams:LHEF\nMain:numberOfEvents"
    self.delphes.step_commons = self.step_commons
    with open("DelphesApp__Run_.sh", "w") as scr:
      scr.write("content")
    with open(self.logFileName, "w") as scr:
      scr.write("content")
    # side effect for the os.path.exists in DelphesAppModule:
    # scriptName, "lib", self.applicationLog, self.pythia8Card, self.applicationLog
    with patch("os.path.exists", new=Mock(side_effect=[True, True, False, True, False])):
      res = self.delphes.runIt()
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  @patch("%s.preparePythia8Card" % MODULE_NAME, new=Mock(return_value=S_OK("edited card")))
  def test_DelphesApp_runIt_success_LogAndScriptPresentEditingThePythiaFile3(self):
    """DelphesApp.runit success log and script exist, also editing the number of events in the Pythia file..................................................."""
    self.delphes.platform = "Windows"
    self.delphes.applicationLog = self.logFileName
    self.delphes.ignoreapperrors = True
    self.delphes.executableName = 'DelphesPythia8_EDM4HEP'
    self.delphes.detectorCard = self.detectorCard
    self.delphes.outputCard = self.outputCard
    self.delphes.pythia8CardContent = PYTHIA_LHE_INPUT_CMD
    self.delphes.InputFile = ['fakeinput.lhe',]
    self.delphes.step_commons = self.step_commons
    with open("DelphesApp__Run_.sh", "w") as scr:
      scr.write("content")
    with open(self.logFileName, "w") as scr:
      scr.write("content")
    # side effect for the os.path.exists in DelphesAppModule:
    # scriptName, "lib", self.applicationLog, self.pythia8Card, self.applicationLog
    with patch("os.path.exists", new=Mock(side_effect=[True, True, False, True, False])):
      res = self.delphes.runIt()
    assertDiracSucceeds(res, self)
    self.assertIn(self.delphes.InputFile, self.delphes.pythia8CardContent)

#--------------------------------ASI

class TestDelphesAppModuleASI(TestDelphesAppModule):
  """delphes.ApplicationSpecificInputs."""

  @patch.dict(os.environ, {"JOBID": "12345"})
  def test_DelphesApp_ASI_NoVariables(self):
    """delphes.applicationSpecificInputs: checks that no variables have been set after this call......"""
    gLogger.setLevel("ERROR")
    self.delphes.workflow_commons = dict()
    self.delphes.applicationSpecificInputs()
    self.assertFalse(self.delphes.jobReport or self.delphes.productionID)

  @patch.dict(os.environ, {"JOBID": "12345"})
  def test_DelphesAPP_ASI_success_Randomseed(self):
    """DelphesApp.applicationSpecificInputs success with a random seed............................................."""
    self.delphes.workflow_commons = {"IS_PROD": True,
                                     "PRODUCTION_ID": '2345',
                                     "JOB_ID": '12345'}
    self.delphes.OutputFile = 'outputfile.root'
    self.delphes.randomSeed = 10
    res = self.delphes.applicationSpecificInputs()
    assertDiracSucceeds(res, self)

  @patch.dict(os.environ, {"JOBID": "12345"})
  def test_DelphesAPP_ASI_success_workflowstartfrom_Inputdata(self):
    """DelphesApp.applicationSpecificInputs success with a workflowstartfrom............................................."""
    self.delphes.InputData = "inputdata"
    self.delphes.WorkflowStartFrom = True     
    res = self.delphes.applicationSpecificInputs()
    assertDiracSucceeds(res, self)

#-----------------------------------------------------------------------------------------

def runTests():
  """Runs our tests."""
  suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestDelphesAppModule)
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestDelphesAppModuleRunit))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestDelphesAppModuleASI))
  testResult = unittest.TextTestRunner(verbosity=2).run(suite)
  print(testResult)


#if __name__ == '__main__':
runTests()
