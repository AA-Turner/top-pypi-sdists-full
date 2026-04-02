#!/bin/env python
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
"""Prepare the production summary tables.

Obtains the list of known detectors and their summary-table titles from the /Operations/Transformation/TablesTitles section in the Configuration System.

Options:
   -P, --prods prodID            Productions: greater than with gt1234, range with 32-56, list with 34,56
   -p, --precise_detail          Precise detail, slow
   -t, --types prodTypeList      Production Types, comma separated, default all
   -S, --Statuses statusList     Statuses, comma separated, default all
   -N, --sample_size             The number of generator files to sample for cross-section and "luminosity, default 100
"""
from __future__ import absolute_import
from six.moves import range
__RCSID__ = "$Id$"

from collections import defaultdict
import os
import random
import textwrap

from DIRAC.Core.Base.Script import Script
from DIRAC.Core.Utilities.List import breakListIntoChunks
from DIRAC import S_OK, exit as dexit, S_ERROR
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations

def _getFileInfo(lfn, fc):
  """Retrieve the file info."""
  from DIRAC.Core.Utilities import DEncode
  from DIRAC import gLogger
  lumi = 0.0
  nbevts = 0
  res = fc.getFileUserMetadata(lfn)
  if not res['OK']:
    gLogger.error("Failed to get metadata of %s" % lfn)
    return (0, 0, {})

  lumi += float(res['Value'].get('Luminosity', 0.0))
  nbevts += int(res['Value'].get('NumberOfEvents', 0))

  addinfo = {}
  if 'AdditionalInfo' in res['Value']:
    addinfo = res['Value']['AdditionalInfo']
    if addinfo.count("{"):
      addinfo = eval(addinfo)
    else:
      addinfo = DEncode.decode(addinfo.encode())[0]
  xsec = addinfo.get('xsection', {}).get('sum', {}).get('xsection', 0.0)
  return (float(lumi), int(nbevts), float(xsec))

def _addDetectorOutputs(detector):
  """Adds all the possible outputs to a new detector."""
  detector.update({'SIM': [],
                  'REC': [],
                  'DST': [],
                  'delphes': [],
                  'fastsim': [],
                  'sim': [],
                  'rec': [],
                  'phys': [],
                  })
  return detector

def _translate(detail):
  """Replace whizard naming convention by human conventions."""
  detail = detail.replace('v', 'n1:n2:n3:N1:N2:N3')
  detail = detail.replace('qli', 'u:d:s:U:D:S')
  detail = detail.replace('ql', 'u:d:s:c:b:U:D:S:C:B')
  detail = detail.replace('q', 'u:d:s:c:b:t')
  detail = detail.replace('Q', 'U:D:S:C:B:T')
  detail = detail.replace('e1', 'e-')
  detail = detail.replace('E1', 'e+')
  detail = detail.replace('e2', 'mu-')
  detail = detail.replace('E2', 'mu+')
  detail = detail.replace('e3', 'tau-')
  detail = detail.replace('E3', 'tau+')
  detail = detail.replace('n1', 'nue')
  detail = detail.replace('N1', 'nueb')
  detail = detail.replace('n2', 'numu')
  detail = detail.replace('N2', 'numub')
  detail = detail.replace('n3', 'nutau')
  detail = detail.replace('N3', 'nutaub')
  detail = detail.replace('U', 'ubar')
  detail = detail.replace('C', 'cbar')
  detail = detail.replace('T', 'tbar')
  detail = detail.replace('tbareV', 'TeV')
  detail = detail.replace('D', 'dbar')
  detail = detail.replace('S', 'sbar')
  detail = detail.replace('B', 'bbar')
  detail = detail.replace('Z0', 'Z')
  detail = detail.replace('Z', 'Z0')
  detail = detail.replace('gghad', 'gamma gamma -> hadrons')
  detail = detail.replace(',', '')
  detail = detail.replace('n N', 'nu nub')
  detail = detail.replace('se--', 'seL-')
  detail = detail.replace('se-+', 'seL+')
  detail = detail.replace(' -> ', '->')
  detail = detail.replace('->', ' -> ')
  detail = detail.replace(' H ->', ', H ->')
  detail = detail.replace(' Z0 ->', ', Z0 ->')
  detail = detail.replace(' W ->', ', W ->')

  return detail

# def getAncestor(lfn):
#  from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
#  fc = FileCatalogClient()
#  res = fc.getFileAncestors([lfn],1)
#  if not res['OK']:
#    return S_ERROR("Failed getting ancestor")
#  for ancestor in res['Value']['Successful'][lfn].keys():
#    if not ancestor.count("stdhep"):
#      res = getAncestor(ancestor)
#      if not res['OK']:
#        return S_ERROR("Failed geting ancestor")
#    else:
#      return S_OK(ancestor)


class _Params(object):
  """CLI Parameters class."""

  def __init__(self):
    """Initialize."""
    self.prod = []
    self.minprod = 0
    self.full_det = False
    self.sampleSize = 100
    self.ptypes = ['MCGeneration', 'MCSimulation', 'MCReconstruction', "MCReconstruction_Overlay"]
    self.statuses = ['Active', 'Stopped', 'Completed', 'Archived']

  def setProdID(self, opt):
    """Set the prodID to use.

    Can be a range, a list, a unique value and a 'greater than' value.
    """
    if opt.count(","):
      parts = opt.split(",")
    else:
      parts = [opt]
    prods = []
    try:
      for part in parts:
        if part.count("gt"):
          self.minprod = int(part.replace("gt", ""))
          continue
        if part.count("-"):
          prods.extend(list(range(int(part.split("-")[0]), int(part.split("-")[1]) + 1)))
        else:
          prods.append(int(part))
    except ValueError:
      return S_ERROR('ProductionID: bad syntax')
    self.prod = prods

    return S_OK()

  def setFullDetail(self, _opt):
    """Get every individual file's properties, makes this very very slow."""
    self.full_det = True
    return S_OK()

  def setSampleSize(self, opt):
    """Set the number of generator files to sample for cross-section and luminosity."""
    try:
      self.sampleSize = int(opt)
    except ValueError:
      return S_ERROR('SampleSize: bad value')
    return S_OK()

  def setProdTypes(self, opt):
    """Set the prod types to consider."""
    self.ptypes = opt.split(",")
    return S_OK()

  def setStatuses(self, opt):
    """Set the prod statuses."""
    self.statuses = opt.split(",")
    return S_OK()

  def registerSwitches(self):
    """Register all CLI switches."""
    Script.registerSwitch(
        "P:",
        "prods=",
        "Productions: greater than with gt1234, range with 32-56, list with 34,56",
        self.setProdID)
    Script.registerSwitch("p", "precise_detail", "Precise detail, slow", self.setFullDetail)
    Script.registerSwitch("N:", "sample_size=", "The number of generator files to sample for cross-section and "
                          "luminosity, default 100", self.setSampleSize)
    Script.registerSwitch("t:", "types=", "Production Types, comma separated, default all", self.setProdTypes)
    Script.registerSwitch("S:", "Statuses=", "Statuses, comma separated, default all", self.setStatuses)
    Script.setUsageMessage('\n'.join([__doc__.split('\n')[1],
                                         '\nUsage:',
                                         '  %s [option|cfgfile] ...\n' % Script.scriptName]))


@Script()
def main():
  clip = _Params()
  clip.registerSwitches()
  Script.parseCommandLine()
  from ILCDIRAC.Core.Utilities.HTML import Table
  from ILCDIRAC.Core.Utilities.ProcessList import ProcessList
  from DIRAC.TransformationSystem.Client.TransformationClient import TransformationClient
  from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
  from DIRAC import gConfig, gLogger
  prod = clip.prod
  full_detail = clip.full_det
  fc = FileCatalogClient()

  processlist = gConfig.getValue('/LocalSite/ProcessListPath', '')
  prl = ProcessList(processlist)
  processesdict = prl.getProcessesDict()

  trc = TransformationClient()
  prodids = []
  if not prod:
    conddict = {}
    conddict['Status'] = clip.statuses
    if clip.ptypes:
      conddict['Type'] = clip.ptypes
    res = trc.getTransformations(conddict)
    if res['OK']:
      for transfs in res['Value']:
        prodids.append(transfs['TransformationID'])
  else:
    prodids.extend(prod)

  metadata = []

  gLogger.info("Will run on prods %s" % str(prodids))

  for prodID in prodids:
    if prodID < clip.minprod:
      continue
    meta = {}
    meta['ProdID'] = prodID
    res = trc.getTransformation(str(prodID))
    if not res['OK']:
      gLogger.error("Error getting transformation %s" % prodID)
      continue
    prodtype = res['Value']['Type']
    proddetail = res['Value']['Description']

    if prodtype in ['Split', 'Merge']:
      gLogger.warn("Invalid query for %s productions" % prodtype)
      continue
    if prodtype not in ['MCReconstruction', 'MCReconstruction_Overlay', 'MCGeneration', 'MCSimulation']:
      gLogger.error("Unknown production type %s" % prodtype)
      continue

    res = fc.getCompatibleMetadata({'ProdID': prodID})
    if not (res['OK'] and res['Value'].get('Datatype')):
      gLogger.error(f"Error getting transformation {prodID}: ", res.get("Message", "No 'Datatype' found for this transformation"))
      continue
    if 'delphes' in res['Value']['Datatype']:
      meta['Datatype'] = 'delphes'
    else:
      meta['Datatype'] = res['Value']['Datatype'][0]

    gLogger.verbose('Looking for files: %s' % meta)
    res = fc.findFilesByMetadata(meta)
    if not res['OK']:
      gLogger.error(res['Message'])
      continue
    lfns = res['Value']
    nb_files = len(lfns)
    if not lfns:
      gLogger.warn("No files found for prod %s" % prodID)
      continue
    path = os.path.dirname(lfns[0])
    gLogger.verbose('Looking for user metadata')
    res = fc.getDirectoryUserMetadata(path)
    if not res['OK']:
      gLogger.warn('No meta data found for %s' % path)
      continue
    dirmeta = {'proddetail': proddetail,
               'prodtype': prodtype,
               'nb_files': nb_files,
               }
    dirmeta.update(res['Value'])
    lumi = 0.
    nbevts = 0
    files = 0
    xsec = 0.0
    if not full_detail:
      info = _getFileInfo(lfns[0], fc)
      lumi = info[0] * len(lfns)
      nbevts = info[1] * len(lfns)
      if info[2]:
        xsec += info[2]
        files += 1
    else:
      for lfn in lfns:
        info = _getFileInfo(lfn, fc)
        lumi += info[0]
        nbevts += info[1]
        if info[2]:
          xsec += info[2]
          files += 1
        gLogger.verbose('Found lumi: %s, xsec: %s' % (lumi, xsec))
        if not lumi:  # we are guessing none of the files have that information at this point
          gLogger.notice('Files do not have xsection info, looking at ancestors now')
          nbevts = info[1] * len(lfns)
          break

    if (not lumi) and (prodtype != 'MCGeneration'):
      xsec = 0
      files = 0
      depthDict = defaultdict(set)
      gLogger.verbose('Looking for Ancestors of %s files' % len(lfns))
      for index, lfnChunk in enumerate(breakListIntoChunks(lfns[:1000], 1000)):
        gLogger.verbose('Looking at chunk %s/%s' % (index, len(lfns) // 1000))
        res = fc.getFileAncestors(lfnChunk, [1, 2, 3, 4])
        if not res['OK']:
          gLogger.error('failed to find ancenstors')
          return res
        for lfn, ancestorsDict in res['Value']['Successful'].items():
          for ancestor, dep in ancestorsDict.items():
            depthDict[dep].add(ancestor)
      gLogger.verbose('Found all the ancestors')
      oldestAncestorID = sorted(depthDict)[-1]
      oldestAncestors = depthDict[oldestAncestorID]
      numberOfAncestors = len(oldestAncestors)
      sampleSize = clip.sampleSize if not full_detail else numberOfAncestors
      gLogger.verbose('Sampling %s from %s' % (sampleSize, numberOfAncestors))
      for index, ancestor in enumerate(random.sample(oldestAncestors, sampleSize)):
        gLogger.verbose('Getting info for ancestor %s / %s' % (index, sampleSize))
        info = _getFileInfo(ancestor, fc)
        # lumi is not used later on
        lumi += info[0] * float(numberOfAncestors) / float(sampleSize)
        if info[2]:
          xsec += info[2]
          files += 1
        gLogger.verbose('Found %s, %s, %s' % (info[0], info[2], files))

    dirmeta['CrossSection'] = xsec / float(files) if xsec and files else 0.0
    dirmeta['NumberOfEvents'] = nbevts if nbevts else 0

    detail = dirmeta['EvtType']
    if dirmeta['EvtType'] in processesdict and 'Detail' in processesdict[dirmeta['EvtType']]:
      detail = processesdict[dirmeta['EvtType']]['Detail']
    dirmeta['detail'] = _translate(detail)

    dirmeta['MomProdID'] = 0
    if prodtype != 'MCGeneration':
      res = trc.getTransformationMetaQuery(str(prodID), 'Input')
      if res['OK']:
        if 'ProdID' in res['Value']:
          dirmeta['MomProdID'] = res['Value']['ProdID']

    metadata.append(dirmeta)

  detectors = {'gen': []}

  for channel in metadata:
    if 'DetectorType' not in channel:
      detectors['gen'].append((channel['detail'],
                               channel['Energy'],
                               channel['ProdID'],
                               channel['nb_files'],
                               channel['NumberOfEvents'] / channel['nb_files'],
                               channel['NumberOfEvents'],
                               channel['CrossSection'], str(channel['proddetail'])))
      gLogger.notice(f'Transformation {channel["ProdID"]} found as generation.')

    else:
      ops = Operations()
      detOptions = ops.getOptions("/Transformations/TablesTitles", listOrdered=False)['Value']
      matchDet = ""
      # Check if the DetectorType of the transformation is a version of a known detector of the Configuration System
      for det in detOptions:
        # Take the longest match in order to not confuse idea and idea lar.
        if channel['DetectorType'].startswith(det) and (len(det) > len(matchDet)):
          matchDet = det
      if matchDet:
        detTitle = ops.getValue(f"/Transformations/TablesTitles/{matchDet}", None)
        if matchDet not in detectors:
          # If the detector is encountered for the first time, we create a new detector in the `detectors` dictionary, using the name found in the Configuration System
          gLogger.notice(f'Detector "{matchDet}", matching transformation DetectorType "{channel["DetectorType"]}", found in Operations, with title "{detTitle}". Adding to known detectors.')
          detectors[matchDet] = _addDetectorOutputs({'title': detTitle})
      else:
        gLogger.error("This is unknown detector", channel['DetectorType'])
        continue
      detectors[matchDet][channel['Datatype']].append((channel['detail'],
                                                      channel['Energy'],
                                                      channel['DetectorType'],
                                                      channel['ProdID'],
                                                      channel['nb_files'],
                                                      channel['NumberOfEvents'] / channel['nb_files'],
                                                      channel['NumberOfEvents'],
                                                      channel['CrossSection'],
                                                      channel['MomProdID'],
                                                      str(channel['proddetail'])))
      gLogger.notice(f'Transformation {channel["ProdID"]} found for detector {matchDet}')

  header_row_tuple_gen = ('Channel', 'Energy', 'ProdID', 'Tasks', 'Average Evts/task', 'Statistics',
                          'Cross Section (fb)', 'Comment')
  header_row_tuple_det = ('Channel', 'Energy', 'Detector', 'ProdID', 'Number of Files', 'Events/File',
                          'Statistics', 'Cross Section (fb)', 'Origin ProdID', 'Comment')

  with open('tables.html', 'w') as of:
    of.write(textwrap.dedent("""
                             <!DOCTYPE html>
                             <html>
                               <head>
                                 <title> Production summary </title>
                               </head>
                               <body>
                             """).strip())
    if detectors['gen']:
      of.write("<h1>gen prods</h1>\n")
      table = Table(header_row=header_row_tuple_gen)
      table.rows.extend(detectors['gen'])
      of.write(str(table))
      gLogger.info("Gen prods")
      gLogger.info(str(table))
    detectors.pop('gen')

    # pylint: disable=no-member, invalid-sequence-index
    for detName, infos in detectors.items():
      if any(infos.get(pt) for pt in _addDetectorOutputs({}).keys()):
        of.write('<h1>%s prods</h1>\n' % infos['title'])
        for ptype in _addDetectorOutputs({}).keys():
          if infos[ptype]:
            of.write('<h2>%s</h2>\n' % ptype)
            table = Table(header_row=header_row_tuple_det)
            table.rows.extend(infos[ptype])
            of.write(str(table))
            gLogger.info('%s prods %s' % (infos['title'], ptype))
            gLogger.info(str(table))
    # pylint: enable=no-member, invalid-sequence-index
    of.write(textwrap.dedent("""
                               </body>
                             </html>"""))
  gLogger.notice("Check ./tables.html in any browser for the results")
  dexit(0)

if __name__ == "__main__":
  main()
