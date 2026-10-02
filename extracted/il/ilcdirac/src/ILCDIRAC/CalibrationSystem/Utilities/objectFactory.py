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
"""Object factory."""

from __future__ import absolute_import
from DIRAC import gLogger

LOG = gLogger.getSubLogger(__name__)


class ObjectFactory:
  """Standard object factiry."""

  def __init__(self):
    """Initialize."""
    self._builders = {}

  def registerBuilder(self, key, builder):
    """Register builder."""
    self._builders[key] = builder

  def getClass(self, key):
    """Return class (builder) which corresponds to the input key."""
    builder = self._builders.get(key)
    if not builder:
      LOG.error('Unknown key: %s. Available keys are: %s' % (key, list(self._builders.keys())))
      raise ValueError(key)
    return builder
