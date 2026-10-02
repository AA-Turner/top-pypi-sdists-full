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
"""List the VO members.

Accesses the VOMS server to print members of given VO

Options:
  -u, --UserName <value>      Family name of the user
  -v, --VO <value>            VO to print or search: [ilc|calice]
  -A, --addUser               print output as input for dirac-ilc-add-user
"""

from __future__ import print_function
from __future__ import absolute_import
__RCSID__ = "$Id$"

from DIRAC import S_OK, S_ERROR, gLogger, exit as dexit
from DIRAC.Core.Base.Script import Script

LOG = gLogger.getSubLogger(__name__)

import suds


class _Params(object):
  """Parameter Object."""

  def __init__(self):
    self.username = ''
    self.voName = 'ilc'
    self.adminUrl = "https://grid-voms.desy.de:8443/voms/%s/services/VOMSAdmin"
    self.attributeUrl = "https://grid-voms.desy.de:8443/voms/%s/services/VOMSAttributes"
    self.addPrint = False

  def registerSwitches(self):
    Script.registerSwitch("u:", "UserName=", "Family name of the user", self.setUser)
    Script.registerSwitch("v:", "VO=", "VO to print or search: [ilc|calice]", self.setVO)
    Script.registerSwitch("A", "addUser:", "print output as input for dirac-ilc-add-user", self.setAddPrint)
    Script.setUsageMessage("""%s -U <username> [-v ilc|calice] [-A]""" % Script.scriptName)

  def setUser(self, opt):
    self.username = opt
    return S_OK()

  def setVO(self, opt):
    if opt not in ['ilc', 'calice']:
      return S_ERROR("Unknown VO %s: ilc or calice only" % opt)
    self.voName = opt
    return S_OK()

  def setAddPrint(self, dummy=False):
    """Set the flag to print user strings as input for dirac-ilc-add-user."""
    self.addPrint = True
    return S_OK()

  def setURLs(self):
    """Set the proper urls based on the vo."""
    self.adminUrl = self.adminUrl % self.voName
    self.attributeUrl = self.attributeUrl % self.voName


def printUser(user, addPrint):
  """print user information."""
  if addPrint:
    gLogger.notice("-D\"%s\" -C\"%s\" -E\"%s\"" % (user['DN'], user['CA'], user['mail']))
  else:
    gLogger.notice("%s, %s, %s" % (user['DN'], user['CA'], user['mail']))


@Script()
def main():
  """Print the list of users in the VO."""
  clip = _Params()
  clip.registerSwitches()
  Script.parseCommandLine()
  clip.setURLs()

  from DIRAC.Core.Security.VOMSService import VOMSService
  voms = VOMSService(vo=clip.voName)
  res = voms.getUsers()
  if not res['OK']:
    gLogger.error(res['Message'])
    dexit(1)
  users = res['Value']
  for userDN, userInfo in users.items():
    userInfo['DN'] = userDN
    if not clip.username:
      printUser(userInfo, clip.addPrint)
    else:
      if userDN.lower().count(clip.username.lower()):
        printUser(userInfo, clip.addPrint)


if __name__ == "__main__":
  main()
