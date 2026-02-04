"""FortiOS CMDB - Policy category (stub)"""

from typing import Any
from ..policy_base import Policy as PolicyBase
from .clear_counters import ClearCounters
from .reset import Reset
from .update_global_label import UpdateGlobalLabel

class Policy(PolicyBase):
    """Policy endpoints wrapper for CMDB API."""

    clear_counters: ClearCounters
    reset: Reset
    update_global_label: UpdateGlobalLabel

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
