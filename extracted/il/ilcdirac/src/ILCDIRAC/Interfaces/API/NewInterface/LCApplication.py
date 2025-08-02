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
"""Linear Collider Application.

Allows setting the Steering File dependency, as well as other LC community things

:author: sposs
:since: Nov 1st, 2013
"""

from __future__ import absolute_import
from ILCDIRAC.Interfaces.API.NewInterface.LCUtilityApplication import LCUtilityApplication
from DIRAC.Core.Workflow.Parameter import Parameter

from DIRAC import S_OK

__RCSID__ = "$Id$"


class LCApplication(LCUtilityApplication):
  """LC specific implementation of the applications."""

  def __init__(self, paramdict=None):
    super(LCApplication, self).__init__(paramdict)
    self.steeringFileVersion = ""
    self.forgetAboutInput = False
    self._importLocation = "ILCDIRAC.Workflow.Modules"

  def setSteeringFileVersion(self, version):
    """Define the SteeringFile version to use.

    :param str version:
    """
    self.steeringFileVersion = version

    return S_OK()

  def setForgetAboutInput(self, flag=True):
    """Do not overwrite the input file set in the SteeringFile.

    :param bool flag: True or False
    """

    self.forgetAboutInput = flag

    return S_OK()

  def _getSpecificAppParameters(self, stepdef):
    """Overload of Application._getSpecificAppParameter."""
    stepdef.addParameter(Parameter("ForgetInput", False, "boolean", "", "", False, False,
                                   "Do not overwrite input steering"))
    if self.steeringFileVersion:
      stepdef.addParameter(Parameter("SteeringFileVers", "", "string", "", "", False, False,
                                     "SteeringFile version to use"))
    return S_OK()

  def _setSpecificAppParameters(self, stepinst):
    """Overload of Application._setSpecificAppParameters."""
    stepinst.setValue("ForgetInput", self.forgetAboutInput)

    if self.steeringFileVersion:
      stepinst.setValue("SteeringFileVers", self.steeringFileVersion)

    return S_OK()

  def _doSomethingWithJob(self):
    """Overloads the Application._doSomethingWithJob."""
    if self.steeringFileVersion:
      self._job._addSoftware("steeringfiles", self.steeringFileVersion)
    return S_OK()
# "
