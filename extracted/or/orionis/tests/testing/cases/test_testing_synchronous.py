from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.test.cases.synchronous import SyncTestCase
import inspect

class TestSyncTestCase(AsyncTestCase):

    async def testHasMethods(self):
        """
        Verify that SyncTestCase defines the required synchronous lifecycle methods.

        This method asserts the presence of the following methods in SyncTestCase:
        - setUp
        - tearDown
        - onSetup
        - onTeardown

        Returns
        -------
        None
        """
        # Assert that SyncTestCase has a setUp method
        self.assertTrue(hasattr(SyncTestCase, "setUp"))

        # Assert that SyncTestCase has a tearDown method
        self.assertTrue(hasattr(SyncTestCase, "tearDown"))

        # Assert that SyncTestCase has an onSetup method
        self.assertTrue(hasattr(SyncTestCase, "onSetup"))

        # Assert that SyncTestCase has an onTeardown method
        self.assertTrue(hasattr(SyncTestCase, "onTeardown"))

    async def testMethodsAreNotCoroutines(self):
        """
        Ensure that the lifecycle methods of SyncTestCase are synchronous functions.

        This method checks that the following methods are not coroutine functions:
        - setUp
        - tearDown
        - onSetup
        - onTeardown

        Returns
        -------
        None
        """
        # Assert that setUp is not a coroutine function
        self.assertFalse(inspect.iscoroutinefunction(SyncTestCase.setUp))

        # Assert that tearDown is not a coroutine function
        self.assertFalse(inspect.iscoroutinefunction(SyncTestCase.tearDown))

        # Assert that onSetup is not a coroutine function
        self.assertFalse(inspect.iscoroutinefunction(SyncTestCase.onSetup))

        # Assert that onTeardown is not a coroutine function
        self.assertFalse(inspect.iscoroutinefunction(SyncTestCase.onTeardown))
