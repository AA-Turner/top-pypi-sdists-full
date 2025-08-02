from dataclasses import dataclass, field
from typing import Optional
from orionis.foundation.config.database.enums import (
    OracleEncoding,
    OracleNencoding
)
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.services.environment.env import Env
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class Oracle(BaseEntity):
    """
    Data class to represent Oracle database configuration using oracledb.

    Attributes
    ----------
    driver : str
        The database driver being used, typically 'oracle'.
    username : str
        Username for the database connection.
    password : str
        Password for the database connection.
    host : str
        Hostname or IP address of the Oracle server.
    port : int
        Port number for the Oracle listener (default 1521).
    service_name : Optional[str]
        Service name for connection using the SERVICE_NAME method.
    sid : Optional[str]
        SID for connection using the SID method.
    dsn : Optional[str]
        Full DSN string, used if service_name/sid are not specified.
    tns_name : Optional[str]
        TNS alias name defined in tnsnames.ora.
    encoding : str
        Character encoding for the connection.
    """

    driver: str = field(
        default = "oracle",
        metadata = {
            "description": "The database driver being used, typically 'oracle'.",
            "default": "oracle"
        }
    )

    username: str = field(
        default_factory = lambda: Env.get("DB_USERNAME", "sys"),
        metadata = {
            "description": "Oracle DB username.",
            "default": "sys"
        }
    )

    password: str = field(
        default_factory = lambda: Env.get("DB_PASSWORD", ""),
        metadata = {
            "description": "Oracle DB password.",
            "default": ""
        }
    )

    host: str = field(
        default_factory = lambda: Env.get("DB_HOST", "localhost"),
        metadata = {
            "description": "Oracle DB host address.",
            "default": "localhost"
        }
    )

    port: int = field(
        default_factory = lambda: Env.get("DB_PORT", 1521),
        metadata = {
            "description": "Oracle DB listener port.",
            "default": 1521
        }
    )

    service_name: Optional[str] = field(
        default_factory = lambda: Env.get("DB_SERVICE_NAME", "ORCL"),
        metadata = {
            "description": "Service name for Oracle DB.",
            "default": "ORCL"
        }
    )

    sid: Optional[str] = field(
        default_factory = lambda: Env.get("DB_SID", None),
        metadata = {
            "description": "SID for Oracle DB.",
            "default": None
        }
    )

    dsn: Optional[str] = field(
        default_factory = lambda: Env.get("DB_DSN", None),
        metadata = {
            "description": "DSN string (overrides host/port/service/sid).",
            "default": None
        }
    )

    tns_name: Optional[str] = field(
        default_factory = lambda: Env.get("DB_TNS", None),
        metadata = {
            "description": "TNS alias defined in tnsnames.ora file.",
            "default": None
        }
    )

    encoding: str | OracleEncoding = field(
        default_factory = lambda: Env.get("DB_ENCODING", OracleEncoding.AL32UTF8.value),
        metadata = {
            "description": "Database charset (CHAR/VARCHAR2)",
            "default": OracleEncoding.AL32UTF8.value
        }
    )

    nencoding: str | OracleNencoding = field(
        default_factory = lambda: Env.get("DB_NENCODING", OracleNencoding.AL32UTF8.value),
        metadata = {
            "description": "Database charset (NCHAR/NVARCHAR2)",
            "default": OracleNencoding.AL32UTF8.value
        }
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Post-initialization validation for Oracle database connection entity.
        This method performs strict validation on the configuration fields required to establish
        an Oracle database connection. It ensures that all necessary parameters are present and
        correctly formatted, raising an `OrionisIntegrityException` if any validation fails.

        Validation rules:
        - `driver` must be the string 'oracle'.
        - `username` and `password` must be non-empty strings.
        - `dsn` and `tns_name`, if provided, must be non-empty strings or None.
        - If neither `dsn` nor `tns_name` is provided:
            - `host` must be a non-empty string.
            - `port` must be an integer between 1 and 65535.
            - At least one of `service_name` or `sid` must be provided as a non-empty string.
            - If provided, `service_name` and `sid` must be non-empty strings or None.
        - `encoding` must be a non-empty string or an instance of `OracleEncoding`.
        - `nencoding` must be a non-empty string.

        Raises:
            OrionisIntegrityException: If any configuration parameter is invalid.
        """

        # Validate driver
        if not isinstance(self.driver, str) or self.driver.strip().lower() != "oracle":
            raise OrionisIntegrityException("Invalid 'driver': must be the string 'oracle'.")

        # Validate username
        if not isinstance(self.username, str) or not self.username.strip():
            raise OrionisIntegrityException("Invalid 'username': must be a non-empty string.")

        # Validate password
        if not isinstance(self.password, str):
            raise OrionisIntegrityException("Invalid 'password': must be a string.")

        # Validate dsn
        if self.dsn is not None and (not isinstance(self.dsn, str) or not self.dsn.strip()):
            raise OrionisIntegrityException("Invalid 'dsn': must be a non-empty string or None.")

        # Validate tns_name
        if self.tns_name is not None and (not isinstance(self.tns_name, str) or not self.tns_name.strip()):
            raise OrionisIntegrityException("Invalid 'tns_name': must be a non-empty string or None.")

        # If not using DSN or TNS, validate host/port/service_name/sid
        if not self.dsn and not self.tns_name:

            # Validate host
            if not isinstance(self.host, str) or not self.host.strip():
                raise OrionisIntegrityException("Invalid 'host': must be a non-empty string.")

            # Validate port
            if not isinstance(self.port, int) or self.port <= 0 or self.port > 65535:
                raise OrionisIntegrityException("Invalid 'port': must be an integer between 1 and 65535.")

            # Validate service_name and sid
            if (self.service_name is None or not str(self.service_name).strip()) and (self.sid is None or not str(self.sid).strip()):
                raise OrionisIntegrityException(
                    "You must provide at least one of: 'service_name', 'sid', 'dsn', or 'tns_name'."
                )

            # Validate service_name and sid
            if self.service_name is not None and (not isinstance(self.service_name, str) or not self.service_name.strip()):
                raise OrionisIntegrityException("Invalid 'service_name': must be a non-empty string or None.")

            # Validate sid
            if self.sid is not None and (not isinstance(self.sid, str) or not self.sid.strip()):
                raise OrionisIntegrityException("Invalid 'sid': must be a non-empty string or None.")

        # Validate encoding
        options_encoding = OracleEncoding._member_names_
        if isinstance(self.encoding, str):
            _value = self.encoding.upper().strip()
            if _value not in options_encoding:
                raise OrionisIntegrityException(
                    f"The 'encoding' attribute must be a valid option {str(OracleEncoding._member_names_)}"
                )
            else:
                self.encoding = OracleEncoding[_value].value
        elif isinstance(self.encoding, OracleEncoding):
            self.encoding = self.encoding.value
        else:
            raise OrionisIntegrityException("Invalid 'encoding': must be a string or OracleEncoding.")

        # Validate nencoding
        options_nencoding = OracleNencoding._member_names_
        if isinstance(self.nencoding, str):
            _value = self.nencoding.upper().strip()
            if _value not in options_nencoding:
                raise OrionisIntegrityException(
                    f"The 'nencoding' attribute must be a valid option {str(OracleNencoding._member_names_)}"
                )
            else:
                self.nencoding = OracleNencoding[_value].value
        elif isinstance(self.nencoding, OracleNencoding):
            self.nencoding = self.nencoding.value
        else:
            raise OrionisIntegrityException("Invalid 'nencoding': must be a string or OracleNencoding.")