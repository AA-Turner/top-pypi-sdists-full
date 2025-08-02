from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.test.cases.synchronous import SyncTestCase
import inspect

class TestSyncTestCase(AsyncTestCase):

    async def testHasMethods(self):
        """
        Checks whether the SyncTestCase class defines the required synchronous lifecycle methods.

        This test verifies the existence of the following methods in SyncTestCase:
            - setUp: Prepares the test environment before each test.
            - tearDown: Cleans up the test environment after each test.
            - onSetup: Additional setup logic for tests.
            - onTeardown: Additional teardown logic for tests.

        Returns
        -------
        None
            This method does not return any value. It performs assertions to validate the presence of required methods.
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
        Checks that the lifecycle methods of SyncTestCase are regular functions and not coroutine functions.

        This test ensures that the following methods are synchronous:
            - setUp
            - tearDown
            - onSetup
            - onTeardown

        Returns
        -------
        None
            This method does not return any value. It performs assertions to confirm that the methods are not coroutine functions.
        """
        # Assert that setUp is not a coroutine function
        self.assertFalse(inspect.iscoroutinefunction(SyncTestCase.setUp))

        # Assert that tearDown is not a coroutine function
        self.assertFalse(inspect.iscoroutinefunction(SyncTestCase.tearDown))

        # Assert that onSetup is not a coroutine function
        self.assertFalse(inspect.iscoroutinefunction(SyncTestCase.onSetup))

        # Assert that onTeardown is not a coroutine function
        self.assertFalse(inspect.iscoroutinefunction(SyncTestCase.onTeardown))
