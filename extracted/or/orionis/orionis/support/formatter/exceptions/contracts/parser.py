from abc import ABC, abstractmethod
from typing import Any, Dict

class IExceptionParser(ABC):
    """
    Abstract base interface for classes that parse exceptions
    into a structured dictionary format.
    """

    @property
    @abstractmethod
    def raw_exception(self) -> Exception:
        """
        Get the original exception object.

        Returns
        -------
        Exception
            The raw exception instance.
        """
        pass

    @abstractmethod
    def toDict(self) -> Dict[str, Any]:
        """
        Serialize the exception into a dictionary.

        Returns
        -------
        dict
            A structured representation of the exception including details such as:
            - error_type
            - error_message
            - error_code
            - stack_trace
            - cause (if any)
        """
        pass
