from dataclasses import dataclass, field
from orionis.support.entities.base import BaseEntity
from orionis.foundation.config.logging.validators import IsValidLevel, IsValidPath
from orionis.foundation.config.logging.enums import Level

@dataclass(unsafe_hash=True, kw_only=True)
class Stack(BaseEntity):
    """
    Represents the configuration for a logging stack, including the log file path and logging level.
    """

    path: str = field(
        default = 'storage/log/stack.log',
        metadata = {
            "description": "The file path where the log is stored.",
            "default": "storage/log/stack.log"
        },
    )

    level: int | str | Level = field(
        default = Level.INFO.value,
        metadata = {
            "description": "The logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).",
            "default": Level.INFO.value
        },
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Validates the 'path' and 'level' attributes after dataclass initialization.

        Raises:
            OrionisIntegrityException: If 'path' is not a non-empty string, or if 'level' is not a valid type or value.
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