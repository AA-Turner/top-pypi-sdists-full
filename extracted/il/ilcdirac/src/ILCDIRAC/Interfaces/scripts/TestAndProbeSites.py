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
"""submit jobs to all sites and checks the worker nodes for functionality."""
from __future__ import absolute_import
__RCSID__ = "$Id$"
from DIRAC.Core.Base.Script import Script
from DIRAC import S_OK

from DIRAC import gLogger

LOG = gLogger.getSubLogger(__name__)


class _Params(object):
  def __init__(self):
    self.site = None
    self.ce = None

  def setSite(self, opt):
    self.site = opt
    return S_OK()

  def setCE(self, opt):
    self.ce = opt
    return S_OK()

  def registerSwitches(self):
    Script.registerSwitch("S:", "Site=", "Site to probe", self.setSite)
    Script.registerSwitch("C:", "CE=", "Computing Element to probe", self.setCE)
    Script.setUsageMessage("%s --Site LCG.CERN.ch" % Script.scriptName)


def testAndProbeSites():
  """submits jobs to test sites."""
  clip = _Params()
  clip.registerSwitches()
  Script.parseCommandLine()

  from DIRAC import exit as dexit

  from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob
  from ILCDIRAC.Interfaces.API.NewInterface.Applications import CheckWNs
  from ILCDIRAC.Interfaces.API.DiracILC import DiracILC

  from DIRAC.ConfigurationSystem.Client.Helpers.Resources import getQueues

  res = getQueues(siteList=clip.site, ceList=clip.ce)
  if not res['OK']:
    LOG.error("Failed getting the queues", res['Message'])
    dexit(1)

  sitedict = res['Value']
  CEs = []

  for ces in sitedict.values():
    CEs.extend(list(ces.keys()))

  LOG.notice("Found %s CEs to look at." % len(CEs))

  d = DiracILC(True, "SiteProbe.rep")

  for CE in CEs:
    j = UserJob()
    j.setDestinationCE(CE)
    c = CheckWNs()
    res = j.append(c)
    if not res['OK']:
      LOG.error(res['Message'])
      continue
    j.setOutputSandbox("*.log")
    j.setCPUTime(30000)
    j.dontPromptMe()
    res = j.submit(d)
    if not res['OK']:
      LOG.error("Failed to submit job, aborting")
      dexit(1)

  dexit(0)


if __name__ == "__main__":
  testAndProbeSites()
