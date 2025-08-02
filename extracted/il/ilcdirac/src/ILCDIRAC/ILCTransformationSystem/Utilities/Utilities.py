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
"""Holding helper objects or functions to create transformations."""
from __future__ import absolute_import
from pprint import pformat

from DIRAC import gLogger

LOG = gLogger.getSubLogger(__name__)


class Task(object):
  """Object holding all information for a task."""

  def __init__(self, metaInput, parameterDict, eventsPerJob,
               metaPrev=None, nbTasks=None, genFile=None, secondGenFile=None, eventsPerBaseFile=None,
               applicationOptions=None, datatype=None, generator=None,
               taskName='',
               ):
    """Initialise task with all the information we need to create a transformation."""
    LOG.notice('Creating task with meta', str(metaInput))
    self.meta = dict(metaInput)
    self.parameterDict = dict(parameterDict)
    self.eventsPerJob = eventsPerJob
    self.metaPrev = dict(metaPrev) if metaPrev else {}
    self.nbTasks = nbTasks
    self.genFile = genFile
    self.secondGenFile = secondGenFile
    self.eventsPerBaseFile = eventsPerBaseFile
    self.applicationOptions = dict(applicationOptions) if applicationOptions is not None else {}
    self.cliReco = ''
    self.taskName = taskName
    self.sourceName = ''
    self._updateMeta(self.meta)
    self.datatype = datatype
    self.generator = generator

  def __str__(self):
    """Return string representation of Task."""
    return pformat(vars(self))

  def __repr__(self):
    """Return string representation of Task."""
    return pformat(vars(self), width=150, indent=10)

  def _updateMeta(self, metaDict):
    """Ensure the meta dict contains the correct NumberOfEvents."""
    if self.eventsPerJob is not None:
      metaDict['NumberOfEvents'] = self.eventsPerJob
    if self.eventsPerBaseFile:
      metaDict['NumberOfEvents'] = self.eventsPerBaseFile

  def getProdName(self, *args):
    """Create the production name."""
    workflowName = '_'.join([self.parameterDict['process'],
                             self.meta['Energy'],
                             '_'.join(args),
                             self.sourceName,
                             self.taskName,
                             ]).strip('_')
    while '__' in workflowName:
      workflowName = workflowName.replace('__', '_')
    return workflowName
