"""FortiOS CMDB - ConfigRevision category"""

from ..config_revision_base import ConfigRevision as ConfigRevisionBase
from .delete import Delete
from .file import File
from .info import Info
from .save import Save
from .update_comments import UpdateComments

__all__ = [
    "ConfigRevision",
    "Delete",
    "File",
    "Info",
    "Save",
    "UpdateComments",
]


class ConfigRevision(ConfigRevisionBase):
    """ConfigRevision endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """ConfigRevision endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.delete = Delete(client)
        self.file = File(client)
        self.info = Info(client)
        self.save = Save(client)
        self.update_comments = UpdateComments(client)
