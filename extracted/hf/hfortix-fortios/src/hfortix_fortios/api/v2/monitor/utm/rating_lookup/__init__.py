"""FortiOS CMDB - RatingLookup category"""

from .select import Select

__all__ = [
    "RatingLookup",
    "Select",
]


class RatingLookup:
    """RatingLookup endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """RatingLookup endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.select = Select(client)
