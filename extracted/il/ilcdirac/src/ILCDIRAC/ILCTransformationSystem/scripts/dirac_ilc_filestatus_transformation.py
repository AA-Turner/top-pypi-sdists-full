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
"""Execute the FileStatusTransformationAgent checks on a given Transformation ID.

Check for consistency in the status of replication of moving transformation.

Example::

  dirac-ilc-filestatus-transformation <transformationID> -x

Options:
   -x, --enable         Perform actions on tasks, requests and files
"""

from __future__ import print_function
from __future__ import absolute_import
__RCSID__ = "$Id$"

from DIRAC.Core.Base.Script import Script
from DIRAC import gLogger, S_OK, S_ERROR
from DIRAC import exit as dexit


class _Params(object):
  """parameters object."""

  def __init__(self):
    self.transID = None
    self.enabled = False

  def setTransID(self, transID):
    self.transID = transID

  def setEnabled(self, opt):
    self.enabled = True
    return S_OK()

  def registerSwitches(self):
    Script.registerSwitch("x", "enable", "perform delete operations on file catalog", self.setEnabled)
    Script.setUsageMessage("""%s <transformationID> -x""" % Script.scriptName)

  def checkSettings(self):
    """parse arguments."""

    args = Script.getPositionalArgs()
    if len(args) < 1:
      return S_ERROR()

    self.setTransID(args[0])

    return S_OK()


@Script()
def main():
  """read commands line params and run FST agent for a given transformation ID."""
  params = _Params()
  params.registerSwitches()
  Script.parseCommandLine()
  if not params.checkSettings()['OK']:
    Script.showHelp()
    dexit(1)

  from ILCDIRAC.ILCTransformationSystem.Agent.FileStatusTransformationAgent import FileStatusTransformationAgent
  fstAgent = FileStatusTransformationAgent('ILCTransformation/FileStatusTransformationAgent',
                                           'ILCTransformation/FileStatusTransformationAgent',
                                           'dirac-ilc-filestatus-transformation')
  fstAgent.log = gLogger
  fstAgent.enabled = params.enabled

  res = fstAgent.getTransformations(transID=params.transID)
  if not res['OK']:
    dexit(1)

  if not res['Value']:
    print("Transformation Not Found")
    dexit(1)

  trans = res['Value'][0]

  res = fstAgent.processTransformation(
      int(params.transID), trans['SourceSE'], trans['TargetSE'], trans['DataTransType'])
  if not res["OK"]:
    dexit(1)

  dexit(0)


if __name__ == "__main__":
  main()
