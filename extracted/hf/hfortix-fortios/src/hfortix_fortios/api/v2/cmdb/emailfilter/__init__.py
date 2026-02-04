"""FortiOS CMDB - Emailfilter category"""

from .block_allow_list import BlockAllowList
from .bword import Bword
from .dnsbl import Dnsbl
from .fortishield import Fortishield
from .iptrust import Iptrust
from .mheader import Mheader
from .options import Options
from .profile import Profile

__all__ = [
    "BlockAllowList",
    "Bword",
    "Dnsbl",
    "Emailfilter",
    "Fortishield",
    "Iptrust",
    "Mheader",
    "Options",
    "Profile",
]


class Emailfilter:
    """Emailfilter endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Emailfilter endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.block_allow_list = BlockAllowList(client)
        self.bword = Bword(client)
        self.dnsbl = Dnsbl(client)
        self.fortishield = Fortishield(client)
        self.iptrust = Iptrust(client)
        self.mheader = Mheader(client)
        self.options = Options(client)
        self.profile = Profile(client)
