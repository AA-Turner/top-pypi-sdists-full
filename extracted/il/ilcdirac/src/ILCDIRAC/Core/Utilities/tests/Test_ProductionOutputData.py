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
"""Tests for .Core.Utilities.ProductionData.constructProductionLFNs."""

from __future__ import print_function
from __future__ import absolute_import
import unittest
from ILCDIRAC.Core.Utilities.ProductionData import constructProductionLFNs

__RCSID__ = "$Id$"


class ProductionOutputDataTestCase(unittest.TestCase):
  """Base class for the test cases."""

  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_contructProductionLFNBad(self):
    """test ProductionOutputData construct Bad LFN.................................................."""
    commons = {}
    result = constructProductionLFNs(commons)
    self.assertEqual(result['OK'], False)

  def test_contructProductionLFNstdhep(self):
    """test ProductionOutputData construct stdhep LFN..............................................."""
    commons = {}
    commons['PRODUCTION_ID'] = 12345
    commons['JOB_ID'] = 1234
    commons['outputList'] = [{'outputFile': "something_gen.stdhep",
                              'outputPath': '/ilc/prod/clic/test/gen'}]
    result = constructProductionLFNs(commons)

    self.assertEqual(result['OK'], True)

  def test_contructProductionLFNsim(self):
    """test ProductionOutputData construct sim LFN.................................................."""
    commons = {}
    commons['PRODUCTION_ID'] = 12345
    commons['JOB_ID'] = 1234
    commons['outputList'] = [{'outputFile': "something_sim.slcio",
                              'outputPath': '/ilc/prod/clic/test/SIM'}]
    result = constructProductionLFNs(commons)
    self.assertEqual(result['OK'], True)

  def test_contructProductionLFNrec(self):
    """test ProductionOutputData construct rec LFN.................................................."""
    commons = {}
    commons['PRODUCTION_ID'] = 12345
    commons['JOB_ID'] = 1234
    commons['outputList'] = [{'outputFile': "something_rec.slcio",
                              'outputPath': '/ilc/prod/clic/test/REC'},
                             {'outputFile': "something_dst.slcio",
                              'outputPath': '/ilc/prod/clic/test/DST'}]
    result = constructProductionLFNs(commons)
    self.assertEqual(result['OK'], True)

  def test_contructProductionLFNoutput(self):
    """test ProductionOutputData construct out LFN.................................................."""
    commons = {}
    commons['PRODUCTION_ID'] = 12345
    commons['JOB_ID'] = 1234
    commons['outputList'] = [{'outputFile': "something_gen.stdhep",
                              'outputPath': '/ilc/prod/clic/test/gen'}]
    result = constructProductionLFNs(commons)
    res = {'ProductionOutputData': ["/ilc/prod/clic/test/gen/00012345/001/something_gen_12345_1234.stdhep"],
           'LogFilePath': ["/ilc/prod/clic/test/gen/00012345/LOG/001"],
           'LogTargetPath': ["/ilc/prod/clic/test/gen/LOG/00012345/00012345_1234.tar"]}
    for key in res.keys():
      self.assertEqual(result['Value'][key], res[key])


def runTests():
  """runs all the tests."""
  suite = unittest.defaultTestLoader.loadTestsFromTestCase(ProductionOutputDataTestCase)
  testResult = unittest.TextTestRunner(verbosity=2).run(suite)
  print(testResult)


if __name__ == '__main__':
  runTests()
