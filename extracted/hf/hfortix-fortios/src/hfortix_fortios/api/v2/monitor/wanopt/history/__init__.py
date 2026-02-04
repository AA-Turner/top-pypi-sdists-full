"""FortiOS CMDB - History category"""

from ..history_base import History as HistoryBase
from .reset import Reset

__all__ = [
    "History",
    "Reset",
]


class History(HistoryBase):
    """History endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """History endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.reset = Reset(client)
