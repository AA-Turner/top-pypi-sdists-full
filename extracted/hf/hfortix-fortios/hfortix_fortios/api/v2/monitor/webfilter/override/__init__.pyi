"""FortiOS CMDB - Override category (stub)"""

from typing import Any
from ..override_base import Override as OverrideBase
from .delete import Delete

class Override(OverrideBase):
    """Override endpoints wrapper for CMDB API."""

    delete: Delete

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
