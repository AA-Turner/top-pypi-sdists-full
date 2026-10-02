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
SLCIOSplit : Helper to split SLCIO files
"""

from __future__ import absolute_import

from DIRAC.Core.Workflow.Parameter import Parameter
from DIRAC import S_OK, S_ERROR, gLogger

from ILCDIRAC.Interfaces.API.NewInterface.LCUtilityApplication import LCUtilityApplication
import six

LOG = gLogger.getSubLogger(__name__)
__RCSID__ = "$Id$"


class SLCIOSplit(LCUtilityApplication):
  """Helper to split slcio files.

  Example:

  >>> slciosplit = SLCIOSplit()
  >>> slciosplit.setInputFile( "slcioFile_1.slcio" )
  >>> slciosplit.setNumberOfEventsPerFile(100)
  """

  def __init__(self, paramdict=None):
    self.numberOfEventsPerFile = 0
    super(SLCIOSplit, self).__init__(paramdict)
    if not self.version:
      self.version = 'HEAD'
    self._modulename = "LCIOSplit"
    self.appname = 'lcio'
    self._moduledescription = 'Helper call to split SLCIO files'

  def setNumberOfEventsPerFile(self, numberofevents):
    """Number of events to have in each file.

    "param int numberofevents: number of events in the output files
    """
    self._checkArgs({'numberofevents': int})
    self.numberOfEventsPerFile = numberofevents

  def _applicationModule(self):
    m1 = self._createModuleDefinition()
    m1.addParameter(Parameter("debug", False, "bool", "", "", False, False, "debug mode"))
    m1.addParameter(Parameter("nbEventsPerSlice", 0, "int", "", "", False, False,
                                "Number of events per output file"))
    return m1

  def _applicationModuleValues(self, moduleinstance):
    moduleinstance.setValue('debug', self.debug)
    moduleinstance.setValue('nbEventsPerSlice', self.numberOfEventsPerFile)

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
    """Checks that all needed parameters are set."""

    # steal the datatype and detector type from the job (for production):
    if hasattr(self._job, "datatype"):
      self.datatype = self._job.datatype
    if hasattr(self._job, "detector"):
      self.detectortype = self._job.detector

    # This is needed for metadata registration
    self.numberOfEvents = self.numberOfEventsPerFile

    if not self.outputFile and self._jobtype == 'User':
      LOG.error('No output file name specified.')

    if self._jobtype != 'User':
      self._listofoutput.append({"outputFile": "@{OutputFile}", "outputPath": "@{OutputPath}",
                                 "outputDataSE": '@{OutputSE}'})
      self.prodparameters['nb_events_per_file'] = self.numberOfEventsPerFile

    return S_OK()

  def _checkWorkflowConsistency(self):
    return self._checkRequiredApp()

  def _resolveLinkedStepParameters(self, stepinstance):
    if isinstance(self._linkedidx, six.integer_types):
      self._inputappstep = self._jobsteps[self._linkedidx]
    if self._inputappstep:
      stepinstance.setLink("InputFile", self._inputappstep.getType(), "OutputFile")
    return S_OK()
