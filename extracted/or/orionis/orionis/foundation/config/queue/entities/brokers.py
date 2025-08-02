
from dataclasses import dataclass, field
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.foundation.config.queue.entities.database import Database
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class Brokers(BaseEntity):
    """
    Represents the configuration for queue brokers.

    Attributes:
        sync (bool): Indicates if the sync broker is enabled. Defaults to True.
        database (Database): The configuration for the database-backed queue. Defaults to a new Database instance.

    Methods:
        __post_init__():
            Validates and normalizes the properties after initialization.
            Ensures 'sync' is a boolean and 'database' is an instance of Database.
    """

    sync: bool = field(
        default = True,
        metadata = {
            "description": "Indicates if the sync broker is enabled.",
            "default": True
        }
    )

    database: Database | dict = field(
        default_factory = lambda: Database(),
        metadata = {
            "description": "The configuration for the database-backed queue.",
            "default": lambda: Database().toDict()
        }
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Post-initialization validation for the Brokers entity.

        Validates and normalizes the following properties:
        - sync: Must be a boolean.
        - database: Must be an instance of the Database class.
        """

        # Validate 'sync' property
        if not isinstance(self.sync, bool):
            raise OrionisIntegrityException("sync must be a boolean.")

        # Validate 'database' property
        if not isinstance(self.database, (Database, dict)):
            raise OrionisIntegrityException("database must be an instance of the Database class or a dictionary.")
        if isinstance(self.database, dict):
            self.database = Database(**self.database)
