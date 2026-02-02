"""FortiOS CMDB - Webproxy category"""

from . import pacfile

__all__ = [
    "Pacfile",
    "Webproxy",
]


class Webproxy:
    """Webproxy endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Webproxy endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.pacfile = pacfile.Pacfile(client)
