from dataclasses import dataclass, field
from orionis.support.entities.base import BaseEntity
from orionis.foundation.config.logging.validators import IsValidPath, IsValidLevel
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.foundation.config.logging.enums import Level

@dataclass(unsafe_hash=True, kw_only=True)
class Monthly(BaseEntity):
    """
    Configuration entity for monthly log file management.

    Attributes:
        path (str): The file path where the log is stored.
        level (int | str | Level): The logging level (e.g., 'info', 'error', 'debug').
        retention_months (int): The number of months to retain log files before deletion.
    """

    path: str = field(
        default = 'storage/log/monthly.log',
        metadata = {
            "description": "The file path where the log is stored.",
            "default": "storage/log/monthly.log"
        },
    )

    level: int | str | Level = field(
        default = Level.INFO.value,
        metadata = {
            "description": "The logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).",
            "default": Level.INFO.value
        },
    )

    retention_months: int = field(
        default = 4,
        metadata = {
            "description": "The number of months to retain log files before deletion.",
            "default": 4
        },
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Validates the 'path', 'level', and 'retention_months' attributes after dataclass initialization.

        Raises:
            OrionisIntegrityException: If any attribute is invalid.
                - 'path' must be a non-empty string.
                - 'level' must be an int, str, or Level enum, and a valid logging level.
                - 'retention_months' must be an integer between 1 and 12 (inclusive).
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

        # Validate 'retention_months'
        if not isinstance(self.retention_months, int):
            raise OrionisIntegrityException(
                f"Invalid type for 'retention_months': expected int, got {type(self.retention_months).__name__}."
            )
        if not (1 <= self.retention_months <= 12):
            raise OrionisIntegrityException(
                f"'retention_months' must be an integer between 1 and 12 (inclusive), got {self.retention_months}."
            )