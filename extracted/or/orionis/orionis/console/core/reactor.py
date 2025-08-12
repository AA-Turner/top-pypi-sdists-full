import argparse
import os
from pathlib import Path
import time
from typing import List, Optional
from orionis.app import Orionis
from orionis.console.args.argument import CLIArgument
from orionis.console.base.command import BaseCommand
from orionis.console.base.contracts.command import IBaseCommand
from orionis.console.output.contracts.executor import IExecutor
from orionis.console.output.executor import Executor
from orionis.foundation.contracts.application import IApplication
from orionis.services.introspection.modules.reflection import ReflectionModule
import re

class Reactor:

    def __init__(
        self,
        app: Optional[IApplication] = None
    ):
        """
        Initializes a new Reactor instance for command discovery and management.

        The Reactor constructor sets up the command processing environment by establishing
        the application context, determining the project root directory, and automatically
        discovering and loading command classes from the console commands directory.
        It maintains an internal registry of discovered commands for efficient lookup
        and execution.

        Parameters
        ----------
        app : Optional[IApplication], default None
            The application instance to use for command processing. If None is provided,
            a new Orionis application instance will be created automatically. The
            application instance provides access to configuration, paths, and other
            framework services required for command execution.

        Returns
        -------
        None
            This is a constructor method and does not return any value. The instance
            is configured with the provided or default application and populated with
            discovered commands.

        Notes
        -----
        - Command discovery is performed automatically during initialization
        - The current working directory is used as the project root for module resolution
        - Commands are loaded from the path specified by app.path('console_commands')
        - The internal command registry is initialized as an empty dictionary before loading
        """

        # Initialize the application instance, using provided app or creating new Orionis instance
        self.__app = app or Orionis()

        # Set the project root directory to current working directory for module path resolution
        self.__root: str = str(Path.cwd())

        # Initialize the internal command registry as an empty dictionary
        self.__commands: dict = {}

        # Automatically discover and load command classes from the console commands directory
        self.__loadCommands(str(self.__app.path('console_commands')), self.__root)

        # Initialize the executor for command output management
        self.__executer: IExecutor = self.__app.make('x-orionis.console.output.executor')

    def __loadCommands(self, commands_path: str, root_path: str) -> None:
        """
        Loads command classes from Python files in the specified commands directory.

        This method recursively walks through the commands directory, imports Python modules,
        and registers command classes that inherit from BaseCommand. It performs module path
        sanitization to handle virtual environment paths and validates command structure
        before registration.

        Parameters
        ----------
        commands_path : str
            The absolute path to the directory containing command modules to load.
        root_path : str
            The root path of the project, used for module path normalization.

        Returns
        -------
        None
            This method does not return any value. Command classes are registered
            internally in the reactor's command registry.

        Notes
        -----
        - Only Python files (.py extension) are processed
        - Virtual environment paths are automatically filtered out during module resolution
        - Command classes must inherit from BaseCommand to be registered
        - Each discovered command class undergoes structure validation via __ensureStructure
        """

        # Iterate through the command path and load command modules
        for current_directory, _, files in os.walk(commands_path):
            for file in files:

                # Only process Python files
                if file.endswith('.py'):

                    # Sanitize the module path by converting filesystem path to Python module notation
                    pre_module = current_directory.replace(root_path, '')\
                                                  .replace(os.sep, '.')\
                                                  .lstrip('.')

                    # Remove virtual environment paths using regex (Windows, Linux, macOS)
                    # Windows: venv\Lib\site-packages or venv\lib\site-packages
                    # Linux/macOS: venv/lib/python*/site-packages
                    pre_module = re.sub(r'[^.]*\.(?:Lib|lib)\.(?:python[^.]*\.)?site-packages\.?', '', pre_module)

                    # Remove any remaining .venv or venv patterns from the module path
                    pre_module = re.sub(r'\.?v?env\.?', '', pre_module)

                    # Clean up any double dots or leading/trailing dots that may have been created
                    pre_module = re.sub(r'\.+', '.', pre_module).strip('.')

                    # Skip if module name is empty after cleaning (invalid module path)
                    if not pre_module:
                        continue

                    # Create the reflection module path by combining sanitized path with filename
                    rf_module = ReflectionModule(f"{pre_module}.{file[:-3]}")

                    # Iterate through all classes found in the current module
                    for name, obj in rf_module.getClasses().items():

                        # Check if the class is a valid command class (inherits from BaseCommand but is not BaseCommand itself)
                        if issubclass(obj, BaseCommand) and obj is not BaseCommand and obj is not IBaseCommand:

                            # Validate the command class structure and register it
                            timestamp = self.__ensureTimestamps(obj)
                            signature = self.__ensureSignature(obj)
                            description = self.__ensureDescription(obj)
                            args = self.__ensureArguments(obj)

                            # Add the command to the internal registry
                            self.__commands[signature] = {
                                "class": obj,
                                "timestamps": timestamp,
                                "signature": signature,
                                "description": description,
                                "args": args
                            }

    def __ensureTimestamps(self, obj: IBaseCommand) -> bool:
        """
        Validates that a command class has a properly formatted timestamps attribute.

        This method ensures that the command class contains a 'timestamps' attribute
        that is a boolean value, indicating whether timestamps should be included in
        console output messages.

        Parameters
        ----------
        obj : IBaseCommand
            The command class instance to validate.

        Returns
        -------
        Reactor
            Returns self to enable method chaining for additional validation calls.

        Raises
        ------
        ValueError
            If the command class lacks a 'timestamps' attribute or if the attribute is not a boolean.
        """

        # Check if the command class has a timestamps attribute
        if not hasattr(obj, 'timestamps'):
            return False

        # Ensure the timestamps attribute is a boolean type
        if not isinstance(obj.timestamps, bool):
            raise TypeError(f"Command class {obj.__name__} 'timestamps' must be a boolean.")

        # Return timestamps value
        return obj.timestamps

    def __ensureSignature(self, obj: IBaseCommand) -> str:
        """
        Validates that a command class has a properly formatted signature attribute.

        This method ensures that the command class contains a 'signature' attribute
        that follows the required naming conventions for command identification.
        The signature must be a non-empty string containing only alphanumeric
        characters, underscores, and colons, with specific placement rules.

        Parameters
        ----------
        obj : IBaseCommand
            The command class instance to validate.

        Returns
        -------
        Reactor
            Returns self to enable method chaining.

        Raises
        ------
        ValueError
            If the command class lacks a 'signature' attribute, if the signature
            is an empty string, or if the signature doesn't match the required pattern.
        TypeError
            If the 'signature' attribute is not a string.
        """

        # Check if the command class has a signature attribute
        if not hasattr(obj, 'signature'):
            raise ValueError(f"Command class {obj.__name__} must have a 'signature' attribute.")

        # Ensure the signature attribute is a string type
        if not isinstance(obj.signature, str):
            raise TypeError(f"Command class {obj.__name__} 'signature' must be a string.")

        # Validate that the signature is not empty after stripping whitespace
        if obj.signature.strip() == '':
            raise ValueError(f"Command class {obj.__name__} 'signature' cannot be an empty string.")

        # Define the regex pattern for valid signature format
        # Pattern allows: alphanumeric chars, underscores, colons
        # Cannot start/end with underscore or colon, cannot start with number
        pattern = r'^[a-zA-Z][a-zA-Z0-9_:]*[a-zA-Z0-9]$|^[a-zA-Z]$'

        # Validate the signature against the required pattern
        if not re.match(pattern, obj.signature):
            raise ValueError(f"Command class {obj.__name__} 'signature' must contain only alphanumeric characters, underscores (_) and colons (:), cannot start or end with underscore or colon, and cannot start with a number.")

        # Return signature
        return obj.signature.strip()

    def __ensureDescription(self, obj: IBaseCommand) -> str:
        """
        Validates that a command class has a properly formatted description attribute.

        This method ensures that the command class contains a 'description' attribute
        that provides meaningful documentation for the command. The description must
        be a non-empty string that can be used for help documentation and command
        listing purposes.

        Parameters
        ----------
        obj : IBaseCommand
            The command class instance to validate.

        Returns
        -------
        Reactor
            Returns self to enable method chaining for additional validation calls.

        Raises
        ------
        ValueError
            If the command class lacks a 'description' attribute or if the description
            is an empty string after stripping whitespace.
        TypeError
            If the 'description' attribute is not a string type.
        """

        # Check if the command class has a description attribute
        if not hasattr(obj, 'description'):
            raise ValueError(f"Command class {obj.__name__} must have a 'description' attribute.")

        # Ensure the description attribute is a string type
        if not isinstance(obj.description, str):
            raise TypeError(f"Command class {obj.__name__} 'description' must be a string.")

        # Validate that the description is not empty after stripping whitespace
        if obj.description.strip() == '':
            raise ValueError(f"Command class {obj.__name__} 'description' cannot be an empty string.")

        # Return description
        return obj.description.strip()

    def __ensureArguments(self, obj: IBaseCommand) -> Optional[argparse.ArgumentParser]:
        """
        Validates and processes command arguments for a command class.

        This method ensures that the command class has properly formatted arguments
        and creates an ArgumentParser instance configured with those arguments.

        Parameters
        ----------
        obj : IBaseCommand
            The command class instance to validate.

        Returns
        -------
        Optional[argparse.ArgumentParser]
            An ArgumentParser instance configured with the command's arguments,
            or None if the command has no arguments.

        Raises
        ------
        TypeError
            If the 'arguments' attribute is not a list or contains non-CLIArgument instances.
        """

        # Check if the command class has an arguments attribute
        if not hasattr(obj, 'arguments'):
            return None

        # Ensure the arguments attribute is a list type
        if not isinstance(obj.arguments, list):
            raise TypeError(f"Command class {obj.__name__} 'arguments' must be a list.")

        # If arguments is empty, return None
        if len(obj.arguments) == 0:
            return None

        # Validate that all items in the arguments list are CLIArgument instances
        for index, value in enumerate(obj.arguments):
            if not isinstance(value, CLIArgument):
                raise TypeError(f"Command class {obj.__name__} 'arguments' must contain only CLIArgument instances, found '{type(value).__name__}' at index {index}.")

        # Build the arguments dictionary from the CLIArgument instances
        required_args: List[CLIArgument] = obj.arguments

        # Create an ArgumentParser instance to handle the command arguments
        arg_parser = argparse.ArgumentParser(
            description=f"{obj.signature} - {obj.description}",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            add_help=True,
            allow_abbrev=False
        )
        for arg in required_args:
            arg.addToParser(arg_parser)

        # Return the configured ArgumentParser
        return arg_parser

    def call(
        self,
        signature: str,
        args: Optional[List[str]] = None
    ):
        """
        Executes a command by its signature with optional command-line arguments.

        This method retrieves a registered command by its signature, validates any provided
        arguments against the command's argument parser, and executes the command's handle
        method with the parsed arguments and application context.

        Parameters
        ----------
        signature : str
            The unique signature identifier of the command to execute.
        args : Optional[List[str]], default None
            Command-line arguments to pass to the command. If None, no arguments are provided.

        Returns
        -------
        None
            This method does not return any value. The command's handle method is called
            directly for execution.

        Raises
        ------
        ValueError
            If the command with the specified signature is not found in the registry.
        SystemExit
            If argument parsing fails due to invalid arguments provided.
        """

        # Retrieve the command from the registry
        command: dict = self.__commands.get(signature)
        if command is None:
            raise ValueError(f"Command '{signature}' not found.")

        # Start execution timer
        start_time = time.perf_counter()

        # Get command details
        command_class = command.get("class")
        arg_parser: Optional[argparse.ArgumentParser] = command.get("args")
        timestamps: bool = command.get("timestamps")

        # Initialize parsed arguments
        parsed_args = None

        # If the command has arguments and args were provided, validate them
        if arg_parser is not None and isinstance(arg_parser, argparse.ArgumentParser):
            if args is None:
                args = []
            try:
                # Parse the provided arguments using the command's ArgumentParser
                parsed_args = arg_parser.parse_args(args)
            except SystemExit:
                # Re-raise SystemExit to allow argparse to handle help/error messages
                raise

        # Log the command execution start with RUNNING state
        if timestamps:
            self.__executer.running(program=signature)

        try:

            # Create an instance of the command class and execute it
            command_instance: IBaseCommand = command_class()
            command_instance._args = vars(parsed_args) if parsed_args else {}
            output =  command_instance.handle(self.__app.make('x-orionis.services.inspirational.inspire'))

            # Log the command execution completion with DONE state
            if timestamps:
                elapsed_time = round(time.perf_counter() - start_time, 2)
                self.__executer.done(program=signature, time=f"{elapsed_time}s")

            # If the command has a return value or output, return it
            if output is not None:
                return output

        except Exception as e:

            # Log the command execution failure with ERROR state
            if timestamps:
                elapsed_time = round(time.perf_counter() - start_time, 2)
                self.__executer.fail(program=signature, time=f"{elapsed_time}s")
