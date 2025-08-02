from dataclasses import dataclass, field
from orionis.support.entities.base import BaseEntity
from orionis.foundation.config.logging.validators import IsValidPath, IsValidLevel
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.foundation.config.logging.enums import Level

@dataclass(unsafe_hash=True, kw_only=True)
class Weekly(BaseEntity):
    """
    Configuration entity for weekly log file management.

    Attributes:
        path (str): The file path where the log is stored.
        level (int | str | Level): The logging level (e.g., 'info', 'error', 'debug').
        retention_weeks (int): The number of weeks to retain log files before deletion.
    """

    path: str = field(
        default = 'storage/log/weekly.log',
        metadata = {
            "description": "The file path where the log is stored.",
            "default": "storage/log/weekly.log"
        },
    )

    level: int | str | Level = field(
        default = Level.INFO.value,
        metadata = {
            "description": "The logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).",
            "default": Level.INFO.value
        },
    )

    retention_weeks: int = field(
        default = 4,
        metadata = {
            "description": "The number of weeks to retain log files before deletion.",
            "default": 4
        },
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Post-initialization validation for Weekly configuration.

        Validates:
            - 'path' is a non-empty string.
            - 'level' is a valid int, str, or Level enum member.
            - 'retention_weeks' is an integer between 1 and 12 (inclusive).

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

        # Validate 'retention_weeks'
        if not isinstance(self.retention_weeks, int):
            raise OrionisIntegrityException(
                f"Invalid type for 'retention_weeks': expected int, got {type(self.retention_weeks).__name__}."
            )
        if self.retention_weeks < 1 or self.retention_weeks > 12:
            raise OrionisIntegrityException(
                f"'retention_weeks' must be an integer between 1 and 12 (inclusive), but got {self.retention_weeks}."
            )