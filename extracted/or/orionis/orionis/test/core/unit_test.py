import io
import json
import os
import re
import time
import traceback
import unittest
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime
from importlib import import_module
from os import walk
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from orionis.foundation.config.testing.entities.testing import Testing
from orionis.foundation.config.testing.enums.drivers import PersistentDrivers
from orionis.foundation.config.testing.enums.mode import ExecutionMode
from orionis.foundation.contracts.application import IApplication
from orionis.services.introspection.instances.reflection import ReflectionInstance
from orionis.support.performance.contracts.counter import IPerformanceCounter
from orionis.test.contracts.test_result import IOrionisTestResult
from orionis.test.contracts.unit_test import IUnitTest
from orionis.test.entities.result import TestResult
from orionis.test.enums import TestStatus
from orionis.test.exceptions import OrionisTestValueError, OrionisTestFailureException, OrionisTestPersistenceError
from orionis.test.output.printer import TestPrinter
from orionis.test.records.logs import TestLogs
from orionis.test.validators import (
    ValidBasePath,
    ValidExecutionMode,
    ValidFailFast,
    ValidFolderPath,
    ValidModuleName,
    ValidNamePattern,
    ValidPattern,
    ValidPersistentDriver,
    ValidPersistent,
    ValidPrintResult,
    ValidThrowException,
    ValidVerbosity,
    ValidWebReport,
    ValidWorkers,
)
from orionis.test.view.render import TestingResultRender

class UnitTest(IUnitTest):
    """
    Orionis UnitTest

    Advanced unit testing manager for the Orionis framework.

    This class provides mechanisms for discovering, executing, and reporting unit tests with extensive configurability.
    It supports sequential and parallel execution, test filtering by name or tags, and detailed result tracking including
    execution times, error messages, and tracebacks. The UnitTest manager integrates with the Orionis application for
    dependency injection, configuration loading, and result persistence.

    Parameters
    ----------
    app : IApplication
        The application instance used for dependency injection, configuration access, and path resolution.

    Notes
    -----
    - The application instance is stored for later use in dependency resolution and configuration access.
    - The test loader and suite are initialized for test discovery and execution.
    - Output buffers, paths, configuration, modules, and tests are loaded in sequence to prepare the test manager.
    - Provides methods for running tests, retrieving results, and printing output/error buffers.
    """

    def __init__(
        self,
        app: IApplication
    ) -> None:
        """
        Initialize the UnitTest manager for the Orionis framework.

        This constructor sets up the internal state required for advanced unit testing,
        including dependency injection, configuration loading, test discovery, and result tracking.
        It initializes the application instance, test loader, test suite, module list, and result storage.
        The constructor also loads output buffers, paths, configuration, test modules, and discovered tests.

        Parameters
        ----------
        app : IApplication
            The application instance used for dependency injection, configuration access, and path resolution.

        Returns
        -------
        None
            This method does not return a value. It initializes the internal state of the UnitTest instance.

        Notes
        -----
        - The application instance is stored for later use in dependency resolution and configuration access.
        - The test loader and suite are initialized for test discovery and execution.
        - Output buffers, paths, configuration, modules, and tests are loaded in sequence to prepare the test manager.
        """

        # Store the application instance for dependency injection and configuration access
        self.__app: IApplication = app

        # Initialize the unittest loader for discovering test cases
        self.__loader = unittest.TestLoader()

        # Initialize the test suite to hold discovered tests
        self.__suite = unittest.TestSuite()

        # List to store imported test modules
        self.__modules: List = []

        # List to track discovered tests and their metadata
        self.__discovered_tests: List = []

        # Variable to store the result summary after test execution
        self.__result: Optional[Dict[str, Any]] = None

        # Load the output and error buffers for capturing test execution output
        self.__loadOutputBuffer()

        # Load and set internal paths for test discovery and result storage
        self.__loadPaths()

        # Load and validate the testing configuration from the application
        self.__loadConfig()

        # Discover and import test modules based on the configuration
        self.__loadModules()

        # Discover and load all test cases from the imported modules into the suite
        self.__loadTests()

    def __loadOutputBuffer(
        self
    ) -> None:
        """
        Load the output buffer from the last test execution.

        This method retrieves the output buffer containing standard output generated during
        the last test run. It stores the output as a string in an internal attribute for later access.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return a value. It sets the internal output buffer attribute.
        """
        self.__output_buffer = None
        self.__error_buffer = None

    def __loadPaths(
        self
    ) -> None:
        """
        Load and set internal paths required for test discovery and result storage.

        This method retrieves the base test path, project root path, and storage path from the application instance.
        It then sets the internal attributes for the test path, root path, base path (relative to the project root),
        and the absolute storage path for test results.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It sets internal attributes for test and storage paths.

        Notes
        -----
        - The base path is computed as the relative path from the test directory to the project root.
        - The storage path is set to an absolute path for storing test results under 'testing/results'.
        """

        # Get the base test path and project root path from the application
        self.__test_path = ValidBasePath(self.__app.path('tests'))
        self.__root_path = ValidBasePath(self.__app.path('root'))

        # Compute the base path for test discovery, relative to the project root
        # Remove the root path prefix and leading slash
        self.__base_path: Optional[str] = self.__test_path.as_posix().replace(self.__root_path.as_posix(), '')[1:]

        # Get the storage path from the application and set the absolute path for test results
        storage_path = self.__app.path('storage')
        self.__storage: Path = (storage_path / 'testing' / 'results').resolve()

    def __loadConfig(
        self
    ) -> None:
        """
        Load and validate the testing configuration from the application.

        This method retrieves the testing configuration from the application instance,
        validates each configuration parameter, and updates the internal state of the
        UnitTest instance accordingly. It ensures that all required fields are present
        and correctly formatted.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return a value. It updates the internal state of the UnitTest instance.

        Raises
        ------
        OrionisTestValueError
            If the testing configuration is invalid or missing required fields.
        """

        # Load the testing configuration from the application
        try:
            config = Testing(**self.__app.config('testing'))
        except Exception as e:
            raise OrionisTestValueError(
                f"Failed to load testing configuration: {str(e)}. "
                "Please ensure the testing configuration is correctly defined in the application settings."
            )

        # Set verbosity level for test output
        self.__verbosity: Optional[int] = ValidVerbosity(config.verbosity)

        # Set execution mode (sequential or parallel)
        self.__execution_mode: Optional[str] = ValidExecutionMode(config.execution_mode)

        # Set maximum number of workers for parallel execution
        self.__max_workers: Optional[int] = ValidWorkers(config.max_workers)

        # Set fail-fast behavior (stop on first failure)
        self.__fail_fast: Optional[bool] = ValidFailFast(config.fail_fast)

        # Set whether to throw an exception if tests fail
        self.__throw_exception: Optional[bool] = ValidThrowException(config.throw_exception)

        # Set persistence flag for saving test results
        self.__persistent: Optional[bool] = ValidPersistent(config.persistent)

        # Set the persistence driver (e.g., 'sqlite', 'json')
        self.__persistent_driver: Optional[str] = ValidPersistentDriver(config.persistent_driver)

        # Set web report flag for generating web-based test reports
        self.__web_report: Optional[bool] = ValidWebReport(config.web_report)

        # Initialize the printer for console output
        self.__printer = TestPrinter(
            print_result = ValidPrintResult(config.print_result)
        )

        # Set the file name pattern for test discovery
        self.__pattern: Optional[str] = ValidPattern(config.pattern)

        # Set the test method name pattern for filtering
        self.__test_name_pattern: Optional[str] = ValidNamePattern(config.test_name_pattern)

        # Set the folder(s) where test files are located
        folder_path = config.folder_path

        # If folder_path is a list, validate each entry
        if isinstance(folder_path, list):

            # Clean and validate each folder path in the list
            cleaned_folders = []

            # Validate each folder path in the list
            for folder in folder_path:

                # If any folder is invalid, raise an error
                if not isinstance(folder, str) or not folder.strip():
                    raise OrionisTestValueError(
                        f"Invalid 'folder_path' configuration: expected '*' or a list of relative folder paths, got {repr(folder_path)}."
                    )

                # Remove leading/trailing slashes and base path
                scope_folder = folder.strip().lstrip("/\\").rstrip("/\\")

                # Make folder path relative to base path if it starts with it
                if scope_folder.startswith(self.__base_path):
                    scope_folder = scope_folder[len(self.__base_path):].lstrip("/\\")
                if not scope_folder:
                    raise OrionisTestValueError(
                        f"Invalid 'folder_path' configuration: expected '*' or a list of relative folder paths, got {repr(folder_path)}."
                    )

                # Add the cleaned folder path to the list
                cleaned_folders.append(ValidFolderPath(scope_folder))

            # Store the cleaned list of folder paths
            self.__folder_path: Optional[List[str]] = cleaned_folders

        elif isinstance(folder_path, str) and folder_path == '*':

            # Use wildcard to search all folders
            self.__folder_path: Optional[str] = '*'

        else:

            # Invalid folder_path configuration
            raise OrionisTestValueError(
                f"Invalid 'folder_path' configuration: expected '*' or a list of relative folder paths, got {repr(folder_path)}."
            )

    def __loadModules(
        self
    ) -> None:
        """
        Loads and validates Python modules for test discovery based on the configured folder paths and file patterns.

        This method determines which test modules to load by inspecting the `folder_path` configuration.
        If the folder path is set to '*', it discovers all modules matching the configured file pattern in the test directory.
        If the folder path is a list, it discovers modules in each specified subdirectory.
        The discovered modules are imported and stored in the internal state for later test discovery and execution.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It updates the internal state of the UnitTest instance by extending
            the `self.__modules` list with the discovered and imported module objects.

        Raises
        ------
        OrionisTestValueError
            If any module name or folder path is invalid, or if module discovery fails.

        Notes
        -----
        - Uses `__listMatchingModules` to find and import modules matching the file pattern.
        - Avoids duplicate modules by using a set.
        - Updates the internal module list for subsequent test discovery.
        """

        modules = set()  # Use a set to avoid duplicate module imports

        # If folder_path is '*', discover all modules matching the pattern in the test directory
        if self.__folder_path == '*':
            list_modules = self.__listMatchingModules(
                self.__root_path, self.__test_path, None, self.__pattern
            )
            modules.update(list_modules)

        # If folder_path is a list, discover modules in each specified subdirectory
        elif isinstance(self.__folder_path, list):
            for custom_path in self.__folder_path:
                list_modules = self.__listMatchingModules(
                    self.__root_path, self.__test_path, custom_path, self.__pattern
                )
                modules.update(list_modules)

        # Extend the internal module list with the sorted discovered modules
        self.__modules.extend(modules)

    def __loadTests(
        self
    ) -> None:
        """
        Discover and load all test cases from the imported test modules into the test suite.

        This method iterates through all imported test modules, loads their test cases,
        flattens nested suites, checks for failed imports, applies optional test name filtering,
        and adds the discovered tests to the main test suite. It also tracks the number of discovered
        tests per module and raises detailed errors for import failures or missing tests.

        Returns
        -------
        None

        Raises
        ------
        OrionisTestValueError
            If a test module fails to import, or if no tests are found matching the provided patterns.

        Notes
        -----
        - Uses `__flattenTestSuite` to extract individual test cases from each module.
        - Applies test name filtering if `self.__test_name_pattern` is set.
        - Updates `self.__suite` and `self.__discovered_tests` with discovered tests and metadata.
        - Provides detailed error messages for failed imports and missing tests.
        """
        try:

            # Iterate through all imported test modules
            for test_module in self.__modules:

                # Load all tests from the current module
                module_suite = self.__loader.loadTestsFromModule(test_module)

                # Flatten the suite to get individual test cases
                flat_tests = self.__flattenTestSuite(module_suite)

                # Check for failed imports and raise a detailed error if found
                for test in flat_tests:
                    if test.__class__.__name__ == "_FailedTest":
                        error_message = ""
                        if hasattr(test, "_exception"):
                            error_message = str(test._exception)
                        elif hasattr(test, "_outcome") and hasattr(test._outcome, "errors"):
                            error_message = str(test._outcome.errors)
                        else:
                            error_message = str(test)
                        raise OrionisTestValueError(
                            f"Failed to import test module: {test.id()}.\n"
                            f"Error details: {error_message}\n"
                            "Please check for import errors or missing dependencies."
                        )

                # Rebuild the suite with only valid tests
                valid_suite = unittest.TestSuite(flat_tests)

                # If a test name pattern is provided, filter tests by name
                if self.__test_name_pattern:
                    valid_suite = self.__filterTestsByName(
                        suite=valid_suite,
                        pattern=self.__test_name_pattern
                    )

                # If no tests are found, raise an error
                if not list(valid_suite):
                    raise OrionisTestValueError(
                        f"No tests found in module '{test_module.__name__}' matching file pattern '{self.__pattern}'"
                        + (f", test name pattern '{self.__test_name_pattern}'" if self.__test_name_pattern else "")
                        + ". Please check your patterns and test files."
                    )

                # Add discovered tests to the main suite
                self.__suite.addTests(valid_suite)

                # Count the number of tests discovered
                test_count = len(list(self.__flattenTestSuite(valid_suite)))

                # Append discovered tests information for reporting
                self.__discovered_tests.append({
                    "module": test_module.__name__,
                    "test_count": test_count,
                })

        except ImportError as e:

            # Raise a specific error if the import fails
            raise OrionisTestValueError(
                f"Error importing tests from module '{getattr(test_module, '__name__', str(test_module))}': {str(e)}.\n"
                "Please verify that the module and test files are accessible and correct."
            )

        except Exception as e:

            # Raise a general error for unexpected issues
            raise OrionisTestValueError(
                f"Unexpected error while discovering tests in module '{getattr(test_module, '__name__', str(test_module))}': {str(e)}.\n"
                "Ensure that the test files are valid and that there are no syntax errors or missing dependencies."
            )

    def run(
        self,
        performance_counter: IPerformanceCounter
    ) -> Dict[str, Any]:
        """
        Execute the test suite and return a summary of the results.

        Returns
        -------
        dict
            Dictionary summarizing the test results, including statistics and execution time.

        Raises
        ------
        OrionisTestFailureException
            If the test suite execution fails and throw_exception is True.
        """

        # Record the start time in seconds
        performance_counter.start()

        # Length of all tests in the suite
        total_tests = len(list(self.__flattenTestSuite(self.__suite)))

        # If no tests are found, print a message and return early
        if total_tests == 0:
            return self.__printer.zeroTestsMessage()

        # Print the start message with test suite details
        self.__printer.startMessage(
            length_tests=total_tests,
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
        performance_counter.stop()
        execution_time = performance_counter.getSeconds()

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
        Recursively flattens a unittest.TestSuite into a list of unique unittest.TestCase instances.

        Parameters
        ----------
        suite : unittest.TestSuite
            The test suite to be flattened.

        Returns
        -------
        List[unittest.TestCase]
            A flat list containing unique unittest.TestCase instances extracted from the suite.

        Notes
        -----
        Test uniqueness is determined by a shortened test identifier (the last two components of the test id).
        This helps avoid duplicate test cases in the returned list.
        """

        # Initialize an empty list to hold unique test cases and a set to track seen test IDs
        tests = []
        seen_ids = set()

        # Recursive function to flatten the test suite
        def _flatten(item):
            if isinstance(item, unittest.TestSuite):
                for sub_item in item:
                    _flatten(sub_item)
            elif hasattr(item, "id"):
                test_id = item.id()

                # Use the last two components of the test id for uniqueness
                parts = test_id.split('.')
                if len(parts) >= 2:
                    short_id = '.'.join(parts[-2:])
                else:
                    short_id = test_id
                if short_id not in seen_ids:
                    seen_ids.add(short_id)
                    tests.append(item)

        # Start the flattening process
        _flatten(suite)
        return tests

    def __runSuite(
        self
    ) -> Tuple[unittest.TestResult, io.StringIO, io.StringIO]:
        """
        Executes the test suite according to the configured execution mode, capturing both standard output and error streams.

        Returns
        -------
        tuple
            result : unittest.TestResult
                The result object containing the outcomes of the executed tests.
            output_buffer : io.StringIO
                Buffer capturing the standard output generated during test execution.
            error_buffer : io.StringIO
                Buffer capturing the standard error generated during test execution.
        """

        # Initialize output and error buffers to capture test execution output
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()

        # Run tests in parallel mode using multiple workers
        if self.__execution_mode == ExecutionMode.PARALLEL.value:
            result = self.__runTestsInParallel(
                output_buffer,
                error_buffer
            )

        # Run tests sequentially
        else:
            result = self.__runTestsSequentially(
                output_buffer,
                error_buffer
            )

        # Return the result, output, and error buffers
        return result, output_buffer, error_buffer

    def __isFailedImport(
        self,
        test_case: unittest.TestCase
    ) -> bool:
        """
        Check if the given test case is a failed import.

        Parameters
        ----------
        test_case : unittest.TestCase
            The test case to check.

        Returns
        -------
        bool
            True if the test case is a failed import, False otherwise.
        """

        return test_case.__class__.__name__ == "_FailedTest"

    def __notFoundTestMethod(
        self,
        test_case: unittest.TestCase
    ) -> bool:
        """
        Check if the test case does not have a valid test method.

        Parameters
        ----------
        test_case : unittest.TestCase
            The test case to check.

        Returns
        -------
        bool
            True if the test case does not have a valid test method, False otherwise.
        """

        # Use reflection to get the test method name
        rf_instance = ReflectionInstance(test_case)
        method_name = rf_instance.getAttribute("_testMethodName")

        # If no method name is found, return True indicating no valid test method
        return not method_name or not hasattr(test_case.__class__, method_name)

    def __isDecoratedMethod(
        self,
        test_case: unittest.TestCase
    ) -> bool:
        """
        Determine if the test case's test method is decorated (wrapped by decorators).

        This method examines the test method of a given test case to determine if it has been
        decorated with one or more Python decorators. It traverses the decorator chain by
        following the `__wrapped__` attribute to identify the presence of any decorators.
        Decorated methods typically have a `__wrapped__` attribute that points to the
        original unwrapped function.

        Parameters
        ----------
        test_case : unittest.TestCase
            The test case instance whose test method will be examined for decorators.

        Returns
        -------
        bool
            True if the test method has one or more decorators applied to it, False if
            the test method is not decorated or if no test method is found.

        Notes
        -----
        This method checks for decorators by examining the `__wrapped__` attribute chain.
        The method collects decorator names from `__qualname__` or `__name__` attributes
        as it traverses the wrapper chain. If any decorators are found in the chain,
        the method returns True.
        """

        # Retrieve the test method from the test case's class using the test method name
        test_method = getattr(test_case.__class__, getattr(test_case, "_testMethodName"), None)

        # Initialize a list to store decorator information found during traversal
        decorators = []

        # Check if the method has the __wrapped__ attribute, indicating it's decorated
        if hasattr(test_method, '__wrapped__'):
            # Start with the outermost decorated method
            original = test_method

            # Traverse the decorator chain by following __wrapped__ attributes
            while hasattr(original, '__wrapped__'):
                # Collect decorator name information for tracking purposes
                if hasattr(original, '__qualname__'):
                    # Prefer __qualname__ as it provides more detailed naming information
                    decorators.append(original.__qualname__)
                elif hasattr(original, '__name__'):
                    # Fall back to __name__ if __qualname__ is not available
                    decorators.append(original.__name__)

                # Move to the next level in the decorator chain
                original = original.__wrapped__

        # Return True if any decorators were found during the traversal
        if decorators:
            return True

        # Return False if no decorators are found or if the method is not decorated
        return False

    def __resolveFlattenedTestSuite(
        self
    ) -> unittest.TestSuite:
        """
        Resolves and injects dependencies for all test cases in the current suite, returning a flattened TestSuite.

        This method iterates through all test cases in the suite, checks for failed imports, decorated methods, and unresolved dependencies.
        For each test case, it uses reflection to determine the test method and its dependencies. If dependencies are required and can be resolved,
        it injects them using the application's resolver. If a test method has unresolved dependencies, an exception is raised.
        Decorated methods and failed imports are added as-is. The resulting TestSuite contains all test cases with dependencies injected where needed.

        Returns
        -------
        unittest.TestSuite
            A new TestSuite containing all test cases with dependencies injected as required.

        Raises
        ------
        OrionisTestValueError
            If any test method has unresolved dependencies that cannot be resolved by the resolver.
        """

        # Create a new TestSuite to hold the resolved test cases
        flattened_suite = unittest.TestSuite()

        # Iterate through all test cases in the flattened suite
        for test_case in self.__flattenTestSuite(self.__suite):

            # If the test case is a failed import, add it directly
            if self.__isFailedImport(test_case):
                flattened_suite.addTest(test_case)
                continue

            # If no method name is found, add the test case as-is
            if self.__notFoundTestMethod(test_case):
                flattened_suite.addTest(test_case)
                continue

            # If decorators are present, add the test case as-is
            if self.__isDecoratedMethod(test_case):
                flattened_suite.addTest(test_case)
                continue

            try:

                # Get the method's dependency signature
                rf_instance = ReflectionInstance(test_case)
                dependencies = rf_instance.getMethodDependencies(
                    method_name=getattr(test_case, "_testMethodName")
                )

                # If no dependencies are required or unresolved, add the test case as-is
                if ((not dependencies.resolved and not dependencies.unresolved) or (not dependencies.resolved and len(dependencies.unresolved) > 0)):
                    flattened_suite.addTest(test_case)
                    continue

                # If there are unresolved dependencies, raise an error
                if (len(dependencies.unresolved) > 0):
                    raise OrionisTestValueError(
                        f"Test method '{getattr(test_case, "_testMethodName")}' in class '{test_case.__class__.__name__}' has unresolved dependencies: {dependencies.unresolved}. "
                        "Please ensure all dependencies are correctly defined and available."
                    )

                # Get the original test class and method
                test_class = rf_instance.getClass()
                original_method = getattr(test_class, getattr(test_case, "_testMethodName"))

                # Resolve the dependencies using the application's resolver
                params = self.__app.resolveDependencyArguments(
                    rf_instance.getClassName(),
                    dependencies
                )

                # Create a wrapper to inject resolved dependencies into the test method
                def create_test_wrapper(original_test, resolved_args: dict):
                    def wrapper(self_instance):
                        return original_test(self_instance, **resolved_args)
                    return wrapper

                # Bind the wrapped method to the test case instance
                wrapped_method = create_test_wrapper(original_method, params)
                bound_method = wrapped_method.__get__(test_case, test_case.__class__)
                setattr(test_case, getattr(test_case, "_testMethodName"), bound_method)
                flattened_suite.addTest(test_case)

            except Exception:

                # If dependency resolution fails, add the original test case
                flattened_suite.addTest(test_case)

        return flattened_suite

    def __runTestsSequentially(
        self,
        output_buffer: io.StringIO,
        error_buffer: io.StringIO
    ) -> unittest.TestResult:
        """
        Executes all test cases in the test suite sequentially, capturing standard output and error streams.

        Parameters
        ----------
        output_buffer : io.StringIO
            Buffer to capture the standard output generated during test execution.
        error_buffer : io.StringIO
            Buffer to capture the standard error generated during test execution.

        Returns
        -------
        unittest.TestResult
            The aggregated result object containing the outcomes of all executed test cases.

        Raises
        ------
        OrionisTestValueError
            If an item in the suite is not a valid unittest.TestCase instance.

        Notes
        -----
        Each test case is executed individually, and results are merged into a single result object.
        Output and error streams are redirected for each test case to ensure complete capture.
        The printer is used to display the result of each test immediately after execution.
        """

        # Initialize output and error buffers to capture test execution output
        result = None

        # Iterate through all resolved test cases in the suite
        for case in self.__resolveFlattenedTestSuite():

            # Ensure the test case is a valid unittest.TestCase instance
            if not isinstance(case, unittest.TestCase):
                raise OrionisTestValueError(
                    f"Invalid test case type: Expected unittest.TestCase, got {type(case).__name__}."
                )

            # Redirect output and error streams for the current test case
            with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
                runner = unittest.TextTestRunner(
                    stream=output_buffer,
                    verbosity=self.__verbosity,
                    failfast=self.__fail_fast,
                    resultclass=self.__customResultClass()
                )
                # Run the current test case and obtain the result
                single_result: IOrionisTestResult = runner.run(unittest.TestSuite([case]))

            # Print the result of the current test case using the printer
            self.__printer.unittestResult(single_result.test_results[0])

            # Merge the result of the current test case into the aggregated result
            if result is None:
                result = single_result
            else:
                self.__mergeTestResults(result, single_result)

        # Return the aggregated result containing all test outcomes
        return result

    def __runTestsInParallel(
        self,
        output_buffer: io.StringIO,
        error_buffer: io.StringIO
    ) -> unittest.TestResult:
        """
        Executes all test cases in the test suite concurrently using a thread pool and aggregates their results.

        Parameters
        ----------
        output_buffer : io.StringIO
            Buffer to capture the standard output generated during test execution.
        error_buffer : io.StringIO
            Buffer to capture the standard error generated during test execution.

        Returns
        -------
        unittest.TestResult
            Combined result object containing the outcomes of all executed test cases.

        Notes
        -----
        Each test case is executed in a separate thread using a ThreadPoolExecutor.
        Results from all threads are merged into a single result object.
        Output and error streams are redirected for the entire parallel execution.
        If fail-fast is enabled, execution stops as soon as a failure is detected.
        """

        # Resolve and flatten all test cases in the suite, injecting dependencies if needed
        test_cases = list(self.__resolveFlattenedTestSuite())

        # Get the custom result class for enhanced test tracking
        result_class = self.__customResultClass()

        # Create a combined result object to aggregate all individual test results
        combined_result = result_class(io.StringIO(), descriptions=True, verbosity=self.__verbosity)

        # Define a function to run a single test case and return its result
        def run_single_test(test):
            runner = unittest.TextTestRunner(
                stream=io.StringIO(),
                verbosity=self.__verbosity,
                failfast=False,
                resultclass=result_class
            )
            return runner.run(unittest.TestSuite([test]))

        # Redirect output and error streams for the entire parallel execution
        with redirect_stdout(output_buffer), redirect_stderr(error_buffer):

            # Create a thread pool with the configured number of workers
            with ThreadPoolExecutor(max_workers=self.__max_workers) as executor:

                # Submit all test cases to the thread pool for execution
                futures = [executor.submit(run_single_test, test) for test in test_cases]

                # As each test completes, merge its result into the combined result
                for future in as_completed(futures):
                    test_result = future.result()
                    self.__mergeTestResults(combined_result, test_result)

                    # If fail-fast is enabled and a failure occurs, cancel remaining tests
                    if self.__fail_fast and not combined_result.wasSuccessful():
                        for f in futures:
                            f.cancel()
                        break

        # Print the result of each individual test using the printer
        for test_result in combined_result.test_results:
            self.__printer.unittestResult(test_result)

        # Return the aggregated result containing all test outcomes
        return combined_result

    def __mergeTestResults(
        self,
        combined_result: unittest.TestResult,
        individual_result: unittest.TestResult
    ) -> None:
        """
        Merge the results of two unittest.TestResult objects into a single result.

        Parameters
        ----------
        combined_result : unittest.TestResult
            The TestResult object that will be updated with the merged results.
        individual_result : unittest.TestResult
            The TestResult object whose results will be merged into the combined_result.

        Returns
        -------
        None
            This method does not return a value. It updates combined_result in place.

        Notes
        -----
        This method aggregates the test statistics and detailed results from individual_result into combined_result.
        It updates the total number of tests run, and extends the lists of failures, errors, skipped tests,
        expected failures, and unexpected successes. If the result objects contain a 'test_results' attribute,
        this method also merges the detailed test result entries.
        """

        # Increment the total number of tests run
        combined_result.testsRun += individual_result.testsRun

        # Extend the list of failures with those from the individual result
        combined_result.failures.extend(individual_result.failures)

        # Extend the list of errors with those from the individual result
        combined_result.errors.extend(individual_result.errors)

        # Extend the list of skipped tests with those from the individual result
        combined_result.skipped.extend(individual_result.skipped)

        # Extend the list of expected failures with those from the individual result
        combined_result.expectedFailures.extend(individual_result.expectedFailures)

        # Extend the list of unexpected successes with those from the individual result
        combined_result.unexpectedSuccesses.extend(individual_result.unexpectedSuccesses)

        # If the individual result contains detailed test results, merge them as well
        if hasattr(individual_result, 'test_results'):
            if not hasattr(combined_result, 'test_results'):
                combined_result.test_results = []
            combined_result.test_results.extend(individual_result.test_results)

    def __customResultClass(
        self
    ) -> type:
        """
        Create and return a custom test result class for enhanced test tracking.

        Returns
        -------
        type
            A dynamically created subclass of unittest.TextTestResult that collects
            detailed information about each test execution, including timing, status,
            error messages, tracebacks, and metadata.

        Notes
        -----
        The returned class, OrionisTestResult, extends unittest.TextTestResult and
        overrides key methods to capture additional data for each test case. This
        includes execution time, error details, and test metadata, which are stored
        in a list of TestResult objects for later reporting and analysis.
        """
        this = self

        class OrionisTestResult(unittest.TextTestResult):

            # Initialize the parent class and custom attributes for tracking results and timings
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.test_results = []              # Stores detailed results for each test
                self._test_timings = {}             # Maps test instances to their execution time
                self._current_test_start = None     # Tracks the start time of the current test

            # Record the start time of the test
            def startTest(self, test):
                self._current_test_start = time.time()
                super().startTest(test)

            # Calculate and store the elapsed time for the test
            def stopTest(self, test):
                elapsed = time.time() - self._current_test_start
                self._test_timings[test] = elapsed
                super().stopTest(test)

            # Handle a successful test case and record its result
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

            # Handle a failed test case, extract error info, and record its result
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
                        exception=err[1]
                    )
                )

            # Handle a test case that raised an error, extract error info, and record its result
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
                        exception=err[1]
                    )
                )

            # Handle a skipped test case and record its result
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

        Parameters
        ----------
        traceback_str : str
            The full traceback string to process.

        Returns
        -------
        tuple
            file_path : str or None
                The path to the Python file where the error occurred, or None if not found.
            clean_tb : str or None
                The cleaned traceback string with framework internals removed, or the original traceback if no cleaning was possible.

        Notes
        -----
        This method parses the traceback string to identify the most relevant file path (typically the last Python file in the traceback).
        It then filters out lines related to framework internals (such as 'unittest/', 'lib/python', or 'site-packages') to produce a more concise and relevant traceback.
        The cleaned traceback starts from the first occurrence of the relevant file path.
        """

        # Find all Python file paths in the traceback
        file_matches = re.findall(r'File ["\'](.*?.py)["\']', traceback_str)

        # Select the last file path as the most relevant one
        file_path = file_matches[-1] if file_matches else None

        # Split the traceback into individual lines for processing
        tb_lines = traceback_str.split('\n')
        clean_lines = []
        relevant_lines_started = False

        # Iterate through each line to filter out framework internals
        for line in tb_lines:

            # Skip lines that are part of unittest, Python standard library, or site-packages
            if any(s in line for s in ['unittest/', 'lib/python', 'site-packages']):
                continue

            # Start collecting lines from the first occurrence of the relevant file path
            if file_path and file_path in line and not relevant_lines_started:
                relevant_lines_started = True
            if relevant_lines_started:
                clean_lines.append(line)

        # Join the filtered lines to form the cleaned traceback
        clean_tb = str('\n').join(clean_lines) if clean_lines else traceback_str
        return file_path, clean_tb

    def __generateSummary(
        self,
        result: unittest.TestResult,
        execution_time: float
    ) -> Dict[str, Any]:
        """
        Generates a summary dictionary of the test suite execution, including statistics,
        timing, and detailed results for each test. Optionally persists the summary and/or
        generates a web report if configured.

        Parameters
        ----------
        result : unittest.TestResult
            The result object containing details of the test execution.
        execution_time : float
            The total execution time of the test suite in seconds.

        Returns
        -------
        dict
            A dictionary containing test statistics, details, and metadata.

        Notes
        -----
        - If persistence is enabled, the summary is saved to storage.
        - If web reporting is enabled, a web report is generated.
        - The summary includes per-test details, overall statistics, and a timestamp.
        """

        # Collect detailed information for each test result
        test_details = []
        for test_result in result.test_results:
            rst: TestResult = test_result

            # Extraer información solo del último frame del traceback si existe
            traceback_frames = []
            if rst.exception and rst.exception.__traceback__:
                tb = traceback.extract_tb(rst.exception.__traceback__)
                for frame in tb:
                    traceback_frames.append({
                        'file': frame.filename,
                        'line': frame.lineno,
                        'function': frame.name,
                        'code': frame.line
                    })

            test_details.append({
                'id': rst.id,
                'class': rst.class_name,
                'method': rst.method,
                'status': rst.status.name,
                'execution_time': float(rst.execution_time),
                'error_message': rst.error_message,
                'traceback': rst.traceback,
                'file_path': rst.file_path,
                'doc_string': rst.doc_string,
                'traceback_frames': traceback_frames
            })

        # Calculate the number of passed tests
        passed = result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)

        # Calculate the success rate as a percentage
        success_rate = (passed / result.testsRun * 100) if result.testsRun > 0 else 100.0

        # Build the summary dictionary with all relevant statistics and details
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

        Parameters
        ----------
        summary : dict
            Summary of test results for web report generation.

        Returns
        -------
        None

        Notes
        -----
        This method creates a web-based report for the given test results summary.
        It uses the TestingResultRender class to generate the report, passing the storage path,
        the summary result, and a flag indicating whether to persist the report based on the
        persistence configuration and driver. After rendering, it prints a link to the generated
        web report using the printer.
        """

        # Create a TestingResultRender instance with the storage path, result summary,
        # and persistence flag (True if persistent and using sqlite driver)
        render = TestingResultRender(
            storage_path=self.__storage,
            result=summary,
            persist=self.__persistent and self.__persistent_driver == 'sqlite'
        )

        # Print the link to the generated web report
        self.__printer.linkWebReport(render.render())

    def __handlePersistResults(
        self,
        summary: Dict[str, Any]
    ) -> None:
        """
        Persist the test results summary using the configured persistence driver.

        Parameters
        ----------
        summary : dict
            The summary dictionary containing test results and metadata to be persisted.

        Raises
        ------
        OSError
            If there is an error creating directories or writing files.
        OrionisTestPersistenceError
            If database operations fail or any other error occurs during persistence.

        Notes
        -----
        This method persists the test results summary according to the configured persistence driver.
        If the driver is set to 'sqlite', the summary is stored in a SQLite database using the TestLogs class.
        If the driver is set to 'json', the summary is saved as a JSON file in the specified storage directory,
        with a filename based on the current timestamp. The method ensures that the target directory exists,
        and handles any errors that may occur during file or database operations.
        """
        try:

            # If the persistence driver is SQLite, store the summary in the database
            if self.__persistent_driver == PersistentDrivers.SQLITE.value:
                history = TestLogs(self.__storage)
                history.create(summary)

            # If the persistence driver is JSON, write the summary to a JSON file
            elif self.__persistent_driver == PersistentDrivers.JSON.value:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                log_path = Path(self.__storage) / f"{timestamp}_test_results.json"

                # Ensure the parent directory exists
                log_path.parent.mkdir(parents=True, exist_ok=True)

                # Write the summary to the JSON file
                with open(log_path, 'w', encoding='utf-8') as log:
                    json.dump(summary, log, indent=4)
        except OSError as e:

            # Raise an error if directory creation or file writing fails
            raise OSError(f"Error creating directories or writing files: {str(e)}")
        except Exception as e:

            # Raise a persistence error for any other exceptions
            raise OrionisTestPersistenceError(f"Error persisting test results: {str(e)}")

    def __filterTestsByName(
        self,
        suite: unittest.TestSuite,
        pattern: str
    ) -> unittest.TestSuite:
        """
        Filter tests in a test suite by a regular expression pattern applied to test names.

        Parameters
        ----------
        suite : unittest.TestSuite
            The test suite containing the tests to be filtered.
        pattern : str
            Regular expression pattern to match against test names (test IDs).

        Returns
        -------
        unittest.TestSuite
            A new TestSuite containing only the tests whose names match the given pattern.

        Raises
        ------
        OrionisTestValueError
            If the provided pattern is not a valid regular expression.

        Notes
        -----
        This method compiles the provided regular expression and applies it to the IDs of all test cases
        in the flattened suite. Only tests whose IDs match the pattern are included in the returned suite.
        If the pattern is invalid, an OrionisTestValueError is raised with details about the regex error.
        """

        # Create a new TestSuite to hold the filtered tests
        filtered_suite = unittest.TestSuite()

        try:

            # Compile the provided regular expression pattern
            regex = re.compile(pattern)

        except re.error as e:

            # Raise a value error if the regex is invalid
            raise OrionisTestValueError(
                f"The provided test name pattern is invalid: '{pattern}'. "
                f"Regular expression compilation error: {str(e)}. "
                "Please check the pattern syntax and try again."
            )

        # Iterate through all test cases in the flattened suite
        for test in self.__flattenTestSuite(suite):

            # Add the test to the filtered suite if its ID matches the regex
            if regex.search(test.id()):
                filtered_suite.addTest(test)

        # Return the suite containing only the filtered tests
        return filtered_suite

    def __listMatchingModules(
        self,
        root_path: Path,
        test_path: Path,
        custom_path: Path,
        pattern_file: str
    ) -> List[str]:
        """
        Discover and import Python modules containing test files that match a given filename pattern within a specified directory.

        This method recursively searches for Python files in the directory specified by `test_path / custom_path` that match the provided
        filename pattern. For each matching file, it constructs the module's fully qualified name relative to the project root, imports
        the module using `importlib.import_module`, and adds it to a set to avoid duplicates. The method returns a list of imported module objects.

        Parameters
        ----------
        root_path : Path
            The root directory of the project, used to calculate the relative module path.
        test_path : Path
            The base directory where tests are located.
        custom_path : Path
            The subdirectory within `test_path` to search for matching test files.
        pattern_file : str
            The filename pattern to match (supports '*' and '?' wildcards).

        Returns
        -------
        List[module]
            A list of imported Python module objects corresponding to test files that match the pattern.

        Notes
        -----
        - Only files ending with `.py` are considered as Python modules.
        - Duplicate modules are avoided by using a set.
        - The module name is constructed by converting the relative path to dot notation.
        - If the relative path is '.', only the module name is used.
        - The method imports modules dynamically and returns them as objects.
        """

        # Compile the filename pattern into a regular expression for matching.
        regex = re.compile('^' + pattern_file.replace('*', '.*').replace('?', '.') + '$')

        # Use a set to avoid duplicate module imports.
        matched_folders = set()

        # Walk through all files in the target directory.
        for root, _, files in walk(str(test_path / custom_path) if custom_path else str(test_path)):
            for file in files:

                # Check if the file matches the pattern and is a Python file.
                if regex.fullmatch(file) and file.endswith('.py'):

                    # Calculate the relative path from the root, convert to module notation.
                    ralative_path = str(Path(root).relative_to(root_path)).replace(os.sep, '.')
                    module_name = file[:-3]  # Remove '.py' extension.

                    # Build the full module name.
                    full_module = f"{ralative_path}.{module_name}" if ralative_path != '.' else module_name

                    # Import the module and add to the set.
                    matched_folders.add(import_module(ValidModuleName(full_module)))

        # Return the list of imported module objects.
        return list(matched_folders)

    def getTestNames(
        self
    ) -> List[str]:
        """
        Get a list of test names (unique identifiers) from the test suite.

        Returns
        -------
        list of str
            List of test names from the test suite.
        """
        return [test.id() for test in self.__flattenTestSuite(self.__suite)]

    def getTestCount(
        self
    ) -> int:
        """
        Get the total number of test cases in the test suite.

        Returns
        -------
        int
            Total number of individual test cases in the suite.
        """
        return len(list(self.__flattenTestSuite(self.__suite)))

    def clearTests(
        self
    ) -> None:
        """
        Clear all tests from the current test suite.

        Returns
        -------
        None
        """
        self.__suite = unittest.TestSuite()

    def getResult(
        self
    ) -> dict:
        """
        Get the results of the executed test suite.

        Returns
        -------
        dict
            Result of the executed test suite.
        """
        return self.__result

    def getOutputBuffer(
        self
    ) -> int:
        """
        Get the output buffer used for capturing test results.

        Returns
        -------
        int
            Output buffer containing the results of the test execution.
        """
        return self.__output_buffer

    def printOutputBuffer(
        self
    ) -> None:
        """
        Print the contents of the output buffer to the console.

        Returns
        -------
        None
        """
        self.__printer.print(self.__output_buffer)

    def getErrorBuffer(
        self
    ) -> int:
        """
        Get the error buffer used for capturing test errors.

        Returns
        -------
        int
            Error buffer containing errors encountered during test execution.
        """
        return self.__error_buffer

    def printErrorBuffer(
        self
    ) -> None:
        """
        Print the contents of the error buffer to the console.

        Returns
        -------
        None
        """
        self.__printer.print(self.__error_buffer)