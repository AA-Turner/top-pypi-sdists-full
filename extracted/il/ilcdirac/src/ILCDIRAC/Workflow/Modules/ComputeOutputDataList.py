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
"""Compute the outputdata list for production jobs.

:since:  Jun 30, 2010

:author: sposs
"""

from __future__ import absolute_import
from ILCDIRAC.Workflow.Modules.ModuleBase import ModuleBase

from DIRAC import gLogger, S_OK

__RCSID__ = '$Id$'
LOG = gLogger.getSubLogger(__name__)


class ComputeOutputDataList(ModuleBase):
  """In case the previous module executed properly, add the output to the listoutput.

  This is used in the prduction context to ensure only the files coming from successful applications
  are added to the output list. Otherwise, there is a risk to register corrupted files.
  """

  def __init__(self):
    """Module initialization."""
    super(ComputeOutputDataList, self).__init__()
    self.version = __RCSID__
    self.listoutput = []

  def applicationSpecificInputs(self):
    """Update the workflow_commons dictionary with the current step's output."""
    if 'listoutput' in self.step_commons:
      self.listoutput = self.step_commons['listoutput']

    if 'outputList' in self.workflow_commons:
      self.workflow_commons['outputList'] = self.workflow_commons['outputList'] + self.listoutput
    else:
      self.workflow_commons['outputList'] = self.listoutput

    return S_OK()

  def execute(self):
    """Not much to do..."""
    res = self.resolveInputVariables()
    if not res['OK']:
      LOG.error("Failed to resolve input variables:", res['Message'])
      return res
    return S_OK()
