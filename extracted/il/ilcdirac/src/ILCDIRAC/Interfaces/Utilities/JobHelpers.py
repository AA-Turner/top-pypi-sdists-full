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
"""Helper Functions for Job Interfaces."""


def getValue(value, conversion=None, typeToCheck=None):
  """returns the first entry, if it is a list, or the value otherwise.

  :param value: value to check
  :param conversion: type to convert the value to, callable
  :type conversion: ``callable``
  :param typeToCheck: class the parameter should be an instance of
  :param typeToCheck: ``class``
  """
  newValue = None
  if isinstance(value, list):
    newValue = value[0]
  elif typeToCheck is None or isinstance(value, typeToCheck):
    newValue = value

  if conversion is not None and newValue is not None:
    newValue = conversion(newValue)

  return newValue
