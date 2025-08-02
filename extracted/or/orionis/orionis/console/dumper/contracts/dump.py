from abc import ABC, abstractmethod
from typing import Any

class IDebug(ABC):
    """
    Debugging utility class for enhanced output and inspection of Python objects.

    This class provides methods for dumping and inspecting data in various formats,
    including plain text, JSON, and tabular representations. It also supports
    rendering nested structures with recursion handling and customizable indentation.
    """

    @abstractmethod
    def dd(self, *args: Any) -> None:
        """
        Dumps the provided arguments to the output and exits the program.

        Parameters
        ----------
        *args : Any
            Variable length argument list to be processed and output.
        """
        pass

    @abstractmethod
    def dump(self, *args: Any) -> None:
        """
        Dumps the provided arguments for debugging or logging purposes.

        Parameters
        ----------
        *args : Any
            Variable length argument list to be processed and output.
        """
        pass