# ------------------------------------------------------------------------------
# Copyright (C) 2019, 2021 Maximilian Stahlberg
#
# This file is part of PICOS Testbench.
#
# PICOS Testbench is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# PICOS Testbench is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

"""A small doctest integration framework for PICOS.

Provides helpers to load doctests from PICOS' source and documentation as
:mod:`unittest` test suites.
"""

import doctest
import importlib
import pkgutil
import unittest
from pathlib import Path
from types import ModuleType

import picos

RST_DIR = Path(__file__).parent.parent / "doc"
"""Directory containing .rst documentation files."""


def submodules(module):
    """Import and yield all submodules of a module recursively."""
    if not isinstance(module, ModuleType):
        raise TypeError("Not a module: {}".format(module))

    yield module

    if hasattr(module, "__path__"):
        for submodule_info in pkgutil.iter_modules(module.__path__):
            submodule = importlib.import_module(
                "." + submodule_info.name, module.__name__)

            yield from submodules(submodule)


class SrcTestCase(doctest.DocTestCase):
    """Class for monkey-patching a :class:`doctest.DocTestCase`."""

    def testName(self):
        """Return a short test name."""
        module = self._caseName.rsplit(".", 1)[0]
        tokens = self._dt_test.name.split(".")
        try:
            index = tokens.index(module) + 1
            if index == len(tokens):
                return tokens[-1]
            else:
                return ".".join(tokens[index:])
        except Exception:
            return tokens[-1]

    def __str__(self):
        return "Doctests of {}: {}".format(self._caseName, self.testName())

    def shortDescription(self):
        """Remove the short description."""
        return None


class RstTestCase(doctest.DocTestCase):
    """Class for monkey-patching a :class:`doctest.DocTestCase`."""

    def testName(self):
        """Return a short test name."""
        return self._dt_test.name

    def __str__(self):
        return "Doctests of {}".format(self._caseName)

    def shortDescription(self):
        """Remove the short description."""
        return None


def makeTestSuite(testSetFilter=None, testCaseFilter=None, testNameFilter=None,
        listSelection=False):
    """Create a doctest test suite.

    :param list(str) testSetFilter:
        Collection of test set names to select.

    :param list(str) testCaseFilter:
        Collection of test case names to select.

    :param list(str) testNameFilter:
        Collection of test names to select.

    :param bool listSelection:
        Whether to return a triple ``(sets, cases, names)`` with sorted names of
        selected test sets, cases, and tests.

    :returns:
        A :class:`unittest.TestSuite`.
    """
    if listSelection:
        setList  = ["source", "docs"]
        caseList = []
        testList = []
    else:
        testSuite = unittest.TestSuite()

    # Make filters case-insensitive.
    if testSetFilter:
        testSetFilter = [name.lower() for name in testSetFilter]
    if testCaseFilter:
        testCaseFilter = [name.lower() for name in testCaseFilter]
    if testNameFilter:
        testNameFilter = [name.lower() for name in testNameFilter]

    # Add source doctests.
    if not testSetFilter or "source" in testSetFilter:
        sourceTestSuite = unittest.TestSuite()

        for module in submodules(picos):
            caseName = Path(module.__file__).name.lower()

            if not testCaseFilter or caseName in testCaseFilter:
                fullSuite = doctest.DocTestSuite(module)

                # Filter the suite with respect to test names.
                suite = unittest.TestSuite()
                for test in fullSuite:
                    # HACK: Monkey-patch the test case instance (= single test).
                    test.__class__ = SrcTestCase
                    test._caseName = caseName

                    testName = test.testName().lower()

                    if not testNameFilter or testName in testNameFilter:
                        suite.addTest(test)

                if suite.countTestCases():
                    if listSelection:
                        caseList.append(caseName)
                        testList.extend(test.testName() for test in suite)
                    else:
                        sourceTestSuite.addTest(suite)

        if not listSelection:
            testSuite.addTest(sourceTestSuite)

    # Add documentation doctests.
    # NOTE: Test names are not tracked because every test case (representing an
    #       .rst file) has just one test (the whole file's merged doctests).
    if not testNameFilter and (not testSetFilter or "docs" in testSetFilter):
        docsTestSuite = unittest.TestSuite()

        for rst in RST_DIR.iterdir():
            if not rst.suffix == ".rst":
                continue

            caseName = rst.name.lower()

            if not testCaseFilter or caseName in testCaseFilter:
                # NOTE: str() is not required by doctest but by coverage.py.
                suite = doctest.DocFileSuite(str(rst), module_relative=False)

                for test in suite:
                    # HACK: Monkey-patch the test case instance (= single test).
                    test.__class__ = RstTestCase
                    test._caseName = caseName

                if suite.countTestCases():
                    if listSelection:
                        caseList.append(caseName)
                    else:
                        docsTestSuite.addTest(suite)

        if not listSelection:
            testSuite.addTest(docsTestSuite)

    if listSelection:
        return sorted(setList), sorted(caseList), sorted(testList)
    else:
        return testSuite
