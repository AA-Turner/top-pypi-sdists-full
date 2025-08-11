from enum import Enum

class ArgumentAction(Enum):
    """
    Enumeration for valid argparse action types.

    This enum provides a comprehensive list of all standard action types
    that can be used with Python's argparse module when defining command
    line arguments. Each enum member corresponds to a specific behavior
    for how argument values should be processed and stored.

    Returns
    -------
    str
        The string value representing the argparse action type.
    """

    # Store the argument value directly
    STORE = "store"

    # Store a constant value when the argument is specified
    STORE_CONST = "store_const"

    # Store True when the argument is specified
    STORE_TRUE = "store_true"

    # Store False when the argument is specified
    STORE_FALSE = "store_false"

    # Append each argument value to a list
    APPEND = "append"

    # Append a constant value to a list when the argument is specified
    APPEND_CONST = "append_const"

    # Count the number of times the argument is specified
    COUNT = "count"

    # Display help message and exit
    HELP = "help"

    # Display version information and exit
    VERSION = "version"