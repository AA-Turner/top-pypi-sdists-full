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
"""Executor to check which Sites have the proper software installed for any given job.

Based on some part of the SoftwarePackage name we ban a lists of sites.

Arbitrary number of BanLists can be created. In the CS: BanLists is a list of strings, for each string create two more
options.

* <string>Reason
* <string>Sites

Where Reason is the substring of the softwarePackage that is looked for and Sites is a lists of sites to be banned if
the software package includes the substring

Example:

+----------------------------+--------------------------------------------+---------------------------------------+
|  **Option**                |    **Description**                         |  **Example**                          |
+----------------------------+--------------------------------------------+---------------------------------------+
| BanLists                   | List of Reason/Sites combinations          | BanLists=CVMFS                        |
|                            |                                            |                                       |
+----------------------------+--------------------------------------------+---------------------------------------+
| CVMFSReason                | String matched in software version names   | CVMFSReason=ILCSoft                   |
+----------------------------+--------------------------------------------+---------------------------------------+
| CVMFSSites                 | Sites added to the ban lists of the        | CVMFSSites=LCG.SomeSite.cern          |
|                            | software version matches                   |                                       |
+----------------------------+--------------------------------------------+---------------------------------------+
"""

from __future__ import absolute_import
import six
__RCSID__ = '$Id$'

import time
from pprint import pformat

from DIRAC import S_OK
from DIRAC.WorkloadManagementSystem.Executor.Base.OptimizerExecutor import OptimizerExecutor


class SoftwareVersions(OptimizerExecutor):
  """Executor Class for Auto Banning based on software use."""

  @classmethod
  def initializeOptimizer(cls):
    """Initialize specific parameters for SoftwareVersions."""
    cls.__softToBanned = {}
    cls.__lastCacheUpdate = 0
    cls.__cacheLifeTime = 600
    return S_OK()

  def _updateBanLists(self):
    """Update the list of banned sites and reasons."""
    banLists = self.ex_getOption('BanLists', [])
    self.log.notice(pformat(banLists))

    for banList in banLists:
      resReason = self.ex_getOption(banList + 'Reason', '')
      resSites = self.ex_getOption(banList + 'Sites', [])
      self.__softToBanned[resReason] = resSites

    self.log.notice('BanLists:', pformat(self.__softToBanned))

    return S_OK()

  def optimizeJob(self, jid, jobState):
    """Update the banlists if pattern matched."""
    now = time.time()
    if (now - self.__lastCacheUpdate) > self.__cacheLifeTime:
      self.__lastCacheUpdate = now
      self._updateBanLists()

    result = jobState.getManifest()
    if not result['OK']:
      return result
    manifest = result['Value']

    software = manifest.getOption('SoftwarePackages')
    self.log.verbose('SoftwarePackages: %s ' % software)
    if isinstance(software, six.string_types):
      software = [software]

    if software:
      self.checkSoftware(manifest, software)

    result = jobState.setStatus('SoftwareCheck',
                                'Done',
                                appStatus='',
                                source=self.ex_optimizerName())
    if not result['OK']:
      return result

    self.log.verbose('Done SoftwareVersioning')

    return self.setNextOptimizer(jobState)

  def checkSoftware(self, manifest, software):
    """Check Manifest and update BannedSites.

    Check if there are softwarepackages needed for the job and ban all sites if there is some prohibitions for that
    package.
    """
    bannedSites = manifest.getOption('BannedSites', [])
    if not bannedSites:
      bannedSites = manifest.getOption('BannedSite', [])

    self.log.verbose('Original BannedSites:', bannedSites)

    softBanned = set()
    for reason, sites in self.__softToBanned.items():
      for package in software:
        self.log.verbose('Checking %s against %s ' % (reason, package))
        if reason in package:
          softBanned.update(sites)

    newBannedSites = sorted(set(bannedSites).union(softBanned))
    newBannedSites = ', '.join(newBannedSites)
    manifest.setOption('BannedSites', newBannedSites)

    self.log.notice('Updated BannedSites', newBannedSites)
    return
