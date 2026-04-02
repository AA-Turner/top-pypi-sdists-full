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
"""Test the Babayaga WorkflowModule."""

from __future__ import print_function
from __future__ import absolute_import
import unittest
import os
import os.path
import shutil
import tempfile
from mock import patch, MagicMock as Mock


from DIRAC import gLogger, S_OK, S_ERROR
from ILCDIRAC.Workflow.Modules.BabayagaAnalysis import BabayagaAnalysis
from Tests.Utilities.GeneralUtils import assertDiracSucceeds

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Workflow.Modules.BabayagaAnalysis'
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
class TestBabayagaAnalysis(unittest.TestCase):
  """test BabayagaAnalysis."""

  def assertIn(self, *args, **kwargs):
    """make this existing to placate pylint."""
    return super(TestBabayagaAnalysis, self).assertIn(*args, **kwargs)

  @patch("%s.getProxyInfoAsString" % MODULEBASE_NAME, new=Mock(return_value=S_OK()))
  @patch("%s.getProxyInfoAsString" % PROXYINFO_NAME, new=Mock(return_value=S_OK()))
  def setUp(self):
    self.babayaga = BabayagaAnalysis()
    self.curdir = os.getcwd()
    self.tempdir = tempfile.mkdtemp("", dir="./")
    os.chdir(self.tempdir)
    self.babayaga.ops = Mock()

  def tearDown(self):
    os.chdir(self.curdir)
    cleanup(self.tempdir)

class TestBabayagaAnalysisRunit(TestBabayagaAnalysis):
  """test Babayaga runtIt."""

  def setUp(self):
    super(TestBabayagaAnalysisRunit, self).setUp()
    self.logFileName = "localEnv.log"
    with open(self.logFileName, "w") as logF:
      logF.write("logged the logging logs")

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_ERROR("missing setup.sh")))
  def test_Babayaga_runIt_fail_env(self):
    """babayaga.runit failed to get env................................................................"""
    self.babayaga.platform = "Windows"
    self.babayaga.applicationLog = self.logFileName
    res = self.babayaga.runIt()
    self.assertEqual(res['Message'], "missing setup.sh")

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Babayaga_runIt_failure_NostepOK(self):
    """Babayaga.runit failure with platform ........................................................."""
    self.babayaga.applicationLog = self.logFileName
    self.babayaga.platform = "Windows"
    self.babayaga.stepStatus = S_ERROR('aaa')
    # side effect for Steer, Script, log x 2
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False])):
      res = self.babayaga.runIt()
    self.assertIn("Babayaga should not proceed as previous step did not end properly", res['Value'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Babayaga_runIt_failure_NoPlatform(self):
    """Babayaga.runit failure with platform ........................................................."""
    self.babayaga.applicationLog = self.logFileName
    self.babayaga.ignoreapperrors = True
    # side effect for Steer, Script, log x 2
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False])):
      res = self.babayaga.runIt()
    self.assertIn("No ILC platform selected", res['Message'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Babayaga_runIt_failure_NoLogFile(self):
    """Babayaga.runit failure with applicationLog not set............................................."""
    self.babayaga.platform = "Windows"
    self.babayaga.ignoreapperrors = True
    # side effect for Steer, Script, log x 2
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False])):
      res = self.babayaga.runIt()
    self.assertIn("No Log file provide", res['Message'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Babayaga_runIt_failure_LogFile(self):
    """Babayaga.runit failure with applicationLog......................................................"""
    self.babayaga.platform = "Windows"
    self.babayaga.applicationLog = self.logFileName
    self.babayaga.ignoreapperrors = False
  # side effect for Steer, Script, log x 2
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False])):
      res = self.babayaga.runIt()
    self.assertIn("did not produce the expected log", res['Message'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Babayaga_runIt_failure_LogFile_ignore(self):
    """Babayaga.runit failure with applicationLog but ignore..........................................."""
    self.babayaga.platform = "Windows"
    self.babayaga.applicationLog = self.logFileName
    self.babayaga.ignoreapperrors = True
  # side effect for Steer, Script, log x 2
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False])):
      res = self.babayaga.runIt()
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Babayaga_runIt_failure_LogFile_ignore_withseedfile(self):
    """Babayaga.runit failure with applicationLog but with seed file content..........................................."""
    self.babayaga.platform = "Windows"
    self.babayaga.applicationLog = self.logFileName
    self.babayaga.ignoreapperrors = True
    self.babayaga.seedFile = 'content of the seedfile'
  # side effect for (Steer), Script, log x 2
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False])):
      res = self.babayaga.runIt()
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Babayaga_runIt_failure_LogFile_ignore_withseedfile_outputdir(self):
    """Babayaga.runit failure with applicationLog, with seed file content and outputdir but ignore..........................................."""
    self.babayaga.platform = "Windows"
    self.babayaga.applicationLog = self.logFileName
    self.babayaga.ignoreapperrors = True
    self.babayaga.seedFile = 'content of the seedfile'
    self.babayaga.outputDir = 'outputdir'
  # side effect for (Steer), Script, log x 2
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False])):
      res = self.babayaga.runIt()
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Babayaga_runIt_success_LogAndScriptPresent2(self):
    """Babayaga.runit success log and script exist..................................................."""
    self.babayaga.platform = "Windows"
    self.babayaga.applicationLog = self.logFileName
    self.babayaga.ignoreapperrors = True
    self.babayaga.babayagaConfigFile = 'content'
    with open("babayaga__Run_.sh", "w") as scr:
      scr.write("content")
    with open("Babayaga__Steer_.input", "w") as scr:
      scr.write("content")
    with open(self.logFileName, "w") as scr:
      scr.write("content")
  # side effect for Steer, Script, log x 2
    with patch("os.path.exists", new=Mock(side_effect=[True, True, True, False])):
      res = self.babayaga.runIt()
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Babayaga_runIt_success_LogAndScriptPresent3(self):
    """Babayaga.runit success log and script exist..................................................."""
    self.babayaga.platform = "Windows"
    self.babayaga.applicationLog = self.logFileName
    self.babayaga.ignoreapperrors = True
    self.babayaga.babayagaConfigFile = 'content'
    with open("babayaga__Run_.sh", "w") as scr:
      scr.write("content")
    with open("Babayaga__Steer_.input", "w") as scr:
      scr.write("content")
    with open(self.logFileName, "w") as scr:
      scr.write("content")
  # side effect for Steer, Script, log x 2
    with patch("os.path.exists", new=Mock(side_effect=[False, True, True, True])):
      res = self.babayaga.runIt()
    assertDiracSucceeds(res, self)

class TestBabayagaAnalysisASI(TestBabayagaAnalysis):
  """babayaga.ApplicationSpecificInputs."""

  @patch.dict(os.environ, {"JOBID": "12345"})
  def test_Babayaga_ASI_NoVariables(self):
    """babayaga.applicationSpecificInputs: checks that no variables have been set after this call......"""
    gLogger.setLevel("ERROR")
    self.babayaga.workflow_commons = dict()
    self.babayaga.applicationSpecificInputs()
    self.assertFalse(self.babayaga.jobReport or self.babayaga.productionID)

  @patch.dict(os.environ, {"JOBID": "12345"})
  def test_Babayaga_ASI_zeroseed(self):
    """babayaga.applicationSpecificInputs: checks that no variables have been set after this call......"""
    gLogger.setLevel("ERROR")
    self.babayaga.randomSeed = 0
    self.babayaga.workflow_commons = dict()
    self.babayaga.applicationSpecificInputs()
    self.assertFalse(self.babayaga.jobReport or self.babayaga.productionID)

  def test_Babayaga_ASI_bigseed(self):
    """babayaga.applicationSpecificInputs: checks that no variables have been set after this call......"""
    gLogger.setLevel("ERROR")
    self.babayaga.randomSeed = 999999999
    self.babayaga.workflow_commons = dict()
    self.babayaga.applicationSpecificInputs()
    self.assertFalse(self.babayaga.jobReport or self.babayaga.productionID)

  def test_Babayaga_ASI_seedandworkflow(self):
    """babayaga.applicationSpecificInputs: checks that no variables have been set after this call......"""
    gLogger.setLevel("ERROR")
    self.babayaga.randomSeed = 999999999
    self.babayaga.workflow_commons = {"IS_PROD": True,
                                     "PRODUCTION_ID": '2345',
                                     "JOB_ID": '12345'}
    self.babayaga.OutputFile = 'outputfile.root'
    res = self.babayaga.applicationSpecificInputs()
    assertDiracSucceeds(res, self)

def runTests():
  """Runs our tests."""
  suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestBabayagaAnalysis)
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestBabayagaAnalysis))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestBabayagaAnalysis))
  testResult = unittest.TextTestRunner(verbosity=2).run(suite)
  print(testResult)


if __name__ == '__main__':
  runTests()