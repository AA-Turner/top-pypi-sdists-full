"""FortiOS CMDB - Client category (stub)"""

from typing import Any
from ..client_base import Client as ClientBase
from .disassociate import Disassociate

class Client(ClientBase):
    """Client endpoints wrapper for CMDB API."""

    disassociate: Disassociate

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
