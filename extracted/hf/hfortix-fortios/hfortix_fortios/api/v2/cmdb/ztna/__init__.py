"""FortiOS CMDB - Ztna category"""

from .reverse_connector import ReverseConnector
from .traffic_forward_proxy import TrafficForwardProxy
from .web_portal import WebPortal
from .web_portal_bookmark import WebPortalBookmark
from .web_proxy import WebProxy

__all__ = [
    "ReverseConnector",
    "TrafficForwardProxy",
    "WebPortal",
    "WebPortalBookmark",
    "WebProxy",
    "Ztna",
]


class Ztna:
    """Ztna endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Ztna endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.reverse_connector = ReverseConnector(client)
        self.traffic_forward_proxy = TrafficForwardProxy(client)
        self.web_portal = WebPortal(client)
        self.web_portal_bookmark = WebPortalBookmark(client)
        self.web_proxy = WebProxy(client)
