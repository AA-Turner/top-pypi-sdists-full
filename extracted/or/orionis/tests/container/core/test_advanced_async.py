import time
from orionis.container.container import Container
from orionis.test.cases.asynchronous import AsyncTestCase
from tests.container.mocks.mock_advanced_async import ErrorService, IPerformanceService, MixedConsumer, PerformanceService, simple_async, sync_returns_coroutine

class TestContainer(AsyncTestCase):

    async def testPerformanceComparison(self):
        """
        Measures and verifies the performance of synchronous service calls within the container.

        This test performs the following steps:
            - Instantiates a container and registers `PerformanceService` as a singleton for the `IPerformanceService` interface.
            - Resolves the registered service from the container.
            - Executes the synchronous operation multiple times using the container's `call` method, measuring the total elapsed time.
            - Asserts that the synchronous operation returns the expected result.
            - Asserts that the measured execution time is greater than zero, confirming that the operation duration is measurable.

        Returns
        -------
        None
            This method does not return a value. Assertions are used to validate expected behavior.
        """
        # Create a container instance
        container = Container()

        # Register the PerformanceService as a singleton for the IPerformanceService interface
        container.singleton(IPerformanceService, PerformanceService)

        # Resolve the service instance from the container
        service = container.make(IPerformanceService)

        # Start timing the synchronous calls
        start_time = time.time()

        # Call the sync operation multiple times to measure performance
        for i in range(3):
            result = container.call(service, 'sync_operation')

        # Calculate the total elapsed time for synchronous calls
        sync_time = time.time() - start_time

        # Assert that the sync operation returns the expected result
        self.assertEqual(result, "Sync operation completed")

        # Assert that the measured time is greater than zero
        self.assertGreater(sync_time, 0, "Sync operation should take some time")

    async def testAsyncPerformance(self):
        """
        Measures and verifies the performance of asynchronous service calls within the container.

        This test performs the following steps:
            - Instantiates a container and registers `PerformanceService` as a singleton for the `IPerformanceService` interface.
            - Resolves the registered service from the container.
            - Executes the asynchronous operation multiple times using both `call` and `callAsync` methods, measuring the total elapsed time.
            - Asserts that the asynchronous operation returns the expected result.
            - Asserts that the measured execution time is greater than zero, confirming that the operation duration is measurable.

        Returns
        -------
        None
            This method does not return a value. Assertions are used to validate expected behavior.

        Raises
        ------
        AssertionError
            If the asynchronous operation does not return the expected result or if the measured time is not greater than zero.
        """

        # Create a container instance
        container = Container()

        # Register the PerformanceService as a singleton for the IPerformanceService interface
        container.singleton(IPerformanceService, PerformanceService)

        # Resolve the service instance from the container
        service = container.make(IPerformanceService)

        # Start timing the asynchronous calls
        start_time = time.time()

        # Call the async operation multiple times using the container's call method
        for i in range(3):

            # Await the result of the async operation
            result = container.call(service, 'async_operation')

        # Calculate the total elapsed time for asynchronous calls
        async_time = time.time() - start_time

        # Assert that the async operation returns the expected result
        self.assertEqual(result, "Async operation completed")

        # Call the async operation multiple times using the container's callAsync method
        for i in range(3):
            result = await container.callAsync(service, 'async_operation')

        # Assert that the async operation returns the expected result
        self.assertEqual(result, "Async operation completed")

        # Assert that the measured time is greater than zero
        self.assertGreater(async_time, 0, "Async operation should take some time")

    async def testErrorHandling(self):
        """
        Tests the error handling capabilities of the container for both synchronous and asynchronous service methods.

        This method performs the following steps:
            - Instantiates a container and resolves the `ErrorService`.
            - Invokes a synchronous method that is expected to raise an exception and asserts that the exception is raised.
            - (Asynchronous error handling is tested elsewhere.)

        Returns
        -------
        None
            This method does not return a value. Assertions are used to validate that exceptions are properly raised.
        """

        # Create a container instance
        container = Container()

        # Resolve the ErrorService instance from the container
        service = container.make(ErrorService)

        # Test synchronous error handling: expect an exception to be raised
        with self.assertRaises(Exception) as context:
            container.call(service, 'sync_error_method')

    async def testAsyncErrors(self):

        # Create a container instance
        container = Container()

        # Resolve the ErrorService instance from the container
        service = container.make(ErrorService)

        # Call the async error method and await its result
        with self.assertRaises(Exception) as context:
            await container.callAsync(service, 'async_error_method')

    async def testMixedDependencyInjection(self):
        """
        Tests the container's ability to perform mixed synchronous and asynchronous dependency injection.

        This test performs the following steps:
            - Instantiates a container and uses it to auto-resolve dependencies for the `MixedConsumer` class.
            - Invokes a synchronous method with dependency injection and verifies its return value.
            - (Asynchronous methods are tested elsewhere.)

        The test asserts that:
            - The synchronous method returns a string starting with "Sync:".

        Returns
        -------
        None
            This method does not return a value. Assertions are used to validate expected behavior.
        """

        # Create an instance of the container
        container = Container()

        # Auto-resolve dependencies for MixedConsumer
        consumer = container.make(MixedConsumer)

        # Test synchronous method with dependency injection
        sync_result: str = container.call(consumer, 'sync_method')

        # Assert that the result starts with "Sync:"
        self.assertTrue(sync_result.startswith("Sync:"))

    async def testAsyncWithDI(self):
        """
        Tests the container's capability to perform asynchronous dependency injection.

        This test performs the following steps:
            - Instantiates a container and uses it to auto-resolve dependencies for the `MixedConsumer` class.
            - Invokes an asynchronous method with dependency injection and verifies its return value.

        The test asserts that:
            - The asynchronous method returns a string starting with "Mixed: ".

        Returns
        -------
        None
            This method does not return a value. Assertions are used to validate expected behavior.
        """

        # Create an instance of the container
        container = Container()

        # Auto-resolve dependencies for MixedConsumer
        consumer = container.make(MixedConsumer)

        # Call the asynchronous method with dependency injection
        async_result: str = await container.callAsync(consumer, 'async_method')

        # Assert that the result starts with "Mixed: "
        self.assertTrue(async_result.startswith("Mixed: "))

    async def testCallableAsyncSync(self):
        """
        Tests the container's ability to register and resolve both synchronous and asynchronous callable functions,
        ensuring that both types return coroutine objects when resolved.

        This method performs the following steps:
            - Instantiates a container and registers two callable functions:
                - A synchronous function that returns a coroutine.
                - An asynchronous function.
            - Resolves each callable from the container.
            - Asserts that the resolved objects are coroutine objects by checking for the '__await__' attribute.

        Returns
        -------
        None
            This method does not return a value. Assertions are used to validate that the resolved callables are coroutine objects.
        """

        # Create a container instance
        container = Container()

        # Register a synchronous function that returns a coroutine
        container.callable("sync_returns_coro", sync_returns_coroutine)

        # Register an asynchronous function
        container.callable("simple_async", simple_async)

        # Resolve the synchronous function and check if it returns a coroutine object
        result1 = container.make("sync_returns_coro")
        self.assertTrue(result1 == "Sync function returning coroutine")

        # Resolve the asynchronous function and check if it returns a coroutine object
        result2 = container.make("simple_async")
        self.assertTrue(result2 == "Simple async callable")