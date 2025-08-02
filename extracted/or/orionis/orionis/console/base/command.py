from typing import Any, Dict
from orionis.console.dynamic.progress_bar import ProgressBar
from orionis.console.output.console import Console
from orionis.console.base.contracts.command import IBaseCommand

class BaseCommand(Console, ProgressBar, IBaseCommand):
    """
    Abstract base class for console commands in Orionis.

    Inherits from Console and ProgressBar, allowing commands to:
    - Display messages, errors, and formatted text in the console.
    - Manage progress bars for long-running tasks.
    - Access and manipulate parsed arguments from the command line.

    Attributes
    ----------
    args : dict
        Dictionary containing the parsed arguments for the command. Set via the setArgs method.

    Methods
    -------
    handle()
        Must be implemented by each subclass to define the main logic of the command.
    argument(key)
        Retrieves the value of a specific argument by key.
    arguments()
        Returns all parsed arguments as a dictionary.
    """

    args: Dict[str, Any] = {}

    def handle(self):
        """
        Main entry point for command execution.

        This method must be overridden in each subclass to define the specific logic of the command.
        Access parsed arguments via self.args and use console and progress bar methods as needed.

        Example:
            def handle(self):
                self.write("Processing...")
                value = self.argument("key")
                # custom logic

        Raises
        ------
        NotImplementedError
            Always raised in the base class. Subclasses must implement this method.
        """
        raise NotImplementedError("The 'handle' method must be implemented in the subclass.")

    def argument(self, key: str):
        """
        Retrieves the value of a specific argument by its key.

        Parameters
        ----------
        key : str
            Name of the argument to retrieve.

        Returns
        -------
        any or None
            Value associated with the key, or None if it does not exist or arguments are not set.

        Raises
        ------
        ValueError
            If the key is not a string or if arguments are not a dictionary.

        Example:
            value = self.argument("user")
        """
        if not isinstance(key, str):
            raise ValueError("Argument key must be a string.")
        if not isinstance(self.args, dict):
            raise ValueError("Arguments must be a dictionary.")
        return self.args.get(key)

    def arguments(self) -> dict:
        """
        Returns all parsed arguments as a dictionary.

        Returns
        -------
        dict
            Dictionary containing all arguments received by the command. If no arguments, returns an empty dictionary.

        Example:
            args = self.arguments()
        """
        return dict(self.args) if isinstance(self.args, dict) else {}