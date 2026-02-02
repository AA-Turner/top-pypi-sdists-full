"""FortiOS CMDB - Ssh category"""

from .host_key import HostKey
from .local_ca import LocalCa
from .local_key import LocalKey
from .setting import Setting

__all__ = [
    "HostKey",
    "LocalCa",
    "LocalKey",
    "Setting",
    "Ssh",
]


class Ssh:
    """Ssh endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Ssh endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.host_key = HostKey(client)
        self.local_ca = LocalCa(client)
        self.local_key = LocalKey(client)
        self.setting = Setting(client)
