"""FortiOS CMDB - Forticloud category (stub)"""

from typing import Any
from ..forticloud_base import Forticloud as ForticloudBase
from .connection import Connection

class Forticloud(ForticloudBase):
    """Forticloud endpoints wrapper for CMDB API."""

    connection: Connection

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
