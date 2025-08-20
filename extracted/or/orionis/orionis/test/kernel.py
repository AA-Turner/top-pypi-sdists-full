from orionis.console.output.contracts.console import IConsole
from orionis.foundation.contracts.application import IApplication
from orionis.services.log.contracts.log_service import ILogger
from orionis.test.contracts.kernel import ITestKernel
from orionis.test.contracts.unit_test import IUnitTest
from orionis.foundation.config.testing.entities.testing import Testing
from orionis.test.exceptions import OrionisTestConfigException, OrionisTestFailureException

class TestKernel(ITestKernel):

    def __init__(
        self,
        app: IApplication
    ) -> None:
        """
        Initialize the TestKernel with the provided application instance.

        This constructor sets up the test kernel by validating the application
        instance and resolving required dependencies for testing operations.

        Parameters
        ----------
        app : IApplication
            The application instance that provides dependency injection
            and service resolution capabilities.

        Raises
        ------
        OrionisTestConfigException
            If the provided app parameter is not an instance of IApplication.

        Returns
        -------
        None
            This is a constructor method and does not return a value.
        """
        # Validate that the provided app parameter is an IApplication instance
        if not isinstance(app, IApplication):
            raise OrionisTestConfigException(
                f"Failed to initialize TestKernel: expected IApplication, got {type(app).__module__}.{type(app).__name__}."
            )

        # Load testing configuration from application config and create Testing instance
        config = Testing(**app.config('testing'))

        # Resolve the unit test service from the application container
        self.__unit_test: IUnitTest = app.make('x-orionis.test.core.unit_test')

        # Apply configuration settings to the UnitTest instance
        self.__unit_test.configure(
            verbosity=config.verbosity,                 # Set output verbosity level
            execution_mode=config.execution_mode,       # Configure test execution mode
            max_workers=config.max_workers,             # Set maximum worker threads for parallel execution
            fail_fast=config.fail_fast,                 # Enable/disable fail-fast behavior
            print_result=config.print_result,           # Control result output printing
            throw_exception=config.throw_exception,     # Configure exception throwing behavior
            persistent=config.persistent,               # Enable/disable persistent test results
            persistent_driver=config.persistent_driver, # Set persistent storage driver
            web_report=config.web_report                # Enable/disable web-based reporting
        )

        # Discover and load test files based on configuration criteria
        self.__unit_test.discoverTests(
            base_path=config.base_path,                 # Root directory for test discovery
            folder_path=config.folder_path,             # Specific folder path within base_path
            pattern=config.pattern,                     # File name pattern for test files
            test_name_pattern=config.test_name_pattern, # Pattern for test method names
            tags=config.tags                            # Tags to filter tests during discovery
        )

        # Resolve the console service from the application container
        self.__console: IConsole = app.make('x-orionis.console.output.console')

        # Initialize the logger service for logging command execution details
        self.__logger: ILogger = app.make('x-orionis.services.log.log_service')

    def handle(self) -> IUnitTest:
        """
        Execute the unit test suite and handle any exceptions that occur during testing.

        This method serves as the main entry point for running tests through the test kernel.
        It executes the unit test suite via the injected unit test service and provides
        comprehensive error handling for both expected test failures and unexpected errors.
        The method ensures graceful termination of the application in case of any failures.

        Returns
        -------
        IUnitTest
            The unit test service instance after successful test execution. This allows
            for potential chaining of operations or access to test results.

        Raises
        ------
        SystemExit
            Indirectly raised through console.exitError() when test failures or
            unexpected errors occur during test execution.
        """

        # Execute the unit test suite through the injected unit test service
        try:

            # Log the start of test execution
            ouput = self.__unit_test.run()

            # Extract report details from output
            total_tests = ouput.get("total_tests")
            passed = ouput.get("passed")
            failed = ouput.get("failed")
            errors = ouput.get("errors")
            skipped = ouput.get("skipped")
            total_time = ouput.get("total_time")
            success_rate = ouput.get("success_rate")
            timestamp = ouput.get("timestamp")

            # Log test execution completion with detailed summary
            self.__logger.info(
                f"Test execution completed at {timestamp} | "
                f"Total: {total_tests}, Passed: {passed}, Failed: {failed}, "
                f"Errors: {errors}, Skipped: {skipped}, "
                f"Time: {total_time:.2f}s, Success rate: {success_rate:.2f}%"
            )

            # Report the test results to the console
            return ouput

        # Handle expected test failures with a descriptive error message
        except OrionisTestFailureException as e:
            self.__logger.error(f"Test execution failed: {e}")
            self.__console.exitError(f"Test execution failed: {e}")

        # Handle any unexpected errors that occur during test execution
        except Exception as e:
            self.__logger.error(f"An unexpected error occurred while executing tests: {e}")
            self.__console.exitError(f"An unexpected error occurred: {e}")
