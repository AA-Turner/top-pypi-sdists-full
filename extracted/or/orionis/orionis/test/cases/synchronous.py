import unittest
from orionis.test.output.dumper import TestDumper

class SyncTestCase(unittest.TestCase, TestDumper):
    """
    Base class for synchronous unit tests in the Orionis framework.

    Inherits from `unittest.TestCase` and `TestDumper`, providing
    hooks for custom setup and teardown logic via `onSetup()` and
    `onTeardown()` methods. Subclasses should override these hooks
    to implement test-specific initialization and cleanup.

    Attributes
    ----------
    None
    """

    def setUp(self):
        """
        Set up the test environment before each test method.

        Calls the superclass `setUp()` and then invokes the
        `onSetup()` hook for additional initialization.

        Returns
        -------
        None
        """
        super().setUp()
        self.onSetup()

    def tearDown(self):
        """
        Clean up the test environment after each test method.

        Invokes the `onTeardown()` hook for custom cleanup and
        then calls the superclass `tearDown()`.

        Returns
        -------
        None
        """
        self.onTeardown()
        super().tearDown()

    def onSetup(self):
        """
        Hook for subclass-specific setup logic.

        Intended to be overridden by subclasses to perform
        custom initialization before each test.

        Returns
        -------
        None
        """
        pass

    def onTeardown(self):
        """
        Hook for subclass-specific teardown logic.

        Intended to be overridden by subclasses to perform
        custom cleanup after each test.

        Returns
        -------
        None
        """
        pass
