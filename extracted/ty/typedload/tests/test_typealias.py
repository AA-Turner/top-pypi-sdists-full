# typedload
# Copyright (C) 2024 Salvo "LtWorf" Tomaselli
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
from dataclasses import dataclass
from typing import List, Set, FrozenSet, Tuple, TypedDict, Required, NamedTuple

# Run tests for attr only if it is installed
try:
    from attr import define
    attr_module = True
except ImportError:
    attr_module = False

from typedload import typechecks, load


class TestSimpleAliasLoad(unittest.TestCase):

    def test_basicload(self):
        type s = str
        type i = int

        assert load(3, i) == 3
        assert load("iaffieddu", s) == "iaffieddu"

    def test_unionload(self):
        type IntOrStr = int | str
        assert load(3, IntOrStr) == 3
        assert load("iaffieddu", IntOrStr) == "iaffieddu"
        assert load("3", IntOrStr) == "3"

    def test_forward_def_load(self):
        type t = int | A

        @dataclass
        class A:
            i: int

        assert load(3, t) == 3
        assert load({'i': 3}, t) == A(3)

    def test_tuple(self):
        type Point = tuple[float, float]
        assert load([4,2], Point) == (4, 2)

    def test_tupleunion(self):
        type FPoint = tuple[float, float]
        type IPoint = tuple[int, int]
        type Point = FPoint | IPoint

        assert load([4,2], Point) == (4, 2)
        assert load([4.0,2.0], Point) == (4.0, 2.0)

    def test_nested(self):
        type i = int
        type IntOrStr = i | str
        r=load(3, IntOrStr)
        assert load(3, IntOrStr) == 3

        type l = list[i]
        type L = List[i]
        assert load([1], l) == [1]
        assert load([1], L) == [1]

        type s = set[i]
        type S = Set[i]
        assert load([1], s) == {1}
        assert load([1], S) == {1}

        type f = frozenset[i]
        type F = FrozenSet[i]
        assert load([1], f) == frozenset({1})
        assert load([1], F) == frozenset({1})

        type t = tuple[i, ...]
        type T = Tuple[i, ...]
        assert load([1, 2], t) == (1, 2)
        assert load([1, 2], T) == (1, 2)

class TestFieldAliasLoad(unittest.TestCase):
    def test_indataclass(self):
        type int_alias = int

        @dataclass
        class A:
            i: int_alias

        assert load({'i': 1}, A) == A(1)

    def test_intypeddict(self):
        type int_alias = int

        class A(TypedDict):
            i: Required[int_alias]

        assert load({'i': 1}, A) == {'i': 1}

    def test_innamedtuple(self):
        type int_alias = int

        class A(NamedTuple):
            i: int_alias

        assert load({'i': 1}, A) == A(1)

    if attr_module:
        def test_inattr(self):
            type int_alias = int

            @define
            class A:
                i: int_alias

            assert load({'i': 1}, A) == A(1)

    def test_unioninnamedtuple(self):
        type number = int | float

        class A(NamedTuple):
            i: number

        assert load({'i': 3}, A) == A(3)

    def test_listinnamedtuple(self):
        type number = int | float

        class A(NamedTuple):
            i: list[number]

        assert load({'i': [3]}, A) == A([3])
        assert load({'i': [3.0]}, A) == A([3.0])

    def test_listaliasinnamedtuple(self):
        type number = int | float
        type list_of_numbers = list[number]

        class A(NamedTuple):
            i: list_of_numbers

        assert load({'i': [3,4,5,0.1]}, A) == A([3,4,5,0.1])

    def test_listunionaliasinnamedtuple(self):
        type list_of_numbers = list[int | float]

        class A(NamedTuple):
            i: list_of_numbers

        assert load({'i': [3,4,5,0.1]}, A) == A([3,4,5,0.1])

    def test_nesteduniontuple(self):
        type FPoint = tuple[float, float]
        type IPoint = tuple[int, int]
        type Point = FPoint | IPoint

        class A(NamedTuple):
            i: list[Point]

        assert load({'i': [[1,1], [1.0, 1.0]]}, A) == A([(1,1), (1.0,1.0)])
