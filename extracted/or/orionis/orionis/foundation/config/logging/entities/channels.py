from dataclasses import dataclass, field
from orionis.support.entities.base import BaseEntity
from orionis.foundation.config.logging.entities.monthly import Monthly
from orionis.foundation.config.logging.entities.chunked import Chunked
from orionis.foundation.config.logging.entities.daily import Daily
from orionis.foundation.config.logging.entities.hourly import Hourly
from orionis.foundation.config.logging.entities.stack import Stack
from orionis.foundation.config.logging.entities.weekly import Weekly
from orionis.foundation.exceptions import OrionisIntegrityException

@dataclass(unsafe_hash=True, kw_only=True)
class Channels(BaseEntity):
    """
    Represents the different logging channels available.
    """

    stack: Stack | dict = field(
        default_factory = lambda: Stack(),
        metadata = {
            "description": "Configuration for stack log channel.",
            "default": lambda: Stack().toDict()
        }
    )

    hourly: Hourly | dict = field(
        default_factory = lambda: Hourly(),
        metadata = {
            "description": "Configuration for hourly log rotation.",
            "default": lambda: Hourly().toDict()
        }
    )

    daily: Daily | dict = field(
        default_factory = lambda: Daily(),
        metadata = {
            "description": "Configuration for daily log rotation.",
            "default": lambda: Daily().toDict()
        }
    )

    weekly: Weekly | dict = field(
        default_factory = lambda: Weekly(),
        metadata = {
            "description": "Configuration for weekly log rotation.",
            "default": lambda: Weekly().toDict()
        }
    )

    monthly: Monthly | dict= field(
        default_factory = lambda: Monthly(),
        metadata = {
            "description": "Configuration for monthly log rotation.",
            "default": lambda: Monthly().toDict()
        }
    )

    chunked: Chunked | dict = field(
        default_factory = lambda: Chunked(),
        metadata = {
            "description": "Configuration for chunked log file storage.",
            "default": lambda: Chunked().toDict()
        }
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Post-initialization method to validate the types of log rotation properties.
        Ensures that the following instance attributes are of the correct types:
        - `stack` must be an instance of `Stack`
        - `hourly` must be an instance of `Hourly`
        - `daily` must be an instance of `Daily`
        - `weekly` must be an instance of `Weekly`
        - `monthly` must be an instance of `Monthly`
        - `chunked` must be an instance of `Chunked`
        Raises:
            OrionisIntegrityException: If any of the properties are not instances of their expected classes.
        """

        # Validate `stack` attribute
        if not isinstance(self.stack, (Stack, dict)):
            raise OrionisIntegrityException(
                "The 'stack' property must be an instance of Stack or a dictionary."
            )
        if isinstance(self.stack, dict):
            self.stack = Stack(**self.stack)

        # Validate `hourly` attribute
        if not isinstance(self.hourly, (Hourly, dict)):
            raise OrionisIntegrityException(
                "The 'hourly' property must be an instance of Hourly or a dictionary."
            )
        if isinstance(self.hourly, dict):
            self.hourly = Hourly(**self.hourly)

        # Validate `daily` attribute
        if not isinstance(self.daily, (Daily, dict)):
            raise OrionisIntegrityException(
                "The 'daily' property must be an instance of Daily or a dictionary."
            )
        if isinstance(self.daily, dict):
            self.daily = Daily(**self.daily)

        # Validate `weekly` attribute
        if not isinstance(self.weekly, (Weekly, dict)):
            raise OrionisIntegrityException(
                "The 'weekly' property must be an instance of Weekly or a dictionary."
            )
        if isinstance(self.weekly, dict):
            self.weekly = Weekly(**self.weekly)

        # Validate `monthly` attribute
        if not isinstance(self.monthly, (Monthly, dict)):
            raise OrionisIntegrityException(
                "The 'monthly' property must be an instance of Monthly or a dictionary."
            )
        if isinstance(self.monthly, dict):
            self.monthly = Monthly(**self.monthly)

        # Validate `chunked` attribute
        if not isinstance(self.chunked, (Chunked, dict)):
            raise OrionisIntegrityException(
                "The 'chunked' property must be an instance of Chunked or a dictionary."
            )
        if isinstance(self.chunked, dict):
            self.chunked = Chunked(**self.chunked)
