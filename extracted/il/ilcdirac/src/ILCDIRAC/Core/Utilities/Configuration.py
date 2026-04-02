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
"""helper functions for getting configuration options."""

from __future__ import absolute_import
import os


def getOptionValue(ops, basePath, optionName, defaultValue, levels):
  """get option from any place in the hierarchy starting from basepath, going through each section level.

  :param ops: Operation helper
  :param str basePath: section in Operation to start looking for the option
  :param str optionName: the name of the option to find
  :param defaultValue: the default value to use for this option
  :param list levels: the different [sub-]sub-sections to check for this option
  :returns: value at the deepest level in the configuration
  """

  join = os.path.join
  value = ops.getValue(join(basePath, optionName), defaultValue)

  path = basePath
  for level in levels:
    path = join(path, level)
    value = ops.getValue(join(path, optionName), value)

  return value
