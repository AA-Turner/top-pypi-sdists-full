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
"""ROOT class for common functionality of :doc:`RootScript` and :doc:`RootMacro`."""

from __future__ import absolute_import

from DIRAC import S_OK, S_ERROR, gLogger
from DIRAC.Core.Workflow.Parameter import Parameter

from ILCDIRAC.Interfaces.API.NewInterface.LCApplication import LCApplication
import six

LOG = gLogger.getSubLogger(__name__)
__RCSID__ = "$Id"


class _Root(LCApplication):
  """Root principal class.

  Will inherit in :doc:`RootScript` and :doc:`RootMacro` classes, so don't use this (you can't anyway)!
  """

  def __init__(self, paramdict=None):
    self.arguments = ''
    self.script = None
    super(_Root, self).__init__(paramdict)

  def setScript(self, script):
    """Base method, overloaded in :mod:`~ILCDIRAC.Interfaces.API.NewInterface.Applications.RootScript`"""
    LOG.error("Don't use this!")
    return S_ERROR("Not allowed here")

  def setMacro(self, macro):
    """Base method, overloaded in :mod:`~ILCDIRAC.Interfaces.API.NewInterface.Applications.RootMacro`"""
    LOG.error("Don't use this!")
    return S_ERROR("Not allowed here")

  def setArguments(self, args):
    """ Optional: Define the arguments of the script

    :param str args: Arguments to pass to the command line call

    Note for RootMacro string arguments need to be passed as a raw string with the quotation marks escaped.
    E.g.:

    >>> root = RootMacro()
    >>> root.setArguments(r"\\"myString\\"")

    """
    self._checkArgs({'args': (str,)})
    self.arguments = args
    return S_OK()

  def _applicationModule(self):
    m1 = self._createModuleDefinition()
    m1.addParameter(Parameter("arguments", "", "string", "", "", False, False, "Arguments to pass to the script"))
    m1.addParameter(Parameter("script", "", "string", "", "", False, False, "Script to execute"))
    m1.addParameter(Parameter("debug", False, "bool", "", "", False, False, "debug mode"))
    return m1

  def _applicationModuleValues(self, moduleinstance):
    moduleinstance.setValue('arguments', self.arguments)
    moduleinstance.setValue("script", self.script)
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
    """Checks that script is set."""
    if not self.script:
      return S_ERROR("Script or macro not defined")
    if not self.version:
      return S_ERROR("You need to specify the Root version")

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
