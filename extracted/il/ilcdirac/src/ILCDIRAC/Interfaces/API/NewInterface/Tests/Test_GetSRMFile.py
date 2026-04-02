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
"""Test GetSRMFile  module."""

from __future__ import absolute_import
import unittest
from mock import patch, MagicMock as Mock

from DIRAC import S_OK, S_ERROR
from ILCDIRAC.Interfaces.API.NewInterface.Applications import GetSRMFile
from Tests.Utilities.GeneralUtils import assertEqualsImproved, assertDiracFailsWith, \
    assertDiracSucceeds

__RCSID__ = "$Id$"

MODULE_NAME = 'ILCDIRAC.Interfaces.API.NewInterface.Applications.GetSRMFile'

# pylint: disable=protected-access


class GetSRMFileTestCase(unittest.TestCase):
  """Base class for the GetSRMFile test cases."""

  def setUp(self):
    """set up the objects."""
    self.gsf = GetSRMFile({})

  def test_setfiles(self):
    self.assertFalse(self.gsf._errorDict)
    self.gsf.setFiles({'mydict': True, 'soimething': 138, True: []})
    self.assertFalse(self.gsf._errorDict)
    assertEqualsImproved(self.gsf.files, {'mydict': True, 'soimething': 138, True: []}, self)
    self.gsf.setFiles([{'some_dict': True}, {}, {True: 184, False: [], 'bla': 'aiejf'}])
    self.assertFalse(self.gsf._errorDict)
    assertEqualsImproved(self.gsf.files, [{'some_dict': True}, {},
                                            {True: 184, False: [], 'bla': 'aiejf'}], self)

  def test_setfiles_wrongtype(self):
    self.assertFalse(self.gsf._errorDict)
    self.gsf.setFiles(1498)
    assertEqualsImproved(len(self.gsf._errorDict['setFiles']), 1, self)

  def test_userjobmodules(self):
    module_mock = Mock()
    assertDiracSucceeds(self.gsf._userjobmodules(module_mock), self)

  def test_prodjobmodules(self):
    assertDiracFailsWith(self.gsf._prodjobmodules(Mock()),
                          'should not use in production', self)

  def test_userjobmodules_fails(self):
    with patch('%s._setUserJobFinalization' % MODULE_NAME, new=Mock(return_value=S_OK('something'))),\
        patch('%s._setApplicationModuleAndParameters' % MODULE_NAME, new=Mock(return_value=S_ERROR('some_test_err'))):
      assertDiracFailsWith(self.gsf._userjobmodules(None),
                            'userjobmodules method failed', self)

  def test_checkconsistency_nofiles(self):
    assertDiracFailsWith(self.gsf._checkConsistency(), 'file list was not defined', self)

  def test_checkconsistency(self):
    self.gsf.setFiles({'file': '/invalid/dir/mycoolfile.txt', 'something': True})
    assertDiracSucceeds(self.gsf._checkConsistency(), self)
    assertEqualsImproved(self.gsf.outputFile, 'mycoolfile.txt', self)

  def test_checkconsistency_list(self):
    self.gsf.setFiles([{'file': '/invalid/dir/mycoolfile.txt', 'something': True},
                         {'file': '/some/other/dir/other_file.123.stdhep'}])
    assertDiracSucceeds(self.gsf._checkConsistency(), self)
    assertEqualsImproved(self.gsf.outputFile, 'mycoolfile.txt;other_file.123.stdhep', self)

  def test_addparams(self):
    assertDiracSucceeds(self.gsf._addParametersToStep(Mock()), self)

  def test_addparams_fails(self):
    with patch.object(self.gsf, '_addBaseParameters', new=Mock(return_value=S_ERROR('my_patched_testerr'))):
      assertDiracFailsWith(self.gsf._addParametersToStep(None),
                            'failed to set base parameters', self)
