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
"""Print all applications and their versions registered in the configuration service.

Options:

   -S, --software software       show versions for this application only
   -A, --apps                    show only available Applications, not their versions

:since: Dec 17, 2010
:author: sposs
"""
from __future__ import absolute_import
__RCSID__ = "$Id$"

import os

from DIRAC.Core.Base.Script import Script
from DIRAC import S_OK


class _Params(object):
  """Parameter Object."""

  def __init__(self):
    self.software = ''
    self.appsOnly = False

  def setSoftware(self, opt):
    self.software = opt
    return S_OK()

  def setAppsOnly(self, _):
    self.appsOnly = True
    return S_OK()

  def registerSwitches(self):
    Script.registerSwitch("S:", "software=", "show versions for this software", self.setSoftware)
    Script.registerSwitch("A", "apps", "show only available Applications, not their versions", self.setAppsOnly)
    Script.setUsageMessage("""%s """ % ("dirac-ilc-show-software",))


@Script()
def main():
  """Show available software."""
  clip = _Params()
  clip.registerSwitches()
  Script.parseCommandLine()
  from DIRAC import gConfig, gLogger

  base = '/Operations/Defaults/AvailableTarBalls'
  platforms = gConfig.getSections(base)

  for platform in platforms['Value']:
    gLogger.notice("For platform %s, here are the available software" % platform)
    apps = gConfig.getSections(base + "/" + platform)
    for app in apps['Value']:
      if clip.software and app.lower() != clip.software.lower():
        continue
      gLogger.notice("   - %s" % app)
      versions = gConfig.getSections(base + "/" + platform + "/" + app)
      if clip.appsOnly:
        continue
      for vers in versions['Value']:
        gLogger.notice("     * %s" % vers)
        depsb = gConfig.getSections(base + "/" + platform + "/" + app + "/" + vers)
        if 'Dependencies' in depsb['Value']:
          gLogger.notice("       Depends on")
          deps = gConfig.getSections(os.path.join(base, platform, app, vers, "Dependencies"))
          for dep in deps['Value']:
            depversions = gConfig.getOption(base + "/" + platform + "/" + app + "/"
                                            + vers + "/Dependencies/" + dep + "/version")
            gLogger.notice("         %s %s" % (dep, depversions['Value']))

      if not len(versions['Value']):
        gLogger.notice("      No version available")


if __name__ == "__main__":
  main()
