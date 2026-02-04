"""FortiOS CMDB - WebProxy category"""

from .debug_url import DebugUrl
from .explicit import Explicit
from .fast_fallback import FastFallback
from .forward_server import ForwardServer
from .forward_server_group import ForwardServerGroup
from .global_ import Global
from .isolator_server import IsolatorServer
from .profile import Profile
from .url_match import UrlMatch
from .wisp import Wisp

__all__ = [
    "DebugUrl",
    "Explicit",
    "FastFallback",
    "ForwardServer",
    "ForwardServerGroup",
    "Global",
    "IsolatorServer",
    "Profile",
    "UrlMatch",
    "WebProxy",
    "Wisp",
]


class WebProxy:
    """WebProxy endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """WebProxy endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.debug_url = DebugUrl(client)
        self.explicit = Explicit(client)
        self.fast_fallback = FastFallback(client)
        self.forward_server = ForwardServer(client)
        self.forward_server_group = ForwardServerGroup(client)
        self.global_ = Global(client)
        self.isolator_server = IsolatorServer(client)
        self.profile = Profile(client)
        self.url_match = UrlMatch(client)
        self.wisp = Wisp(client)
