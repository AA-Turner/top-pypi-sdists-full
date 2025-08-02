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
"""Created on Jul 25, 2011.

:author: Stephane Poss
"""

from __future__ import absolute_import
__RCSID__ = "$Id$"

from DIRAC.Core.Base.AgentModule import AgentModule
from DIRAC import S_OK, gLogger
from DIRAC.WorkloadManagementSystem.Client.JobMonitoringClient import JobMonitoringClient

from ILCDIRAC.OverlaySystem.Client.OverlaySystemClient import OverlaySystemClient

AGENT_NAME = 'Overlay/ResetCounters'


class ResetCounters (AgentModule):
  """Reset the number of jobs at all sites: some sites are not updated properly, so once in a while it's needed to restore the correct number of jobs.

  It does not need to be exact, but enough to clear some of the jobs.
  """

  def initialize(self):
    """Initialize the agent."""
    self.am_setOption("PollingTime", 60)
    self.ovc = OverlaySystemClient()
    self.jobmon = JobMonitoringClient()
    return S_OK()

  def execute(self):
    """This is called by the Agent Reactor."""
    res = self.ovc.getSites()
    if not res['OK']:
      return res
    sitedict = {}
    sites = res['Value']
    gLogger.info("Will update info for sites %s" % sites)
    for site in sites:
      attribdict = {"Site": site, "ApplicationStatus": 'Getting overlay files'}
      res = self.jobmon.getCounters(['Status'], attribdict)
      if not res['OK']:
        continue
      sitedict[site] = res['Value'].get('Running', 0)
    gLogger.info("Setting new values %s" % sitedict)
    res = self.ovc.setJobsAtSites(sitedict)
    if not res['OK']:
      gLogger.error(res['Message'])
      return res

    return S_OK()
