"""FortiOS CMDB - Fortiguard category"""

from .answers import Answers
from .redirect_portal import RedirectPortal
from .service_communication_stats import ServiceCommunicationStats

__all__ = [
    "Answers",
    "Fortiguard",
    "RedirectPortal",
    "ServiceCommunicationStats",
]


class Fortiguard:
    """Fortiguard endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Fortiguard endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.answers = Answers(client)
        self.redirect_portal = RedirectPortal(client)
        self.service_communication_stats = ServiceCommunicationStats(client)
