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
"""Unit tests for the CalibrationClient."""

from __future__ import absolute_import
import pytest
from mock import MagicMock as Mock
from DIRAC import S_OK
from ILCDIRAC.CalibrationSystem.Client.CalibrationClient import CalibrationClient

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.CalibrationSystem.Client.CalibrationClient'


@pytest.fixture
def calibClient():
  """Create calibration handler."""
  calibClient = CalibrationClient(1, 1)
  return calibClient


def test_getInputDataDict(mocker):
  """Test getInputDataDict."""
  #  mocker.patch('%s.Client' % MODULE_NAME, new=Mock(return_value=True))
  from DIRAC.Core.Base.Client import Client
  mocker.patch.object(Client, '__init__', new=Mock(return_value=True))

  calibClientWithInputArguments = CalibrationClient(1, 1)

  tmpMock = Mock(name='instance')
  tmpMock.getInputDataDict.return_value = S_OK()
  mocker.patch.object(calibClientWithInputArguments, '_getRPC', return_value=tmpMock)

  res = calibClientWithInputArguments .getInputDataDict()
  assert res['OK']

  calibClientWoInputArguments = CalibrationClient()
  mocker.patch.object(calibClientWoInputArguments, '_getRPC', return_value=tmpMock)

  res = calibClientWoInputArguments .getInputDataDict(1, 1)
  assert res['OK']
