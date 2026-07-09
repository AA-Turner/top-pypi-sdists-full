#!/usr/bin/env python3

import doctest
import pkgutil
import sys
import logging
import unittest
import warnings

from argparse import ArgumentParser
from importlib import import_module
from pathlib import Path

import slixmpp

def run_tests(filenames=None, debug=False, log_filename=None, only_doctests=False):
    """
    Find and run all tests in the tests/ directory.

    Excludes live tests (tests/live_*).
    """

    suites = []
    if not only_doctests:
        suites.extend(collect_unit_tests(filenames))
    if filenames is None or only_doctests:
        suites.extend(collect_doctests())

    tests = unittest.TestSuite(suites)
    runner = unittest.TextTestRunner(verbosity=2)

    if log_filename:
        print(f'Storing log output to {log_filename}')
        kwargs = {
            'filename': log_filename,
            'level': logging.INFO,
            'force': True,
        }
        if debug:
            kwargs['level'] = logging.DEBUG
        logging.basicConfig(**kwargs)
    else:
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=100)
            logging.disable(100)

    result = runner.run(tests)
    return result


def collect_unit_tests(filenames):
    if not filenames:
        filenames = [i for i in Path('tests').glob('test_*')]
    else:
        filenames = [Path(i) for i in filenames]

    modules = ['.'.join(test.parts[:-1] + (test.stem,)) for test in filenames]

    suites = []
    for filename in modules:
        module = import_module(filename)
        suites.append(module.suite)
    return suites


def collect_doctests():
    suites = []
    for _importer, modname, _ispkg in pkgutil.walk_packages(
        slixmpp.__path__,
        prefix=slixmpp.__name__ + ".",
    ):
        if "thirdparty" in modname:
            continue
        module = import_module(modname)
        suites.append(doctest.DocTestSuite(module))
    return suites


if __name__ == '__main__':
    warnings.filterwarnings("once", category=DeprecationWarning)

    parser = ArgumentParser(description='Run unit tests.')
    parser.add_argument('tests', metavar='TEST', nargs='*', help='list of tests to run, or nothing to run them all')
    parser.add_argument('-d', '--debug', action='store_true', dest='debug', default=False, help='enable debug output')
    parser.add_argument('-f', '--log-filename', dest='log_filename', default=None, help='File to store slixmpp logs during test execution.')
    parser.add_argument('--only-doctests', action='store_true', help='Only run doctests')
    args = parser.parse_args()

    result = run_tests(args.tests, args.debug, log_filename=args.log_filename, only_doctests=args.only_doctests)
    print("<tests %s ran='%s' errors='%s' fails='%s' success='%s'/>" % (
        "xmlns='http//andyet.net/protocol/tests'",
        result.testsRun, len(result.errors),
        len(result.failures), result.wasSuccessful()))

    sys.exit(not result.wasSuccessful())
