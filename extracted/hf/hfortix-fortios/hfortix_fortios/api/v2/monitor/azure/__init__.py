"""FortiOS CMDB - Azure category"""

from . import application_list

__all__ = [
    "ApplicationList",
    "Azure",
]


class Azure:
    """Azure endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Azure endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.application_list = application_list.ApplicationList(client)
