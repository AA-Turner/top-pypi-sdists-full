from dataclasses import dataclass, field
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class Public(BaseEntity):
    """
    Represents a local filesystem configuration.

    Attributes
    ----------
    path : str
        The absolute or relative path where public files are stored.
    """
    path: str = field(
        default = "storage/app/public",
        metadata = {
            "description": "The absolute or relative path where public files are stored.",
            "default": "storage/app/public"
        }
    )

    url: str = field(
        default = "static",
        metadata = {
            "description": "The URL where the public files can be accessed.",
            "default": "static"
        }
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Post-initialization method to ensure the 'path' attribute is a non-empty string.

        Raises:
            OrionisIntegrityException: If any of the attributes are not of the expected type or are empty.
        """

        # Validate the 'path' attribute
        if not isinstance(self.path, str):
            raise OrionisIntegrityException("The 'path' attribute must be a string.")

        # Validate the 'url' attribute
        if not isinstance(self.url, str):
            raise OrionisIntegrityException("The 'url' attribute must be a string.")
        if not self.path.strip() or not self.url.strip():
            raise OrionisIntegrityException("The 'path' and 'url' attributes cannot be empty.")