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
"""Utilities for Overlay Files."""
from __future__ import absolute_import
import os
from decimal import Decimal
from math import modf

from DIRAC import gLogger

LOG = gLogger.getSubLogger(__name__)
__RCSID__ = "$Id$"


def getOverlayFiles(evttype='gghad'):
  """List the content of the overlay directory given a background type. Called from :func:`~ILCDIRAC.Core.Utilities.PrepareOptionFiles.prepareXMLFile`.

  :param str evttype: type of the background event to find
  :return: list of files contained in the overlay_BKG folder, where BKG can be anything
  """
  localfiles = []
  ovdir = os.path.join(os.getcwd(), "overlayinput_" + evttype)

  if not os.path.exists(ovdir):
    LOG.error('overlay directory does not exists', "overlayinput_" + evttype)
    return localfiles
  listdir = os.listdir(ovdir)
  for item in listdir:
    if item.count('.slcio'):
      localfiles.append(os.path.join(ovdir, item))
  return localfiles


def energyToInt(energy):
  """return energy as integer.

  :param str energy: energy with gev/tev unit
  :return: energy in gev
  :rtype: int
  """
  energy = energy.lower()
  if energy.endswith('tev'):
    return int(float(energy.split('tev')[0]) * 1000)
  if energy.endswith('gev'):
    return int(energy.split('gev')[0])
  raise RuntimeError('Cannot transform %s to energy integer' % energy)


def energyWithUnit(energy):
  """return energy with unit, GeV below 1000, TeV above.

  .. note :: Precision only to the 1 GeV level below 1 TeV, and one digit above 1 TeV

  :param energy: energy
  :type energy: int or float
  :return: energy string with unit
  :rtype: str
  """
  energyString = ''
  if energy < 1000.:
    energyString = "%dGeV" % int(energy)
  elif float(energy / 1000.).is_integer():
    energyString = "%dTeV" % int(energy / 1000.0)
  else:
    energyString = "%1.1fTeV" % float(energy / 1000.0)

  return energyString


def energyWithLowerCaseUnit(energy):
  """return energy with lower case unit, gev below 1000, tev above.

  Same as :func:`energyWithUnit` but lowerCase

  :param energy: energy
  :type energy: int or float
  :return: energy string with unit
  :rtype: str
  """
  return energyWithUnit(energy).lower()


def oldEnergyWithUnit(energy):
  """legacy conversion to energyWithLowerCaseUnit.

  .. deprecated :: v26r0p11
  """
  fracappen = modf(float(energy) / 1000.)
  if fracappen[1] > 0:
    energytouse = "%stev" % (Decimal(str(energy)) / Decimal("1000."))
  else:
    energytouse = "%sgev" % (Decimal(str(energy)))
  if energytouse.count(".0"):
    energytouse = energytouse.replace(".0", "")
  return energytouse
