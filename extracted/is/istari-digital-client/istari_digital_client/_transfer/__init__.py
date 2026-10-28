"""Stack-neutral transfer engine: streaming, parallel, resumable uploads and downloads.

This package is hand-maintained and shared by the ``legacy`` and ``sdk`` stacks. It
depends only on ``urllib3``, ``native_crypto`` and the standard library; the
stack-specific pieces (HTTP transport, presign/discover/complete calls, error
classes) are injected by the thin adapters generated into each stack's
``storage_api.py``. It must never import ``istari_digital_client.legacy`` or
``istari_digital_client.sdk``.
"""

from __future__ import annotations

from istari_digital_client._transfer.errors import (
    ContentVerificationError,
    FileChangedDuringUploadError,
    InsufficientDiskSpaceError,
    MultipartUploadRestartRequiredError,
    PartPlanError,
    SourceReadError,
    TransferCancelledError,
    TransferError,
    TransferFailed,
)
from istari_digital_client._transfer.events import EventKind, TransferEvent

__all__ = [
    "ContentVerificationError",
    "EventKind",
    "FileChangedDuringUploadError",
    "InsufficientDiskSpaceError",
    "MultipartUploadRestartRequiredError",
    "PartPlanError",
    "SourceReadError",
    "TransferCancelledError",
    "TransferError",
    "TransferEvent",
    "TransferFailed",
]
