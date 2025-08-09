from enum import Enum

class EnvironmentValueType(Enum):
    """
    Enum representing the supported types for casting environment variable values.

    Attributes
    ----------
    BASE64 : str
        Represents a base64 encoded value.
    PATH : str
        Represents a file system path.
    STR : str
        Represents a string value.
    INT : str
        Represents an integer value.
    FLOAT : str
        Represents a floating-point value.
    BOOL : str
        Represents a boolean value.
    LIST : str
        Represents a list value.
    DICT : str
        Represents a dictionary value.
    TUPLE : str
        Represents a tuple value.
    SET : str
        Represents a set value.
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
