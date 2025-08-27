from abc import abstractmethod
from typing import Any
from orionis.console.contracts.cli_request import ICLIRequest
from orionis.console.contracts.console import IConsole
from orionis.services.log.contracts.log_service import ILogger

class IBaseExceptionHandler:

    @abstractmethod
    async def destructureException(self, e: BaseException):
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
        pass

    @abstractmethod
    async def shouldIgnoreException(self, e: BaseException) -> bool:
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
        pass

    @abstractmethod
    async def report (self, exception: BaseException, log: ILogger) -> Any:
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
        pass

    @abstractmethod
    async def renderCLI(self, exception: BaseException, request: ICLIRequest, log: ILogger, console: IConsole) -> Any:
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
        pass