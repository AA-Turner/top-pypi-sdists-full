import unittest
from orionis.test.output.dumper import TestDumper

class AsyncTestCase(unittest.IsolatedAsyncioTestCase, TestDumper):
    """
    Base test case class for asynchronous unit testing.

    This class provides a foundation for writing asynchronous unit tests within
    the Orionis framework. It extends unittest.IsolatedAsyncioTestCase and includes
    TestDumper functionality for enhanced test output and debugging capabilities.

    The class provides hooks for custom async setup and teardown logic through the
    onAsyncSetup() and onAsyncTeardown() methods, which can be overridden by subclasses
    to implement test-specific asynchronous initialization and cleanup procedures.

    Each test method runs in its own isolated asyncio event loop, ensuring proper
    isolation and preventing side effects between tests.

    Attributes
    ----------
    None

    Methods
    -------
    asyncSetUp()
        Initialize test environment before each async test method execution.
    asyncTearDown()
        Clean up test environment after each async test method execution.
    onAsyncSetup()
        Hook method for subclass-specific async setup logic.
    onAsyncTeardown()
        Hook method for subclass-specific async teardown logic.
    """

    async def asyncSetUp(self):
        """
        Initialize the test environment before each async test method.

        This method is automatically called by the unittest framework before
        each async test method execution. It performs the standard unittest
        async setup and then calls the onAsyncSetup() hook for custom
        asynchronous initialization.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----
        This method should not be overridden directly. Use onAsyncSetup() instead
        for custom async setup logic. The method runs in the isolated event loop
        created for each test.
        """
        await super().asyncSetUp()
        await self.onAsyncSetup()

    async def asyncTearDown(self):
        """
        Clean up the test environment after each async test method.

        This method is automatically called by the unittest framework after
        each async test method execution. It calls the onAsyncTeardown() hook
        for custom cleanup and then performs the standard unittest async teardown.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----
        This method should not be overridden directly. Use onAsyncTeardown() instead
        for custom async teardown logic. The method runs in the same isolated event
        loop as the test.
        """
        await self.onAsyncTeardown()
        await super().asyncTearDown()

    async def onAsyncSetup(self):
        """
        Hook method for subclass-specific async setup logic.

        This method is called during the asyncSetUp() phase and is intended to be
        overridden by subclasses that need to perform custom asynchronous
        initialization before each test method execution.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Examples
        --------
        >>> async def onAsyncSetup(self):
        ...     self.db_connection = await create_async_connection()
        ...     self.mock_service = AsyncMockService()
        ...     await self.mock_service.initialize()
        """
        pass

    async def onAsyncTeardown(self):
        """
        Hook method for subclass-specific async teardown logic.

        This method is called during the asyncTearDown() phase and is intended to be
        overridden by subclasses that need to perform custom asynchronous cleanup
        after each test method execution.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Examples
        --------
        >>> async def onAsyncTeardown(self):
        ...     await self.db_connection.close()
        ...     await self.mock_service.cleanup()
        ...     del self.test_data
        """
        pass
