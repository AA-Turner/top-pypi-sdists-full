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
"""Several file utilities.

:since: Mar 13, 2013
:author: sposs
"""

from __future__ import absolute_import
import glob
import os
import re
import shutil

from distutils import dir_util, errors  # pylint: disable=no-name-in-module

from DIRAC import S_OK, S_ERROR, gLogger

from DIRAC.DataManagementSystem.Client.DataManager import DataManager
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations

from DIRAC.RequestManagementSystem.Client.Request import Request
from DIRAC.RequestManagementSystem.Client.Operation import Operation
from DIRAC.RequestManagementSystem.Client.Operation import File
from DIRAC.RequestManagementSystem.private.RequestValidator import RequestValidator
from DIRAC.RequestManagementSystem.Client.ReqClient import ReqClient

LOG = gLogger.getSubLogger(__name__)
__RCSID__ = "$Id$"


def upload(path, appTar):
  """Upload software tar ball to storage."""
  datMan = DataManager()
  ops = Operations()
  if path[-1] != "/":
    path += "/"
  if not os.path.exists(appTar):
    LOG.error("Tar ball %s does not exists, cannot continue." % appTar)
    return S_ERROR()
  if path.find("http://www.cern.ch/lcd-data") > -1:
    final_path = "/afs/cern.ch/eng/clic/data/software/"
    try:
      shutil.copy(appTar, "%s%s" % (final_path, os.path.basename(appTar)))
    except EnvironmentError as x:
      LOG.error("Could not copy because %s" % x)
      return S_ERROR("Could not copy because %s" % x)
  elif path.find("http://") > -1:
    LOG.error("Path %s was not foreseen!" % path)
    LOG.error("Location not known, upload to location yourself, and publish in CS manually")
    return S_ERROR()
  else:
    lfnpath = "%s%s" % (path, os.path.basename(appTar))
    res = datMan.putAndRegister(lfnpath, appTar, ops.getValue('Software/BaseStorageElement', "CERN-SRM"))
    if not res['OK']:
      return res
    request = Request()
    requestClient = ReqClient()
    request.RequestName = 'copy_%s' % os.path.basename(appTar).replace(".tgz", "").replace(".tar.gz", "")
    request.SourceComponent = 'ReplicateILCSoft'
    copies_at = ops.getValue('Software/CopiesAt', [])
    for copies in copies_at:
      transfer = Operation()
      transfer.Type = "ReplicateAndRegister"
      transfer.TargetSE = copies
      trFile = File()
      trFile.LFN = lfnpath
      trFile.GUID = ""
      transfer.addFile(trFile)
      request.addOperation(transfer)

    res = RequestValidator().validate(request)
    if not res['OK']:
      return res

    if copies_at:
      res = requestClient.putRequest(request)
      if not res['OK']:
        LOG.error('Could not set replication request', res['Message'])
      return S_OK('Application uploaded')
  return S_OK()


def fullCopy(srcdir, dstdir, item):
  """Copy the item from srcdir to dstdir, creates missing directories if needed."""
  item = item.rstrip().lstrip().lstrip("./").rstrip("/")
  srcdir = srcdir.rstrip("/")
  dstdir = dstdir.rstrip("/")
  if not re.match(r"(.*)[a-zA-Z0-9]+(.*)", item):  # we want to have explicit elements
    LOG.error("You try to get all files, that cannot happen")
    return S_OK()
  src = os.path.join(srcdir, item)
  items = glob.glob(src)
  if not items:
    LOG.error("No items found matching", src)
    return S_ERROR("No items found!")

  for item in items:
    item = item.replace(srcdir, "").lstrip("/")
    dst = os.path.join(dstdir, item)

    try:
      dir_util.create_tree(dstdir, [item])
    except errors.DistutilsFileError as why:
      return S_ERROR(str(why))

    if os.path.isfile(os.path.join(srcdir, item)):
      try:
        shutil.copy2(os.path.join(srcdir, item), dst)
      except EnvironmentError as why:
        return S_ERROR(str(why))
    else:
      try:
        shutil.copytree(os.path.join(srcdir, item), dst)
      except EnvironmentError as why:
        return S_ERROR(str(why))
  return S_OK()
