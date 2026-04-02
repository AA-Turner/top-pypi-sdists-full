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
"""Create a production to replicate files from one storage element to another.

Example::

  dirac-ilc-replication-transformation <prodID> <TargetSEs> <SourceSEs> {GEN,SIM,REC,DST} -NExtraName

Options:
   -N, --Extraname string      String to append to transformation name in case one already exists with that name
   -R, --GroupName <value>     TransformationGroup Name, by itself the group of the prodID
   -G, --GroupSize <value>     Number of Files per transformation task
   -x, --Enable                Enable the transformation creation, otherwise dry-run

:since:  May 18, 2015
:author: A. Sailer
"""
from __future__ import absolute_import
from pprint import pformat

from DIRAC.Core.Base.Script import Script
from DIRAC import gLogger, exit as dexit
from DIRAC.TransformationSystem.Utilities.ReplicationTransformation import createDataTransformation

from ILCDIRAC.ILCTransformationSystem.Utilities.DataParameters import Params as _Params, getTransformationGroup

__RCSID__ = "$Id$"

LOG = gLogger.getSubLogger("ReplTrans")


def registerSwitches(script):
  """register additional switches for replication transformation."""
  script.setUsageMessage("""%s <prodID> <TargetSEs> <SourceSEs> {GEN,SIM,REC,DST} -NExtraName""" % script.scriptName)


@Script()
def main():
  """reads command line parameters, makes check and creates replication transformation."""
  clip = _Params()
  clip.groupSize = 10
  clip.registerSwitches(Script)
  registerSwitches(Script)
  Script.parseCommandLine()
  if not clip.checkSettings(Script)['OK']:
    LOG.error("ERROR: Missing settings")
    return 1
  for prodID in clip.metaValues:
    tGroup = getTransformationGroup(prodID, clip.groupName)
    parDict = dict(flavour=clip.flavour,
                   targetSE=clip.targetSE,
                   sourceSE=clip.sourceSE,
                   metaKey=clip.metaKey,
                   metaValue=prodID,
                   extraData={'Datatype': clip.datatype},
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
  dexit(main)
