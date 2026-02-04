"""FortiOS CMDB - User category"""

from . import banned
from . import device
from . import firewall
from . import fortitoken
from . import fortitoken_cloud
from . import fsso
from . import guest
from . import info
from . import local
from . import password_policy_conform
from . import proxy
from . import query
from . import radius
from . import scim
from . import tacacs_plus
from .collected_email import CollectedEmail

__all__ = [
    "Banned",
    "CollectedEmail",
    "Device",
    "Firewall",
    "Fortitoken",
    "FortitokenCloud",
    "Fsso",
    "Guest",
    "Info",
    "Local",
    "PasswordPolicyConform",
    "Proxy",
    "Query",
    "Radius",
    "Scim",
    "TacacsPlus",
    "User",
]


class User:
    """User endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """User endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.banned = banned.Banned(client)
        self.device = device.Device(client)
        self.firewall = firewall.Firewall(client)
        self.fortitoken = fortitoken.Fortitoken(client)
        self.fortitoken_cloud = fortitoken_cloud.FortitokenCloud(client)
        self.fsso = fsso.Fsso(client)
        self.guest = guest.Guest(client)
        self.info = info.Info(client)
        self.local = local.Local(client)
        self.password_policy_conform = password_policy_conform.PasswordPolicyConform(client)
        self.proxy = proxy.Proxy(client)
        self.query = query.Query(client)
        self.radius = radius.Radius(client)
        self.scim = scim.Scim(client)
        self.tacacs_plus = tacacs_plus.TacacsPlus(client)
        self.collected_email = CollectedEmail(client)
