"""FortiOS CMDB - ExtensionController category"""

from .dataplan import Dataplan
from .extender import Extender
from .extender_profile import ExtenderProfile
from .extender_vap import ExtenderVap
from .fortigate import Fortigate
from .fortigate_profile import FortigateProfile

__all__ = [
    "Dataplan",
    "Extender",
    "ExtenderProfile",
    "ExtenderVap",
    "ExtensionController",
    "Fortigate",
    "FortigateProfile",
]


class ExtensionController:
    """ExtensionController endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """ExtensionController endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.dataplan = Dataplan(client)
        self.extender = Extender(client)
        self.extender_profile = ExtenderProfile(client)
        self.extender_vap = ExtenderVap(client)
        self.fortigate = Fortigate(client)
        self.fortigate_profile = FortigateProfile(client)
