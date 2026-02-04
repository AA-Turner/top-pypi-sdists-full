"""FortiOS CMDB - Registration category"""

from . import forticare
from . import forticloud
from . import vdom

__all__ = [
    "Forticare",
    "Forticloud",
    "Registration",
    "Vdom",
]


class Registration:
    """Registration endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Registration endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.forticare = forticare.Forticare(client)
        self.forticloud = forticloud.Forticloud(client)
        self.vdom = vdom.Vdom(client)
