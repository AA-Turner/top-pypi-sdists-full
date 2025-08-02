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
"""Services for Overlay System."""

from __future__ import absolute_import

from DIRAC import S_OK
from DIRAC.Core.DISET.RequestHandler import RequestHandler

from ILCDIRAC.OverlaySystem.DB.OverlayDB import OverlayDB

__RCSID__ = "$Id$"

# pylint: disable=unused-argument,no-self-use, global-statement

# This is a global instance of the OverlayDB class
OVERLAY_DB = False


def initializeOverlayHandler(serviceInfo):
  """Global initialize for the Overlay service handler."""
  global OVERLAY_DB
  OVERLAY_DB = OverlayDB()
  return S_OK()


class OverlayHandler(RequestHandler):
  """Service for Overlay."""
  types_canRun = [(str,)]

  def export_canRun(self, site):
    """Check if current job can access the data."""
    return OVERLAY_DB.canRun(site)

  types_jobDone = [(str,)]

  def export_jobDone(self, site):
    """report that a given job is done downloading the files at a given site."""
    return OVERLAY_DB.jobDone(site)

  types_getJobsAtSite = [(str,)]

  def export_getJobsAtSite(self, site):
    """Get the jobs running at a given site."""
    return OVERLAY_DB.getJobsAtSite(site)

  types_getSites = []

  def export_getSites(self):
    """Get all sites registered."""
    return OVERLAY_DB.getSites()

  types_setJobsAtSites = [dict]

  def export_setJobsAtSites(self, sitedict):
    """Set the number of jobs running at each site:

    called from the ResetCounter agent
    """
    return OVERLAY_DB.setJobsAtSites(sitedict)
