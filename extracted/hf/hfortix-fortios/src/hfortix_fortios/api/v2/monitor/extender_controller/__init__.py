"""FortiOS CMDB - ExtenderController category"""

from . import extender

__all__ = [
    "Extender",
    "ExtenderController",
]


class ExtenderController:
    """ExtenderController endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """ExtenderController endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.extender = extender.Extender(client)
