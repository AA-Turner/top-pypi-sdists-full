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
"""Test TransformationFileMetadataAgent."""

from __future__ import absolute_import
import unittest
import sys
from contextlib import contextmanager
from mock import MagicMock, patch

import ILCDIRAC.ILCTransformationSystem.Agent.TransformationFileMetadataAgent as TFM
from ILCDIRAC.ILCTransformationSystem.Agent.TransformationFileMetadataAgent import TransformationFileMetadataAgent


class TestTFMAgent(unittest.TestCase):
  """Test_tfmAgent class."""

  def setUp(self):
    self.agent = TFM
    self.agent.AgentModule = MagicMock()
    self.tfmAgent = TransformationFileMetadataAgent()

  @classmethod
  def tearDownClass(cls):
    sys.modules.pop('ILCDIRAC.ILCTransformationSystem.Agent.TransformationFileMetadataAgent')

  def test_init(self):
    self.assertIsInstance(self.tfmAgent, TransformationFileMetadataAgent)



