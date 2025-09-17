from abc import ABC, abstractmethod
from typing import Any, Dict, List
from orionis.console.args.argument import CLIArgument

class IBaseCommand(ABC):
    """
    Abstract base contract for console commands in Orionis framework.

    This abstract base class defines the standardized interface that all console
    commands must implement within the Orionis framework. It provides a consistent
    contract for command execution, argument handling, metadata storage, and console
    output management.

    The class establishes the foundation for command-line interface functionality,
    ensuring all commands follow a uniform pattern for registration, execution,
    and user interaction while maintaining flexibility for specific command logic
    implementation.
    """

    # Enable timestamps in console output by default
    timestamps: bool = True

    # Command signature string for registration and help text generation
    signature: str

    # Human-readable description for documentation and help display
    description: str

    # Dictionary to store parsed command-line arguments and options
    __args: Dict[str, Any] = {}

    @abstractmethod
    async def options(self) -> List[CLIArgument]:
        """
        Defines the command-line arguments and options accepted by the command.

        This asynchronous method should be overridden by subclasses to specify the list of
        command-line arguments and options that the command supports. Each argument or option
        should be represented as a CLIArgument object, which encapsulates details such as the
        argument's name, type, default value, and help description.

        This method enables the framework to automatically parse, validate, and document
        the available arguments for each command, ensuring consistent user experience
        across all commands.

        Parameters
        ----------
        None

        Returns
        -------
        List
            A list of CLIArgument objects, where each object describes a single
            command-line argument or option accepted by the command. If the command
            does not accept any arguments or options, an empty list is returned.

        Notes
        -----
        Subclasses should override this method to declare their specific arguments.
        The returned list is used by the framework for argument parsing and help
        text generation.
        """
        pass

    @abstractmethod
    async def handle(self):
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
        pass

    @abstractmethod
    def setArguments(self, args: Dict[str, Any]) -> None:
        """
        Populate the internal arguments dictionary with parsed command-line arguments and options.

        This method is intended for internal use by the command parsing mechanism to initialize
        the internal arguments state before command execution. It assigns the provided dictionary
        of arguments and options to the internal storage, making them accessible via the
        `argument()` and `arguments()` methods.

        Parameters
        ----------
        args : Dict[str, Any]
            Dictionary containing parsed command-line arguments and options, where each key
            represents an argument name and each value is the corresponding argument value.

        Returns
        -------
        None
            This method does not return any value. It updates the internal state of the command
            instance to reflect the provided arguments.

        Raises
        ------
        ValueError
            If the provided `args` parameter is not a dictionary.

        Notes
        -----
        This method is automatically invoked by the command framework prior to the execution
        of the `handle()` method. It should not be called directly by command implementations.
        """
        pass

    @abstractmethod
    def arguments(self) -> Dict[str, Any]:
        """
        Retrieve the entire dictionary of parsed command-line arguments and options.

        This method provides access to all arguments and options that have been parsed
        and stored internally for the current command execution. It is useful for
        scenarios where bulk access to all argument values is required, such as
        dynamic processing or debugging.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing all parsed command-line arguments and options,
            where each key is the argument name and each value is the corresponding
            argument value.

        Notes
        -----
        The returned dictionary reflects the current state of the command's arguments.
        Modifying the returned dictionary will affect the internal state of the command.
        """
        pass

    @abstractmethod
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
            If the internal __args attribute is not of dictionary type, indicating
            a corrupted or improperly initialized command state.
        """
        pass