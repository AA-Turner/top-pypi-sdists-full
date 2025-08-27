from abc import ABC, abstractmethod
from typing import Any

class IDebug(ABC):
    """
    Abstract base class for debugging utilities that provide enhanced output and inspection of Python objects.

    This class defines the interface for dumping and inspecting data in various formats, 
    supporting features such as recursion handling and customizable indentation.
    """

    @abstractmethod
    def dd(self, *args: Any) -> None:
        """
        Dump the provided arguments to the output and terminate the program.

        Parameters
        ----------
        *args : Any
            Variable length argument list to be dumped and displayed.
        """
        pass

    @abstractmethod
    def dump(self, *args: Any) -> None:
        """
        Dump the provided arguments for debugging or logging purposes.

        Parameters
        ----------
        *args : Any
            Variable length argument list to be dumped and displayed.
        """
        pass
