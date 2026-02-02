"""FortiOS CMDB - CategoryQuota category (stub)"""

from typing import Any
from ..category_quota_base import CategoryQuota as CategoryQuotaBase
from .reset import Reset

class CategoryQuota(CategoryQuotaBase):
    """CategoryQuota endpoints wrapper for CMDB API."""

    reset: Reset

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
