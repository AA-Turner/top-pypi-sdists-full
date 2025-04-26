#######################################################################
# Tests for toposort module.
#
# Copyright 2014-2021 True Blade Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Notes:
#
########################################################################

import unittest

from toposort import toposort, toposort_flatten, CircularDependencyError


class TestCase(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(
            list(
                toposort(
                    {
                        2: {11},
                        9: {11, 8},
                        10: {11, 3},
                        11: {7, 5},
                        8: {7, 3},
                    }
                )
            ),
            [
                {3, 5, 7},
                {8, 11},
                {2, 9, 10},
            ],
        )

        # Make sure self dependencies are ignored.
        self.assertEqual(
            list(
                toposort(
                    {
                        2: {2, 11},
                        9: {11, 8},
                        10: {10, 11, 3},
                        11: {7, 5},
                        8: {7, 3},
                    }
                )
            ),
            [
                {3, 5, 7},
                {8, 11},
                {2, 9, 10},
            ],
        )

        self.assertEqual(list(toposort({1: set()})), [{1}])
        self.assertEqual(list(toposort({1: {1}})), [{1}])

    def test_no_dependencies(self):
        self.assertEqual(
            list(
                toposort(
                    {
                        1: {2},
                        3: {4},
                        5: {6},
                    }
                )
            ),
            [{2, 4, 6}, {1, 3, 5}],
        )

        self.assertEqual(
            list(
                toposort(
                    {
                        1: set(),
                        3: set(),
                        5: set(),
                    }
                )
            ),
            [{1, 3, 5}],
        )

    def test_empty(self):
        self.assertEqual(list(toposort({})), [])

    def test_strings(self):
        self.assertEqual(
            list(
                toposort(
                    {
                        "2": {"11"},
                        "9": {"11", "8"},
                        "10": {"11", "3"},
                        "11": {"7", "5"},
                        "8": {"7", "3"},
                    }
                )
            ),
            [
                {"3", "5", "7"},
                {"8", "11"},
                {"2", "9", "10"},
            ],
        )

    def test_objects(self):
        o2 = object()
        o3 = object()
        o5 = object()
        o7 = object()
        o8 = object()
        o9 = object()
        o10 = object()
        o11 = object()
        self.assertEqual(
            list(
                toposort(
                    {
                        o2: {o11},
                        o9: {o11, o8},
                        o10: {o11, o3},
                        o11: {o7, o5},
                        o8: {o7, o3, o8},
                    }
                )
            ),
            [
                {o3, o5, o7},
                {o8, o11},
                {o2, o9, o10},
            ],
        )

    def test_cycle(self):
        # A simple, 2 element cycle.
        # Make sure we can catch this both as ValueError and CircularDependencyError.
        self.assertRaises(ValueError, list, toposort({1: {2}, 2: {1}}))
        with self.assertRaises(CircularDependencyError) as ex:
            list(toposort({1: {2}, 2: {1}}))
        self.assertEqual(ex.exception.data, {1: {2}, 2: {1}})

        # An indirect cycle.
        self.assertRaises(
            ValueError,
            list,
            toposort(
                {
                    1: {2},
                    2: {3},
                    3: {1},
                }
            ),
        )
        with self.assertRaises(CircularDependencyError) as ex:
            list(
                toposort(
                    {
                        1: {2},
                        2: {3},
                        3: {1},
                    }
                )
            )
        self.assertEqual(ex.exception.data, {1: {2}, 2: {3}, 3: {1}})

        # Not all elements involved in a cycle.
        with self.assertRaises(CircularDependencyError) as ex:
            list(
                toposort(
                    {
                        1: {2},
                        2: {3},
                        3: {1},
                        5: {4},
                        4: {6},
                    }
                )
            )
        self.assertEqual(ex.exception.data, {1: set([2]), 2: set([3]), 3: set([1])})

    def test_input_not_modified(self):
        def get_data():
            return {
                2: {11},
                9: {11, 8},
                10: {11, 3},
                11: {7, 5},
                8: {7, 3, 8},  # Includes something self-referential.
            }

        data = get_data()
        orig = get_data()
        self.assertEqual(data, orig)
        results = list(toposort(data))
        self.assertEqual(data, orig)

    def test_input_not_modified_when_cycle_error(self):
        def get_data():
            return {
                1: {2},
                2: {1},
                3: {4},
            }

        data = get_data()
        orig = get_data()
        self.assertEqual(data, orig)
        self.assertRaises(ValueError, list, toposort(data))
        self.assertEqual(data, orig)

    def test_unsortable_with_circular_dependency(self):
        # https://gitlab.com/ericvsmith/toposort/-/issues/2

        # Objects which are hashable, but not orderable should not raise a
        # typeError when raising a CircularDependencyError.
        class A: pass

        class B: pass

        class C: pass

        # These work okay.
        self.assertEqual(list(toposort({A: {B}, B: {C}})), [{C}, {B}, {A}])
        self.assertEqual(list(toposort({A: set(), B: set(), C: set()})), [{A, B, C}])

        # This used to raise a TypeError, because of the sorting when
        # CircularDependencyError was raised.
        self.assertRaises(CircularDependencyError, list, toposort({A: {B}, B: {C}, C: {A}}))


class TestCaseAll(unittest.TestCase):
    def test_sort_flatten(self):
        data = {
            2: {11},
            9: {11, 8},
            10: {11, 3},
            11: {7, 5},
            8: {7, 3, 8},  # Includes something self-referential.
        }
        expected = [{3, 5, 7}, {8, 11}, {2, 9, 10}]
        self.assertEqual(list(toposort(data)), expected)

        # Now check the sorted results.
        results = []
        for item in expected:
            results.extend(sorted(item))
        self.assertEqual(toposort_flatten(data), results)

        # And the unsorted results.  Break the results up into groups to
        # compare them.
        actual = toposort_flatten(data, False)
        results = [
            {i for i in actual[0:3]},
            {i for i in actual[3:5]},
            {i for i in actual[5:8]},
        ]
        self.assertEqual(results, expected)


class TestAll(unittest.TestCase):
    def test_all(self):
        import toposort

        # Check that __all__ in the module contains everything that should be
        # public, and only those symbols.
        all = set(toposort.__all__)

        # Check that things in __all__ only appear once.
        self.assertEqual(
            len(all),
            len(toposort.__all__),
            "some symbols appear more than once in __all__",
        )

        # Get the list of public symbols.
        found = set(name for name in dir(toposort) if not name.startswith("_"))

        # Make sure it matches __all__.
        self.assertEqual(all, found)


unittest.main()
