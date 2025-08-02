from enum import Enum

class SQLiteSynchronous(Enum):
    """
    Enum representing the possible values for SQLite's synchronous setting.
    Attributes:
        FULL: Provides maximum data integrity and durability, but is the slowest option.
        NORMAL: Offers a balance between data safety and performance.
        OFF: Maximizes speed, but data may be lost in the event of a crash.
    These values correspond to the SQLite PRAGMA synchronous settings:
    https://www.sqlite.org/pragma.html#pragma_synchronous
    """

    FULL = "FULL"      # Greater safety, slower
    NORMAL = "NORMAL"  # Balance between safety and performance
    OFF = "OFF"        # Greater speed, less safe in case of failures