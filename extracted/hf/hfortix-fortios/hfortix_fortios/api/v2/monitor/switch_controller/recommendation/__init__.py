"""FortiOS CMDB - Recommendation category"""

from .pse_config import PseConfig

__all__ = [
    "PseConfig",
    "Recommendation",
]


class Recommendation:
    """Recommendation endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Recommendation endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.pse_config = PseConfig(client)
