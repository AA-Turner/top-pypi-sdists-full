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
"""This class is needed to get the Limited plugin support."""

from __future__ import absolute_import
__RCSID__ = "$Id$"
from DIRAC.TransformationSystem.Client.Transformation import Transformation as DT


class Transformation(DT):
  """ILCDirac version of Transformation."""

  def __init__(self, transID=0, transClient=None):
    super(Transformation, self).__init__(transID=0, transClient=None)
    self.supportedPlugins += ['Limited', 'Sliced', 'SlicedLimited']

  def _checkLimitedPlugin(self):
    """checks the Limitited Plugin, just passes the checkStandardPluging."""
    return self._checkStandardPlugin()

  def _checkSlicedPlugin(self):
    """checks the Sliced Plugin, just passes the checkStandardPluging."""
    return self._checkStandardPlugin()

  def _checkSlicedLimitedPlugin(self):
    """checks the SlicedLimited Plugin, just passes the checkStandardPluging."""
    return self._checkStandardPlugin()
