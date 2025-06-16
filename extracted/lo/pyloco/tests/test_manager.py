"""pyloco unittest module
"""

import os
import unittest

import pyloco

here, myname = os.path.split(__file__)

text = "Hello World!"


class MyManager(pyloco.Manager):
    _name_ = "testmanager"

# Command-line interface
class TaskManagerTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_custommanager(self):

        ret, out = pyloco.perform("print", "1 -n --debug", manager=MyManager)

        self.assertEqual(ret, 0)
        self.assertTrue(isinstance(out, dict))
        self.assertIn("stdout", out)
        self.assertEqual(out["stdout"], '1')


test_classes = (TaskManagerTests,)
