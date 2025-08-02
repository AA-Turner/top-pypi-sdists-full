import io
import json
import re
import time
import traceback
import unittest
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from orionis.container.resolver.resolver import Resolver
from orionis.foundation.config.testing.enums.drivers import PersistentDrivers
from orionis.foundation.config.testing.enums.mode import ExecutionMode
from orionis.foundation.config.testing.enums.verbosity import VerbosityMode
from orionis.foundation.contracts.application import IApplication
from orionis.services.introspection.instances.reflection import ReflectionInstance
from orionis.test.contracts.test_result import IOrionisTestResult
from orionis.test.contracts.unit_test import IUnitTest
from orionis.test.entities.result import TestResult
from orionis.test.enums import TestStatus
from orionis.test.exceptions import (
    OrionisTestFailureException,
    OrionisTestPersistenceError,
    OrionisTestValueError,
)
from orionis.test.output.printer import TestPrinter
from orionis.test.records.logs import TestLogs
from orionis.test.validators import (
    ValidExecutionMode,
    ValidFailFast,
    ValidPersistent,
    ValidPersistentDriver,
    ValidPrintResult,
    ValidThrowException,
    ValidVerbosity,
    ValidWebReport,
    ValidWorkers,
    ValidBasePath,
    ValidFolderPath,
    ValidNamePattern,
    ValidPattern,
    ValidTags,
    ValidModuleName,
)
from orionis.test.view.render import TestingResultRender

class UnitTest(IUnitTest):
    """
    Orionis UnitTest

    Advanced unit testing manager for the Orionis framework.

    This class offers a robust and extensible solution for discovering, executing, and reporting unit tests with high configurability. It supports both sequential and parallel execution modes, filtering by test name or tags, and provides detailed result tracking including execution times, error messages, and tracebacks.

    Key features:
    - Flexible test discovery from folders or modules, with pattern and tag filtering.
    - Rich result reporting: console output, persistent storage (SQLite or JSON), and web-based reports.
    - Dependency injection for test methods via the application context.
    - Customizable verbosity, fail-fast, and exception handling options.
    - Designed for easy integration into CI/CD pipelines and adaptable to diverse project requirements.

    Orionis UnitTest is ideal for teams seeking enhanced traceability, reliability, and visibility in automated testing, with capabilities that go beyond standard unittest frameworks.
    """

    def __init__(
        self
    ) -> None:
        """
        Initialize a new UnitTest instance with default configuration and internal state.

        This constructor sets up all internal attributes required for test discovery, execution,
        result reporting, and configuration management. It prepares the instance for further
        configuration and use, but does not perform any test discovery or execution itself.

        Attributes
        ----------
        __app : Optional[IApplication]
            The application instance used for dependency injection in test cases.
        __verbosity : Optional[int]
            Verbosity level for test output (None until configured).
        __execution_mode : Optional[str]
            Test execution mode, e.g., 'SEQUENTIAL' or 'PARALLEL' (None until configured).
        __max_workers : Optional[int]
            Maximum number of worker threads/processes for parallel execution (None until configured).
        __fail_fast : Optional[bool]
            If True, stops execution upon the first test failure (None until configured).
        __throw_exception : Optional[bool]
            If True, raises exceptions on test failures (None until configured).
        __persistent : Optional[bool]
            If True, enables persistent storage for test results (None until configured).
        __persistent_driver : Optional[str]
            The driver to use for persistence, e.g., 'sqlite' or 'json' (None until configured).
        __web_report : Optional[bool]
            If True, enables web-based reporting of test results (None until configured).
        __folder_path : Optional[str]
            Relative folder path for test discovery (None until set).
        __base_path : Optional[str]
            Base directory for test discovery (None until set).
        __pattern : Optional[str]
            File name pattern to match test files (None until set).
        __test_name_pattern : Optional[str]
            Pattern to filter test names (None until set).
        __tags : Optional[List[str]]
            List of tags to filter tests (None until set).
        __module_name : Optional[str]
            Name of the module for test discovery (None until set).
        __loader : unittest.TestLoader
            Loader for discovering tests.
        __suite : unittest.TestSuite
            Test suite containing discovered tests.
        __discovered_tests : List
            List of discovered test metadata.
        __printer : Optional[TestPrinter]
            Utility for printing test results to the console.
        __output_buffer : Optional[str]
            Buffer for capturing standard output during tests.
        __error_buffer : Optional[str]
            Buffer for capturing error output during tests.
        __result : Optional[dict]
            Result summary of the test execution.

        Returns
        -------
        None
            This constructor does not return a value.
        """

        # Application instance for dependency injection (set via __setApp)
        self.__app: Optional[IApplication] = None

        # Storage path for test results (set via __setApp)
        self.__storage: Optional[str] = None

        # Configuration values (set via configure)
        self.__verbosity: Optional[int] = None
        self.__execution_mode: Optional[str] = None
        self.__max_workers: Optional[int] = None
        self.__fail_fast: Optional[bool] = None
        self.__throw_exception: Optional[bool] = None
        self.__persistent: Optional[bool] = None
        self.__persistent_driver: Optional[str] = None
        self.__web_report: Optional[bool] = None

        # Test discovery parameters for folders
        self.__folder_path: Optional[str] = None
        self.__base_path: Optional[str] = None
        self.__pattern: Optional[str] = None
        self.__test_name_pattern: Optional[str] = None
        self.__tags: Optional[List[str]] = None

        # Test discovery parameter for modules
        self.__module_name: Optional[str] = None

        # Initialize the unittest loader and suite for test discovery and execution
        self.__loader = unittest.TestLoader()
        self.__suite = unittest.TestSuite()
        self.__discovered_tests: List = []

        # Printer for console output (set during configuration)
        self.__printer: TestPrinter = None

        # Buffers for capturing standard output and error during test execution
        self.__output_buffer = None
        self.__error_buffer = None

        # Stores the result summary after test execution
        self.__result = None

    def configure(
        self,
        *,
        verbosity: int | VerbosityMode,
        execution_mode: str | ExecutionMode,
        max_workers: int,
        fail_fast: bool,
        print_result: bool,
        throw_exception: bool,
        persistent: bool,
        persistent_driver: str | PersistentDrivers,
        web_report: bool
    ) -> 'UnitTest':
        """
        Configures the UnitTest instance with the main execution and reporting parameters.

        This method sets all relevant options for running unit tests in Orionis, including execution mode
        (sequential or parallel), verbosity level, maximum number of workers, result persistence, exception
        handling, and web report generation.

        Parameters
        ----------
        verbosity : int | VerbosityMode
            Verbosity level for test output. Can be an integer or a VerbosityMode enum member.
        execution_mode : str | ExecutionMode
            Test execution mode ('SEQUENTIAL' or 'PARALLEL'), as a string or ExecutionMode enum.
        max_workers : int
            Maximum number of threads/processes for parallel execution. Must be between 1 and the maximum allowed by Workers.
        fail_fast : bool
            If True, stops execution on the first failure.
        print_result : bool
            If True, prints results to the console.
        throw_exception : bool
            If True, raises exceptions on test failures.
        persistent : bool
            If True, enables result persistence.
        persistent_driver : str or PersistentDrivers
            Persistence driver to use ('sqlite' or 'json').
        web_report : bool
            If True, enables web report generation.

        Returns
        -------
        UnitTest
            The configured UnitTest instance, allowing method chaining.

        Raises
        ------
        OrionisTestValueError
            If any parameter is invalid or does not meet the expected requirements.
        """

        # Validate and assign parameters using specialized validators
        self.__verbosity = ValidVerbosity(verbosity)
        self.__execution_mode = ValidExecutionMode(execution_mode)
        self.__max_workers = ValidWorkers(max_workers)
        self.__fail_fast = ValidFailFast(fail_fast)
        self.__throw_exception = ValidThrowException(throw_exception)
        self.__persistent = ValidPersistent(persistent)
        self.__persistent_driver = ValidPersistentDriver(persistent_driver)
        self.__web_report = ValidWebReport(web_report)

        # Initialize the result printer with the current configuration
        self.__printer = TestPrinter(
            print_result = ValidPrintResult(print_result)
        )

        # Return the instance to allow method chaining
        return self

    def discoverTestsInFolder(
        self,
        *,
        base_path: str | Path,
        folder_path: str,
        pattern: str,
        test_name_pattern: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> 'UnitTest':
        """
        Discover and add unit tests from a specified folder to the test suite.

        This method searches for test files within a given folder, using a file name pattern,
        and optionally filters discovered tests by test name pattern and tags. All matching
        tests are added to the internal test suite. The method also records metadata about
        the discovery process, such as the folder path and the number of tests found.

        Parameters
        ----------
        base_path : str or Path
            The base directory from which the folder path is resolved.
        folder_path : str
            The relative path to the folder containing test files, relative to `base_path`.
        pattern : str
            The file name pattern to match test files (e.g., 'test_*.py').
        test_name_pattern : str, optional
            A regular expression pattern to filter test names. Only tests whose names match
            this pattern will be included. If None, all test names are included.
        tags : list of str, optional
            A list of tags to filter tests. Only tests decorated or marked with any of these
            tags will be included. If None, no tag filtering is applied.

        Returns
        -------
        UnitTest
            The current instance with the discovered tests added to the suite.

        Raises
        ------
        OrionisTestValueError
            If any argument is invalid, the folder does not exist, no tests are found,
            or if there are import or discovery errors.

        Notes
        -----
        - The method validates all input parameters using Orionis validators.
        - The folder path is resolved relative to the provided base path.
        - Test discovery uses Python's unittest loader.
        - If `test_name_pattern` is provided, only tests whose names match the pattern are included.
        - If `tags` are provided, only tests with matching tags are included.
        - If no tests are found after filtering, an exception is raised.
        - Metadata about the discovery (folder and test count) is appended to the internal record.
        """

        # Validate Parameters
        self.__base_path = ValidBasePath(base_path)
        self.__folder_path = ValidFolderPath(folder_path)
        self.__pattern = ValidPattern(pattern)
        self.__test_name_pattern = ValidNamePattern(test_name_pattern)
        self.__tags = ValidTags(tags)

        # Try to discover tests in the specified folder
        try:

            # Ensure the folder path is absolute
            full_path = Path(self.__base_path / self.__folder_path).resolve()

            # Validate the full path
            if not full_path.exists():
                raise OrionisTestValueError(
                    f"Test folder not found at the specified path: '{str(full_path)}'. "
                    "Please verify that the path is correct and the folder exists."
                )

            # Discover tests using the unittest TestLoader
            tests = self.__loader.discover(
                start_dir=str(full_path),
                pattern=self.__pattern,
                top_level_dir="."
            )

            # Check for failed test imports (unittest.loader._FailedTest)
            for test in self.__flattenTestSuite(tests):
                if test.__class__.__name__ == "_FailedTest":
                    # Extract the error message from the test's traceback
                    error_message = ""
                    if hasattr(test, "_exception"):
                        error_message = str(test._exception)
                    elif hasattr(test, "_outcome") and hasattr(test._outcome, "errors"):
                        error_message = str(test._outcome.errors)
                    else:
                        # Try to get error from test id or str(test)
                        error_message = str(test)
                    raise OrionisTestValueError(
                        f"Failed to import test module: {test.id()}.\n"
                        f"Error details: {error_message}\n"
                        "Please check for import errors or missing dependencies."
                    )

            # If name pattern is provided, filter tests by name
            if test_name_pattern:
                tests = self.__filterTestsByName(
                    suite=tests,
                    pattern=self.__test_name_pattern
                )

            # If tags are provided, filter tests by tags
            if tags:
                tests = self.__filterTestsByTags(
                    suite=tests,
                    tags=self.__tags
                )

            # If no tests are found, raise an error
            if not list(tests):
                raise OrionisTestValueError(
                    f"No tests found in '{str(full_path)}' matching file pattern '{pattern}'"
                    + (f", test name pattern '{test_name_pattern}'" if test_name_pattern else "")
                    + (f", and tags {tags}" if tags else "") +
                    ". Please check your patterns, tags, and test files."
                )

            # Add discovered tests to the suite
            self.__suite.addTests(tests)

            # Count the number of tests discovered
            # Using __flattenTestSuite to ensure we count all individual test cases
            test_count = len(list(self.__flattenTestSuite(tests)))

            # Append the discovered tests information
            self.__discovered_tests.append({
                "folder": str(full_path),
                "test_count": test_count,
            })

            # Return the current instance
            return self

        except ImportError as e:

            # Raise a specific error if the import fails
            raise OrionisTestValueError(
                f"Error importing tests from path '{str(full_path)}': {str(e)}.\n"
                "Please verify that the directory and test modules are accessible and correct."
            )

        except Exception as e:

            # Raise a general error for unexpected issues
            raise OrionisTestValueError(
                f"Unexpected error while discovering tests in '{str(full_path)}': {str(e)}.\n"
                "Ensure that the test files are valid and that there are no syntax errors or missing dependencies."
            )

    def discoverTestsInModule(
        self,
        *,
        module_name: str,
        test_name_pattern: Optional[str] = None
    ) -> 'UnitTest':
        """
        Discover and add unit tests from a specified Python module to the test suite.

        This method loads all unit tests defined within the given module and adds them to the internal test suite.
        Optionally, it can filter discovered tests by a regular expression pattern applied to test names.

        Parameters
        ----------
        module_name : str
            The fully qualified name of the module from which to discover tests (e.g., 'myproject.tests.test_example').
            Must be a non-empty string and importable from the current environment.
        test_name_pattern : str or None, optional
            A regular expression pattern to filter test names. Only tests whose names match this pattern
            will be included in the suite. If None, all discovered tests are included.

        Returns
        -------
        UnitTest
            The current UnitTest instance with the discovered tests added, allowing method chaining.

        Raises
        ------
        OrionisTestValueError
            If `module_name` is invalid, `test_name_pattern` is not a valid regex, the module cannot be imported,
            or if no tests are found after filtering.
        OrionisTestValueError
            For any unexpected error during test discovery, with details about the failure.

        Notes
        -----
        - Input parameters are validated using Orionis validators before discovery.
        - If `test_name_pattern` is provided, only tests matching the pattern are included.
        - Metadata about the discovery (module name and test count) is appended to the internal `__discovered_tests` list.
        - This method is useful for dynamically loading tests from specific modules, such as in plugin architectures or
          when tests are not organized in standard file patterns.
        """

        # Validate input parameters
        self.__module_name = ValidModuleName(module_name)
        self.__test_name_pattern = ValidNamePattern(test_name_pattern)

        try:
            # Load all tests from the specified module
            tests = self.__loader.loadTestsFromName(
                name=self.__module_name
            )

            # If a test name pattern is provided, filter the discovered tests
            if test_name_pattern:
                tests = self.__filterTestsByName(
                    suite=tests,
                    pattern=self.__test_name_pattern
                )

            # Add the filtered (or all) tests to the suite
            self.__suite.addTests(tests)

            # Count the number of discovered tests
            test_count = len(list(self.__flattenTestSuite(tests)))

            if test_count == 0:
                raise OrionisTestValueError(
                    f"No tests found in module '{self.__module_name}'"
                    + (f" matching test name pattern '{test_name_pattern}'." if test_name_pattern else ".")
                    + " Please ensure the module contains valid test cases and the pattern is correct."
                )

            # Record discovery metadata
            self.__discovered_tests.append({
                "module": self.__module_name,
                "test_count": test_count
            })

            # Return the current instance for method chaining
            return self

        except ImportError as e:

            # Raise an error if the module cannot be imported
            raise OrionisTestValueError(
                f"Failed to import tests from module '{self.__module_name}': {str(e)}. "
                "Ensure the module exists, is importable, and contains valid test cases."
            )

        except re.error as e:

            # Raise an error if the test name pattern is not a valid regex
            raise OrionisTestValueError(
                f"Invalid regular expression for test_name_pattern: '{test_name_pattern}'. "
                f"Regex compilation error: {str(e)}. Please check the pattern syntax."
            )

        except Exception as e:

            # Raise a general error for unexpected issues
            raise OrionisTestValueError(
                f"An unexpected error occurred while discovering tests in module '{self.__module_name}': {str(e)}. "
                "Verify that the module name is correct, test methods are valid, and there are no syntax errors or missing dependencies."
            )

    def run(
        self
    ) -> Dict[str, Any]:
        """
        Execute the test suite and return a summary of the results.

        This method manages the full test execution lifecycle: it prints start and finish messages,
        executes the test suite, captures output and error buffers, processes the results, and
        optionally raises an exception if failures occur and exception throwing is enabled.

        Returns
        -------
        Dict[str, Any]
            A dictionary summarizing the test results, including statistics and execution time.

        Raises
        ------
        OrionisTestFailureException
            If the test suite execution fails and `throw_exception` is set to True.

        Notes
        -----
        - Measures total execution time in milliseconds.
        - Uses the configured printer to display start, result, and finish messages.
        - Captures and stores output and error buffers.
        - Raises an exception if tests fail and exception throwing is enabled.
        """

        # Record the start time in nanoseconds
        start_time = time.time_ns()

        # Print the start message with test suite details
        self.__printer.startMessage(
            length_tests=len(list(self.__flattenTestSuite(self.__suite))),
            execution_mode=self.__execution_mode,
            max_workers=self.__max_workers
        )

        # Execute the test suite and capture result, output, and error buffers
        result, output_buffer, error_buffer = self.__printer.executePanel(
            flatten_test_suite=self.__flattenTestSuite(self.__suite),
            callable=self.__runSuite
        )

        # Store the captured output and error buffers as strings
        self.__output_buffer = output_buffer.getvalue()
        self.__error_buffer = error_buffer.getvalue()

        # Calculate execution time in milliseconds
        execution_time = (time.time_ns() - start_time) / 1_000_000_000

        # Generate a summary of the test results
        summary = self.__generateSummary(result, execution_time)

        # Display the test results using the printer
        self.__printer.displayResults(summary=summary)

        # Raise an exception if tests failed and exception throwing is enabled
        if not result.wasSuccessful() and self.__throw_exception:
            raise OrionisTestFailureException(result)

        # Print the final summary message
        self.__printer.finishMessage(summary=summary)

        # Return the summary of the test results
        return summary

    def __flattenTestSuite(
        self,
        suite: unittest.TestSuite
    ) -> List[unittest.TestCase]:
        """
        Recursively flattens a (potentially nested) unittest.TestSuite into a list of unique unittest.TestCase instances.

        This method traverses the provided test suite, which may contain nested suites or individual test cases,
        and collects all unique TestCase instances into a flat list. It ensures that each test case appears only once
        in the resulting list, based on a short identifier derived from the test's id. This is particularly useful
        for operations that require direct access to all test cases, such as filtering, counting, or custom execution.

        Parameters
        ----------
        suite : unittest.TestSuite
            The test suite to flatten. This can be a single suite, a nested suite, or a suite containing test cases.

        Returns
        -------
        List[unittest.TestCase]
            A flat list containing all unique unittest.TestCase instances found within the input suite.

        Notes
        -----
        - The uniqueness of test cases is determined by a "short id", which is composed of the last two segments
          of the test's full id (typically "ClassName.methodName"). This helps avoid duplicate test cases in the result.
        - The method uses recursion to traverse all levels of nested suites.
        - Only objects with an 'id' attribute (i.e., test cases) are included in the result.
        """
        tests = []
        seen_ids = set()

        def _flatten(item):
            """
            Recursively process a TestSuite or test case, collecting unique test cases.

            - If the item is a TestSuite, recursively process its children.
            - If the item is a test case (has 'id'), generate a short id and add it if not already seen.
            """
            if isinstance(item, unittest.TestSuite):
                # Recursively flatten all sub-items in the suite
                for sub_item in item:
                    _flatten(sub_item)
            elif hasattr(item, "id"):
                # Generate a short id for uniqueness (e.g., "ClassName.methodName")
                test_id = item.id()
                parts = test_id.split('.')
                if len(parts) >= 2:
                    short_id = '.'.join(parts[-2:])
                else:
                    short_id = test_id
                # Add the test case only if its short id has not been seen
                if short_id not in seen_ids:
                    seen_ids.add(short_id)
                    tests.append(item)

        # Start flattening from the root suite
        _flatten(suite)

        # Return a flat list of unique unittest.TestCase instances
        return tests

    def __runSuite(
        self
    ) -> Tuple[unittest.TestResult, io.StringIO, io.StringIO]:
        """
        Executes the test suite using the configured execution mode (sequential or parallel),
        while capturing both standard output and error streams during the test run.

        This method determines the execution mode (sequential or parallel) based on the current
        configuration and delegates the actual test execution to the appropriate internal method.
        It ensures that all output and error messages generated during the test run are captured
        in dedicated buffers for later inspection or reporting.

        Returns
        -------
        Tuple[unittest.TestResult, io.StringIO, io.StringIO]
            A tuple containing:
                - result: The unittest.TestResult object with detailed information about the test run,
                  including passed, failed, errored, and skipped tests.
                - output_buffer: An io.StringIO object containing all captured standard output produced
                  during the test execution.
                - error_buffer: An io.StringIO object containing all captured standard error output
                  produced during the test execution.

        Notes
        -----
        - The execution mode is determined by the value of self.__execution_mode.
        - Output and error streams are always captured, regardless of execution mode.
        - The returned buffers can be used for further processing, logging, or displaying test output.
        """

        # Create buffers to capture standard output and error during test execution
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()

        # Determine execution mode and run tests accordingly
        if self.__execution_mode == ExecutionMode.PARALLEL.value:
            # Run tests in parallel mode
            result = self.__runTestsInParallel(
                output_buffer,
                error_buffer
            )
        else:
            # Run tests sequentially (default)
            result = self.__runTestsSequentially(
                output_buffer,
                error_buffer
            )

        # Return the test result along with the captured output and error buffers
        return result, output_buffer, error_buffer

    def __resolveFlattenedTestSuite(
        self
    ) -> unittest.TestSuite:
        """
        Resolves and injects dependencies for all test cases in the suite, returning a flattened TestSuite.

        This method processes each test case in the internal suite, inspects the test method signatures,
        and uses the application's dependency resolver to inject any required dependencies. It handles
        decorated methods, methods without dependencies, and raises errors for unresolved dependencies.
        The result is a new, flat unittest.TestSuite containing test cases with all dependencies resolved
        and injected, ready for execution.

        Parameters
        ----------
        None

        Returns
        -------
        unittest.TestSuite
            A new TestSuite containing all test cases from the original suite, with dependencies injected
            where required. Test cases with unresolved dependencies will cause an exception to be raised.

        Raises
        ------
        OrionisTestValueError
            If any test method has dependencies that cannot be resolved.

        Notes
        -----
        - Decorated test methods are left unchanged and added as-is.
        - Test methods without dependencies are added directly.
        - Test methods with unresolved dependencies will trigger an error.
        - The returned TestSuite is flat and contains all processed test cases.
        """

        # Create a new test suite to hold test cases with dependencies resolved
        flattened_suite = unittest.TestSuite()

        # Iterate through all test cases in the original (possibly nested) suite
        for test_case in self.__flattenTestSuite(self.__suite):

            # If it's a failed test, add it as-is to the flattened suite
            if test_case.__class__.__name__ == "_FailedTest":
                flattened_suite.addTest(test_case)
                continue

            # Get the test method name using reflection
            rf_instance = ReflectionInstance(test_case)
            method_name = rf_instance.getAttribute("_testMethodName")

            # If no method name is found, add the test case as-is
            if not method_name:
                flattened_suite.addTest(test_case)
                continue

            # Retrieve the actual test method object from the class
            test_method = getattr(test_case.__class__, method_name, None)

            # Check if the test method is decorated by looking for __wrapped__ attributes
            decorators = []
            if hasattr(test_method, '__wrapped__'):
                original = test_method
                while hasattr(original, '__wrapped__'):
                    # Collect decorator names for informational purposes
                    if hasattr(original, '__qualname__'):
                        decorators.append(original.__qualname__)
                    elif hasattr(original, '__name__'):
                        decorators.append(original.__name__)
                    original = original.__wrapped__

            # If decorators are present, add the test case as-is (do not inject dependencies)
            if decorators:
                flattened_suite.addTest(test_case)
                continue

            # Attempt to extract dependency information from the test method signature
            signature = rf_instance.getMethodDependencies(method_name)

            # If there are no dependencies to resolve, or unresolved dependencies exist, add as-is
            if ((not signature.resolved and not signature.unresolved) or (not signature.resolved and len(signature.unresolved) > 0)):
                flattened_suite.addTest(test_case)
                continue

            # If there are unresolved dependencies, raise an error
            if (len(signature.unresolved) > 0):
                raise OrionisTestValueError(
                    f"Test method '{method_name}' in class '{test_case.__class__.__name__}' has unresolved dependencies: {signature.unresolved}. "
                    "Please ensure all dependencies are correctly defined and available."
                )

            # All dependencies are resolved; prepare to inject them into the test method
            test_class = ReflectionInstance(test_case).getClass()
            original_method = getattr(test_class, method_name)

            # Resolve dependencies using the application's resolver
            params = Resolver(self.__app).resolveSignature(signature)

            # Create a wrapper function that injects resolved dependencies into the test method
            def create_test_wrapper(original_test, resolved_args: dict):
                def wrapper(self_instance):
                    return original_test(self_instance, **resolved_args)
                return wrapper

            # Wrap the original test method with the dependency-injecting wrapper
            wrapped_method = create_test_wrapper(original_method, params)

            # Bind the wrapped method to the test case instance
            bound_method = wrapped_method.__get__(test_case, test_case.__class__)

            # Replace the original test method on the test case with the wrapped version
            setattr(test_case, method_name, bound_method)

            # Add the modified test case to the flattened suite
            flattened_suite.addTest(test_case)

        # Return the new flattened suite with all dependencies resolved and injected
        return flattened_suite

    def __runTestsSequentially(
        self,
        output_buffer: io.StringIO,
        error_buffer: io.StringIO
    ) -> unittest.TestResult:
        """
        Executes the test suite sequentially, capturing the output and error streams.

        Parameters
        ----------
        output_buffer : io.StringIO
            A buffer to capture the standard output during test execution.
        error_buffer : io.StringIO
            A buffer to capture the standard error during test execution.

        Returns
        -------
        unittest.TestResult
            The result of the test suite execution, containing information about
            passed, failed, and skipped tests.
        """

        # Create a custom result class to capture detailed test results
        result = None
        for case in self.__resolveFlattenedTestSuite():

            if not isinstance(case, unittest.TestCase):
                raise OrionisTestValueError(
                    f"Invalid test case type: Expected unittest.TestCase, got {type(case).__name__}."
                )

            with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
                runner = unittest.TextTestRunner(
                    stream=output_buffer,
                    verbosity=self.__verbosity,
                    failfast=self.__fail_fast,
                    resultclass=self.__customResultClass()
                )
                single_result: IOrionisTestResult = runner.run(unittest.TestSuite([case]))

            # Print a concise summary for each test.
            self.__printer.unittestResult(single_result.test_results[0])

            # Merge results
            if result is None:
                result = single_result
            else:
                self.__mergeTestResults(result, single_result)

        # Return the result object containing test outcomes
        return result

    def __runTestsInParallel(
        self,
        output_buffer: io.StringIO,
        error_buffer: io.StringIO
    ) -> unittest.TestResult:
        """
        Executes all test cases in the test suite concurrently using a thread pool,
        aggregating their results into a single result object. Standard output and error
        streams are redirected to the provided buffers during execution.

        This method is designed to speed up test execution by running multiple test cases
        in parallel threads, making use of the configured maximum number of workers. Each
        test case is executed in isolation, and their results are merged into a combined
        result object. If the `fail_fast` option is enabled and a test fails, remaining
        tests are canceled as soon as possible.

        Parameters
        ----------
        output_buffer : io.StringIO
            Buffer to capture standard output produced during test execution.
        error_buffer : io.StringIO
            Buffer to capture standard error produced during test execution.

        Returns
        -------
        unittest.TestResult
            A combined result object (instance of the custom result class) containing
            the aggregated outcomes of all executed tests, including detailed information
            about passed, failed, errored, and skipped tests.

        Notes
        -----
        - Uses a custom result class to collect detailed test outcomes.
        - If `fail_fast` is enabled and a test fails, remaining tests are canceled.
        - Output and error streams are captured for the entire parallel execution.
        """

        # Flatten the test suite to get individual test cases
        test_cases = list(self.__resolveFlattenedTestSuite())

        # Create a custom result instance to collect all results
        result_class = self.__customResultClass()
        combined_result = result_class(io.StringIO(), descriptions=True, verbosity=self.__verbosity)

        # Helper function to run a single test and return its result.
        # Each test runs in its own thread with minimal output.
        def run_single_test(test):
            runner = unittest.TextTestRunner(
                stream=io.StringIO(),  # Use a dummy stream for individual test output
                verbosity=0,
                failfast=False,
                resultclass=result_class
            )
            # Run the test and return its result object
            return runner.run(unittest.TestSuite([test]))

        # Redirect stdout and stderr to the provided buffers during parallel execution
        with redirect_stdout(output_buffer), redirect_stderr(error_buffer):

            # Create a ThreadPoolExecutor to run tests in parallel
            with ThreadPoolExecutor(max_workers=self.__max_workers) as executor:

                # Submit all test cases to the executor
                futures = [executor.submit(run_single_test, test) for test in test_cases]

                # Process the results as they complete
                for future in as_completed(futures):
                    test_result = future.result()
                    # Merge each individual test result into the combined result
                    self.__mergeTestResults(combined_result, test_result)

                    # If fail_fast is enabled and a test failed, cancel remaining futures
                    if self.__fail_fast and not combined_result.wasSuccessful():
                        for f in futures:
                            f.cancel()
                        break

        # Print a concise summary for each test in the combined result
        for test_result in combined_result.test_results:
            self.__printer.unittestResult(test_result)

        # Return the combined result object containing all test outcomes
        return combined_result

    def __mergeTestResults(
        self,
        combined_result: unittest.TestResult,
        individual_result: unittest.TestResult
    ) -> None:
        """
        Merge the results of two unittest.TestResult objects into a single result.

        This method updates the `combined_result` object by aggregating the test run counts,
        failures, errors, skipped tests, expected failures, and unexpected successes from the
        `individual_result` object. It also merges any custom test results stored in the
        `test_results` attribute, if present, ensuring that all detailed test outcomes are
        included in the combined result.

        Parameters
        ----------
        combined_result : unittest.TestResult
            The TestResult object that will be updated to include the results from `individual_result`.
        individual_result : unittest.TestResult
            The TestResult object whose results will be merged into `combined_result`.

        Returns
        -------
        None
            This method does not return a value. It modifies `combined_result` in place.

        Notes
        -----
        - The method aggregates all relevant test outcome lists and counters.
        - If the `test_results` attribute exists (for custom result classes), it is also merged.
        - This is useful for combining results from parallel or sequential test executions.
        """

        # Aggregate the number of tests run
        combined_result.testsRun += individual_result.testsRun

        # Extend the lists of failures, errors, skipped, expected failures, and unexpected successes
        combined_result.failures.extend(individual_result.failures)
        combined_result.errors.extend(individual_result.errors)
        combined_result.skipped.extend(individual_result.skipped)
        combined_result.expectedFailures.extend(individual_result.expectedFailures)
        combined_result.unexpectedSuccesses.extend(individual_result.unexpectedSuccesses)

        # Merge custom test results if present (for enhanced result tracking)
        if hasattr(individual_result, 'test_results'):
            if not hasattr(combined_result, 'test_results'):
                combined_result.test_results = []
            combined_result.test_results.extend(individual_result.test_results)

    def __customResultClass(
        self
    ) -> type:
        """
        Creates a custom test result class for enhanced test tracking.
        This method dynamically generates an `OrionisTestResult` class that extends
        `unittest.TextTestResult`. The custom class provides advanced functionality for
        tracking test execution details, including timings, statuses, and error information.

        Returns
        -------
        type
            A dynamically created class `OrionisTestResult` that overrides methods to handle
            test results, including success, failure, error, and skipped tests. The class
            collects detailed information about each test, such as execution time, error
            messages, traceback, and file path.

        Notes
        -----
        The `OrionisTestResult` class includes the following method overrides:
        The method uses the `this` reference to access the outer class's methods, such as
        `_extractErrorInfo`, for extracting and formatting error information.
        """

        # Use `this` to refer to the outer class instance
        this = self

        # Define the custom test result class
        class OrionisTestResult(unittest.TextTestResult):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.test_results = []
                self._test_timings = {}
                self._current_test_start = None

            def startTest(self, test):
                self._current_test_start = time.time()
                super().startTest(test)

            def stopTest(self, test):
                elapsed = time.time() - self._current_test_start
                self._test_timings[test] = elapsed
                super().stopTest(test)

            def addSuccess(self, test):
                super().addSuccess(test)
                elapsed = self._test_timings.get(test, 0.0)
                self.test_results.append(
                    TestResult(
                        id=test.id(),
                        name=str(test),
                        status=TestStatus.PASSED,
                        execution_time=elapsed,
                        class_name=test.__class__.__name__,
                        method=ReflectionInstance(test).getAttribute("_testMethodName"),
                        module=ReflectionInstance(test).getModuleName(),
                        file_path=ReflectionInstance(test).getFile(),
                        doc_string=ReflectionInstance(test).getMethodDocstring(test._testMethodName),
                    )
                )

            def addFailure(self, test, err):
                super().addFailure(test, err)
                elapsed = self._test_timings.get(test, 0.0)
                tb_str = ''.join(traceback.format_exception(*err))
                file_path, clean_tb = this._extractErrorInfo(tb_str)
                self.test_results.append(
                    TestResult(
                        id=test.id(),
                        name=str(test),
                        status=TestStatus.FAILED,
                        execution_time=elapsed,
                        error_message=str(err[1]),
                        traceback=clean_tb,
                        class_name=test.__class__.__name__,
                        method=ReflectionInstance(test).getAttribute("_testMethodName"),
                        module=ReflectionInstance(test).getModuleName(),
                        file_path=ReflectionInstance(test).getFile(),
                        doc_string=ReflectionInstance(test).getMethodDocstring(test._testMethodName),
                    )
                )

            def addError(self, test, err):
                super().addError(test, err)
                elapsed = self._test_timings.get(test, 0.0)
                tb_str = ''.join(traceback.format_exception(*err))
                file_path, clean_tb = this._extractErrorInfo(tb_str)
                self.test_results.append(
                    TestResult(
                        id=test.id(),
                        name=str(test),
                        status=TestStatus.ERRORED,
                        execution_time=elapsed,
                        error_message=str(err[1]),
                        traceback=clean_tb,
                        class_name=test.__class__.__name__,
                        method=ReflectionInstance(test).getAttribute("_testMethodName"),
                        module=ReflectionInstance(test).getModuleName(),
                        file_path=ReflectionInstance(test).getFile(),
                        doc_string=ReflectionInstance(test).getMethodDocstring(test._testMethodName),
                    )
                )

            def addSkip(self, test, reason):
                super().addSkip(test, reason)
                elapsed = self._test_timings.get(test, 0.0)
                self.test_results.append(
                    TestResult(
                        id=test.id(),
                        name=str(test),
                        status=TestStatus.SKIPPED,
                        execution_time=elapsed,
                        error_message=reason,
                        class_name=test.__class__.__name__,
                        method=ReflectionInstance(test).getAttribute("_testMethodName"),
                        module=ReflectionInstance(test).getModuleName(),
                        file_path=ReflectionInstance(test).getFile(),
                        doc_string=ReflectionInstance(test).getMethodDocstring(test._testMethodName)
                    )
                )

        # Return the dynamically created OrionisTestResult class
        return OrionisTestResult

    def _extractErrorInfo(
        self,
        traceback_str: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts the file path and a cleaned traceback from a given traceback string.

        This method analyzes a Python traceback string to determine the file path of the Python file
        where the error occurred (typically the last file in the traceback). It also removes lines
        related to framework internals and irrelevant noise, such as those containing 'unittest/', 
        'lib/python', or 'site-packages', to produce a more concise and relevant traceback for reporting.

        Parameters
        ----------
        traceback_str : str
            The full traceback string to process.

        Returns
        -------
        Tuple[Optional[str], Optional[str]]
            A tuple containing:
                - file_path (Optional[str]): The path to the Python file where the error occurred, or None if not found.
                - clean_tb (Optional[str]): The cleaned traceback string, with framework internals and unrelated lines removed.

        Notes
        -----
        The cleaned traceback starts from the first occurrence of the test file path and omits lines
        that are part of the Python standard library or third-party packages, focusing on user code.
        """

        # Extract all Python file paths from the traceback string
        file_matches = re.findall(r'File ["\'](.*?.py)["\']', traceback_str)

        # Use the last file in the traceback as the most relevant (where the error occurred)
        file_path = file_matches[-1] if file_matches else None

        # Split the traceback into individual lines for processing
        tb_lines = traceback_str.split('\n')
        clean_lines = []
        relevant_lines_started = False

        # Iterate through each line in the traceback
        for line in tb_lines:

            # Skip lines that are part of framework internals or third-party libraries
            if any(s in line for s in ['unittest/', 'lib/python', 'site-packages']):
                continue

            # Start including lines once the relevant file path is found
            if file_path and file_path in line and not relevant_lines_started:
                relevant_lines_started = True

            # If we've started collecting relevant lines, add them to the cleaned traceback
            if relevant_lines_started:
                clean_lines.append(line)

        # Join the cleaned lines into a single string; if none, return the original traceback
        clean_tb = str('\n').join(clean_lines) if clean_lines else traceback_str

        # Return the file path and cleaned traceback
        return file_path, clean_tb

    def __generateSummary(
        self,
        result: unittest.TestResult,
        execution_time: float
    ) -> Dict[str, Any]:
        """
        Generates a comprehensive summary of the test suite execution.

        This method processes the provided unittest.TestResult object and aggregates
        statistics such as the total number of tests, counts of passed, failed, errored,
        and skipped tests, as well as the overall execution time and success rate.
        It also collects detailed information for each individual test, including
        identifiers, class and method names, status, execution time, error messages,
        tracebacks, file paths, and docstrings.

        If result persistence is enabled, the summary is saved using the configured
        persistence driver (e.g., SQLite or JSON). If web reporting is enabled, a
        web report is generated and linked.

        Parameters
        ----------
        result : unittest.TestResult
            The result object containing details of the test execution.
        execution_time : float
            The total execution time of the test suite in milliseconds.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing:
                - total_tests (int): Total number of tests executed.
                - passed (int): Number of tests that passed.
                - failed (int): Number of tests that failed.
                - errors (int): Number of tests that encountered errors.
                - skipped (int): Number of tests that were skipped.
                - total_time (float): Total execution time in milliseconds.
                - success_rate (float): Percentage of tests that passed.
                - test_details (List[Dict[str, Any]]): List of dictionaries with details for each test,
                  including id, class, method, status, execution_time, error_message, traceback,
                  file_path, and doc_string.
                - timestamp (str): ISO-formatted timestamp of when the summary was generated.

        Side Effects
        ------------
        - If persistence is enabled, the summary is persisted to storage.
        - If web reporting is enabled, a web report is generated.
        """

        test_details = []

        # Collect detailed information for each test result
        for test_result in result.test_results:
            rst: TestResult = test_result
            test_details.append({
                'id': rst.id,
                'class': rst.class_name,
                'method': rst.method,
                'status': rst.status.name,
                'execution_time': float(rst.execution_time),
                'error_message': rst.error_message,
                'traceback': rst.traceback,
                'file_path': rst.file_path,
                'doc_string': rst.doc_string
            })

        # Calculate the number of passed tests
        passed = result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)
        # Calculate the success rate as a percentage
        success_rate = (passed / result.testsRun * 100) if result.testsRun > 0 else 100.0

        # Build the summary dictionary
        self.__result = {
            "total_tests": result.testsRun,
            "passed": passed,
            "failed": len(result.failures),
            "errors": len(result.errors),
            "skipped": len(result.skipped),
            "total_time": float(execution_time),
            "success_rate": success_rate,
            "test_details": test_details,
            "timestamp": datetime.now().isoformat()
        }

        # Persist the summary if persistence is enabled
        if self.__persistent:
            self.__handlePersistResults(self.__result)

        # Generate a web report if web reporting is enabled
        if self.__web_report:
            self.__handleWebReport(self.__result)

        # Return the summary dictionary
        return self.__result

    def __handleWebReport(
        self,
        summary: Dict[str, Any]
    ) -> None:
        """
        Generate a web-based report for the provided test results summary.

        This method creates a web report for the test execution summary using the `TestingResultRender` class.
        It determines the appropriate storage path for the report, configures persistence options based on the
        current settings, and invokes the rendering process. After generating the report, it prints a link to
        the web report using the configured printer.

        Parameters
        ----------
        summary : dict
            The summary of test results for which the web report will be generated.

        Returns
        -------
        None
            This method does not return any value. The generated web report is rendered and a link to it is printed
            to the console via the printer.

        Notes
        -----
        - The storage path for the report is determined by `self.__base_path`.
        - If result persistence is enabled and the driver is set to 'sqlite', the report is marked as persistent.
        - The web report is generated using the `TestingResultRender` class.
        - The method prints the link to the generated web report using the printer.
        """

        # Create the TestingResultRender instance with the storage path and summary.
        render = TestingResultRender(
            storage_path=self.__storage,
            result=summary,
            persist=self.__persistent and self.__persistent_driver == 'sqlite'
        )

        # Render the web report and print the link using the printer.
        self.__printer.linkWebReport(render.render())

    def __handlePersistResults(
        self,
        summary: Dict[str, Any]
    ) -> None:
        """
        Persist the test results summary using the configured persistence driver.

        This method saves the provided test results summary to persistent storage, based on the
        current configuration. Supported drivers include SQLite (using the TestLogs class) and
        JSON file output. The storage location is determined by the configured base path.

        Parameters
        ----------
        summary : dict
            The summary of test results to persist. This should include all relevant test execution
            details, such as test counts, statuses, execution times, and individual test results.

        Returns
        -------
        None
            This method does not return any value. It performs persistence as a side effect.

        Raises
        ------
        OSError
            If there is an error creating directories or writing files to disk.
        OrionisTestPersistenceError
            If database operations fail or any other error occurs during persistence.

        Notes
        -----
        - If `self.__persistent_driver` is set to 'sqlite', the summary is stored in an SQLite database
          using the TestLogs class.
        - If `self.__persistent_driver` is set to 'json', the summary is written to a timestamped JSON
          file in the specified base path.
        - The method ensures that the target directory exists before writing files.
        - Any errors encountered during persistence are raised as exceptions for the caller to handle.
        """

        try:

            if self.__persistent_driver == PersistentDrivers.SQLITE.value:

                # Persist results to SQLite database using TestLogs
                history = TestLogs(self.__storage)

                # Insert the summary into the database
                history.create(summary)

            elif self.__persistent_driver == PersistentDrivers.JSON.value:

                # Generate a timestamp for the log file name
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                # Construct the log file path with the timestamp
                log_path = Path(self.__storage) / f"{timestamp}_test_results.json"

                # Ensure the directory exists
                log_path.parent.mkdir(parents=True, exist_ok=True)

                # Write the summary dictionary to the JSON file
                with open(log_path, 'w', encoding='utf-8') as log:
                    json.dump(summary, log, indent=4)

        except OSError as e:

            # Raise an OSError if there is an issue with file or directory operations
            raise OSError(f"Error creating directories or writing files: {str(e)}")

        except Exception as e:

            # Raise a custom exception for any other issues during persistence
            raise OrionisTestPersistenceError(f"Error persisting test results: {str(e)}")

    def __filterTestsByName(
        self,
        suite: unittest.TestSuite,
        pattern: str
    ) -> unittest.TestSuite:
        """
        Filters tests in a given test suite based on a specified name pattern.
        Parameters
        ----------
        suite : unittest.TestSuite
            The test suite containing the tests to filter.
        pattern : str
            A regular expression pattern to match test names.
        Returns
        -------
        unittest.TestSuite
            A new test suite containing only the tests that match the pattern.
        Raises
        ------
        OrionisTestValueError
            If the provided pattern is not a valid regular expression.
        Notes
        -----
        """

        # Initialize an empty TestSuite to hold the filtered tests
        filtered_suite = unittest.TestSuite()

        # Validate the pattern
        try:
            regex = re.compile(pattern)
        except re.error as e:
            raise OrionisTestValueError(
                f"The provided test name pattern is invalid: '{pattern}'. "
                f"Regular expression compilation error: {str(e)}. "
                "Please check the pattern syntax and try again."
            )

        # Iterate through all tests in the suite and filter by the regex pattern
        for test in self.__flattenTestSuite(suite):
            if regex.search(test.id()):
                filtered_suite.addTest(test)

        # Return the filtered suite containing only tests that match the pattern
        return filtered_suite

    def __filterTestsByTags(
        self,
        suite: unittest.TestSuite,
        tags: List[str]
    ) -> unittest.TestSuite:
        """
        Filter tests in a unittest TestSuite by specified tags.

        Iterates through all tests in the provided TestSuite and checks for a `__tags__`
        attribute either on the test method or the test case class. If any of the specified
        tags match the tags associated with the test, the test is included in the filtered suite.

        Parameters
        ----------
        suite : unittest.TestSuite
            The original TestSuite containing all tests.
        tags : list of str
            List of tags to filter the tests by.

        Returns
        -------
        unittest.TestSuite
            A new TestSuite containing only the tests that match the specified tags.
        """

        # Initialize an empty TestSuite to hold the filtered tests
        filtered_suite = unittest.TestSuite()
        tag_set = set(tags)

        for test in self.__flattenTestSuite(suite):

            # Get test method if this is a TestCase instance
            test_method = getattr(test, test._testMethodName, None)

            # Check for tags attribute on the test method
            if hasattr(test_method, '__tags__'):
                method_tags = set(getattr(test_method, '__tags__'))
                if tag_set.intersection(method_tags):
                    filtered_suite.addTest(test)

            # Also check on the test case class
            elif hasattr(test, '__tags__'):
                class_tags = set(getattr(test, '__tags__'))
                if tag_set.intersection(class_tags):
                    filtered_suite.addTest(test)

        # Return the filtered suite containing only tests with matching tags
        return filtered_suite

    def getTestNames(
        self
    ) -> List[str]:
        """
        Get a list of test names (unique identifiers) from the test suite.

        Returns
        -------
        List[str]
            List of test names (unique identifiers) from the test suite.
        """
        return [test.id() for test in self.__flattenTestSuite(self.__suite)]

    def getTestCount(
        self
    ) -> int:
        """
        Returns the total number of test cases in the test suite.

        Returns
        -------
        int
            The total number of individual test cases in the suite.
        """
        return len(list(self.__flattenTestSuite(self.__suite)))

    def clearTests(
        self
    ) -> None:
        """
        Clear all tests from the current test suite.

        Resets the internal test suite to an empty `unittest.TestSuite`, removing any previously added tests.
        """
        self.__suite = unittest.TestSuite()

    def getResult(
        self
    ) -> dict:
        """
        Returns the results of the executed test suite.

        Returns
        -------
        UnitTest
            The result of the executed test suite.
        """
        return self.__result

    def getOutputBuffer(
        self
    ) -> int:
        """
        Returns the output buffer used for capturing test results.
        This method returns the internal output buffer that collects the results of the test execution.
        Returns
        -------
        int
            The output buffer containing the results of the test execution.
        """
        return self.__output_buffer

    def printOutputBuffer(
        self
    ) -> None:
        """
        Prints the contents of the output buffer to the console.
        This method retrieves the output buffer and prints its contents using the rich console.
        """
        self.__printer.print(self.__output_buffer)

    def getErrorBuffer(
        self
    ) -> int:
        """
        Returns the error buffer used for capturing test errors.
        This method returns the internal error buffer that collects any errors encountered during test execution.
        Returns
        -------
        int
            The error buffer containing the errors encountered during the test execution.
        """
        return self.__error_buffer

    def printErrorBuffer(
        self
    ) -> None:
        """
        Prints the contents of the error buffer to the console.
        This method retrieves the error buffer and prints its contents using the rich console.
        """
        self.__printer.print(self.__error_buffer)