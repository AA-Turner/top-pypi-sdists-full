"""FortiOS CMDB - Guest category"""

from .email import Email
from .sms import Sms

__all__ = [
    "Email",
    "Guest",
    "Sms",
]


class Guest:
    """Guest endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Guest endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.email = Email(client)
        self.sms = Sms(client)
