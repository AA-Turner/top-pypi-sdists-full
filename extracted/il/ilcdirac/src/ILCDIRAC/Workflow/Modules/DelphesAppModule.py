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
"""Run a DelphesApp.

:author: Lorenzo Valentini
:since:  Mar 03, 2023
"""

from __future__ import absolute_import
import os

from DIRAC.Core.Utilities.Subprocess import shellCall
from DIRAC import S_OK, S_ERROR, gLogger
from ILCDIRAC.Core.Utilities.CombinedSoftwareInstallation import getEnvironmentScript
from ILCDIRAC.Core.Utilities.resolvePathsAndNames import resolveIFpaths, getProdFilename
from ILCDIRAC.Workflow.Modules.ModuleBase import ModuleBase
from ILCDIRAC.Core.Utilities.PrepareOptionFiles import preparePythia8Card, PYTHIA_LHE_INPUT_CMD


__RCSID__ = '$Id$'
LOG = gLogger.getSubLogger(__name__)


class DelphesAppModule(ModuleBase):
  """Specific Module to run a Delphes job."""

  def __init__(self):
    super(DelphesAppModule, self).__init__()
    self.enable = True
    self.STEP_NUMBER = ''
    self.result = S_ERROR()
    self.applicationName = 'delphesapp'
    self.randomSeed = -1
    self.executableName = ''
    self.detectorCard = ''
    self.outputCard = ''
    self.pythia8CardContent = ''
    self.pythia8Card = None
    self.eventstring = ['+++ Initializing event']  # FIXME
    self.evtGenParticleList = ''
    self.evtGenFullDecay = ''
    self.evtGenDecCardContent = ''
    self.evtGenCard = None
    self.evtGenDigit = ''
    self.evtGenPdgid = ''
    self.evtGenBsignal = ''

  def applicationSpecificInputs(self):
    """Resolve all input variables for the module here.

    :return: S_OK()
    """

    if self.WorkflowStartFrom:
      self.startFrom = self.WorkflowStartFrom

    self.randomSeed = self._determineRandomSeed()

    if "IS_PROD" in self.workflow_commons and self.workflow_commons["IS_PROD"]:
      self.OutputFile = getProdFilename(self.OutputFile,
                                        int(self.workflow_commons["PRODUCTION_ID"]),
                                        int(self.workflow_commons["JOB_ID"]),
                                        self.workflow_commons,
                                        )
    LOG.info('Have input files?', self.InputFile)
    LOG.info('Have input data?', self.InputData)
    if not self.InputFile and self.InputData:
      for files in self.InputData:
        self.InputFile.append(files)
        LOG.info('Found input files', self.InputFile)
    return S_OK('Parameters resolved')

  def runIt(self):
    """Execute the following:

    - prepare run script using input parameters
    - prepare pythia card if necessary
    - run a delphes executable using input some input files or the pythia card
    - catch the exit status

    :returns: :func:`~DIRAC.Core.Utilities.ReturnValues.S_OK`, :func:`~DIRAC.Core.Utilities.ReturnValues.S_ERROR`
    """
    self.result = S_OK()
    if not self.platform:
      self.result = S_ERROR('No ILC platform selected')
    elif not self.applicationLog:
      self.result = S_ERROR('No Log file provided')
    elif not self.executableName:
      self.result = S_ERROR('No executable name provided')
    elif not self.detectorCard:
      self.result = S_ERROR('No detectorCard name provided')
    elif not self.outputCard:
      self.result = S_ERROR('No outputCard name provided')
    if not self.result['OK']:
      LOG.error("Failed to resolve input parameters:", self.result['Message'])
      return self.result

    if not self.workflowStatus['OK'] or not self.stepStatus['OK']:
      LOG.verbose('Workflow status = %s, step status = %s' % (self.workflowStatus['OK'], self.stepStatus['OK']))
      return S_OK('DelphesApp should not proceed as previous step did not end properly')

    # TODO: Setup LD_LIBRARY_PATH for extensions
    res = getEnvironmentScript(self.platform, self.applicationName, self.applicationVersion, self.getEnvScript)
    if not res['OK']:
      LOG.error("Could not obtain the environment script: ", res["Message"])
      return res
    envScriptPath = res["Value"]

    if self.InputFile:
      res = resolveIFpaths(self.InputFile)
      if not res['OK']:
        LOG.error("InputFile file not found")
        return res
      self.InputFile = res['Value'][0]

    cmd = []

    self.pythia8Card = f'pythia8card_{self.step_commons["STEP_NUMBER"]}.cmd'
    self.evtGenCard = f'evtGenCard_{self.step_commons["STEP_NUMBER"]}.dec'

    cmd.append({'DelphesPythia8_EDM4HEP': f'{self.detectorCard} {self.outputCard} {self.pythia8Card} {self.OutputFile}',
               'DelphesSTDHEP_EDM4HEP': f'{self.detectorCard} {self.outputCard} {self.OutputFile} {self.InputFile}',
               'DelphesROOT_EDM4HEP': f'{self.detectorCard} {self.outputCard} {self.OutputFile} {self.InputFile}',
               'DelphesPythia8EvtGen_EDM4HEP_k4Interface': f'{self.detectorCard} {self.outputCard} {self.pythia8Card} {self.OutputFile} {self.evtGenFullDecay} {self.evtGenParticleList} {self.evtGenCard} {self.evtGenPdgid} {self.evtGenBsignal} {self.evtGenDigit}',
              }[self.executableName])

    scriptName = 'DelphesApp_%s_Run_%s.sh' % (self.applicationVersion, self.STEP_NUMBER)
    if os.path.exists(scriptName):
      os.remove(scriptName)
    script = []
    script.append('#!/bin/bash')
    script.append('source %s' % envScriptPath)
    script.append('echo =========')

    # for user provided libraries
    if os.path.exists("lib"):
      script.append("export LD_LIBRARY_PATH=$PWD/lib:$LD_LIBRARY_PATH")

    script.append('env | sort >> localEnv.log')
    script.append('echo DelphesApp:`which %s`' % self.executableName)
    script.append('echo =========')
    comm = '%(executable)s %(args)s %(extraArgs)s ' % \
        dict(executable=self.executableName,
             args=' '.join(cmd),
             extraArgs=self.extraCLIarguments,
             )
    # comm += " -v"
    
    LOG.info("Command:", comm)
    script.append(comm)
    script.append('declare -x appstatus=$?')
    script.append('exit $appstatus')

    with open(scriptName, 'w') as scriptFile:
      scriptFile.write("\n".join(script))

    if os.path.exists(self.applicationLog):
      os.remove(self.applicationLog)

    if self.executableName in ['DelphesPythia8_EDM4HEP'] and self.pythia8CardContent == PYTHIA_LHE_INPUT_CMD and self.InputFile.endswith('.lhe'):
      self.pythia8CardContent = self.pythia8CardContent.replace('Beams:LHEF = events.lhe', f'Beams:LHEF = {self.InputFile}')

    if self.executableName in ['DelphesPythia8_EDM4HEP', 'DelphesPythia8EvtGen_EDM4HEP_k4Interface']:
      res = preparePythia8Card(self.pythia8CardContent, self.NumberOfEvents, self.randomSeed, self.energy, self.pythia8Card)
      if not res['OK']:
        return res

    if self.executableName in ['DelphesPythia8EvtGen_EDM4HEP_k4Interface']:
      with open(self.evtGenCard, 'w') as scriptFile:
        scriptFile.write(self.evtGenDecCardContent)
    
    os.chmod(scriptName, 0o755)
    comm = 'bash "./%s"' % scriptName
    self.setApplicationStatus('DelphesApp %s step %s' % (self.applicationVersion, self.STEP_NUMBER))
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

  def getEnvScript(self, platform, appname, appversion):
    """Not Implemented."""
    return S_ERROR('Not implemented')

  def _determineRandomSeed(self):
    """Determine what the randomSeed should be.

    Depends on production or not.

    .. Note::
      In DelphesApp we use *randomSeed* and not *RandomSeed* as in the other workflow modules

    """
    if self.randomSeed == -1:
      self.randomSeed = int(self.jobID)
    if "IS_PROD" in self.workflow_commons:
      self.randomSeed = int('%s%s' % (self.workflow_commons["PRODUCTION_ID"],
                                      self.workflow_commons["JOB_ID"]))
    return self.randomSeed
