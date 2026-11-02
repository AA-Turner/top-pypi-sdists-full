from pydantic import Field

from letschatty.models.company.integrations.product_sync_status import ProductSyncStatus
from letschatty.models.company.integrations.sync_status_enum import SyncStatusEnum


# Backwards-compatible alias (Shopify-specific name, generic enum)
ShopifyProductSyncStatusEnum = SyncStatusEnum


class ShopifyProductSyncStatus(ProductSyncStatus):
    """Shopify-flavored wrapper for the generic ProductSyncStatus."""

    integration_type: str = Field(
        default="shopify",
        frozen=True,
        description="Integration type for this sync status"
    )
