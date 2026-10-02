#!/usr/env python
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

"""Make a RemovalRequest for the new System."""
from __future__ import print_function
from __future__ import absolute_import
__RCSID__ = "$Id$"

from DIRAC.Core.Base.Script import Script
Script.parseCommandLine()

from DIRAC.RequestManagementSystem.Client.Request import Request

from DIRAC.RequestManagementSystem.Client.File import File
from DIRAC.RequestManagementSystem.Client.Operation import Operation
from DIRAC.RequestManagementSystem.private.RequestValidator import RequestValidator
from DIRAC.RequestManagementSystem.Client.ReqClient import ReqClient


def myRequest():
  """Create a request and put it to the db."""

  request = Request()
  request.RequestName = 'myAwesomeRemovalRequest.xml'
  request.JobID = 0
  request.SourceComponent = "myScript"

  remove = Operation()
  remove.Type = "RemoveFile"

  lfn = "/ilc/user/s/sailer/test.txt"
  rmFile = File()
  rmFile.LFN = lfn
  remove.addFile(rmFile)

  request.addOperation(remove)
  isValid = RequestValidator().validate(request)
  if not isValid['OK']:
    raise RuntimeError("Failover request is not valid: %s" % isValid['Message'])
  else:
    print("It is a GOGOGO")
    requestClient = ReqClient()
    result = requestClient.putRequest(request)
    print(result)


if __name__ == "__main__":
  myRequest()
