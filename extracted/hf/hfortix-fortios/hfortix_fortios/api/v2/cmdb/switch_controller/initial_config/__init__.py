"""FortiOS CMDB - InitialConfig category"""

from .template import Template
from .vlans import Vlans

__all__ = [
    "InitialConfig",
    "Template",
    "Vlans",
]


class InitialConfig:
    """InitialConfig endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """InitialConfig endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.template = Template(client)
        self.vlans = Vlans(client)
