from typing import Any, Callable
from orionis.console.args.argument import CLIArgument
from orionis.console.entities.command import Command as CommandEntity
from orionis.services.introspection.concretes.reflection import ReflectionConcrete

class Command:

    def __init__(
        self,
        signature: str,
        concrete: Callable[..., Any],
        method: str = 'handle'
    ) -> None:
        """
        Initialize a new Command instance.

        This constructor creates a Command object that encapsulates a command signature,
        the concrete class that implements the command logic, and the method to be called
        when executing the command. It validates that the provided concrete is a valid
        class with the specified callable method.

        Parameters
        ----------
        signature : str
            The command signature string that defines how the command should be invoked
            from the command line interface.
        concrete : Callable[..., Any]
            The concrete class that contains the implementation logic for the command.
            Must be a valid class (not an instance) that will be instantiated when
            the command is executed.
        method : str, default='handle'
            The name of the method within the concrete class that will be called
            when executing the command. The method must exist and be callable.

        Returns
        -------
        None
            This is a constructor method and does not return a value.

        Raises
        ------
        TypeError
            If the provided concrete is not a class, or if the method parameter
            is not a string value.
        AttributeError
            If the specified method does not exist in the concrete class or
            is not callable.
        """

        # Validate that the concrete parameter is actually a class
        if not ReflectionConcrete.isConcreteClass(concrete):
            raise TypeError("The provided concrete must be a class.")

        # Validate that the method parameter is a string
        if not isinstance(method, str):
            raise TypeError("The method name must be a string.")

        # Validate that the specified method exists in the concrete class and is callable
        if not hasattr(concrete, method) or not callable(getattr(concrete, method)):
            raise AttributeError(f"The method '{method}' does not exist or is not callable in the provided concrete class.")

        # Store the command signature for later use during command parsing
        self.__signature = signature

        # Store the concrete class reference for instantiation during execution
        self.__concrete = concrete

        # Store the method name to be called on the concrete instance
        self.__method = method

        # Initialize timestamp display as enabled by default
        self.__timestamp = True

        # Set default description for commands that don't provide one
        self.__description = "No description provided."

        # Initialize empty arguments list to be populated later
        self.__arguments = []

    def timestamp(self, enabled: bool = True) -> 'Command':
        """
        Configure whether timestamps should be included in command output.

        This method allows enabling or disabling timestamp display for the command.
        When enabled, timestamps will be shown alongside command execution results.

        Parameters
        ----------
        enabled : bool, default=True
            Flag to enable or disable timestamp display. True enables timestamps,
            False disables them.

        Returns
        -------
        Command
            Returns the current Command instance to allow method chaining.

        Raises
        ------
        TypeError
            If the enabled parameter is not a boolean value.
        """

        # Validate that the enabled parameter is a boolean
        if not isinstance(enabled, bool):
            raise TypeError("The timestamp flag must be a boolean value.")

        # Set the internal timestamp flag
        self.__timestamp = enabled

        # Return self to enable method chaining
        return self

    def description(self, desc: str) -> 'Command':
        """
        Set the description for the command.

        This method allows setting a descriptive text that explains what the command
        does. The description is used for help text and documentation purposes when
        displaying command information to users.

        Parameters
        ----------
        desc : str
            The description text for the command. Must be a non-empty string that
            describes the command's purpose and functionality.

        Returns
        -------
        Command
            Returns the current Command instance to allow method chaining.

        Raises
        ------
        TypeError
            If the desc parameter is not a string value.
        """

        # Validate that the description parameter is a string
        if not isinstance(desc, str):
            raise TypeError("The description must be a string.")

        # Set the internal description attribute
        self.__description = desc

        # Return self to enable method chaining
        return self

    def arguments(self, args: list) -> 'Command':
        """
        Set the list of CLI arguments for the command.

        This method configures the command-line arguments that the command will accept.
        Each argument must be a properly configured CLIArgument instance that defines
        the argument's name, type, validation rules, and other properties. The arguments
        are used during command parsing to validate and process user input.

        Parameters
        ----------
        args : list
            A list of CLIArgument instances that define the command's accepted arguments.
            Each element in the list must be a valid CLIArgument object with proper
            configuration for argument parsing and validation.

        Returns
        -------
        Command
            Returns the current Command instance to allow method chaining and enable
            fluent interface pattern for command configuration.

        Raises
        ------
        TypeError
            If the args parameter is not a list, or if any element in the list
            is not an instance of CLIArgument.
        """

        # Validate that the arguments parameter is a list
        if not isinstance(args, list):
            raise TypeError("Arguments must be provided as a list.")

        # Validate that each argument in the list is a CLIArgument instance
        for arg in args:
            if not isinstance(arg, CLIArgument):
                raise TypeError("All arguments must be instances of CLIArgument.")

        # Set the internal arguments list with the validated arguments
        self.__arguments = args

        # Return self to enable method chaining
        return self

    def get(self) -> tuple[str, CommandEntity]:
        """
        Retrieve the configured Command entity.

        This method constructs and returns a Command entity object that encapsulates
        all the configuration details of the command, including its signature, concrete
        class, method, description, arguments, and timestamp setting. The returned
        Command entity can be used for command execution and management.

        Returns
        -------
        CommandEntity
            A Command entity object containing all the command's configuration details.
        """

        # Create and return a Command entity with all the configured properties
        return self.__signature, CommandEntity(
            obj=self.__concrete,
            method=self.__method,
            timestamps=self.__timestamp,
            signature=self.__signature,
            description=self.__description,
            args=self.__arguments
        )