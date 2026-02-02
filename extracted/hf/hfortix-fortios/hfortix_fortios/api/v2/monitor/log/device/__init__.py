"""FortiOS CMDB - Device category"""

from .state import State

__all__ = [
    "Device",
    "State",
]


class Device:
    """Device endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Device endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.state = State(client)
