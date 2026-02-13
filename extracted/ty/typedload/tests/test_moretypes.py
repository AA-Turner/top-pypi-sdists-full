# typedload
# Copyright (C) 2026 Salvo "LtWorf" Tomaselli
#
# typedload is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# author Salvo "LtWorf" Tomaselli <tiposchi@tiscali.it>

import unittest

from typedload.moretypes import *
from typedload import load, dump


class TestHexRGB(unittest.TestCase):

    def test_dump(self):
        assert dump(HexRGB('#Ff0000')) == '#FF0000'
        assert isinstance(dump(HexRGB('#Ff0000')), str)

    def test_load(self):
        assert load('#0000ff', HexRGB) == HexRGB('#0000Ff')
        assert isinstance(load('#0000ff', HexRGB), HexRGB)

    def test_values(self):
        assert HexRGB('#Ff0000').rgb() == (255, 0, 0)
        assert HexRGB('#0AFFFf').rgb() == (10, 255, 255)
        assert HexRGB('#000000').rgb() == (0, 0, 0)
        assert HexRGB('#000001').rgb() == (0, 0, 1)
        assert HexRGB(7).rgb() == (0, 0, 7)

    def test_equality(self):
        assert HexRGB('#0000ff') ==  HexRGB('#0000FF')
        assert HexRGB('#0000ff') !=  '#0000ff'
        assert HexRGB('#0000ff') !=  255
        assert HexRGB('#0000ff').value ==  255

    def test_fail(self):
        with self.assertRaises(TypeError):
            HexRGB()
        with self.assertRaises(ValueError):
            HexRGB('#ffaab')
        with self.assertRaises(ValueError):
            HexRGB('FFAABB')
        with self.assertRaises(ValueError):
            HexRGB('#00000x')
        with self.assertRaises(ValueError):
            HexRGB(-1)
        with self.assertRaises(ValueError):
            HexRGB(16777216)
        with self.assertRaises(TypeError):
            HexRGB(4.1)

    def test_immutable(self):
        c = HexRGB(1)

        with self.assertRaises(AttributeError):
            c.qwe = 123
        with self.assertRaises(AttributeError):
            c.value = 2
