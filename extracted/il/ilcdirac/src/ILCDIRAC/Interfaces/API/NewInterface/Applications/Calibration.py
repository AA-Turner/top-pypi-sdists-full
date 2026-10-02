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
"""Application used by the Calibration system, not for user jobs."""
from __future__ import absolute_import
from ILCDIRAC.Interfaces.API.NewInterface.Applications import Marlin

from DIRAC import S_OK
from DIRAC.Core.Workflow.Parameter import Parameter

__RCSID__ = "$Id$"


class Calibration(Marlin):
  """Application used in the Calibration System.

  .. warn: Not For user jobs
  """

  def __init__(self, paramdict=None):
    """Initialize."""
    self.calibrationID = 0
    self.workerID = 0
    self.baseSteeringFile = None
    super(Calibration, self).__init__(paramdict)
    # Those 5 need to come after default constructor
    self._modulename = 'Calibration'
    self._moduledescription = 'Module to run calibration'
    self.appname = 'marlin'

  def _checkConsistency(self, job=None):

    super(Calibration, self)._checkConsistency(job)

    return S_OK()

  def _applicationModule(self):
    md1 = super(Calibration, self)._applicationModule()

    md1.addParameter(Parameter("calibrationID", '0', "int", "", "", False, False,
                               "calibration ID"))
    md1.addParameter(Parameter("workerID", '0', "int", "", "", False, False,
                               "worker ID"))
    md1.addParameter(Parameter("baseSteeringFile", '', "string", "", "", False, False,
                               "basic steering file for calibration reconstructions"))
    return md1

  def _applicationModuleValues(self, moduleinstance):

    super(Calibration, self)._applicationModuleValues(moduleinstance)

    moduleinstance.setValue("calibrationID", self.calibrationID)
    moduleinstance.setValue("workerID", self.workerID)
    moduleinstance.setValue("baseSteeringFile", self.baseSteeringFile)

  def setCalibrationID(self, calibrationID):
    """Set calibrationID.

    :param int calibrationID: ID of calibration
    """
    self._checkArgs({'calibrationID': int})
    self.calibrationID = calibrationID

  def setWorkerID(self, workerID):
    """Set workerID.

    :param int workerID: ID of worker node
    """
    self._checkArgs({'workerID': int})
    self.workerID = workerID
