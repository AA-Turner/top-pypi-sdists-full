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
"""Test the LFNPathUtilities."""
from __future__ import absolute_import
__RCSID__ = "$Id$"

import pytest

from ILCDIRAC.Core.Utilities.LFNPathUtilities import joinPathForMetaData, cleanUpLFNPath

LOG_PATH = "/ilc/prod/ilc/mc-dbd/ild/"
JOB_ID = 12


@pytest.mark.parametrize('paths, expectedPath',
                         [(("/ilc", "grid", "softwareVersion", "/"), "/ilc/grid/softwareVersion/"),
                          (("/ilc//grid", "/", "softwareVersion", "/"), "/ilc/grid/softwareVersion/"),
                          (("/ilc//grid", "/", "softwareVersion/", "/"), "/ilc/grid/softwareVersion/"),
                          ])
def test_joinPathForMetaData(paths, expectedPath):
  """Test for joinPathForMetaData."""
  assert joinPathForMetaData(*paths) == expectedPath


@pytest.mark.parametrize('lfn, expectedPath',
                         [('%s/%s' % (LOG_PATH, str(int(JOB_ID) // 1000).zfill(3)), '/ilc/prod/ilc/mc-dbd/ild/000'),
                          ('LFN:/some/path/to/some/where', '/some/path/to/some/where'),
                          ('lFn:/some/path/to/some/where', '/some/path/to/some/where'),
                          ])
def test_lfnCleanup(lfn, expectedPath):
  """Test for cleanUpLFNPath."""
  assert cleanUpLFNPath(lfn) == expectedPath
