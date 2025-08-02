from dataclasses import dataclass, field
from typing import Optional
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class Smtp(BaseEntity):
    """
    Represents the configuration for an SMTP (Simple Mail Transfer Protocol) server.
    Attributes:
        url (str): The full URL for the SMTP service.
        host (str): The hostname of the SMTP server.
        port (int): The port number used for SMTP communication.
        encryption (str): The encryption type used for secure communication (e.g., "None", "SSL", "TLS").
        username (str): The username for authentication with the SMTP server.
        password (str): The password for authentication with the SMTP server.
        timeout (Optional[int]): The connection timeout duration in seconds.
    Methods:
        __post_init__():
            Validates the integrity of the SMTP configuration attributes after initialization.
            Raises:
                OrionisIntegrityException: If any attribute does not meet the required constraints.
        toDict() -> dict:
            Converts the SMTP configuration to a dictionary representation.
            Returns:
                dict: A dictionary containing all SMTP configuration attributes.
    """

    url: str = field(
        default = "smtp.mailtrap.io",
        metadata = {
            "description": "The full URL for the SMTP service.",
            "default": "smtp.mailtrap.io"
        }
    )

    host: str = field(
        default = "smtp.mailtrap.io",
        metadata = {
            "description": "The hostname of the SMTP server.",
            "default": "smtp.mailtrap.io"
        }
    )

    port: int = field(
        default = 587,
        metadata = {
            "description": "The port number used for SMTP communication.",
            "default": 587
        }
    )

    encryption: str = field(
        default = "TLS",
        metadata = {
            "description": "The encryption type used for secure communication.",
            "default": "TLS"
        }
    )

    username: str = field(
        default = "",
        metadata = {
            "description": "The username for authentication with the SMTP server.",
            "default": ""
        }
    )

    password: str = field(
        default = "",
        metadata = {
            "description": "The password for authentication with the SMTP server.",
            "default": ""
        }
    )

    timeout: Optional[int] = field(
        default = None,
        metadata = {
            "description": "The connection timeout duration in seconds.",
            "default": None
        }
    )

    def __post_init__(self):
        """
        Validates the initialization of the mail configuration entity.

        Ensures that all required attributes are of the correct type and meet specific constraints:
        - 'url' and 'host' must be non-empty strings.
        - 'port' must be a positive integer.
        - 'encryption', 'username', and 'password' must be strings.
        - 'timeout', if provided, must be a non-negative integer or None.

        Raises:
            OrionisIntegrityException: If any attribute fails its validation check.
        """

        # Validate `url` attribute
        if not isinstance(self.url, str):
            raise OrionisIntegrityException("The 'url' attribute must be a string.")

        # Validate `host` attribute
        if not isinstance(self.host, str):
            raise OrionisIntegrityException("The 'host' attribute must be a string.")

        # Validate `port` attribute
        if not isinstance(self.port, int) or self.port < 0:
            raise OrionisIntegrityException("The 'port' attribute must be a non-negative integer.")

        # Validate `encryption` attribute
        if not isinstance(self.encryption, str):
            raise OrionisIntegrityException("The 'encryption' attribute must be a string.")

        # Validate `username` attribute
        if not isinstance(self.username, str):
            raise OrionisIntegrityException("The 'username' attribute must be a string.")

        # Validate `password` attribute
        if not isinstance(self.password, str):
            raise OrionisIntegrityException("The 'password' attribute must be a string.")

        # Validate `timeout` attribute
        if self.timeout is not None and (not isinstance(self.timeout, int) or self.timeout < 0):
            raise OrionisIntegrityException("The 'timeout' attribute must be a non-negative integer or None.")