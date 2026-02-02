"""FortiOS CMDB - SecurityPolicy category (stub)"""

from typing import Any
from ..security_policy_base import SecurityPolicy as SecurityPolicyBase
from .clear_counters import ClearCounters
from .update_global_label import UpdateGlobalLabel

class SecurityPolicy(SecurityPolicyBase):
    """SecurityPolicy endpoints wrapper for CMDB API."""

    clear_counters: ClearCounters
    update_global_label: UpdateGlobalLabel

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
