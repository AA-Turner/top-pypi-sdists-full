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
"""The job path resolution module is a VO-specific plugin that allows to define VO job policy in a simple way.  This allows the inclusion of ILC specific WMS optimizers without compromising the generic nature of DIRAC.

The arguments dictionary from the JobPathAgent includes the ClassAd
job description and therefore decisions are made based on the existence
of JDL parameters.
:author: Stuart Paterson
"""

from __future__ import absolute_import
__RCSID__ = "$Id$"

from DIRAC import S_OK, S_ERROR, gLogger

LOG = gLogger.getSubLogger(__name__)
COMPONENT_NAME = 'ILCJobPathResolution'


class JobPathResolution(object):
  """VO Specific plugin for jobpath resolution."""
  #############################################################################

  def __init__(self, argumentsDict):
    """Standard constructor."""
    self.arguments = argumentsDict
    self.name = COMPONENT_NAME

  #############################################################################
  def execute(self):
    """Given the arguments from the JobPathAgent, this function resolves job optimizer paths according to ILC VO policy."""
    ilcPath = ''

    if 'ConfigPath' not in self.arguments:
      LOG.warn('No CS ConfigPath defined')
      return S_ERROR('JobPathResoulution Failure')

    LOG.verbose('Attempting to resolve job path for ILC')
    job = self.arguments['JobID']
    classadJob = self.arguments['ClassAd']

    inputData = classadJob.get_expression('InputData').replace('"', '').replace('Unknown', '')
    if inputData:
      LOG.info('Job %s has input data requirement' % (job))
      ilcPath += 'InputData'

    if not ilcPath:
      LOG.info('No ILC specific optimizers to be added')

    return S_OK(ilcPath)

#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#
