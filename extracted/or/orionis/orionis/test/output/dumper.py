import os
import sys
from orionis.console.dumper.dump import Debug
from orionis.test.exceptions import OrionisTestRuntimeError
from orionis.test.contracts.dumper import ITestDumper

class TestDumper(ITestDumper):
    """
    TestDumper provides utility methods for debugging and outputting information during test execution.

    This class implements methods to:
        - Determine if an object is a test case instance.
        - Output debugging information using the Debug class.
        - Manage standard output and error streams during debugging dumps.
        - Capture the caller's file and line number for context.

    Attributes
    ----------
    None

    Methods
    -------
    __isTestCaseClass(value)
        Determines if the given value is an instance of a test case class.
    dd(*args)
        Dumps debugging information using the Debug class.
    dump(*args)
        Dumps debugging information using the Debug class.
    """

    def __isTestCaseClass(self, value) -> bool:
        """
        Determines whether the provided value is an instance of a recognized test case class.

        This method checks if the given object is an instance of either AsyncTestCase or SyncTestCase,
        which are the supported test case base classes in the Orionis testing framework.

        Parameters
        ----------
        value : object
            The object to check for test case class membership.

        Returns
        -------
        bool
            Returns True if `value` is an instance of AsyncTestCase or SyncTestCase.
            Returns False if `value` is None, not an instance of these classes, or if any import error occurs.
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
        Outputs debugging information using the Debug class and halts further execution.

        This method captures the caller's file and line number to provide context for the debug output.
        It temporarily redirects standard output and error streams to ensure the debug information is
        displayed correctly. If the first argument is a recognized test case instance, it is skipped
        in the output to avoid redundant information. The method raises an exception if any error
        occurs during the dumping process.

        Parameters
        ----------
        *args : tuple
            Variable length argument list containing the objects to be dumped.

        Returns
        -------
        None
            This method does not return any value. It outputs debug information and may halt execution.
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
        Outputs debugging information using the Debug class.

        This method captures the caller's file and line number to provide context for the debug output.
        It temporarily redirects standard output and error streams to ensure the debug information is
        displayed correctly. If the first argument is a recognized test case instance, it is skipped
        in the output to avoid redundant information. The method raises an exception if any error
        occurs during the dumping process.

        Parameters
        ----------
        *args : tuple
            Variable length argument list containing the objects to be dumped.

        Returns
        -------
        None
            This method does not return any value. It outputs debug information.
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