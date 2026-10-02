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
"""Tests the ReportErrors WorkflowModule."""

from __future__ import absolute_import
import unittest
from collections import defaultdict
from mock import MagicMock as Mock, call, patch

from ILCDIRAC.Workflow.Modules.ReportErrors import ReportErrors
from Tests.Utilities.GeneralUtils import MatchStringWith

__RCSID__ = "$Id$"
MODULE_NAME = 'ILCDIRAC.Workflow.Modules.ReportErrors'


class TestReportErrors(unittest.TestCase):
  """Test ReportErrors."""

  def setUp(self):
    """Set up the tests."""
    self.log = Mock()
    self.log.info = Mock(name="LogInfo")
    self.log.error = Mock(name="LogError")

    self.patches = [patch('%s.LOG' % MODULE_NAME, new=self.log)]

    for patcher in self.patches:
      patcher.start()

    self.repErr = ReportErrors()
    self.repErr.workflow_commons = {}

  def tearDown(self):
    """Clean up test resources."""
    for patcher in self.patches:
      patcher.stop()

  def test_execute(self):
    """Test the execute function."""
    res = self.repErr.execute()
    self.assertTrue(res['OK'])
    self.log.info.assert_called_with(MatchStringWith('No errors encountered'))

    errorKey = "%s_%s" % ('appname', 'appver')
    message = 'something really bad'
    stdError = 'Segmentation Violation'
    self.repErr.workflow_commons.setdefault('ErrorDict', defaultdict(list))[errorKey].extend([message, stdError])

    res = self.repErr.execute()

    self.assertTrue(res['OK'])
    calls = [call(errorKey, 'something really bad'),
             call(errorKey, 'Segmentation Violation')]
    self.log.error.assert_has_calls(calls, any_order=True)
