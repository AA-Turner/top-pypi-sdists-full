from enum import Enum

class PersistentDrivers(Enum):
    """
    Enumeration of supported persistent storage drivers.

    Attributes
    ----------
    JSON : str
        Represents the JSON file-based storage driver.
    SQLITE : str
        Represents the SQLite database storage driver.
    """

    JSON = 'json'
    SQLITE = 'sqlite'