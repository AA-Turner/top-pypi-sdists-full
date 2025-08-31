import argparse
from dataclasses import dataclass, field
from typing import Any, Optional, List, Type, Union, Dict
from orionis.console.enums.actions import ArgumentAction
from orionis.console.exceptions import CLIOrionisValueError

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
    flags: List[str]
    type: Type
    help: Optional[str] = None

    default: Any = field(
        default=None,
        metadata={
            "description": "Default value for the argument.",
            "default": None
        }
    )

    choices: Optional[List[Any]] = field(
        default=None,
        metadata={
            "description": "List of valid choices for the argument.",
            "default": None
        }
    )

    required: bool = field(
        default=False,
        metadata={
            "description": "Indicates if the argument is required.",
            "default": False
        }
    )

    metavar: Optional[str] = field(
        default=None,
        metadata={
            "description": "Metavar for displaying in help messages.",
            "default": None
        }
    )

    dest: Optional[str] = field(
        default=None,
        metadata={
            "description": "Destination name for the argument in the namespace.",
            "default": None
        }
    )

    action: Union[str, ArgumentAction] = field(
        default=ArgumentAction.STORE,
        metadata={
            "description": "Action to perform with the argument.",
            "default": ArgumentAction.STORE.value
        }
    )

    nargs: Optional[Union[int, str]] = field(
        default=None,
        metadata={
            "description": "Number of arguments expected (e.g., 1, 2, '+', '*').",
            "default": None
        }
    )

    const: Any = field(
        default=None,
        metadata={
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
            clean_flag = primary_flag.lstrip('-').replace('-', ' ').title()
            object.__setattr__(self, 'help', f"{clean_flag} argument")

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
        if isinstance(self.action, str):
            try:
                action_enum = ArgumentAction(self.action)
                object.__setattr__(self, 'action', action_enum.value)
            except ValueError:
                raise CLIOrionisValueError(f"Invalid action '{self.action}'. Please use a valid ArgumentAction value")
        elif isinstance(self.action, ArgumentAction):
            object.__setattr__(self, 'action', self.action.value)
        else:
            raise CLIOrionisValueError("Action must be a string or an ArgumentAction enum value")

        # Determine if this is an optional argument (starts with dash)
        is_optional = any(flag.startswith('-') for flag in self.flags)

        # Special handling for boolean types
        if self.type is bool:
            # Auto-configure action based on default value and whether it's optional
            if is_optional:
                action = ArgumentAction.STORE_FALSE.value if self.default else ArgumentAction.STORE_TRUE.value
                object.__setattr__(self, 'action', action)
                # argparse ignores type with store_true/false actions
                object.__setattr__(self, 'type', None)
            else:
                # For positional boolean arguments, keep type as bool
                pass

        # Special handling for list types
        elif self.type is list:
            if self.nargs is None:
                # Auto-configure for accepting multiple values
                object.__setattr__(self, 'nargs', '+' if is_optional else '*')
            # Keep type as list for proper conversion
            object.__setattr__(self, 'type', str)  # argparse expects element type, not list

        # Handle count action - typically used for verbosity flags
        elif self.action == ArgumentAction.COUNT.value:
            object.__setattr__(self, 'type', None)  # count action doesn't use type
            if self.default is None:
                object.__setattr__(self, 'default', 0)

        # Handle const actions
        if self.action in (ArgumentAction.STORE_CONST.value, ArgumentAction.APPEND_CONST.value):
            if self.const is None:
                # Auto-set const based on type or use True as default
                if self.type is bool:
                    object.__setattr__(self, 'const', True)
                elif self.type is int:
                    object.__setattr__(self, 'const', 1)
                elif self.type is str:
                    object.__setattr__(self, 'const', self.dest)
                else:
                    object.__setattr__(self, 'const', True)
            object.__setattr__(self, 'type', None)  # const actions don't use type

        # Handle nargs '?' - optional single argument
        elif self.nargs == '?':
            if self.const is None and is_optional:
                # For optional arguments with nargs='?', set a reasonable const
                object.__setattr__(self, 'const', True if self.type is bool else self.dest)

        # Validate nargs compatibility
        if self.nargs is not None:
            valid_nargs = ['?', '*', '+'] + [str(i) for i in range(0, 10)]
            if isinstance(self.nargs, int):
                if self.nargs < 0:
                    raise CLIOrionisValueError("nargs cannot be negative")
            elif self.nargs not in valid_nargs:
                raise CLIOrionisValueError(f"Invalid nargs value: {self.nargs}")

        # Handle version action
        if self.action == ArgumentAction.VERSION.value:
            object.__setattr__(self, 'type', None)
            if 'version' not in self.dest:
                object.__setattr__(self, 'dest', 'version')

        # Handle help action
        if self.action == ArgumentAction.HELP.value:
            object.__setattr__(self, 'type', None)


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
        }

        # Handle const parameter for specific actions
        const_actions = [
            ArgumentAction.STORE_CONST.value,
            ArgumentAction.APPEND_CONST.value
        ]

        # Add const parameter when it's needed
        if self.action in const_actions or (self.nargs == '?' and self.const is not None):
            kwargs["const"] = self.const

        # Special handling for version action
        if self.action == ArgumentAction.VERSION.value and hasattr(self, 'version'):
            kwargs["version"] = getattr(self, 'version', None)

        # Define actions that don't accept certain parameters
        type_ignored_actions = [
            ArgumentAction.STORE_TRUE.value,
            ArgumentAction.STORE_FALSE.value,
            ArgumentAction.STORE_CONST.value,
            ArgumentAction.APPEND_CONST.value,
            ArgumentAction.COUNT.value,
            ArgumentAction.HELP.value,
            ArgumentAction.VERSION.value
        ]

        # Define actions that don't accept metavar or default parameters
        metavar_ignored_actions = [
            ArgumentAction.STORE_TRUE.value,
            ArgumentAction.STORE_FALSE.value,
            ArgumentAction.COUNT.value,
            ArgumentAction.HELP.value,
            ArgumentAction.VERSION.value
        ]

        # Define actions that don't accept default parameters
        default_ignored_actions = [
            ArgumentAction.STORE_TRUE.value,
            ArgumentAction.STORE_FALSE.value,
            ArgumentAction.STORE_CONST.value,
            ArgumentAction.APPEND_CONST.value,
            ArgumentAction.HELP.value,
            ArgumentAction.VERSION.value
        ]

        # Filter out None values and incompatible parameters
        filtered_kwargs = {}
        for k, v in kwargs.items():
            if v is not None:

                # Skip parameters that are not compatible with certain actions
                if k == "type" and self.action in type_ignored_actions:
                    continue

                # Skip metavar for actions that don't accept it
                if k == "metavar" and self.action in metavar_ignored_actions:
                    continue

                # Skip default for actions that don't accept it
                if k == "default" and self.action in default_ignored_actions:
                    continue

                # Special case: don't include empty strings for metavar in positional args
                if k == "metavar" and is_positional and v == "":
                    continue

                # Add the parameter to the filtered kwargs
                filtered_kwargs[k] = v

        # Remove parameters that are not compatible with positional arguments
        if is_positional:

            # Remove 'required' parameter for positional arguments since it's not supported
            if 'required' in filtered_kwargs:
                del filtered_kwargs['required']

            # Remove 'dest' parameter for positional arguments as argparse calculates it automatically
            if 'dest' in filtered_kwargs:
                del filtered_kwargs['dest']

            # Remove 'metavar' if it's the same as the flag name (redundant)
            if 'metavar' in filtered_kwargs and len(self.flags) == 1:
                flag_upper = self.flags[0].upper()
                if filtered_kwargs['metavar'] == flag_upper:
                    del filtered_kwargs['metavar']

        # For count action, ensure default is an integer
        if self.action == ArgumentAction.COUNT.value and 'default' in filtered_kwargs:
            if not isinstance(filtered_kwargs['default'], int):
                filtered_kwargs['default'] = 0

        # Return the cleaned and validated kwargs dictionary
        return filtered_kwargs