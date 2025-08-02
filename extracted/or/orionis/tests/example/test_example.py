"""
Orionis Framework Test Examples
===============================

This module contains comprehensive test examples demonstrating the capabilities
of the Orionis testing framework, including both synchronous and asynchronous
testing patterns with dependency injection.

Examples:
--------
    Run synchronous tests:
        >>> from tests.example.test_example import TestSynchronousExample
        >>> test = TestSynchronousExample()
        >>> test.setUp()
        >>> test.testBasicAssertions()

    Run asynchronous tests:
        >>> from tests.example.test_example import TestAsynchronousExample
        >>> test = TestAsynchronousExample()
        >>> await test.asyncSetUp()
        >>> await test.testAsyncBasicOperations()

Notes:
-----
    These examples showcase:
    - Dependency injection patterns
    - Path resolution services
    - Container integration
    - Error handling strategies
    - Data validation techniques
    - Concurrent operations
    - Async/await patterns
"""

import asyncio
import time
from typing import Dict, List, Any
from orionis.foundation.application import Application
from orionis.services.paths.contracts.resolver import IResolver
from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.test.cases.synchronous import SyncTestCase

class TestSynchronousExample(SyncTestCase):
    """
    Synchronous test example demonstrating Orionis framework capabilities.

    This class showcases various testing patterns including dependency injection,
    path resolution, container usage, and error handling in a synchronous context.
    The tests demonstrate best practices for writing maintainable and reliable
    test cases within the Orionis framework.

    Attributes
    ----------
    test_data : Dict[str, Any]
        Test data dictionary containing sample files and expected values
        for use across multiple test methods.

    Methods
    -------
    setUp()
        Initialize test environment before each test method execution.
    tearDown()
        Clean up resources after each test method completion.
    testBasicAssertions()
        Validate basic assertion functionality and patterns.
    testPathResolution(paths)
        Test path resolution service functionality with dependency injection.
    testContainerIntegration(container)
        Validate container dependency injection capabilities.
    testErrorHandling()
        Test error handling and exception management patterns.
    testDataValidation()
        Validate data validation and complex assertion patterns.

    Examples
    --------
    Basic usage:
        >>> test = TestSynchronousExample()
        >>> test.setUp()
        >>> test.testBasicAssertions()
        >>> test.tearDown()

    With dependency injection:
        >>> test = TestSynchronousExample()
        >>> test.setUp()
        >>> # Path resolver will be injected automatically
        >>> test.testPathResolution(resolver_instance)
        >>> test.tearDown()
    """

    def setUp(self) -> None:
        """
        Set up test environment before each test method.

        Initializes test data dictionary with sample files and expected values
        that will be used across multiple test methods. This method is called
        automatically before each test method execution.

        Notes
        -----
        The test_data dictionary contains:
        - sample_file: Path to the current test file for path resolution tests
        - expected_values: List of integers used in assertion validation tests
        """
        self.test_data: Dict[str, Any] = {
            "sample_file": "tests/example/test_example.py",
            "expected_values": [1, 2, 3, 4, 5]
        }

    def tearDown(self) -> None:
        """
        Clean up resources after each test method completion.

        Resets the test_data attribute to None to ensure clean state
        between test method executions and prevent memory leaks.
        """
        self.test_data = None

    def testBasicAssertions(self) -> None:
        """
        Test basic assertion functionality and patterns.

        Validates the fundamental assertion methods provided by the testing
        framework, including equality checks, boolean assertions, and
        container membership validation.

        Tests
        -----
        - Equality assertions (assertEqual)
        - Boolean assertions (assertTrue, assertFalse)
        - Container membership (assertIn, assertNotIn)

        Raises
        ------
        AssertionError
            If any of the basic assertions fail, indicating a problem
            with the testing framework's assertion mechanisms.
        """
        # Test equality assertions
        self.assertEqual(2, 2, "Basic equality check failed")
        self.assertEqual(3, 3, "Second equality check failed")

        # Test boolean assertions
        self.assertTrue(True, "Boolean true assertion failed")
        self.assertFalse(False, "Boolean false assertion failed")

        # Test container assertions
        self.assertIn(
            3,
            self.test_data["expected_values"],
            "Value not found in container"
        )
        self.assertNotIn(
            10,
            self.test_data["expected_values"],
            "Unexpected value found in container"
        )

    def testPathResolution(self, paths: IResolver) -> None:
        """
        Test path resolution service functionality with dependency injection.

        Validates the path resolution service by testing relative path creation
        and string conversion operations. This method demonstrates how dependency
        injection works within the Orionis testing framework.

        Parameters
        ----------
        paths : IResolver
            Injected path resolver service instance for testing path operations.
            This parameter is automatically injected by the testing framework
            based on the type annotation.

        Tests
        -----
        - Relative path creation from string path
        - Path string conversion and format validation
        - Path ending validation
        - Path content validation

        Raises
        ------
        AssertionError
            If path resolution fails or returns unexpected results.
        """
        # Test relative path resolution
        relative_path = paths.relativePath(self.test_data["sample_file"])
        path_string = relative_path.toString()

        # Verify path resolution results
        self.assertTrue(
            path_string.endswith("test_example.py"),
            "Path should end with test_example.py"
        )
        self.assertIn(
            "test_example.py",
            path_string,
            "Path should contain expected directory structure"
        )

    def testContainerIntegration(self, container: Application) -> None:
        """
        Test container dependency injection functionality.

        Validates the container's ability to resolve services and manage
        dependencies. This method demonstrates the dependency injection
        capabilities of the Orionis application container.

        Parameters
        ----------
        container : Application
            Injected application container instance for testing dependency
            injection capabilities. The container manages service resolution
            and dependency lifecycle.

        Tests
        -----
        - Container instance validation
        - Service resolution from container
        - Service functionality validation through container
        - Dependency lifecycle management

        Raises
        ------
        AssertionError
            If container operations fail or services cannot be resolved.
        """
        # Test container instance validation
        self.assertIsNotNone(container, "Container instance should not be None")

        # Test service resolution from container
        path_resolver: IResolver = container.make(IResolver)
        self.assertIsNotNone(
            path_resolver,
            "Service resolution should return valid instance"
        )

        # Test service functionality through container
        test_path = path_resolver.relativePath("README.md")
        self.assertIsNotNone(
            test_path,
            "Service method execution should return valid result"
        )

    def testErrorHandling(self) -> None:
        """
        Test error handling and exception management patterns.

        Validates the framework's ability to handle expected exceptions
        and provides examples of proper exception testing patterns.
        This method demonstrates both basic exception catching and
        regex-based exception message validation.

        Tests
        -----
        - Basic exception assertion with assertRaises
        - Exception message pattern matching with assertRaisesRegex
        - Proper exception type validation
        - Exception context management

        Raises
        ------
        AssertionError
            If expected exceptions are not raised or have incorrect types.
        """
        # Test basic exception assertion
        with self.assertRaises(ValueError):
            raise ValueError("Expected test exception")

        # Test exception message pattern matching
        with self.assertRaisesRegex(RuntimeError, r"test.*pattern"):
            raise RuntimeError("test error pattern match")

    def testDataValidation(self) -> None:
        """
        Test data validation and complex assertion patterns.

        Validates complex data structures and demonstrates advanced assertion
        techniques including list comparisons, dictionary operations, and
        length validation. This method showcases best practices for testing
        data integrity and structure validation.

        Tests
        -----
        - List length validation
        - List content comparison with assertListEqual
        - Dictionary key existence validation
        - Dictionary value validation
        - Complex data structure assertions

        Raises
        ------
        AssertionError
            If data validation fails or structures don't match expectations.
        """
        # Test list operations and validation
        test_list = [1, 2, 3, 4, 5]
        self.assertEqual(
            len(test_list),
            5,
            "List length should match expected value"
        )
        self.assertListEqual(
            test_list,
            self.test_data["expected_values"],
            "List content should match expected values"
        )

        # Test dictionary operations and validation
        test_dict = {"key1": "value1", "key2": "value2"}
        self.assertIn(
            "key1",
            test_dict,
            "Dictionary should contain expected key"
        )
        self.assertEqual(
            test_dict["key1"],
            "value1",
            "Dictionary value should match expected value"
        )

class TestAsynchronousExample(AsyncTestCase):
    """
    Asynchronous test example demonstrating async capabilities in Orionis framework.

    This class showcases asynchronous testing patterns including async dependency
    injection, concurrent operations, timing validation, and async error handling.
    The tests demonstrate best practices for writing async test cases that are
    both performant and reliable.

    Attributes
    ----------
    async_data : Dict[str, Any]
        Asynchronous test data dictionary containing timing parameters,
        task configuration, and expected results for async operations.

    Methods
    -------
    asyncSetUp()
        Initialize async test environment before each test method.
    asyncTearDown()
        Clean up async resources after each test method completion.
    testAsyncBasicOperations()
        Test basic async operations including timing and sleep validation.
    testAsyncPathResolution(paths)
        Test async path resolution with dependency injection.
    testConcurrentOperations()
        Test concurrent async operations and task management.
    testAsyncErrorHandling()
        Test async error handling and timeout management.
    testAsyncContainerIntegration(container)
        Test async container dependency injection functionality.
    testAsyncDataProcessing()
        Test async data processing and validation patterns.

    Examples
    --------
    Basic async usage:
        >>> test = TestAsynchronousExample()
        >>> await test.asyncSetUp()
        >>> await test.testAsyncBasicOperations()
        >>> await test.asyncTearDown()

    Concurrent operations:
        >>> test = TestAsynchronousExample()
        >>> await test.asyncSetUp()
        >>> await test.testConcurrentOperations()
        >>> await test.asyncTearDown()
    """

    async def asyncSetUp(self) -> None:
        """
        Set up async test environment before each test method.

        Initializes async test data dictionary with timing parameters,
        concurrent task configuration, and expected results for async
        operations. This method is called automatically before each
        async test method execution.

        Notes
        -----
        The async_data dictionary contains:
        - delay_time: Standard delay time for async operations testing
        - concurrent_tasks: Number of concurrent tasks for testing
        - expected_results: Expected results from concurrent operations
        """
        self.async_data: Dict[str, Any] = {
            "delay_time": 0.1,
            "concurrent_tasks": 3,
            "expected_results": ["result1", "result2", "result3"]
        }

    async def asyncTearDown(self) -> None:
        """
        Clean up async resources after each test method completion.

        Resets the async_data attribute to None to ensure clean state
        between async test method executions and prevent memory leaks.
        """
        self.async_data = None

    async def testAsyncBasicOperations(self) -> None:
        """
        Test basic async operations including timing and sleep validation.

        Validates the framework's ability to handle async operations
        correctly, including timing precision and sleep duration validation.
        This method demonstrates proper async timing testing patterns.

        Tests
        -----
        - Async sleep duration validation
        - Timing precision testing
        - Async operation timing boundaries
        - Time measurement accuracy

        Raises
        ------
        AssertionError
            If async timing operations don't meet expected constraints.
        """
        # Test async sleep and timing precision
        start_time = time.time()
        await asyncio.sleep(self.async_data["delay_time"])
        end_time = time.time()

        elapsed = end_time - start_time
        self.assertGreaterEqual(
            elapsed,
            self.async_data["delay_time"],
            "Async sleep duration should meet minimum time requirement"
        )
        self.assertLess(
            elapsed,
            self.async_data["delay_time"] + 0.05,
            "Async sleep duration should not exceed maximum time tolerance"
        )

    async def testAsyncPathResolution(self, paths: IResolver) -> None:
        """
        Test async path resolution service functionality with dependency injection.

        Validates async path resolution operations by simulating async I/O
        operations and testing path resolution in an asynchronous context.
        This method demonstrates async dependency injection patterns.

        Parameters
        ----------
        paths : IResolver
            Injected path resolver service instance for async path operations.
            This parameter is automatically injected by the async testing framework.

        Tests
        -----
        - Async path resolution with simulated I/O delay
        - Path string conversion in async context
        - Path validation in async operations
        - Async service method execution

        Raises
        ------
        AssertionError
            If async path resolution fails or returns unexpected results.
        """
        async def resolve_path_async(path_name: str) -> str:
            """
            Simulate async path resolution with I/O delay.

            Parameters
            ----------
            path_name : str
                Path name to resolve asynchronously.

            Returns
            -------
            str
                Resolved path as string.
            """
            await asyncio.sleep(0.01)  # Simulate async I/O operation
            return paths.relativePath(path_name).toString()

        # Test async path resolution
        resolved_path = await resolve_path_async("tests/example/test_example.py")
        self.assertTrue(
            resolved_path.endswith("test_example.py"),
            "Async path resolution should return correct file ending"
        )

    async def testConcurrentOperations(self) -> None:
        """
        Test concurrent async operations and task management.

        Validates the framework's ability to handle multiple concurrent
        async operations correctly, including task creation, execution,
        and result aggregation. This method demonstrates proper concurrent
        async testing patterns.

        Tests
        -----
        - Concurrent task creation and execution
        - Task result aggregation with asyncio.gather
        - Concurrent operation result validation
        - Task count and result verification

        Raises
        ------
        AssertionError
            If concurrent operations fail or results don't match expectations.
        """
        async def async_task(task_id: int) -> str:
            """
            Simulate async task with unique result.

            Parameters
            ----------
            task_id : int
                Unique identifier for the async task.

            Returns
            -------
            str
                Task result string with task ID.
            """
            await asyncio.sleep(0.05)
            return f"result{task_id}"

        # Create concurrent tasks
        tasks = [
            async_task(i)
            for i in range(1, self.async_data["concurrent_tasks"] + 1)
        ]

        # Execute tasks concurrently
        results = await asyncio.gather(*tasks)

        # Verify concurrent operation results
        self.assertEqual(
            len(results),
            self.async_data["concurrent_tasks"],
            "Concurrent task count should match expected value"
        )
        self.assertListEqual(
            results,
            self.async_data["expected_results"],
            "Concurrent task results should match expected values"
        )

    async def testAsyncErrorHandling(self) -> None:
        """
        Test async error handling and timeout management.

        Validates the framework's ability to handle async exceptions
        and timeout scenarios correctly. This method demonstrates proper
        async error handling patterns including exception catching and
        timeout management.

        Tests
        -----
        - Async exception assertion with assertRaises
        - Async timeout handling with asyncio.wait_for
        - Async exception type validation
        - Async context manager exception handling

        Raises
        ------
        AssertionError
            If async error handling doesn't work as expected.
        """
        async def failing_async_function() -> None:
            """
            Simulate async function that raises an exception.

            Raises
            ------
            ValueError
                Always raises ValueError for testing purposes.
            """
            await asyncio.sleep(0.01)
            raise ValueError("Async test exception")

        # Test async exception assertion
        with self.assertRaises(ValueError):
            await failing_async_function()

        async def slow_async_function() -> str:
            """
            Simulate slow async function for timeout testing.

            Returns
            -------
            str
                Result string after long delay.
            """
            await asyncio.sleep(1.0)
            return "slow result"

        # Test async timeout handling
        with self.assertRaises(asyncio.TimeoutError):
            await asyncio.wait_for(slow_async_function(), timeout=0.1)

    async def testAsyncContainerIntegration(self, container: Application) -> None:
        """
        Test async container dependency injection functionality.

        Validates the container's ability to resolve services in async
        contexts and manage async dependencies. This method demonstrates
        async dependency injection patterns and service resolution.

        Parameters
        ----------
        container : Application
            Injected application container instance for testing async
            dependency injection capabilities.

        Tests
        -----
        - Async service resolution from container
        - Async service method execution
        - Async dependency lifecycle management
        - Async service functionality validation

        Raises
        ------
        AssertionError
            If async container operations fail or services cannot be resolved.
        """
        async def resolve_service_async() -> IResolver:
            """
            Simulate async service resolution.

            Returns
            -------
            IResolver
                Resolved path resolver service instance.
            """
            await asyncio.sleep(0.01)
            return container.make(IResolver)

        # Test async service resolution
        path_resolver = await resolve_service_async()
        self.assertIsNotNone(
            path_resolver,
            "Async service resolution should return valid instance"
        )

        async def use_service_async() -> str:
            """
            Simulate async service method execution.

            Returns
            -------
            str
                Result from async service method call.
            """
            await asyncio.sleep(0.01)
            return path_resolver.relativePath("README.md").toString()

        # Test async service method execution
        result = await use_service_async()
        self.assertTrue(
            result.endswith("README.md"),
            "Async service method execution should return correct result"
        )

    async def testAsyncDataProcessing(self) -> None:
        """
        Test async data processing and validation patterns.

        Validates async data transformation, processing, and validation
        operations. This method demonstrates proper async data handling
        patterns and validation techniques.

        Tests
        -----
        - Async data transformation operations
        - Async data validation with type checking
        - Async list processing and comparison
        - Async data integrity validation

        Raises
        ------
        AssertionError
            If async data processing fails or results don't match expectations.
        """
        async def process_data_async(data: List[int]) -> List[int]:
            """
            Simulate async data processing with transformation.

            Parameters
            ----------
            data : List[int]
                Input data list for processing.

            Returns
            -------
            List[int]
                Processed data list with transformed values.
            """
            await asyncio.sleep(0.01)
            return [item * 2 for item in data]

        # Test async data transformation
        input_data = [1, 2, 3, 4, 5]
        processed_data = await process_data_async(input_data)
        expected_data = [2, 4, 6, 8, 10]

        self.assertListEqual(
            processed_data,
            expected_data,
            "Async data processing should transform values correctly"
        )

        async def validate_data_async(data: List[int]) -> bool:
            """
            Simulate async data validation.

            Parameters
            ----------
            data : List[int]
                Data list to validate.

            Returns
            -------
            bool
                True if all items are integers, False otherwise.
            """
            await asyncio.sleep(0.01)
            return all(isinstance(item, int) for item in data)

        # Test async data validation
        is_valid = await validate_data_async(processed_data)
        self.assertTrue(
            is_valid,
            "Async data validation should confirm data integrity"
        )