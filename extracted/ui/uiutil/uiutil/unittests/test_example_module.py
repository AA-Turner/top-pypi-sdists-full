# encoding: utf-8

import unittest
import uiutil
from uiutil import _metadata

__author__ = u'Oli Davis'
__copyright__ = u'Copyright (C) 2016 Oli Davis'


class TestConfiguration(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # Instantiation
    def test_version(self):
        self.assertEqual(uiutil.__version__, _metadata.__version__, u'Version is incorrect')


if __name__ == u'__main__':
    unittest.main()
