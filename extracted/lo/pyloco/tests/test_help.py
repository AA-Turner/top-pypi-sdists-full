"""pyloco help task unittest module
"""

import os
import shutil
import unittest

import pyloco

here, myname = os.path.split(__file__)

text = "Hello World!"

class MyTask(pyloco.Task):
    """sample task for help unittest

This task is a sample task for testing pyloco's help generation feature.

=============
First Section
=============
This is Section 1.

====
Sec2
====
This is Section 2.
"""

    def perform(self, targs):
        """test perform
        """


# Command-line interface
class HelpTaskTests(unittest.TestCase):

    def setUp(self):

        self.tempdir = pyloco.create_tempdir()

    def tearDown(self):

        shutil.rmtree(self.tempdir)

    def test_readme(self):

        readme = os.path.join(self.tempdir, "readme.rst")

        argv = [
            "--format", "readme",
            "--output", readme,
        ]

        forward = {
            "task": MyTask,
        }

        ret, out = pyloco.perform("help", argv=argv, forward=forward)

        self.assertTrue(os.path.isfile(readme))

        os.remove(readme)

test_classes = (HelpTaskTests,)
