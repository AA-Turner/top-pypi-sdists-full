"""FortiOS CMDB - CustomLanguage category"""

from .create import Create
from .download import Download
from .update import Update

__all__ = [
    "Create",
    "CustomLanguage",
    "Download",
    "Update",
]


class CustomLanguage:
    """CustomLanguage endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """CustomLanguage endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.create = Create(client)
        self.download = Download(client)
        self.update = Update(client)
