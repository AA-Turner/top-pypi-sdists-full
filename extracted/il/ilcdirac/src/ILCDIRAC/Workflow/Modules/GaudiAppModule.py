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
"""Run a GaudiApp."""

from __future__ import absolute_import
import os

from DIRAC.Core.Utilities.Subprocess import shellCall
from DIRAC import S_OK, S_ERROR, gLogger
from ILCDIRAC.Core.Utilities.CombinedSoftwareInstallation import getEnvironmentScript
from ILCDIRAC.Core.Utilities.resolvePathsAndNames import resolveIFpaths, getProdFilename
from ILCDIRAC.Workflow.Modules.ModuleBase import ModuleBase
from ILCDIRAC.Workflow.Utilities.DD4hepMixin import DD4hepMixin
from ILCDIRAC.Core.Utilities.PrepareOptionFiles import preparePythia8Card


__RCSID__ = '$Id$'
LOG = gLogger.getSubLogger(__name__)


class GaudiAppModule(DD4hepMixin, ModuleBase):
  """Specific Module to run a Gaudi job."""

  def __init__(self):
    super(GaudiAppModule, self).__init__()
    self.enable = True
    self.STEP_NUMBER = ''
    self.result = S_ERROR()
    self.applicationName = 'gaudiapp'
    self.executableName = ''
    self.startFrom = 0
    self.randomSeed = -1
    self.randomSeedFlag = ''
    self.inputFileFlag = ''
    self.outputFileFlag = ''
    self.compactFile = ''
    self.detectorModel = ''
    self.detectorModelFlag = '--GeoSvc.detectors'
    self.pythia8CardContent = ''
    self.pythia8Card = 'pythia8card.cmd'
    self.eventstring = ['+++ Initializing event']  # FIXME

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

    - if necessary find the detector model xml, using CS query to obtain the path
    - if necessary prepare the pythia card
    - prepare the run script using the input parameters
    - run GaudiApp on the steering eventually using the prepared pythia card and/or the input files

    :returns: :func:`~DIRAC.Core.Utilities.ReturnValues.S_OK`, :func:`~DIRAC.Core.Utilities.ReturnValues.S_ERROR`
    """
    self.result = S_OK()
    if not self.platform:
      self.result = S_ERROR('No ILC platform selected')
    elif not self.applicationLog:
      self.result = S_ERROR('No Log file provided')
    elif not self.executableName:
      self.result = S_ERROR('No executable name provided')
    if not self.result['OK']:
      LOG.error("Failed to resolve input parameters:", self.result['Message'])
      return self.result

    if not self.workflowStatus['OK'] or not self.stepStatus['OK']:
      LOG.verbose('Workflow status = %s, step status = %s' % (self.workflowStatus['OK'], self.stepStatus['OK']))
      return S_OK('GaudiApp should not proceed as previous step did not end properly')

    # TODO: Setup LD_LIBRARY_PATH for extensions
    res = getEnvironmentScript(self.platform, self.applicationName, self.applicationVersion, self.getEnvScript)
    if not res['OK']:
      LOG.error("Could not obtain the environment script: ", res["Message"])
      return res
    envScriptPath = res["Value"]

    # get the path to the detector model, either local or from the software
    if self.detectorModel:
      resXML = self._getDetectorXML()
      if not resXML['OK']:
        LOG.error("Could not obtain the detector XML file: ", resXML["Message"])
        return resXML
      self.compactFile = resXML['Value']

    if self.InputFile:
      res = resolveIFpaths(self.InputFile)
      if not res['OK']:
        LOG.error("InputFile file not found")
        return res
      self.InputFile = res['Value']

    # if steering file is set try to find it
    if self.SteeringFile:
      self.SteeringFile = os.path.basename(self.SteeringFile)
      if not os.path.exists(self.SteeringFile):
        LOG.error("Missing steering file")
        return S_ERROR("Could not find steering file")

    cmd = []
    if self.InputFile:
      cmd.append(" %s %s" % (self.inputFileFlag, ' '.join(self.InputFile)))

    if self.NumberOfEvents:
      cmd.append("-n %s" % self.NumberOfEvents)

    if self.compactFile:
      cmd.append("%s %s" % (self.detectorModelFlag, self.compactFile))

    if self.randomSeedFlag:
      cmd.append("%s %s" % (self.randomSeedFlag, self.randomSeed))

    cmd.append("%s %s" % (self.outputFileFlag, self.OutputFile))

    scriptName = 'GaudiApp_%s_Run_%s.sh' % (self.applicationVersion, self.STEP_NUMBER)
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
    script.append('echo gaudiApp:`which %s`' % self.executableName)
    script.append('echo =========')
    comm = '%(executable)s %(steeringFile)s %(args)s %(extraArgs)s ' % \
        dict(executable=self.executableName,
             args=' '.join(cmd),
             extraArgs=self.extraCLIarguments,
             steeringFile=self.SteeringFile,
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

    if self.pythia8CardContent:
      res = preparePythia8Card(self.pythia8CardContent, self.NumberOfEvents, self.randomSeed, self.energy, self.pythia8Card)
      if not res['OK']:
        return res
    
    os.chmod(scriptName, 0o755)
    comm = 'bash "./%s"' % scriptName
    self.setApplicationStatus('GaudiApp %s step %s' % (self.applicationVersion, self.STEP_NUMBER))
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
      In GaudiApp we use *randomSeed* and not *RandomSeed* as in the other workflow modules

    """
    if self.randomSeed == -1:
      self.randomSeed = int(self.jobID)
    if "IS_PROD" in self.workflow_commons:
      self.randomSeed = int('%s%s' % (self.workflow_commons["PRODUCTION_ID"],
                                      self.workflow_commons["JOB_ID"]))
    return self.randomSeed
