"""FortiOS CMDB - EndpointControl category"""

from .fctems import Fctems
from .fctems_override import FctemsOverride
from .settings import Settings

__all__ = [
    "EndpointControl",
    "Fctems",
    "FctemsOverride",
    "Settings",
]


class EndpointControl:
    """EndpointControl endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """EndpointControl endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.fctems = Fctems(client)
        self.fctems_override = FctemsOverride(client)
        self.settings = Settings(client)
