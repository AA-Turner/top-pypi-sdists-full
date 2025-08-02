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
"""Bhlumi Application to run applications based on Bhlumi.

.. versionadded:: v34r0

Usage:

>>> bhlumi = Bhlumi()
>>> bhlumi.setVersion('key4hep-latest')
>>> bhlumi.setRandomSeed(12340)
>>> bhlumi.setEnergy(91.2)
>>> bhlumi.setNumberOfEvents(100)
>>> bhlumi.setOutputFile('output.lhe')

"""

from __future__ import absolute_import
import os

from ILCDIRAC.Interfaces.API.NewInterface.LCApplication import LCApplication
from DIRAC import S_OK, S_ERROR, gLogger
from DIRAC.Core.Workflow.Parameter import Parameter
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations

LOG = gLogger.getSubLogger(__name__)
__RCSID__ = "$Id$"

class Bhlumi(LCApplication):
  """Bhlumi Application Class."""
  def __init__(self, paramdict=None):
    self.randomSeed = -1
    self.debugLevel = 0
    self.bhlumiConfigFile = ''
    super(Bhlumi, self).__init__(paramdict)

    # Those 5 need to come after default constructor
    self._modulename = 'BhlumiAnalysis'
    self._moduledescription = 'Module to run Bhlumi'
    self.appname = 'bhlumi'
    self.datatype = 'GEN'
    self._ops = Operations()
    self._extension = 'lhe'

  def setConfigFile(self, bhlumiConfigFilePath):
    """Set the Bhlumi options to be used.

    :param str bhlumiConfigFilePath: Path to the Bhlumi input file.
    """
    self._checkArgs({'bhlumiConfigFilePath': (str,)})

    # Chech if file exist
    if not os.path.isfile(bhlumiConfigFilePath):
      return self._reportError('Bhlumi config file does not exist!')

    # Read file
    self.bhlumiConfigFile = open(bhlumiConfigFilePath).read()

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

    Alternative to :func:`Bhlumi.setExtraCLIArguments`.

    :param str args: Arguments to pass to the command call
    """
    self._checkArgs({'args': (str,)})
    self.extraCLIArguments = args
    return S_OK()
  
  def setBhlumiConfigFile(self, bhlumiConfigFilePath):
    """Set the bhlumi configuration file.

    :param str bhlumiConfigFilePath: Name of the Bhlumi configuration file path.
    """
    self._checkArgs({'bhlumiConfigFilePath': (str,)})
    if not os.path.isfile(bhlumiConfigFilePath):
      return self._reportError('Bhlumi configuration file does not exist!')
    self.bhlumiConfigFileContent = open(bhlumiConfigFilePath).read()
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
    """Check consistency of the Bhlumi application, this is called from the `Job` instance.

    :param job: The instance of the job
    :type job: ~ILCDIRAC.Interfaces.API.NewInterface.Job.Job
    :returns: S_OK/S_ERROR
    """

    if not self.version:
      return S_ERROR('No version found!')

    if self.bhlumiConfigFile:
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
    md1.addParameter(Parameter("bhlumiConfigFile", '', "string", "", "", False, False, "Bhlumi steering options"))
    md1.addParameter(Parameter("debug", False, "bool", "", "", False, False, "debug mode"))
    return md1

  def _applicationModuleValues(self, moduleinstance):
    moduleinstance.setValue("bhlumiConfigFile", self.bhlumiConfigFile)
    moduleinstance.setValue("randomSeed", self.randomSeed)
    moduleinstance.setValue("debug", self.debug)

  def _checkWorkflowConsistency(self):
    return self._checkRequiredApp()
