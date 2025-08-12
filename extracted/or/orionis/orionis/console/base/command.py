from typing import Any, Dict, List
from orionis.console.args.argument import CLIArgument
from orionis.console.dynamic.progress_bar import ProgressBar
from orionis.console.output.console import Console
from orionis.console.base.contracts.command import IBaseCommand

class BaseCommand(Console, ProgressBar, IBaseCommand):
    """
    Abstract base class for implementing console commands in the Orionis framework.

    This class provides a foundation for creating command-line interface commands with
    built-in console output capabilities, progress bar functionality, and argument handling.
    It inherits from Console and ProgressBar to provide rich terminal interaction features
    while implementing the IBaseCommand interface contract.

    The BaseCommand class serves as a template that enforces a consistent structure for
    all command implementations in the framework, requiring subclasses to implement the
    core command logic while providing common utilities for argument access and console
    operations.

    This is an abstract base class and should not be instantiated directly.
    All concrete command implementations must inherit from this class and
    provide their own handle() method implementation.

    The class integrates with the framework's console and progress bar systems,
    allowing commands to provide rich user feedback during execution.

    Attributes
    ----------
    timestamps : bool, default True
        Controls whether timestamps are included in console output messages.
        When True, all console output will be prefixed with timestamp information.
    signature : str
        Defines the command signature string used for command registration and
        automatic help text generation. This should follow the framework's
        signature format conventions.
    description : str
        Human-readable description of the command's purpose and functionality.
        Used in help documentation and command listing interfaces.
    _args : Dict[str, Any], default {}
        Dictionary containing parsed command-line arguments and options.
        Populated automatically by the command parser before handle() execution.
    arguments : List[CLIArgument], default []
        List of CLIArgument instances defining the command's accepted arguments
        and options. Used for argument parsing and validation.

    Methods
    -------
    handle()
        Abstract method that must be implemented by subclasses to define the
        main command execution logic.
    argument(key: str)
        Safely retrieves argument values from the parsed arguments dictionary
        with type validation and error handling.
    """

    # Enable timestamps in console output by default
    timestamps: bool = True

    # Command signature string for registration and help text generation
    signature: str

    # Human-readable description for documentation and help display
    description: str

    # Dictionary to store parsed command-line arguments and options
    _args: Dict[str, Any] = {}

    # List of CLIArgument instances defining command arguments
    arguments: List[CLIArgument] = []

    def handle(self):
        """
        Execute the main command logic.

        This abstract method defines the entry point for command execution and must be
        implemented by all concrete command subclasses. It serves as the primary interface
        for running the command's core functionality after argument parsing and validation.

        Returns
        -------
        None
            This method does not return any value. All command output should be handled
            through the inherited console methods or other side effects.

        Raises
        ------
        NotImplementedError
            Always raised when called on the base class, indicating that subclasses
            must provide their own implementation of this method.

        Notes
        -----
        Subclasses should override this method to implement their specific command
        behavior. The method will be called after all command-line arguments have
        been parsed and stored in the _args dictionary.
        """

        # Raise an error to enforce implementation in subclasses
        raise NotImplementedError("The 'handle' method must be implemented in the subclass.")

    def argument(self, key: str, default: Any = None) -> Any:
        """
        Retrieve the value of a specific command-line argument by key with optional default fallback.

        This method provides safe and validated access to command-line arguments stored in the
        internal arguments dictionary. It performs type checking on both the key parameter and
        the internal _args attribute to ensure data integrity before attempting retrieval.

        The method follows a fail-safe approach by returning a default value when the requested
        argument key is not found, preventing KeyError exceptions during command execution.

        Parameters
        ----------
        key : str
            The string identifier used to locate the desired argument in the arguments
            dictionary. Must be a non-empty string that corresponds to a valid argument name.
        default : Any, optional
            The fallback value to return if the specified key is not found in the arguments
            dictionary. Defaults to None if not provided.

        Returns
        -------
        Any
            The value associated with the specified key if it exists in the arguments
            dictionary. If the key is not found, returns the provided default value
            or None if no default was specified.

        Raises
        ------
        ValueError
            If the provided key parameter is not of string type.
        ValueError
            If the internal _args attribute is not of dictionary type, indicating
            a corrupted or improperly initialized command state.
        """

        # Validate that the key parameter is a string type
        if not isinstance(key, str):
            raise ValueError(f"Argument key must be a string, got '{type(key).__name__}' instead.")

        # Ensure the internal args attribute is a valid dictionary
        if not isinstance(self._args, dict):
            raise ValueError(f"Arguments must be a dictionary, got '{type(self._args).__name__}' instead.")

        # Safely retrieve the argument value with optional default fallback
        return self._args.get(key, default)