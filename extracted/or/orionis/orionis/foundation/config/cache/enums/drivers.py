from enum import Enum

class Drivers(Enum):
    """
    Enumeration of supported cache drivers.

    Attributes:
        MEMORY: Represents an in-memory cache driver.
        FILE: Represents a file-based cache driver.
    """
    MEMORY = "memory"
    FILE = "file"