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
"""Test for the SoftwareVersions Executor."""

from __future__ import absolute_import
import pytest
from mock import MagicMock, patch

from DIRAC import gLogger, S_OK


@pytest.fixture
def svExecutor(mocker):
  """Mock the SoftwareVersions executor."""
  class FakeExecutorModule(object):
    log = gLogger

    def __init__(self, *args, **kwargs):
      self.log = gLogger
      self.ex_optimizerName = lambda: "optimus prime"

    @classmethod
    def ex_getOption(cls, *args, **kwargs):
      return {'BanLists': ['1', '2'],
              '1Reason': 'BadSoftware',
              '1Sites': ['Site1', 'Site2'],
              '2Reason': 'BadVersion',
              '2Sites': ['Site2', 'Site3'],
              }[args[0]]

    def setNextOptimizer(self, *args, **kwargs):
      return S_OK()

  mocker.patch('ILCDIRAC.WorkloadManagementSystem.Executor.SoftwareVersions.OptimizerExecutor',
               new=MagicMock(spec="DIRAC.WorkloadManagementSystem.Executor.Base.OptimizerExecutor.OptimizerExecutor"))

  from ILCDIRAC.WorkloadManagementSystem.Executor import SoftwareVersions
  executorClass = SoftwareVersions.SoftwareVersions
  patchBase = patch.object(executorClass, '__bases__', (FakeExecutorModule,))
  with patchBase:
    patchBase.is_local = True
    SoftwareVersions.SoftwareVersions.initializeOptimizer()
    theExecutor = SoftwareVersions.SoftwareVersions()
    theExecutor._updateBanLists()
    theExecutor._updateBanLists = MagicMock()

  theExecutor.setNextOptimizer = MagicMock()
  return theExecutor


@pytest.fixture
def aJobState():
  """Return a jobState mock."""
  js = MagicMock(name="JobState")
  jm = MagicMock(name="JobManifest")

  def _jsOptions(*args, **kwargs):
    return {'SoftwarePackages': ['BadSoftware', 'BadVersion'],
            'BannedSites': [],
            'BannedSite': [],
            }[args[0]]
  jm.getOption = _jsOptions
  jm.setOption = MagicMock(name="setOption")

  js.getManifest.return_value = S_OK(jm)
  js.JM = jm  # for fast access
  return js


def test_optimizeJob(svExecutor, aJobState):
  """Test the optimizeJob function."""
  gLogger.setLevel('DEBUG')
  assert 'BadSoftware' in svExecutor._SoftwareVersions__softToBanned
  res = svExecutor.optimizeJob(1234, aJobState)
  assert res['OK']
  aJobState.JM.setOption.assert_called_with('BannedSites', 'Site1, Site2, Site3')
