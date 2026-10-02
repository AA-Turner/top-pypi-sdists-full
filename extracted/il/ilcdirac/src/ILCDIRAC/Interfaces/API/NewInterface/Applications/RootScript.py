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
"""Root Script Application: use a script in the Root application framework."""
from __future__ import absolute_import
__RCSID__ = "$Id"

from ILCDIRAC.Interfaces.API.NewInterface.Applications import _Root
from DIRAC import S_OK
import os


class RootScript(_Root):
  """Run a script (root executable or shell) in the root application environment.

  Example:

  >>> rootsc = RootScript()
  >>> rootsc.setScript("myscript.exe")
  >>> rootsc.setArguments("some command line arguments")

  Or use an executable in the PATH, for example *hadd* to merge root files:

  >>> rootsc = RootScript()
  >>> rootsc.setScript("hadd")
  >>> rootsc.setArguments("output.root input1.root input2.root")

  The :func:`setExtraCLIArguments` is not available here, use the :func:`setArguments`
  """

  def __init__(self, paramdict=None):
    super(RootScript, self).__init__(paramdict)
    self._modulename = "RootExecutableAnalysis"
    self.appname = 'root'
    self._moduledescription = 'Root application script'

  def setScript(self, executable):
    """Define executable to use.

    :param str executable: Script to run on. Can be shell or root
      executable. Must be a local file or in the PATH when using CVMFS based
      software.
    """
    self._checkArgs({'executable': (str,)})

    self.script = executable
    if os.path.exists(executable) or executable.lower().count("lfn:"):
      self.inputSB.append(executable)
    return S_OK()
