"""FortiOS CMDB - Ips category"""

from . import session
from .anomaly import Anomaly
from .hold_signatures import HoldSignatures
from .metadata import Metadata
from .rate_based import RateBased

__all__ = [
    "Anomaly",
    "HoldSignatures",
    "Ips",
    "Metadata",
    "RateBased",
    "Session",
]


class Ips:
    """Ips endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Ips endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.session = session.Session(client)
        self.anomaly = Anomaly(client)
        self.hold_signatures = HoldSignatures(client)
        self.metadata = Metadata(client)
        self.rate_based = RateBased(client)
