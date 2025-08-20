from abc import ABC, abstractmethod
from typing import Any, List, Optional

class IReactor(ABC):

    @abstractmethod
    def info(self) -> List[dict]:
        """
        Retrieves a list of all registered commands with their metadata.

        This method returns a list of dictionaries, each containing information about
        a registered command, including its signature, description, and whether it has
        timestamps enabled. This is useful for introspection and displaying available
        commands to the user.

        Returns
        -------
        List[dict]
            A list of dictionaries representing the registered commands, where each dictionary
            contains the command's signature, description, and timestamps status.
        """
        pass

    @abstractmethod
    def call(
        self,
        signature: str,
        args: Optional[List[str]] = None
    ) -> Optional[Any]:
        """
        Executes a registered command synchronously by its signature, optionally passing command-line arguments.

        This method retrieves a command from the internal registry using its unique signature,
        validates and parses any provided arguments using the command's argument parser,
        and then executes the command's `handle` method synchronously. It manages execution timing,
        logging, and error handling, and returns any output produced by the command.

        Parameters
        ----------
        signature : str
            The unique signature identifier of the command to execute.
        args : Optional[List[str]], default None
            List of command-line arguments to pass to the command. If None, no arguments are provided.

        Returns
        -------
        Optional[Any]
            The output produced by the command's `handle` method if execution is successful.
            Returns None if the command does not produce a result or if an error occurs.

        Raises
        ------
        CLIOrionisValueError
            If the command with the specified signature is not found in the registry.
        SystemExit
            If argument parsing fails due to invalid arguments provided (raised by argparse).
        Exception
            Propagates any exception raised during command execution after logging and error output.

        Notes
        -----
        - Logs execution start, completion, and errors with timestamps if enabled.
        - Handles argument parsing and injects parsed arguments into the command instance.
        - All exceptions are logged and displayed in the console.
        """
        pass

    @abstractmethod
    async def callAsync(
        self,
        signature: str,
        args: Optional[List[str]] = None
    ) -> Optional[Any]:
        """
        Executes a registered command asynchronously by its signature, optionally passing command-line arguments.

        This method locates a command in the internal registry using its unique signature,
        validates and parses any provided arguments using the command's argument parser,
        and then executes the command's `handle` method asynchronously. It manages execution timing,
        logging, and error handling, and returns any output produced by the command.

        Parameters
        ----------
        signature : str
            The unique signature identifier of the command to execute.
        args : Optional[List[str]], default None
            List of command-line arguments to pass to the command. If None, no arguments are provided.

        Returns
        -------
        Optional[Any]
            The output produced by the command's `handle` method if execution is successful.
            Returns None if the command does not produce a result or if an error occurs.

        Raises
        ------
        CLIOrionisValueError
            If the command with the specified signature is not found in the registry.
        SystemExit
            If argument parsing fails due to invalid arguments provided (raised by argparse).
        Exception
            Propagates any exception raised during command execution after logging and error output.

        Notes
        -----
        - Logs execution start, completion, and errors with timestamps if enabled.
        - Handles argument parsing and injects parsed arguments into the command instance.
        - All exceptions are logged and displayed in the console.
        """
        pass