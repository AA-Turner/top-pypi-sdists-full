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

    Attributes
    ----------
    timestamps : bool, default=True
        Controls whether timestamps are displayed in console output. When enabled,
        all console messages will include timestamp prefixes for better debugging
        and logging capabilities.
    signature : str
        The command signature string that defines the command name and expected
        arguments format. Used for command registration in the console system
        and automatic help text generation. Must follow the framework's signature
        format conventions.
    description : str
        Human-readable description explaining the command's purpose and functionality.
        This text is displayed in help documentation, command listings, and usage
        instructions to assist users in understanding the command's capabilities.
    _args : Dict[str, Any]
        Dictionary containing parsed command-line arguments and options passed to
        the command during execution. Populated automatically by the command parser
        before the handle() method is called, providing structured access to all
        user-provided input parameters.
    arguments : List[CLIArgument]
        List of CLIArgument instances defining the command's accepted arguments
        and options. Used for argument parsing, validation, and help text generation.

    Methods
    -------
    handle() -> None
        Abstract method that must be implemented by all concrete command subclasses.
        Contains the main execution logic specific to each command type and handles
        argument processing, business logic execution, and output generation.

    Notes
    -----
    - All concrete implementations must override the handle() method
    - Command signatures should follow framework naming conventions
    - Use self._args dictionary to access parsed command-line arguments
    - Implement proper error handling and validation within command logic
    - Follow single responsibility principle for maintainable command structure
    - Utilize framework's console output methods for consistent user experience

    See Also
    --------
    abc.ABC : Abstract base class functionality
    typing.Dict : Type hints for argument dictionary structure
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

    @abstractmethod
    def handle(self) -> None:
        """
        Execute the main logic of the console command.

        This abstract method serves as the primary entry point for command execution
        and must be implemented by all concrete command subclasses. The method contains
        the core business logic specific to each command type and is responsible for
        processing the parsed arguments stored in self.args and producing the desired
        output or side effects.

        The implementation should access parsed command-line arguments through the
        self.args dictionary and utilize appropriate console output methods for
        user feedback and result presentation. Error handling and resource cleanup
        should also be managed within this method to ensure robust command execution.

        Returns
        -------
        None
            This method does not return any value. All command output, results,
            error messages, and user feedback should be handled through console
            output methods, file operations, database transactions, or other
            side effects rather than return values.

        Raises
        ------
        NotImplementedError
            Automatically raised when this method is called on the abstract base
            class without a concrete implementation. All subclasses must override
            this method with their specific command logic to avoid this exception.

        Notes
        -----
        - Access command arguments and options via the self.args dictionary
        - Use framework's console output methods for consistent user interaction
        - Implement comprehensive error handling and input validation
        - Ensure proper cleanup of resources (files, connections, etc.) if needed
        - Follow the single responsibility principle for maintainable command logic
        - Handle both success and failure scenarios appropriately
        """

        # Abstract method placeholder - concrete implementations must override this method
        # Each subclass should replace this pass statement with specific command logic
        pass