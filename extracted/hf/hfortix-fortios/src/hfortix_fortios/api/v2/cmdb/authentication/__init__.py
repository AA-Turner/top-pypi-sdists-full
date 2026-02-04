"""FortiOS CMDB - Authentication category"""

from .rule import Rule
from .scheme import Scheme
from .setting import Setting

__all__ = [
    "Authentication",
    "Rule",
    "Scheme",
    "Setting",
]


class Authentication:
    """Authentication endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Authentication endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.rule = Rule(client)
        self.scheme = Scheme(client)
        self.setting = Setting(client)
