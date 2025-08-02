import unittest
from orionis.test.output.dumper import TestDumper

class SyncTestCase(unittest.TestCase, TestDumper):
    """
    Base test case class for synchronous unit testing.

    This class provides a foundation for writing synchronous unit tests within
    the Orionis framework. It extends unittest.TestCase and includes TestDumper
    functionality for enhanced test output and debugging capabilities.

    The class provides hooks for custom setup and teardown logic through the
    onSetup() and onTeardown() methods, which can be overridden by subclasses
    to implement test-specific initialization and cleanup procedures.

    Attributes
    ----------
    None

    Methods
    -------
    setUp()
        Initialize test environment before each test method execution.
    tearDown()
        Clean up test environment after each test method execution.
    onSetup()
        Hook method for subclass-specific setup logic.
    onTeardown()
        Hook method for subclass-specific teardown logic.
    """

    def setUp(self):
        """
        Initialize the test environment before each test method.

        This method is automatically called by the unittest framework before
        each test method execution. It performs the standard unittest setup
        and then calls the onSetup() hook for custom initialization.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----
        This method should not be overridden directly. Use onSetup() instead
        for custom setup logic.
        """
        super().setUp()
        self.onSetup()

    def tearDown(self):
        """
        Clean up the test environment after each test method.

        This method is automatically called by the unittest framework after
        each test method execution. It calls the onTeardown() hook for custom
        cleanup and then performs the standard unittest teardown.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----
        This method should not be overridden directly. Use onTeardown() instead
        for custom teardown logic.
        """
        self.onTeardown()
        super().tearDown()

    def onSetup(self):
        """
        Hook method for subclass-specific setup logic.

        This method is called during the setUp() phase and is intended to be
        overridden by subclasses that need to perform custom initialization
        before each test method execution.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Examples
        --------
        >>> def onSetup(self):
        ...     self.mock_service = MockService()
        ...     self.test_data = {"key": "value"}
        """
        pass

    def onTeardown(self):
        """
        Hook method for subclass-specific teardown logic.

        This method is called during the tearDown() phase and is intended to be
        overridden by subclasses that need to perform custom cleanup after
        each test method execution.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Examples
        --------
        >>> def onTeardown(self):
        ...     self.mock_service.cleanup()
        ...     del self.test_data
        """
        pass