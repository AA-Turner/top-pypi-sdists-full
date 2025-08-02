#!/usr/local/env python
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
"""Test Pythia module."""

from __future__ import absolute_import
import unittest
from mock import patch, MagicMock as Mock

from DIRAC import S_OK, S_ERROR
from ILCDIRAC.Interfaces.API.NewInterface.Applications import Pythia
from Tests.Utilities.GeneralUtils import assertDiracFailsWith, assertDiracSucceeds

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Interfaces.API.NewInterface.Applications.Pythia'

# pylint: disable=protected-access


class PythiaTestCase(unittest.TestCase):
  """Base class for the Pythia test cases."""

  def setUp(self):
    """set up the objects."""
    self.pyt = Pythia({})

  def test_userjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.pyt._userjobmodules(module_mock), self)

  def test_prodjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.pyt._prodjobmodules(module_mock), self)

  def test_userjobmodules_fails(self):
    with patch('%s._setUserJobFinalization' % MODULE_NAME, new=Mock(return_value=S_OK('something'))),\
        patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_test_err'))):
      assertDiracFailsWith(self.pyt._userjobmodules(None),
                            'userjobmodules failed', self)

  def test_prodjobmodules_fails(self):
    with patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_OK('something'))), \
        patch('%s._setOutputComputeDataList' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_other_test_err'))):
      assertDiracFailsWith(self.pyt._prodjobmodules(None),
                            'prodjobmodules failed', self)

  def test_checkconsistency(self):
    self.pyt.version = '134'
    self.pyt.numberOfEvents = 2145
    self.pyt.outputFile = 'myoutput.file'
    self.pyt._jobtype = 'User'
    assertDiracSucceeds(self.pyt._checkConsistency(), self)
    self.assertNotIn({'outputFile': '@{OutputFile}', 'outputPath': '@{OutputPath}',
                        'outputDataSE': '@{OutputSE}'}, self.pyt._listofoutput)
    self.assertNotIn('nbevts', self.pyt.prodparameters)
    self.assertNotIn('Process', self.pyt.prodparameters)

  def test_checkconsistency_noversion(self):
    self.pyt.version = None
    assertDiracFailsWith(self.pyt._checkConsistency(), 'version not specified', self)

  def test_checkconsistency_nonbevts(self):
    self.pyt.version = '134'
    self.pyt.numberOfEvents = None
    assertDiracFailsWith(self.pyt._checkConsistency(), 'number of events to generate not defined', self)

  def test_checkconsistency_nooutput(self):
    self.pyt.version = '134'
    self.pyt.numberOfEvents = 2145
    self.pyt.outputFile = None
    assertDiracFailsWith(self.pyt._checkConsistency(), 'output file not defined', self)

  def test_checkconsistency_no_userjob(self):
    self.pyt.version = '134'
    self.pyt.numberOfEvents = 2145
    self.pyt.outputFile = 'myoutput.file'
    self.pyt._jobtype = 'notUser'
    assertDiracSucceeds(self.pyt._checkConsistency(), self)
    self.assertIn({'outputFile': '@{OutputFile}', 'outputPath': '@{OutputPath}',
                        'outputDataSE': '@{OutputSE}'}, self.pyt._listofoutput)
    self.assertIn('nbevts', self.pyt.prodparameters)
    self.assertIn('Process', self.pyt.prodparameters)

  def test_checkconsistency_no_cut(self):
    self.pyt.version = '134'
    self.pyt.numberOfEvents = 2145
    self.pyt.outputFile = 'myoutput.file'
    self.pyt._jobtype = 'notUser'
    self.pyt.willCut()
    assertDiracSucceeds(self.pyt._checkConsistency(), self)
    self.assertNotIn({'outputFile': '@{OutputFile}', 'outputPath': '@{OutputPath}',
                        'outputDataSE': '@{OutputSE}'}, self.pyt._listofoutput)
    self.assertIn('nbevts', self.pyt.prodparameters)
    self.assertIn('Process', self.pyt.prodparameters)
