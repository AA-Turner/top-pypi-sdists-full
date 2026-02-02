"""FortiOS CMDB - SaasApplication category"""

from .details import Details

__all__ = [
    "Details",
    "SaasApplication",
]


class SaasApplication:
    """SaasApplication endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """SaasApplication endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.details = Details(client)
