"""FortiOS CMDB - Sdwan category"""

from .routes import Routes
from .routes6 import Routes6
from .routes_statistics import RoutesStatistics

__all__ = [
    "Routes",
    "Routes6",
    "RoutesStatistics",
    "Sdwan",
]


class Sdwan:
    """Sdwan endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Sdwan endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.routes = Routes(client)
        self.routes6 = Routes6(client)
        self.routes_statistics = RoutesStatistics(client)
