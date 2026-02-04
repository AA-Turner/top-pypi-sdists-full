"""FortiOS CMDB - WebUi category"""

from . import custom_language
from . import language

__all__ = [
    "CustomLanguage",
    "Language",
    "WebUi",
]


class WebUi:
    """WebUi endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """WebUi endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.custom_language = custom_language.CustomLanguage(client)
        self.language = language.Language(client)
