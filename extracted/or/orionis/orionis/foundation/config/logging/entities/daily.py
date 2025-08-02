from dataclasses import dataclass, field
from datetime import datetime, time
from orionis.support.entities.base import BaseEntity
from orionis.foundation.config.logging.validators import IsValidPath, IsValidLevel
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.foundation.config.logging.enums import Level

@dataclass(unsafe_hash=True, kw_only=True)
class Daily(BaseEntity):
    """
    Represents the configuration for daily log file rotation.

    Attributes:
        path (str): The file path where the log is stored.
        level (int | str | Level): The logging level (e.g., 'info', 'error', 'debug').
        retention_days (int): The number of days to retain log files before deletion.
        at (time): The time of day when the log rotation should occur.
    """

    path: str = field(
        default = 'storage/log/daily.log',
        metadata = {
            "description": "The file path where the log is stored.",
            "default": "storage/log/daily.log"
        },
    )

    level: int | str | Level = field(
        default = Level.INFO.value,
        metadata = {
            "description": "The logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).",
            "default": Level.INFO.value
        },
    )

    retention_days: int = field(
        default = 7,
        metadata = {
            "description": "The number of days to retain log files before deletion.",
            "default": 7
        },
    )

    at: time | str = field(
        default_factory = lambda: time(0, 0).strftime("%H:%M"),
        metadata = {
            "description": "The time of day when the log rotation should occur.",
            "default": "00:00"
        },
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Validates and normalizes the attributes after dataclass initialization.

        Raises:
            OrionisIntegrityException: If any attribute is invalid.
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

        # Validate 'retention_days'
        if not isinstance(self.retention_days, int):
            raise OrionisIntegrityException(
                f"'retention_days' must be an integer, got {type(self.retention_days).__name__}."
            )
        if not (1 <= self.retention_days <= 90):
            raise OrionisIntegrityException(
                f"'retention_days' must be between 1 and 90, got {self.retention_days}."
            )

        # Validate 'at' must be a time instance or a valid "HH:MM" string
        if not isinstance(self.at, (time, str)):
            raise OrionisIntegrityException(
                f"'at' must be a datetime.time instance or a 'HH:MM' string, got {type(self.at).__name__}."
            )

        # Validate and normalize 'at'
        if isinstance(self.at, str):
            try:
                parsed_time = datetime.strptime(self.at, "%H:%M").time()
                self.at = parsed_time
            except ValueError:
                raise OrionisIntegrityException(
                    f"'at' must be a valid time string in 'HH:MM' format, got '{self.at}'."
                )
        elif not isinstance(self.at, time):
            raise OrionisIntegrityException(
                f"'at' must be a datetime.time instance or a 'HH:MM' string, got {type(self.at).__name__}."
            )

        # Normalize 'at' to "HH:MM" format
        self.at = self.at.strftime("%H:%M")