from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Optional

from pydantic import Field

from letschatty.models.company.integrations.sync_status_enum import SyncStatusEnum
from letschatty.models.base_models import CompanyAssetModel


class ProductSyncStatus(CompanyAssetModel):
    """Generic product sync status for any e-commerce integration."""

    COLLECTION: ClassVar[str] = "product_sync_statuses"

    integration_type: str = Field(
        description="Integration type (shopify, tiendanube, etc.)"
    )
    status: SyncStatusEnum = Field(description="Current sync status")

    products_created: int = Field(default=0)
    products_updated: int = Field(default=0)

    name: str = Field(default="")

    finished_at: Optional[datetime] = Field(default=None)

