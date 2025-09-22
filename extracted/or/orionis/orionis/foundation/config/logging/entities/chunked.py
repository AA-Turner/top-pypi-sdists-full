from dataclasses import dataclass, field
from orionis.support.entities.base import BaseEntity
from orionis.foundation.config.logging.validators import IsValidPath, IsValidLevel
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.foundation.config.logging.enums import Level

@dataclass(unsafe_hash=True, kw_only=True)
class Chunked(BaseEntity):
    """
    Configuration for chunked log file rotation.

    This class defines the configuration for managing log files by splitting them into chunks
    based on file size and limiting the number of retained log files. This prevents log files
    from growing indefinitely and helps manage disk usage.

    Attributes
    ----------
    path : str
        Filesystem path where chunked log files are stored.
    level : int | str | Level
        Logging level for the log file. Accepts an integer, string, or Level enum.
    mb_size : int
        Maximum size (in megabytes) of a single log file before a new chunk is created.
    files : int
        Maximum number of log files to retain. Older files are deleted when this limit is exceeded.
    """

    path: str = field(
        default = 'storage/logs/chunked.log',
        metadata = {
            "description": "The file path where the log is stored.",
            "default": "storage/logs/chunked.log"
        },
    )

    level: int | str | Level = field(
        default = Level.INFO.value,
        metadata = {
            "description": "The logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).",
            "default": Level.INFO.value
        },
    )

    mb_size: int = field(
        default = 10,
        metadata = {
            "description": "Maximum size (in MB) of a log file before chunking.",
            "default": 10
        },
    )

    files: int = field(
        default = 5,
        metadata = {
            "description": "Maximum number of log files to retain.",
            "default": 5
        },
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Performs validation and normalization of configuration fields.

        - path: Validates that the path is correct using the IsValidPath validator.
        - level: Validates that the log level is correct using the IsValidLevel validator.
        - mb_size: Checks that it is an integer between 1 and 1000 (MB).
        - files: Checks that it is a positive integer greater than 0.

        Raises
        ------
        OrionisIntegrityException
            If any of the configuration values are invalid.
        """

        # Validate 'path' using the IsValidPath validator
        IsValidPath(self.path)

        # Validate 'level' using the IsValidLevel validator
        IsValidLevel(self.level)

        # Assign the level value.
        if isinstance(self.level, Level):
            self.level = self.level.value
        elif isinstance(self.level, str):
            self.level = Level[self.level.strip().upper()].value
        elif isinstance(self.level, int):
            self.level = self.level

        # Validate 'mb_size'
        if not isinstance(self.mb_size, int):
            raise OrionisIntegrityException(
                f"'mb_size' must be an integer in MB, got {type(self.mb_size).__name__}."
            )
        if self.mb_size < 1 or self.mb_size > 1000:
            raise OrionisIntegrityException(
                f"'mb_size' must be between 1 and 1000 MB, got {self.mb_size}."
            )

        # Validate 'files'
        if not isinstance(self.files, int) or self.files < 1:
            raise OrionisIntegrityException(
                f"'files' must be a positive integer greater than 0, got {self.files} ({type(self.files).__name__})."
            )