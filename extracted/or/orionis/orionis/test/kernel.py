from orionis.console.output.contracts.console import IConsole
from orionis.foundation.contracts.application import IApplication
from orionis.test.contracts.kernel import ITestKernel
from orionis.test.contracts.unit_test import IUnitTest
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

        # Resolve the unit test service from the application container
        self.__unit_test: IUnitTest = app.make('core.orionis.testing')

        # Resolve the console service from the application container
        self.__console: IConsole = app.make('core.orionis.console')

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
            return self.__unit_test.run()

        # Handle expected test failures with a descriptive error message
        except OrionisTestFailureException as e:
            self.__console.exitError(f"Test execution failed: {e}")

        # Handle any unexpected errors that occur during test execution
        except Exception as e:
            self.__console.exitError(f"An unexpected error occurred: {e}")
