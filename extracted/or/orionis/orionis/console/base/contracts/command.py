
from abc import ABC, abstractmethod
from typing import Any, Dict

class IBaseCommand(ABC):
    """
    Abstract base contract for console commands in Orionis.

    Inherits from ABC and defines the required interface for all console commands:
    - Stores parsed command-line arguments.
    - Requires implementation of main execution logic and argument accessors.

    Attributes
    ----------
    args : Dict[str, Any]
        Dictionary containing the parsed arguments for the command. Should be set by the command parser.
    """

    args: Dict[str, Any] = {}

    @abstractmethod
    def handle(self):
        """
        Main entry point for command execution.

        This method must be overridden in each subclass to define the specific logic of the command.
        Access parsed arguments via self.args and use console/output methods as needed.

        Raises
        ------
        NotImplementedError
            Always raised in the base class. Subclasses must implement this method.
        """
        pass

    @abstractmethod
    def argument(self, key: str) -> Any:
        """
        Retrieves the value of a specific argument by its key.

        Parameters
        ----------
        key : str
            Name of the argument to retrieve.

        Returns
        -------
        Any or None
            Value associated with the key, or None if it does not exist or arguments are not set.

        Raises
        ------
        ValueError
            If the key is not a string or if arguments are not a dictionary.
        """
        pass

    @abstractmethod
    def arguments(self) -> Dict[str, Any]:
        """
        Returns all parsed arguments as a dictionary.

        Returns
        -------
        dict
            Dictionary containing all arguments received by the command. If no arguments, returns an empty dictionary.
        """
        pass