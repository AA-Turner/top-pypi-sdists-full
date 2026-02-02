"""FortiOS CMDB - RogueAp category (stub)"""

from typing import Any
from ..rogue_ap_base import RogueAp as RogueApBase
from .clear_all import ClearAll
from .set_status import SetStatus

class RogueAp(RogueApBase):
    """RogueAp endpoints wrapper for CMDB API."""

    clear_all: ClearAll
    set_status: SetStatus

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
