"""FortiOS CMDB - RogueAp category"""

from ..rogue_ap_base import RogueAp as RogueApBase
from .clear_all import ClearAll
from .set_status import SetStatus

__all__ = [
    "ClearAll",
    "RogueAp",
    "SetStatus",
]


class RogueAp(RogueApBase):
    """RogueAp endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """RogueAp endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.clear_all = ClearAll(client)
        self.set_status = SetStatus(client)
