from orionis.test.cases.asynchronous import AsyncTestCase
import inspect

class TestAsyncTestCase(AsyncTestCase):

    async def testMethodsExist(self):
        """
        Checks if the AsyncTestCase class defines the required asynchronous lifecycle methods.

        Parameters
        ----------
        self : TestAsyncTestCase
            The test case instance.

        Returns
        -------
        None
            This method does not return anything. It asserts the existence of required methods.

        Notes
        -----
        This test ensures that the AsyncTestCase class contains all necessary asynchronous lifecycle methods
        for proper setup and teardown in asynchronous test scenarios.
        """
        required_methods = [
            "asyncSetUp",
            "asyncTearDown",
            "onAsyncSetup",
            "onAsyncTeardown"
        ]
        # Assert that each required method exists in AsyncTestCase
        for method_name in required_methods:
            self.assertTrue(hasattr(AsyncTestCase, method_name), f"{method_name} does not exist")

    async def testMethodsAreCoroutines(self):
        """
        Checks that all required asynchronous lifecycle methods in AsyncTestCase are coroutine functions.

        Parameters
        ----------
        self : TestAsyncTestCase
            The test case instance.

        Returns
        -------
        None
            This method does not return anything. It asserts that required methods are coroutine functions.

        Notes
        -----
        This test verifies that the lifecycle methods are implemented as coroutine functions,
        which is necessary for asynchronous execution in test cases.
        """
        required_methods = [
            "asyncSetUp",
            "asyncTearDown",
            "onAsyncSetup",
            "onAsyncTeardown"
        ]
        # Assert that each required method is a coroutine function
        for method_name in required_methods:
            method = getattr(AsyncTestCase, method_name)
            self.assertTrue(inspect.iscoroutinefunction(method), f"{method_name} is not a coroutine function")
