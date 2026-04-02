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
"""Babayaga Application to run applications based on Babayaga.

.. versionadded:: v34r0

Usage:

>>> babayaga = Babayaga()
>>> babayaga.setVersion('key4hep-latest')
>>> babayaga.setRandomSeed(12340)
>>> babayaga.setEnergy(91.2)
>>> babayaga.setNumberOfEvents(100)
>>> babayaga.setOutputFile('output.lhe')

"""

from __future__ import absolute_import
import os

from ILCDIRAC.Interfaces.API.NewInterface.LCApplication import LCApplication
from DIRAC import S_OK, S_ERROR, gLogger
from DIRAC.Core.Workflow.Parameter import Parameter
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations

LOG = gLogger.getSubLogger(__name__)
__RCSID__ = "$Id$"

class Babayaga(LCApplication):
  """Babayaga Application Class."""
  def __init__(self, paramdict=None):
    self.randomSeed = -1
    self.debugLevel = 0
    self.babayagaConfigFile = ''
    super(Babayaga, self).__init__(paramdict)

    # Those 5 need to come after default constructor
    self._modulename = 'BabayagaAnalysis'
    self._moduledescription = 'Module to run Babayaga'
    self.appname = 'babayaga'
    self.datatype = 'GEN'
    self._ops = Operations()
    self._extension = 'lhe'

  def setConfigFile(self, babayagaConfigFilePath):
    """Set the Babayaga options to be used.

    :param str babayagaConfigFilePath: Path to the Babayaga input file.
    """
    self._checkArgs({'babayagaConfigFilePath': (str,)})

    # Chech if file exist
    if not os.path.isfile(babayagaConfigFilePath):
      return self._reportError('Babayaga config file does not exist!')

    # Read file
    self.babayagaConfigFile = open(babayagaConfigFilePath).read()

    return None
  
  def setRandomSeed(self, randomSeed):
    """Define random seed to use. Default is the jobID.

    :param int randomSeed: Seed to use during simulation.
    """
    self._checkArgs({'randomSeed': int})
    self.randomSeed = randomSeed
    return S_OK()

  def setArguments(self, args):
    """Define the arguments of the script.

    Alternative to :func:`Babayaga.setExtraCLIArguments`.

    :param str args: Arguments to pass to the command call
    """
    self._checkArgs({'args': (str,)})
    self.extraCLIArguments = args
    return S_OK()
  
  def setBabayagaConfigFile(self, babayagaConfigFilePath):
    """Set the babayaga configuration file.

    :param str babayagaConfigFilePath: Name of the Babayaga configuration file path.
    """
    self._checkArgs({'babayagaConfigFilePath': (str,)})
    if not os.path.isfile(babayagaConfigFilePath):
      return self._reportError('Babayaga configuration file does not exist!')
    self.babayagaConfigFileContent = open(babayagaConfigFilePath).read()
    return S_OK()
  
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
    """Check consistency of the Babayaga application, this is called from the `Job` instance.

    :param job: The instance of the job
    :type job: ~ILCDIRAC.Interfaces.API.NewInterface.Job.Job
    :returns: S_OK/S_ERROR
    """

    if not self.version:
      return S_ERROR('No version found!')

    if self.babayagaConfigFile:
      return S_OK()

    if self._jobtype != 'User':
      self._listofoutput.append({"outputFile": "@{OutputFile}", "outputPath": "@{OutputPath}",
                                 "outputDataSE": '@{OutputSE}'})
      return S_OK()

    if not self.energy and not self.numberOfEvents and not self.outputFile:
      return S_ERROR('No config file set!')
    if not self.energy:
      return S_ERROR('No energy set!')
    if not self.numberOfEvents:
      return S_ERROR('No number of events set!')
    if not self.outputFile:
      return S_ERROR('No output file set!')
    if self.randomSeed < -1:
      return S_ERROR('Random Seed has to be equal or greater than -1')
    return S_OK()

  
  def _applicationModule(self):
    md1 = self._createModuleDefinition()
    md1.addParameter(Parameter("randomSeed", 0, "int", "", "", False, False, "Random seed for the generator"))
    md1.addParameter(Parameter("babayagaConfigFile", '', "string", "", "", False, False, "Babayaga steering options"))
    md1.addParameter(Parameter("debug", False, "bool", "", "", False, False, "debug mode"))
    return md1

  def _applicationModuleValues(self, moduleinstance):
    moduleinstance.setValue("babayagaConfigFile", self.babayagaConfigFile)
    moduleinstance.setValue("randomSeed", self.randomSeed)
    moduleinstance.setValue("debug", self.debug)

  def _checkWorkflowConsistency(self):
    return self._checkRequiredApp()
