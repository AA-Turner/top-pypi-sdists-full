from dataclasses import dataclass, field
from orionis.foundation.config.database.entities.mysql import MySQL
from orionis.foundation.config.database.entities.oracle import Oracle
from orionis.foundation.config.database.entities.pgsql import PGSQL
from orionis.foundation.config.database.entities.sqlite import SQLite
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class Connections(BaseEntity):
    """
    Data class to represent all database connections used by the application.

    Attributes
    ----------
    sqlite : Sqlite
        Configuration for the SQLite database connection.
    mysql : MySQL
        Configuration for the MySQL database connection.
    pgsql : Pgsql
        Configuration for the PostgreSQL database connection.
    oracle : Oracle
        Configuration for the Oracle database connection.
    """
    sqlite: SQLite | dict = field(
        default_factory = lambda: SQLite(),
        metadata = {
            "description": "SQLite database connection configuration",
            "default": lambda: SQLite().toDict()
        }
    )

    mysql: MySQL | dict = field(
        default_factory = lambda: MySQL(),
        metadata = {
            "description": "MySQL database connection configuration",
            "default": lambda: MySQL().toDict()
        }
    )

    pgsql: PGSQL | dict = field(
        default_factory = lambda: PGSQL(),
        metadata = {
            "description": "PostgreSQL database connection configuration",
            "default": lambda: PGSQL().toDict()
        }
    )

    oracle: Oracle | dict = field(
        default_factory = lambda: Oracle(),
        metadata = {
            "description": "Oracle database connection configuration",
            "default": lambda: Oracle().toDict()
        }
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Post-initialization method to validate the types of database connection attributes.
        Ensures that the attributes `sqlite`, `mysql`, `pgsql`, and `oracle` are instances of their respective classes.
        Raises:
            OrionisIntegrityException: If any attribute is not an instance of its expected class.
        """

        # Validate `sqlite` attribute
        if not isinstance(self.sqlite, (SQLite, dict)):
            raise OrionisIntegrityException(
                f"Invalid type for 'sqlite': expected 'SQLite' or 'dict', got '{type(self.sqlite).__name__}'."
            )
        if isinstance(self.sqlite, dict):
            self.sqlite = SQLite(**self.sqlite)

        # Validate `mysql` attribute
        if not isinstance(self.mysql, (MySQL, dict)):
            raise OrionisIntegrityException(
                f"Invalid type for 'mysql': expected 'MySQL' or 'dict', got '{type(self.mysql).__name__}'."
            )
        if isinstance(self.mysql, dict):
            self.mysql = MySQL(**self.mysql)

        # Validate `pgsql` attribute
        if not isinstance(self.pgsql, (PGSQL, dict)):
            raise OrionisIntegrityException(
                f"Invalid type for 'pgsql': expected 'PGSQL' or 'dict', got '{type(self.pgsql).__name__}'."
            )
        if isinstance(self.pgsql, dict):
            self.pgsql = PGSQL(**self.pgsql)

        # Validate `oracle` attribute
        if not isinstance(self.oracle, (Oracle, dict)):
            raise OrionisIntegrityException(
                f"Invalid type for 'oracle': expected 'Oracle' or 'dict', got '{type(self.oracle).__name__}'."
            )
        if isinstance(self.oracle, dict):
            self.oracle = Oracle(**self.oracle)