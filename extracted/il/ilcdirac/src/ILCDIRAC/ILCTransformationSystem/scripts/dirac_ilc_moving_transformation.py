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
"""Create a transformation to move files from one storage element to another.

Example::

  dirac-ilc-moving-transformation <prodID> <TargetSEs> <SourceSEs> {GEN,SIM,REC,DST} -NExtraName
  dirac-ilc-moving-transformation --AllFor="<prodID1>, <prodID2>, ..." <TargetSEs> <SourceSEs> -NExtraName [-F]

Options:
   -A, --AllFor    list        Comma separated list of production IDs. For each prodID three moving productions are
                               created: ProdID/Gen, ProdID+1/SIM, ProdID+2/REC
   -F, --Forcemoving           Move GEN or SIM files even if they do not have descendents
   -N, --Extraname string      String to append to transformation name in case one already exists with that name
   -R, --GroupName <value>     TransformationGroup Name, by itself the group of the prodID
   -G, --GroupSize <value>     Number of Files per transformation task
   -x, --Enable                Enable the transformation creation, otherwise dry-run

:since:  Dec 4, 2015
:author: A. Sailer
"""
from __future__ import absolute_import
from pprint import pformat

from DIRAC.Core.Base.Script import Script
from DIRAC import gLogger as LOG, exit as dexit
from DIRAC.TransformationSystem.Utilities.ReplicationTransformation import createDataTransformation

from ILCDIRAC.ILCTransformationSystem.Utilities.DataParameters import Params as _Params, checkDatatype, \
    getTransformationGroup

__RCSID__ = "$Id$"


def registerSwitches(clip, script):
  """register additional switches for moving transformations."""
  script.registerSwitch("A:", "AllFor=", "Create usual set of moving transformations for prodID/GEN, prodID+1/SIM"
                        " prodID+2/REC", clip.setAllFor)
  script.registerSwitch("F", "Forcemoving", "Move GEN or SIM files even if they do not have descendents",
                        clip.setForcemoving)


@Script()
def main():
  """reads command line parameters, makes check and creates replication transformation."""
  clip = _Params()
  clip.flavour = 'Moving'
  clip.plugin = 'BroadcastProcessed'
  clip.groupSize = 10
  clip.registerSwitches(Script)
  registerSwitches(clip, Script)
  Script.parseCommandLine()
  if not clip.checkSettings(Script)['OK']:
    LOG.error("ERROR: Missing settings")
    return 1
  for index, prodID in enumerate(clip.metaValues):
    datatype = clip.datatype if clip.datatype else ['GEN', 'SIM', 'REC'][index % 3]
    if clip.forcemoving:
      LOG.notice('Forced moving: setting plugin to "Broadcast"')
      clip.plugin = 'Broadcast'
    if datatype == 'REC':
      LOG.notice('Moving REC files: setting plugin to "Broadcast"')
      clip.plugin = 'Broadcast'
    retData = checkDatatype(prodID, datatype)
    if not retData['OK']:
      LOG.error("ERROR: %s" % retData['Message'])
      return 1
    tGroup = getTransformationGroup(prodID, clip.groupName)
    parDict = dict(flavour=clip.flavour,
                   targetSE=clip.targetSE,
                   sourceSE=clip.sourceSE,
                   metaKey=clip.metaKey,
                   metaValue=prodID,
                   extraData={'Datatype': datatype},
                   extraname=clip.extraname,
                   plugin=clip.plugin,
                   groupSize=clip.groupSize,
                   tGroup=tGroup,
                   enable=clip.enable,
                   )
    LOG.notice('Parameters: %s' % pformat(parDict))
    resCreate = createDataTransformation(**parDict)
    if not resCreate['OK']:
      LOG.error('Failed to create the transformation', resCreate['Message'])
      return 1

  return 0


if __name__ == '__main__':
  dexit(main())
