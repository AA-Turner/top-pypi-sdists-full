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
"""Test the Core CheckAndGetProdProxy."""

from __future__ import absolute_import
import unittest
from mock import MagicMock as Mock, patch
from DIRAC import S_OK, S_ERROR
from ILCDIRAC.Core.Utilities.CheckAndGetProdProxy import checkAndGetProdProxy, checkOrGetGroupProxy

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Core.Utilities.CheckAndGetProdProxy'


class CheckProxyTest(unittest.TestCase):
  """Test the CheckProxy."""

  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_success(self):
    """test for CheckandGetProdProxy: success......................................................."""
    with patch("%s.call" % MODULE_NAME, new=Mock(return_value=0)), \
         patch("%s.getProxyInfo" % MODULE_NAME, new=Mock(return_value=S_OK({"group": "ilc_prod"}))):
      res = checkAndGetProdProxy()
      self.assertTrue(res['OK'])

  def test_success_2(self):
    """test for CheckandGetProdProxy: sucess 2......................................................"""
    with patch("%s.call" % MODULE_NAME, new=Mock(return_value=0)), \
         patch("%s.getProxyInfo" % MODULE_NAME, new=Mock(side_effect=[S_OK({"group": "ilc_user"}), S_OK({"group": "ilc_prod"})])):
      res = checkAndGetProdProxy()
      self.assertTrue(res['OK'])

  def test_failure(self):
    """test for CheckandGetProdProxy: failure......................................................."""
    with patch("%s.call" % MODULE_NAME, new=Mock(return_value=1)), \
         patch("%s.getProxyInfo" % MODULE_NAME, new=Mock(return_value=S_ERROR('No proxy info'))):
      res = checkAndGetProdProxy()
      self.assertFalse(res['OK'])

  def test_failure_2(self):
    """test for CheckandGetProdProxy: semi failure 1................................................"""
    with patch("%s.call" % MODULE_NAME, new=Mock(return_value=0)), \
         patch("%s.getProxyInfo" % MODULE_NAME, new=Mock(return_value=S_ERROR('message'))):
      res = checkAndGetProdProxy()
      self.assertFalse(res['OK'])

  def test_failure_3(self):
    """test for CheckandGetProdProxy: semi failure 2................................................"""
    with patch("%s.call" % MODULE_NAME, new=Mock(return_value=0)), \
         patch("%s.getProxyInfo" % MODULE_NAME, new=Mock(side_effect=[S_OK({}), S_OK({"group": "ilc_prod"})])):
      res = checkAndGetProdProxy()
      self.assertTrue(res['OK'])

  def test_failure_4(self):
    """test for CheckandGetProdProxy: semi failure 3................................................"""
    with patch("%s.call" % MODULE_NAME, new=Mock(return_value=0)), \
         patch("%s.getProxyInfo" % MODULE_NAME, new=Mock(side_effect=[S_ERROR("no proxy info"), S_OK({"group": "ilc_prod"})])):
      res = checkAndGetProdProxy()
      self.assertTrue(res['OK'])

  def test_failure_5(self):
    """test for CheckandGetProdProxy: semi failure 4................................................"""
    with patch("%s.call" % MODULE_NAME, new=Mock(return_value=0)), \
         patch("%s.getProxyInfo" % MODULE_NAME, new=Mock(side_effect=[S_ERROR("no proxy info"), S_OK({"notgroup": "ilc_user"})])):
      res = checkAndGetProdProxy()
      self.assertTrue(not res['OK'])

  def test_failure_6(self):
    """test for CheckandGetProdProxy: semi failure 5................................................"""
    with patch("%s.call" % MODULE_NAME, new=Mock(return_value=0)), \
         patch("%s.getProxyInfo" % MODULE_NAME, new=Mock(side_effect=[S_ERROR("no proxy info"), S_OK({"group": "ilc_user"})])):
      res = checkAndGetProdProxy()
      self.assertTrue(not res['OK'])

  def test_failure_7(self):
    """test for CheckandGetProdProxy: semi failure 6................................................"""
    with patch("%s.call" % MODULE_NAME, new=Mock(return_value=0)), \
         patch("%s.getProxyInfo" % MODULE_NAME, new=Mock(side_effect=[S_ERROR("no proxy info"), S_ERROR("Still no proxy")])):
      res = checkAndGetProdProxy()
      self.assertTrue(not res['OK'])

  def test_checkOrGet(self):
    """test for checkOrGetGroupProxy: .............................................................."""
    with patch('%s.call' % MODULE_NAME, new=Mock(return_value=0)), \
         patch('%s.getProxyInfo' % MODULE_NAME, new=Mock(return_value=S_OK({'group': 'fcc_prod'}))):
      res = checkOrGetGroupProxy(['ilc_prod', 'fcc_prod'])
      self.assertTrue(res['OK'])
      self.assertEqual(res['Value'], 'fcc_prod')

    with patch('%s.call' % MODULE_NAME, new=Mock(return_value=0)), \
         patch('%s.getProxyInfo' % MODULE_NAME, new=Mock(return_value=S_OK({'groupProperties': 'NormalUser'}))):
      res = checkOrGetGroupProxy(['ilc_prod', 'fcc_prod'])
      self.assertFalse(res['OK'])
      self.assertIn('More than one', res['Message'])

    with patch('%s.call' % MODULE_NAME, new=Mock(return_value=0)), \
         patch('%s.getProxyInfo' % MODULE_NAME, new=Mock(return_value=S_OK({'group': 'ilc_user'}))):
      res = checkOrGetGroupProxy('ilc_user')
      self.assertTrue(res['OK'])
      self.assertEqual(res['Value'], 'ilc_user')


if __name__ == "__main__":
  SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(CheckProxyTest)
  TESTRESULT = unittest.TextTestRunner(verbosity=2).run(SUITE)
