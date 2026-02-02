"""FortiOS CMDB - Policy category"""

from ..policy_base import Policy as PolicyBase
from .clear_counters import ClearCounters
from .reset import Reset
from .update_global_label import UpdateGlobalLabel

__all__ = [
    "ClearCounters",
    "Policy",
    "Reset",
    "UpdateGlobalLabel",
]


class Policy(PolicyBase):
    """Policy endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Policy endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.clear_counters = ClearCounters(client)
        self.reset = Reset(client)
        self.update_global_label = UpdateGlobalLabel(client)
