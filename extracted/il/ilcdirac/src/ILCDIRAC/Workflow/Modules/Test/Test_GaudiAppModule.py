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
"""Test the GaudiApp WorkflowModule."""

from __future__ import print_function
from __future__ import absolute_import
import unittest
import os
import os.path
import shutil
import tempfile
from mock import patch, MagicMock as Mock


from DIRAC import gLogger, S_OK, S_ERROR
from ILCDIRAC.Workflow.Modules.GaudiAppModule import GaudiAppModule
from Tests.Utilities.GeneralUtils import assertDiracSucceeds, assertDiracFails

__RCSID__ = "$Id$"


MODULE_NAME = 'ILCDIRAC.Workflow.Modules.GaudiAppModule'
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
class TestGaudiAppModule(unittest.TestCase):
  """test GaudiAppModule."""

  def assertIn(self, *args, **kwargs):
    """make this existing to placate pylint."""
    return super(TestGaudiAppModule, self).assertIn(*args, **kwargs)

  @patch("%s.getProxyInfoAsString" % MODULEBASE_NAME, new=Mock(return_value=S_OK()))
  @patch("%s.getProxyInfoAsString" % PROXYINFO_NAME, new=Mock(return_value=S_OK()))
  def setUp(self):
    self.gaudi = GaudiAppModule()
    self.curdir = os.getcwd()
    self.tempdir = tempfile.mkdtemp("", dir="./")
    os.chdir(self.tempdir)
    self.gaudi.ops = Mock()

  def tearDown(self):
    os.chdir(self.curdir)
    cleanup(self.tempdir)

#---------------------------------------------------------------------------

class TestGaudiAppModuleRunit(TestGaudiAppModule):
  """test GaudiApp runtIt."""

  def setUp(self):
    super(TestGaudiAppModuleRunit, self).setUp()
    self.logFileName = "localEnv.log"
    self.executableName = "k4run"
    self.outputFileFlag = "flag"
    with open(self.logFileName, "w") as logF:
      logF.write("logged the logging logs")

#-------------------------- RUNIT - noscript -failures

  def test_GaudiApp_runIt_failure_NoPlatform(self):
    """GaudiApp.runit failure with platform ........................................................."""
    self.gaudi.applicationLog = self.logFileName
    self.gaudi.executableName = self.executableName
    res = self.gaudi.runIt()
    self.assertIn("No ILC platform selected", res['Message'])

  def test_GaudiApp_runIt_failure_NoLogFile(self):
    """gaudi.runit failure with logfile................................................................"""
    self.gaudi.platform = "Windows"
    self.gaudi.executableName = self.executableName
    res = self.gaudi.runIt()
    self.assertIn("No Log file provided", res['Message'])

  def test_GaudiApp_runIt_failure_NoExecutable(self):
    """gaudi.runit failure with executable name................................................................"""
    self.gaudi.platform = "Windows"
    self.gaudi.applicationLog = self.logFileName
    res = self.gaudi.runIt()
    self.assertIn("No executable name provided", res['Message'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_ERROR("missing setup.sh")))
  def test_GaudiApp_runIt_failure_env(self):
    """gaudi.runit failed to get env................................................................"""
    self.gaudi.platform = "Windows"
    self.gaudi.applicationLog = self.logFileName
    self.gaudi.executableName = self.executableName
    res = self.gaudi.runIt()
    self.assertEqual(res['Message'], "missing setup.sh")

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value={"OK": False, "Message": ""}))
  def test_GaudiApp_runIt_failure_wrong_env_res(self):
    """gaudi.runit failed to obtain the environment script................................................................"""
    self.gaudi.platform = "Windows"
    self.gaudi.applicationLog = self.logFileName
    self.gaudi.executableName = self.executableName
    res = self.gaudi.runIt()
    assertDiracFails(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  def test_GaudiApp_runIt_failure_WrongSteeringFileName(self):
    """GaudiApp.runit failure with the name of a steering file that does not exist............................................."""
    self.gaudi.platform = "Windows"
    self.gaudi.executableName = self.executableName
    self.gaudi.applicationLog = self.logFileName
    self.gaudi.SteeringFile = "steeringfilethatisnotthere"
    # side effect for the os.path.exists in GaudiAppModule:
    # The first one (self.SteeringFile) (in GaudiAppModule) was called.
    # self.SteeringFile, scriptName, "lib", self.applicationLog, neventsfile, self.applicationLog
    # actually the error happens before the last 5 ones are used   
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False, False, False])):
      res = self.gaudi.runIt()
    self.assertIn("Could not find steering file", res['Message'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_GaudiApp_runIt_failure_LogFile(self):
    """GaudiApp.runit failure with applicationLog......................................................"""
    self.gaudi.platform = "Windows"
    self.gaudi.applicationLog = self.logFileName
    self.gaudi.executableName = self.executableName
    self.gaudi.ignoreapperrors = False
    self.gaudi.outputFileFlag= self.outputFileFlag
    # side effect for the os.path.exists in GaudiAppModule:
    # The first one (self.SteeringFile) (in GaudiAppModule) was not called. 5 were left:
    # scriptName, "lib", self.applicationLog, neventsfile, self.applicationLog
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False, False])):
      res = self.gaudi.runIt()
    self.assertIn("did not produce the expected log", res['Message'])

#-------------------------- RUNIT - noscript - success

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.resolveIFpaths" % MODULE_NAME, new=Mock(return_value={"OK": True, "Value": "inputfile", "Message": "just a test"}))
  def test_GaudiApp_runIt_success_inputfile_ignoreapperrors(self):
    """gaudi.runit failure using the resolveIFpaths function but changing its output................................................................"""
    self.gaudi.platform = "Windows"
    self.gaudi.applicationLog = self.logFileName
    self.gaudi.executableName = self.executableName
    self.gaudi.InputFile = "inputfile"
    self.gaudi.compactFile = "compactfile"
    self.gaudi.NumberOfEvents = "100"
    self.gaudi.ignoreapperrors = True
    with patch("os.path.exists", new=Mock(side_effect=[False, False, True, False, True])):
      res = self.gaudi.runIt()
      assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  def test_GaudiApp_runIt_success_MockedSteeringFileName_ignoreapperrors(self):
    """GaudiApp.runit failure with the name of a steering file that does not exist............................................."""
    self.gaudi.platform = "Windows"
    self.gaudi.executableName = self.executableName
    self.gaudi.applicationLog = self.logFileName
    self.gaudi.SteeringFile = "steeringfilettobemocked"
    self.gaudi.ignoreapperrors = True
    # side effect for the os.path.exists in GaudiAppModule:
    # The first one (self.SteeringFile) (in GaudiAppModule) was called.
    # self.SteeringFile, scriptName, "lib", self.applicationLog, neventsfile, self.applicationLog
    # actually the error happens before the last 5 ones are used   
    with patch("os.path.exists", new=Mock(side_effect=[True, False, False, False, False, False])):
      with patch("os.path.basename", new=Mock(return_value=True)):
        res = self.gaudi.runIt()
        assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  def test_GaudiApp_runIt_success_workflowStatusOK(self):
    """gaudi.runit success while having workflowStatus[OK] set as False................................................................"""
    self.gaudi.platform = "Windows"
    self.gaudi.applicationLog = self.logFileName
    self.gaudi.executableName = self.executableName
    self.gaudi.workflowStatus['OK'] = False
    #NB: workflowStatus['OK'] = False will cause RunIt() to be interrupted earlier
    res = self.gaudi.runIt()
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.resolveIFpaths" % MODULE_NAME, new=Mock(return_value={"OK": False, "Message": "just a test"}))
  def test_GaudiApp_runIt_success_resolveIFpaths(self):
    """gaudi.runit success using the resolveIFpaths function................................................................"""
    self.gaudi.platform = "Windows"
    self.gaudi.applicationLog = self.logFileName
    self.gaudi.executableName = self.executableName
    self.gaudi.InputFile = "inputfile"
    res = self.gaudi.runIt()
    #NB: resolveIFpaths = {"OK": False} will cause RunIt() to be interrupted earlier
    self.assertEqual(res['Message'], "just a test")

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_GaudiApp_runIt_fail_getdetectormodelmocking(self):
    """gaudi.runit fail using the getdetectormodel function but mocked................................................................"""
    self.gaudi.platform = "Windows"
    self.gaudi.applicationLog = self.logFileName
    self.gaudi.executableName = self.executableName
    self.gaudi.detectorModel = "detectormodel"
    with patch("ILCDIRAC.Workflow.Utilities.DD4hepMixin.DD4hepMixin._getDetectorXML", new=Mock(return_value={"OK": True, "Value": "something"})):
      res = self.gaudi.runIt()
    self.assertIn("gaudiapp did not produce the expected log", res['Message'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_GaudiApp_runIt_failure_LogFile_ignoreapperrors(self):
    """GaudiApp.runit failure with applicationLog but ignore..........................................."""
    self.gaudi.platform = "Windows"
    self.gaudi.applicationLog = self.logFileName
    self.gaudi.executableName = self.executableName
    self.gaudi.ignoreapperrors = True
    self.gaudi.outputFileFlag = self.outputFileFlag
    # side effect for the os.path.exists in GaudiAppModule:
    # The first one (self.SteeringFile) (in GaudiAppModule) was not called. 5 were left:
    # scriptName, "lib", self.applicationLog, neventsfile, self.applicationLog
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False, False])):
      res = self.gaudi.runIt()
    assertDiracSucceeds(res, self)

#--------------------------------RUNIT - withscript

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_GaudiApp_runIt_success_LogAndScriptPresent(self):
    """GaudiApp.runit success log and script exist..................................................."""
    self.gaudi.platform = "Windows"
    self.gaudi.applicationLog = self.logFileName
    self.gaudi.ignoreapperrors = True
    self.gaudi.executableName = self.executableName
    self.gaudi.outputFileFlag= self.outputFileFlag
    with open("GaudiApp__Run_.sh", "w") as scr:
      scr.write("content")
    with open("GaudiApp__Steer_.input", "w") as scr:
      scr.write("content")
    with open(self.logFileName, "w") as scr:
      scr.write("content")
    # side effect for the os.path.exists in GaudiAppModule:
    # The first one (self.SteeringFile) (in GaudiAppModule) was not called. 5 were left:
    # scriptName, "lib", self.applicationLog, neventsfile, self.applicationLog    with patch("os.path.exists", new=Mock(side_effect=[True, True, False, True, True])):#[True, True, False, True, False]
    with patch("os.path.exists", new=Mock(side_effect=[True, True, False, True, False])):
      res = self.gaudi.runIt()
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_GaudiApp_runIt_success_LogAndScriptPresentandrandomseedflag(self):
    """GaudiApp.runit success log and script exist..................................................."""
    self.gaudi.platform = "Windows"
    self.gaudi.applicationLog = self.logFileName
    self.gaudi.ignoreapperrors = True
    self.gaudi.executableName = self.executableName
    self.gaudi.outputFileFlag= self.outputFileFlag
    self.gaudi.randomSeedFlag= '--SimG4Svc.seedValue'
    with open("GaudiApp__Run_.sh", "w") as scr:
      scr.write("content")
    with open("GaudiApp__Steer_.input", "w") as scr:
      scr.write("content")
    with open(self.logFileName, "w") as scr:
      scr.write("content")
    # side effect for the os.path.exists in GaudiAppModule:
    # The first one (self.SteeringFile) (in GaudiAppModule) was not called. 5 were left:
    # scriptName, "lib", self.applicationLog, neventsfile, self.applicationLog    with patch("os.path.exists", new=Mock(side_effect=[True, True, False, True, True])):#[True, True, False, True, False]
    with patch("os.path.exists", new=Mock(side_effect=[True, True, False, True, False])):
      res = self.gaudi.runIt()
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_GaudiApp_runIt_success_pythiacard(self):
    """GaudiApp.runit success using the pythia card..................................................."""
    self.gaudi.platform = "Windows"
    self.gaudi.applicationLog = self.logFileName
    self.gaudi.ignoreapperrors = True
    self.gaudi.executableName = self.executableName
    self.gaudi.outputFileFlag = self.outputFileFlag
    self.gaudi.randomSeedFlag = '--SimG4Svc.seedValue'
    self.gaudi.pythia8CardContent = "Beams:LHEF\nMain:numberOfEvents"
    with open("GaudiApp__Run_.sh", "w") as scr:
      scr.write("content")
    with open("GaudiApp__Steer_.input", "w") as scr:
      scr.write("content")
    with open(self.logFileName, "w") as scr:
      scr.write("content")
    # side effect for the os.path.exists in GaudiAppModule:
    # The first one (self.SteeringFile) (in GaudiAppModule) was not called. 5 were left:
    # scriptName, "lib", self.applicationLog, neventsfile, self.applicationLog    with patch("os.path.exists", new=Mock(side_effect=[True, True, False, True, True])):#[True, True, False, True, False]
    with patch("os.path.exists", new=Mock(side_effect=[True, True, False, True, False])):
      res = self.gaudi.runIt()
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_GaudiApp_runIt_failure_notfindbeam(self):
    """GaudiApp.runit not succeeded in finding beam in pythia card..................................................."""
    self.gaudi.platform = "Windows"
    self.gaudi.applicationLog = self.logFileName
    self.gaudi.ignoreapperrors = True
    self.gaudi.executableName = self.executableName
    self.gaudi.outputFileFlag = self.outputFileFlag
    self.gaudi.randomSeedFlag = '--SimG4Svc.seedValue'
    self.gaudi.pythia8CardContent = "ciao\nMain:numberOfEvents\nciao"
    with open("GaudiApp__Run_.sh", "w") as scr:
      scr.write("content")
    with open("GaudiApp__Steer_.input", "w") as scr:
      scr.write("content")
    with open(self.logFileName, "w") as scr:
      scr.write("content")
    # side effect for the os.path.exists in GaudiAppModule:
    # The first one (self.SteeringFile) (in GaudiAppModule) was not called. 5 were left:
    # scriptName, "lib", self.applicationLog, neventsfile, self.applicationLog    with patch("os.path.exists", new=Mock(side_effect=[True, True, False, True, True])):#[True, True, False, True, False]
    with patch("os.path.exists", new=Mock(side_effect=[True, True, False, True, False])):
      res = self.gaudi.runIt()
    self.assertIn("Pythia card with unusual content: neither `Beams:LHEF` nor `Beams:eCM` fields present. Please check the content of your card.", res['Message'])

#--------------------------------ASI

class TestGaudiAppModuleASI(TestGaudiAppModule):
  """gaudi.ApplicationSpecificInputs."""

  @patch.dict(os.environ, {"JOBID": "12345"})
  def test_GaudiApp_ASI_NoVariables(self):
    """gaudi.applicationSpecificInputs: checks that no variables have been set after this call......"""
    gLogger.setLevel("ERROR")
    self.gaudi.workflow_commons = dict()
    self.gaudi.applicationSpecificInputs()
    self.assertFalse(self.gaudi.jobReport or self.gaudi.productionID)

  @patch.dict(os.environ, {"JOBID": "12345"})
  def test_GaudiAPP_ASI_success_workflowstartfrom_Inputdata(self):
    """GaudiApp.applicationSpecificInputs success with a workflowstartfrom............................................."""
    self.gaudi.InputData = "inputdata"
    self.gaudi.WorkflowStartFrom = True     
    res = self.gaudi.applicationSpecificInputs()
    assertDiracSucceeds(res, self)

  @patch.dict(os.environ, {"JOBID": "12345"})
  def test_GaudiAPP_ASI_success_Randomseed(self):
    """GaudiApp.applicationSpecificInputs success with a randomseed............................................."""
    self.gaudi.workflow_commons = {"IS_PROD": True,
                                     "PRODUCTION_ID": '2345',
                                     "JOB_ID": '12345'}
    self.gaudi.OutputFile = 'outputfile.root'
    self.gaudi.randomSeed = 10
    res = self.gaudi.applicationSpecificInputs()
    assertDiracSucceeds(res, self)

#-----------------------------------------------------------------------------------------

def runTests():
  """Runs our tests."""
  suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestGaudiAppModule)
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestGaudiAppModuleRunit))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestGaudiAppModuleASI))
  testResult = unittest.TextTestRunner(verbosity=2).run(suite)
  print(testResult)


#if __name__ == '__main__':
runTests()
