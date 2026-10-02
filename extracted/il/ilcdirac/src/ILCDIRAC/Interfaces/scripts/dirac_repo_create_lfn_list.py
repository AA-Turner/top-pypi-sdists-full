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
"""Create a list of LFNs form a repository file created during job submission.

The repository file is defined when creating the :class:`~ILCDIRAC.Interfaces.API.DiracILC.DiracILC` instance.

Options:

  -r repoLocation       Path to repository file


:since: Apr 22, 2010
:author: Stephane Poss
"""
from __future__ import absolute_import
__RCSID__ = "$Id$"

from DIRAC.Core.Base.Script import Script
from DIRAC import exit as dexit
from DIRAC import S_OK, gLogger
LOG = gLogger.getSubLogger(__name__)


class _Params(object):
  """dummy."""

  def __init__(self):
    self.repo = ''

  def setRepo(self, optionVal):
    self.repo = optionVal
    return S_OK()

  def registerSwitches(self):
    Script.registerSwitch('r:', 'repository=', 'Path to repository file', self.setRepo)
    Script.setUsageMessage('\n'.join([__doc__.split('\n')[1],
                                        '\nUsage:',
                                        '  %s [option|cfgfile] ...\n' % Script.scriptName]))


@Script()
def main():
  """create the LFnList."""
  cliparams = _Params()
  cliparams.registerSwitches()
  Script.parseCommandLine(ignoreErrors=False)

  repoLocation = cliparams.repo
  if not repoLocation:
    Script.showHelp()
    dexit(2)
  from ILCDIRAC.Interfaces.API.DiracILC import DiracILC
  dirac = DiracILC(True, repoLocation)

  dirac.monitorRepository(False)
  lfns = []
  lfns = dirac.retrieveRepositoryOutputDataLFNs()
  LOG.notice("lfnlist=[")
  for lfn in lfns:
    LOG.notice('"LFN:%s",' % lfn)
  LOG.notice("]")
  dexit(0)


if __name__ == "__main__":
  main()
