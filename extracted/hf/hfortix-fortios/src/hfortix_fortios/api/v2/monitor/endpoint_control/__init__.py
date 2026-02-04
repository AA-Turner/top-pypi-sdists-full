"""FortiOS CMDB - EndpointControl category"""

from . import avatar
from . import ems
from . import installer
from .record_list import RecordList
from .summary import Summary

__all__ = [
    "Avatar",
    "Ems",
    "EndpointControl",
    "Installer",
    "RecordList",
    "Summary",
]


class EndpointControl:
    """EndpointControl endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """EndpointControl endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.avatar = avatar.Avatar(client)
        self.ems = ems.Ems(client)
        self.installer = installer.Installer(client)
        self.record_list = RecordList(client)
        self.summary = Summary(client)
