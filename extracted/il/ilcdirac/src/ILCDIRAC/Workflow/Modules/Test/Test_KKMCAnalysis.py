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
"""Test the KKMC WorkflowModule."""

from __future__ import print_function
from __future__ import absolute_import
import unittest
import os
import os.path
import shutil
import tempfile
from mock import patch, MagicMock as Mock


from DIRAC import gLogger, S_OK, S_ERROR
from ILCDIRAC.Workflow.Modules.KKMCAnalysis import KKMCAnalysis
from Tests.Utilities.GeneralUtils import assertDiracSucceeds

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Workflow.Modules.KKMCAnalysis'
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
class TestKKMCAnalysis(unittest.TestCase):
  """test KKMCAnalysis."""

  def assertIn(self, *args, **kwargs):
    """make this existing to placate pylint."""
    return super(TestKKMCAnalysis, self).assertIn(*args, **kwargs)

  @patch("%s.getProxyInfoAsString" % MODULEBASE_NAME, new=Mock(return_value=S_OK()))
  @patch("%s.getProxyInfoAsString" % PROXYINFO_NAME, new=Mock(return_value=S_OK()))
  def setUp(self):
    self.kkmc = KKMCAnalysis()
    self.curdir = os.getcwd()
    self.tempdir = tempfile.mkdtemp("", dir="./")
    os.chdir(self.tempdir)
    self.kkmc.ops = Mock()

  def tearDown(self):
    os.chdir(self.curdir)
    cleanup(self.tempdir)


class TestKKMCAnalysisRunit(TestKKMCAnalysis):
  """test KKMC runtIt."""

  def setUp(self):
    super(TestKKMCAnalysisRunit, self).setUp()
    self.logFileName = "localEnv.log"
    with open(self.logFileName, "w") as logF:
      logF.write("logged the logging logs")

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_KKMC_runIt_success(self):
    """KKMC.runit ................................................................................."""
    self.kkmc.platform = 'Windows'
    self.kkmc.applicationLog = self.logFileName
    # side effect for Script, userlibs, log, logAfter
    with patch("os.path.exists", new=Mock(side_effect=[False, False, True, True])):
      res = self.kkmc.runIt()
    print(res)
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_KKMC_runIt_failure_NostepOK(self):
    """KKMC.runit failure with platform ........................................................."""
    self.kkmc.applicationLog = self.logFileName
    self.kkmc.platform = "Windows"
    self.kkmc.stepStatus = S_ERROR('aaa')
    # side effect for Steer, Script, log x 2
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False])):
      res = self.kkmc.runIt()
    self.assertIn("KKMC should not proceed as previous step did not end properly", res['Value'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_KKMC_runIt_failure_LogFile(self):
    """KKMC.runit failure with applicationLog......................................................"""
    self.kkmc.platform = "Windows"
    self.kkmc.applicationLog = self.logFileName
    self.kkmc.ignoreapperrors = False
    # side effect for Script, userlibs, log, logAfter
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False])):
      res = self.kkmc.runIt()
    self.assertIn("did not produce the expected log", res['Message'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_KKMC_runIt_failure_LogFile_ignore(self):
    """KKMC.runit failure with applicationLog but ignore..........................................."""
    self.kkmc.platform = "Windows"
    self.kkmc.applicationLog = self.logFileName
    self.kkmc.ignoreapperrors = True
    # side effect for Script, userlibs, log, logAfter
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False])):
      res = self.kkmc.runIt()
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_KKMC_runIt_failure_NoLogFile(self):
    """KKMC.runit failure with applicationLog not set............................................."""
    self.kkmc.platform = "Windows"
    self.kkmc.ignoreapperrors = True
    # side effect for Script, userlibs, log, logAfter
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False])):
      res = self.kkmc.runIt()
    self.assertIn("No Log file provide", res['Message'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_KKMC_runIt_failure_NoPlatform(self):
    """KKMC.runit failure with platform ........................................................."""
    self.kkmc.applicationLog = self.logFileName
    self.kkmc.ignoreapperrors = True
    # side effect for Script, userlibs, log, logAfter
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False])):
      res = self.kkmc.runIt()
    self.assertIn("No ILC platform selected", res['Message'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_KKMC_runIt_success_LogAndScriptPresent(self):
    """KKMC.runit success log and script exist..................................................."""
    self.kkmc.platform = "Windows"
    self.kkmc.applicationLog = self.logFileName
    self.kkmc.ignoreapperrors = True
    with open("kkmc__Run_.sh", "w") as scr:
      scr.write("content")
    with open("KKMC__Steer_.input", "w") as scr:
      scr.write("content")
    with open(self.logFileName, "w") as scr:
      scr.write("content")
    # side effect for Script, userlibs, log, logAfter
    with patch("os.path.exists", new=Mock(side_effect=[True, True, False, True])):
      res = self.kkmc.runIt()
    assertDiracSucceeds(res, self)

  # @parameterized.expand([('NumberOfEvents', 100, 'n_events = 100'),
  #                        ('OutputFile', 'test.slcio', 'sample_format = lcio'),
  #                        ('OutputFile', 'test.ascii', 'sample_format = ascii'),
  #                        ('OutputFile', 'test.stdhep', 'sample_format = stdhep'),
  #                        ('randomSeed', '321', 'seed = 321'),
  #                        param('KKMCRawSin', True, 'sample_format', pUnExpected=True),
  #                        ])
  # @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh") ) )
  # @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0,"AllGood")) ) )
  # def test_KKMC_runIt_success_configFile(self, pName, pValue, pExpected, pUnExpected=None):
  #   """kkmc.runit success with configFile........................................................."""
  #   self.kkmc.platform = "Windows"
  #   self.kkmc.applicationLog = self.logFileName
  #   self.kkmc.kkmcConfigFile  = "kkmc instructions"
  #   setattr(self.kkmc, pName, pValue)
  #   ## side effect for Steering1, Steering2, Script, userlib, log, logAfter
  #   with patch("os.path.exists", new=Mock(side_effect=[False, False, False, True] ) ):
  #     res = self.kkmc.runIt()
  #   assertDiracSucceeds( res, self )
  #   self.assertEqual( self.kkmc.kkmcConfigFile , "kkmc instructions" )
  #   self.assertIn( "kkmc instructions", open("KKMC__Steer_.input").read())
  #   if not pUnExpected:
  #     self.assertIn(pExpected, open("KKMC__Steer_.input").read())
  #   else:
  #     self.assertNotIn(pExpected, open("KKMC__Steer_.input").read())

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_ERROR("missing setup.sh")))
  def test_KKMC_runIt_fail_env(self):
    """kkmc.runit failed to get env................................................................"""
    self.kkmc.platform = "Windows"
    self.kkmc.applicationLog = self.logFileName
    res = self.kkmc.runIt()
    self.assertEqual(res['Message'], "missing setup.sh")


class TestKKMCAnalysisASI(TestKKMCAnalysis):
  """kkmc.ApplicationSpecificInputs."""

  @patch.dict(os.environ, {"JOBID": "12345"})
  def test_KKMC_ASI_NoVariables(self):
    """kkmc.applicationSpecificInputs: checks that no variables have been set after this call......"""
    gLogger.setLevel("ERROR")
    self.kkmc.workflow_commons = dict()
    self.kkmc.applicationSpecificInputs()
    self.assertFalse(self.kkmc.jobReport or self.kkmc.productionID)

  def test_KKMC_ASI_bigseed(self):
    """kkmc.applicationSpecificInputs: checks that no variables have been set after this call......"""
    gLogger.setLevel("ERROR")
    self.kkmc.randomSeed = 999999999999999999999
    self.kkmc.workflow_commons = dict()
    self.kkmc.applicationSpecificInputs()
    self.assertFalse(self.kkmc.jobReport or self.kkmc.productionID)

  def test_KKMC_ASI_seedandworkflow(self):
    """kkmc.applicationSpecificInputs: checks that no variables have been set after this call......"""
    gLogger.setLevel("ERROR")
    self.kkmc.randomSeed = 999999999
    self.kkmc.workflow_commons = {"IS_PROD": True,
                                     "PRODUCTION_ID": '2345',
                                     "JOB_ID": '12345'}
    self.kkmc.OutputFile = 'outputfile.root'
    res = self.kkmc.applicationSpecificInputs()
    assertDiracSucceeds(res, self)

def runTests():
  """Runs our tests."""
  suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestKKMCAnalysis)
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestKKMCAnalysisRunit))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestKKMCAnalysisASI))
  testResult = unittest.TextTestRunner(verbosity=2).run(suite)
  print(testResult)


if __name__ == '__main__':
  runTests()
