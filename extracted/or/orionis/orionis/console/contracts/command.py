from abc import ABC, abstractmethod

class ICommand(ABC):

    @abstractmethod
    def timestamp(self, enabled: bool = True) -> 'ICommand':
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
        pass

    @abstractmethod
    def description(self, desc: str) -> 'ICommand':
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
        pass

    @abstractmethod
    def arguments(self, args: list) -> 'ICommand':
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
        pass