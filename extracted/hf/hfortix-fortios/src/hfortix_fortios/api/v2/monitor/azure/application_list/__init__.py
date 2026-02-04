"""FortiOS CMDB - ApplicationList category"""

from ..application_list_base import ApplicationList as ApplicationListBase
from .refresh import Refresh

__all__ = [
    "ApplicationList",
    "Refresh",
]


class ApplicationList(ApplicationListBase):
    """ApplicationList endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """ApplicationList endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.refresh = Refresh(client)
