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
"""Goes with DBDGeneration, not used.

:since: Jan 26, 2012

:author: Stephane Poss
"""

from __future__ import absolute_import
from ILCDIRAC.Workflow.Modules.ModuleBase import ModuleBase

from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

from DIRAC import S_OK, gLogger

__RCSID__ = '$Id$'
LOG = gLogger.getSubLogger(__name__)


class DBDGenRegisterOutputData(ModuleBase):
  """Normally, was supposed to be used to produce the DBD gen level files.

  Dropped in the end.
  """

  def __init__(self):
    super(DBDGenRegisterOutputData).__init__()
    self.version = "DBDGenRegisterOutputData v1"
    self.commandTimeOut = 10 * 60
    self.enable = True
    self.fcc = FileCatalogClient()
    self.nbofevents = 0
    self.prodOutputLFNs = []

  def applicationSpecificInputs(self):
    if 'ProductionOutputData' in self.workflow_commons:
      self.prodOutputLFNs = self.workflow_commons['ProductionOutputData'].split(";")

    if 'NbOfEvts' in self.workflow_commons:
      self.nbofevents = self.workflow_commons['NbOfEvts']
    return S_OK("Parameters resolved")

  def execute(self):
    LOG.info('Initializing %s' % self.version)
    result = self.resolveInputVariables()
    if not result['OK']:
      LOG.error(result['Message'])
      return result

    if not self.workflowStatus['OK'] or not self.stepStatus['OK']:
      LOG.verbose('Workflow status = %s, step status = %s' % (self.workflowStatus['OK'], self.stepStatus['OK']))
      return S_OK('No registration of output data metadata attempted')

    if not len(self.prodOutputLFNs):
      LOG.info('No production data found, so no metadata registration to be done')
      return S_OK("No files' metadata to be registered")

    LOG.verbose("Will try to set the metadata for the following files: \n %s" % '\n'.join(self.prodOutputLFNs))

    for files in self.prodOutputLFNs:
      metadict = {}
      metadict['NumberOfEvents'] = self.nbofevents
      path = files

      res = self.fcc.setMetadata(files, metadict)
      if not res['OK']:
        LOG.error("Could not register %s for %s" % (metadict, path))
        return res

    return S_OK()
