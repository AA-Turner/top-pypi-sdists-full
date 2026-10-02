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
'''
:author: sposs
:since: Nov 7, 2013
'''

from __future__ import absolute_import

from DIRAC import S_OK

from ILCDIRAC.Interfaces.API.NewInterface.Application import Application

__RCSID__ = "$Id$"


class LCUtilityApplication(Application):
  """Utility applications."""

  def __init__(self, paramdict=None):
    super(LCUtilityApplication, self).__init__(paramdict)
    # Number of events to process
    self.numberOfEvents = 0
    # Energy to use (duh! again)
    self.energy = 0
    self._importLocation = "ILCDIRAC.Workflow.Modules"

  def setNumberOfEvents(self, numberOfEvents):
    """Set the number of events to process, alias to :func:`setNbEvts`"""
    return self.setNbEvts(numberOfEvents)

  def setEnergy(self, energy):
    """Set the energy to use.

    :param float energy: Energy used in GeV
    """
    if not isinstance(energy, float):
      energy = float(energy)
    self._checkArgs({'energy': float})
    self.energy = energy
    return S_OK()


#### DEPRECATED ################################################################


  def setNbEvts(self, numberOfEvents):
    """Set the number of events to process.

    .. deprecated:: v23r0p0
       use :func:`setNumberOfEvents`

    :param int numberOfEvents: Number of events to process (or generate)
    """
    self._checkArgs({'numberOfEvents': int})
    self.numberOfEvents = numberOfEvents
    return S_OK()
