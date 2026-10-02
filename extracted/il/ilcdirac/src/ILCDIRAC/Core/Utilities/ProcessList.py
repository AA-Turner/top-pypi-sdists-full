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
"""Interface to the processlist.whiz that contains all the processes known to WHIZARD.

:author: S. Poss
:since: Sep 21, 2010
"""

from __future__ import absolute_import
__RCSID__ = "$Id$"

from DIRAC import S_OK, S_ERROR, gLogger
from diraccfg import CFG
from pprint import pprint
import os
import tempfile
import shutil
import subprocess

LOG = gLogger.getSubLogger(__name__)


class ProcessList(object):
  """The ProcessList uses internally the CFG utility to store the processes and their properties."""

  def __init__(self, location):
    self.cfg = CFG()
    self.location = location
    self.goodProcessList = True
    if os.path.exists(self.location):
      self.cfg.loadFromFile(self.location)
      if not self.cfg.existsKey('Processes'):
        self.cfg.createNewSection('Processes')
    else:
      self.goodProcessList = False

  def _writeProcessList(self, path):
    """Write to text."""
    handle, tmpName = tempfile.mkstemp()
    written = self.cfg.writeToFile(tmpName)
    os.close(handle)
    if not written:
      if os.path.exists(tmpName):
        os.remove(tmpName)
      return written
    if os.path.exists(path):
      LOG.debug("Replacing %s" % path)
    try:
      shutil.move(tmpName, path)
      return True
    except OSError as err:
      LOG.error("Failed to overwrite process list.", err)
      LOG.info("If your process list is corrupted a backup can be found %s" % tmpName)
      return False

  def isOK(self):
    """Check if the content is OK."""
    return self.goodProcessList

  def updateProcessList(self, processes):
    """Adds a new entry or updates an existing one.

    :param dict processes: dictionary of processes to treat
    """
    LOG.verbose("Updating process list:")
    for process, mydict in processes.items():
      if not self._existsProcess(process):
        self._addEntry(process, mydict)
        # return res
      else:
        LOG.warn("Process %s already defined in ProcessList, will replace it" % process)
        self.cfg.deleteKey("Processes/%s" % process)
        self._addEntry(process, mydict)
        # return res
    LOG.verbose("Done Updating process list")
    return S_OK()

  def _addEntry(self, process, processdic):
    """Adds a new entry."""
    if not self.cfg.isSection("Processes/%s" % process):
      self.cfg.createNewSection("Processes/%s" % process)
    self.cfg.setOption("Processes/%s/TarBallCSPath" % process, processdic['TarBallCSPath'])
    self.cfg.setOption("Processes/%s/Detail" % process, processdic['Detail'])
    self.cfg.setOption("Processes/%s/Generator" % process, processdic['Generator'])
    self.cfg.setOption("Processes/%s/Model" % process, processdic['Model'])
    self.cfg.setOption("Processes/%s/Restrictions" % process, processdic['Restrictions'])
    self.cfg.setOption("Processes/%s/InFile" % process, processdic['InFile'])
    cross_section = 0
    if 'CrossSection' in processdic:
      cross_section = processdic["CrossSection"]
    self.cfg.setOption("Processes/%s/CrossSection" % process, cross_section)
    return S_OK()

  def getCSPath(self, process):
    """Return the path to the TarBall (for install)

    :param str process: process to look for
    """
    return self.cfg.getOption("Processes/%s/TarBallCSPath" % process, None)

  def getInFile(self, process):
    """Get the associated whizard.in file to the process."""
    return self.cfg.getOption("Processes/%s/InFile" % process, None)

  def getProcesses(self):
    """Return the list of all processes available."""
    processesdict = self.cfg.getAsDict("Processes")
    processes = list(processesdict.keys())
    return processes

  def getProcessesDict(self):
    """Return all processes as a dictionary {'process':{'TarBall':Path, etc.

    etc.}}
    """
    return self.cfg.getAsDict("Processes")

  def existsProcess(self, process):
    """Check if the specified process exists."""
    return S_OK(self._existsProcess(process))

  def _existsProcess(self, process):
    """Check that the process exists."""
    return self.cfg.isSection('Processes/%s' % process)

  def writeProcessList(self, alternativePath=None):
    """Write the process list."""
    destination = self.location
    if alternativePath:
      destination = alternativePath
    written = self._writeProcessList(destination)
    if not written:
      return S_ERROR("Failed to write repository")
    return S_OK(destination)

  def printProcesses(self):
    """Dump to screen the content of the process list."""
    processesdict = self.cfg.getAsDict("Processes")
    pprint(processesdict)

  def uploadProcessListToFileCatalog(self, path_to_process_list, appVersion):
    """Upload the new processList to the FileCatalog."""
    from ILCDIRAC.Core.Utilities.FileUtils import upload
    from DIRAC.DataManagementSystem.Client.DataManager import DataManager
    from DIRAC import gConfig, exit as dexit

    datMan = DataManager()
    LOG.notice("Removing process list from file catalog" + path_to_process_list)
    res = datMan.removeFile(path_to_process_list)
    if not res['OK']:
      LOG.error("Could not remove process list from file catalog, do it by hand")
      dexit(2)
    LOG.notice("Done removing process list from file catalog")

    res = upload(os.path.dirname(path_to_process_list) + "/", self.location)
    if not res['OK']:
      LOG.error("something went wrong in the copy")
      dexit(2)

    LOG.notice("Putting process list to local processlist directory")
    localprocesslistpath = gConfig.getOption("/LocalSite/ProcessListPath", "")
    if localprocesslistpath['Value']:

      try:
        localSvnRepo = "/afs/cern.ch/eng/clic/software/whizard/whizard_195/"
        # because it does not make a difference if we hardcode it here or in
        # ${DIRAC}/etc/dirac.cfg, yours truly APS, JFS
        shutil.copy(self.location, localSvnRepo)
      except OSError as err:
        LOG.error("Copy of process list to %s failed with error %s!" % (localSvnRepo, str(err)))

      try:
        subprocess.call(["svn", "ci", os.path.join(localSvnRepo, os.path.basename(
            localprocesslistpath['Value'])), "-m'Process list for whizard version %s'" % appVersion], shell=False)
      except OSError as err:
        LOG.error("Commit failed! Error: %s" % str(err))

      try:
        shutil.copy(self.location, localprocesslistpath['Value'])
      except OSError:
        LOG.error("Copy of process list to %s failed!" % localprocesslistpath['Value'])

    LOG.notice("Done")
