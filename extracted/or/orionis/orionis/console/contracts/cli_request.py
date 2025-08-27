from abc import ABC, abstractmethod
from typing import Any

class ICLIRequest(ABC):

    @abstractmethod
    def command(self) -> str:
        """
        Retrieve the command name associated with this CLI request.

        This method provides access to the command string that was specified during
        the initialization of the CLIRequest object. The command represents the
        primary action or operation that should be executed based on the CLI input.

        Returns
        -------
        str
            The command name stored as a string. This is the exact command value
            that was passed to the constructor during object initialization.

        Notes
        -----
        The returned command string is immutable and represents the core action
        identifier for this CLI request. This value is essential for determining
        which operation should be performed by the CLI handler.
        """
        pass

    @abstractmethod
    def all(self) -> dict:
        """
        Retrieve all command line arguments as a complete dictionary.

        This method provides access to the entire collection of command line arguments
        that were passed during the initialization of the CLIRequest object. It returns
        a reference to the internal arguments dictionary, allowing for comprehensive
        access to all parsed CLI parameters.

        Returns
        -------
        dict
            A dictionary containing all the parsed command line arguments as key-value
            pairs, where keys are argument names (str) and values are the corresponding
            argument values of any type. If no arguments were provided during
            initialization, returns an empty dictionary.

        Notes
        -----
        This method returns a reference to the internal arguments dictionary rather
        than a copy. Modifications to the returned dictionary will affect the
        internal state of the CLIRequest object.
        """
        pass

    @abstractmethod
    def argument(self, name: str, default: Any = None):
        """
        Retrieve the value of a specific command line argument by its name.

        This method provides access to individual command line arguments that were
        passed during initialization. It safely retrieves argument values without
        raising exceptions if the argument doesn't exist.

        Parameters
        ----------
        name : str
            The name of the command line argument to retrieve. This should match
            the key used when the argument was originally parsed and stored.
        default : Any, optional
            The default value to return if the specified argument name does not
            exist in the arguments dictionary. Defaults to None.

        Returns
        -------
        Any or None
            The value associated with the specified argument name if it exists
            in the arguments dictionary. Returns None if the argument name is
            not found or was not provided during CLI execution.

        Notes
        -----
        This method uses the dictionary's get() method to safely access values,
        ensuring that missing arguments return None rather than raising a KeyError.
        """
        pass