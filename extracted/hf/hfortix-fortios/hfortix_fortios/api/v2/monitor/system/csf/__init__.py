"""FortiOS CMDB - Csf category"""

from ..csf_base import Csf as CsfBase
from .pending_authorizations import PendingAuthorizations
from .register_appliance import RegisterAppliance

__all__ = [
    "Csf",
    "PendingAuthorizations",
    "RegisterAppliance",
]


class Csf(CsfBase):
    """Csf endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Csf endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.pending_authorizations = PendingAuthorizations(client)
        self.register_appliance = RegisterAppliance(client)
