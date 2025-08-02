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
"""Run Whizard2.

:author: Marko Petric
:since:  June 29, 2015
"""

from __future__ import absolute_import
import os
import re

from DIRAC.Core.Utilities.Subprocess import shellCall
from DIRAC.DataManagementSystem.Client.DataManager import DataManager
from DIRAC import S_OK, S_ERROR, gLogger
from ILCDIRAC.Workflow.Modules.ModuleBase import ModuleBase
from ILCDIRAC.Core.Utilities.CombinedSoftwareInstallation import getEnvironmentScript, extractTarball
from ILCDIRAC.Core.Utilities.resolvePathsAndNames import getProdFilename

__RCSID__ = '$Id$'
LOG = gLogger.getSubLogger(__name__)


class Whizard2Analysis(ModuleBase):
  """Specific Module to run a Whizard2 job."""

  def __init__(self):
    super(Whizard2Analysis, self).__init__()
    self.enable = True
    self.STEP_NUMBER = ''
    self.result = S_ERROR()
    self.applicationName = 'whizard2'
    self.startFrom = 0
    self.randomSeed = -1
    self.whizard2SinFile = ''
    self.whizard2RawSin = False
    self.eventstring = ['+++ Generating event']
    self.decayProc = ['decay_proc']
    self.integratedProcess = ''
    self.datMan = DataManager()

  def applicationSpecificInputs(self):
    """Resolve all input variables for the module here.

    :return: S_OK()
    """
    self.randomSeed = self._determineRandomSeed()

    if "IS_PROD" in self.workflow_commons and self.workflow_commons["IS_PROD"]:
      self.OutputFile = getProdFilename(self.OutputFile,
                                        int(self.workflow_commons["PRODUCTION_ID"]),
                                        int(self.workflow_commons["JOB_ID"]),
                                        self.workflow_commons,
                                       )

    return S_OK('Parameters resolved')

  def resolveIntegratedProcess(self):
    """Check if integrated process is set and act accordingly.

    If the integrated process was given as a tarball it should already be available in the working directory and we do
    nothing.
    """
    if not self.integratedProcess:
      return S_OK()

    # integratedProcess is set, check CVMFS or filecatalog
    processes = self.ops.getOptionsDict('/AvailableTarBalls/%s/whizard2/%s/integrated_processes/processes' %
                                        ('x86_64-slc5-gcc43-opt', self.applicationVersion))

    if not processes['OK']:
      LOG.error('Could not resolve known integrated processes', processes['Message'])
      return processes

    options = self.ops.getOptionsDict('/AvailableTarBalls/%s/whizard2/%s/integrated_processes' %
                                      ('x86_64-slc5-gcc43-opt', self.applicationVersion))
    if not options['OK']:
      LOG.error('Failed to get integrated processes options', options['Message'])
      return options

    cvmfsPath = options['Value'].get('CVMFSPath', '')
    tarballURL = options['Value'].get('TarBallURL', '')
    processTarball = processes['Value'].get(self.integratedProcess, '')

    localTarball = os.path.join(cvmfsPath, processTarball)
    if os.path.exists(localTarball):
      LOG.info('Tarball found on cvmfs: %r' % localTarball)
      return extractTarball(localTarball, os.getcwd())

    tarballLFN = os.path.join(tarballURL, processTarball)
    LOG.info('Trying to download tarball', tarballLFN)
    getFile = self.datMan.getFile(tarballLFN)
    if not getFile['OK']:
      LOG.error('Failed to download tarball', getFile['Message'])
      return getFile
    return extractTarball(os.path.split(tarballLFN)[1], os.getcwd())

  def runIt(self):
    """Called by JobAgent.

    Execute the following:
      - get the environment variables that should have been set during installation
      - prepare the steering file and command line parameters
      - run Whizard2 on this steering file and catch the exit status

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
      return S_OK('Whizard2 should not proceed as previous step did not end properly')

    resIntProc = self.resolveIntegratedProcess()
    if not resIntProc['OK']:
      return resIntProc

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

    whizard2SteerName = 'Whizard2_%s_Steer_%s.sin' % (self.applicationVersion, self.STEP_NUMBER)
    if os.path.exists(whizard2SteerName):
      os.remove(whizard2SteerName)

    whizard2Steer = []
    whizard2Steer.append('!Seed set via API')
    whizard2Steer.append('seed = %s' % self.randomSeed)
    whizard2Steer.append('')
    whizard2Steer.append('!Parameters set via whizard2SinFile')
    whizard2Steer.append('')
    whizard2Steer.append('')
    whizard2Steer.append(self.whizard2SinFile)
    whizard2Steer.append('')
    if not self.whizard2RawSin:
      whizard2Steer.append('!Number of events set via API')
      whizard2Steer.append('')
      whizard2Steer.append('n_events = %s' % self.NumberOfEvents)
      whizard2Steer.append('')
      whizard2Steer.append('simulate (%s) {' % ','.join(self.decayProc))
      whizard2Steer.append('        $sample = "%s"' % self.OutputFile.rsplit('.', 1)[0])
      # https://whizard.hepforge.org/manual/ , more specifically: https://whizard.hepforge.org/manual.pdf , chapter variables.
      if self.OutputFile.rsplit('.', 1)[-1] == 'slcio':
        whizard2Steer.append('        sample_format = lcio')
        whizard2Steer.append('        $extension_lcio = "slcio"')
      elif self.OutputFile.rsplit('.', 1)[-1] == 'lhe':
        whizard2Steer.append('        sample_format = lhef')
        whizard2Steer.append('        $lhef_extension = "lhe"')
      else:
        whizard2Steer.append('        sample_format = %s' % self.OutputFile.rsplit('.', 1)[-1])
        whizard2Steer.append('        $extension_{st} = "{st}"'.format(st=self.OutputFile.rsplit('.', 1)[-1]))
      whizard2Steer.append('}')

    with open(whizard2SteerName, 'w') as steerFile:
      steerFile.write("\n".join(whizard2Steer))

    scriptName = 'Whizard2_%s_Run_%s.sh' % (self.applicationVersion, self.STEP_NUMBER)
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
    script.append('echo whizard:`which whizard`')
    script.append('echo =========')
    script.append('whizard %s' % whizard2SteerName)
    script.append('declare -x appstatus=$?')
    script.append(f'cp {self.OutputFile} events.{self.OutputFile.rsplit(".", 1)[-1]}')
    script.append('exit $appstatus')

    with open(scriptName, 'w') as scriptFile:
      scriptFile.write("\n".join(script))

    if os.path.exists(self.applicationLog):
      os.remove(self.applicationLog)

    os.chmod(scriptName, 0o755)
    comm = 'bash "./%s"' % scriptName
    self.setApplicationStatus('Whizard2 %s step %s' % (self.applicationVersion, self.STEP_NUMBER))
    self.stdError = ''
    self.result = shellCall(0, comm, callbackFunction=self.redirectLogOutput, bufferLimit=20971520)
    resultTuple = self.result['Value']
    if not os.path.exists(self.applicationLog):
      LOG.error("Something went terribly wrong, the log file is not present")
      self.setApplicationStatus('%s failed to produce log file' % (self.applicationName))
      if not self.ignoreapperrors:
        return S_ERROR('%s did not produce the expected log %s' % (self.applicationName, self.applicationLog))
    status = resultTuple[0]

    res = self._analyseTheLog()
    if not res['OK']:
      status = 1
      LOG.error("Failed to analyse the log file", res['Message'])
    LOG.info("Status after the application execution is %s" % status)

    return self.finalStatusReport(status)

  def _determineRandomSeed(self):
    """determine what the randomSeed should be, depends on production or not.

    .. Note::
      Whizard2 we use *randomSeed* and not *RandomSeed* as in the other workflow modules
    """
    if self.randomSeed == -1:
      self.randomSeed = self.jobID
    if "IS_PROD" in self.workflow_commons:
      self.randomSeed = int(
          str(
              int(
                  self.workflow_commons["PRODUCTION_ID"]))
          + str(
              int(
                  self.workflow_commons["JOB_ID"])))
    else:
      self.randomSeed = int(self.randomSeed)
    if self.randomSeed > 4294967295: # whizard does not accept seed > 4294967296
      self.randomSeed = self.randomSeed % 4294967295
    return self.randomSeed

  def _analyseTheLog(self):
    """Extract luminosity, cross section, efficiency, from the log files"""
    info = {'xsection': {'sum': {}}}
    with open(self.applicationLog) as logfile:
      fullog = logfile.read()

      # Luminosity
      # The regex matches something that looks like "corr. to luminosity [fb-1] =   1.2792E+02" and extracts the value
      pattern = r'corr. to luminosity \[fb-1\] =\s+(\d+\.\d+E[+-]\d+)' #
      match = re.search(pattern, fullog)
      if not match:
        return S_ERROR('luminosity not found')
      lumi = match.groups()[0]
      LOG.info(f'The sample generated has an equivalent luminosity of {lumi}.')
      self.workflow_commons['Luminosity'] = float(lumi)

      # Xsection, Xsec error, fraction
      # The regex matches something like the following, and extracts values from the central row. 
      # |-----------------------------------------------------------------------------|
      #   17      69993  7.8172284E-02  1.32E-04    0.17    0.45   19.12    0.41   7
      # |=============================================================================|
      # The values correspond to the following labels:
      #   It      Calls  Integral[fb]  Error[fb]   Err[%]    Acc  Eff[%]   Chi2 N[It]
      # find a line wedged between a |{'-'*70}| line and a |{'='*70}| line
      #                   iter.   calls  | Integral       |   |  int error     |   |perc err|   |do not care about the rest
      pattern = r'-{70,}\|\s+\d+\s+\d+\s+(\d+\.\d+E[+-]\d+)\s+(\d+\.\d+E[+-]\d+)\s+(\d+\.\d+)\s+\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\d+\s+\|={70,}'
      match = re.search(pattern, fullog)
      if not match:
        return S_ERROR('cross section not found')
      xsec, xsecerr, fraction= match.groups()

      info['xsection']['sum']['xsection'] = float(xsec)
      info['xsection']['sum']['err_xsection'] = float(xsecerr)
      info['xsection']['sum']['fraction'] = float(fraction)
      LOG.info(f'The sample generated has a cross section of {xsec} +- {xsecerr} fb.')
      LOG.info(f'The sample generated has a fraction of {fraction}')

      # Efficiency, Eff info
      # The regex matches something that looks like "actual unweighting efficiency =  15.15 %" and extracts the value
      pattern = r'actual unweighting efficiency =\s+(\d+.\d+)\s+%'
      match = re.search(pattern, fullog)
      if not match:
        return S_ERROR('efficiency not found')
      efficiency = match.groups()[0]
      info['efficiency'] = float(efficiency)
      info['efficiency-info'] = ''
      LOG.info(f'The sample generated has an efficiency of {efficiency} %')

      if 'Info' not in self.workflow_commons:
        self.workflow_commons['Info'] = info
      else:
        self.workflow_commons['Info'].update(info)

    return S_OK()
