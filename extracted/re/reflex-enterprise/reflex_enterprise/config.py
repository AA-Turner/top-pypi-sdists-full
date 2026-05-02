"""Enterprise utilities for Reflex CLI."""

from dataclasses import dataclass
from typing import ClassVar

from reflex.config import Config


@dataclass(kw_only=True, init=False)
class ConfigEnterprise(Config):
    """Enterprise configuration class."""

    use_single_port: bool | None = None

    _prefixes: ClassVar[list[str]] = ["REFLEX_", "REFLEX_ENTERPRISE_"]

    def __init__(self, **kwargs):
        """Initialize the configuration."""
        # This is a hack due to how upstream Config/BaseConfig interact
        if "use_single_port" in kwargs:
            self.use_single_port = kwargs.pop("use_single_port")
        super().__init__(**kwargs)


Config = ConfigEnterprise
