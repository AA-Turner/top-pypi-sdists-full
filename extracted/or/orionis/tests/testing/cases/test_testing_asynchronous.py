from orionis.test.cases.asynchronous import AsyncTestCase
import inspect

class TestAsyncTestCase(AsyncTestCase):

    async def testMethodsExist(self):
        """
        Verify that AsyncTestCase defines the required asynchronous lifecycle methods.

        Parameters
        ----------
        self : TestAsyncTestCase
            Instance of the test case.

        Returns
        -------
        None
            This method does not return a value.

        Raises
        ------
        AssertionError
            If any of the required methods do not exist in AsyncTestCase.
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
        Check that all required asynchronous lifecycle methods in AsyncTestCase are coroutine functions.

        Parameters
        ----------
        self : TestAsyncTestCase
            Instance of the test case.

        Returns
        -------
        None
            This method does not return a value.

        Raises
        ------
        AssertionError
            If any of the required methods are not coroutine functions.
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
