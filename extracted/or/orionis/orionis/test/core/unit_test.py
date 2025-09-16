import inspect
import io
import json
import logging
import os
import re
import time
import traceback
import unittest
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from importlib import import_module
from os import walk
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from orionis.foundation.config.testing.entities.testing import Testing
from orionis.foundation.config.testing.enums.drivers import PersistentDrivers
from orionis.foundation.config.testing.enums.mode import ExecutionMode
from orionis.foundation.contracts.application import IApplication
from orionis.services.introspection.concretes.reflection import ReflectionConcrete
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
    ValidBasePath, ValidExecutionMode, ValidFailFast, ValidFolderPath,
    ValidModuleName, ValidNamePattern, ValidPattern, ValidPersistentDriver,
    ValidPersistent, ValidThrowException, ValidVerbosity, ValidWebReport, ValidWorkers,
)
from orionis.test.view.render import TestingResultRender
import asyncio

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

        # Suppress overly verbose asyncio logging during test execution
        logging.getLogger("asyncio").setLevel(logging.ERROR)

        # Store the application instance for dependency injection and configuration access
        self.__app: IApplication = app

        # Initialize the unittest loader for discovering test cases
        self.__loader = unittest.TestLoader()

        # Initialize the test suite to hold discovered tests
        self.__suite = unittest.TestSuite()
        self.__flatten_test_suite: Optional[List[unittest.TestCase]] = None

        # List to store imported test modules
        self.__imported_modules: List = []

        # Sets to track discovered test cases, modules, and IDs
        self.__discovered_test_cases: set = set()
        self.__discovered_test_modules: set = set()
        self.__discovered_test_ids: set = set()

        # Variable to store the result summary after test execution
        self.__result: Optional[Dict[str, Any]] = None

        # Define keywords to detect debugging or dump calls in test code
        self.__debbug_keywords: list = ['self.dd', 'self.dump']

        # Use live console output during test execution
        self.__live_console: bool = True

        # Load and set internal paths for test discovery and result storage
        self.__loadPaths()

        # Load and validate the testing configuration from the application
        self.__loadConfig()

        # Discover and import test modules based on the configuration
        self.__loadModules()

        # Discover and load all test cases from the imported modules into the suite
        self.__loadTests()

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
        self.__test_path: Path = ValidBasePath(self.__app.path('tests'))
        self.__root_path: Path = ValidBasePath(self.__app.path('root'))

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
            verbosity=self.__verbosity
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
            the `self.__imported_modules` list with the discovered and imported module objects.

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

        # Use a set to avoid duplicate module imports
        modules = set()

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
        self.__imported_modules.extend(modules)

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

            # Iterate through each file in the current directory
            for file in files:

                # Check if the file matches the pattern and is a Python file.
                if regex.fullmatch(file) and file.endswith('.py'):

                    # Calculate the relative path from the root, convert to module notation.
                    ralative_path = str(Path(root).relative_to(root_path)).replace(os.sep, '.')

                    # Remove '.py' extension.
                    module_name = file[:-3]

                    # Build the full module name.
                    full_module = f"{ralative_path}.{module_name}" if ralative_path != '.' else module_name

                    # Import the module and add to the set.
                    matched_folders.add(import_module(ValidModuleName(full_module)))

        # Return the list of imported module objects.
        return list(matched_folders)

    def __raiseIsFailedTest(
        self,
        test_case: unittest.TestCase
    ) -> None:
        """
        Raises an error if the provided test case represents a failed import.

        This method checks whether the given test case is an instance of a failed import
        (typically indicated by the class name '_FailedTest'). If so, it extracts the error
        details from the test case and raises an `OrionisTestValueError` with a descriptive
        message, including the test case ID and error information. This helps to surface
        import errors or missing dependencies during test discovery.

        Parameters
        ----------
        test_case : unittest.TestCase
            The test case to check for failed import status.

        Returns
        -------
        None
            This method does not return a value. If the test case is a failed import,
            an exception is raised.

        Raises
        ------
        OrionisTestValueError
            If the test case is a failed import, with details about the failure.

        Notes
        -----
        - The error message is extracted from the `_exception` attribute if present,
          otherwise from the `_outcome.errors` or the string representation of the test case.
        - This method is typically used during test discovery to halt execution and
          provide immediate feedback about import failures.
        """

        # Check if the test case is a failed import by its class name
        if test_case.__class__.__name__ == "_FailedTest":
            error_message = ""

            # Try to extract the error message from known attributes
            if hasattr(test_case, "_exception"):
                error_message = str(test_case._exception)
            elif hasattr(test_case, "_outcome") and hasattr(test_case._outcome, "errors"):
                error_message = str(test_case._outcome.errors)
            else:
                error_message = str(test_case)

            # Raise a value error with detailed information about the failure
            raise OrionisTestValueError(
                f"Failed to import test module: {test_case.id()}.\n"
                f"Error details: {error_message}\n"
                "Please check for import errors or missing dependencies."
            )

    def __raiseIfNotFoundTestMethod(
        self,
        test_case: unittest.TestCase
    ) -> None:
        """
        Raises an error if the provided test case does not have a valid test method.

        This method uses reflection to check whether the given `unittest.TestCase` instance
        contains a valid test method. It retrieves the method name from the test case and
        verifies that the method exists in the test case's class. If the method is missing
        or invalid, an `OrionisTestValueError` is raised with a descriptive message.

        Parameters
        ----------
        test_case : unittest.TestCase
            The test case instance to validate.

        Returns
        -------
        None
            This method does not return any value. If the test case is invalid, an exception is raised.

        Raises
        ------
        OrionisTestValueError
            If the test case does not have a valid test method.

        Notes
        -----
        - Uses `ReflectionInstance` to retrieve the test method name.
        - Checks for both missing method names and missing attributes in the test case class.
        - Provides detailed error information including test case ID, class name, and module name.
        """

        # Use reflection to get the test method name
        rf_instance = ReflectionInstance(test_case)
        method_name = rf_instance.getAttribute("_testMethodName")

        # Check for missing or invalid test method
        if not method_name or not hasattr(test_case.__class__, method_name):
            class_name = test_case.__class__.__name__
            module_name = getattr(test_case, "__module__", "unknown")

            # Raise an error with detailed information
            raise OrionisTestValueError(
                f"Test case '{test_case.id()}' in class '{class_name}' (module '{module_name}') "
                f"does not have a valid test method '{method_name}'. "
                "Please ensure the test case is correctly defined and contains valid test methods."
            )

    def __loadTests(
        self
    ) -> None:
        """
        Discover and load all test cases from the imported test modules into the test suite.

        This method iterates through all imported test modules, loads their test cases,
        flattens nested suites, checks for failed imports, applies optional test name filtering,
        and adds the discovered tests to the main test suite. It also tracks the number of discovered
        tests per module and raises detailed errors for import failures or missing tests.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It updates the internal test suite and
            discovered tests metadata.

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

            # Lists to categorize tests with and without debugger calls
            normal_tests = []
            debug_tests = []

            # Use a progress bar to indicate module loading status
            with self.__printer.progressBar() as progress:

                # Set total steps for the progress bar
                steps = len(self.__imported_modules) + 1

                # Add a task to the progress bar for loading modules
                task = progress.add_task("Loading test modules...", total=steps)

                # Print a newline for better console formatting
                self.__printer.line(1)

                # Iterate through all imported test modules
                for test_module in self.__imported_modules:

                    # Load all tests from the current module using the unittest loader
                    module_suite = self.__loader.loadTestsFromModule(test_module)

                    # Flatten the suite to get individual test cases
                    flat_tests = self.__flattenTestSuite(module_suite)

                    # Iterate through each test case
                    for test in flat_tests:

                        # Raise an error if the test case is a failed import
                        self.__raiseIsFailedTest(test)

                        # Raise an error if the test case does not have a valid test method
                        self.__raiseIfNotFoundTestMethod(test)

                        # Add the test case to the discovered tests list
                        self.__discovered_test_cases.add(test.__class__)

                        # Track the module name of the discovered test case
                        self.__discovered_test_modules.add(test.__module__)

                        # Track the test ID of the discovered test case
                        self.__discovered_test_ids.add(test.id())

                        # Categorize and resolve test dependencies efficiently
                        target_list = debug_tests if self.__withDebugger(test) else normal_tests
                        target_list.append(self.__resolveTestDependencies(test))

                    # If no tests are found, raise an error
                    if not flat_tests:
                        raise OrionisTestValueError(
                            f"No tests found in module '{test_module.__name__}'. "
                            "Please ensure that the module contains valid unittest.TestCase classes with test methods."
                        )

                    # Update the progress bar after processing each module
                    progress.advance(task, advance=1)

                # Add debug tests first
                self.__suite.addTests(debug_tests)

                # Then add normal tests
                self.__suite.addTests(normal_tests)

                # Flatten the entire suite for easier access later
                self.__flatten_test_suite = self.__flattenTestSuite(self.__suite)

                # Finalize the progress bar
                progress.update(task, completed=steps)

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

    def __withDebugger(
        self,
        test_case: unittest.TestCase
    ) -> bool:
        """
        Determine if the given test case contains debugging or dump calls.

        This method inspects the source code of the test method and common setup/teardown methods
        (such as `setUp`, `tearDown`, `onSetup`, `onTeardown`) for the presence of any keywords
        specified in the internal `__debbug_keywords` list (e.g., 'self.dd', 'self.dump').
        Commented lines are ignored during inspection. If any debug keyword is found, the method
        disables live console output and returns True.

        Parameters
        ----------
        test_case : unittest.TestCase
            The test case instance whose source code will be inspected.

        Returns
        -------
        bool
            True if any debug or dump keyword is found in the test case source code;
            False otherwise.

        Notes
        -----
        - Uses `inspect.getsource` to retrieve the source code of relevant methods.
        - Ignores lines that are commented out.
        - If an error occurs during source code retrieval or inspection, returns False.
        - If a debug keyword is found, disables live console output for the test run.
        """
        try:

            # Gather method names to inspect: main test method and common setup/teardown hooks
            rf_instance = ReflectionInstance(test_case)
            method_name = rf_instance.getAttribute("_testMethodName")
            extra_methods = ["setUp", "tearDown", "onSetup", "onTeardown"]
            method_names_to_check = [method_name] if method_name else []
            method_names_to_check += [m for m in extra_methods if rf_instance.hasMethod(m)]

            # Inspect each method's source code for debug keywords
            for mname in method_names_to_check:

                # Skip if method name is None
                if not mname:
                    continue

                try:

                    # Retrieve the source code of the method
                    source = rf_instance.getSourceCode(mname)

                except Exception:

                    # Skip if source cannot be retrieved
                    continue

                # Inspect each line of the source code
                for line in source.splitlines():

                    # Strip leading/trailing whitespace for accurate matching
                    stripped = line.strip()

                    # Ignore commented lines
                    if stripped.startswith('#') or re.match(r'^\s*#', line):
                        continue

                    # Check for any debug keyword in the line
                    if any(keyword in line for keyword in self.__debbug_keywords):

                        # Disable live console output if a debug keyword is found
                        if self.__live_console is True:
                            self.__live_console = False
                        return True

        except Exception:

            # On any error during inspection, return False
            return False

        # No debug keywords found in any inspected method
        return False

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
        total_tests = self.getTestCount()

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
        result = self.__printer.executePanel(
            func=self.__runSuite,
            live_console=self.__live_console
        )

        # Calculate execution time in milliseconds
        performance_counter.stop()

        # Generate a summary of the test results
        summary = self.__generateSummary(result, performance_counter.getSeconds())

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
        Recursively flatten a unittest.TestSuite into a list of unique unittest.TestCase instances.

        This method traverses the given test suite, recursively extracting all individual test cases,
        while preserving their order and ensuring uniqueness by test ID. If a test name pattern is configured,
        only test cases whose IDs match the regular expression are included.

        Parameters
        ----------
        suite : unittest.TestSuite
            The test suite to flatten.

        Returns
        -------
        List[unittest.TestCase]
            List of unique test case instances contained in the suite, optionally filtered by name pattern.

        Raises
        ------
        OrionisTestValueError
            If the configured test name pattern is not a valid regular expression.

        Notes
        -----
        - The returned list preserves the order in which test cases appear in the suite.
        - If a test name pattern is set, only test cases matching the pattern are included.
        - Uniqueness is enforced by test ID.
        """
        # Determine if test name pattern filtering is enabled
        regex = None
        if self.__test_name_pattern:
            try:
                regex = re.compile(self.__test_name_pattern)
            except re.error as e:
                raise OrionisTestValueError(
                    f"The provided test name pattern is invalid: '{self.__test_name_pattern}'. "
                    f"Regular expression compilation error: {str(e)}. "
                    "Please check the pattern syntax and try again."
                )

        # Use an ordered dict to preserve order and uniqueness by test id
        tests = {}

        def _flatten(item):
            if isinstance(item, unittest.TestSuite):
                for sub_item in item:
                    _flatten(sub_item)
            elif isinstance(item, unittest.TestCase):
                test_id = item.id() if hasattr(item, "id") else None
                if test_id and test_id not in tests:
                    if regex:
                        if regex.search(test_id):
                            tests[test_id] = item
                    else:
                        tests[test_id] = item

        _flatten(suite)
        return list(tests.values())

    def __runSuite(
        self
    ) -> unittest.TestResult:
        """
        Executes the test suite according to the configured execution mode, capturing both standard output and error streams.

        This method determines whether to run the test suite sequentially or in parallel based on the configured execution mode.
        It delegates execution to either `__runTestsSequentially` or `__runTestsInParallel`, and returns the aggregated test result.

        Parameters
        ----------
        None

        Returns
        -------
        unittest.TestResult
            The aggregated result object containing the outcomes of all executed test cases, including
            detailed per-test results, aggregated statistics, and error information.

        Notes
        -----
        - If the execution mode is set to parallel, tests are run concurrently using multiple workers.
        - If the execution mode is sequential, tests are run one after another.
        - The returned result object contains all test outcomes, including successes, failures, errors, skips, and custom metadata.
        """

        # Run tests in parallel mode using multiple workers if configured
        if self.__execution_mode == ExecutionMode.PARALLEL.value:
            # Execute tests concurrently and aggregate results
            result = self.__runTestsInParallel()

        # Otherwise, run tests sequentially
        else:
            # Execute tests one by one and aggregate results
            result = self.__runTestsSequentially()

        # Return the aggregated test result object
        return result

    def __resolveTestDependencies(
        self,
        test_case: unittest.TestCase
    ) -> unittest.TestSuite:
        """
        Inject dependencies into a single test case if required, returning a TestSuite containing the resolved test case.

        This method uses reflection to inspect the test method for dependency requirements. If dependencies are resolved,
        it injects them into the test method. Supports both synchronous and asynchronous test methods: async methods are
        wrapped to run in an event loop. If dependencies cannot be resolved, the original test case is returned as-is
        within a TestSuite.

        Parameters
        ----------
        test_case : unittest.TestCase
            The test case instance to resolve dependencies for.

        Returns
        -------
        unittest.TestSuite
            A TestSuite containing the test case with injected dependencies if resolution is successful.
            If dependency injection is not possible or fails, the original test case is returned as-is within the suite.

        Raises
        ------
        OrionisTestValueError
            If the test method has unresolved dependencies.

        Notes
        -----
        - Uses ReflectionInstance to determine method dependencies.
        - If dependencies are resolved, injects them into the test method.
        - Supports async test methods by running them in an event loop.
        - If dependencies are unresolved or an error occurs, the original test case is returned.
        """

        # Create a new TestSuite to hold the resolved test case
        suite = unittest.TestSuite()

        try:

            # Use reflection to inspect the test case for dependency requirements
            rf_instance = ReflectionInstance(test_case)
            method_name = rf_instance.getAttribute("_testMethodName", None)

            # If no method name is found, return the original test case
            if not method_name:
                return test_case

            # Get the method dependencies using the dependency injection system
            dependencies = rf_instance.getMethodDependencies(method_name)

            # If there are unresolved dependencies, return the original test case
            if dependencies.unresolved:
                return test_case

            # If dependencies are resolved, inject them into the test method
            if dependencies.resolved:

                # Get the test case class
                test_cls = rf_instance.getClass()

                # Create a ReflectionConcrete instance for the test case class
                rf_concrete = ReflectionConcrete(test_cls)

                # Get the original test method
                original_method = rf_concrete.getAttribute(method_name)

                # Resolve the actual arguments to inject
                resolved_args = self.__app.resolveDependencyArguments(
                    rf_instance.getClassName(),
                    dependencies
                )

                # If the test method is asynchronous, wrap it to run in an event loop
                if asyncio.iscoroutinefunction(original_method):

                    # Define an async wrapper to inject dependencies
                    async def async_wrapper(self_instance):
                        return await original_method(self_instance, **resolved_args)

                    # Wrap with a sync function for unittest compatibility
                    def sync_wrapper(self_instance):
                        return asyncio.run(async_wrapper(self_instance))

                    # Bind the wrapped method to the test case instance
                    bound_method = sync_wrapper.__get__(test_case, test_cls)

                else:

                    # For synchronous methods, inject dependencies directly
                    def wrapper(self_instance):
                        return original_method(self_instance, **resolved_args)

                    # Bind the wrapped method to the test case instance
                    bound_method = wrapper.__get__(test_case, test_cls)

                # Replace the test method with the dependency-injected version
                rf_instance.setMethod(method_name, bound_method)

            # Add the (possibly resolved) test case to the suite
            suite.addTest(rf_instance.getInstance())

            # Return the suite containing the resolved test case
            return suite

        except Exception:

            # On error, return the original test case
            return test_case

    def __runTestsSequentially(
        self
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
        result: unittest.TestResult = None

        # Iterate through all resolved test cases in the suite
        for case in self.__flatten_test_suite:

            runner = unittest.TextTestRunner(
                stream=io.StringIO(),
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
        self
    ) -> unittest.TestResult:
        """
        Executes all test cases in the test suite concurrently using a thread pool and aggregates their results.

        Parameters
        ----------
        None

        Returns
        -------
        unittest.TestResult
            A combined `unittest.TestResult` object containing the outcomes of all executed test cases.
            This includes detailed per-test results, aggregated statistics, error information, and custom metadata.

        Notes
        -----
        - Each test case is executed in a separate thread using `ThreadPoolExecutor`.
        - Results from all threads are merged into a single aggregated result object.
        - Output and error streams are redirected for each test case.
        - If fail-fast is enabled, execution stops as soon as a failure is detected and remaining tests are cancelled.
        - The returned result object contains all test outcomes, including successes, failures, errors, skips, and custom metadata.
        """

        # Initialize the aggregated result object
        result: unittest.TestResult = None

        # Define a function to run a single test case and return its result
        def run_single_test(test):
            runner = unittest.TextTestRunner(
                stream=io.StringIO(),
                verbosity=self.__verbosity,
                failfast=False,
                resultclass=self.__customResultClass()
            )
            return runner.run(unittest.TestSuite([test]))

        # Create a thread pool with the configured number of workers
        with ThreadPoolExecutor(max_workers=self.__max_workers) as executor:

            # Submit all test cases to the thread pool for execution
            futures = [executor.submit(run_single_test, test) for test in self.__flatten_test_suite]

            # As each test completes, merge its result into the combined result
            for future in as_completed(futures):

                # Get the result of the completed test case
                single_result: IOrionisTestResult = future.result()

                # Print the result of the current test case using the printer
                # Ensure print goes to the real stdout even inside redirected context
                self.__printer.unittestResult(single_result.test_results[0])

                # Merge the result of the current test case into the aggregated result
                if result is None:
                    result = single_result
                else:
                    self.__mergeTestResults(result, single_result)

                # If fail-fast is enabled and a failure occurs, cancel remaining tests
                if self.__fail_fast and not result.wasSuccessful():
                    for f in futures:
                        f.cancel()
                    break

        # Return the aggregated result containing all test outcomes
        return result

    def __mergeTestResults(
        self,
        combined_result: unittest.TestResult,
        individual_result: unittest.TestResult
    ) -> None:
        """
        Merge the results of two unittest.TestResult objects into a single aggregated result.

        This method updates the `combined_result` in place by aggregating test statistics and detailed results
        from `individual_result`. It ensures that all test outcomes, including failures, errors, skipped tests,
        expected failures, unexpected successes, and custom test result entries, are merged for comprehensive reporting.

        Parameters
        ----------
        combined_result : unittest.TestResult
            The result object to be updated with merged statistics and details.
        individual_result : unittest.TestResult
            The result object whose statistics and details will be merged into `combined_result`.

        Returns
        -------
        None
            This method does not return any value. The `combined_result` is updated in place with merged data.

        Notes
        -----
        - Increments the total number of tests run.
        - Extends lists of failures, errors, skipped tests, expected failures, and unexpected successes.
        - If present, merges custom `test_results` entries for detailed per-test reporting.
        - This method is used to aggregate results from parallel or sequential test execution.
        """

        # Increment the total number of tests run
        combined_result.testsRun += individual_result.testsRun

        # Merge failures from the individual result
        combined_result.failures.extend(individual_result.failures)

        # Merge errors from the individual result
        combined_result.errors.extend(individual_result.errors)

        # Merge skipped tests from the individual result
        combined_result.skipped.extend(individual_result.skipped)

        # Merge expected failures from the individual result
        combined_result.expectedFailures.extend(individual_result.expectedFailures)

        # Merge unexpected successes from the individual result
        combined_result.unexpectedSuccesses.extend(individual_result.unexpectedSuccesses)

        # Merge custom detailed test results if available
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
        this: "UnitTest" = self

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
        Generate a summary dictionary of the test suite execution.

        This method aggregates statistics, timing, and detailed results for each test case in the suite.
        It optionally persists the summary and/or generates a web report if configured in the test manager.

        Parameters
        ----------
        result : unittest.TestResult
            The result object containing details of the test execution, including per-test outcomes.
        execution_time : float
            The total execution time of the test suite in seconds.

        Returns
        -------
        Dict[str, Any]
            Dictionary containing:
                - total_tests: int
                    Total number of tests executed.
                - passed: int
                    Number of tests that passed.
                - failed: int
                    Number of tests that failed.
                - errors: int
                    Number of tests that raised errors.
                - skipped: int
                    Number of tests that were skipped.
                - total_time: float
                    Total execution time in seconds.
                - success_rate: float
                    Percentage of tests that passed.
                - test_details: List[dict]
                    List of dictionaries with per-test details (ID, class, method, status, timing, error info, traceback, etc.).
                - timestamp: str
                    ISO-formatted timestamp of when the summary was generated.

        Notes
        -----
        - If persistence is enabled, the summary is saved to storage using the configured driver.
        - If web reporting is enabled, a web report is generated and a link is printed.
        - The summary includes per-test details, overall statistics, and a timestamp.
        """

        # Collect detailed information for each test result
        test_details = []
        for test_result in result.test_results:
            rst: TestResult = test_result

            # Extract traceback frames from the exception, if available
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

            # Build the per-test detail dictionary
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

        # Return the summary dictionary containing all test statistics and details
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
            Dictionary containing the summary of test results to be used for web report generation.

        Returns
        -------
        None
            This method does not return any value. It generates a web report and prints a link to it.

        Notes
        -----
        This method creates a web-based report for the given test results summary using the `TestingResultRender` class.
        It passes the storage path, the summary result, and a persistence flag (True if persistence is enabled and the driver is set to 'sqlite').
        After rendering the report, it prints a link to the generated web report using the internal printer.
        The report is persisted only if configured to do so.
        """

        # Create a TestingResultRender instance to generate the web report.
        # The 'persist' flag is True only if persistence is enabled and the driver is 'sqlite'.
        html_report = TestingResultRender(
            result = summary,
            storage_path = self.__storage,
            persist = self.__persistent and self.__persistent_driver == PersistentDrivers.SQLITE.value
        )

        # Print the link to the generated web report using the printer.
        self.__printer.linkWebReport(html_report.render())

    def __handlePersistResults(
        self,
        summary: Dict[str, Any]
    ) -> None:
        """
        Persist the test results summary using the configured persistence driver.

        Parameters
        ----------
        summary : dict
            Dictionary containing the test results and metadata to be persisted.

        Returns
        -------
        None
            This method does not return any value. It performs persistence operations as a side effect.

        Raises
        ------
        OSError
            If there is an error creating directories or writing files.
        OrionisTestPersistenceError
            If database operations fail or any other error occurs during persistence.

        Notes
        -----
        This method saves the test results summary according to the configured persistence driver.
        - If the driver is set to 'sqlite', the summary is stored in a SQLite database using the TestLogs class.
        - If the driver is set to 'json', the summary is saved as a JSON file in the specified storage directory,
          with a filename based on the current timestamp.
        The method ensures that the target directory exists before writing files, and handles any errors that may
        occur during file or database operations.
        """

        try:

            # Persist results using SQLite database if configured
            if self.__persistent_driver == PersistentDrivers.SQLITE.value:
                TestLogs(self.__storage).create(summary)

            # Persist results as a JSON file if configured
            elif self.__persistent_driver == PersistentDrivers.JSON.value:

                # Generate a unique filename based on the current timestamp
                timestamp = str(int(datetime.now().timestamp()))
                log_path = Path(self.__storage) / f"{timestamp}.json"

                # Ensure the parent directory exists before writing the file
                log_path.parent.mkdir(parents=True, exist_ok=True)

                # Write the summary dictionary to the JSON file
                with open(log_path, 'w', encoding='utf-8') as log:
                    json.dump(summary, log, indent=4)

        except OSError as e:

            # Raise an error if directory creation or file writing fails
            raise OSError(
                f"Failed to create directories or write the test results file: {str(e)}. "
                "Please check the storage path permissions and ensure there is enough disk space."
            )

        except Exception as e:

            # Raise a persistence error for any other exceptions
            raise OrionisTestPersistenceError(
                f"An unexpected error occurred while persisting test results: {str(e)}. "
                "Please verify the persistence configuration and check for possible issues with the storage backend."
            )

    def getDiscoveredTestCases(
        self
    ) -> List[unittest.TestCase]:
        """
        Return a list of all discovered test case classes in the test suite.

        This method provides access to all unique test case classes that have been discovered
        during test suite initialization and loading. It does not execute any tests, but simply
        reports the discovered test case classes.

        Returns
        -------
        List[unittest.TestCase]
            A list of unique `unittest.TestCase` classes that have been discovered in the suite.

        Notes
        -----
        - The returned list contains the test case classes, not instances or names.
        - The classes are derived from the `__class__` attribute of each discovered test case.
        - This method is useful for introspection or reporting purposes.
        """

        # Return all unique discovered test case classes as a list
        return list(self.__discovered_test_cases)

    def getDiscoveredModules(
        self
    ) -> List:
        """
        Return a list of all discovered test module names in the test suite.

        This method provides access to all unique test modules that have been discovered
        during test suite initialization and loading. It does not execute any tests, but simply
        reports the discovered module names.

        Parameters
        ----------
        None

        Returns
        -------
        List[str]
            A list of unique module names (as strings) that have been discovered in the suite.

        Notes
        -----
        - The returned list contains the module names, not module objects.
        - The module names are derived from the `__module__` attribute of each discovered test case.
        - This method is useful for introspection or reporting purposes.
        """

        # Return all unique discovered test module names as a list
        return list(self.__discovered_test_modules)

    def getTestIds(
        self
    ) -> List[str]:
        """
        Return a list of all unique test IDs discovered in the test suite.

        This method provides access to the unique identifiers (IDs) of all test cases
        that have been discovered and loaded into the suite. The IDs are collected from
        each `unittest.TestCase` instance during test discovery and are returned as a list
        of strings. This is useful for introspection, reporting, or filtering purposes.

        Parameters
        ----------
        None

        Returns
        -------
        List[str]
            A list of strings, where each string is the unique ID of a discovered test case.
            The IDs are generated by the `id()` method of each `unittest.TestCase` instance.

        Notes
        -----
        - The returned list contains only unique test IDs.
        - This method does not execute any tests; it only reports the discovered IDs.
        - The IDs typically include the module, class, and method name for each test case.
        """

        # Return all unique discovered test IDs as a list
        return list(self.__discovered_test_ids)

    def getTestCount(
        self
    ) -> int:
        """
        Return the total number of individual test cases discovered in the test suite.

        This method calculates and returns the total number of test cases that have been
        discovered and loaded into the suite, including all modules and filtered tests.
        It uses the internal metadata collected during test discovery to provide an accurate count.

        Returns
        -------
        int
            The total number of individual test cases discovered and loaded in the suite.

        Notes
        -----
        - The count reflects all tests after applying any name pattern or folder filtering.
        - This method does not execute any tests; it only reports the discovered count.
        """

        # Return the sum of all discovered test cases across modules
        return len(self.__discovered_test_ids)

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