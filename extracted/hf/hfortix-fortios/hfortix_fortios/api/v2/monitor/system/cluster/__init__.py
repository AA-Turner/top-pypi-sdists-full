"""FortiOS CMDB - Cluster category"""

from .state import State

__all__ = [
    "Cluster",
    "State",
]


class Cluster:
    """Cluster endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Cluster endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.state = State(client)
