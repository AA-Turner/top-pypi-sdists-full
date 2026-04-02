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
"""For any input file, try to determine from the FC the number of events / luminosity / event type.

:author: S. Poss
:since: Nov 2, 2010
"""

from __future__ import absolute_import
__RCSID__ = "$Id$"

from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
import os

from DIRAC import gLogger, S_OK, S_ERROR

LOG = gLogger.getSubLogger(__name__)


def getNumberOfEvents(inputfile):
  """Find from the FileCatalog the number of events in a file.

  :param list inputfile: list of file LFNs
  :returns: S_OK() with dictionary containing information on the number of events with the keys:

     * nbevts
     * lumi
     * EvtType
  """

  files = inputfile
  flist = {}
  for myfile in files:
    if not myfile:
      continue
    bpath = os.path.dirname(myfile)
    if bpath not in flist:
      flist[bpath] = [myfile]
    else:
      flist[bpath].append(myfile)

  fc = FileCatalogClient()
  nbevts = {}
  luminosity = 0
  numberofevents = 0
  evttype = ''
  others = {}
  completeFailure = True

  for path, files in flist.items():
    found_nbevts = False
    found_lumi = False

    if len(files) == 1:
      res = fc.getFileUserMetadata(files[0])
      if not res['OK']:
        LOG.warn("Failed to get Metadata from file: %s, because: %s" % (files[0], res['Message']))
      else:
        tags = res['Value']
        if "NumberOfEvents" in tags and not found_nbevts:
          numberofevents += int(tags["NumberOfEvents"])
          found_nbevts = True
          completeFailure = False
        if "Luminosity" in tags and not found_lumi:
          luminosity += float(tags["Luminosity"])
          found_lumi = True
        others.update(tags)
        if found_nbevts:
          continue

    res = fc.getDirectoryUserMetadata(path)
    if res['OK']:
      tags = res['Value']
      if "NumberOfEvents" in tags and not found_nbevts:
        numberofevents += len(files) * int(tags["NumberOfEvents"])
        found_nbevts = True
        completeFailure = False
      if "Luminosity" in tags and not found_lumi:
        luminosity += len(files) * float(tags["Luminosity"])
        found_lumi = True

      evttype = tags.get("EvtType", evttype)
      others.update(tags)
      if found_nbevts:
        continue
    else:
      LOG.warn("Failed to get Metadata from path: %s, because: %s" % (path, res['Message']))

    for myfile in files:
      res = fc.getFileUserMetadata(myfile)
      if not res['OK']:
        LOG.warn("Failed to get Metadata from file: %s, because: %s" % (myfile, res['Message']))
        continue
      tags = res['Value']
      if "NumberOfEvents" in tags:
        numberofevents += int(tags["NumberOfEvents"])
        completeFailure = False
      if "Luminosity" in tags and not found_lumi:
        luminosity += float(tags["Luminosity"])
      others.update(tags)

  nbevts['nbevts'] = numberofevents
  nbevts['lumi'] = luminosity
  nbevts['EvtType'] = evttype
  if 'NumberOfEvents' in others:
    del others['NumberOfEvents']
  if 'Luminosity' in others:
    del others['Luminosity']
  nbevts['AdditionalMeta'] = others

  if completeFailure:
    LOG.warn("Did not obtain NumberOfEvents from FileCatalog")
    return S_ERROR("Failed to get Number of Events")

  return S_OK(nbevts)
