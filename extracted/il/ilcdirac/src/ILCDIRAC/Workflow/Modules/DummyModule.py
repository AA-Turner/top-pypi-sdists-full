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
"""Dummy module that prints out the workflow parameters.

:since: Mar 11, 2011

:author: sposs
"""

from __future__ import absolute_import
from ILCDIRAC.Workflow.Modules.ModuleBase import ModuleBase
from DIRAC import S_OK, S_ERROR, gLogger

__RCSID__ = '$Id$'
LOG = gLogger.getSubLogger(__name__)


class DummyModule(ModuleBase):
  """Dummy module used to check Workflow Parameters (Parametric jobs check)"""

  def __init__(self):
    super(DummyModule, self).__init__()
    self.result = S_ERROR()

  def applicationSpecificInputs(self):
    """Resolve the parameters."""

    for key, val in self.workflow_commons.items():
      LOG.info("%s=%s" % (key, val))

    for key, val in self.step_commons.items():
      LOG.info("%s=%s" % (key, val))
    return S_OK()

  def execute(self):
    """Not much to do..."""
    self.result = self.resolveInputVariables()
    return S_OK()
