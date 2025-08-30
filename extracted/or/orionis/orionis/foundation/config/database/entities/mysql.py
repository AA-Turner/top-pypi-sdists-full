from dataclasses import dataclass, field
from orionis.foundation.config.database.enums import (
    MySQLCharset,
    MySQLCollation,
    MySQLEngine
)
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.services.environment.env import Env
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class MySQL(BaseEntity):
    """
    Data class to represent the MySQL database configuration.

    Attributes
    ----------
    driver : str
        The database driver being used, e.g., 'mysql'.
    host : str
        The host address for the MySQL server.
    port : str
        The port for connecting to the MySQL server.
    database : str
        The name of the MySQL database.
    username : str
        The username for connecting to the MySQL database.
    password : str
        The password for the MySQL database.
    unix_socket : str
        The path to the Unix socket for MySQL connections (optional).
    charset : str
        The charset used for the connection.
    collation : str
        The collation for the database.
    prefix : str
        Prefix for table names.
    prefix_indexes : bool
        Whether to prefix index names.
    strict : bool
        Whether to enforce strict SQL mode.
    engine : Optional[str]
        The storage engine for the MySQL database (optional).
    """

    driver: str = field(
        default = "mysql",
        metadata = {
            "description": "The database driver being used.",
            "default": "mysql"
        }
    )

    host: str = field(
        default_factory = lambda: Env.get("DB_HOST", "127.0.0.1"),
        metadata = {
            "description": "The host address for the MySQL server.",
            "default": "127.0.0.1"
        }
    )

    port: int = field(
        default_factory = lambda: Env.get("DB_PORT", 3306),
        metadata = {
            "description": "The port for connecting to the MySQL server.",
            "default": 3306
        }
    )

    database: str = field(
        default_factory = lambda: Env.get("DB_DATABASE", "orionis"),
        metadata = {
            "description": "The name of the MySQL database.",
            "default": "orionis"
        }
    )

    username: str = field(
        default_factory = lambda: Env.get("DB_USERNAME", "root"),
        metadata = {
            "description": "The username for connecting to the MySQL database.",
            "default": "root"
        }
    )

    password: str = field(
        default_factory = lambda: Env.get("DB_PASSWORD", ""),
        metadata = {
            "description": "The password for the MySQL database.",
            "default": ""
        }
    )

    unix_socket: str = field(
        default_factory = lambda: Env.get("DB_SOCKET", ""),
        metadata = {
            "description": "The path to the Unix socket for MySQL connections (optional).",
            "default": ""
        }
    )

    charset: str | MySQLCharset = field(
        default = MySQLCharset.UTF8MB4.value,
        metadata = {
            "description": "The charset used for the connection.",
            "default": MySQLCharset.UTF8MB4.value
        }
    )

    collation: str | MySQLCollation = field(
        default = MySQLCollation.UTF8MB4_UNICODE_CI.value,
        metadata = {
            "description": "The collation for the database.",
            "default": MySQLCollation.UTF8MB4_UNICODE_CI.value
        }
    )

    prefix: str = field(
        default = "",
        metadata = {
            "description": "Prefix for table names.",
            "default": ""
        }
    )

    prefix_indexes: bool = field(
        default = True,
        metadata = {
            "description": "Whether to prefix index names.",
            "default": True
        }
    )

    strict: bool = field(
        default = True,
        metadata = {
            "description": "Whether to enforce strict SQL mode.",
            "default": True
        }
    )

    engine: str | MySQLEngine = field(
        default = MySQLEngine.INNODB.value,
        metadata = {
            "description": "The storage engine for the MySQL database (optional).",
            "default": MySQLEngine.INNODB.value
        }
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Post-initialization validation for MySQL database entity configuration.
        This method performs comprehensive validation on the instance attributes to ensure
        that all required fields are present and correctly typed. It raises an
        OrionisIntegrityException with a descriptive message if any validation fails.

        Validations performed:
        - Host: Must be a non-empty string.
        - Port: Must be an integer between 1 and 65535.
        - Database name: Must be a non-empty string.
        - Username: Must be a non-empty string.
        - Password: Must be a string (can be empty).
        - Unix socket: If provided, must be a string.
        - Charset: Must be a non-empty string.
        - Collation: Must be a non-empty string.
        - Prefix: If provided, must be a string.
        - Prefix indexes: Must be a boolean.
        - Strict: Must be a boolean.
        - Engine: If provided, must be a string.

        Raises:
            OrionisIntegrityException: If any attribute fails validation.
        """

        # Validate driver
        if self.driver not in ['mysql']:
            raise OrionisIntegrityException("Invalid driver: expected 'mysql'. Please ensure the 'driver' attribute is set to 'mysql'.")

        # Validate host
        if not self.host or not isinstance(self.host, str):
            raise OrionisIntegrityException("Database host must be a non-empty string.")

        # Validate port type
        if not isinstance(self.port, int):
            raise OrionisIntegrityException("Database port must be an integer.")

        # Validate port range
        if self.port > 65535 or self.port < 1:
            raise OrionisIntegrityException("Database port must be between 1 and 65535.")

        # Validate database name
        if not self.database or not isinstance(self.database, str):
            raise OrionisIntegrityException("Database name must be a non-empty string.")

        # Validate username
        if not self.username or not isinstance(self.username, str):
            raise OrionisIntegrityException("Database username must be a non-empty string.")

        # Validate password
        if self.password is None or not isinstance(self.password, str):
            raise OrionisIntegrityException("Database password must be a string (can be empty for some setups).")

        # Validate unix_socket
        if self.unix_socket is not None and not isinstance(self.unix_socket, str):
            raise OrionisIntegrityException("Unix socket path must be a string.")

        # Validate charset
        if not self.charset or not isinstance(self.charset, (str, MySQLCharset)):
            raise OrionisIntegrityException("Charset must be a non-empty string or MySQLCharset enum.")

        # Convert charset to MySQLCharset enum if it's a string
        if isinstance(self.charset, str):
            _value = str(self.charset).upper().strip()
            options_charsets = MySQLCharset._member_names_
            if _value not in options_charsets:
                raise OrionisIntegrityException(f"Charset must be a valid MySQLCharset ({str(options_charsets)}) or string.")
            else:
                self.charset = MySQLCharset[_value].value
        else:
            self.charset = self.charset.value

        # Validate collation
        if not self.collation or not isinstance(self.collation, (str, MySQLCollation)):
            raise OrionisIntegrityException("Collation must be a non-empty string or MySQLCollation enum.")

        # Convert collation to MySQLCollation enum if it's a string
        if isinstance(self.collation, str):
            _value = str(self.collation).upper().strip()
            options_collations = MySQLCollation._member_names_
            if _value not in options_collations:
                raise OrionisIntegrityException(f"Collation must be a valid MySQLCollation ({str(options_collations)}) or string.")
            else:
                self.collation = MySQLCollation[_value].value
        else:
            self.collation = self.collation.value

        # Validate prefix
        if self.prefix is not None and not isinstance(self.prefix, str):
            raise OrionisIntegrityException("Prefix must be a string.")

        # Validate prefix_indexes
        if not isinstance(self.prefix_indexes, bool):
            raise OrionisIntegrityException("prefix_indexes must be a boolean value.")

        # Validate strict
        if not isinstance(self.strict, bool):
            raise OrionisIntegrityException("strict must be a boolean value.")

        # Validate engine
        if self.engine is not None:

            # Check if engine is a string or MySQLEngine enum
            if not isinstance(self.engine, (str, MySQLEngine)):
                raise OrionisIntegrityException("Engine must be a string or MySQLEngine enum.")

            # Convert engine to MySQLEngine enum if it's a string
            options_engines = MySQLEngine._member_names_
            if isinstance(self.engine, str):
                _value = str(self.engine).upper().strip()
                if _value not in options_engines:
                    raise OrionisIntegrityException(f"Engine must be a valid MySQLEngine ({str(options_engines)}) or string.")
                else:
                    self.engine = MySQLEngine[_value].value
            elif isinstance(self.engine, MySQLEngine):
                self.engine = self.engine.value