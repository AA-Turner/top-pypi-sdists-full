
from dataclasses import dataclass, field
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.foundation.config.queue.enums import Strategy
from orionis.support.entities.base import BaseEntity
import re

@dataclass(unsafe_hash=True, kw_only=True)
class Database(BaseEntity):
    """
    Represents the configuration entity for a database-backed queue.

    Attributes:
        table (str): The name of the table used for the queue. Must match the pattern `[a-z_][a-z_]*` (lowercase letters or underscores only, no numbers).
        queue (str): The name of the queue. Must contain only ASCII characters.
        retry_after (int): The time in seconds to wait before retrying a failed job. Must be a positive integer.
        strategy (str | Strategy): The strategy used for the queue. Options are FIFO, LIFO, or PRIORITY. Can be provided as a string (case-insensitive) or as a `Strategy` enum member.

    Methods:
        __post_init__():
            Validates and normalizes the entity's properties after initialization.
            - Ensures `table` is a valid string matching the required pattern.
            - Ensures `queue` is a valid ASCII string.
            - Ensures `retry_after` is a positive integer.
            - Ensures `strategy` is a valid string or `Strategy` enum member, and normalizes it to the corresponding enum value.
    """

    table: str = field(
        default = "jobs",
        metadata = {
            "description": "The name of the table used for the queue.",
            "default": "jobs"
        }
    )

    queue: str = field(
        default = "default",
        metadata = {
            "description": "The name of the queue.",
            "default": "default"
        }
    )

    retry_after: int = field(
        default = 90,
        metadata = {
            "description": "The time in seconds to wait before retrying a failed job.",
            "default": 90
        }
    )

    strategy : str | Strategy = field(
        default = Strategy.FIFO.value,
        metadata = {
            "description": "The strategy used for the queue. Options are FIFO, LIFO, or PRIORITY.",
            "default": Strategy.FIFO.value
        }
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Post-initialization validation for the entity.

        Validates and normalizes the following properties:
        - `table`: Must be a string matching the pattern `[a-z_][a-z_]*` (lowercase letters or underscores only, no numbers).
        - `queue`: Must be a string containing only ASCII characters.
        - `retry_after`: Must be a positive integer.
        - `strategy`: Must be either a string (matching a valid `Strategy` member name, case-insensitive) or an instance of `Strategy`. Converts the value to the corresponding `Strategy` enum value.

        Raises:
            OrionisIntegrityException: If any property fails validation.
        """

        # Validate `table` attribute
        if not isinstance(self.table, str):
            raise OrionisIntegrityException("The 'table' property must be a string.")
        if not re.fullmatch(r'[a-z_][a-z_]*', self.table):
            raise OrionisIntegrityException(
                "The 'table' property must be a valid table name: start with a lowercase letter or underscore, contain only lowercase letters or underscores (no numbers allowed)."
            )

        # Validate `queue` attribute
        if not isinstance(self.queue, str):
            raise OrionisIntegrityException("The 'queue' property must be a string.")
        try:
            self.queue.encode('ascii')
        except UnicodeEncodeError:
            raise OrionisIntegrityException("The 'queue' property must contain only ASCII characters (no UTF-8 or non-ASCII allowed).")

        # Validate `retry_after` attribute
        if not isinstance(self.retry_after, int) or self.retry_after <= 0:
            raise OrionisIntegrityException("The 'retry_after' property must be a positive integer.")

        # Validate `strategy` attribute
        if not isinstance(self.strategy, (str, Strategy)):
            raise OrionisIntegrityException("The 'strategy' property must be a string or an instance of Strategy.")
        if isinstance(self.strategy, str):
            options = Strategy._member_names_
            _value = str(self.strategy).upper().strip()
            if _value not in options:
                raise OrionisIntegrityException(
                    f"The 'strategy' property must be one of the following: {', '.join(options)}."
                )
            else:
                self.strategy = Strategy[_value].value
        else:
            self.strategy = self.strategy.value