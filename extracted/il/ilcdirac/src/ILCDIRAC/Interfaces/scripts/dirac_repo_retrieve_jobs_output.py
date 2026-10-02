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
"""Retrieve the output sandboxes of jobs created using the API, stored in the repository file.

The repository file is defined when creating the :class:`~ILCDIRAC.Interfaces.API.DiracILC.DiracILC` instance.

Options:
  -r repoLocation             Path to repository file
  -O, --Outputdata            retrieve also the outputdata

:since: Mar 24, 2010
:author: sposs
"""
from __future__ import absolute_import
__RCSID__ = "$Id$"

from DIRAC.Core.Base.Script import Script
from DIRAC import S_OK, exit as dexit
from DIRAC import gLogger

LOG = gLogger.getSubLogger(__name__)


class _Params(object):
  def __init__(self):
    self.outputdata = False
    self.repo = ''

  def setOuputData(self, dummy_opt):
    self.outputdata = True
    return S_OK()

  def setRepo(self, opt):
    self.repo = opt
    return S_OK()

  def registerSwitches(self):
    Script.registerSwitch('O', 'Outputdata', 'retrieve also the outputdata', self.setOuputData)
    Script.registerSwitch('r:', 'Repository=', 'repository file to use', self.setRepo)
    Script.setUsageMessage('\n'.join([__doc__.split('\n')[1],
                                        '\nUsage:',
                                        '  %s [option|cfgfile] ...\n' % Script.scriptName]))


@Script()
def main():
  repoLocation = ''
  clip = _Params()
  clip.registerSwitches()
  Script.parseCommandLine(ignoreErrors=False)
  repoLocation = clip.repo
  if not repoLocation:
    Script.showHelp()
    dexit(1)
  from DIRAC.Interfaces.API.Dirac import Dirac

  dirac = Dirac(True, repoLocation)

  exitCode = 0
  res = dirac.monitorRepository(False)
  if not res['OK']:
    LOG.error("Failed because %s" % res['Message'])
    dexit(1)

  res = dirac.retrieveRepositorySandboxes()
  if not res['OK']:
    LOG.error("Failed because %s" % res['Message'])
    dexit(1)
  if clip.outputdata:
    res = dirac.retrieveRepositoryData()
    if not res['OK']:
      LOG.error("Failed because %s" % res['Message'])
      exit(1)
  dexit(exitCode)


if __name__ == "__main__":
  main()
