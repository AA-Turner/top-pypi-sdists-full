from dataclasses import dataclass, field
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class Local(BaseEntity):
    """
    Represents a local filesystem configuration.

    Attributes
    ----------
    path : str
        The absolute or relative path where local files are stored.
    """
    path: str = field(
        default = "storage/app/private",
        metadata = {
            "description": "The absolute or relative path where local files are stored.",
            "default": "storage/app/private",
        }
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Post-initialization method to ensure the 'path' attribute is a non-empty string.

        - Raises:
            ValueError: If the 'path' is empty.
        """

        # Validate the 'path' attribute
        if not isinstance(self.path, str):
            raise OrionisIntegrityException("The 'path' attribute must be a string.")
        if not self.path.strip():
            raise OrionisIntegrityException("The 'path' attribute cannot be empty.")