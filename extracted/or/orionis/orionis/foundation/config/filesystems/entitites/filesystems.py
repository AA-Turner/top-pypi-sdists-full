from dataclasses import dataclass, field, fields
from orionis.foundation.config.filesystems.entitites.disks import Disks
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class Filesystems(BaseEntity):
    """
    Represents the filesystems configuration.

    Attributes
    ----------
    default : str
        The default filesystem disk to use.
    disks : Disks
        A collection of available filesystem disks.
    """

    default: str = field(
        default = "local",
        metadata = {
            "description": "The default filesystem disk to use.",
            "default": "local",
        }
    )

    disks: Disks | dict = field(
        default_factory = lambda: Disks(),
        metadata={
            "description": "A collection of available filesystem disks.",
            "default": lambda: Disks().toDict()
        }
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Validates the types of the attributes after initialization.
        """

        # Validate the 'default' property
        options = [f.name for f in fields(Disks)]
        if not isinstance(self.default, str) or self.default not in options:
            raise OrionisIntegrityException(
                f"The 'default' property must be a string and match one of the available options ({options})."
            )

        # Validate the 'disks' property
        if not isinstance(self.disks, (Disks, dict)):
            raise OrionisIntegrityException(
                "The 'disks' property must be an instance of Disks or a dictionary."
            )
        if isinstance(self.disks, dict):
            self.disks = Disks(**self.disks)