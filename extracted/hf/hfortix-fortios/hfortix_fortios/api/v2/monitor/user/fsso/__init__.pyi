"""FortiOS CMDB - Fsso category (stub)"""

from typing import Any
from ..fsso_base import Fsso as FssoBase
from .refresh_server import RefreshServer

class Fsso(FssoBase):
    """Fsso endpoints wrapper for CMDB API."""

    refresh_server: RefreshServer

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
