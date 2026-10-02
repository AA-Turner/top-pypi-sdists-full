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
"""Run BabaYaga.

:author: Lorenzo Valentini
:since:  May 11, 2023
"""

from __future__ import absolute_import
import os

from DIRAC.Core.Utilities.Subprocess import shellCall
from DIRAC import S_OK, S_ERROR, gLogger
from ILCDIRAC.Workflow.Modules.ModuleBase import ModuleBase
from ILCDIRAC.Core.Utilities.CombinedSoftwareInstallation import getEnvironmentScript
from ILCDIRAC.Core.Utilities.resolvePathsAndNames import getProdFilename

__RCSID__ = '$Id$'
LOG = gLogger.getSubLogger(__name__)

class BabayagaAnalysis(ModuleBase):
  """Specific Module to run a Babayaga job."""

  def __init__(self):
    super(BabayagaAnalysis, self).__init__()
    self.enable = True
    self.STEP_NUMBER = ''
    self.result = S_ERROR()
    self.applicationName = 'babayaga'
    self.startFrom = 0

    self.randomSeed = -1
    self.outputDir = '' #what to set?
    self.debugLevel = 0
    self.babayagaConfigFileContent = ''

  def applicationSpecificInputs(self):
    """Resolve all input variables for the module here.

    :return: S_OK()
    """

    self.randomSeed = self._determineRandomSeed()

    if self.workflow_commons.get("IS_PROD"):
      self.OutputFile = getProdFilename(self.OutputFile,
                                        int(self.workflow_commons["PRODUCTION_ID"]),
                                        int(self.workflow_commons["JOB_ID"]),
                                        self.workflow_commons,
                                        )

    return S_OK('Parameters resolved')
  
  def runIt(self):
    """Called by JobAgent.

    Execute the following:
      - get the environment variables that should have been set during installation
      - prepare the steering file and command line parameters
      - run Babayaga on this steering file and catch the exit status

    :rtype: :func:`~DIRAC.Core.Utilities.ReturnValues.S_OK`, :func:`~DIRAC.Core.Utilities.ReturnValues.S_ERROR`
    """
    self.result = S_OK()
    if not self.platform:
      self.result = S_ERROR('No ILC platform selected')
    elif not self.applicationLog:
      self.result = S_ERROR('No Log file provided')
    if not self.result['OK']:
      LOG.error("Failed to resolve input parameters:", self.result['Message'])
      return self.result
    
    if not self.workflowStatus['OK'] or not self.stepStatus['OK']:
      LOG.verbose('Workflow status = %s, step status = %s' % (self.workflowStatus['OK'], self.stepStatus['OK']))
      return S_OK('Babayaga should not proceed as previous step did not end properly')

    # get the enviroment script
    res = getEnvironmentScript(
        self.platform,
        self.applicationName,
        self.applicationVersion,
        S_ERROR("No init script provided in CVMFS!"))
    if not res['OK']:
      LOG.error("Could not obtain the environment script: ", res["Message"])
      return res
    envScriptPath = res["Value"]

    CLIArguments = ''

    if self.babayagaConfigFileContent:
      babayagaSteerName = 'Babayaga_%s_Steer_%s.input' % (self.applicationVersion, self.STEP_NUMBER)
      if os.path.exists(babayagaSteerName):
        os.remove(babayagaSteerName)

      babayagaSteer = []
      babayagaSteer.append(self.babayagaConfigFileContent)

      with open(babayagaSteerName, 'w') as steerFile:
        steerFile.write("\n".join(babayagaSteer))

      CLIArguments += '--config %s ' % babayagaSteerName
    else:
      CLIArguments += '--ecms %s ' % self.energy
      CLIArguments += '--nevts %s ' % self.NumberOfEvents
      CLIArguments += '--outfile %s ' % self.OutputFile
      CLIArguments += '--debug %s ' % self.debugLevel
      CLIArguments += '--seed %s ' % self.randomSeed
      CLIArguments += self.extraCLIarguments
      if self.outputDir:
        CLIArguments += '--outdir %s ' % self.outputDir

    scriptName = 'babayaga_%s_Run_%s.sh' % (self.applicationVersion, self.STEP_NUMBER)
    if os.path.exists(scriptName):
      os.remove(scriptName)
    script = []
    script.append('#!/bin/bash')
    script.append('#####################################################################')
    script.append('# Dynamically generated script to run a production or analysis job. #')
    script.append('#####################################################################')
    script.append('source %s' % envScriptPath)
    script.append('echo =========')
    script.append('env | sort >> localEnv.log')
    script.append('echo babayaga:`which babayaga`')
    script.append('echo =========')
    script.append('babayaga %s' % CLIArguments)
    script.append('declare -x appstatus=$?')
    # FIXME!
    script.append('cp %s events.lhe' % self.OutputFile)
    script.append('exit $appstatus')

    with open(scriptName, 'w') as scriptFile:
      scriptFile.write("\n".join(script))

    if os.path.exists(self.applicationLog):
      os.remove(self.applicationLog)

    os.chmod(scriptName, 0o755)
    comm = 'bash "./%s"' % scriptName
    self.setApplicationStatus('Babayaga %s step %s' % (self.applicationVersion, self.STEP_NUMBER))
    self.stdError = ''
    self.result = shellCall(0, comm, callbackFunction=self.redirectLogOutput, bufferLimit=20971520)
    resultTuple = self.result['Value']
    if not os.path.exists(self.applicationLog):
      LOG.error("Something went terribly wrong, the log file is not present")
      self.setApplicationStatus('%s failed to produce log file' % (self.applicationName))
      if not self.ignoreapperrors:
        return S_ERROR('%s did not produce the expected log %s' % (self.applicationName, self.applicationLog))
    status = resultTuple[0]

    LOG.info("Status after the application execution is %s" % status)

    return self.finalStatusReport(status)
  
  def _determineRandomSeed(self):
    """Determine what the randomSeed should be.

    Depends on production or not.

    .. Note::
      In Babayaga we use *randomSeed* and not *RandomSeed* as in the other workflow modules

    """
    if self.randomSeed == -1:
      self.randomSeed = int(self.jobID)
    if "IS_PROD" in self.workflow_commons:
      self.randomSeed = int('%s%s' % (self.workflow_commons["PRODUCTION_ID"],
                                      self.workflow_commons["JOB_ID"]))
    if self.randomSeed == 0: # babayaga does not accept 0 as random seed
      LOG.info('babayaga does not accept seed = 0. The new seed is 1')
      self.randomSeed = 1
    return self.randomSeed