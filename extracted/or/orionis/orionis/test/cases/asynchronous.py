import unittest
from orionis.test.output.dumper import TestDumper

class AsyncTestCase(unittest.IsolatedAsyncioTestCase, TestDumper):
    """
    Base class for asynchronous unit tests in the Orionis framework.

    Inherits from `unittest.IsolatedAsyncioTestCase` and `TestDumper`, providing
    a structure for writing asynchronous tests with isolated event loops and
    enhanced output capabilities. Subclasses can override `onAsyncSetup` and
    `onAsyncTeardown` for custom asynchronous setup and teardown logic.

    Attributes
    ----------
    None
    """

    async def asyncSetUp(self):
        """
        Asynchronous setup executed before each test method.

        Calls the parent class's asyncSetUp and then invokes the
        `onAsyncSetup` hook for additional subclass-specific setup.

        Returns
        -------
        None
        """
        await super().asyncSetUp()
        await self.onAsyncSetup()

    async def asyncTearDown(self):
        """
        Asynchronous teardown executed after each test method.

        Invokes the `onAsyncTeardown` hook for subclass-specific cleanup,
        then calls the parent class's asyncTearDown.

        Returns
        -------
        None
        """
        await self.onAsyncTeardown()
        await super().asyncTearDown()

    async def onAsyncSetup(self):
        """
        Hook for subclass-specific asynchronous setup logic.

        Intended to be overridden by subclasses to perform custom
        asynchronous initialization before each test.

        Returns
        -------
        None
        """
        pass

    async def onAsyncTeardown(self):
        """
        Hook for subclass-specific asynchronous teardown logic.

        Intended to be overridden by subclasses to perform custom
        asynchronous cleanup after each test.

        Returns
        -------
        None
        """
        pass
