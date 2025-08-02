from dataclasses import dataclass, field
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.foundation.config.mail.entities.file import File
from orionis.foundation.config.mail.entities.smtp import Smtp
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class Mailers(BaseEntity):
    """
    Represents the mail transport configurations for the application.

    Attributes:
        smtp (Smtp): The SMTP configuration used for sending emails.
        file (File): The file-based mail transport configuration.

    Methods:
        __post_init__():
            Validates that the 'smtp' and 'file' attributes are instances of their respective classes.
            Raises:
                OrionisIntegrityException: If 'smtp' is not a Smtp object or 'file' is not a File object.
        toDict() -> dict:
            Serializes the Mailers instance to a dictionary.
    """

    smtp: Smtp | dict = field(
        default_factory = lambda: Smtp(),
        metadata = {
            "description": "The SMTP configuration used for sending emails.",
            "default": lambda: Smtp().toDict()
        }
    )

    file: File | dict = field(
        default_factory = lambda: File(),
        metadata = {
            "description": "The file-based mail transport configuration.",
            "default": lambda: File().toDict()
        }
    )

    def __post_init__(self):
        """
        Post-initialization method to validate attribute types.

        Ensures that the 'smtp' attribute is an instance of the Smtp class and the 'file' attribute is an instance of the File class.

        Raises:
            OrionisIntegrityException: If 'smtp' is not a Smtp object or 'file' is not a File object.
        """

        # Validate `smtp` attribute
        if not isinstance(self.smtp, (Smtp, dict)):
            raise OrionisIntegrityException("The 'smtp' attribute must be a Smtp object or a dictionary.")
        if isinstance(self.smtp, dict):
            self.smtp = Smtp(**self.smtp)

        # Validate `file` attribute
        if not isinstance(self.file, (File, dict)):
            raise OrionisIntegrityException("The 'file' attribute must be a File object or a dictionary.")
        if isinstance(self.file, dict):
            self.file = File(**self.file)