"""pyloco unittest module
"""

from __future__ import unicode_literals

import os
import unittest

import pyloco

here, myname = os.path.split(__file__)


class TaskUtilTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_system(self):

        retval, stdout, stderr = pyloco.system("echo %s" % myname)
        self.assertEqual(retval, 0)
        self.assertEqual(stdout.rstrip(), u"%s" % myname)


test_classes = (TaskUtilTests,)
