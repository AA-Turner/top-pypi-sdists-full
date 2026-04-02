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
StdHepSplit : Helper to split Stdhep files
"""

from __future__ import absolute_import

from DIRAC.Core.Workflow.Parameter import Parameter
from DIRAC import S_OK, S_ERROR, gLogger

from ILCDIRAC.Interfaces.API.NewInterface.LCUtilityApplication import LCUtilityApplication
import six

LOG = gLogger.getSubLogger(__name__)

__RCSID__ = "$Id$"


class StdHepSplit(LCUtilityApplication):
  """Helper to split stdhep files.

  Example:

  >>> stdhepsplit = StdHepSplit()
  >>> stdhepsplit.setInputFile( "File_1.stdhep" )
  >>> stdhepsplit.setNumberOfEventsPerFile(100)
  >>> stdhepsplit.setOutputFile("somefile.stdhep")

  The outpufiles will then be *somefile_X.stdhep*, where *X* corresponds to the slice index
  """

  def __init__(self, paramdict=None):
    self.numberOfEventsPerFile = 0
    self.maxRead = 0
    super(StdHepSplit, self).__init__(paramdict)
    if not self.version:
      self.version = 'V2'
    self._modulename = "StdHepSplit"
    self.appname = 'stdhepsplit'
    self._moduledescription = 'Helper call to split Stdhep files'

  def setNumberOfEventsPerFile(self, numberofevents):
    """Number of events to have in each file.

    :param int numberofevents: number of events in each output file
    """
    self._checkArgs({'numberofevents': int})
    self.numberOfEventsPerFile = numberofevents

  def setMaxRead(self, maxRead):
    """set the number of events to get out of the input stdhep file.

    :param int maxRead: number of events to get out of the input stdhep file

    .. note::

      We already correct for the off-by-1 error of hepslit by using maxRead+1, which results in maxRead events read.
    """
    self._checkArgs({'maxRead': int})
    self.maxRead = maxRead

  def checkProductionMetaData(self, metaDict):
    """Make sure NumberOfEvents is set to the number of events after splitting.

    :param dict metaDict: production job metadata dictionary, will be updated
    :returns: S_OK, S_ERROR
    """

    if 'NumberOfEvents' in metaDict:
      metaDict['NumberOfEvents'] = self.numberOfEventsPerFile
    return super(StdHepSplit, self).checkProductionMetaData(metaDict)

  def _applicationModule(self):
    m1 = self._createModuleDefinition()
    m1.addParameter(Parameter("debug", False, "bool", "", "", False, False, "debug mode"))
    m1.addParameter(Parameter("maxRead", 0, "int", "", "", False, False, "max events to read"))
    m1.addParameter(Parameter("nbEventsPerSlice", 0, "int", "", "", False, False,
                                "Number of events per output file"))
    return m1

  def _applicationModuleValues(self, moduleinstance):
    moduleinstance.setValue('debug', self.debug)
    moduleinstance.setValue('nbEventsPerSlice', self.numberOfEventsPerFile)
    moduleinstance.setValue('maxRead', self.maxRead)

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

    # This is needed for metadata registration
    self.numberOfEvents = self.numberOfEventsPerFile

    if not self.outputFile and self._jobtype == 'User':
      LOG.notice('No output file name specified.')

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
