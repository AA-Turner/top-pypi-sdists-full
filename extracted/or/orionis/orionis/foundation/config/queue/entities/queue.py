from dataclasses import dataclass, field, fields
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.foundation.config.queue.entities.brokers import Brokers
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class Queue(BaseEntity):
    """
    Represents the configuration for a queue system.

    Attributes:
        default (str): The default queue connection to use. Must be a string.
        brokers (Brokers | dict): The configuration for the queue brokers. Can be an instance of Brokers or a dictionary.

    Methods:
        __post_init__():
            Validates and normalizes the properties after initialization.
            Ensures 'default' is a string and 'brokers' is an instance of Brokers or a dictionary.
    """

    default: str = field(
        default = "sync",
        metadata = {
            "description": "The default queue connection to use.",
            "default": "sync"
        }
    )

    brokers: Brokers | dict = field(
        default_factory = lambda: Brokers(),
        metadata={
            "description": "The default queue broker to use.",
            "default": lambda: Brokers().toDict()
        }
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Post-initialization validation for the Queue entity.

        Validates and normalizes the following properties:
        - default: Must be a string.
        - brokers: Must be a string or an instance of the Brokers class.
        """

        # Validate 'default' property
        options = [f.name for f in fields(Brokers)]
        if not isinstance(self.default, str) or self.default not in options:
            raise OrionisIntegrityException(
                f"The 'default' property must be a string and match one of the available options ({options})."
            )

        # Validate 'brokers' property
        if not isinstance(self.brokers, (Brokers, dict)):
            raise OrionisIntegrityException("brokers must be an instance of the Brokers class or a dictionary.")
        if isinstance(self.brokers, dict):
            self.brokers = Brokers(**self.brokers)