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
"""Root Macro Application: use a macro in the Root application framework."""
from __future__ import absolute_import
__RCSID__ = "$Id"

from ILCDIRAC.Interfaces.API.NewInterface.Applications import _Root
from DIRAC import S_OK
import os


class RootMacro(_Root):
  """Run a root macro in the root application environment.

  Example:

  >>> rootmac = RootMacro()
  >>> rootmac.setMacro("mymacro.C")
  >>> rootmac.setArguments("some command line arguments")

  The :func:`setExtraCLIArguments` is not available here, use the :func:`setArguments`
  """

  def __init__(self, paramdict=None):
    super(RootMacro, self).__init__(paramdict)
    self._modulename = "RootMacroAnalysis"
    self.appname = 'root'
    self._moduledescription = 'Root macro execution'

  def setMacro(self, macro):
    """Define macro to use.

    :param str macro: Macro to run on. Must be a local C file.
    """
    self._checkArgs({'macro': (str,)})

    self.script = macro
    if os.path.exists(macro) or macro.lower().count("lfn:"):
      self.inputSB.append(macro)
    return S_OK()
