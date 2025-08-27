from typing import Any
from orionis.console.kernel import KernelCLI
from orionis.console.tasks.schedule import Schedule
from orionis.failure.contracts.catch import ICatch
from orionis.failure.contracts.handler import IBaseExceptionHandler
from orionis.foundation.contracts.application import IApplication

class Catch(ICatch):

    def __init__(self, app: IApplication) -> None:
        """
        Initializes the Catch handler with application services for console output and logging.

        Parameters
        ----------
        app : IApplication
            The application instance used to resolve required services.

        Attributes
        ----------
        console : IConsole
            Console output service obtained from the application for displaying messages and exceptions.
        logger : ILogger
            Logger service obtained from the application for logging errors and exceptions.

        Returns
        -------
        None
            This constructor does not return any value.

        Notes
        -----
        The constructor retrieves the console and logger services from the application container
        using their respective service keys. These services are used throughout the class for
        error reporting and output.
        """

        # Store the application instance
        self.__app: IApplication = app

        # Retrieve the console output service from the application container
        self.__exception_handler: IBaseExceptionHandler = app.getExceptionHandler()

    def exception(self, kernel: Any, request: Any, e: BaseException) -> None:
        """
        Handles and reports exceptions that occur during CLI execution.

        This method reports the provided exception using the application's exception handler and logger.
        If a kernel instance is provided, it also renders the exception details to the CLI for user visibility.

        Parameters
        ----------
        kernel : Any
            The kernel instance associated with the CLI, or None if not available.
        request : Any
            The request or arguments associated with the CLI command.
        e : BaseException
            The exception instance to be handled.

        Returns
        -------
        None
            This method does not return any value. It performs side effects such as logging and output.

        Notes
        -----
        The exception is always reported using the exception handler and logger.
        If a valid kernel is provided, the exception details are rendered to the CLI.
        """

        # If there is no exception handler, return early
        if self.__app.call(self.__exception_handler, 'shouldIgnoreException', exception=e):
            return

        # Report the exception using the exception handler and logger
        self.__app.call(self.__exception_handler, 'report', exception=e)

        # Check if the kernel is of type `KernelCLI` or `Any`
        if isinstance(kernel, KernelCLI) or isinstance(kernel, Schedule):

            # Render the exception details to the CLI using the exception handler
            self.__app.call(self.__exception_handler, 'renderCLI', exception=e, request=request)