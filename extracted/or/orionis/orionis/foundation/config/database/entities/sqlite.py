from dataclasses import dataclass, field
from orionis.foundation.config.database.enums import (
    SQLiteForeignKey,
    SQLiteJournalMode,
    SQLiteSynchronous
)
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.services.environment.env import Env
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class SQLite(BaseEntity):
    """
    Data class to represent the SQLite database configuration.

    Attributes
    ----------
    driver : str
        The database driver being used, e.g., 'sqlite'.
    url : str
        The URL for connecting to the database.
    database : str
        The path to the SQLite database file.
    prefix : str
        Prefix for table names.
    foreign_key_constraints : bool
        Whether foreign key constraints are enabled.
    busy_timeout : Optional[int]
        The timeout period (in milliseconds) before retrying a locked database.
    journal_mode : Optional[str]
        The journal mode used for transactions.
    synchronous : Optional[str]
        The synchronization level for the database.
    """

    driver: str = field(
        default = 'sqlite',
        metadata = {
            "description": "The database driver being used.",
            "example": "sqlite",
        },
    )

    url: str = field(
        default_factory = lambda: Env.get('DB_URL', 'sqlite:///' + Env.get('DB_DATABASE', 'database/database.sqlite')),
        metadata = {
            "description": "The URL for connecting to the database.",
            "example": "sqlite:///database/database.sqlite",
        },
    )

    database: str = field(
        default_factory = lambda: Env.get('DB_DATABASE', 'database.sqlite'),
        metadata = {
            "description": "The path to the SQLite database file.",
            "example": "database.sqlite",
        },
    )

    prefix: str = field(
        default_factory = lambda: Env.get('DB_PREFIX', ''),
        metadata = {
            "description": "Prefix for table names.",
            "example": "",
        },
    )

    foreign_key_constraints: bool | SQLiteForeignKey = field(
        default_factory = lambda: Env.get('DB_FOREIGN_KEYS', SQLiteForeignKey.OFF.value),
        metadata = {
            "description": "Whether foreign key constraints are enabled.",
            "example": SQLiteForeignKey.OFF.value
        },
    )

    busy_timeout: int = field(
        default_factory = lambda: Env.get('DB_BUSY_TIMEOUT', 5000),
        metadata = {
            "description": "The timeout period (in milliseconds) before retrying a locked database.",
            "example": 5000
        },
    )

    journal_mode: str | SQLiteJournalMode = field(
        default_factory = lambda: Env.get('DB_JOURNAL_MODE', SQLiteJournalMode.DELETE.value),
        metadata = {
            "description": "The journal mode used for transactions.",
            "example": SQLiteJournalMode.DELETE.value
        },
    )

    synchronous: str | SQLiteSynchronous = field(
        default_factory = lambda: Env.get('DB_SYNCHRONOUS', SQLiteSynchronous.NORMAL.value),
        metadata = {
            "description": "The synchronization level for the database.",
            "example": SQLiteSynchronous.NORMAL.value
        },
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Post-initialization validation for SQLite database configuration fields.

        This method ensures that all configuration attributes are of the correct type and meet required constraints:
        - `driver`: Must be a non-empty string (e.g., 'sqlite').
        - `url`: Must be a non-empty string (e.g., 'sqlite:///database/database.sqlite').
        - `database`: Must be a non-empty string representing the database file path.
        - `prefix`: Must be a string (can be empty).
        - `foreign_key_constraints`: Must be a boolean (True or False).
        - `busy_timeout`: If provided, must be a non-negative integer (milliseconds) or None.
        - `journal_mode`: If provided, must be a string or None (e.g., 'WAL', 'DELETE').
        - `synchronous`: If provided, must be a string or None (e.g., 'FULL', 'NORMAL', 'OFF').

        Raises:
            OrionisIntegrityException: If any attribute fails its validation check.
        """

        # Validate driver
        if not isinstance(self.driver, str) or not self.driver.strip():
            raise OrionisIntegrityException("Invalid 'driver': must be a non-empty string (e.g., 'sqlite').")

        # Validate url
        if not isinstance(self.url, str) or not self.url.strip():
            raise OrionisIntegrityException("Invalid 'url': must be a non-empty string (e.g., 'sqlite:///database/database.sqlite').")

        # Validate database
        if not isinstance(self.database, str) or not self.database.strip():
            raise OrionisIntegrityException("Invalid 'database': must be a non-empty string representing the database file path.")

        # Validate prefix
        if not isinstance(self.prefix, str):
            raise OrionisIntegrityException("Invalid 'prefix': must be a string (can be empty).")

        # Validate foreign_key_constraints
        options_foreign_keys = SQLiteForeignKey._member_names_
        if isinstance(self.foreign_key_constraints, str):
            _value = self.foreign_key_constraints.upper().strip()
            if _value not in options_foreign_keys:
                raise OrionisIntegrityException(
                    f"The 'foreign_key_constraints' attribute must be a valid option {str(SQLiteForeignKey._member_names_)}"
                )
            else:
                self.foreign_key_constraints = SQLiteForeignKey[_value].value
        else:
            self.foreign_key_constraints = self.foreign_key_constraints.value

        # Validate busy_timeout
        if self.busy_timeout is not None and (not isinstance(self.busy_timeout, int) or self.busy_timeout < 0):
            raise OrionisIntegrityException("Invalid 'busy_timeout': must be a non-negative integer (milliseconds) or None.")

        # Validate journal_mode
        options_journal_mode = SQLiteJournalMode._member_names_
        if isinstance(self.journal_mode, str):
            _value = self.journal_mode.upper().strip()
            if _value not in options_journal_mode:
                raise OrionisIntegrityException(
                    f"The 'journal_mode' attribute must be a valid option {str(SQLiteJournalMode._member_names_)}"
                )
            else:
                self.journal_mode = SQLiteJournalMode[_value].value
        else:
            self.journal_mode = self.journal_mode.value

        # Validate synchronous
        options_synchronous = SQLiteSynchronous._member_names_
        if isinstance(self.synchronous, str):
            _value = self.synchronous.upper().strip()
            if _value not in options_synchronous:
                raise OrionisIntegrityException(
                    f"The 'synchronous' attribute must be a valid option {str(SQLiteSynchronous._member_names_)}"
                )
            else:
                self.synchronous = SQLiteSynchronous[_value].value
        else:
            self.synchronous = self.synchronous.value