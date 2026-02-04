"""FortiOS CMDB - ExternalResource category"""

from .dynamic import Dynamic
from .entry_list import EntryList
from .generic_address import GenericAddress
from .refresh import Refresh
from .validate_jsonpath import ValidateJsonpath

__all__ = [
    "Dynamic",
    "EntryList",
    "ExternalResource",
    "GenericAddress",
    "Refresh",
    "ValidateJsonpath",
]


class ExternalResource:
    """ExternalResource endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """ExternalResource endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.dynamic = Dynamic(client)
        self.entry_list = EntryList(client)
        self.generic_address = GenericAddress(client)
        self.refresh = Refresh(client)
        self.validate_jsonpath = ValidateJsonpath(client)
