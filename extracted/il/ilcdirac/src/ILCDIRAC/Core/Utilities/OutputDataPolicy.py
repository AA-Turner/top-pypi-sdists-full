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
"""OutputDataPolicy generates the output data that will be created by a workflow task.

DIRAC assumes an execute() method will exist during usage.
"""

from __future__ import absolute_import
from DIRAC import gLogger
from DIRAC.Interfaces.API.Job import Job
from ILCDIRAC.Core.Utilities.ProductionData import constructProductionLFNs
from ILCDIRAC.Core.Utilities.resolvePathsAndNames import getProdFilenameFromInput

LOG = gLogger.getSubLogger(__name__)
__RCSID__ = "$Id$"

ILDJOBTYPES = ['MCGeneration_ILD',
                'MCSimulation_ILD',
                'MCReconstruction_ILD',
                'MCReconstruction_Overlay_ILD',
                'Split_ILD',
              ]


class OutputDataPolicy(object):
  """The OutputDataPolicy formats output file names.

  This module is called from the TransformationSystem TaskManager
  """

  def __init__(self, paramDict):
    self.paramDict = paramDict

  def execute(self):
    """Execute it."""
    jobDescription = self.paramDict['Job']
    prodID = self.paramDict['TransformationID']
    jobID = self.paramDict['TaskID']
    inputData = self.paramDict['InputData']

    job = Job(jobDescription)
    commons = job._getParameters()  # pylint: disable=protected-access
    code = job.workflow.createCode()
    outputList = []
    for line in code.split("\n"):
      if line.count("listoutput"):
        outputList += eval(line.split("#")[0].split("=")[-1])  # pylint: disable=eval-used

    commons['outputList'] = outputList
    commons['PRODUCTION_ID'] = prodID
    commons['JOB_ID'] = jobID
    if inputData:
      commons['InputData'] = inputData

    result = constructProductionLFNs(commons)
    if not result['OK']:
      LOG.error(result['Message'])
      return result

    if commons['JobType'] in ILDJOBTYPES and commons.get('InputData'):
      inputData = commons['InputData']
      inputData = inputData[0] if isinstance(inputData, list) else inputData
      for index, outputFile in enumerate(result['Value']['ProductionOutputData']):
        outputFileILD = getProdFilenameFromInput(inputData, outputFile, prodID, jobID)
        result['Value']['ProductionOutputData'][index] = outputFileILD
        LOG.debug("Changed output file name from '%s' to '%s' " % (outputFile, outputFileILD))

    return result
