# Copyright (C) 2002-2006 Python Software Foundation

"""A simple test runner, which sets up sys.path properly.

Usage: python test.py [options]
Options:

    --help / -h
        Print this message and exit.

    -v
        This is passed on to unittest.
"""

import sys
import unittest
import getopt

from email.test import test_email
from email.test import test_email_renamed

from test.test_support import TestSkipped
try:
    from email.test import test_email_torture
except TestSkipped:
    test_email_torture = None

# See if we have the Japanese codecs package installed
try:
    from email.test import test_email_codecs
    from email.test import test_email_codecs_renamed
except TestSkipped:
    test_email_codecs = None



def suite():
    suite = unittest.TestSuite()
    suite.addTest(test_email.suite())
    suite.addTest(test_email_renamed.suite())
    if test_email_codecs is not None:
        suite.addTest(test_email_codecs.suite())
        suite.addTest(test_email_codecs_renamed.suite())
    if test_email_torture is not None:
        suite.addTest(test_email_torture.suite())
    return suite



def usage(code, msg=''):
    print >> sys.stderr, __doc__
    if msg:
        print >> sys.stderr, msg
    sys.exit(code)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hv', ['help'])
    except getopt.error, msg:
        usage(1, msg)

    if args:
        usage(1)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage(0)
        # No -v test since that's passed along to unittest

    unittest.main(defaultTest='suite')



if __name__ == '__main__':
    main()
