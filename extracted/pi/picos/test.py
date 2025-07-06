#!/usr/bin/env python3

# ------------------------------------------------------------------------------
# Copyright (C) 2018-2021 Maximilian Stahlberg
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

"""Test runner for PICOS."""

import argparse
import sys
import unittest
from textwrap import TextWrapper

import picos

import tests


def str2dict(string):
    """Read a Python dictionary from a string."""
    import ast
    if string == "_":
        return {}
    dictionary = {}
    pairs = string.split(";")
    for pair in pairs:
        if "=" in pair:
            key, val = pair.split("=", 1)
            dictionary[key] = ast.literal_eval(val)
        else:
            key, val = pair.split(":", 1)
            dictionary[key] = val
    return dictionary


defaultProductionTestOptions = tests.ptest.ProductionTestCase.Options()

parser = argparse.ArgumentParser(description="Test runner for PICOS.")
group = parser.add_mutually_exclusive_group()
group.add_argument("-u", "--unit", action="store_true",
    help="run only unit tests")
group.add_argument("-p", "--production", action="store_true",
    help="run only production tests")
parser.add_argument("-a", "--additional", action="store_true",
    help="run additional slow tests")
parser.add_argument("-v", action="count", dest="testingVerbosity", default=0,
    help="increase testing verbosity, repeatable")
group = parser.add_mutually_exclusive_group()
group.add_argument("-d", action="count", dest="testVerbosity", default=0,
    help="increase test verbosity for debugging, repeatable")
group.add_argument("-q", action="store_const", const=-1, dest="testVerbosity",
    help="suppress test output, including warnings")
parser.add_argument("-l", "--list", action="store_true",
    help="list available filter options")
parser.add_argument("-s", "--solvers", metavar="SOLVER", nargs="+",
    help="select a subset of solvers to test (implies -p)")
parser.add_argument("-t", "--testsets", metavar="SET", nargs="+",
    help="select a subset of test sets to run")
parser.add_argument("-c", "--testcases", metavar="CASE", nargs="+",
    help="select a subset of test cases to run from each set")
parser.add_argument("-n", "--testnames", metavar="TEST", nargs="+",
    help="select a subset of tests to run from each test case")
parser.add_argument("-k", "--known-failures", action="store_true",
    help="run tests that are marked as known failures")
parser.add_argument("-b", "--solveboth", action="store_true",
    help="always ask solver for primal and dual solution")
parser.add_argument("-o", "--options", metavar="SET", nargs="+", type=str2dict,
    default=[{}], help="define a set of solver options to be tested, each given"
    " either as _, the empty set, or as a sequence key1:val1;key2=val2 where "
    "val1 is a string literal and val2 will be evaluated to a Python literal")
group = parser.add_mutually_exclusive_group()
# TODO: Find a working HTML test runner and add it to the group.
group.add_argument("-x", "--xml", action="store_true",
    help="produce XML output via the xmlrunner package")
group = parser.add_mutually_exclusive_group()
group.add_argument("-f", "--forks", metavar="NUM", type=int, default=0,
    help="number of tests to run in parallel via the concurrencytest package, "
    "-1 for number of cpu threads")
group.add_argument("-F", dest="forks", action="store_const", const=-1,
    help="equals -f -1, create number of cpu threads many forks")
parser.add_argument("--objplaces", metavar="NUM", type=int,
    default=defaultProductionTestOptions.objPlaces,
    help="number of decimal places after the point to consider when comparing "
    "objective values")
parser.add_argument("--varplaces", metavar="NUM", type=int,
    default=defaultProductionTestOptions.varPlaces,
    help="number of decimal places after the point to consider when comparing "
    "variable values")

args = parser.parse_args()

# Let -s imply -p.
if args.solvers is None:
    args.solvers = picos.solvers.available_solvers()
else:
    if args.unit:
        parser.error("argument -s implies -p and thus cannot be used with -u")
    args.production = True

if args.list:
    solvers = picos.solvers.available_solvers()
    psets, pcases, ptests = tests.ptest.makeTestSuite(listSelection=True)
    dsets, dcases, dtests = tests.dtest.makeTestSuite(listSelection=True)

    wrapper = TextWrapper(initial_indent=" "*4, subsequent_indent=" "*4)

    print("\n".join([
        "Note:\n",
        "  - Filters are case-insensitive.",
        "  - The 'test' prefix can be ommitted for test names.",
        "  - Some slow test cases are skipped unless selected or -a is passed.",
        "\nProduction testing (-p):",
        "\n  Available solvers (-s):",
        wrapper.fill(", ".join(solvers)),
        "\n  Test sets (-t):",
        wrapper.fill(", ".join(psets)),
        "\n  Test cases (-c):",
        wrapper.fill(", ".join(pcases)),
        "\n  Test names (-n):",
        wrapper.fill(", ".join(ptests)),
        "\nUnit testing (-u):",
        "\n  Doctest sets (-t):",
        wrapper.fill(", ".join(dsets)),
        "\n  Doctest cases (-c):",
        wrapper.fill(", ".join(dcases)),
        "\n  Doctest names (-n):",
        wrapper.fill(", ".join(dtests))
    ]))

    quit()

# Create a suite of all selected tests.
testSuite = unittest.TestSuite()

# Add production tests.
if not args.unit:
    testOptions = tests.ptest.ProductionTestCase.Options()

    testOptions.verbosity = args.testVerbosity
    testOptions.knownFailures = args.known_failures
    testOptions.solveBoth = args.solveboth

    if args.objplaces is not None:
        testOptions.objPlaces = args.objplaces

    if args.varplaces is not None:
        testOptions.varPlaces = args.varplaces

    productionTestSuite = tests.ptest.makeTestSuite(
        testSetFilter=args.testsets,
        testCaseFilter=args.testcases,
        testNameFilter=args.testnames,
        slowTests=args.additional,
        solvers=args.solvers,
        solverOptionSets=args.options,
        testOptions=testOptions)

    testSuite.addTest(productionTestSuite)

# Add unit tests.
if not args.production:
    doctestTestSuite = tests.dtest.makeTestSuite(
        testSetFilter=args.testsets, testCaseFilter=args.testcases,
        testNameFilter=args.testnames)

    testSuite.addTest(doctestTestSuite)

# Decide on a test runner to use.
if args.xml:
    import xmlrunner

    testRunner = xmlrunner.XMLTestRunner(
        output="xml-reports", verbosity=args.testingVerbosity)
else:
    testRunner = unittest.TextTestRunner(verbosity=args.testingVerbosity)

# Parallelize if requested.
if args.forks:
    if args.forks < 0:
        import multiprocessing
        numForks = multiprocessing.cpu_count()
    else:
        numForks = args.forks

    import concurrencytest

    testSuite = concurrencytest.ConcurrentTestSuite(
        testSuite, concurrencytest.fork_for_tests(numForks))

result   = testRunner.run(testSuite)
failures = len(result.failures)
errors   = len(result.errors)
retval   = ((failures > 0) << 0) + ((errors > 0) << 1)

sys.exit(retval)
