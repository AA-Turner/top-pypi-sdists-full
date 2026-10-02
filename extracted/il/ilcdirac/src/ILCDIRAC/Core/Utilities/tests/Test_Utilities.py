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
"""Tests for Utilities functions."""

from __future__ import absolute_import
import pytest

from ILCDIRAC.Core.Utilities.Utilities import toInt, listify, lowerFirst, canConvert


@pytest.mark.parametrize("number, expected, cond",
                         [("1", 1, None),
                          ("1.2", False, None),
                          (1.2, 1, None),
                          ("-1", -1, None),
                          (None, None, None),
                          ("a", False, None),
                          ("-1", False, lambda x: x > 0),
                          ("12", 12, lambda x: x > 0),
                          ])
def test_toint(number, expected, cond):
  """Testing the to int function."""
  assert toInt(number, cond=cond) == expected


@pytest.mark.parametrize("string, cast, expected",
                         [("1", None, ['1']),
                          ("1,3", None, ['1', '3']),
                          ("1,3,,,", int, [1, 3]),
                          ("0, 1,3", int, [0, 1, 3]),
                          ("  foo  , bar  ", None, ['foo', 'bar']),
                          ([1, 3, 4], None, [1, 3, 4]),
                          ])
def test_listify(string, cast, expected):
  """Testing the to int function."""
  assert listify(string, cast) == expected


@pytest.mark.parametrize('string, expected',
                         [('1', '1'),
                          ('SOMETHING', 'sOMETHING'),
                          ('something', 'something'),
                          ('CamelCase', 'camelCase'),
                          ])
def test_lowerFirst(string, expected):
  """Testing the lowerFirst function."""
  assert lowerFirst(string) == expected


@pytest.mark.parametrize('string, cast, expected',
                         [('5', int, True),
                           ('Five', int, False),
                           ('5.', int, False),
                           ('5.0', float, True),
                           ('5.0e10', float, True),
                           ('fff5.0f', float, False),
                           ])
def test_canConvert(string, cast, expected):
  """Testing the canConvert function."""
  assert canConvert(string, cast) == expected
