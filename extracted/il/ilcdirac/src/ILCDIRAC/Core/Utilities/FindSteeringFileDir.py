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
"""Obtain the related steering file directory given a certain software name, version and platform.

Created on Feb 10, 2012

:author: Stephane Poss
:since: Feb 10, 2012
"""

from __future__ import absolute_import
__RCSID__ = "$Id$"

from DIRAC import S_OK, S_ERROR
from ILCDIRAC.Core.Utilities.CombinedSoftwareInstallation import getSoftwareFolder, checkCVMFS
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
from ILCDIRAC.Core.Utilities.TARsoft import check


def getSteeringFileDirName(platform, application, applicationVersion):
  """Locate the path of the steering file directory assigned to the specified application."""
  ops = Operations()
  version = ops.getValue('/AvailableTarBalls/%s/%s/%s/Dependencies/steeringfiles/version' % (platform,
                                                                                             application,
                                                                                             applicationVersion), '')
  if not version:
    return S_ERROR("Could not find attached SteeringFile version")

  return getSteeringFileDir(platform, version)


def getSteeringFileDir(platform, version):
  """Return directly the directory, without passing by the dependency resolution."""
  res = checkCVMFS(platform, ['steeringfiles', version])
  if res['OK']:
    return S_OK(res['Value'][0])
  # Here means CVMFS is not defined, so we need to rely on the tar ball
  res = getSoftwareFolder(platform, 'steeringfiles', version)
  if not res['OK']:
    return res
  mySoftDir = res['Value']
  # check that all the files are there: software is not corrupted.
  res = check('steeringfiles.%s' % version, '.', [mySoftDir])
  if not res['OK']:
    return res
  return S_OK(mySoftDir)
