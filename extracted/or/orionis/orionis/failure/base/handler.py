from typing import Any, List
from orionis.console.output.contracts.console import IConsole
from orionis.failure.contracts.handler import IBaseExceptionHandler
from orionis.failure.entities.throwable import Throwable
from orionis.services.log.contracts.log_service import ILogger

class BaseExceptionHandler(IBaseExceptionHandler):

    # Exceptions that should not be caught by the handler
    dont_cathc: List[type[BaseException]] = [
        # Add specific exceptions that should not be caught
        # Example: OrionisContainerException
    ]

    def destructureException(self, e: BaseException) -> Throwable:
        """
        Converts an exception into a structured `Throwable` object containing detailed information.

        Parameters
        ----------
        e : BaseException
            The exception instance to be destructured.

        Returns
        -------
        Throwable
            A `Throwable` object encapsulating the exception's class type, message, arguments, and traceback.

        Notes
        -----
        This method extracts the type, message, arguments, and traceback from the provided exception
        and wraps them in a `Throwable` object for consistent error handling and reporting.
        """

        # Create and return a Throwable object with detailed exception information
        return Throwable(
            classtype=type(e),                              # The class/type of the exception
            message=str(e),                                 # The exception message as a string
            args=e.args,                                    # The arguments passed to the exception
            traceback=getattr(e, '__traceback__', None)     # The traceback object, if available
        )

    def shouldIgnoreException(self, e: BaseException) -> bool:
        """
        Determines if the exception should be ignored (not handled) by the handler.

        Parameters
        ----------
        e : BaseException
            The exception instance to check.

        Returns
        -------
        bool
            True if the exception should be ignored, False otherwise.
        """

        # Ensure the provided object is an exception
        if not isinstance(e, BaseException):
            raise TypeError(f"Expected BaseException, got {type(e).__name__}")

        # Convert the exception into a structured Throwable object
        throwable = self.destructureException(e)

        # Check if the exception type is in the list of exceptions to ignore
        return hasattr(self, 'dont_cathc') and throwable.classtype in self.dont_cathc

    def report(self, exception: BaseException, log: ILogger) -> Any:
        """
        Report or log an exception.

        Parameters
        ----------
        exception : BaseException
            The exception instance that was caught.

        Returns
        -------
        None
        """
        # Ensure the provided object is an exception
        if not isinstance(exception, BaseException):
            raise TypeError(f"Expected BaseException, got {type(exception).__name__}")

        # Convert the exception into a structured Throwable object
        throwable = self.destructureException(exception)

        # Log the exception details
        log.error(f"[{throwable.classtype.__name__}] {throwable.message}")

        # Return the structured exception
        return throwable

    def renderCLI(self, args: List[str], exception: BaseException, log: ILogger, console: IConsole) -> Any:
        """
        Render the exception message for CLI output.

        Parameters
        ----------
        exception : BaseException
            The exception instance that was caught.

        Returns
        -------
        None
        """
        # Ensure the provided object is an exception
        if not isinstance(exception, BaseException):
            raise TypeError(f"Expected BaseException, got {type(exception).__name__}")

        # Convert the exception into a structured Throwable object
        throwable = self.destructureException(exception)

        # Log the CLI error message with arguments
        log.error(f"CLI Error: {throwable.message} (Args: {args})")

        # Output the exception traceback to the console
        console.newLine()
        console.exception(exception)
        console.newLine()