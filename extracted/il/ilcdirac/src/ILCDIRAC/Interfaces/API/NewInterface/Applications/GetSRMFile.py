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
"""Download files directly from an SRM.

Use this to download files not available in the DiracFileCatalog
"""
from __future__ import absolute_import
from ILCDIRAC.Interfaces.API.NewInterface.LCUtilityApplication import LCUtilityApplication
from DIRAC import S_OK, S_ERROR, gLogger
from DIRAC.Core.Workflow.Parameter import Parameter

LOG = gLogger.getSubLogger(__name__)
__RCSID__ = "$Id$"


class GetSRMFile(LCUtilityApplication):
  """Gets a given file from storage directly using srm path.

  Usage:

  >>> gf = GetSRMFile()
  >>> fdict = {"file" : "srm://srm-public.cern.ch/castor/cern.ch/grid/ilc/prod/clic/1tev/Z_uds/gen/0/nobeam_nobrem_0-200.stdhep","site":"CERN-SRM"}
  >>> gf.setFiles(fdict)
  """

  def __init__(self, paramdict=None):
    self.files = {}
    super(GetSRMFile, self).__init__(paramdict)
    self._modulename = "GetSRMFile"
    self.appname = self._modulename
    self._moduledescription = "Module to get files directly from Storage"

  def setFiles(self, fdict):
    """Specify the files you need.

    :param fdict: file dictionary: {'file':'site'}, can be also [{},{}] etc.
    :type fdict: :class:`python:dict`, or :any:`python:list` of :class:`python:dict`
    """
    kwargs = {"fdict": fdict}
    if not isinstance(fdict, (dict, list)):
      return self._reportError('Expected dict or list of dicts for fdict', __name__, **kwargs)

    self.files = fdict

  def _applicationModule(self):
    m1 = self._createModuleDefinition()
    m1.addParameter(Parameter("srmfiles", [], "list", "", "", False, False, "list of files to retrieve"))
    m1.addParameter(Parameter("debug", False, "bool", "", "", False, False, "debug mode"))
    return m1

  def _applicationModuleValues(self, moduleinstance):
    moduleinstance.setValue("srmfiles", self.files)
    moduleinstance.setValue("debug", self.debug)

  def _userjobmodules(self, stepdefinition):
    res1 = self._setApplicationModuleAndParameters(stepdefinition)
    if not res1["OK"]:
      return S_ERROR("userjobmodules method failed")
    return S_OK()

  def _prodjobmodules(self, step):
    LOG.error("This application is not meant to be used in Production context")
    return S_ERROR('Should not use in Production')

  def _checkConsistency(self, job=None):

    if not self.files:
      return S_ERROR("The file list was not defined")

    if isinstance(self.files, dict):
      self.files = [self.files]

    # For the getInputFromApp to work, we nedd to tell the application about the expected OutputFile
    flist = ''
    for fdict in self.files:
      filePath = fdict['file']
      bname = filePath.split("/")[-1]
      flist += bname + ";"

    self.setOutputFile(flist.rstrip(";"))

    return S_OK()

  def _addParametersToStep(self, step):
    res = self._addBaseParameters(step)
    if not res["OK"]:
      return S_ERROR("Failed to set base parameters")
    return S_OK()
