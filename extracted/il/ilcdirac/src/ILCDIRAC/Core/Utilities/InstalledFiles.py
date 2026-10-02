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
"""List of files in the SteeringFiles tar ball.

:author: S. Poss
:since: Nov 8, 2011
"""

from __future__ import absolute_import
import os

from DIRAC import S_OK, S_ERROR, gLogger
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
from DIRAC.DataManagementSystem.Client.DataManager import DataManager

from ILCDIRAC.Core.Utilities.CombinedSoftwareInstallation import extractTarball

LOG = gLogger.getSubLogger(__name__)

def Exists(myfile, platform=None, configversion=None):
  """check if the file exists in the tarball First based on a list of files.

  Also checks if CVMFS is used for the configuration package (ILDConfig) set by
  :func:`~ILCDIRAC.Interfaces.API.NewInterface.UserJob.UserJob.setILDConfig`
  If CVMFS is not available in the submission machine, but ILDConfig is on CVMFS we assume the file exists.

  :param str myfile: filename to be checked
  :param str platform: requested platform, optional
  :param str configversion: ILDConfig version defined for the :class:`~ILCDIRAC.Interfaces.API.NewInterface.UserJob.UserJob`
  :returns: S_OK/S_ERROR
  """
  files = ["defaultClicCrossingAngle.mac", "clic_ild_cdr500.steer",
           "clic_ild_cdr.steer", "clic_cdr_prePandora.lcsim",
           "clic_cdr_postPandora.lcsim", "clic_cdr_prePandoraOverlay.lcsim",
           "clic_cdr_prePandoraOverlay_1400.0.lcsim",
           "clic_cdr_prePandoraOverlay_3000.0.lcsim",
           "clic_cdr_postPandoraOverlay.lcsim", "clic_ild_cdr.gear",
           "clic_ild_cdr500.gear", "clic_ild_cdr_steering_overlay.xml",
           "clic_ild_cdr_steering_overlay_3000.0.xml",
           "clic_ild_cdr_steering_overlay_1400.0.xml",
           "clic_ild_cdr500_steering_overlay.xml",
           "clic_ild_cdr500_steering_overlay_350.0.xml",
           "clic_ild_cdr_steering.xml",
           "clic_ild_cdr500_steering.xml", "GearOutput.xml",
           'cuts_e1e1ff_500gev.txt',
           "cuts_e2e2ff_500gev.txt", 'cuts_qq_nunu_1400.txt',
           'cuts_e3e3nn_1400.txt',
           "cuts_e3e3_1400.txt", "cuts_e1e1e3e3_o_1400.txt",
           "cuts_aa_e3e3_o_1400.txt",
           "cuts_aa_e3e3nn_1400.txt", "cuts_aa_e2e2e3e3_o_1400.txt",
           "cuts_aa_e1e1e3e3_o_1400.txt",
           "defaultStrategies_clic_sid_cdr.xml",
           "defaultIlcCrossingAngle.mac",
           "defaultIlcCrossingAngleZSmearing320.mac",
           "defaultIlcCrossingAngleZSmearing225.mac",
           "sid_dbd_pandoraSettings.xml",
           "sid_dbd_postPandora.xml",
           "sid_dbd_prePandora.xml",
           "sid_dbd_prePandora_noOverlay.xml",
           "sid_dbd_vertexing.xml",
           "sidloi3.gear",
           "sidloi3_trackingStrategies.xml",
           "sidloi3_trackingStrategies_default.xml",
           "ild_00.gear",
           "ild_00_steering.xml",
           "ild_00.steer",
           "cuts_quarks_1400.txt", "cuts_taus_1400.txt",
           "cuts_h_gammaZ_1400.txt", "cuts_h_gammagamma_1400.txt",
           "cuts_h_mumu_3000.txt", 
           "card_IDEA.tcl", "edm4hep_IDEA.tcl",
           "k4simdelphesalg_pythia.py",
           "DECAY.dec",
           "evt.pdl",
           "cld_steer.py",
           "fcc_steer.py",
           "CLDReconstruction.py",
           ]
  if myfile in files:
    return S_OK()
  elif configversion is None or platform is None:
    return S_ERROR("File %s is not available locally nor in the software installation." % myfile)

  app = configversion.split("Config")[0] + "Config"
  version = configversion.split("Config")[1]
  if configPath := Operations().getValue(f"/AvailableTarBalls/{platform}/{app.lower()}/{version}/CVMFSPath", ""):
    return _checkInCVMFS(myfile, configPath)

  # if there is no CVMFSPath defined for the config version, we check the tarball
  # we only download and extract if it does not yet exist
  baseDir = "tmp_config_checks"
  tarballUrl = Operations().getValue(f"/AvailableTarBalls/{platform}/{app.lower()}/TarBallURL", "")
  tarball = Operations().getValue(f"/AvailableTarBalls/{platform}/{app.lower()}/{version}/TarBall", "")
  tarballDir = os.path.splitext(tarball)[0]
  LFN = os.path.join(tarballUrl, tarball)
  if not os.path.exists(os.path.join(baseDir, tarball)):
    if not (resDM := DataManager().getFile(LFN, destinationDir=baseDir))["OK"]:
      return resDM
    if not (resET := extractTarball(f"{baseDir}/{tarball}", directory=baseDir))["OK"]:
      return resET

  checkPath = os.path.join(baseDir, tarballDir, myfile)
  LOG.info(f"Checking for {checkPath}")
  if os.path.exists(checkPath):
    LOG.info(f"Found {myfile} in config package")
    return S_OK()
  return S_ERROR(f"Could not find {myfile} in the specified config tarball")


def _checkInCVMFS(cFile, configPath):
  """check if the file is available on cvmfs or not."""

  # check if cvmfs exists on this machine, if not we guess the person knows what they are doing
  if not os.path.exists("/cvmfs"):
    LOG.warn("CMVFS does not exist on this machine, cannot check for file existance.")
    return S_OK()

  if os.path.exists(os.path.join(configPath, cFile)):
    LOG.info("Found file on CVMFS %s/%s" % (configPath, cFile))
    return S_OK()
  else:
    LOG.error("Cannot find file %s in cvmfs folder: %s  " % (cFile, configPath))
    return S_ERROR("Cannot find file on cvmfs")
