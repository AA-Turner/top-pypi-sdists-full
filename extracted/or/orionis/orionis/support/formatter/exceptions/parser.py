import traceback
from typing import Any, Dict, List, Optional, Union
from orionis.support.formatter.exceptions.contracts.parser import IExceptionParser

class ExceptionParser(IExceptionParser):
    """
    A utility class to parse an exception and convert it into a structured dictionary.
    """

    def __init__(self, exception: Exception) -> None:
        """
        Initialize the ExceptionParser with the given exception.

        Parameters
        ----------
        exception : Exception
            The exception to be parsed.
        """
        self.__exception = exception

    @property
    def raw_exception(self) -> Exception:
        """
        Get the original exception object.

        Returns
        -------
        Exception
            The raw exception instance.
        """
        return self.__exception

    def toDict(self) -> Dict[str, Any]:
        """
        Serialize the exception into a dictionary format.

        Returns
        -------
        dict
            A dictionary containing:
            - 'error_type': The type of exception.
            - 'error_message': The complete traceback string.
            - 'error_code': Custom error code, if available.
            - 'stack_trace': A list of frames in the stack trace, each with:
                - 'filename': File where the error occurred.
                - 'lineno': Line number.
                - 'name': Function or method name.
                - 'line': The source line of code.
            - 'cause': A nested dictionary representing the original cause (if any).
        """
        tb = traceback.TracebackException.from_exception(self.__exception, capture_locals=False)

        return {
            "error_type": tb.exc_type.__name__ if tb.exc_type else "Unknown",
            "error_message": str(tb).strip(),
            "error_code": getattr(self.__exception, "code", None),
            "stack_trace": self.__parse_stack(tb.stack),
            "cause": self.__parse_cause(self.__exception.__cause__) if self.__exception.__cause__ else None
        }

    def __parse_stack(self, stack: traceback.StackSummary) -> List[Dict[str, Union[str, int, None]]]:
        """
        Helper method to parse the stack trace.

        Parameters
        ----------
        stack : traceback.StackSummary
            The summary of the stack.

        Returns
        -------
        list of dict
            A list of dictionaries with detailed frame information.
        """
        return [
            {
                "filename": frame.filename,
                "lineno": frame.lineno,
                "name": frame.name,
                "line": frame.line
            }
            for frame in stack
        ]

    def __parse_cause(self, cause: Optional[BaseException]) -> Optional[Dict[str, Any]]:
        """
        Recursively parse the cause of an exception, if available.

        Parameters
        ----------
        cause : BaseException or None
            The original cause of the exception.

        Returns
        -------
        dict or None
            A dictionary with the cause information or None if no cause exists.
        """
        if not isinstance(cause, BaseException):
            return None

        cause_tb = traceback.TracebackException.from_exception(cause)
        return {
            "error_type": cause_tb.exc_type.__name__ if cause_tb.exc_type else "Unknown",
            "error_message": str(cause_tb).strip(),
            "stack_trace": self.__parse_stack(cause_tb.stack)
        }