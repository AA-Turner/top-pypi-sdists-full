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
"""Utility functions for DD4hep geometry files etc."""

from __future__ import absolute_import
import os
import tarfile
from DIRAC.Core.Utilities.Subprocess import shellCall


from DIRAC import S_OK, S_ERROR, gLogger

from ILCDIRAC.Core.Utilities.CombinedSoftwareInstallation import unzip_file_into_dir, getEnvironmentScript, getSoftwareFolder

LOG = gLogger.getSubLogger(__name__)


class DD4hepMixin(object):
  """mixin class for DD4hep functionality."""

  def _getDetectorXML(self):
    """returns the path to the detector XML file.

    Checks the Configuration System for the Path to DetectorModels or extracts the input sandbox detector xml files

    :returns: S_OK(PathToXMLFile), S_ERROR
    """
    if os.path.exists(os.path.join(self.detectorModel, self.detectorModel + ".xml")):
      LOG.notice("Found detector model: %s" % os.path.join(self.detectorModel, self.detectorModel + ".xml"))
      return S_OK(os.path.join(self.detectorModel, self.detectorModel + ".xml"))
    elif os.path.exists(self.detectorModel + ".zip"):
      LOG.notice("Found detector model zipFile: %s" % self.detectorModel + ".zip")
      return self._extractZip()
    elif os.path.exists(self.detectorModel + ".tar.gz"):
      LOG.notice("Found detector model tarball: %s" % self.detectorModel + ".tar.gz")
      return self._extractTar()
    elif os.path.exists(self.detectorModel + ".tgz"):
      LOG.notice("Found detector model tarball: %s" % self.detectorModel + ".tgz")
      return self._extractTar(extension=".tgz")

    detectorModels = self.ops.getOptionsDict("/DDSimDetectorModels/%s" % (self.applicationVersion))
    if not detectorModels['OK']:
      LOG.error("Failed to get list of DetectorModels from the ConfigSystem", detectorModels['Message'])
      return S_ERROR("Failed to get list of DetectorModels from the ConfigSystem")

    res = getEnvironmentScript(self.platform, self.applicationName, self.applicationVersion, self.getEnvScript)
    if not res['OK']:
      LOG.error("Could not obtain the environment script: ", res["Message"])
      return res
    envScriptPath = res["Value"]

    # getting the value of the detectors XML directory.
    envVariableName = self.ops.getValue(f"/DDSimDetectorModels/{self.applicationVersion}/EnvironmentVariable", None)

    if self.detectorModel in detectorModels['Value']:

      if envVariableName or detectorModels['Value'][self.detectorModel].startswith("/"):
        res = shellCall(0, "source %s > /dev/null; echo $%s" % (envScriptPath, envVariableName), callbackFunction=None, bufferLimit=20971520)
        if not res['OK']:
          LOG.error("Failed to obtain the detector XML location: ", res["Message"])
          return res
        softwareRoot = res['Value'][1].strip()

      else:
        softwareFolder = getSoftwareFolder(self.platform, self.applicationName, self.applicationVersion)
        if not softwareFolder['OK']:
          LOG.error("Failed to obtain the detector XML location: ", res["Message"])
          return softwareFolder
        softwareRoot = softwareFolder['Value']

      detModelPath = os.path.join(softwareRoot, detectorModels['Value'][self.detectorModel])
      LOG.info("Found path for DetectorModel %s in CS: %s " % (self.detectorModel, detModelPath))
      return S_OK(detModelPath)

    LOG.error('Detector model %s was not found neither locally nor on the web, exiting' % self.detectorModel)
    return S_ERROR('Detector model was not found')

  def _extractTar(self, extension=".tar.gz"):
    """extract the detector tarball for the detectorModel."""
    try:
      detTar = tarfile.open(self.detectorModel + extension, "r:gz")
      detTar.extractall()
      xmlPath = os.path.abspath(os.path.join(self.detectorModel, self.detectorModel + ".xml"))
      return S_OK(xmlPath)
    except (RuntimeError, OSError, IOError) as e:
      LOG.error("Failed to untar detector model", str(e))
      return S_ERROR("Failed to untar detector model")

  def _extractZip(self):
    """extract the detector zip file for the detectorModel."""
    try:
      LOG.notice("Exracting zip file")
      unzip_file_into_dir(open(self.detectorModel + ".zip", 'rb'), os.getcwd())
      xmlPath = os.path.join(os.getcwd(), self.detectorModel, self.detectorModel + ".xml")
      return S_OK(xmlPath)
    except (RuntimeError, OSError, IOError) as err:  # RuntimeError is for zipfile
      LOG.error('Failed to unzip detector model: ', str(err))
      return S_ERROR('Failed to unzip detector model')
