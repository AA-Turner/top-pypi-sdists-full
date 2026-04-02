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
"""Tests for ProductionData."""
from __future__ import absolute_import
import unittest

from mock import patch, MagicMock as Mock
from DIRAC import S_OK, S_ERROR
from ILCDIRAC.Core.Utilities.ProductionData import constructUserLFNs, getExperimentFromPath
from Tests.Utilities.GeneralUtils import assertDiracSucceedsWith, assertDiracSucceedsWith_equals

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Core.Utilities.ProductionData'


class TestProductionData(unittest.TestCase):
  """Tests constructUserLFNs."""

  # Rest of class is covered by other tests

  def test_construct_user_lfns(self):
    today_mock = Mock()
    today_mock.timetuple.return_value = [1999, 27]
    date_mock = Mock()
    date_mock.today.return_value = today_mock
    with patch('%s.datetime.date' % MODULE_NAME, new=date_mock), \
         patch('%s.Operations.getValue' % MODULE_NAME, new=Mock(return_value='testpre')):
      result = constructUserLFNs(1234567, 'mytestVO', 'mytestowner',
                                  ['myTestOutputFile1.txt', 'myTestOutputFile2.ppt'],
                                  '/mydir/dir//MyTestOutputPath1')
      assertDiracSucceedsWith(
          result, '/mytestVO/testpre/m/mytestowner/mydir/dir/MyTestOutputPath1/myTestOutputFile1.txt', self)
      assertDiracSucceedsWith(
          result, '/mytestVO/testpre/m/mytestowner/mydir/dir/MyTestOutputPath1/myTestOutputFile2.ppt', self)

  def test_construct_user_lfns_getvo_fails(self):
    today_mock = Mock()
    today_mock.timetuple.return_value = [1999, 27]
    date_mock = Mock()
    date_mock.today.return_value = today_mock
    with patch('%s.datetime.date' % MODULE_NAME, new=date_mock), \
         patch('%s.Operations.getValue' % MODULE_NAME, new=Mock(return_value='testpre')), \
         patch('%s.getVOfromProxyGroup' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_err'))), \
         patch('%s.gLogger.error' % MODULE_NAME) as log_mock:
      result = constructUserLFNs(1234567, None, 'mytestowner',
                                  ['myTestOutputFile1.txt', 'myTestOutputFile2.ppt'],
                                  '/mydir/dir//MyTestOutputPath1')
      assertDiracSucceedsWith(
          result, '/ilc/testpre/m/mytestowner/mydir/dir/MyTestOutputPath1/myTestOutputFile1.txt', self)
      assertDiracSucceedsWith(
          result, '/ilc/testpre/m/mytestowner/mydir/dir/MyTestOutputPath1/myTestOutputFile2.ppt', self)
      log_mock.assert_called_once_with('Could not get VO from CS, assuming ilc')

  def test_construct_user_lfns_novo(self):
    today_mock = Mock()
    today_mock.timetuple.return_value = [1999, 27]
    date_mock = Mock()
    date_mock.today.return_value = today_mock
    with patch('%s.datetime.date' % MODULE_NAME, new=date_mock), \
         patch('%s.Operations.getValue' % MODULE_NAME, new=Mock(return_value='testpre')), \
         patch('%s.getVOfromProxyGroup' % MODULE_NAME, new=Mock(return_value=S_OK('mytestproxyvo'))):
      result = constructUserLFNs(1234567, None, 'mytestowner',
                                  ['myTestOutputFile1.txt', 'myTestOutputFile2.ppt'],
                                  '/mydir/dir//MyTestOutputPath1')
      assertDiracSucceedsWith(
          result, '/mytestproxyvo/testpre/m/mytestowner/mydir/dir/MyTestOutputPath1/myTestOutputFile1.txt', self)
      assertDiracSucceedsWith(
          result, '/mytestproxyvo/testpre/m/mytestowner/mydir/dir/MyTestOutputPath1/myTestOutputFile2.ppt', self)

  def test_construct_user_lfns_no_outputpath(self):
    today_mock = Mock()
    today_mock.timetuple.return_value = [1999, 27]
    date_mock = Mock()
    date_mock.today.return_value = today_mock
    with patch('%s.datetime.date' % MODULE_NAME, new=date_mock), \
         patch('%s.Operations.getValue' % MODULE_NAME, new=Mock(return_value='testpre')):
      result = constructUserLFNs(1234567, 'mytestVO', 'mytestowner', '/ignore/this/myOutputString.md5', None)
      assertDiracSucceedsWith(
          result, '/mytestVO/testpre/m/mytestowner/1999_27/1234/1234567/myOutputString.md5', self)

  def test_construct_user_lfns_no_lfns(self):
    with patch('%s.Operations.getValue' % MODULE_NAME, new=Mock(return_value='testpre')), \
        patch('%s.gLogger.info' % MODULE_NAME) as log_mock:
      result = constructUserLFNs(1234567, 'mytestVO', 'mytestowner', [], '')
      log_mock.assert_called_once_with('No output LFN(s) constructed')
      assertDiracSucceedsWith_equals(result, [], self)

  def test_getExperimentFromBasePath(self):
    optDict = S_OK({'exp1': '/ilc/prod/exp1', 'exp2': '/ilc/prod/exp2/path1, /ilc/prod/exp2/path2'})
    with patch('%s.Operations.getOptionsDict' % MODULE_NAME, new=Mock(return_value=optDict)):
      experiment = getExperimentFromPath(Mock(), '/ilc/prod/exp2/path1/log/file', 'default')
      self.assertEqual(experiment, 'exp2')
      experiment = getExperimentFromPath(Mock(), '/ilc/prod/exp/log/file', 'default')
      self.assertEqual(experiment, 'default')

    optDict = S_ERROR("not found")
    with patch('%s.Operations.getOptionsDict' % MODULE_NAME, new=Mock(return_value=optDict)):
      experiment = getExperimentFromPath(Mock(), '/ilc/prod/exp2/path1/log/file', 'default')
      self.assertEqual(experiment, 'default')
