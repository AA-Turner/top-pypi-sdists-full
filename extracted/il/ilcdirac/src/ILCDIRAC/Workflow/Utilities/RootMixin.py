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
"""Shared functionality for :mod:`~ILCDIRAC.Workflow.Modules.RootMacroAnalysis` and :mod:`~ILCDIRAC.Workflow.Modules.RootExecutableAnalysis`"""

from __future__ import absolute_import
import os

from DIRAC import S_OK, S_ERROR


class RootMixin(object):
  """Mixin class for :mod:`~ILCDIRAC.Workflow.Modules.RootMacroAnalysis` and :mod:`~ILCDIRAC.Workflow.Modules.RootExecutableAnalysis`"""

  def getRootEnvScript(self, _platform, _appname, _appversion):
    """create the environment script if it is not already available.

    Need to set LD_LIBRARY_PATH and PATH based on ROOTSYS

    As this is only called when we are not CVMFS native the ROOTSYS must have
    been set by :func:`~ILCDIRAC.Core.Utilities.TARsoft.configureRoot`. Function
    signature must conform to
    :func:`~ILCDIRAC.Core.Utilities.CombinedSoftwareInstallation.getEnvironmentScript`,
    but none of the arguments are used.

    :param str _platform: Unused, Software platform
    :param str _appname: Unused, application name
    :param str _appversion: Unused, application version
    :returns: S_OK( pathToScript )
    """
    if 'ROOTSYS' not in os.environ:
      self.log.error("ROOTSYS is not set")
      return S_ERROR("ROOTSYS is not set")
    self.log.info("Creating RootEnv.sh with ROOTSYS: %s " % os.environ['ROOTSYS'])

    scriptName = "rootEnv.sh"
    with open(scriptName, "w") as script:
      if 'LD_LIBRARY_PATH' in os.environ:
        script.write('declare -x LD_LIBRARY_PATH=$ROOTSYS/lib:$LD_LIBRARY_PATH\n')
      else:
        script.write('declare -x LD_LIBRARY_PATH=$ROOTSYS/lib\n')
        script.write('declare -x PATH=$ROOTSYS/bin:$PATH\n')
    return S_OK(os.path.join(os.getcwd(), scriptName))
