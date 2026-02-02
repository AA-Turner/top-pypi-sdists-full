"""FortiOS CMDB - ApplicationList category (stub)"""

from typing import Any
from ..application_list_base import ApplicationList as ApplicationListBase
from .refresh import Refresh

class ApplicationList(ApplicationListBase):
    """ApplicationList endpoints wrapper for CMDB API."""

    refresh: Refresh

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
