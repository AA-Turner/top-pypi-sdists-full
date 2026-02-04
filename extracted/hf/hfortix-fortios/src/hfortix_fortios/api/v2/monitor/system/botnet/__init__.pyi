"""FortiOS CMDB - Botnet category (stub)"""

from typing import Any
from ..botnet_base import Botnet as BotnetBase
from .stat import Stat

class Botnet(BotnetBase):
    """Botnet endpoints wrapper for CMDB API."""

    stat: Stat

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
