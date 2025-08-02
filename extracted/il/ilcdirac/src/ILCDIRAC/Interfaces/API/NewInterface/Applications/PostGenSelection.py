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
PostGenSelection : Helper to filter generator selection
"""

from __future__ import absolute_import

from DIRAC import S_OK, S_ERROR
from DIRAC.Core.Workflow.Parameter import Parameter

from ILCDIRAC.Interfaces.API.NewInterface.LCUtilityApplication import LCUtilityApplication
import six

__RCSID__ = "$Id$"


class PostGenSelection(LCUtilityApplication):
  """Helper to filter generator selection.

  Example:

  >>> postGenSel = PostGenSelection()
  >>> postGenSel.setNbEvtsToKeep(30)
  """

  def __init__(self, paramdict=None):

    self.numberOfEventsToKeep = 0
    super(PostGenSelection, self).__init__(paramdict)
    self._modulename = "PostGenSelection"
    self.appname = 'postgensel'
    self._moduledescription = 'Helper to filter generator selection'

  def setNbEvtsToKeep(self, numberOfEventsToKeep):
    """Set the number of events to keep in the input file.

    :param int numberOfEventsToKeep: number of events to keep in the input file. Must be inferior to the number of events.
    """
    self._checkArgs({'numberOfEventsToKeep': int})

    self.numberOfEventsToKeep = numberOfEventsToKeep
    return S_OK()

  def _applicationModule(self):
    m1 = self._createModuleDefinition()
    m1.addParameter(Parameter("NbEvtsKept", 0, "int", "", "", False, False, "Number of events to keep"))
    m1.addParameter(Parameter("debug", False, "bool", "", "", False, False, "debug mode"))
    return m1

  def _applicationModuleValues(self, moduleinstance):
    moduleinstance.setValue('NbEvtsKept', self.numberOfEventsToKeep)
    moduleinstance.setValue('debug', self.debug)

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

    if not self.numberOfEventsToKeep:
      return S_ERROR('Number of events to keep was not given! Throw your brain to the trash and try again!')

    # res = self._checkRequiredApp() ##Check that job order is correct
    # if not res['OK']:
    #  return res

    return S_OK()

  def _checkWorkflowConsistency(self):
    return self._checkRequiredApp()

  def _resolveLinkedStepParameters(self, stepinstance):
    if isinstance(self._linkedidx, six.integer_types):
      self._inputappstep = self._jobsteps[self._linkedidx]
    if self._inputappstep:
      stepinstance.setLink("InputFile", self._inputappstep.getType(), "OutputFile")
    return S_OK()
