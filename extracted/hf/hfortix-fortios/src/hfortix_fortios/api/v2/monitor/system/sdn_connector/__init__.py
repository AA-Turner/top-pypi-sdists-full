"""FortiOS CMDB - SdnConnector category"""

from .nsx_security_tags import NsxSecurityTags
from .status import Status
from .update import Update
from .validate_gcp_key import ValidateGcpKey

__all__ = [
    "NsxSecurityTags",
    "SdnConnector",
    "Status",
    "Update",
    "ValidateGcpKey",
]


class SdnConnector:
    """SdnConnector endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """SdnConnector endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.nsx_security_tags = NsxSecurityTags(client)
        self.status = Status(client)
        self.update = Update(client)
        self.validate_gcp_key = ValidateGcpKey(client)
