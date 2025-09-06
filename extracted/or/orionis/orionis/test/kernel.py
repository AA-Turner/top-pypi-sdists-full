from orionis.foundation.contracts.application import IApplication
from orionis.services.log.contracts.log_service import ILogger
from orionis.test.contracts.kernel import ITestKernel
from orionis.test.contracts.unit_test import IUnitTest
from orionis.test.exceptions import OrionisTestConfigException

class TestKernel(ITestKernel):

    def __init__(
        self,
        app: IApplication
    ) -> None:
        """
        Initialize the TestKernel instance with the provided application.

        This constructor validates the given application instance and sets up
        the test kernel by resolving required dependencies for unit testing.
        It ensures that the application parameter is of the correct type and
        retrieves the unit test service from the application's dependency container.

        Parameters
        ----------
        app : IApplication
            The application instance responsible for dependency injection and
            service resolution.

        Raises
        ------
        OrionisTestConfigException
            If the provided `app` parameter is not an instance of `IApplication`.

        Returns
        -------
        None
            This constructor does not return any value.
        """

        # Ensure the provided app is a valid IApplication instance
        if not isinstance(app, IApplication):
            raise OrionisTestConfigException(
                f"Failed to initialize TestKernel: expected IApplication, got {type(app).__module__}.{type(app).__name__}."
            )

        # Store the application instance for later use
        self.__app: IApplication = app

        # Retrieve the unit test service from the application container
        self.__unit_test: IUnitTest = app.make(IUnitTest)

    def handle(self) -> dict:
        """
        Executes the unit test suite and logs a summary of the results.

        This method serves as the main entry point for running unit tests via the test kernel.
        It invokes the unit test service, collects the results, and logs a detailed summary
        including the number of tests, passed, failed, errors, skipped, total execution time,
        and success rate. If no output is returned, no summary is logged.

        Parameters
        ----------
        None

        Returns
        -------
        dict
            A dictionary containing the test results summary with keys such as
            'total_tests', 'passed', 'failed', 'errors', 'skipped', 'total_time',
            'success_rate', and 'timestamp'. If no tests are run, returns None.
        """

        # Run the unit test suite and collect the output summary
        output = self.__app.call(self.__unit_test, 'run')

        # Only log detailed report if output is available
        if output is not None and isinstance(output, dict):

            # Extract report details from output dictionary
            total_tests = output.get("total_tests", 0)
            passed = output.get("passed", 0)
            failed = output.get("failed", 0)
            errors = output.get("errors", 0)
            skipped = output.get("skipped", 0)
            total_time = output.get("total_time", 0)
            success_rate = output.get("success_rate", 0)
            timestamp = output.get("timestamp", 0)

            # Resolve the logger service from the application container
            self.__logger: ILogger = self.__app.make(ILogger)

            # Log test execution completion with detailed summary
            self.__logger.info(
                f"Test execution completed at {timestamp} | "
                f"Total: {total_tests}, Passed: {passed}, Failed: {failed}, "
                f"Errors: {errors}, Skipped: {skipped}, "
                f"Time: {total_time:.2f}s, Success rate: {success_rate:.2f}%"
            )

        # Return the test results summary dictionary (or None if no output)
        return output
