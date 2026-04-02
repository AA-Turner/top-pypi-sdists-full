"""
ConnectorErrorMetadata and build_metadata.
"""

from __future__ import annotations

from connector_sdk_types.generated.models.connector_error_metadata import ConnectorErrorMetadata

from .classification import (
    CODE_CATEGORY_MAP,
    CODE_FAULT_MAP,
    ConnectorErrorCategory,
    ConnectorErrorFault,
)
from .codes import (
    REFRESHABLE_CODES,
    RETRYABLE_CODES,
    THROTTLE_AND_RETRY_CODES,
    ConnectorErrorCode,
)

__all__ = ["ConnectorErrorMetadata", "build_metadata"]


def build_metadata(
    code: ConnectorErrorCode,
    hint: str | None = None,
    retryable: bool | None = None,
    throttled: bool | None = None,
    refreshable: bool | None = None,
) -> ConnectorErrorMetadata:
    """
    Build ConnectorErrorMetadata for a resolved ConnectorErrorCode.
    """
    return ConnectorErrorMetadata(
        fault=CODE_FAULT_MAP.get(code, ConnectorErrorFault.UNKNOWN),
        category=CODE_CATEGORY_MAP.get(code, ConnectorErrorCategory.INTERNAL),
        hint=hint,
        retryable=retryable
        if retryable is not None
        else code in RETRYABLE_CODES or code in THROTTLE_AND_RETRY_CODES,
        throttled=throttled if throttled is not None else code in THROTTLE_AND_RETRY_CODES,
        refreshable=refreshable if refreshable is not None else code in REFRESHABLE_CODES,
    )
