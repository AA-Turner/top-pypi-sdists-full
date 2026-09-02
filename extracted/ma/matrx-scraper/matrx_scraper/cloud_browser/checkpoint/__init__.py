"""WS-3 checkpoint / crypto engine — the standalone library that captures, encrypts,
verifies, restores, prunes, and cryptographically deletes a Chromium profile
checkpoint per the frozen S3 contract.

Pure library: it runs against a scratch profile directory, an injected object store,
and an injected key-wrap provider (local KMS stand-in or real AWS KMS) — no worker,
no Browser Manager, no ``browser.*`` schema, no AWS account. See the contract at
``common-docs/projects/persistent-cloud-browser/contracts/S3-checkpoint-format.md``.
"""

from __future__ import annotations

from . import constants
from .engine import (
    CaptureRequest,
    CheckpointEngine,
    DeletionOutcome,
    RestoreOutcome,
    WorkerContext,
)
from .errors import (
    CaptureError,
    CheckpointError,
    CheckpointKmsNotConfiguredError,
    ClosureError,
    DeletionError,
    LocalDevProviderRefusedError,
    NoRestorableRevisionError,
    RestoreError,
    VerificationError,
    FAILURE_CODES,
)
from .key_wrap import (
    KeyWrapProvider,
    KmsKeyWrapProvider,
    LocalDevKeyWrapProvider,
    configure_checkpoint_key_wrapping,
    get_key_wrap_provider,
    reset_checkpoint_key_wrapping_for_tests,
)
from .manifest import (
    CheckpointManifest,
    ClosureProof,
    FailureBlock,
    VerificationBlock,
    canonical_bytes,
)
from .object_store import InMemoryObjectStore, ObjectRef, ObjectStore, PutResult

__all__ = [
    "constants",
    # engine
    "CheckpointEngine",
    "CaptureRequest",
    "WorkerContext",
    "RestoreOutcome",
    "DeletionOutcome",
    # manifest
    "CheckpointManifest",
    "ClosureProof",
    "VerificationBlock",
    "FailureBlock",
    "canonical_bytes",
    # key wrap
    "KeyWrapProvider",
    "KmsKeyWrapProvider",
    "LocalDevKeyWrapProvider",
    "configure_checkpoint_key_wrapping",
    "get_key_wrap_provider",
    "reset_checkpoint_key_wrapping_for_tests",
    # object store
    "ObjectStore",
    "InMemoryObjectStore",
    "ObjectRef",
    "PutResult",
    # errors
    "CheckpointError",
    "ClosureError",
    "CaptureError",
    "VerificationError",
    "RestoreError",
    "NoRestorableRevisionError",
    "DeletionError",
    "CheckpointKmsNotConfiguredError",
    "LocalDevProviderRefusedError",
    "FAILURE_CODES",
]
