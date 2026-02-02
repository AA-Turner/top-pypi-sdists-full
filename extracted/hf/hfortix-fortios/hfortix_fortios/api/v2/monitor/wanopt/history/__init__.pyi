"""FortiOS CMDB - History category (stub)"""

from typing import Any
from ..history_base import History as HistoryBase
from .reset import Reset

class History(HistoryBase):
    """History endpoints wrapper for CMDB API."""

    reset: Reset

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
