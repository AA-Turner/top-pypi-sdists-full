"""FortiOS CMDB - Fortitoken category"""

from ..fortitoken_base import Fortitoken as FortitokenBase
from .activate import Activate
from .import_mobile import ImportMobile
from .import_seed import ImportSeed
from .import_trial import ImportTrial
from .provision import Provision
from .refresh import Refresh
from .send_activation import SendActivation

__all__ = [
    "Activate",
    "Fortitoken",
    "ImportMobile",
    "ImportSeed",
    "ImportTrial",
    "Provision",
    "Refresh",
    "SendActivation",
]


class Fortitoken(FortitokenBase):
    """Fortitoken endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Fortitoken endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.activate = Activate(client)
        self.import_mobile = ImportMobile(client)
        self.import_seed = ImportSeed(client)
        self.import_trial = ImportTrial(client)
        self.provision = Provision(client)
        self.refresh = Refresh(client)
        self.send_activation = SendActivation(client)
