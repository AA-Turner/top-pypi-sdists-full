"""Data operations for DealCloud SDK."""

from intapp_rest_client.models import ErrorHandling

from .dealcloud_data import DealCloudData
from .models import (
    BatchResult,
    DeltaSyncResult,
    ModifiedEntry,
    ReferenceCache,
    ReferenceFormat,
)

__all__ = [
    "DealCloudData",
    "ErrorHandling",  # Re-exported from intapp-rest-client for backward compatibility
    "BatchResult",
    "ModifiedEntry",
    "DeltaSyncResult",
    "ReferenceFormat",
    "ReferenceCache",
]


