import asyncio
import time
from typing import Dict, List, Any
from orionis.foundation.application import Application
from orionis.services.system.contracts.workers import IWorkers
from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.test.cases.synchronous import SyncTestCase

class TestSynchronousExample(SyncTestCase):
    """
    Synchronous test example demonstrating Orionis framework capabilities.

    This class showcases various testing patterns including dependency injection,
    path resolution, container usage, and error handling in a synchronous context.
    The tests demonstrate best practices for writing maintainable and reliable
    test cases within the Orionis framework.
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

    def testMaxWorkers(self, worker: IWorkers) -> None:
        """
        Test worker service functionality with dependency injection.

        Validates the worker service's ability to calculate the maximum number
        of available workers in the system. This method demonstrates dependency
        injection capabilities with the IWorkers service and ensures proper
        worker count calculation functionality.

        Parameters
        ----------
        worker : IWorkers
            Injected worker service instance for testing worker calculation
            capabilities. The service provides methods for determining optimal
            worker counts based on system resources.

        Returns
        -------
        None
            This test method does not return any value. It performs assertions
            to validate the worker service functionality.

        Tests
        -----
        - Worker service instance validation
        - Worker count calculation functionality
        - Worker count positive value validation
        - Service method execution through dependency injection

        Raises
        ------
        AssertionError
            If worker count calculation fails, returns invalid values, or
            the calculated worker count is not greater than zero.
        """

        # Calculate maximum available workers using the injected service
        max_workers = worker.calculate()

        # Validate that worker count is greater than zero
        self.assertGreater(
            max_workers,
            0,
            "Worker count should be greater than zero"
        )

    def testContainerIntegration(self, container: Application) -> None:
        """
        Test container dependency injection functionality.

        Validates the application container's ability to resolve services and manage
        dependencies correctly. This method demonstrates the dependency injection
        capabilities of the Orionis application container, including service
        registration, resolution, and lifecycle management. The test ensures that
        the container can successfully instantiate and provide service instances
        when requested through the dependency injection mechanism.

        Parameters
        ----------
        container : Application
            Injected application container instance for testing dependency
            injection capabilities. The container manages service resolution,
            dependency lifecycle, and provides access to registered services
            throughout the application.

        Returns
        -------
        None
            This test method does not return any value. It performs assertions
            to validate the container's dependency injection functionality.

        Tests
        -----
        - Container instance validation and null checking
        - Service resolution from container using interface contracts
        - Service functionality validation through container-resolved instances
        - Dependency lifecycle management and proper instantiation
        - Interface-to-implementation mapping verification

        Raises
        ------
        AssertionError
            If container operations fail, services cannot be resolved, or
            the container instance is invalid or None.

        Notes
        -----
        This test validates the core dependency injection functionality that
        is essential for the Orionis framework's service architecture. The
        container must be able to resolve services using their interface
        contracts and provide properly configured instances.
        """

        # Validate that the injected container instance is not None
        # This ensures the dependency injection framework is working correctly
        self.assertIsNotNone(container, "Container instance should not be None")

        # Attempt to resolve the IWorkers service from the container
        # This tests the container's ability to map interfaces to implementations
        workers: IWorkers = container.make(IWorkers)

        # Verify that the service resolution was successful
        # The container should return a valid instance implementing IWorkers
        self.assertIsNotNone(
            workers,
            "Service resolution should return valid instance"
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

    async def testAsyncMaxWorkers(self, worker: IWorkers) -> None:
        """
        Test async worker service functionality with dependency injection.

        Validates async worker operations by simulating async I/O
        operations and testing worker calculation in an asynchronous context.
        This method demonstrates async dependency injection patterns.

        Parameters
        ----------
        worker : IWorkers
            Injected worker service instance for async worker operations.
            This parameter is automatically injected by the async testing framework.

        Tests
        -----
        - Async worker calculation with simulated I/O delay
        - Worker count validation in async context
        - Worker validation in async operations
        - Async service method execution

        Raises
        ------
        AssertionError
            If async worker calculation fails or returns unexpected results.
        """
        async def calculate_workers_async() -> int:
            """
            Simulate async worker calculation with I/O delay.

            Returns
            -------
            int
                Calculated maximum workers count.
            """
            await asyncio.sleep(0.01)  # Simulate async I/O operation
            return worker.calculate()

        # Test async worker calculation
        max_workers = await calculate_workers_async()
        self.assertGreater(
            max_workers,
            0,
            "Async worker calculation should return positive value"
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

        Validates the application container's ability to resolve services and manage
        dependencies in asynchronous contexts. This method demonstrates async dependency
        injection patterns, service resolution capabilities, and validates that the
        container can properly handle service lifecycle management in async environments.
        The test ensures that services resolved through the container maintain their
        functionality when used in asynchronous operations.

        Parameters
        ----------
        container : Application
            Injected application container instance for testing async dependency
            injection capabilities. The container manages service resolution,
            dependency lifecycle, and provides access to registered services
            throughout the async application context.

        Returns
        -------
        None
            This test method does not return any value. It performs assertions
            to validate the container's async dependency injection functionality
            and service resolution capabilities in asynchronous contexts.

        Tests
        -----
        - Async service resolution from container using interface contracts
        - Service instance validation after async resolution
        - Async service method execution and functionality verification
        - Dependency lifecycle management in async contexts
        - Interface-to-implementation mapping in async scenarios

        Raises
        ------
        AssertionError
            If async container operations fail, services cannot be resolved,
            service methods return invalid results, or the container instance
            fails to properly manage async dependencies.

        Notes
        -----
        This test validates the core async dependency injection functionality
        that is essential for the Orionis framework's async service architecture.
        The container must be able to resolve services using their interface
        contracts and provide properly configured instances that work correctly
        in asynchronous execution contexts.
        """
        async def resolve_service_async() -> IWorkers:
            """
            Simulate async service resolution with I/O delay.

            Demonstrates async service resolution from the container while
            simulating real-world async I/O operations that might occur
            during service instantiation or configuration.

            Returns
            -------
            IWorkers
                Resolved worker service instance implementing the IWorkers interface.
            """
            # Simulate async I/O operation that might occur during service resolution
            await asyncio.sleep(0.01)
            # Resolve the IWorkers service from the injected container
            return container.make(IWorkers)

        # Test async service resolution from the container
        # This validates that the container can resolve services in async contexts
        worker_service = await resolve_service_async()

        # Verify that the async service resolution was successful
        # The container should return a valid instance implementing IWorkers
        self.assertIsNotNone(
            worker_service,
            "Async service resolution should return valid instance"
        )

        async def use_service_async() -> int:
            """
            Simulate async service method execution with I/O delay.

            Demonstrates using a resolved service in an async context while
            simulating real-world async operations that might be performed
            by the service methods.

            Returns
            -------
            int
                Result from async service method call representing worker count.
            """
            # Simulate async I/O operation that might occur during service usage
            await asyncio.sleep(0.01)
            # Execute the calculate method on the resolved worker service
            return worker_service.calculate()

        # Test async service method execution after resolution
        # This validates that resolved services function properly in async contexts
        result = await use_service_async()

        # Verify that the async service method execution returns expected results
        # The worker calculation should return a positive integer representing available workers
        self.assertGreater(
            result,
            0,
            "Async service method execution should return positive worker count"
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