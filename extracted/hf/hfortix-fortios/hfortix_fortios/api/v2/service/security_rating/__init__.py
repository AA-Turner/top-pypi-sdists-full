"""FortiOS CMDB - SecurityRating category"""

from .recommendations import Recommendations
from .report import Report

__all__ = [
    "Recommendations",
    "Report",
    "SecurityRating",
]


class SecurityRating:
    """SecurityRating endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """SecurityRating endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.recommendations = Recommendations(client)
        self.report = Report(client)
