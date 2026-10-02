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
"""Run Bhlumi.

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

class BhlumiAnalysis(ModuleBase):
  """Specific Module to run a Bhlumi job."""

  def __init__(self):
    super(BhlumiAnalysis, self).__init__()
    self.enable = True
    self.STEP_NUMBER = ''
    self.result = S_ERROR()
    self.applicationName = 'bhlumi'
    self.startFrom = 0

    self.randomSeed = -1
    self.bhlumiConfigFileContent = ''
    self.seedName = 'iniseed'
    self.seedFile = '' # to understand how to implement correctly
    # usage of the seeds: 
    # https://github.com/KrakowHEPSoft/BHLUMI/blob/29df3fed7955f335c04a171c18c685d2f187e4c1/lib/yfslib.f
    # https://github.com/KrakowHEPSoft/BHLUMI/blob/29df3fed7955f335c04a171c18c685d2f187e4c1/4.x-cpc/demo2.f
    # seed semaphore in the middle of a sequence:
    # https://github.com/KrakowHEPSoft/BHLUMI/blob/29df3fed7955f335c04a171c18c685d2f187e4c1/4.x-cpc/prod1/semaphore
    # iniseed examples:
      # 13517277      IJKLIN= 03806061
      #    0      NTOTIN= 0
      #    0      NTOT2N= 0
    # https://github.com/KrakowHEPSoft/BHLUMI/blob/29df3fed7955f335c04a171c18c685d2f187e4c1/4.x-cpc/iniseed/iniseed.9

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
      - run Bhlumi on this steering file and catch the exit status

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
      return S_OK('Bhlumi should not proceed as previous step did not end properly')

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

    if self.bhlumiConfigFileContent:
      bhlumiSteerName = 'Bhlumi_%s_Steer_%s.input' % (self.applicationVersion, self.STEP_NUMBER)
      if os.path.exists(bhlumiSteerName):
        os.remove(bhlumiSteerName)

      bhlumiSteer = []
      bhlumiSteer.append(self.bhlumiConfigFileContent)

      with open(bhlumiSteerName, 'w') as steerFile:
        steerFile.write("\n".join(bhlumiSteer))

      CLIArguments += '--config %s ' % bhlumiSteerName

    else:
      CLIArguments += '--ecms %s ' % self.energy
      CLIArguments += '--nevts %s ' % self.NumberOfEvents
      CLIArguments += '--outfile %s ' % self.OutputFile
      CLIArguments += self.extraCLIarguments
    CLIArguments += '--seedfile %s ' % self.seedName


    if os.path.exists(self.seedName):
      os.remove(self.seedName)

    if self.seedFile:
      lines = self.seedFile.splitlines(keepends=True)
      lines[0] = f" {self.randomSeed}      IJKLIN= {self.randomSeed*7 % 900000000}\n"
      with open(self.seedName, 'w') as iniseed:
        iniseed.writelines(lines)

    else:
      with open(self.seedName, 'w') as iniseed:
        # IMPORTANT: Spaces are important! The Fortran routine reads the first 10 characters to get the seed.
        #            We need to be sure that letters start at least from the 11th character of the line.
        iniseed.writelines([f"{self.randomSeed}" + " "*10 + f"IJKLIN= {self.randomSeed*7 % 900000000}\n",
                            "0" + " "*10 + "NTOTIN= 0\n",
                            "0" + " "*10 + "NTOT2N= 0\n"])  


    scriptName = 'bhlumi_%s_Run_%s.sh' % (self.applicationVersion, self.STEP_NUMBER)
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
    script.append('echo bhlumi:`which BHLUMI`')
    script.append('echo =========')
    script.append('BHLUMI %s' % CLIArguments)
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
    self.setApplicationStatus('Bhlumi %s step %s' % (self.applicationVersion, self.STEP_NUMBER))
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
      In Bhlumi we use *randomSeed* and not *RandomSeed* as in the other workflow modules

    """
    if self.randomSeed == -1:
      self.randomSeed = int(self.jobID)
      LOG.info(f'bhlumi does not accept seed > 900000000. The new seed is {self.randomSeed} = seed % 900000000.')
    if "IS_PROD" in self.workflow_commons:
      self.randomSeed = int('%s%s' % (self.workflow_commons["PRODUCTION_ID"],
                                      self.workflow_commons["JOB_ID"]))
    if self.randomSeed > 900000000: # bhlumi does not accept seed > 900000000
      self.randomSeed = self.randomSeed % 900000000
    return self.randomSeed