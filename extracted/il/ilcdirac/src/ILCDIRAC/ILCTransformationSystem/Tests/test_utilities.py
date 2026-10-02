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
"""Tests for ILCTransformationSystem.Utilities.Utilities."""
from __future__ import absolute_import
from ILCDIRAC.ILCTransformationSystem.Utilities.Utilities import Task


def test_Constructor():
  """Test for the constructor and functions used inside."""
  metaInput = {'ProdID': 123, 'Energy': '100'}
  parameterDict = {'process': 'higgses'}
  eventsPerJob = 22
  theTask = Task(metaInput, parameterDict, eventsPerJob)
  assert theTask.meta['ProdID'] == 123
  assert theTask.getProdName() == 'higgses_100'

  metaInput = {'ProdID': 124, 'Energy': '100'}
  metaPrev = {'ProdID': 123, 'Energy': '100'}
  theTask = Task(metaInput, parameterDict, eventsPerJob, metaPrev)
  assert theTask.meta['ProdID'] == 124
  assert theTask.meta['NumberOfEvents'] == eventsPerJob
  theTask.taskName = 'aTask'
  assert theTask.getProdName() == 'higgses_100_aTask'
  theTask.sourceName = 'theSource'
  assert theTask.getProdName() == 'higgses_100_theSource_aTask'

  theTask = Task(metaInput, parameterDict, eventsPerJob, metaPrev)
  assert theTask.meta['ProdID'] == 124
  assert theTask.meta['NumberOfEvents'] == eventsPerJob

  theTask = Task(metaInput, parameterDict, None, metaPrev)
  assert theTask.meta['ProdID'] == 124
  assert theTask.meta.get('NumberOfEvents') is None

  theTask = Task(metaInput, parameterDict, eventsPerJob=0, metaPrev=metaPrev)
  assert theTask.meta.get('NumberOfEvents') == 0
  assert theTask.meta.get('ProdID') == 124

  # expect eventsPerBaseFile
  theTask = Task(metaInput, parameterDict, eventsPerJob=0, metaPrev=metaPrev, eventsPerBaseFile=333)
  assert theTask.meta.get('NumberOfEvents') == 333


def test_repr():
  """Test the str and repr functions for Task."""
  task = Task({}, {}, 1)
  expectation = '{' + ',\n'.join('%r:%r' % (p, val) for p, val in sorted(vars(task).items())) + '}'
  assert repr(task).replace(' ', '') == expectation.replace(' ', '')
