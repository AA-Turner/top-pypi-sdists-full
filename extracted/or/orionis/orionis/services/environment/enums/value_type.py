from enum import Enum

class EnvironmentValueType(Enum):
    """
    Enum representing supported environment variable cast types.

    Attributes
    ----------
    PATH : EnvCastType
        Cast to a file system path.
    STR : EnvCastType
        Cast to a string.
    INT : EnvCastType
        Cast to an integer.
    FLOAT : EnvCastType
        Cast to a floating-point number.
    BOOL : EnvCastType
        Cast to a boolean value.
    LIST : EnvCastType
        Cast to a list.
    DICT : EnvCastType
        Cast to a dictionary.
    TUPLE : EnvCastType
        Cast to a tuple.
    SET : EnvCastType
        Cast to a set.

    Returns
    -------
    EnvCastType
        An enumeration member representing the desired cast type.
    """

    BASE64 = 'base64' # Represents a base64 encoded type
    PATH = 'path'     # Represents a file system path
    STR = 'str'       # Represents a string type
    INT = 'int'       # Represents an integer type
    FLOAT = 'float'   # Represents a floating-point type
    BOOL = 'bool'     # Represents a boolean type
    LIST = 'list'     # Represents a list type
    DICT = 'dict'     # Represents a dictionary type
    TUPLE = 'tuple'   # Represents a tuple type
    SET = 'set'       # Represents a set type