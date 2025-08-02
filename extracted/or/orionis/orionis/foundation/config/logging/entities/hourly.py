from dataclasses import dataclass, field
from orionis.support.entities.base import BaseEntity
from orionis.foundation.config.logging.validators import IsValidLevel, IsValidPath
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.foundation.config.logging.enums import Level

@dataclass(unsafe_hash=True, kw_only=True)
class Hourly(BaseEntity):
    """
    Represents the configuration for hourly log file management.

    Attributes:
        path (str): The file path where the log is stored.
        level (int | str | Level): The logging level (e.g., 'info', 'error', 'debug').
        retention_hours (int): The number of hours to retain log files before deletion.
    """

    path: str = field(
        default = 'storage/log/hourly.log',
        metadata = {
            "description": "The file path where the log is stored.",
            "default": "storage/log/hourly.log"
        },
    )

    level: int | str | Level = field(
        default = Level.INFO.value,
        metadata = {
            "description": "The logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).",
            "default": Level.INFO.value
        },
    )

    retention_hours: int = field(
        default = 24,
        metadata = {
            "description": "The number of hours to retain log files before deletion.",
            "default": 24
        },
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Validates the attributes after dataclass initialization.

        Raises:
            OrionisIntegrityException: If any attribute is invalid.
                - 'path' must be a non-empty string.
                - 'level' must be an int, str, or Level enum, and a valid value.
                - 'retention_hours' must be an integer between 1 and 168.
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

        # Validate 'retention_hours'
        if not isinstance(self.retention_hours, int) or self.retention_hours < 0:
            raise OrionisIntegrityException(
                f"File cache configuration error: 'retention_hours' must be a non-negative integer, got {self.retention_hours}."
            )
        if self.retention_hours < 1 or self.retention_hours > 168:
            raise OrionisIntegrityException(
                f"File cache configuration error: 'retention_hours' must be between 1 and 168, got {self.retention_hours}."
            )