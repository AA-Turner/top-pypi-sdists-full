import argparse
from dataclasses import dataclass, field
from typing import Any, Optional, List, Type, Union, Dict
from orionis.console.args.enums.actions import ArgumentAction
from orionis.console.exceptions.cli_orionis_value_error import CLIOrionisValueError

@dataclass(kw_only=True, frozen=True, slots=True)
class CLIArgument:
    """
    Represents a command-line argument for argparse.

    This class encapsulates all the properties and validation logic needed to create
    a command-line argument that can be added to an argparse ArgumentParser. It provides
    automatic validation, type checking, and smart defaults for common argument patterns.

    Attributes
    ----------
    flags : List[str]
        List of flags for the argument (e.g., ['--export', '-e']). Must contain at least one flag.
    type : Type
        Data type of the argument. Can be any Python type or custom type.
    help : str
        Description of the argument. If not provided, will be auto-generated from the primary flag.
    default : Any, optional
        Default value for the argument.
    choices : List[Any], optional
        List of valid values for the argument. All choices must match the specified type.
    required : bool, default False
        Whether the argument is required. Only applies to optional arguments.
    metavar : str, optional
        Metavar for displaying in help messages. Auto-generated from primary flag if not provided.
    dest : str, optional
        Destination name for the argument in the namespace. Auto-generated from primary flag if not provided.
    action : Union[str, ArgumentAction], default ArgumentAction.STORE
        Action to perform with the argument when it's encountered.
    nargs : Union[int, str], optional
        Number of arguments expected (e.g., 1, 2, '+', '*').
    const : Any, optional
        Constant value for store_const or append_const actions.

    Raises
    ------
    CLIOrionisValueError
        If any validation fails during initialization.
    """

    # Required fields
    flags: List[str] = None
    type: Type = None
    help: str = None

    default: Any = field(
        default_factory = None,
        metadata = {
            "description": "Default value for the argument.",
            "default": None
        }
    )

    choices: Optional[List[Any]] = field(
        default_factory = None,
        metadata = {
            "description": "List of valid choices for the argument.",
            "default": None
        }
    )

    required: bool = field(
        default_factory = False,
        metadata = {
            "description": "Indicates if the argument is required.",
            "default": False
        }
    )

    metavar: Optional[str] = field(
        default_factory = None,
        metadata = {
            "description": "Metavar for displaying in help messages.",
            "default": None
        }
    )

    dest: Optional[str] = field(
        default_factory = None,
        metadata = {
            "description": "Destination name for the argument in the namespace.",
            "default": None
        }
    )

    action: Union[str, ArgumentAction] = field(
        default_factory = ArgumentAction.STORE,
        metadata = {
            "description": "Action to perform with the argument.",
            "default": ArgumentAction.STORE.value
        }
    )

    nargs: Optional[Union[int, str]] = field(
        default_factory = None,
        metadata = {
            "description": "Number of arguments expected (e.g., 1, 2, '+', '*').",
            "default": None
        }
    )

    const: Any = field(
        default_factory = None,
        metadata = {
            "description": "Constant value for store_const or append_const actions.",
            "default": None
        }
    )

    def __post_init__(self):
        """
        Validate and normalize all argument attributes after initialization.

        This method performs comprehensive validation of all argument attributes
        and applies smart defaults where appropriate. It ensures the argument
        configuration is valid for use with argparse.

        Raises
        ------
        CLIOrionisValueError
            If any validation fails or invalid values are provided.
        """

        # Validate flags - must be provided and non-empty
        if not self.flags:
            raise CLIOrionisValueError(
                "Flags list cannot be empty. Please provide at least one flag (e.g., ['--export', '-e'])"
            )

        # Convert single string flag to list for consistency
        if isinstance(self.flags, str):
            object.__setattr__(self, 'flags', [self.flags])

        # Ensure flags is a list
        if not isinstance(self.flags, list):
            raise CLIOrionisValueError("Flags must be a string or a list of strings")

        # Validate each flag format and ensure they're strings
        for flag in self.flags:
            if not isinstance(flag, str):
                raise CLIOrionisValueError("All flags must be strings")

        # Check for duplicate flags
        if len(set(self.flags)) != len(self.flags):
            raise CLIOrionisValueError("Duplicate flags are not allowed in the flags list")

        # Determine primary flag (longest one, or first if only one)
        primary_flag = max(self.flags, key=len) if len(self.flags) > 1 else self.flags[0]

        # Validate type is actually a type
        if not isinstance(self.type, type):
            raise CLIOrionisValueError("Type must be a valid Python type or custom type class")

        # Auto-generate help if not provided
        if self.help is None:
            object.__setattr__(self, 'help', f"Argument for {primary_flag}")

        # Ensure help is a string
        if not isinstance(self.help, str):
            raise CLIOrionisValueError("Help text must be a string")

        # Validate choices if provided
        if self.choices is not None:
            # Ensure choices is a list
            if not isinstance(self.choices, list):
                raise CLIOrionisValueError("Choices must be provided as a list")

            # Ensure all choices match the specified type
            if self.type and not all(isinstance(choice, self.type) for choice in self.choices):
                raise CLIOrionisValueError(
                    f"All choices must be of type {self.type.__name__}"
                )

        # Validate required is boolean
        if not isinstance(self.required, bool):
            raise CLIOrionisValueError("Required field must be a boolean value (True or False)")

        # Auto-generate metavar if not provided
        if self.metavar is None:
            metavar = primary_flag.lstrip('-').upper().replace('-', '_')
            object.__setattr__(self, 'metavar', metavar)

        # Ensure metavar is a string
        if not isinstance(self.metavar, str):
            raise CLIOrionisValueError("Metavar must be a string")

        # Auto-generate dest if not provided
        if self.dest is None:
            dest = primary_flag.lstrip('-').replace('-', '_')
            object.__setattr__(self, 'dest', dest)

        # Ensure dest is a string
        if not isinstance(self.dest, str):
            raise CLIOrionisValueError("Destination (dest) must be a string")

        # Ensure dest is a valid Python identifier
        if not self.dest.isidentifier():
            raise CLIOrionisValueError(f"Destination '{self.dest}' is not a valid Python identifier")

        # Normalize action value
        if self.action is None:
            object.__setattr__(self, 'action', ArgumentAction.STORE.value)
        elif isinstance(self.action, str):
            try:
                action_enum = ArgumentAction(self.action)
                object.__setattr__(self, 'action', action_enum.value)
            except ValueError:
                raise CLIOrionisValueError(f"Invalid action '{self.action}'. Please use a valid ArgumentAction value")
        elif isinstance(self.action, ArgumentAction):
            object.__setattr__(self, 'action', self.action.value)
        else:
            raise CLIOrionisValueError("Action must be a string or an ArgumentAction enum value")

        # Special handling for boolean types
        if self.type is bool:

            # Auto-configure action based on default value
            action = ArgumentAction.STORE_TRUE.value if not self.default else ArgumentAction.STORE_FALSE.value
            object.__setattr__(self, 'action', action)

            # argparse ignores type with store_true/false actions
            object.__setattr__(self, 'type', None)

        # Special handling for list types
        if self.type is list and self.nargs is None:

            # Auto-configure for accepting multiple values
            object.__setattr__(self, 'nargs', '+')
            object.__setattr__(self, 'type', str)

    def addToParser(self, parser: argparse.ArgumentParser) -> None:
        """
        Add this argument to an argparse ArgumentParser instance.

        This method integrates the CLIArgument configuration with an argparse
        ArgumentParser by building the appropriate keyword arguments and adding
        the argument with all its flags and options. The method handles all
        necessary conversions and validations to ensure compatibility with
        argparse's expected format.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            The ArgumentParser instance to which this argument will be added.
            The parser must be a valid argparse.ArgumentParser object.

        Returns
        -------
        None
            This method does not return any value. It modifies the provided
            parser by adding the argument configuration to it.

        Raises
        ------
        CLIOrionisValueError
            If there's an error adding the argument to the parser, such as
            conflicting argument names, invalid configurations, or argparse
            internal errors during argument registration.
        """

        # Build the keyword arguments dictionary for argparse compatibility
        # This filters out None values and handles special argument types
        kwargs = self._buildParserKwargs()

        # Attempt to add the argument to the parser with all flags and options
        try:
            # Use unpacking to pass all flags as positional arguments
            # and all configuration options as keyword arguments
            parser.add_argument(*self.flags, **kwargs)

        # Catch any exception that occurs during argument addition
        # and wrap it in our custom exception for consistent error handling
        except Exception as e:
            raise CLIOrionisValueError(f"Error adding argument {self.flags}: {e}")

    def _buildParserKwargs(self) -> Dict[str, Any]:
        """
        Build the keyword arguments dictionary for argparse compatibility.

        This private method constructs a dictionary of keyword arguments that will be
        passed to argparse's add_argument method. It handles the conversion from
        CLIArgument attributes to argparse-compatible parameters, filtering out None
        values and applying special handling for different argument types (optional
        vs positional arguments).

        The method ensures that the resulting kwargs dictionary contains only valid
        argparse parameters with appropriate values, preventing errors during argument
        registration with the ArgumentParser.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing keyword arguments ready to be unpacked and passed
            to argparse.ArgumentParser.add_argument(). The dictionary includes only
            non-None values and excludes parameters that are invalid for the specific
            argument type (e.g., 'required' parameter for positional arguments).

        Notes
        -----
        This method distinguishes between optional arguments (those starting with '-')
        and positional arguments, applying different validation rules for each type.
        Positional arguments cannot use the 'required' parameter, so it's automatically
        removed from the kwargs if present.
        """

        # Determine argument type by checking if any flag starts with a dash
        # Optional arguments have flags like '--export' or '-e'
        # Positional arguments have flags without dashes like 'filename'
        is_optional = any(flag.startswith('-') for flag in self.flags)
        is_positional = not is_optional

        # Build the base kwargs dictionary with all possible argparse parameters
        # Each key corresponds to a parameter accepted by argparse.add_argument()
        kwargs = {
            "help": self.help,                          # Help text displayed in usage messages
            "default": self.default,                    # Default value when argument not provided
            "required": self.required and is_optional,  # Whether argument is mandatory
            "metavar": self.metavar,                    # Name displayed in help messages
            "dest": self.dest,                          # Attribute name in the parsed namespace
            "choices": self.choices,                    # List of valid values for the argument
            "action": self.action,                      # Action to take when argument is encountered
            "nargs": self.nargs,                        # Number of command-line arguments expected
            "type": self.type,                          # Type to convert the argument to
            "const": self.const                         # Constant value for certain actions
        }

        # Filter out None values to prevent passing invalid parameters to argparse
        # argparse will raise errors if None values are explicitly passed for certain parameters
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        # Remove 'required' parameter for positional arguments since it's not supported
        # Positional arguments are inherently required by argparse's design
        if is_positional and 'required' in kwargs:
            del kwargs['required']

        # Return the cleaned and validated kwargs dictionary
        return kwargs