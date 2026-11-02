"""Transport-layer state machines for the cloud-sync upload paths.

The buffered (single-POST) path lives directly on :class:`SyncEngine`.
This subpackage hosts the more involved transports:

- :class:`TUSSessionManager` — TUS resumable-upload state machine atop S3 multipart.
- (future) Presigned-PUT create + finalize manager.
"""

from .presigned import (
    OwnerMismatch,
    PresignedCreateResult,
    PresignedError,
    PresignedFinalizeResult,
    PresignedManager,
    PresignedUnavailable,
    UploadNotFound as PresignedUploadNotFound,
)
from .tus import (
    TUSAppendResult,
    TUSCreateResult,
    TUSError,
    TUSFinalizeResult,
    TUSSessionManager,
    TUSSessionRow,
    UploadCompleted,
    UploadNotFound,
    OffsetMismatch,
    PartTooSmall,
    ExceedsLength,
    PatchTooLarge,
    S3Failure,
    S3NotConfigured,
)

__all__ = [
    "TUSSessionManager",
    "TUSSessionRow",
    "TUSCreateResult",
    "TUSAppendResult",
    "TUSFinalizeResult",
    "TUSError",
    "UploadCompleted",
    "UploadNotFound",
    "OffsetMismatch",
    "PartTooSmall",
    "ExceedsLength",
    "PatchTooLarge",
    "S3Failure",
    "S3NotConfigured",
    "PresignedManager",
    "PresignedCreateResult",
    "PresignedFinalizeResult",
    "PresignedError",
    "PresignedUnavailable",
    "PresignedUploadNotFound",
    "OwnerMismatch",
]
