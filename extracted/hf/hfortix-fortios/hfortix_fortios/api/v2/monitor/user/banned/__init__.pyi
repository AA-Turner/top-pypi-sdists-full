"""FortiOS CMDB - Banned category (stub)"""

from typing import Any
from ..banned_base import Banned as BannedBase
from .add_users import AddUsers
from .check import Check
from .clear_all import ClearAll
from .clear_users import ClearUsers

class Banned(BannedBase):
    """Banned endpoints wrapper for CMDB API."""

    add_users: AddUsers
    check: Check
    clear_all: ClearAll
    clear_users: ClearUsers

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
