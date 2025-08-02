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
"""Reports any applications errors at the end of the Workflow execution.

Depends on the 'ErrorDict' of the workflow_commons

:since: June 11, 2018
:author: A. Sailer
"""

from __future__ import absolute_import
from ILCDIRAC.Workflow.Modules.ModuleBase import ModuleBase
from DIRAC import S_OK, gLogger

__RCSID__ = '$Id$'
LOG = gLogger.getSubLogger(__name__)


class ReportErrors(ModuleBase):
  """Reports errors from applications at the end of the workflow execution."""

  def __init__(self):
    """Constructor, no arguments."""
    super(ReportErrors, self).__init__()
    self.result = S_OK()

  def execute(self):
    """Print out the errors from all applications.

    ErrorDict is filled in
    :func:`ILCDIRAC.Workflow.Modules.ModuleBase.ModuleBase.finalStatusReport`, which is called from
    all modules.
    """
    errorDict = self.workflow_commons.get('ErrorDict', {})
    if not errorDict:
      LOG.info("No errors encountered")

    for app, errorMessages in errorDict.items():
      for message in errorMessages:
        LOG.error(app, message)
    return S_OK()
