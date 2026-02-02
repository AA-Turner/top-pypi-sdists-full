"""FortiOS CMDB - AutoConfig category"""

from .custom import Custom
from .default import Default
from .policy import Policy

__all__ = [
    "AutoConfig",
    "Custom",
    "Default",
    "Policy",
]


class AutoConfig:
    """AutoConfig endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """AutoConfig endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.custom = Custom(client)
        self.default = Default(client)
        self.policy = Policy(client)
