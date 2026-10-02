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
"""
:synopsis: RequestOperation to handle log file failover

Uploads log files to the LogSE that were uploaded to a GridSE as a failover
mechanism. Removes log files from the GridSE

Adapted from LHCbDirac.

"""

from __future__ import absolute_import
import os

from DIRAC import S_OK, S_ERROR
from DIRAC.RequestManagementSystem.private.OperationHandlerBase import OperationHandlerBase

__RCSID__ = "$Id$"


class LogUpload(OperationHandlerBase):
  """LogUpload operation handler."""

  def __init__(self, operation=None, csPath=None):
    """c'tor.

    :param self: self reference
    :param Operation operation: Operation instance
    :param str csPath: CS path for this handler
    """
    # # base class ctor
    OperationHandlerBase.__init__(self, operation, csPath)
    self.workDirectory = os.environ.get('LOGUPLOAD_CACHE', os.environ.get('AGENT_WORKDIRECTORY', '/tmp/LogUpload'))

  def __call__(self):
    """LogUpload operation processing."""
    # # list of targetSEs

    targetSEs = self.operation.targetSEList

    if len(targetSEs) != 1:
      self.log.error("wrong value for TargetSE list = %s, should contain only one target!" % targetSEs)
      self.operation.Error = "Wrong parameters: TargetSE should contain only one targetSE"
      for opFile in self.operation:

        opFile.Status = "Failed"
        opFile.Error = "Wrong parameters: TargetSE should contain only one targetSE"


      return S_ERROR("TargetSE should contain only one target, got %s" % targetSEs)

    targetSE = targetSEs[0]
    targetWrite = self.rssSEStatus(targetSE, "WriteAccess")
    if not targetWrite["OK"]:
      self.log.error(targetWrite["Message"])
      for opFile in self.operation:
        opFile.Status = "Failed"
        opFile.Error = "Wrong parameters: %s" % targetWrite["Message"]
      self.operation.Error = targetWrite["Message"]
      return S_OK()

    if not targetWrite["Value"]:
      self.operation.Error = "TargetSE %s is banned for writing"
      return S_ERROR(self.operation.Error)

    # # get waiting files
    waitingFiles = self.getWaitingFilesList()

    # # loop over files
    for opFile in waitingFiles:
      # # get LFN
      lfn = opFile.LFN
      self.log.info("processing file %s" % lfn)

      destinationFolder = '/'.join(lfn.split('/')[0:-1])
      destinationSubFolder = "%03d" % (int((os.path.basename(lfn)).split('_')[1].split('.')[0]) // 1000)
      destination = destinationFolder + '/' + destinationSubFolder

      logUpload = self.dm.replicate(lfn, targetSE, destPath=destination, localCache=self.workDirectory)
      if not logUpload["OK"]:
#         self.dataLoggingClient().addFileRecord( lfn, "LogUploadFail", targetSE, "", "LogUpload" )
        self.log.error("completely failed to upload log file: %s" % logUpload["Message"])
        opFile.Error = str(logUpload["Message"])
        opFile.Attempt += 1
        self.operation.Error = opFile.Error
        if 'No such file or directory' in opFile.Error:
          opFile.Status = 'Failed'
        continue

      if lfn in logUpload['Value']:
#         self.dataLoggingClient().addFileRecord( lfn, "LogUpload", targetSE, "", "LogUpload" )
        opFile.Status = 'Done'
        self.log.info("Uploaded %s to %s" % (lfn, targetSE))

    return S_OK()

  def setOperation(self, operation):  # pylint: disable=useless-super-delegation
    """operation and request setter.

    :param ~DIRAC.RequestManagementSystem.Client.Operation.Operation operation: operation instance
    :raises TypeError: if ``operation`` in not an instance of :class:`~DIRAC.RequestManagementSystem.Client.Operation.Operation`
    """
    super(LogUpload, self).setOperation(operation)
