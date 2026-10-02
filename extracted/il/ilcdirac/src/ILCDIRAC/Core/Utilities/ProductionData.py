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
"""Utility to construct production LFNs from workflow parameters according to LHCb conventions.

:author: S. Poss
:since: Jun 16, 2010
"""

from __future__ import absolute_import
__RCSID__ = "$Id$"

import datetime
import os

from DIRAC.Core.Security.ProxyInfo import getVOfromProxyGroup
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
from DIRAC import S_OK, S_ERROR, gLogger

from ILCDIRAC.Core.Utilities.resolvePathsAndNames import getProdFilename
from ILCDIRAC.Core.Utilities.LFNPathUtilities import cleanUpLFNPath

gLogger = gLogger.getSubLogger('ProductionData')
#############################################################################


def constructProductionLFNs(paramDict):
  """Used for local testing of a workflow, a temporary measure until LFN construction is tidied.  This works using the workflow commons for on the fly construction.

  :param dict paramDict: dictionary with at least the keys ``PRODUCTION_ID``, ``JOB_ID``, ``outputList``
  :returns: S_OK with ``ProductionOutputData``, ``LogFilePath``, ``LogTargetPath``
  """
  result = checkForMandatoryKeys(paramDict, ['PRODUCTION_ID', 'JOB_ID', 'outputList'])
  if not result['OK']:
    return result

  productionID = paramDict['PRODUCTION_ID']
  jobID = paramDict['JOB_ID']
  outputList = paramDict['outputList']

  fileTupleList = []
  gLogger.verbose('outputList %s' % (outputList))
  for info in outputList:
    # Nasty check on whether the created code parameters were not updated e.g. when changing defaults in a workflow
    fileName = info['outputFile']
    # rename to take care of correct path
    fileName = getProdFilename(fileName, int(productionID), int(jobID))
    fileTupleList.append((info['outputPath'], fileName))

  # Get all LFN(s) to output data
  outputData = []
  for fileTuple in fileTupleList:
    lfn = fileTuple[0] + "/" + str(productionID).zfill(8) + "/" + str(int(jobID) // 1000).zfill(3) + "/" + fileTuple[1]
    lfn = cleanUpLFNPath(lfn)
    outputData.append(lfn)

  # Get log file path - unique for all modules

  # get First outputfile
  basePath = fileTupleList[0][0]
  # TODO adjust for ILD
  logPath = basePath + "/" + str(productionID).zfill(8) + "/LOG"

  # used for logFile upload to the LogSE
  logFilePath = [cleanUpLFNPath('%s/%s' % (logPath, str(int(jobID) // 1000).zfill(3)))]

  resLogs = getLogPath(dict(PRODUCTION_ID=productionID,
                             JOB_ID=jobID,
                             LogFilePath=logFilePath), basePath=basePath)
  if not resLogs['OK']:
    return resLogs
  logTargetPath = resLogs['Value']['LogTargetPath']
  logFilePath = resLogs['Value']['LogFilePath']

  if not outputData:
    gLogger.info('No output data LFN(s) constructed')
  else:
    gLogger.verbose('Created the following output data LFN(s):\n%s' % ('\n'.join(outputData)))
  gLogger.verbose('Log file path is:\n%s' % logFilePath[0])
  gLogger.verbose('Log target path is:\n%s' % logTargetPath[0])
  jobOutputs = {'ProductionOutputData': outputData, 'LogFilePath': logFilePath, 'LogTargetPath': logTargetPath}
  return S_OK(jobOutputs)

#############################################################################


def getLogPath(paramDict, basePath=None):
  """Can construct log file paths even if job fails e.g. no output files available.

  :param dict paramDict: dictionary with at least the keys ``PRODUCTION_ID``, ``JOB_ID``, ``LogFilePath``
  :param str basePath: Optional, base path for the log file failover, of not set LogFilePath
    from paramDict is used as a base
  :returns: S_OK with dict with LogFilePath and LogTargetPath
  """
  result = checkForMandatoryKeys(paramDict, ['PRODUCTION_ID', 'JOB_ID', 'LogFilePath'])
  if not result['OK']:
    return result

  productionID = paramDict['PRODUCTION_ID']
  jobID = paramDict['JOB_ID']
  logFileName = "%s_%s.tar" % (str(productionID).zfill(8), str(int(jobID)).zfill(4))
  if basePath:
    logTargetPath = [cleanUpLFNPath(os.path.join(basePath, "LOG", str(productionID).zfill(8), logFileName))]
  else:
    # need to built logPath from logFilePath, as it's not there, and must be as in method above
    logPathtemp = cleanUpLFNPath(paramDict['LogFilePath']).split("/")
    logPath = "/" + os.path.join(*logPathtemp[0:-1])
    logTargetPath = ['%s/%s_%s.tar' % (logPath, str(productionID).zfill(8), str(int(jobID)).zfill(3))]

  # this is not doing anything except return the same string as was passed into the function
  logFilePath = paramDict['LogFilePath']
  gLogger.verbose('Log file path is: %s' % logFilePath)
  gLogger.verbose('Log target path is: %s' % logTargetPath)
  jobOutputs = {'LogFilePath': logFilePath, 'LogTargetPath': logTargetPath}
  return S_OK(jobOutputs)

#############################################################################


def constructUserLFNs(jobID, vo, owner, outputFiles, outputPath):
  """This method is used to supplant the standard job wrapper output data policy for ILC.  The initial convention adopted for user output files is the following:

  If outputpath is not defined:
   * <vo>/user/<initial e.g. s>/<owner e.g. sposs>/<yearMonth e.g. 2010_02>/<subdir>/<fileName>
  Otherwise:
   * <vo>/user/<initial e.g. s>/<owner e.g. sposs>/<outputPath>/<fileName>

  :param int jobID: the jobID
  :param str vo: the vo of the owners proxy
  :param str owner: the username
  :param list outputFiles: the list of outputfiles found for the job
  :param str outputPath: the outputpath defined for the job
  :returns: S_OK with list of output file lfns
  """
  initial = owner[:1]
  subdir = str(jobID // 1000)
  timeTup = datetime.date.today().timetuple()
  yearMonth = '%s_%s' % (timeTup[0], str(timeTup[1]).zfill(2))
  outputLFNs = {}
  if not vo:
    res = getVOfromProxyGroup()
    if not res['OK']:
      gLogger.error('Could not get VO from CS, assuming ilc')
      vo = 'ilc'
    else:
      vo = res['Value']
  ops = Operations(vo=vo)
  lfn_prefix = ops.getValue("LFNUserPrefix", "user")
  # Strip out any leading or trailing slashes but allow fine structure
  if outputPath:
    outputPathList = outputPath.split(os.sep)
    newPath = []
    for i in outputPathList:
      if i:
        newPath.append(i)
    outputPath = os.sep.join(newPath)

  if not isinstance(outputFiles, list):
    outputFiles = [outputFiles]

  for outputFile in outputFiles:
    # strip out any fine structure in the output file specified by the user, restrict to output file names
    # the output path field can be used to describe this
    outputFile = outputFile.replace('LFN:', '')
    lfn = ''
    if outputPath:
      lfn = os.sep + os.path.join(vo, lfn_prefix, initial, owner, outputPath + os.sep + os.path.basename(outputFile))
    else:
      lfn = os.sep + os.path.join(vo, lfn_prefix, initial, owner, yearMonth, subdir,
                                  str(jobID)) + os.sep + os.path.basename(outputFile)
    outputLFNs[outputFile] = lfn

  outputData = list(outputLFNs.values())
  if outputData:
    gLogger.info('Created the following output data LFN(s):\n%s' % ('\n'.join(outputData)))
  else:
    gLogger.info('No output LFN(s) constructed')

  return S_OK(outputData)

#############################################################################
# def _makeProductionPath(JOB_ID, LFN_ROOT, typeName, mode, prodstring, log = False):
#   """ Constructs the path in the logical name space where the output
#       data for the given production will go. In
#   """
#   result = LFN_ROOT + '/' + typeName.upper() + '/' + prodstring + '/'
#   if log:
#     try:
#       jobid = int(JOB_ID)
#       jobindex = string.zfill(jobid/10000, 4)
#     except:
#       jobindex = '0000'
#     result += jobindex
#   return result

#############################################################################
# def _makeProductionLfn(JOB_ID, LFN_ROOT, filetuple, mode, prodstring):
#   """ Constructs the logical file name according to LHCb conventions.
#       Returns the lfn without 'lfn:' prepended.
#   """
#   gLogger.debug('Making production LFN for JOB_ID %s, LFN_ROOT %s, mode %s, prodstring %s for\n%s' %(JOB_ID, LFN_ROOT, mode, prodstring, str(filetuple)))
#   try:
#     jobid = int(JOB_ID)
#     jobindex = string.zfill(jobid/10000, 4)
#   except:
#     jobindex = '0000'
#   fname = filetuple[0]
#   if re.search('lfn:', fname) or re.search('LFN:', fname):
#     return fname.replace('lfn:', '').replace('LFN:', '')
#   return LFN_ROOT + '/' + filetuple[1].upper() + '/' + prodstring + '/' + jobindex + '/' + filetuple[0]


def checkForMandatoryKeys(paramDict, keys):
  """checks for mandatory keys in the paramDict.

  :param dict paramDict: dictionary to check for mandatory ``keys``
  :param list keys: list of keys that need to be in ``paramDict``
  :returns: :func:`~DIRAC.Core.Utilities.ReturnValues.S_OK`, :func:`~DIRAC.Core.Utilities.ReturnValues.S_ERROR`
  """
  for k in keys:
    if k not in paramDict:
      return S_ERROR('%s not defined' % k)
  return S_OK()


def getExperimentFromPath(logger, exampleFile, defaultExperiment):
  """returns the experiment based on the base paths defined in the CS.

  Find experiment based on the basepaths defined in Operations/Production/ExperimentBasePaths

  :param logger: logging instance
  :param str exampleFile: file to match
  :param str defaultExperiment: experiment to return if no match
  :returns: experiment string
  """
  basePaths = Operations().getOptionsDict('Production/ExperimentBasePaths')
  if not basePaths['OK']:
    logger.warn("Could not get ExperimentBasePaths", basePaths['Message'])
  else:
    for experiment, paths in basePaths['Value'].items():
      for path in paths.split(','):
        if exampleFile.startswith(path.strip()):
          logger.info("Found experiment %s for %s matching %s" % (experiment, path, exampleFile))
          return experiment

  logger.warn("Failed to determine experiment, reverting to default: %s" % defaultExperiment)
  return defaultExperiment

#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#
