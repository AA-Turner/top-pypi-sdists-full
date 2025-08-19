from orionis.container.container import Container
from orionis.test.cases.asynchronous import AsyncTestCase
from tests.container.mocks.mock_async_optimizations import AsyncTestService, AsyncTestServiceWithDependency, IAsyncTestService, IAsyncTestServiceWithDependency, ITestService, ITestServiceWithDependency, MixedService, TestService, TestServiceWithDependency, async_callable, async_callable_with_dependency, sync_callable, sync_callable_with_dependency

class TestContainer(AsyncTestCase):

    async def testSyncServices(self):
        """
        Tests the registration and resolution of synchronous services in the container.

        This method verifies that singleton and transient services can be registered and resolved correctly.
        It checks that the singleton service returns the same instance on multiple resolutions, and that
        the service with a dependency is properly constructed.

        Returns
        -------
        None
            This method does not return a value. Assertions are used to validate behavior.
        """

        # Create a new container instance
        container = Container()

        # Register a singleton service and a transient service with dependency
        container.singleton(ITestService, TestService)
        container.transient(ITestServiceWithDependency, TestServiceWithDependency)

        # Resolve the singleton service and verify its method output
        service: ITestService = container.make(ITestService)
        self.assertEqual(service.get_message(), "Hello from sync service")

        # Resolve the transient service with dependency and check its output
        service_with_dep: ITestServiceWithDependency = container.make(ITestServiceWithDependency)
        self.assertTrue(service_with_dep.get_combined_message().startswith("Combined: "))

        # Ensure that singleton returns the same instance on multiple resolutions
        service2: ITestService = container.make(ITestService)
        self.assertIs(service, service2, "Singleton service should return the same instance")

    async def testAsyncServices(self):
        """
        Tests the registration and resolution of asynchronous services in the dependency injection container.

        This method ensures that asynchronous services can be registered as singletons or transients and resolved correctly.
        It verifies that the resolved service instance matches the expected implementation type.

        Parameters
        ----------
        self : TestContainer
            The test case instance.

        Returns
        -------
        None
            This method does not return a value. Assertions are used to validate correct behavior.
        """

        # Create a new container instance
        container = Container()

        # Register an asynchronous singleton service
        container.singleton(IAsyncTestService, AsyncTestService)

        # Register an asynchronous transient service with dependency
        container.transient(IAsyncTestServiceWithDependency, AsyncTestServiceWithDependency)

        # Resolve the asynchronous singleton service and check its type
        async_service = container.make(IAsyncTestService)
        self.assertIsInstance(async_service, AsyncTestService)

    async def testAsyncCalls(self):
        """
        Tests asynchronous service resolution and asynchronous method invocation in the dependency injection container.

        This method verifies that asynchronous services can be registered, resolved, and their asynchronous methods invoked correctly.
        It checks both singleton and transient registrations, and asserts that the returned values are as expected.

        Parameters
        ----------
        self : TestContainer
            The test case instance.

        Returns
        -------
        None
            This method does not return a value. Assertions are used to validate correct behavior.
        """

        # Create a new container instance
        container = Container()

        # Register an asynchronous singleton service
        container.singleton(IAsyncTestService, AsyncTestService)

        # Register an asynchronous transient service with dependency
        container.transient(IAsyncTestServiceWithDependency, AsyncTestServiceWithDependency)

        # Resolve the asynchronous singleton service
        async_service: IAsyncTestService = container.make(IAsyncTestService)

        # Call an asynchronous method on the resolved service and check the result
        result = await container.callAsync(async_service, 'get_async_message')
        self.assertEqual(result, "Hello from async service")

        # Resolve the asynchronous transient service with dependency
        service_with_dep: IAsyncTestServiceWithDependency = container.make(IAsyncTestServiceWithDependency)

        # Call an asynchronous method that combines results from dependencies and check the result
        result2: str = await container.callAsync(service_with_dep, 'get_combined_async_message')
        self.assertTrue(result2.startswith("Combined: "))

    async def testCallableRegistration(self):
        """
        Tests the registration and resolution of synchronous and asynchronous callables in the dependency injection container.

        This method verifies that:
        - Synchronous services can be registered as singletons.
        - Synchronous callables can be registered and resolved by name.
        - Callables with dependencies are correctly resolved and invoked.
        - The resolved callables return the expected results.

        Parameters
        ----------
        self : TestContainer
            The test case instance.

        Returns
        -------
        None
            This method does not return a value. Assertions are used to validate correct behavior.
        """

        # Create a new container instance
        container = Container()

        # Register base services as singletons
        container.singleton(ITestService, TestService)
        container.singleton(IAsyncTestService, AsyncTestService)

        # Register synchronous callables, including one with a dependency
        container.callable("sync_func", sync_callable)
        container.callable("sync_func_with_dep", sync_callable_with_dependency)

        # Resolve and invoke the synchronous callable, then check its result
        result1: str = container.make("sync_func")
        self.assertEqual(result1, "Sync callable result")

        # Resolve and invoke the callable with dependency, then check its result
        result2: str = container.make("sync_func_with_dep")
        self.assertTrue(result2.startswith("Callable with dependency: "))

    async def testAsyncCallables(self):
        """
        Tests registration, resolution, and invocation of asynchronous callables in the dependency injection container.

        This method ensures that:
            - Asynchronous callables can be registered using the `callable` method.
            - Registered asynchronous callables are resolved correctly from the container.
            - Dependencies for asynchronous callables are properly injected by the container.
            - The results returned by the asynchronous callables match the expected output.

        Parameters
        ----------
        self : TestContainer
            The test case instance.

        Returns
        -------
        None
            This method does not return a value. Assertions are used to validate correct behavior.
        """

        # Create a new container instance
        container = Container()

        # Register base services as singletons for dependency injection
        container.singleton(ITestService, TestService)
        container.singleton(IAsyncTestService, AsyncTestService)

        # Register asynchronous callables, including one with a dependency
        container.callable("async_func", async_callable)
        container.callable("async_func_with_dep", async_callable_with_dependency)

        # Resolve and invoke the asynchronous callable, then check its result
        result1: str = container.make("async_func")
        self.assertEqual(result1, "Async callable result")

        # Resolve and invoke the asynchronous callable with dependency, then check its result
        result2: str = container.make("async_func_with_dep")
        self.assertTrue(result2.startswith("Async callable with dependency: "))

    async def testMixedSyncAsync(self):
        """
        Tests the container's ability to integrate synchronous and asynchronous services and dependencies.

        This method registers both a synchronous service (`TestService`) and an asynchronous service (`AsyncTestService`)
        as singletons in the container. It then resolves a `MixedService` instance, which depends on both types of services,
        and invokes its synchronous method `get_sync_message` using the container's `call` method. The test asserts that
        the returned message from the synchronous method starts with "Mixed sync: ", verifying that the container can
        correctly handle and inject both synchronous and asynchronous dependencies into a mixed service.

        Parameters
        ----------
        self : TestContainer
            The test case instance.

        Returns
        -------
        None
            This method does not return a value. Assertions are used to validate correct behavior.
        """

        # Create a new container instance
        container = Container()

        # Register synchronous and asynchronous services as singletons
        container.singleton(ITestService, TestService)
        container.singleton(IAsyncTestService, AsyncTestService)

        # Resolve the mixed service, which depends on both sync and async services
        mixed_service = container.make(MixedService)

        # Invoke the synchronous method and check the result
        sync_result: str = container.call(mixed_service, 'get_sync_message')
        self.assertTrue(sync_result.startswith("Mixed sync: "))

    async def testMixedAsync(self):
        """
        Tests the container's ability to integrate synchronous and asynchronous services and dependencies,
        focusing on asynchronous method invocation.

        This method performs the following verifications:
            - Registers both a synchronous service (`TestService`) and an asynchronous service (`AsyncTestService`)
              as singletons in the container.
            - Resolves a `MixedService` instance, which depends on both types of services.
            - Invokes the asynchronous method `get_async_message` on the mixed service using `callAsync` and asserts
              that the returned message starts with "Mixed async: ".
            - Invokes the asynchronous method `get_both_messages` on the mixed service using `callAsync` and asserts
              that the returned message starts with "Both: ".

        Parameters
        ----------
        self : TestContainer
            The test case instance.

        Returns
        -------
        None
            This method does not return a value. Assertions are used to validate correct behavior.
        """

        # Create a new container instance
        container = Container()

        # Register synchronous and asynchronous services as singletons
        container.singleton(ITestService, TestService)
        container.singleton(IAsyncTestService, AsyncTestService)

        # Resolve the mixed service, which depends on both sync and async services
        mixed_service = container.make(MixedService)

        # Invoke the asynchronous method and check the result
        async_result: str = await container.callAsync(mixed_service, 'get_async_message')
        self.assertTrue(async_result.startswith("Mixed async: "))

        # Invoke the asynchronous method that combines both sync and async dependencies and check the result
        both_result = await container.callAsync(mixed_service, 'get_both_messages')
        self.assertTrue(both_result.startswith("Both: "))
