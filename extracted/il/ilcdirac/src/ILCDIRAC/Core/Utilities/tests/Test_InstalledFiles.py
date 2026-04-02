#!/usr/bin/env python
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
"""Test the InstalledFiles Module."""

import os
import pytest
import unittest

from mock import patch, MagicMock as Mock

from Tests.Utilities.OperationsMock import opsMockTemplate
from ILCDIRAC.Core.Utilities.InstalledFiles import Exists, _checkInCVMFS

@pytest.fixture
def opsMock():
  theOpsMock = opsMockTemplate(getValueDict={"/cvmfs/CVMFSPath": "/foo",
                                             "/TarBallURL": "/tar/ball/url",
                                             "/yes/TarBall": "yes.tgz",
                                             "/no/TarBall": "no.tgz",
                                             },
                               getOptionsDict={})
  return theOpsMock


EXISTS_PAR = [(False, {"file": "f.py", "platform": "el9", "cv": "lhcConfigcvmfs", "M": "Cannot find file on cvmfs"}),
              (True, {"file": "t.py", "platform": "el9", "cv": "lhcConfigcvmfs"}),
              ]
@pytest.mark.parametrize("success, par", EXISTS_PAR)
def test_Exists_wCVMFS(success, par, opsMock, mocker):
  """Tests assuming we have CVMFS on the machine"""
  exists_dict = {"/cvmfs": True,
                 "/foo/t.py": True,
                 "/foo/f.py": False,
                 }

  mocker.patch("ILCDIRAC.Core.Utilities.InstalledFiles.Operations", new=Mock(return_value=opsMock))
  mocker.patch("ILCDIRAC.Core.Utilities.InstalledFiles.os.path.exists", new=Mock(side_effect=lambda path: exists_dict[path]))

  result = Exists(par.get("file"), par.get("platform"), par.get("cv"))
  assert result["OK"] == success
  if not success:
    assert par.get("M") in  result["Message"]


EXISTS_PAR = [(True, {"file": "f.py", "platform": "el9", "cv": "lhcConfigcvmfs"}),
              ]
@pytest.mark.parametrize("success, par", EXISTS_PAR)
def test_Exists_woCVMFS(success, par, opsMock, mocker):
  """Tests that we do not have CVMFS on the machine"""
  exists_dict = {"/cvmfs": False}
  mocker.patch("ILCDIRAC.Core.Utilities.InstalledFiles.Operations", new=Mock(return_value=opsMock))
  mocker.patch("ILCDIRAC.Core.Utilities.InstalledFiles.os.path.exists", new=Mock(side_effect=lambda path: exists_dict[path]))
  result = Exists(par.get("file"), par.get("platform"), par.get("cv"))
  assert result["OK"] == success
  if not success:
    assert par.get("M") in  result["Message"]


EXISTS_PAR = [(True, {"file": "cld_steer.py"}),
               (False, {"file": "no_steer.py", "M": "is not available"}),
              ]
@pytest.mark.parametrize("success, par", EXISTS_PAR)
def test_Exists_fromList(success, par, opsMock, mocker):
  """Test when the file is in the list or not, and we do not have CVMFSPath defined"""
  mocker.patch("ILCDIRAC.Core.Utilities.InstalledFiles.Operations", new=Mock(return_value=opsMock))

  result = Exists(par.get("file"), par.get("platform"), par.get("cv"))
  assert result["OK"] == success
  if not success:
    assert par.get("M") in  result["Message"]


EXISTS_PAR = [
  (True, {"file": "t.py", "platform": "el9", "cv": "lhcConfigyes", "M": "Cannot find file on cvmfs"}),
  (False, {"file": "f.py", "platform": "el9", "cv": "lhcConfigyes", "M": "in the specified config tarball"}),
  (True, {"file": "t.py", "platform": "el9", "cv": "lhcConfigno", "getFile": True, "extract": True}),
  (False, {"file": "f.py", "platform": "el9", "cv": "lhcConfigno", "getFile": True, "extract": True, "M": "in the specified config tarball"}),
  (False, {"file": "t.py", "platform": "el9", "cv": "lhcConfigno", "getFile": True, "extract": False, "M": "Failed to extract"}),
  (False, {"file": "t.py", "platform": "el9", "cv": "lhcConfigno", "getFile": False, "extract": True, "M": "Failed to getFile"}),
]
@pytest.mark.parametrize("success, par", EXISTS_PAR)
def test_Exists_fromTarball(success, par, opsMock, mocker):
  """Test when the file we have tarball URL for the config defined"""
  exists_dict = {"tmp_config_checks/yes/t.py": True,
                 "tmp_config_checks/yes/f.py": False,
                 "tmp_config_checks/yes.tgz": True,
                 "tmp_config_checks/no.tgz": False,
                 "tmp_config_checks/no/t.py": True,
                 "tmp_config_checks/no/f.py": False,
                 "/cvmfs": False,
                 }

  DMops = Mock(name="DataManager")
  DMops.getFile.return_value = {"OK": par.get("getFile"), "Message": "Failed to getFile"}
  mocker.patch("ILCDIRAC.Core.Utilities.InstalledFiles.os.path.exists", new=Mock(side_effect=lambda path: exists_dict[path]))
  mocker.patch("ILCDIRAC.Core.Utilities.InstalledFiles.Operations", new=Mock(return_value=opsMock))
  mocker.patch("ILCDIRAC.Core.Utilities.InstalledFiles.DataManager", new=Mock(return_value=DMops))
  mocker.patch("ILCDIRAC.Core.Utilities.InstalledFiles.extractTarball", new=Mock(return_value={"OK": par.get("extract"), "Message": "Failed to extract"}))
  result = Exists(par.get("file"), par.get("platform"), par.get("cv"))
  assert result["OK"] == success
  if not success:
    assert par.get("M") in  result["Message"]
