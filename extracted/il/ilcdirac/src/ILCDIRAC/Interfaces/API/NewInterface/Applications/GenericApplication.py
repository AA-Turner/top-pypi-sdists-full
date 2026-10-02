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
"""Interface for a GenericApplication.

Allows one to use a script in an application framework. Can also use a compiled executable as long as
all the libraries and supplemental files are available.

See here for more information about running your own executable: https://twiki.cern.ch/twiki/bin/view/CLIC/IlcdiracUserLibraries
"""
from __future__ import absolute_import
__RCSID__ = "$Id$"
import os

from DIRAC import S_OK, S_ERROR
from DIRAC.Core.Workflow.Parameter import Parameter

from ILCDIRAC.Interfaces.API.NewInterface.LCApplication import LCApplication


class GenericApplication(LCApplication):
  """Run a script (python or shell) in an application environment.

  Example:

  >>> ga = GenericApplication()
  >>> ga.setScript("myscript.py")
  >>> ga.setArguments("some command line arguments")
  >>> ga.setDependency({"root":"5.26"})

  In case you also use the :func:`setExtraCLIArguments` method, whatever you put
  in there will be added at the end of the command line, i.e., after the Arguments
  """

  def __init__(self, paramdict=None):
    self.script = None
    self.setupScript = ''
    self.arguments = ''
    self.dependencies = {}
    # The Application init has to come last as if not the passed parameters are overwritten by the defaults.
    super(GenericApplication, self).__init__(paramdict)
    # Those have to come last as the defaults from Application are not right
    self._modulename = "ApplicationScript"
    self.appname = self._modulename
    self._moduledescription = 'An Application script module that can execute any provided script in the given \
    project name and version environment'

  def setScript(self, script):
    """Define script to use.

    :param str script: Script to run. Can be shell or python or compiled executable. Can be local file or LFN.
    """
    self._checkArgs({'script': (str,)})
    if os.path.exists(script) or script.lower().count("lfn:"):
      self.inputSB.append(script)
    self.script = script
    return S_OK()

  def setSetupScript(self, setupScript):
    """Define setup script to use.

    :param str setupScript: Shell script to source. Can be local file or LFN.
    """
    self._checkArgs({'setupScript': (str,)})
    if not setupScript.endswith('.sh'):
      return S_ERROR("The script must be a shell file")

    if os.path.exists(setupScript) or setupScript.lower().count("lfn:"):
      self.inputSB.append(setupScript)
    self.setupScript = setupScript
    return S_OK()

  def setArguments(self, args):
    """ Optional: Define the arguments of the script

    :param str args: Arguments to pass to the command call
    """
    self._checkArgs({'args': (str,)})
    self.arguments = args
    return S_OK()

  def setDependency(self, appdict):
    """Define list of application you need.

    >>> app.setDependency({"mokka":"v0706P08","marlin":"v0111Prod"})

    :param dict appdict: Dictionary of application to use: {"App":"version"}
    """
    # check that dict has proper structure
    self._checkArgs({'appdict': dict})

    self.dependencies.update(appdict)
    return S_OK()

  def _applicationModule(self):
    m1 = self._createModuleDefinition()
    m1.addParameter(Parameter("script", "", "string", "", "", False, False, "Script to execute"))
    m1.addParameter(Parameter("arguments", "", "string", "", "", False, False, "Arguments to pass to the script"))
    m1.addParameter(Parameter("debug", False, "bool", "", "", False, False, "debug mode"))
    m1.addParameter(Parameter("setupScript", "", "string", "", "", False, False, "Script to source"))
    return m1

  def _applicationModuleValues(self, moduleinstance):
    moduleinstance.setValue("script", self.script)
    moduleinstance.setValue("setupScript", self.setupScript)
    moduleinstance.setValue('arguments', self.arguments)
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

  def _addParametersToStep(self, stepdefinition):
    res = self._addBaseParameters(stepdefinition)
    if not res["OK"]:
      return S_ERROR("Failed to set base parameters")
    return S_OK()

  def _setStepParametersValues(self, instance):
    self._setBaseStepParametersValues(instance)
    for depn, depv in self.dependencies.items():
      self._job._addSoftware(depn, depv)
    return S_OK()

  def _checkConsistency(self, job=None):
    """Checks that script and dependencies are set."""
    if not self.script:
      return S_ERROR("Script not defined")
    elif not self.script.lower().count("lfn:") and not os.path.exists(self.script):
      return S_ERROR("Specified script is not an LFN and was not found on disk")

    if self.setupScript and not self.setupScript.lower().count("lfn:") and not os.path.exists(self.setupScript):
      return S_ERROR("Specified source script is not an LFN and was not found on disk")

    # if not len(self.dependencies):
    #  return S_ERROR("Dependencies not set: No application to install. If correct you should use job.setExecutable")
    return S_OK()
