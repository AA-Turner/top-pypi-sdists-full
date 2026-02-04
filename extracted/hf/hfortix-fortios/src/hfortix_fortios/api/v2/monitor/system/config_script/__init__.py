"""FortiOS CMDB - ConfigScript category"""

from ..config_script_base import ConfigScript as ConfigScriptBase
from .delete import Delete
from .run import Run
from .upload import Upload

__all__ = [
    "ConfigScript",
    "Delete",
    "Run",
    "Upload",
]


class ConfigScript(ConfigScriptBase):
    """ConfigScript endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """ConfigScript endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.delete = Delete(client)
        self.run = Run(client)
        self.upload = Upload(client)
