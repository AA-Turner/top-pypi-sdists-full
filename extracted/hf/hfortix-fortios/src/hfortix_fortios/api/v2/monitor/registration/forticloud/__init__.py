"""FortiOS CMDB - Forticloud category"""

from .device_status import DeviceStatus
from .disclaimer import Disclaimer
from .domains import Domains
from .login import Login
from .logout import Logout
from .migrate import Migrate
from .register_device import RegisterDevice

__all__ = [
    "DeviceStatus",
    "Disclaimer",
    "Domains",
    "Forticloud",
    "Login",
    "Logout",
    "Migrate",
    "RegisterDevice",
]


class Forticloud:
    """Forticloud endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Forticloud endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.device_status = DeviceStatus(client)
        self.disclaimer = Disclaimer(client)
        self.domains = Domains(client)
        self.login = Login(client)
        self.logout = Logout(client)
        self.migrate = Migrate(client)
        self.register_device = RegisterDevice(client)
