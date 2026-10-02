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
"""
 PYTHIA: Second Generator application
"""
from __future__ import absolute_import
__RCSID__ = "$Id$"

from ILCDIRAC.Interfaces.API.NewInterface.LCApplication import LCApplication
from DIRAC import S_OK, S_ERROR


class Pythia(LCApplication):
  """Call pythia.

  Usage:

  >>> py = Pythia()
  >>> py.setVersion("tt_500gev_V2")
  >>> py.setEnergy(500) #Can look like a duplication of info, but trust me, it's needed.
  >>> py.setNbEvts(50)
  >>> py.setOutputFile("myfile.stdhep")
  """

  def __init__(self, paramdict=None):
    self.eventType = ''
    super(Pythia, self).__init__(paramdict)
    self.appname = 'pythia'
    self._modulename = 'PythiaAnalysis'
    self._moduledescription = 'Module to run PYTHIA'
    self.datatype = 'gen'

  def willCut(self):
    """You need this if you plan on cutting using :mod:`~ILCDIRAC.Interfaces.API.NewInterface.Applications.StdhepCut`"""
    self.willBeCut = True

  def _applicationModule(self):
    m1 = self._createModuleDefinition()
    return m1

  def _userjobmodules(self, stepdefinition):
    res1 = self._setApplicationModuleAndParameters(stepdefinition)
    res2 = self._setUserJobFinalization(stepdefinition)
    if not res1["OK"] or not res2["OK"]:
      return S_ERROR('userjobmodules failed')
    return S_OK()

  def _prodjobmodules(self, stepdefinition):
    res1 = self._setApplicationModuleAndParameters(stepdefinition)
    res2 = self._setOutputComputeDataList(stepdefinition)
    if not res1["OK"] or not res2["OK"]:
      return S_ERROR('prodjobmodules failed')
    return S_OK()

  def _checkConsistency(self, job=None):
    if not self.version:
      return S_ERROR("Version not specified")

    # Resolve event type, needed for production jobs
    self.eventType = self.version.split("_")[0]

    if not self.numberOfEvents:
      return S_ERROR("Number of events to generate not defined")

    if not self.outputFile:
      return S_ERROR("Output File not defined")

    if not self._jobtype == 'User':
      if not self.willBeCut:
        self._listofoutput.append({"outputFile": "@{OutputFile}", "outputPath": "@{OutputPath}",
                                   "outputDataSE": '@{OutputSE}'})
      self.prodparameters['nbevts'] = self.numberOfEvents
      self.prodparameters['Process'] = self.eventType

    return S_OK()
