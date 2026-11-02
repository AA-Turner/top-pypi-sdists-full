from pydantic import Field

from letschatty.models.company.integrations.product_sync_status import ProductSyncStatus
from letschatty.models.company.integrations.sync_status_enum import SyncStatusEnum


# Backwards-compatible alias (Tienda Nube-specific name, generic enum)
TiendaNubeProductSyncStatusEnum = SyncStatusEnum


class TiendaNubeProductSyncStatus(ProductSyncStatus):
    """Tienda Nube-flavored wrapper for the generic ProductSyncStatus."""

    integration_type: str = Field(
        default="tiendanube",
        frozen=True,
        description="Integration type for this sync status"
    )
