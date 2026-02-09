#!/usr/bin/env python3

import sys
import logging
import unittest
import warnings

from argparse import ArgumentParser
from importlib import import_module
from pathlib import Path


def run_tests(filenames=None, debug=False, log_filename=None):
    """
    Find and run all tests in the tests/ directory.

    Excludes live tests (tests/live_*).
    """
    if not filenames:
        filenames = [i for i in Path('itests').glob('test_*')]
    else:
        filenames = [Path(i) for i in filenames]

    modules = ['.'.join(test.parts[:-1] + (test.stem,)) for test in filenames]

    suites = []
    for filename in modules:
        module = import_module(filename)
        suites.append(module.suite)

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


if __name__ == '__main__':
    warnings.filterwarnings("once", category=DeprecationWarning)

    parser = ArgumentParser(description='Run integration unit tests.')
    parser.add_argument('tests', metavar='TEST', nargs='*', help='list of tests to run, or nothing to run them all')
    parser.add_argument('-d', '--debug', action='store_true', dest='debug', default=False, help='enable debug output')
    parser.add_argument('-f', '--log-filename', dest='log_filename', default=None, help='File to store slixmpp logs during test execution.')
    args = parser.parse_args()

    result = run_tests(args.tests, args.debug, log_filename=args.log_filename)
    print("<tests %s ran='%s' errors='%s' fails='%s' success='%s'/>" % (
        "xmlns='http//andyet.net/protocol/tests'",
        result.testsRun, len(result.errors),
        len(result.failures), result.wasSuccessful()))

    sys.exit(not result.wasSuccessful())
