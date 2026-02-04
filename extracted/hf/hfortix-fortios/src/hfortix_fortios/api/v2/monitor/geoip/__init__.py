"""FortiOS CMDB - Geoip category"""

from . import geoip_query

__all__ = [
    "Geoip",
    "GeoipQuery",
]


class Geoip:
    """Geoip endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Geoip endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.geoip_query = geoip_query.GeoipQuery(client)
