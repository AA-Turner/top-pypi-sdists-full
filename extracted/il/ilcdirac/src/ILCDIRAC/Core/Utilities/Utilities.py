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
"""Utility functions."""
from __future__ import absolute_import
from DIRAC import gLogger

LOG = gLogger.getSubLogger(__name__)


def toInt(number, cond=None):
  """Cast number parameter to an integer.

  >>> number = toInt("1000")

  :param number: the number to cast (number of events, number of jobs)
  :type number: str or int
  :param cond: unary function to check validity of number, range, etc.
  :return: The success or the failure of the casting
  :rtype: bool, int or None
  """
  if number is None:
    return number

  try:
    number = int(number)
  except ValueError:
    LOG.error("Argument is not an integer")
    return False
  if cond is not None and not cond(number):
    LOG.error("Argument does not pass condition: %r" % cond)
    return False
  return number


def listify(value, cast=None):
  """Turn a comma separate string into a list.

  :param str value: string to turn into a list
  :param cast: function to apply in all values, e.g., `int`
  :returns: list, empty elements are stripped
  """
  if isinstance(value, list):
    thisList = value
  else:
    thisList = [val.strip() for val in value.strip('[]').split(',') if val.strip()]
  if cast is not None:
    thisList = [cast(val) for val in thisList]
  return thisList


def canConvert(value, funType):
  """Check if value can be converted to a variable of type funType.

  >>> canConvert("5.",int)
  False

  >>> canConvert("3",int)
  True

  :param value: variable to be checked for conversion
  :param funType: function used for conversion e.g. int(), float()
  :return: True if can be converved to funType, else False
  :rtype: bool
  """
  try:
    funType(value)
    return True
  except ValueError:
    return False


def lowerFirst(inputString):
  """Return string with first charecter converted to lower case."""
  return inputString[0].lower() + inputString[1:]
