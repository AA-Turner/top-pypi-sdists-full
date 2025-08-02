from dataclasses import dataclass, field
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.foundation.config.filesystems.entitites.aws import S3
from orionis.foundation.config.filesystems.entitites.public import Public
from orionis.foundation.config.filesystems.entitites.local import Local
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class Disks(BaseEntity):
    """
    Represents the configuration for different filesystem disks.
    Attributes:
        local (Local): The disk configuration for local file storage.
        public (Public): The disk configuration for public file storage.
    Methods:
        __post_init__():
            Ensures the 'path' attribute is a non-empty Path object and of the correct type.
        toDict() -> dict:
            Converts the Disks object into a dictionary representation.
    """

    local : Local | dict = field(
        default_factory = lambda: Local(),
        metadata={
            "description": "The absolute or relative path where local files are stored.",
            "default": lambda: Local().toDict()
        }
    )

    public : Public | dict = field(
        default_factory = lambda: Public(),
        metadata={
            "description": "The absolute or relative path where public files are stored.",
            "default": lambda: Public().toDict()
        }
    )

    aws : S3 | dict = field(
        default_factory = lambda: S3(),
        metadata={
            "description": "The configuration for AWS S3 storage.",
            "default": lambda: S3().toDict()
        }
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Post-initialization method to ensure the 'path' attribute is a non-empty Path object.
        - Converts 'path' to a Path instance if it is not already.
        - Raises:
            ValueError: If the 'path' is empty after conversion.
        """

        # Validate the 'local' attribute
        if not isinstance(self.local, (Local, dict)):
            raise OrionisIntegrityException("The 'local' attribute must be a Local object or a dictionary.")
        if isinstance(self.local, dict):
            self.local = Local(**self.local)

        # Validate the 'public' attribute
        if not isinstance(self.public, (Public, dict)):
            raise OrionisIntegrityException("The 'public' attribute must be a Public object or a dictionary.")
        if isinstance(self.public, dict):
            self.public = Public(**self.public)

        # Validate the 'aws' attribute
        if not isinstance(self.aws, (S3, dict)):
            raise OrionisIntegrityException("The 'aws' attribute must be an S3 object or a dictionary.")
        if isinstance(self.aws, dict):
            self.aws = S3(**self.aws)