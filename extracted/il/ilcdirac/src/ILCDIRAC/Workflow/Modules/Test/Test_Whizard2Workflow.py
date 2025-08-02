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
"""Test the Whizard2 WorkflowModule."""

from __future__ import print_function
from __future__ import absolute_import
import unittest
import os
import os.path
import shutil
import tempfile
from mock import patch, MagicMock as Mock, mock_open

from parameterized import parameterized, param

from DIRAC import gLogger, S_OK, S_ERROR
from ILCDIRAC.Workflow.Modules.Whizard2Analysis import Whizard2Analysis
from Tests.Utilities.GeneralUtils import assertDiracSucceeds

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Workflow.Modules.Whizard2Analysis'
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
class TestWhizard2Analysis(unittest.TestCase):
  """test Whizard2Analysis."""

  def assertIn(self, *args, **kwargs):
    """make this existing to placate pylint."""
    return super(TestWhizard2Analysis, self).assertIn(*args, **kwargs)

  @patch("%s.getProxyInfoAsString" % MODULEBASE_NAME, new=Mock(return_value=S_OK()))
  @patch("%s.getProxyInfoAsString" % PROXYINFO_NAME, new=Mock(return_value=S_OK()))
  def setUp(self):
    self.whiz = Whizard2Analysis()
    self.curdir = os.getcwd()
    self.tempdir = tempfile.mkdtemp("", dir="./")
    os.chdir(self.tempdir)
    self.whiz.ops = Mock()

  def tearDown(self):
    os.chdir(self.curdir)
    cleanup(self.tempdir)


class TestWhizard2AnalysisRunit(TestWhizard2Analysis):
  """test Whizard2 runtIt."""

  def setUp(self):
    super(TestWhizard2AnalysisRunit, self).setUp()
    self.logFileName = "python101.log"
    with open(self.logFileName, "w") as logF:
      logF.write("logged the logging logs")

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Whizard2_runIt_success(self):
    """Whizard2.runit ................................................................................."""
    self.whiz.platform = 'Windows'
    self.whiz.applicationLog = self.logFileName
    # side effect for Script, userlibs, log, logAfter
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, True])),\
      patch.object(self.whiz, "_analyseTheLog", new=Mock(return_value=S_OK())):
      res = self.whiz.runIt()
    print(res)
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Whizard2_runIt_failure_LogFile(self):
    """Whizard2.runit failure with applicationLog......................................................"""
    self.whiz.platform = "Windows"
    self.whiz.applicationLog = self.logFileName
    self.whiz.ignoreapperrors = False
    # side effect for Script, userlibs, log, logAfter
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False])):
      res = self.whiz.runIt()
    self.assertIn("did not produce the expected log", res['Message'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Whizard2_runIt_failure_LogFile_ignore(self):
    """Whizard2.runit failure with applicationLog but ignore..........................................."""
    self.whiz.platform = "Windows"
    self.whiz.applicationLog = self.logFileName
    self.whiz.ignoreapperrors = True
    # side effect for Script, userlibs, log, logAfter
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False])):
      res = self.whiz.runIt()
    assertDiracSucceeds(res, self)

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Whizard2_runIt_failure_NoLogFile(self):
    """Whizard2.runit failure with applicationLog not set............................................."""
    self.whiz.platform = "Windows"
    self.whiz.ignoreapperrors = True
    # side effect for Script, userlibs, log, logAfter
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False])):
      res = self.whiz.runIt()
    self.assertIn("No Log file provide", res['Message'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Whizard2_runIt_failure_NoPlatform(self):
    """Whizard2.runit failure with platform ........................................................."""
    self.whiz.applicationLog = self.logFileName
    self.whiz.ignoreapperrors = True
    # side effect for Script, userlibs, log, logAfter
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, False])):
      res = self.whiz.runIt()
    self.assertIn("No ILC platform selected", res['Message'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Whizard2_runIt_success_LogAndScriptPresent(self):
    """Whizard2.runit success log and script exist..................................................."""
    self.whiz.platform = "Windows"
    self.whiz.applicationLog = self.logFileName
    self.whiz.ignoreapperrors = True
    with open("Whizard2__Run_.sh", "w") as scr:
      scr.write("content")
    with open("Whizard2__Steer_.sin", "w") as scr:
      scr.write("content")
    with open(self.logFileName, "w") as scr:
      scr.write("content")
    # side effect for Script, userlibs, log, logAfter
    with patch("os.path.exists", new=Mock(side_effect=[True, True, False, True])):
      res = self.whiz.runIt()
    assertDiracSucceeds(res, self)

  @parameterized.expand([('NumberOfEvents', 100, 'n_events = 100'),
                         ('OutputFile', 'test.slcio', 'sample_format = lcio'),
                         ('OutputFile', 'test.ascii', 'sample_format = ascii'),
                         ('OutputFile', 'test.stdhep', 'sample_format = stdhep'),
                         ('randomSeed', '321', 'seed = 321'),
                         param('whizard2RawSin', True, 'sample_format', pUnExpected=True),
                         ])
  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_OK("setup.sh")))
  @patch("%s.shellCall" % MODULE_NAME, new=Mock(return_value=S_OK((0, "AllGood"))))
  def test_Whizard2_runIt_success_sinFile(self, pName, pValue, pExpected, pUnExpected=None):
    """Whizard.runit success with steeringFile........................................................."""
    self.whiz.platform = "Windows"
    self.whiz.applicationLog = self.logFileName
    self.whiz.whizard2SinFile = "whizard instructions"
    setattr(self.whiz, pName, pValue)
    # side effect for Steering1, Steering2, Script, userlib, log, logAfter
    with patch("os.path.exists", new=Mock(side_effect=[False, False, False, True])), \
      patch.object(self.whiz, "_analyseTheLog", new=Mock(return_value=S_OK())):
      res = self.whiz.runIt()
    assertDiracSucceeds(res, self)
    self.assertEqual(self.whiz.whizard2SinFile, "whizard instructions")
    self.assertIn("whizard instructions", open("Whizard2__Steer_.sin").read())
    if not pUnExpected:
      self.assertIn(pExpected, open("Whizard2__Steer_.sin").read())
    else:
      self.assertNotIn(pExpected, open("Whizard2__Steer_.sin").read())

  @parameterized.expand([(S_ERROR(), S_OK(), 'Whizard2 should not proceed as'),
                         (S_OK(), S_ERROR('resInt Failed'), 'resInt Failed')])
  def test_Whizard2_runIt_fail(self, preStatus, resInt, errorMessage):
    """Whizard.runit fail steps......................................................................."""
    self.whiz.platform = "Windows"
    self.whiz.applicationLog = self.logFileName
    self.whiz.resolveIntegratedProcess = Mock(return_value=resInt)
    self.whiz.workflowStatus = preStatus
    res = self.whiz.runIt()
    if preStatus['OK']:
      self.assertIn(errorMessage, res['Message'])
    else:
      self.assertIn(errorMessage, res['Value'])

  @patch("%s.getEnvironmentScript" % MODULE_NAME, new=Mock(return_value=S_ERROR("missing setup.sh")))
  def test_Whizard2_runIt_fail_env(self):
    """Whizard.runit failed to get env................................................................"""
    self.whiz.platform = "Windows"
    self.whiz.applicationLog = self.logFileName
    res = self.whiz.runIt()
    self.assertEqual(res['Message'], "missing setup.sh")


class TestWhizard2AnalysisASI(TestWhizard2Analysis):
  """Whizard.ApplicationSpecificInputs."""

  @patch.dict(os.environ, {"JOBID": "12345"})
  def test_Whizard2_ASI_NoVariables(self):
    """Whizard.applicationSpecificInputs: checks that no variables have been set after this call......"""
    gLogger.setLevel("ERROR")
    self.whiz.workflow_commons = dict()
    self.whiz.applicationSpecificInputs()
    self.assertFalse(self.whiz.jobReport or self.whiz.productionID)

  @patch.dict(os.environ, {"JOBID": "12345"})
  def test_Whizard2_ASI_RandomSeed_Prod(self):
    """Whizard.applicationSpecificInputs: check setting of randomseed in production..................."""
    gLogger.setLevel("ERROR")
    self.whiz.workflow_commons = dict(IS_PROD=True, PRODUCTION_ID=6666, JOB_ID=123)
    self.whiz.OutputFile = 'events.stdhep'
    self.whiz.resolveInputVariables()
    self.whiz.applicationSpecificInputs()
    self.assertEqual(self.whiz.randomSeed, 6666123)

  def test_Whizard2_ASI_RandomSeedchange_Prod(self):
    """Whizard.applicationSpecificInputs: check changing of randomseed in production..................."""
    gLogger.setLevel("ERROR")
    self.whiz.workflow_commons = dict(IS_PROD=True, PRODUCTION_ID=0, JOB_ID=12345 + 4294967295)
    self.whiz.OutputFile = 'events.stdhep'
    self.whiz.resolveInputVariables()
    self.whiz.applicationSpecificInputs()
    self.assertEqual(self.whiz.randomSeed, 12345)

  @patch.dict(os.environ, {"JOBID": "12345"})
  def test_Whizard2_ASI_RandomSeed_Set(self):
    """Whizard.applicationSpecificInputs: check setting of default randomseed in user jobs............"""
    gLogger.setLevel("ERROR")
    self.whiz = Whizard2Analysis()
    self.whiz.workflow_commons = dict()
    self.whiz.resolveInputVariables()
    self.whiz.applicationSpecificInputs()
    self.assertEqual(int(self.whiz.randomSeed), 12345)

  @patch.dict(os.environ, {"JOBID": "12345"})
  def test_Whizard2_ASI_RandomSeed_User(self):
    """Whizard.applicationSpecificInputs: check setting of randomseed in user jobs...................."""
    gLogger.setLevel("ERROR")
    self.whiz = Whizard2Analysis()
    self.whiz.randomSeed = 654321
    self.whiz.workflow_commons = dict()
    self.whiz.resolveInputVariables()
    self.whiz.applicationSpecificInputs()
    self.assertEqual(int(self.whiz.randomSeed), 654321)

  @patch.dict(os.environ, {"JOBID": "12345"})
  def test_Whizard2_ASI_RandomSeed_User_Zero(self):
    """Whizard.applicationSpecificInputs: check setting of randomseed to zero in user jobs............"""
    gLogger.setLevel("ERROR")
    self.whiz = Whizard2Analysis()
    self.whiz.randomSeed = 0
    self.whiz.workflow_commons = dict()
    self.whiz.resolveInputVariables()
    self.whiz.applicationSpecificInputs()
    self.assertEqual(int(self.whiz.randomSeed), 0)

  def test_Whizard2_resolveIntegratedProcess_NoProc(self):
    """Test resolveIntegratedProcess with no integrated process."""
    gLogger.setLevel('ERROR')
    self.whiz = Whizard2Analysis()
    self.whiz.integratedProcess = ''
    ret = self.whiz.resolveIntegratedProcess()
    self.assertTrue(ret['OK'])

  GOD_RET_VALs = (S_OK({'tt': 'tt.tar'}), S_OK(dict(CVMFSPath='/c/c/c', TarBallURL='/ilc/vo')))

  @parameterized.expand([(False, (S_ERROR('No Processes'),), (None,), False),  # no processes defined
                         (False, (S_OK(), S_ERROR('No Options')), (None,), False),  # no options defined
                         (True, GOD_RET_VALs, (S_OK(),), True),  # cvmfs file exists
                         (True, GOD_RET_VALs, (S_OK(),), False),  # cvmfs file does not exist
                         (False, GOD_RET_VALs, (S_ERROR(),), False),  # getFile fails
                       ])
  def test_Whizard2_resolveIntegratedProcess_WithProc(self, success, sideEffects, gf_SE, localFile):
    self.whiz.integratedProcess = 'tt'
    self.whiz.ops = Mock()
    self.whiz.datMan = Mock(name='DatMan')
    self.whiz.datMan.getFile.side_effect = gf_SE
    self.whiz.ops.getOptionsDict.side_effect = sideEffects
    pathMock = Mock(name='pathMock')
    pathMock.path.join = os.path.join
    pathMock.path.exists.return_value = localFile
    with patch('%s.os' % MODULE_NAME, new=pathMock), \
         patch('%s.extractTarball' % MODULE_NAME, return_value=S_OK()):
      ret = self.whiz.resolveIntegratedProcess()
    self.assertEqual(ret['OK'], success)

  strings = ["corr. to luminosity [fb-1] =   1.2792E+02", """|-----------------------------------------------------------------------------|
  17      69993  7.8172284E-02  1.32E-04    0.17    0.45   19.12    0.41   7
|=============================================================================|""", "Events: actual unweighting efficiency =  15.15 %"]
  @parameterized.expand([(True, "", strings[0] + strings[1] + strings[2], False),
                        (True, "", strings[0] + strings[1] + strings[2], True),
                        (False, "luminosity not found", strings[1] + strings[2], False),
                        (False, "cross section not found", strings[0] + strings[2], False),
                        (False, "efficiency not found", strings[0] + strings[1], False),
                       ])
  def test_Whizard2__analyseTheLog(self, success, error, applog, info):
    """Whizard._analyseTheLog;......................................................................."""
    self.whiz.applicationLog = ""
    if info:
      self.whiz.workflow_commons = {'Info': {}}
    with patch('%s.open' % MODULE_NAME, mock_open(read_data=applog), create=True):
      res = self.whiz._analyseTheLog()
    if success:
      assertDiracSucceeds(res, self)
    else:
      self.assertIn(error, res['Message'])

def runTests():
  """Runs our tests."""
  suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestWhizard2Analysis)
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestWhizard2AnalysisRunit))
  suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestWhizard2AnalysisASI))
  testResult = unittest.TextTestRunner(verbosity=2).run(suite)
  print(testResult)


if __name__ == '__main__':
  runTests()
