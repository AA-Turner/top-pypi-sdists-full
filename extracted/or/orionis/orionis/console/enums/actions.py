from enum import Enum

class ArgumentAction(Enum):
    """
    Enumeration of valid action types for use with Python's argparse module.

    This enum defines all standard action types that can be assigned to command-line arguments
    using argparse. Each member represents a specific way argparse processes and stores argument values.

    Attributes
    ----------
    STORE : str
        Stores the argument value directly.
    STORE_CONST : str
        Stores a constant value when the argument is specified.
    STORE_TRUE : str
        Stores True when the argument is specified.
    STORE_FALSE : str
        Stores False when the argument is specified.
    APPEND : str
        Appends each argument value to a list.
    APPEND_CONST : str
        Appends a constant value to a list when the argument is specified.
    COUNT : str
        Counts the number of times the argument is specified.
    HELP : str
        Displays the help message and exits.
    VERSION : str
        Displays version information and exits.

    Returns
    -------
    str
        The string value representing the corresponding argparse action type.
    """

    # Stores the argument value directly
    STORE = "store"

    # Stores a constant value when the argument is specified
    STORE_CONST = "store_const"

    # Stores True when the argument is specified
    STORE_TRUE = "store_true"

    # Stores False when the argument is specified
    STORE_FALSE = "store_false"

    # Appends each argument value to a list
    APPEND = "append"

    # Appends a constant value to a list when the argument is specified
    APPEND_CONST = "append_const"

    # Counts the number of times the argument is specified
    COUNT = "count"

    # Displays the help message and exits the program
    HELP = "help"

    # Displays version information and exits the program
    VERSION = "version"