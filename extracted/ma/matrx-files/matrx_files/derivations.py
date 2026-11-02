"""Canonical binary-file derivation vocabulary and lineage normalization."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from matrx_utils.row_access import RowAccess
from pydantic import BaseModel, ConfigDict, model_validator


class FileDerivationKind(StrEnum):
    """Kinds accepted by ``files.files.derivation_kind``."""

    MANUAL_UPLOAD = "manual_upload"
    EXTRACTED_PAGES = "extracted_pages"
    PDF_PAGE_SELECTION = "pdf_page_selection"
    CROPPED = "cropped"
    ROTATED = "rotated"
    PAGES_DELETED = "pages_deleted"
    MERGED = "merged"
    SPLIT_PART = "split_part"
    COMPRESSED = "compressed"
    RENDERED_PAGE_IMAGE = "rendered_page_image"
    REORDERED_PAGES = "reordered_pages"
    INSERTED_PAGES = "inserted_pages"
    DUPLICATED_PAGES = "duplicated_pages"
    REDACTED = "redacted"
    CLEANED = "cleaned"
    VARIANT = "variant"
    SCANNED = "scanned"
    AUDIO_EXTRACTED = "audio_extracted"
    PDF_CONVERSION = "pdf_conversion"


FILE_DERIVATION_KINDS: frozenset[str] = frozenset(
    kind.value for kind in FileDerivationKind
)


class UnknownFileDerivationKindError(ValueError):
    """Raised before storage/DB work when a derivation kind is not registered."""


class FileLineage(BaseModel):
    """Normalized lineage columns for one file write."""

    model_config = ConfigDict(frozen=True)

    parent_file_id: str | None = None
    derivation_kind: FileDerivationKind | None = None

    @model_validator(mode="after")
    def _require_kind_for_parent(self) -> FileLineage:
        if self.parent_file_id is not None and self.derivation_kind is None:
            raise ValueError(
                "parent_file_id requires derivation_kind; register the binary "
                "transformation in FileDerivationKind and pass both together."
            )
        return self


def normalize_file_derivation_kind(
    value: str | FileDerivationKind | None,
) -> FileDerivationKind | None:
    """Normalize one kind or raise with the complete registered vocabulary."""
    if value is None:
        return None
    if isinstance(value, FileDerivationKind):
        return value
    try:
        return FileDerivationKind(str(value))
    except ValueError as exc:
        allowed = ", ".join(sorted(FILE_DERIVATION_KINDS))
        raise UnknownFileDerivationKindError(
            f"Unknown file derivation_kind {value!r}. Registered kinds: {allowed}. "
            "Add new binary transformations to FileDerivationKind and the "
            "files.files check-constraint migration in the same change."
        ) from exc


def resolve_file_lineage(
    *,
    parent_file_id: str | None,
    derivation_kind: str | FileDerivationKind | None,
    metadata: dict[str, Any] | None,
) -> FileLineage:
    """Resolve explicit and legacy metadata lineage into one consistent shape."""
    metadata = metadata or {}
    metadata_parent = metadata.get("parent_file_id")
    metadata_kind = metadata.get("derivation_kind")

    if (
        parent_file_id is not None
        and metadata_parent is not None
        and str(parent_file_id) != str(metadata_parent)
    ):
        raise ValueError(
            "Conflicting parent_file_id values in write arguments and metadata: "
            f"{parent_file_id!r} != {metadata_parent!r}."
        )

    explicit_kind = normalize_file_derivation_kind(derivation_kind)
    legacy_kind = normalize_file_derivation_kind(metadata_kind)
    if explicit_kind is not None and legacy_kind is not None and explicit_kind != legacy_kind:
        raise ValueError(
            "Conflicting derivation_kind values in write arguments and metadata: "
            f"{explicit_kind.value!r} != {legacy_kind.value!r}."
        )

    resolved_parent = parent_file_id if parent_file_id is not None else metadata_parent
    return FileLineage(
        parent_file_id=str(resolved_parent) if resolved_parent is not None else None,
        derivation_kind=explicit_kind or legacy_kind,
    )


# Access-policy metadata a DERIVED file must carry forward from its master.
# These keys are what the platform access policy keys on: `system_artifact` +
# `artifact_domain` route the file to contextual (container-derived) access
# resolution, and `web_site_id`/`crawl_session_id`/`capture_id` are the lanes
# the DB policy (`files.has_access_for`, migration 0298) uses to convey site
# access onto everything derived from a crawl. A variant that drops them
# silently falls back to owner-only access and 403s every legitimate org
# member (the 2026-07-29 vision-variant defect, FOUND_DEFECTS E-ii).
# `system_immutable` is deliberately NOT inherited — a derived variant is
# re-renderable output, not canonical evidence.
DERIVED_POLICY_METADATA_KEYS: tuple[str, ...] = (
    "system_artifact",
    "artifact_domain",
    "web_site_id",
    "crawl_session_id",
    "capture_id",
)

EXTERNAL_OBJECT_CUSTODY_METADATA_KEY = "external_object_custody"


# The full set of metadata keys owned by server policy/custody machinery.
# Most are read by the platform ACCESS POLICY; ``external_object_custody`` is
# checksummed provider-ingest evidence whose mutation would invalidate the
# audit trail. They are all protected by the same client-write choke point.
# These are
# authorization-bearing: `system_artifact`+`artifact_domain` reclassify a file
# into contextual (container-derived) access resolution, and `web_site_id` /
# `crawl_session_id` decide WHICH container conveys access. Only SERVER code
# (the crawler writer, the variants engine) may stamp them — a client that can
# write them at editor level can widen a file's audience to a site's viewers
# or lock its own owner out (viewer ceiling), bypassing every admin-gated
# sharing channel. Every CLIENT-facing metadata write path must call
# `assert_no_client_policy_metadata` before persisting.
SYSTEM_POLICY_METADATA_KEYS: frozenset[str] = frozenset(
    {
        *DERIVED_POLICY_METADATA_KEYS,
        EXTERNAL_OBJECT_CUSTODY_METADATA_KEY,
        "system_immutable",
    }
)


class ClientPolicyMetadataError(PermissionError):
    """A client-supplied metadata write tried to set/change a policy key."""


def assert_no_client_policy_metadata(
    metadata: dict[str, Any] | None,
    *,
    existing: dict[str, Any] | None = None,
    context: str = "metadata write",
) -> None:
    """Reject client-supplied metadata that sets or CHANGES a policy key.

    Echoing back a key with its current value is tolerated (clients often
    round-trip whole metadata blobs); introducing or altering one is refused
    loudly — those keys are server-stamped authorization inputs.
    """
    if not metadata:
        return
    existing = existing or {}
    offending = [
        key
        for key in SYSTEM_POLICY_METADATA_KEYS
        if key in metadata and (key not in existing or metadata[key] != existing[key])
    ]
    if offending:
        raise ClientPolicyMetadataError(
            f"{context}: metadata keys {sorted(offending)} are server-stamped policy or "
            "custody inputs and cannot be set or changed by a client. A client write here "
            "would corrupt access decisions or durable evidence."
        )


def inherit_derived_file_policy(
    master_record: dict[str, Any],
    own_metadata: dict[str, Any],
) -> tuple[RowAccess, dict[str, Any]]:
    """The (row access, metadata) for a file DERIVED from ``master_record``.

    A derived file inherits its master's access context — ``published_to_web`` and
    ``shown_to``, the
    contextual-access policy keys above, and the master's ``organization_id``
    (via the metadata org channel ``managed_write_async`` reads; without it
    the row falls back to the writer's PERSONAL org and lands in the wrong
    tenant — the exact wrong-org bug on the first vision variant). The
    variant's own keys in ``own_metadata`` always win on conflict.

    Every variant write site MUST go through this — constructing row access
    or metadata for a derived file by hand recreates the defect class.
    """
    master_meta = master_record.get("metadata") or {}
    metadata = dict(own_metadata)
    for key in DERIVED_POLICY_METADATA_KEYS:
        if key in master_meta and key not in metadata:
            metadata[key] = master_meta[key]
    org = master_record.get("organization_id")
    if org and not metadata.get("organization_id"):
        metadata["organization_id"] = str(org)
    access = RowAccess(
        published_to_web=bool(master_record.get("published_to_web")),
        shown_to=master_record.get("shown_to"),
    )
    return access, metadata


def normalize_derivation_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Normalize a DB payload's derivation kind without mutating the caller."""
    value = payload.get("derivation_kind")
    if value is None:
        return payload
    normalized = normalize_file_derivation_kind(value)
    assert normalized is not None
    if type(value) is str and value == normalized.value:
        return payload
    return {**payload, "derivation_kind": normalized.value}


__all__ = [
    "ClientPolicyMetadataError",
    "DERIVED_POLICY_METADATA_KEYS",
    "EXTERNAL_OBJECT_CUSTODY_METADATA_KEY",
    "FILE_DERIVATION_KINDS",
    "SYSTEM_POLICY_METADATA_KEYS",
    "FileDerivationKind",
    "assert_no_client_policy_metadata",
    "inherit_derived_file_policy",
    "FileLineage",
    "UnknownFileDerivationKindError",
    "normalize_derivation_payload",
    "normalize_file_derivation_kind",
    "resolve_file_lineage",
]
