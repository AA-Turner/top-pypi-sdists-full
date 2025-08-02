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
"""Download the output data for the jobs in the repository file created during job submission.

The repository file is defined when creating the :class:`~ILCDIRAC.Interfaces.API.DiracILC.DiracILC` instance.

Options:

  -r repoLocation       Path to repository file

:since: Mar 24, 2010
:author: sposs
"""
from __future__ import absolute_import
from DIRAC.Core.Base.Script import Script
from DIRAC import S_OK, exit as dexit

__RCSID__ = "$Id$"


class _Params(object):
  """CLI params class."""

  def __init__(self):
    self.repo = ''

  def setRepo(self, val):
    self.repo = val
    return S_OK()

  def registerSwitches(self):
    Script.registerSwitch("r:", "repo=", "repo file", self.setRepo)
    # Define a help message
    Script.setUsageMessage('\n'.join([__doc__,
                                         'Usage:',
                                         '  %s [option|cfgfile] ' % Script.scriptName]))


@Script()
def main():
  cliParams = _Params()
  cliParams.registerSwitches()
  Script.parseCommandLine(ignoreErrors=False)
  if not cliParams.repo:
    Script.showHelp()
    dexit(2)
  from DIRAC.Interfaces.API.Dirac import Dirac

  dirac = Dirac(True, cliParams.repo)

  exitCode = 0
  dirac.monitorRepository(False)
  dirac.retrieveRepositoryData()

  dexit(exitCode)


if __name__ == "__main__":
  main()
