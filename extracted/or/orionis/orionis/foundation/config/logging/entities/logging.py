from dataclasses import dataclass, field, fields
from orionis.support.entities.base import BaseEntity
from orionis.foundation.config.logging.entities.channels import Channels
from orionis.foundation.exceptions import OrionisIntegrityException

@dataclass(unsafe_hash=True, kw_only=True)
class Logging(BaseEntity):
    """
    Represents the logging system configuration.

    Attributes
    ----------
    default : str
        The default logging channel to use.
    channels : Channels
        A collection of available logging channels.
    """
    default: str = field(
        default = "stack",
        metadata = {
            "description": "The default logging channel to use.",
            "default": "stack"
        }
    )

    channels: Channels | dict = field(
        default_factory = lambda: Channels(),
        metadata = {
            "description": "A collection of available logging channels.",
            "default": lambda: Channels().toDict()
        }
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Validates the logging configuration after dataclass initialization by ensuring
        the default channel and channels configuration are properly formatted and valid.
        Parameters
        ----------
        None
        Raises
        ------
        OrionisIntegrityException
            If the default channel is not a string or doesn't match available channel options.
        OrionisIntegrityException
            If the channels configuration is malformed or cannot be converted to a Channels instance.
        OrionisIntegrityException
            If the channels property is not a Channels instance or a dictionary.
        Notes
        -----
        This method performs the following validations:
        - Ensures 'default' is a string matching available channel options from Channels fields
        """

        options = [field.name for field in fields(Channels)]
        if not isinstance(self.default, str) or self.default not in options:
            raise OrionisIntegrityException(
                f"The 'default' property must be a string and match one of the available options ({options})."
            )

        if not isinstance(self.channels, (Channels, dict)):
            raise OrionisIntegrityException(
                "The 'channels' property must be an instance of Channels or a dictionary."
            )
        if isinstance(self.channels, dict):
            self.channels = Channels(**self.channels)