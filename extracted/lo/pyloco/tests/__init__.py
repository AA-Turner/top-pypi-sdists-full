import unittest

from pyloco.test import TestSuite

from .test_help import test_classes as task_helps
from .test_manager import test_classes as task_managers
from .test_basics import test_classes as task_basics
from .test_utils import test_classes as task_utils


def pyloco_unittest_suite():

    loader = unittest.TestLoader()
    #suite = unittest.TestSuite()
    suite = TestSuite()

    #all_tests = task_helps

    all_tests = (task_utils + task_basics + task_managers +
                 task_helps)

    for test_class in all_tests:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    return suite
