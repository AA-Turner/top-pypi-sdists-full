"""FortiOS CMDB - EthernetOam category"""

from .cfm import Cfm

__all__ = [
    "Cfm",
    "EthernetOam",
]


class EthernetOam:
    """EthernetOam endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """EthernetOam endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.cfm = Cfm(client)
