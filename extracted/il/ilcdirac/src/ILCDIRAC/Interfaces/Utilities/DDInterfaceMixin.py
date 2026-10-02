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
"""Mixin for DD4hep interface functions."""

from __future__ import absolute_import
import os

from DIRAC import S_OK, S_ERROR, gLogger

LOG = gLogger.getSubLogger("ILCJob")


class DDInterfaceMixin(object):
  """Mixin for DD4hep interface functions.

  This mixin class requires that the main class should be of
  :class:`~ILCDIRAC.Interfaces.API.NewInterface.Application.Application` type and have the
  ``detectorModel``, ``_ops``, ``version``, and ``_log`` attributes.

   * ``_ops`` is an Operations instance
   * ``_log`` a gLogger sublogger
   * ``version`` is the version of the application
   * ``detectorModel`` is set to the name of the detector model as inferred in the :func:`setDetectorModel` function
  """

  def setDetectorModel(self, detectorModel):
    """Define detector model to use for ddsim simulation.

    The detector model can be a collection of XML files. Either one has to use a
    detector model provided by LCGeo or DD4hep, which can be found on CVMFS or
    the complete XML needs to be passed as a tarball in the input sandbox or on the grid

    >>> ddsim.setDetectorModel("CLIC_o3_v13") # detector model part of lcgeo

    >>> ddsim.setDetectorModel("CLIC_o3_v13.tar.gz") # local tarball, will be added to input sandbox

    >>> ddsim.setDetectorModel("LFN:/ilc/user/u/username/CLIC_o3_v13.tar.gz") # tarball on the grid

    The tarball name must be detectorModel plus extension.
    The tarball must contain all xml files inside a folder called detectorModel.
    That is the main file is located in *detectorModel/detectorModel.xml*

    :param str detectorModel: Detector Model to use for simulation or reconstruction. Can
      be on CVMFS, tarball LFN or inputSandbox tarball
    """
    self._checkArgs({'detectorModel': (str,)})
    extensions = (".zip", ".tar.gz", ".tgz")

    # file on the grid
    if detectorModel.lower().startswith("lfn:"):
      self.inputSB.append(detectorModel)
      self.detectorModel = os.path.basename(detectorModel)
      for ext in extensions:
        if detectorModel.endswith(ext):
          self.detectorModel = os.path.basename(detectorModel).replace(ext, '')
      return S_OK()

    # local file
    elif detectorModel.endswith(extensions):
      for ext in extensions:
        if detectorModel.endswith(ext):
          self.detectorModel = os.path.basename(detectorModel).replace(ext, '')
          break

      if os.path.exists(detectorModel):
        self.inputSB.append(detectorModel)
      else:
        LOG.notice("Specified detector model file does not exist locally, I hope you know what you're doing")
      return S_OK()

    # DetectorModel is part of the software
    else:
      knownDetectors = self.getKnownDetectorModels()
      if not knownDetectors['OK']:
        return self._reportError("Failed to get knownDetectorModels: %s" % knownDetectors["Message"])
      elif detectorModel in knownDetectors['Value']:
        self.detectorModel = detectorModel
      else:
        return self._reportError("Unknown detector model in %s: %s" % (self.appname, detectorModel))
    return S_OK()

  def getKnownDetectorModels(self, version=None):
    """return a list of known detectorModels.

    Depends on the version of the software though...

    :param str version: Optional: Software version for which to print the detector models. If not given the version of the application instance is used.
    :returns: S_OK with list of detector models known for this software version, S_ERROR
    """
    if version is None and not self.version:
      return S_ERROR("No software version defined")
    detectorModels = self._ops.getOptionsDict("/DDSimDetectorModels/%s" % (self.version))
    return detectorModels
