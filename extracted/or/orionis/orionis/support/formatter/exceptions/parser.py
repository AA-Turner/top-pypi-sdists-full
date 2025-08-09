import traceback
from typing import Any, Dict, List, Optional, Union
from orionis.support.formatter.exceptions.contracts.parser import IExceptionParser

class ExceptionParser(IExceptionParser):
    """
    Parses an exception and converts it into a structured dictionary representation.

    Parameters
    ----------
    exception : Exception
        The exception instance to be parsed.
    """

    def __init__(self, exception: Exception) -> None:
        self.__exception = exception

    @property
    def raw_exception(self) -> Exception:
        """
        Returns the original exception object.

        Returns
        -------
        Exception
            The raw exception instance.
        """
        return self.__exception

    def toDict(self) -> Dict[str, Any]:
        """
        Serializes the exception into a dictionary containing detailed error information.

        Returns
        -------
        dict
            Dictionary with the following keys:
            - 'error_type': str, the type of the exception.
            - 'error_message': str, the formatted traceback string.
            - 'error_code': Any, custom error code if present on the exception.
            - 'stack_trace': list of dict, each dict contains frame details:
                - 'filename': str, file where the error occurred.
                - 'lineno': int, line number in the file.
                - 'name': str, function or method name.
                - 'line': str or None, source line of code.
            - 'cause': dict or None, nested dictionary for the original cause if present.
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
        Parses the stack trace summary into a list of frame dictionaries.

        Parameters
        ----------
        stack : traceback.StackSummary
            The summary of the stack trace.

        Returns
        -------
        list of dict
            Each dictionary contains:
            - 'filename': str, file where the frame is located.
            - 'lineno': int, line number in the file.
            - 'name': str, function or method name.
            - 'line': str or None, source line of code.
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
        Recursively parses the cause of an exception, if present.

        Parameters
        ----------
        cause : BaseException or None
            The original cause of the exception.

        Returns
        -------
        dict or None
            Dictionary with the cause's error type, message, and stack trace,
            or None if no cause exists.
        """
        if not isinstance(cause, BaseException):
            return None

        cause_tb = traceback.TracebackException.from_exception(cause)
        return {
            "error_type": cause_tb.exc_type.__name__ if cause_tb.exc_type else "Unknown",
            "error_message": str(cause_tb).strip(),
            "stack_trace": self.__parse_stack(cause_tb.stack)
        }