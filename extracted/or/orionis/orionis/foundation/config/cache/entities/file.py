from dataclasses import dataclass, field
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class File(BaseEntity):
    """
    Represents the configuration entity for a file-based cache store.

    Attributes:
        path (str): The file system path where cache data will be stored. By default, this is set to
            'storage/framework/cache/data' using a relative path resolver.

    Methods:
        __post_init__():
            Validates the 'path' attribute after dataclass initialization. Raises an
            OrionisIntegrityException if 'path' is empty or not a string, ensuring correct cache setup.
    """

    path: str = field(
        default = 'storage/framework/cache/data',
        metadata = {
            "description": "The configuration for available cache stores. Defaults to a file store at the specified path.",
            "default": "storage/framework/cache/data"
        },
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Validates the 'path' attribute after dataclass initialization.

        Raises:
            OrionisIntegrityException: If 'path' is empty or not a string, indicating a misconfiguration
            in the file cache setup.
        """

        # Validate the 'path' attribute to ensure it is not empty and is a string
        if not self.path:
            raise OrionisIntegrityException("File cache configuration error: 'path' cannot be empty. Please provide a valid file path.")
        if not isinstance(self.path, str):
            raise OrionisIntegrityException(f"File cache configuration error: 'path' must be a string, got {type(self.path).__name__}.")