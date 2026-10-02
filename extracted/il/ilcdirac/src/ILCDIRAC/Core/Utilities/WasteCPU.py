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
"""This is the worst piece of code ever NEEDED: just run some CPU intensive code to waste CPU time.

:author: Stephane Poss
:since: Jul 26, 2011
"""

from __future__ import absolute_import
from datetime import datetime
from math import log
from DIRAC import S_OK, S_ERROR

__RCSID__ = "$Id$"


def wasteCPUCycles(timecut):
  """Waste, waste, and waste more CPU."""
  number = 1e31
  first = datetime.utcnow()
  try:
    while (datetime.utcnow() - first).total_seconds() < timecut:
      try:
        number = log(number)
      except ValueError as x:
        return S_ERROR("Failed to waste %s CPU seconds:%s" % (timecut, str(x)))
      if number <= 0:
        number = -number + 4
  except Exception as e:  # pylint: disable=broad-except
    return S_ERROR("Failed to waste %s CPU seconds, OtherException: %r" % (timecut, e))
  return S_OK("Successfully wasted %s seconds" % timecut)
