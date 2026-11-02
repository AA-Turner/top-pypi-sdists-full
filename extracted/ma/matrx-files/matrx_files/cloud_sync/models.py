"""Pydantic models for the cloud file sync layer.

These models represent the database entities (cld_files, cld_folders,
cld_file_versions, etc.) and the results returned by sync operations.
They are used for validation, serialization, and as typed return values
throughout the cloud_sync package.

Note: the Python class names retain the ``Cloud*`` prefix for backwards
compatibility with importers (``CloudFile``, ``CloudFolder``, …).
Only the DB table names use the ``cld_`` prefix.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from matrx_utils import new_id


def _uuid() -> str:
    return new_id()


# ------------------------------------------------------------------
# Core entities
# ------------------------------------------------------------------


class CloudFile(BaseModel):
    """A tracked file in the cloud sync system.

    Mirrors the full cld_files DB schema as of migration 010 (the
    UnifiedMediaBlock contract rollout). Hosts that don't use every
    field (organization scoping, lineage, thumbnails) leave them None.
    """

    id: str = Field(default_factory=_uuid)
    owner_id: str
    organization_id: str | None = None
    file_path: str
    storage_uri: str
    file_name: str
    mime_type: str | None = None
    size_bytes: int | None = None
    checksum: str | None = None
    published_to_web: bool = False
    shown_to: str | None = None
    current_version: int = 1
    parent_folder_id: str | None = None
    # Visual / temporal dimensions promoted to first-class columns in
    # migration 010 — populated for image/video/audio masters.
    width: int | None = None
    height: int | None = None
    duration_ms: int | None = None
    # Binary lineage (migration 004). Set when this file was derived
    # from another (extracted pages, crop, rotation, variant render, …).
    parent_file_id: str | None = None
    derivation_kind: str | None = None
    derivation_metadata: dict[str, Any] = Field(default_factory=dict)
    # Phase 1b dropped the legacy ``thumbnail_storage_uri`` /
    # ``thumbnail_url`` columns (migration 011). Thumbnails now live as
    # variant cld_files rows — query via
    # ``matrx_files.cloud_sync.thumbnail_resolver.resolve_thumbnail_url_async``.
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class CloudFolder(BaseModel):
    """A virtual folder in the cloud sync file tree."""

    id: str = Field(default_factory=_uuid)
    owner_id: str
    folder_path: str
    folder_name: str
    parent_id: str | None = None
    published_to_web: bool = False
    shown_to: str | None = None
    # True when the folder lives under a system-managed root (generations/ or
    # system-files/). Stamped automatically by the DB trigger
    # ``trg_cld_folders_set_is_system`` (migration 015) from ``folder_path`` —
    # never set this by hand; it is derived, not authored. System folders are
    # hidden from the user file tree and protected from deletion.
    is_system: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class CloudFileVersion(BaseModel):
    """A single version of a tracked file."""

    id: str = Field(default_factory=_uuid)
    file_id: str
    version_number: int
    storage_uri: str
    size_bytes: int | None = None
    checksum: str | None = None
    created_by: str | None = None
    created_at: datetime | None = None
    change_summary: str | None = None


class CloudFilePermission(BaseModel):
    """An ACL entry granting access to a file or folder."""

    id: str = Field(default_factory=_uuid)
    resource_id: str
    resource_type: Literal["file", "folder"]
    grantee_id: str
    grantee_type: Literal["user", "group"] = "user"
    permission_level: Literal["read", "write", "admin"]
    granted_by: str | None = None
    granted_at: datetime | None = None
    expires_at: datetime | None = None


class CloudShareLink(BaseModel):
    """A shareable link to a file or folder (canonical ``platform.share_links`` row)."""

    id: str = Field(default_factory=_uuid)
    resource_id: str
    resource_type: Literal["file", "folder"]
    token: str = Field(default_factory=_uuid)
    permission_level: Literal["viewer", "editor"] = "viewer"
    created_by: str | None = None
    label: str | None = None
    created_at: datetime | None = None
    expires_at: datetime | None = None
    last_used_at: datetime | None = None
    max_uses: int | None = None
    use_count: int = 0
    is_active: bool = True


class CloudUserGroup(BaseModel):
    """A named group of users for group-based ACL."""

    id: str = Field(default_factory=_uuid)
    name: str
    owner_id: str
    created_at: datetime | None = None


class CloudGroupMember(BaseModel):
    """Membership record linking a user to a group."""

    id: str = Field(default_factory=_uuid)
    group_id: str
    user_id: str
    role: Literal["member", "admin"] = "member"
    added_at: datetime | None = None
    added_by: str | None = None


# ------------------------------------------------------------------
# Operation results
# ------------------------------------------------------------------


class SyncResult(BaseModel):
    """Returned from managed write/update operations.

    DURABLE URL contract (single source of truth — SyncEngine builds every
    URL, callers must NEVER sign storage_uri; nothing returns a signed URL):

    - ``url``           canonical FE-visible URL the FE renders directly
                        (inline-correct for browsers). CDN URL when public
                        + CDN configured; the authenticated durable
                        ``/files/{id}/download?inline=1`` route otherwise.
    - ``cdn_url``       permanent CDN URL when published to the web and the
                        CDN is configured; ``None`` otherwise.
    - ``download_url``  durable ``/files/{id}/download`` route
                        (attachment disposition).
    - ``published_to_web`` / ``shown_to`` echo the row's access words after
                        the write so callers don't need to re-query.
    - ``origin``        always ``"matrx"`` — this is our own write result.
                        Aligned with the UnifiedMediaBlock contract so
                        helpers that consume SyncResult can stamp the
                        origin field without a literal.

    NOTE: ``storage_uri`` (the native ``s3://…`` location) stays on this
    INTERNAL write-result — callers use it to read bytes / mint URLs. It
    MUST NOT be copied onto any client-facing shape (see FileRef / the
    audit_api_types FORBIDDEN_WIRE_FIELDS guard). The old ``file_uri``
    "FE-friendly alias" was removed — nothing read it, and it only ever
    leaked the storage URI onto the wire.
    """

    file_id: str
    storage_uri: str
    # The logical path of the ROW this write actually landed on. Normally the
    # path the caller asked for; on an implicit dedup alias (content already
    # held by another root of this owner+organization) it is the CANONICAL
    # row's path, which is not the caller's. Doors echo THIS, never the
    # requested path: a response that repeats a path the server discarded is
    # how a client comes to believe a placement exists when it does not
    # (measured 2026-09-17: 287 coding-session artifacts filed under another
    # session because the door echoed the request).
    file_path: str | None = None
    version_number: int
    size_bytes: int | None = None
    checksum: str | None = None
    is_new: bool = False
    published_to_web: bool = False
    shown_to: str | None = None
    url: str | None = None
    cdn_url: str | None = None
    download_url: str | None = None
    share_token: str | None = None
    share_url: str | None = None
    origin: Literal["matrx"] = "matrx"
    parent_file_id: str | None = None
    derivation_kind: str | None = None


class FileTreeEntry(BaseModel):
    """A single entry in the user's file tree (returned by list operations)."""

    id: str
    owner_id: str
    file_path: str
    file_name: str
    mime_type: str | None = None
    size_bytes: int | None = None
    published_to_web: bool = False
    shown_to: str | None = None
    current_version: int
    parent_folder_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime | None = None
    updated_at: datetime | None = None
    effective_permission: str | None = None


class PermissionInfo(BaseModel):
    """Summary of a permission grant (for listing permissions on a resource)."""

    id: str
    grantee_id: str
    grantee_type: str
    permission_level: str
    granted_by: str | None = None
    granted_at: datetime | None = None
    expires_at: datetime | None = None
