from typing import Literal

MissingValueStrategy = Literal[
    # Raise a TypeError if missing values are found
    "error",
    # PROBABLY THIS ONE
    # Coerce missing values to the default value for the feature, if one is defined.
    # Otherwise, raise a TypeError
    "default_or_error",
    # Coerce missing values to the default value for the feature, if one is defined.
    # Otherwise, treat missing values as valid.
    "default_or_allow",
    # Treat missing values as valid values
    "allow",
]
