#! /usr/bin/python3

import sys
import unittest
import doctest
import DNS
from DNS.tests import test_suite

result = unittest.TextTestRunner().run(test_suite())
if result.wasSuccessful():
    print("Test run successful.", file=sys.stderr)
    sys.exit(0)
print("Test run failed.", file=sys.stderr)
sys.exit(1)
