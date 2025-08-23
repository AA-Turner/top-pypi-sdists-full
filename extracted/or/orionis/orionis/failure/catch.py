from typing import Any
from orionis.console.kernel import KernelCLI
from orionis.console.output.contracts.console import IConsole
from orionis.failure.contracts.catch import ICatch
from orionis.failure.contracts.handler import IBaseExceptionHandler
from orionis.foundation.contracts.application import IApplication
from orionis.services.log.contracts.log_service import ILogger

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

        # Retrieve the console output service from the application container
        self.__console: IConsole = app.make('x-orionis.console.output.console')

        # Retrieve the logger service from the application container
        self.__logger: ILogger = app.make('x-orionis.services.log.log_service')

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

        # Check if the exception should be ignored by the handler
        if self.__exception_handler.shouldIgnoreException(e):
            return

        # Report the exception using the application's exception handler and logger
        self.__exception_handler.report(
            exception=e,
            log=self.__logger
        )

        # If a kernel is provided, render the exception details to the CLI
        if isinstance(kernel, KernelCLI):
            return self.__exception_handler.renderCLI(
                request=request,
                exception=e,
                log=self.__logger,
                console=self.__console
            )