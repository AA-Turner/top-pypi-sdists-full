"""FortiOS CMDB - Query category"""

from .abort import Abort

__all__ = [
    "Abort",
    "Query",
]


class Query:
    """Query endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Query endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.abort = Abort(client)
