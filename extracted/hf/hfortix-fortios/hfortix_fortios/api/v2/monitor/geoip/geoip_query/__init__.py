"""FortiOS CMDB - GeoipQuery category"""

from .select import Select

__all__ = [
    "GeoipQuery",
    "Select",
]


class GeoipQuery:
    """GeoipQuery endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """GeoipQuery endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.select = Select(client)
