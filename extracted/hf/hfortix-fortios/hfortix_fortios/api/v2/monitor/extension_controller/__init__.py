"""FortiOS CMDB - ExtensionController category"""

from .fortigate import Fortigate
from .lan_extension_vdom_status import LanExtensionVdomStatus

__all__ = [
    "ExtensionController",
    "Fortigate",
    "LanExtensionVdomStatus",
]


class ExtensionController:
    """ExtensionController endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """ExtensionController endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.fortigate = Fortigate(client)
        self.lan_extension_vdom_status = LanExtensionVdomStatus(client)
