"""FortiOS CMDB - Qos category"""

from .dot1p_map import Dot1pMap
from .ip_dscp_map import IpDscpMap
from .qos_policy import QosPolicy
from .queue_policy import QueuePolicy

__all__ = [
    "Dot1pMap",
    "IpDscpMap",
    "Qos",
    "QosPolicy",
    "QueuePolicy",
]


class Qos:
    """Qos endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Qos endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.dot1p_map = Dot1pMap(client)
        self.ip_dscp_map = IpDscpMap(client)
        self.qos_policy = QosPolicy(client)
        self.queue_policy = QueuePolicy(client)
