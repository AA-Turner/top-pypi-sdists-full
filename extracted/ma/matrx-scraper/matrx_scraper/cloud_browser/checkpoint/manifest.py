"""The checkpoint manifest — exact fields, canonical serialization, AAD header,
and manifest hash (S3 §2).

The manifest is the self-describing sidecar that makes database-less recovery
possible. Its canonical byte form is what ``manifest_hash`` covers and what the
GCM AAD binds. Two invariants are load-bearing and enforced here:

* canonical serialization is ``sort_keys=True``, no whitespace, UTF-8, no newline;
* the *manifest header* (every field known BEFORE encryption) is the GCM AAD, so a
  tampered ``profile_id`` / ``revision`` / ``chromium_version`` breaks the tag.

No field may carry a URL, user id, org id, email, account label, site origin,
cookie value, credential reference, Vault id, or the plaintext DEK (S3 §2.2).
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .constants import MANIFEST_VERSION

# Fields that are only known AFTER encryption / upload / verification and therefore
# are NOT part of the AAD-bound manifest header (S3 §3.1 step 4).
_POST_ENCRYPTION_FIELDS: frozenset[str] = frozenset(
    {
        "content_hash",
        "byte_count",
        "object_version_id",
        "wrapped_dek_b64",
        "auth_tag_b64",
        "verified_at",
        "verification",
        "failure",
    }
)


class ClosureProof(BaseModel):
    """Evidence the profile was closed before archiving (S3 §4)."""

    model_config = ConfigDict(extra="forbid")

    context_closed_at: str
    process_exit_confirmed_at: str
    close_wait_ms: int
    escalation: Literal["none", "sigterm", "sigkill"]
    open_fd_count: int
    singleton_files_present: list[str]
    sqlite_checked: list[str]
    sqlite_result: str
    wal_bytes_remaining: int


class VerificationBlock(BaseModel):
    """Record of what the verification gate actually checked (S3 §5.4)."""

    model_config = ConfigDict(extra="forbid")

    verified_at: str
    checks: list[str]
    verifier_image_ref: str
    duration_ms: int
    bytes_read: int


class FailureBlock(BaseModel):
    """Populated when a checkpoint fails verification or is later found corrupt (S3 §5.5)."""

    model_config = ConfigDict(extra="forbid")

    code: str
    detected_at: str
    stage: str
    detail: str
    detected_by: str


class CheckpointManifest(BaseModel):
    """The full per-checkpoint manifest document (S3 §2.2).

    ``extra='forbid'`` — an unexpected field is a bug, never silently carried.
    """

    model_config = ConfigDict(extra="forbid")

    manifest_version: int = MANIFEST_VERSION
    checkpoint_id: str
    profile_id: str
    revision: int
    parent_revision: int | None
    object_ref: str
    object_version_id: str | None
    manifest_object_ref: str
    archive_format: str
    profile_format_version: int
    content_cipher: str
    nonce_b64: str
    auth_tag_b64: str | None
    wrapped_dek_b64: str
    wrap_alg: str
    key_version: str
    kms_key_id: str | None
    encryption_context: dict[str, str]
    content_hash: str | None
    plaintext_hash: str
    byte_count: int | None
    plaintext_byte_count: int
    chromium_version: str
    chromium_major: int
    cookie_scheme: str  # D-5: observed Chromium cookie scheme (v10 / v11)
    worker_image_ref: str
    playwright_version: str
    closure_proof: ClosureProof
    created_at: str
    verified_at: str | None = None
    verification: VerificationBlock | None = None
    failure: FailureBlock | None = None
    capture_reason: Literal[
        "stop", "pre_upgrade", "scheduled", "pre_move", "pre_delete", "recovery"
    ]
    retention_expires_at: str | None = None

    # ── serialization ────────────────────────────────────────────────────
    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")

    def canonical_bytes(self) -> bytes:
        return canonical_bytes(self.to_dict())

    def manifest_hash(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()

    def header_aad(self) -> bytes:
        """The GCM additional-authenticated-data: the manifest with every
        post-encryption field removed, serialized canonically (S3 §3.1 step 4)."""
        header = {k: v for k, v in self.to_dict().items() if k not in _POST_ENCRYPTION_FIELDS}
        return canonical_bytes(header)


def canonical_bytes(manifest: dict[str, Any]) -> bytes:
    """Canonical serialization (S3 §2.1): sorted keys, no whitespace, UTF-8, no newline."""
    return json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


def manifest_hash_of(manifest: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(manifest)).hexdigest()
