from enum import Enum

class IfExists(Enum):
    REPLACE = "replace"
    APPEND = "append"
    ERROR = "error"
    SKIP = "skip"
    FILL_EMPTY = "fill_empty"