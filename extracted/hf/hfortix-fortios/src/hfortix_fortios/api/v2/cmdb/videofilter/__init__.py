"""FortiOS CMDB - Videofilter category"""

from .keyword import Keyword
from .profile import Profile
from .youtube_key import YoutubeKey

__all__ = [
    "Keyword",
    "Profile",
    "Videofilter",
    "YoutubeKey",
]


class Videofilter:
    """Videofilter endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Videofilter endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.keyword = Keyword(client)
        self.profile = Profile(client)
        self.youtube_key = YoutubeKey(client)
