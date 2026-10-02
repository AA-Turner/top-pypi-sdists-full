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
"""DB for Overlay System."""
from __future__ import absolute_import
__RCSID__ = "$Id$"

from DIRAC import gLogger, S_OK, S_ERROR
from DIRAC.Core.Base.DB import DB
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations


class OverlayDB (DB):
  """DB for OverlaySystem."""

  def __init__(self):
    """"""
    self.ops = Operations()
    self.dbname = 'OverlayDB'
    self.logger = gLogger.getSubLogger('OverlayDB')
    DB.__init__(self, self.dbname, 'Overlay/OverlayDB')
    self._createTables({"OverlayData": {'Fields': {'Site': "VARCHAR(255) UNIQUE NOT NULL",
                                                         'NumberOfJobs': "INTEGER DEFAULT 0"
                                                       },
                                            'PrimaryKey': 'Site',
                                            'Indexes': {'Index': ['Site']}
                                          }
                        }
                      )
    limits = self.ops.getValue("/Overlay/MaxConcurrentRunning", 200)
    self.limits = {}
    self.limits["default"] = limits
    res = self.ops.getSections("/Overlay/Sites/")
    sites = []
    if res['OK']:
      sites = res['Value']
    for tempsite in sites:
      res = self.ops.getValue("/Overlay/Sites/%s/MaxConcurrentRunning" % tempsite, 200)
      self.limits[tempsite] = res
    self.logger.info("Using the following restrictions : %s" % self.limits)

  #####################################################################
  # Private methods

  def __getConnection(self, connection):
    if connection:
      return connection
    res = self._getConnection()
    if res['OK']:
      return res['Value']
    gLogger.warn("Failed to get MySQL connection", res['Message'])
    return connection

  #pylint: disable-msg=too-many-function-args
  def _checkSite(self, site, connection=False):
    """Check the number of jobs running at a given site."""
    connection = self.__getConnection(connection)

    req = "SELECT NumberOfJobs FROM OverlayData WHERE Site='%s';" % (site)
    res = self._query(req, conn=connection)
    if not res['OK']:
      return S_ERROR("Could not get site")
    if len(res['Value']):
      return res
    else:
      return S_ERROR("Could not find any site %s" % (site))
  #pylint: enable-msg=too-many-function-args

  #pylint: disable-msg=too-many-function-args
  def _addSite(self, site, connection=False):
    """Add a new site to the DB."""
    connection = self.__getConnection(connection)
    req = "INSERT INTO OverlayData (Site,NumberOfJobs) VALUES ('%s',1);" % site
    res = self._update(req, conn=connection)
    if not res['OK']:
      return res
    return res
  #pylint: enable-msg=too-many-function-args

  def _limitForSite(self, site):
    """Get the current limit of jobs for a given site."""
    if site in self.limits:
      return self.limits[site]
    return self.limits['default']

  #pylint: disable-msg=too-many-function-args
  def _addNewJob(self, site, nbjobs, connection=False):
    """Add a new running job in the DB."""
    connection = self.__getConnection(connection)
    nbjobs += 1
    req = "UPDATE OverlayData SET NumberOfJobs=%s WHERE Site='%s';" % (nbjobs, site)
    self._update(req, conn=connection)
    return S_OK()
  #pylint: enable-msg=too-many-function-args

# Methods to fix the site
  #pylint: disable-msg=too-many-function-args
  def getSites(self, connection=False):
    """Return the list of sites known to the service."""
    connection = self.__getConnection(connection)
    req = 'SELECT Site From OverlayData;'
    res = self._query(req, conn=connection)
    if not res['OK']:
      return S_ERROR("Could not get sites")
    sites = []
    for row in res['Value']:
      sites.append(row[0])
    return S_OK(sites)
  #pylint: enable-msg=too-many-function-args

  #pylint: disable-msg=too-many-function-args
  def setJobsAtSites(self, sitedict, connection=False):
    """As name suggests: set the number of jobs running at the site."""
    connection = self.__getConnection(connection)
    for site, nbjobs in sitedict.items():
      req = "UPDATE OverlayData SET NumberOfJobs=%i WHERE Site='%s';" % (int(nbjobs), site)
      res = self._update(req, conn=connection)
      if not res['OK']:
        return S_ERROR("Could not set number of jobs at site %s" % site)

    return S_OK()
  #pylint: enable-msg=too-many-function-args

# Useful methods for the users

  def getJobsAtSite(self, site, connection=False):
    """Get the number of jobs currently run."""
    connection = self.__getConnection(connection)
    nbjobs = 0
    res = self._checkSite(site, connection)
    if not res['OK']:
      return S_OK(nbjobs)
    nbjobs = res['Value'][0][0]
    return S_OK(nbjobs)

# Important methods

  def canRun(self, site, connection=False):
    """Can the job run at that site?"""
    connection = self.__getConnection(connection)
    res = self._checkSite(site, connection)
    nbjobs = 0
    if not res['OK']:
      self._addSite(site, connection)
      nbjobs = 1
    else:
      nbjobs = res['Value'][0][0]
    if nbjobs < self._limitForSite(site):
      res = self._addNewJob(site, nbjobs, connection)
      if not res['OK']:
        return res
      return S_OK(True)
    else:
      return S_OK(False)

  #pylint: disable-msg=too-many-function-args
  def jobDone(self, site, connection=False):
    """Remove a job from the DB, should not remove a job from the DB if the Site does not exist, but this should never happen."""
    connection = self.__getConnection(connection)
    res = self._checkSite(site, connection)
    if not res['OK']:
      return res
    nbjobs = res['Value'][0][0]
    if nbjobs == 1:
      return S_OK()
    nbjobs -= 1
    req = "UPDATE OverlayData SET NumberOfJobs=%s WHERE Site='%s';" % (nbjobs, site)
    res = self._update(req, conn=connection)
    if not res['OK']:
      return res
    return S_OK()
  #pylint: enable-msg=too-many-function-args
