"""FortiOS CMDB - SecurityPolicy category"""

from ..security_policy_base import SecurityPolicy as SecurityPolicyBase
from .clear_counters import ClearCounters
from .update_global_label import UpdateGlobalLabel

__all__ = [
    "ClearCounters",
    "SecurityPolicy",
    "UpdateGlobalLabel",
]


class SecurityPolicy(SecurityPolicyBase):
    """SecurityPolicy endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """SecurityPolicy endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.clear_counters = ClearCounters(client)
        self.update_global_label = UpdateGlobalLabel(client)
