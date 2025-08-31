from abc import ABC, abstractmethod
from typing import Any

class ICatch(ABC):

    @abstractmethod
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
        pass