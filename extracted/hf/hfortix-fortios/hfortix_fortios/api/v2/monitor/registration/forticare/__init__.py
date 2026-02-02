"""FortiOS CMDB - Forticare category"""

from .add_license import AddLicense
from .check_connectivity import CheckConnectivity
from .create import Create
from .deregister_device import DeregisterDevice
from .login import Login
from .transfer import Transfer

__all__ = [
    "AddLicense",
    "CheckConnectivity",
    "Create",
    "DeregisterDevice",
    "Forticare",
    "Login",
    "Transfer",
]


class Forticare:
    """Forticare endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Forticare endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.add_license = AddLicense(client)
        self.check_connectivity = CheckConnectivity(client)
        self.create = Create(client)
        self.deregister_device = DeregisterDevice(client)
        self.login = Login(client)
        self.transfer = Transfer(client)
