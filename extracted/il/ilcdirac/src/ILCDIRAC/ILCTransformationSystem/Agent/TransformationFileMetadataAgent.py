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
"""The TransformationFileMetadata agent writes a information about transformation files into a json file

The information for the transformation is about the number of files, events, luminsoty, and cross-section, as required
for FCC analysers.  The json file is made available via a grid storage element.

:since: Nov 7, 2023
:author: lorenzo valentini

"""

from DIRAC import S_OK, S_ERROR, gLogger, gConfig
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
from DIRAC.ConfigurationSystem.Client.Helpers.Registry import getVOOption
from DIRAC.Core.Base.AgentModule import AgentModule
from DIRAC.Core.Utilities.List import breakListIntoChunks
from DIRAC.Core.Utilities.Proxy import executeWithUserProxy
from DIRAC.Core.Utilities.ReturnValues import returnSingleResult
from DIRAC.DataManagementSystem.Client.DataManager import DataManager
from DIRAC.Interfaces.API.Dirac import Dirac
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
from DIRAC.TransformationSystem.Client.TransformationClient import TransformationClient

import os
import json
import tarfile
from collections import defaultdict
from datetime import datetime, timezone, timedelta
import numpy
from uncertainties import unumpy
from pprint import pformat, pprint

def getFileInfo(lfn, metadata):
  """Retrieve the file info.

  :returns: Dictionary with lumi, nbevts, xsec, xsecerror, efficiency for given file.
  """
  from DIRAC.Core.Utilities import DEncode

  lumi = 0.0
  nbevts = 0
  xsec = 0.0
  xsercerror = 0.0

  if not metadata:
    gLogger.error("There is no metadata for", lfn)
    return {}

  lumi += float(metadata.get('Luminosity', 0.0))
  nbevts += int(metadata.get('NumberOfEvents', 0))

  addinfo = {}
  if (addinfo := metadata.get("AdditionalInfo", {})):
    if '{' in addinfo:
      addinfo = eval(addinfo)
    else:
      addinfo = DEncode.decode(addinfo.encode())[0]
  gLogger.debug("Additional info for:", f"{lfn}: {addinfo}")
  xsec = addinfo.get('xsection', {}).get('sum', {}).get('xsection', 0.0)
  xsecerror = addinfo.get('xsection', {}).get('sum', {}).get('err_xsection', 0.0)
  fraction = addinfo.get('xsection', {}).get('sum', {}).get('fraction', 0.0)
  retVal = dict(lumi=float(lumi),
                nbevts=int(nbevts),
                xsection=float(xsec),
                xsectionerror=float(xsecerror),
                efficiency=float(fraction),
                )
  return retVal


class TransformationFileMetadataAgent(AgentModule):
  """Main class of the TFMA"""

  def __init__(self, *args, **kwargs):
    """Constructor."""
    AgentModule.__init__(self, *args, **kwargs)
    self.name = "TransformationFileMetadataAgent"
    self.trc = None
    self.ops = None
    self.fc = None
    self.transfLevelJsonName = 'fcc_ee_transf_info.json'
    self.transfLevelTarName = 'fcc_ee_transf_info.tar.gz'
    self.transfLevelTarDestination = os.path.join('/fcc/ee/', self.transfLevelTarName)
    self.transfInfoSE = 'CERN-DST-EOS'
    self.condDict = {'Status': ['New',
                                'Active',
                                'Stopped',
                                'Flush',
                                'Completing',
                                'Completed',
                                ],
                     'AuthorGroup': 'fcc_prod',
                     'Type': ['MCReconstruction',
                              'MCReconstruction_Overlay',
                              'MCGeneration',
                              'MCSimulation',
                              ]
                     }

  def initialize(self):
    """Sets defaults"""

    self.fc = FileCatalogClient()
    self.trc = TransformationClient()
    self.ops = Operations()
    self.dirac = Dirac()
    self.dm = DataManager()

    res = gConfig.getSections("/Registry/VO")
    if not res["OK"]:
        return S_ERROR(res['Message'])
    self.voList = res["Value"]
    # FIXME: make this configurable?
    self.voAdminUser = getVOOption('fcc', "VOAdmin")
    self.voAdminGroup = getVOOption('fcc', "VOAdminGroup", getVOOption('fcc', "DefaultGroup"))

    gLogger.info('Will consider the following transformation kinds:', pformat(self.condDict))
    gLogger.info('*********************** Running ***********************')

    return S_OK()
      
  def loopThroughFiles(self, transformation, path):
    """Loop over all the files gettint their meta data and collating it."""
    meta = {}
    meta['ProdID'] = transformation['TransformationID']
    res = self.fc.getCompatibleMetadata(meta)
    if not res['OK']:
      return res
    if not res['Value'].get('Datatype'):
      return S_ERROR("Error while looking for output directories paths: no information about transformation 'Datatype'")
    # FIXME: replace directory with delphes if we have delphes
    # FIXME: we get the path, which already contains a datatype, should check via SubDirs etc. if we need to switch to delphes or not?
    meta['Datatype'] = 'delphes' if 'delphes' in res['Value']['Datatype'] else res['Value']['Datatype'][0]

    gLogger.info("Getting files for the path", f"{path}")
    res = returnSingleResult(self.fc.listDirectory(path))
    if not res["OK"]:
      gLogger.error("Failed to find directories:", res["Message"])
      return res
    allLfns = []
    for subDir in res['Value']['SubDirs']:
      res = returnSingleResult(self.fc.listDirectory(subDir))
      if not res['OK']:
        gLogger.error("Failed getting files for", f"{subDir}: {res['Message']}")
        return res
      allLfns.extend(list(res['Value']['Files'].keys()))
    gLogger.info("Number of files found:", len(allLfns))
    # '/fcc/ee/test_spring2024/240gev/Hbb/CLD_o2_v05/rec/00016562/010/Hbb_rec_16562_10070.root':
    # {'Size': 134674358,
    #  'UID': 8048,
    #  'GID': 30,
    #  'Status': 'AprioriGood',
    #  'GUID': 'D71194F0-3840-A730-9162-68B0D0AD73F7',
    #  'CreationDate': datetime.datetime(2024, 6, 29, 16, 36, 17),
    #  'Metadata': {'NumberOfEvents': '100'}},
    allDetails = {}
    for index, lfnChunk in enumerate(breakListIntoChunks(allLfns, 1000)):
      details = self.fc.getFileDetails(lfnChunk, LFNChecking=False)  # pylint: disable=unexpected-keyword-arg
      if not details['OK']:
        gLogger.error("Failed to get FileDetails", details['Message'])
        return details
      if "Successful" in details['Value']:
        allDetails.update(details['Value']["Successful"])
      else:
        allDetails.update(details['Value'])

    gLogger.info("Got info for this number of files:", len(allDetails))

    if not allDetails:
      gLogger.error("Got no details")
      return S_ERROR('No files found for the transformation')

    lumi = 0.
    nbevts = 0
    xseclist = []
    xsecerrlist = []
    efficiencylist = []
    for lfn, lfnMeta in allDetails.items():
      gLogger.debug("Trying to get info out of", lfnMeta.get('Metadata'))
      info = getFileInfo(lfn, lfnMeta.get('Metadata'))
      nbevts += info.get('nbevts', 0)
      lumi += info.get('lumi', 0)
      if (xsection := info.get('xsection')) and (xsecerror := info.get('xsectionerror')):
        xseclist.append(xsection)
        xsecerrlist.append(xsecerror)
      if (efficiency := info.get('efficiency')):
        efficiencylist.append(efficiency)
      # efficiencyInfo WHAT TO DO WITH THIS?

    if (not lumi) and (transformation['Type'] != 'MCGeneration'):
      gLogger.info('The transformation is not MCGeneration: Looking at ancestors for detailed info.')
      depthDict = defaultdict(set)
      gLogger.verbose("Looking for ancestors of this many files", len(allLfns))
      for index, lfnChunk in enumerate(breakListIntoChunks(allLfns, 1000)):
        gLogger.verbose('Looking at chunk %s/%s' % (index, len(allLfns) // 1000))
        res = self.fc.getFileAncestors(lfnChunk, [1, 2, 3, 4])
        if not res['OK']:
          gLogger.error('failed to find ancenstors')
          return res
        for lfn, ancestorsDict in res['Value']['Successful'].items():
          for ancestor, dep in ancestorsDict.items():
            depthDict[dep].add(ancestor)
      oldestAncestorID = sorted(depthDict)[-1]
      oldestAncestors = depthDict[oldestAncestorID]
      gLogger.info("Found this number of ancestors", len(oldestAncestors))
      for index, lfnChunk in enumerate(breakListIntoChunks(oldestAncestors, 1000)):
        gLogger.debug("Getting info for ancestor:", index)
        details = self.fc.getFileDetails(lfnChunk, LFNChecking=False)  # pylint: disable=unexpected-keyword-arg
        if not details['OK']:
          gLogger.error("Failed to get ancestor information", details['Message'])
          return details
        if "Successful" not in details["Value"]:
          theDetails = details["Value"]
        else:
          theDetails = details["Value"]["Succcesful"]
        gLogger.debug("Successfully got ancestor information")
        for lfn, lfnMeta in theDetails.items():
          info = getFileInfo(ancestor, lfnMeta.get('Metadata'))
          if not any(info.values()):
            gLogger.info('Files do not have detailed info here either.')
            break
          nbevts += info.get('nbevts', 0)
          lumi += info.get('lumi', 0)
          if (xsec := info.get('xsection')) and (xsecerror := info.get('xsectionerror')):
            xseclist.append(xsec)
            xsecerrlist.append(xsecerror)
          if (efficiency := info.get('efficiency')):
            efficiencylist.append(efficiency)
          # efficiencyInfo WHAT TO DO WITH THIS?


    xsecs = unumpy.uarray(xseclist, xsecerrlist)
    xsecerrs = unumpy.uarray(xsecerrlist, [0]*len(xsecerrlist))
    xsec = sum(xsecs/xsecerrs)/sum(1/xsecerrs) if len(xsecs) else 0.0
    CrossSection = unumpy.nominal_values(xsec) if len(xsecs) else 0.0
    CrossSectionError = unumpy.std_devs(xsec) if len(xsecs) else 0.0

    Efficiency = numpy.average(efficiencylist) if len(efficiencylist) else 0.0
    EfficiencyInfo = 'FIXME: no idea of what to put here'

    result = {'cross-section': float(CrossSection),
              'cross-section-error': float(CrossSectionError),
              'efficiency': Efficiency,
              'efficiency-info' : EfficiencyInfo,
              'total-number-of-events': nbevts,
              }

    return S_OK(result)

  def makeInfoDictFromTransf(self, transformation):
    """
    Creates and fills the dictionary with all the information relative to each transformation to edit in the json
    """
    transfInfoDict = {}

    gLogger.debug("Transformation info", pformat(transformation))
    # MaxNumberOfTasks is only defined for MCGeneration
    numberOfTasks = transformation.get('MaxNumberOfTasks', None)
    eventsPerTask = transformation.get('EventsPerTask', None)
    totalNumberOfEvents = int(numberOfTasks)*int(eventsPerTask) if (eventsPerTask and numberOfTasks) else None

    transfInfoDict['Status'] = transformation.get('Status', None)
    transfInfoDict['total-number-of-events'] = totalNumberOfEvents
    transfInfoDict['number-of-events-per-file'] = eventsPerTask
    transfInfoDict['production-manager'] = transformation.get('AuthorDN', None)

    keys = list(transfInfoDict.keys())
    gLogger.info('Extracting values from the transformation with keys:',  ', '.join(keys))
    for key in keys:
      if not transfInfoDict[key]:
        gLogger.warn("No value found for:", key)

    gLogger.info("Taking 'path' value from filecatalog.")
    res = self.fc.findDirectoriesByMetadata({'ProdID': transformation['TransformationID']}, '/')
    manyPaths = res.get('Value', None)
    # Key not needed, at least not actively used
    mainPaths = {key: value for key, value in manyPaths.items() if value.endswith(str(transformation['TransformationID']))}
    if not mainPaths:
      gLogger.error("No output directories found for transformation", transformation['TransformationID'])
      return S_ERROR("No output directories found")
    gLogger.info("Main paths for Transformation", mainPaths)
    transfInfoDict['path'] = list(mainPaths.values())[0]
    if not res["OK"]:
      gLogger.warn("Problem while looking for output directories paths, Value for 'path' not found.:", res["Message"])

    gLogger.info('Retrieving remaining information by looping through output files metadata.')
    res = self.loopThroughFiles(transformation, transfInfoDict['path'])
    if not res["OK"]:
      gLogger.warn('Problem while looping through files:', res["Message"])
      res['Value'] = {}
    transfInfoDict['cross-section'] = res['Value'].get('cross-section', None)
    transfInfoDict['cross-section-error'] = res['Value'].get('cross-section-error', None)
    transfInfoDict['efficiency'] = res['Value'].get('efficiency', None)
    transfInfoDict['efficiency-info'] = res['Value'].get('efficiency-info', None)
    transfInfoDict['total-number-of-events'] = res['Value'].get('total-number-of-events',
                                                                transfInfoDict['total-number-of-events'])

    return S_OK(transfInfoDict)

  @executeWithUserProxy
  def noProxyExecute(self):
    """Run it!"""

    now = datetime.now(timezone.utc)
    result = self.dirac.getFile(self.transfLevelTarDestination)
    if not result["OK"]:
      gLogger.warn('Failed to download the compressed json from the grid from the grid', result["Message"])
      # we can handle the missing json file
    else:
      gLogger.info('Downloaded the compressed json from the grid')
      with tarfile.open(self.transfLevelTarName, 'r') as tar:
          tar.extractall('.')

    last_file_update = None
    if os.path.exists(self.transfLevelJsonName):
      with open(self.transfLevelJsonName, 'r') as file:
        transfJson = json.load(file)
      last_file_update = datetime.strptime(transfJson['last_file_update'], '%Y-%m-%d %H:%M:%S.%f%z')
    else:
      gLogger.error('The transformation level json does not exist.')
      transfJson = {'last_file_update': '',
                    'transformations': {},
                    }
    #   return S_ERROR(f'The transformation level json does not exist.')

    gLogger.info('Getting transformations from Transformation Client')
    res = self.trc.getTransformations(self.condDict)
    if not res["OK"]:
      gLogger.error('Error while getting transformations from Transformation Client', res["Message"])
      return res
    currentTransf = res['Value']
    gLogger.info('The following transformations have been received:',  ', '.join(str(transf["TransformationID"]) for transf in currentTransf))

    for index, transf in enumerate(currentTransf):
      
      prodID = transf['TransformationID']
      gLogger.info(f'+++++++++++++++++++++++ Processing {prodID} ({index}/ {len(currentTransf)}) +++++++++++++++++++++++')

      if last_file_update and (transf['Status'] in ['Completed']) and (transf['LastUpdate'].replace(tzinfo=timezone.utc) - last_file_update < timedelta(days=0)):
        gLogger.warn('Nothing new happened since the last update. Skipping')
        continue

      # Creating the new dictionary with the info of the specific transformation, to be inserted into the main json
      try:
        res = self.makeInfoDictFromTransf(transf)
        if not res["OK"]:
          gLogger.error(f'While getting information about the transformation, the following happened: {res["Message"]}')
          continue
      except Exception as e:
        gLogger.exception("Exception during makeInfoDict")
      # Updating the cached dictionary with the new values
      # If some new value is None, the old value is kept
      if prodID not in transfJson['transformations']:
        transfJson['transformations'][prodID] = {'Status': None,
                                                 'Version': 0,
                                                 'cross-section': None, # dirac         FIXME
                                                 'cross-section-error': None, # dirac         FIXME
                                                 'efficiency': None, # dirac          FIXME
                                                 'efficiency-info': None, # dirac ?         FIXME
                                                 'total-number-of-events': None, # dirac
                                                 'number-of-events-per-file': None, # dirac
                                                 'production-manager': None, # dirac
                                                 'path': None, # dirac
                                                }

      gLogger.info('Updating any pre-existing information with the new transformation information.')
      mergedDict = {k: res['Value'][k] if (k in res['Value'] and res['Value'][k]) else v for k, v in transfJson['transformations'][prodID].items()}
      mergedDict.update({k: v for k, v in res['Value'].items() if (v is not None or k not in mergedDict)})
      transfJson['transformations'][prodID] = mergedDict
      gLogger.info('The total information for the transformation is:', pformat(mergedDict))

    # Saving and uploading the current version of the transformations json
    transfJson['last_file_update'] = str(now)
    with open(self.transfLevelJsonName, 'w') as file:
      json.dump(transfJson, file)
    with tarfile.open(self.transfLevelTarName, 'w:gz') as tar:
      tar.add(self.transfLevelJsonName)
    gLogger.info('Finished updating and compressing the transformation level json',
                 f'({self.transfLevelJsonName} -> {self.transfLevelTarName}) with the new information as of {now}')

    res = self.dm.putAndRegister(self.transfLevelTarDestination, self.transfLevelTarName, self.transfInfoSE, overwrite=True)
    if not res['OK']:
      gLogger.error('Failure while uploading metadata json', res["Message"])
    else:
      gLogger.info('Successfully uploaded the json file to the grid')

    return S_OK()

  def execute(self):
    try:
      res = self.noProxyExecute(proxyUserName = self.voAdminUser, proxyUserGroup = self.voAdminGroup) # pylint: disable=unexpected-keyword-arg
    except Exception as e:
      gLogger.error("Exception", repr(e))
      gLogger.exception("Exception during execution")
    return res
