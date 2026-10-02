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
"""Set of functions used to resolve the applications' dependencies, looking into the CS.

Works recursively

:since: Apr 26, 2010
:author: Stephane Poss
"""

from __future__ import absolute_import
__RCSID__ = "$Id$"

from DIRAC import gLogger
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations


def resolveDeps(sysconfig, appli, appversion):
  """Resolve the dependencies.

  :param str sysconfig: system configuration
  :param str appli: application name
  :param str appversion: application version
  :return: list of dictionaries
  """
  log = gLogger.getSubLogger("resolveDeps")
  ops = Operations()
  deps = ops.getSections('/AvailableTarBalls/%s/%s/%s/Dependencies' % (sysconfig, appli,
                                                                       appversion), '')
  depsarray = []
  if deps['OK']:
    for dep in deps['Value']:
      vers = ops.getValue('/AvailableTarBalls/%s/%s/%s/Dependencies/%s/version' % (sysconfig, appli,
                                                                                   appversion, dep), '')
      depvers = ''
      if vers:
        depvers = vers
      else:
        log.error("Retrieving dependency version for %s failed, skipping to next !" % (dep))
        continue
      log.verbose("Found dependency %s %s" % (dep, depvers))
      depdict = {}
      depdict["app"] = dep
      depdict["version"] = depvers
      depsarray.append(depdict)
      # resolve recursive dependencies
      depsofdeps = resolveDeps(sysconfig, dep, depvers)
      depsarray.extend(depsofdeps)
  else:
    log.verbose("Could not find any dependency for %s %s, ignoring" % (appli, appversion))
  return depsarray
