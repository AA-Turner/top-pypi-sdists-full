"""FortiOS CMDB - Casb category"""

from .attribute_match import AttributeMatch
from .profile import Profile
from .saas_application import SaasApplication
from .user_activity import UserActivity

__all__ = [
    "AttributeMatch",
    "Casb",
    "Profile",
    "SaasApplication",
    "UserActivity",
]


class Casb:
    """Casb endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Casb endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.attribute_match = AttributeMatch(client)
        self.profile = Profile(client)
        self.saas_application = SaasApplication(client)
        self.user_activity = UserActivity(client)
