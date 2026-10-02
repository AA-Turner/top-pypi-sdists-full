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
"""Test the Bhlumi WorkflowModule."""

from __future__ import print_function
from __future__ import absolute_import
import unittest
import os
import os.path
import shutil
import tempfile
from mock import patch, MagicMock as Mock


from DIRAC import gLogger, S_OK, S_ERROR
from ILCDIRAC.Workflow.Modules.BhlumiAnalysis import BhlumiAnalysis
from Tests.Utilities.GeneralUtils import assertDiracSucceeds

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Workflow.Modules.BhlumiAnalysis'
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
class TestBhlumiAnalysis(unittest.TestCase):
  """test BhlumiAnalysis."""

  def assertIn(self, *args, **kwargs):
    """make this existing to placate pylint."""
    return super(TestBhlumiAnalysis, self).assertIn(*args, **kwargs)

  @patch("%s.getProxyInfoAsString" % MODULEBASE_NAME, new=Mock(return_value=S_OK()))
  @patch("%s.getProxyInfoAsString" % PROXYINFO_NAME, new=Mock(return_value=S_OK()))
  def setUp(self):
    self.bhlumi = BhlumiAnalysis()
    self.curdir = os.getcwd()
    self.tempdir = tempfile.mkdtemp("", dir="./")
    os.chdir(self.tempdir)
    self.bhlumi.ops = Mock()

  def tearDown(self):
    os.chdir(self.curdir)
    cleanup(self.tempdir)

class TestBhlumiAnalysisRunit(TestBhlumiAnalysis):
  """test Bhlumi runtIt."""

  def setUp(self):
    super(TestBhlumiAnalysisRunit, self).setUp()
    self.logFileName = "localEnv.log"
    with open(self.logFileName, "w") as logF:
      logF.write("logged the logging logs")

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_ERROR("missing setup.sh")))
  def test_Bhlumi_runIt_fail_env(self):
    """bhlumi.runit failed to get env................................................................"""
    self.bhlumi.platform = "Windows"
    self.bhlumi.applicationLog = self.logFileName
    res = self.bhlumi.runIt()
    self.assertEqual(res['Message'], "missing setup.sh")

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Bhlumi_runIt_failure_NostepOK(self):
    """Bhlumi.runit failure with platform ........................................................."""
    self.bhlumi.applicationLog = self.logFileName
    self.bhlumi.platform = "Windows"
    self.bhlumi.stepStatus = S_ERROR('aaa')
    # side effect for Steer, Seed, Script, log x 2
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False, False])):
      res = self.bhlumi.runIt()
    self.assertIn("Bhlumi should not proceed as previous step did not end properly", res['Value'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Bhlumi_runIt_failure_NoPlatform(self):
    """Bhlumi.runit failure with platform ........................................................."""
    self.bhlumi.applicationLog = self.logFileName
    self.bhlumi.ignoreapperrors = True
    # side effect for Steer, Seed, Script, log x 2
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False, False])):
      res = self.bhlumi.runIt()
    self.assertIn("No ILC platform selected", res['Message'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Bhlumi_runIt_failure_NoLogFile(self):
    """Bhlumi.runit failure with applicationLog not set............................................."""
    self.bhlumi.platform = "Windows"
    self.bhlumi.ignoreapperrors = True
    # side effect for Steer, Seed, Script, log x 2
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False, False])):
      res = self.bhlumi.runIt()
    self.assertIn("No Log file provide", res['Message'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Bhlumi_runIt_failure_LogFile(self):
    """Bhlumi.runit failure with applicationLog......................................................"""
    self.bhlumi.platform = "Windows"
    self.bhlumi.applicationLog = self.logFileName
    self.bhlumi.ignoreapperrors = False
  # side effect for Steer, Seed, Script, log x 2
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False, False])):
      res = self.bhlumi.runIt()
    self.assertIn("did not produce the expected log", res['Message'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Bhlumi_runIt_failure_LogFile_ignore(self):
    """Bhlumi.runit failure with applicationLog but ignore..........................................."""
    self.bhlumi.platform = "Windows"
    self.bhlumi.applicationLog = self.logFileName
    self.bhlumi.ignoreapperrors = True
  # side effect for Steer, Seed, Script, log x 2
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False, False])):
      res = self.bhlumi.runIt()
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Bhlumi_runIt_failure_LogFile_ignore_withiniseed(self):
    """Bhlumi.runit failure with applicationLog and iniseed but ignore apperrors..........................................."""
    self.bhlumi.platform = "Windows"
    self.bhlumi.applicationLog = self.logFileName
    self.bhlumi.ignoreapperrors = True
  # side effect for (Steer), Seed, Script, log x 2
    with open("iniseed", "w") as scr:
      scr.write("content")
    with patch("os.path.exists", new=Mock(side_effect=[True, False, False, False])):
      res = self.bhlumi.runIt()
    assert os.path.exists('iniseed') 
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Bhlumi_runIt_failure_LogFile_ignore_withseedfile(self):
    """Bhlumi.runit failure with applicationLog but with seed file content..........................................."""
    self.bhlumi.platform = "Windows"
    self.bhlumi.applicationLog = self.logFileName
    self.bhlumi.ignoreapperrors = True
    self.bhlumi.seedFile = 'content of the seedfile'
  # side effect for (Steer), Seed, Script, log x 2
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False])):
      res = self.bhlumi.runIt()
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Bhlumi_runIt_success_LogAndScriptPresent(self):
    """Bhlumi.runit success log and script exist..................................................."""
    self.bhlumi.platform = "Windows"
    self.bhlumi.applicationLog = self.logFileName
    self.bhlumi.ignoreapperrors = True
    with open("iniseed", "w") as scr:
      scr.write("content")
    with open("bhlumi__Run_.sh", "w") as scr:
      scr.write("content")
    with open(self.logFileName, "w") as scr:
      scr.write("content")
  # side effect for (Steer), Seed, Script, log x 2
    with patch("os.path.exists", new=Mock(side_effect=[True, True, True, False])):
      res = self.bhlumi.runIt()
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Bhlumi_runIt_success_LogAndScriptPresent2(self):
    """Bhlumi.runit success log and script exist..................................................."""
    self.bhlumi.platform = "Windows"
    self.bhlumi.applicationLog = self.logFileName
    self.bhlumi.ignoreapperrors = True
    self.bhlumi.bhlumiConfigFile = 'content'
    with open("iniseed", "w") as scr:
      scr.write("content")
    with open("bhlumi__Run_.sh", "w") as scr:
      scr.write("content")
    with open("Bhlumi__Steer_.input", "w") as scr:
      scr.write("content")
    with open(self.logFileName, "w") as scr:
      scr.write("content")
  # side effect for Steer, Seed, Script, log x 2
    with patch("os.path.exists", new=Mock(side_effect=[True, True, True, True, False])):
      res = self.bhlumi.runIt()
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Bhlumi_runIt_success_LogAndScriptPresentnosteering(self):
    """Bhlumi.runit success log and script exist but no steering file..................................................."""
    self.bhlumi.platform = "Windows"
    self.bhlumi.applicationLog = self.logFileName
    self.bhlumi.ignoreapperrors = True
    self.bhlumi.bhlumiConfigFile = 'content'
    with open("iniseed", "w") as scr:
      scr.write("content")
    with open("bhlumi__Run_.sh", "w") as scr:
      scr.write("content")
    with open("Bhlumi__Steer_.input", "w") as scr:
      scr.write("content")
    with open(self.logFileName, "w") as scr:
      scr.write("content")
  # side effect for Steer, Seed, Script, log x 2
    with patch("os.path.exists", new=Mock(side_effect=[False, True, True, False, True])):
      res = self.bhlumi.runIt()
    with open("iniseed", "r") as rd:
      iniseed = rd.read()
    with open("bhlumi__Run_.sh", "r") as rd:
      script = rd.read()
    assertDiracSucceeds(res, self)
    self.assertIn("IJKLIN", iniseed)
    self.assertIn("Dynamically generated script to run a production or analysis job.", script)

class TestBhlumiAnalysisASI(TestBhlumiAnalysis):
  """bhlumi.ApplicationSpecificInputs."""

  @patch.dict(os.environ, {"JOBID": "12345"})
  def test_Bhlumi_ASI_NoVariables(self):
    """bhlumi.applicationSpecificInputs: checks that no variables have been set after this call......"""
    gLogger.setLevel("ERROR")
    self.bhlumi.workflow_commons = dict()
    self.bhlumi.applicationSpecificInputs()
    self.assertFalse(self.bhlumi.jobReport or self.bhlumi.productionID)

  @patch.dict(os.environ, {"JOBID": "12345"})
  def test_Bhlumi_ASI_zeroseed(self):
    """bhlumi.applicationSpecificInputs: checks that no variables have been set after this call......"""
    gLogger.setLevel("ERROR")
    self.bhlumi.randomSeed = 0
    self.bhlumi.workflow_commons = dict()
    self.bhlumi.applicationSpecificInputs()
    self.assertFalse(self.bhlumi.jobReport or self.bhlumi.productionID)

  def test_Bhlumi_ASI_bigseed(self):
    """bhlumi.applicationSpecificInputs: checks that no variables have been set after this call......"""
    gLogger.setLevel("ERROR")
    self.bhlumi.randomSeed = 999999999
    self.bhlumi.workflow_commons = dict()
    self.bhlumi.applicationSpecificInputs()
    self.assertFalse(self.bhlumi.jobReport or self.bhlumi.productionID)

  def test_Bhlumi_ASI_seedandworkflow(self):
    """bhlumi.applicationSpecificInputs: checks that no variables have been set after this call......"""
    gLogger.setLevel("ERROR")
    self.bhlumi.randomSeed = 999999999
    self.bhlumi.workflow_commons = {"IS_PROD": True,
                                     "PRODUCTION_ID": '2345',
                                     "JOB_ID": '12345'}
    self.bhlumi.OutputFile = 'outputfile.root'
    res = self.bhlumi.applicationSpecificInputs()
    assertDiracSucceeds(res, self)

def runTests():
  """Runs our tests."""
  suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestBhlumiAnalysis)
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestBhlumiAnalysis))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestBhlumiAnalysis))
  testResult = unittest.TextTestRunner(verbosity=2).run(suite)
  print(testResult)


if __name__ == '__main__':
  runTests()