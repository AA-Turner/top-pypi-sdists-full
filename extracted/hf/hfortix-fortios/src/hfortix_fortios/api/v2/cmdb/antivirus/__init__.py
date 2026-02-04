"""FortiOS CMDB - Antivirus category"""

from .exempt_list import ExemptList
from .profile import Profile
from .quarantine import Quarantine
from .settings import Settings

__all__ = [
    "Antivirus",
    "ExemptList",
    "Profile",
    "Quarantine",
    "Settings",
]


class Antivirus:
    """Antivirus endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Antivirus endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.exempt_list = ExemptList(client)
        self.profile = Profile(client)
        self.quarantine = Quarantine(client)
        self.settings = Settings(client)
