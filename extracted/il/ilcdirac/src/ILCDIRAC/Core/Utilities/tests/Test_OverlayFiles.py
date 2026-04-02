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
"""tests for OverlayFiles module."""

from __future__ import absolute_import
import unittest


from ILCDIRAC.Core.Utilities import OverlayFiles as module


class TestHelper(unittest.TestCase):
  """Test helper functions in the script."""

  def setUp(self):
    pass

  def test_energyWithUnit(self):
    self.assertEqual(module.energyWithUnit(300.0), '300GeV')
    self.assertEqual(module.energyWithUnit(380.0), '380GeV')
    self.assertEqual(module.energyWithUnit(3000.0), '3TeV')
    self.assertEqual(module.energyWithUnit(1000.0), '1TeV')
    self.assertEqual(module.energyWithUnit(1400.0), '1.4TeV')
    self.assertEqual(module.energyWithUnit(2500.0), '2.5TeV')

  def test_backwardcompatibility(self):
    self.assertEqual(module.energyWithLowerCaseUnit(300.0), module.oldEnergyWithUnit(300.0))
    self.assertEqual(module.energyWithLowerCaseUnit(380.0), module.oldEnergyWithUnit(380.0))
    self.assertEqual(module.energyWithLowerCaseUnit(3000.0), module.oldEnergyWithUnit(3000.0))
    self.assertEqual(module.energyWithLowerCaseUnit(1000.0), module.oldEnergyWithUnit(1000.0))
    self.assertEqual(module.energyWithLowerCaseUnit(1400.0), module.oldEnergyWithUnit(1400.0))
    self.assertEqual(module.energyWithLowerCaseUnit(2500.0), module.oldEnergyWithUnit(2500.0))

  def test_energyToInt(self):
    self.assertEqual(module.energyToInt('300GeV'), 300)
    self.assertEqual(module.energyToInt('380GeV'), 380)
    self.assertEqual(module.energyToInt('3TeV'), 3000)
    self.assertEqual(module.energyToInt('1TeV'), 1000)
    self.assertEqual(module.energyToInt('1.4TeV'), 1400)
    self.assertEqual(module.energyToInt('2.5TeV'), 2500)
