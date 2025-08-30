import os
import sys
from orionis.console.dumper.debug import Debug
from orionis.test.exceptions import OrionisTestRuntimeError
from orionis.test.contracts.dumper import ITestDumper

class TestDumper(ITestDumper):
    """
    Utility class for debugging and outputting information during test execution.

    Provides methods to determine if an object is a test case instance, output debugging
    information using the Debug class, manage standard output and error streams, and
    capture the caller's file and line number for context.
    """

    def __isTestCaseClass(self, value) -> bool:
        """
        Check if the provided value is an instance of a recognized test case class.

        Parameters
        ----------
        value : object
            The object to check for test case class membership.

        Returns
        -------
        bool
            True if `value` is an instance of AsyncTestCase, SyncTestCase, unittest.TestCase,
            or unittest.IsolatedAsyncioTestCase. False otherwise or if an import error occurs.
        """

        # If the value is None, it cannot be a test case instance.
        if value is None:
            return False

        try:

            # Attempt to import the test case base classes.
            from orionis.test.cases.asynchronous import AsyncTestCase
            from orionis.test.cases.synchronous import SyncTestCase
            import unittest

            # Check if the value is an instance of either Orionis or native unittest test case class.
            return isinstance(
                value,
                (
                    AsyncTestCase,
                    SyncTestCase,
                    unittest.TestCase,
                    unittest.IsolatedAsyncioTestCase
                )
            )

        except Exception:

            # If imports fail or any other exception occurs, return False.
            return False

    def dd(self, *args) -> None:
        """
        Output debugging information and halt further execution.

        Captures the caller's file and line number for context. Temporarily redirects
        standard output and error streams to ensure correct display. If the first argument
        is a recognized test case instance, it is skipped in the output. Raises a custom
        runtime error if dumping fails.

        Parameters
        ----------
        *args : tuple
            Objects to be dumped.

        Returns
        -------
        None
        """

        # If no arguments are provided, exit the method early.
        if not args:
            return

        # Save the original stdout and stderr to restore them later
        original_stdout = sys.stdout
        original_stderr = sys.stderr

        try:

            # Redirect stdout and stderr to the system defaults for proper debug output
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

            # Retrieve the caller's frame to get file and line number context
            caller_frame = sys._getframe(1)
            _file = os.path.abspath(caller_frame.f_code.co_filename)
            _line = caller_frame.f_lineno

            # Initialize the Debug dumper with context information
            dumper = Debug(f"{_file}:{_line}")

            # If the first argument is a test case instance, skip it in the output
            if self.__isTestCaseClass(args[0]):
                dumper.dd(*args[1:])
            else:
                dumper.dd(*args)

        except Exception as e:

            # Raise a custom runtime error if dumping fails
            raise OrionisTestRuntimeError(f"An error occurred while dumping debug information: {e}")

        finally:

            # Restore the original stdout and stderr
            sys.stdout = original_stdout
            sys.stderr = original_stderr

    def dump(self, *args) -> None:
        """
        Output debugging information.

        Captures the caller's file and line number for context. Temporarily redirects
        standard output and error streams to ensure correct display. If the first argument
        is a recognized test case instance, it is skipped in the output. Raises a custom
        runtime error if dumping fails.

        Parameters
        ----------
        *args : tuple
            Objects to be dumped.

        Returns
        -------
        None
        """

        # If no arguments are provided, exit the method early.
        if not args:
            return

        # Save the original stdout and stderr to restore them later
        original_stdout = sys.stdout
        original_stderr = sys.stderr

        try:

            # Redirect stdout and stderr to the system defaults for proper debug output
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

            # Retrieve the caller's frame to get file and line number context
            caller_frame = sys._getframe(1)
            _file = os.path.abspath(caller_frame.f_code.co_filename)
            _line = caller_frame.f_lineno

            # Initialize the Debug dumper with context information
            dumper = Debug(f"{_file}:{_line}")

            # If the first argument is a test case instance, skip it in the output
            if self.__isTestCaseClass(args[0]):
                dumper.dump(*args[1:])
            else:
                dumper.dump(*args)

        except Exception as e:

            # Raise a custom runtime error if dumping fails
            raise OrionisTestRuntimeError(f"An error occurred while dumping debug information: {e}")

        finally:

            # Restore the original stdout and stderr
            sys.stdout = original_stdout
            sys.stderr = original_stderr
