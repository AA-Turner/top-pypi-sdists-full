"""FortiOS CMDB - Videofilter category"""

from .fortiguard_categories import FortiguardCategories

__all__ = [
    "FortiguardCategories",
    "Videofilter",
]


class Videofilter:
    """Videofilter endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Videofilter endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.fortiguard_categories = FortiguardCategories(client)
