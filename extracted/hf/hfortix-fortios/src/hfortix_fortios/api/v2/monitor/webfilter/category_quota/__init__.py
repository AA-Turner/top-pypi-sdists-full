"""FortiOS CMDB - CategoryQuota category"""

from ..category_quota_base import CategoryQuota as CategoryQuotaBase
from .reset import Reset

__all__ = [
    "CategoryQuota",
    "Reset",
]


class CategoryQuota(CategoryQuotaBase):
    """CategoryQuota endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """CategoryQuota endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.reset = Reset(client)
