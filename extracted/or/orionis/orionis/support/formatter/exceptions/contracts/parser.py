from abc import ABC, abstractmethod
from typing import Any, Dict

class IExceptionParser(ABC):
    """
    Interface for parsing exceptions into structured dictionary representations.

    This abstract base class defines the contract for classes that convert
    exception objects into a standardized dictionary format, which may include
    details such as error type, message, code, stack trace, and cause.
    """

    @property
    @abstractmethod
    def raw_exception(self) -> Exception:
        """
        Returns the original exception instance.

        Returns
        -------
        Exception
            The exception object to be parsed.
        """
        pass

    @abstractmethod
    def toDict(self) -> Dict[str, Any]:
        """
        Converts the exception into a structured dictionary.

        Returns
        -------
        dict
            A dictionary containing details about the exception, such as:
            - error_type
            - error_message
            - error_code
            - stack_trace
            - cause (if present)
        """
        pass
