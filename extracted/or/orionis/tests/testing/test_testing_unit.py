import unittest
from unittest.mock import MagicMock
from orionis.app import Orionis
from orionis.foundation.config.testing.enums.drivers import PersistentDrivers
from orionis.foundation.config.testing.enums.mode import ExecutionMode
from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.test.core.unit_test import UnitTest

class TestTestingUnit(AsyncTestCase):

    async def testDefaultConfiguration(self) -> None:
        """
        Test that the `UnitTest` class initializes with the correct default configuration values and internal attributes.

        Returns
        -------
        None
        """
        unit_test = UnitTest(Orionis())
        # Assert that the loader is correctly initialized as a TestLoader
        self.assertIsInstance(unit_test._UnitTest__loader, unittest.TestLoader)
        # Assert that the suite is correctly initialized as a TestSuite
        self.assertIsInstance(unit_test._UnitTest__suite, unittest.TestSuite)

    async def testConfigureMethod(self) -> None:
        """
        Test that the `configure` method of `UnitTest` updates internal configuration attributes as expected.

        Returns
        -------
        None
        """
        unit_test = UnitTest(Orionis())
        # Configure the UnitTest instance with custom parameters
        configured = unit_test.configure(
            verbosity=1,
            execution_mode=ExecutionMode.PARALLEL,
            max_workers=4,
            fail_fast=True,
            print_result=False,
            throw_exception=True,
            persistent=False,
            persistent_driver=PersistentDrivers.JSON,
            web_report=False
        )
        # Assert that each internal attribute matches the configured value
        self.assertEqual(unit_test._UnitTest__verbosity, 1)
        self.assertEqual(unit_test._UnitTest__execution_mode, ExecutionMode.PARALLEL.value)
        self.assertEqual(unit_test._UnitTest__max_workers, 4)
        self.assertTrue(unit_test._UnitTest__fail_fast)
        self.assertTrue(unit_test._UnitTest__throw_exception)
        self.assertFalse(unit_test._UnitTest__persistent)
        self.assertEqual(unit_test._UnitTest__persistent_driver, PersistentDrivers.JSON.value)
        self.assertFalse(unit_test._UnitTest__web_report)
        # Ensure the configure method returns the same instance for chaining
        self.assertIs(configured, unit_test)

    async def testFlattenTestSuite(self) -> None:
        """
        Test that the `_flattenTestSuite` method of `UnitTest` flattens nested `TestSuite` instances into a list of test cases.

        Returns
        -------
        None
        """
        unit_test = UnitTest(Orionis())
        # Create mock test cases
        test_case1 = MagicMock()
        test_case2 = MagicMock()
        # Create a nested TestSuite containing the mock test cases
        nested_suite = unittest.TestSuite()
        nested_suite.addTest(test_case1)
        nested_suite.addTest(test_case2)
        # Create the main TestSuite and add the nested suite to it
        main_suite = unittest.TestSuite()
        main_suite.addTest(nested_suite)
        # Flatten the main suite using the method under test
        flattened = unit_test._UnitTest__flattenTestSuite(main_suite)
        # Assert that the flattened list contains both test cases
        self.assertEqual(len(flattened), 2)
        self.assertIn(test_case1, flattened)
        self.assertIn(test_case2, flattened)

    async def testMergeTestResults(self) -> None:
        """
        Test that the `_mergeTestResults` method of `UnitTest` correctly aggregates results from an individual `TestResult` into a combined `TestResult`.

        Returns
        -------
        None
        """
        unit_test = UnitTest(Orionis())
        # Create a combined TestResult to aggregate results into
        combined = unittest.TestResult()
        # Create an individual TestResult with sample data
        individual = unittest.TestResult()
        individual.testsRun = 2
        individual.failures = [('test1', 'failure')]
        individual.errors = [('test2', 'error')]
        individual.skipped = []
        individual.expectedFailures = []
        individual.unexpectedSuccesses = []
        # Merge the individual results into the combined result
        unit_test._UnitTest__mergeTestResults(combined, individual)
        # Assert that the combined result reflects the merged data
        self.assertEqual(combined.testsRun, 2)
        self.assertEqual(len(combined.failures), 1)
        self.assertEqual(len(combined.errors), 1)

    async def testClearTests(self) -> None:
        """
        Test that the `clearTests` method of `UnitTest` resets the test suite, removing all test cases.

        Returns
        -------
        None
        """
        unit_test = UnitTest(Orionis())
        # Add a mock test case to the suite
        mock_test = MagicMock()
        unit_test._UnitTest__suite.addTest(mock_test)
        # Clear all tests from the suite
        unit_test.clearTests()
        # Assert that the suite is now empty
        self.assertEqual(len(unit_test._UnitTest__suite._tests), 0)

    async def testGetTestNames(self) -> None:
        """
        Test that the `getTestNames` method of `UnitTest` returns a list of identifiers for all test cases in the suite.

        Returns
        -------
        None
        """
        unit_test = UnitTest(Orionis())
        # Create a mock test case and set its id() method to return a specific identifier
        mock_test = MagicMock()
        mock_test.id.return_value = 'test_id'
        # Add the mock test case to the UnitTest's internal suite
        unit_test._UnitTest__suite.addTest(mock_test)
        # Retrieve the list of test names using the method under test
        names = unit_test.getTestNames()
        # Assert that the returned list contains the expected test identifier
        self.assertEqual(names, ['test_id'])

    async def testGetTestCount(self) -> None:
        """
        Test that the `getTestCount` method of `UnitTest` returns the correct number of test cases in the suite.

        Returns
        -------
        None
        """
        unit_test = UnitTest(Orionis())
        # Create two mock test cases
        mock_test1 = MagicMock()
        mock_test2 = MagicMock()
        # Add the mock test cases to the UnitTest's internal suite
        unit_test._UnitTest__suite.addTest(mock_test1)
        unit_test._UnitTest__suite.addTest(mock_test2)
        # Retrieve the count of test cases using the method under test
        count = unit_test.getTestCount()
        # Assert that the returned count matches the number of test cases added
        self.assertEqual(count, 2)
