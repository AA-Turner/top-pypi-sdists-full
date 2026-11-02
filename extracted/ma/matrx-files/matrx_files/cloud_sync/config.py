"""Configuration for the cloud file sync layer.

CloudSyncConfig holds the S3 settings needed by the sync engine. Metadata
access uses the independently configured Matrx ORM/Postgres connection. Pass
this config to FileManager to enable automatic cloud synchronization:

    from matrx_files import FileManager
    from matrx_files.cloud_sync import CloudSyncConfig

    fm = FileManager("my_app", cloud_sync=CloudSyncConfig(
        user_id="current-user-uuid",
        s3_bucket="my-files-bucket",
    ))

When no explicit bucket is provided, the config falls back to the value in
``matrx_utils.conf.settings``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class CloudSyncConfig:
    """Immutable configuration for the cloud sync layer.

    Parameters
    ----------
    user_id:
        UUID of the currently authenticated user.  Required for all
        permission checks and file ownership.  In web apps (FastAPI),
        set this per-request via ``sync_engine.set_user(user_id)``.
    s3_bucket:
        Default S3 bucket name for file storage.  Files are stored at
        ``s3://{s3_bucket}/{user_id}/{file_path}``.
    storage_backend:
        File-byte backend. Only ``"s3"`` is supported.
    auto_sync:
        When True (default), all FileManager write/delete operations
        automatically sync to cloud + database.  Pass ``cloud_sync=False``
        per-call to override.
    version_storage_prefix:
        Prefix within the bucket for storing previous file versions.
        Defaults to ``.versions``.
    database_url:
        Direct Postgres connection string for the migration runner. It is not
        used by runtime file operations.
    """

    # Required
    user_id: str = ""
    s3_bucket: str = ""

    # Backend selection
    storage_backend: Literal["s3"] = "s3"

    # Behavior
    auto_sync: bool = True
    version_storage_prefix: str = ".versions"

    # Direct Postgres (migration runner only)
    database_url: str = ""

    #: Largest single resumable (TUS) upload this host accepts, in bytes.
    #: ``None`` means "use the package default". This is a TRANSPORT ceiling,
    #: not an entitlement: what a person may actually store is decided by the
    #: host's quota checker, per request. Hosts that accept whole data exports
    #: (a Google Takeout, a Slack workspace, a video library) set it explicitly
    #: rather than inheriting a number chosen for ordinary attachments.
    tus_max_size_bytes: int | None = None

    def __post_init__(self) -> None:
        if self.storage_backend != "s3":
            raise ValueError("CloudSyncConfig.storage_backend must be 's3'")

    def resolve_s3_bucket(self) -> str:
        """Return the S3 bucket name, falling back to settings/env."""
        if self.s3_bucket:
            return self.s3_bucket
        from matrx_utils.conf import settings
        return _safe_get(settings, "AWS_S3_DEFAULT_BUCKET")

    def is_configured(self) -> bool:
        """Return True if the minimum settings are present for cloud sync."""
        try:
            bucket = self.resolve_s3_bucket()
            return bool(bucket)
        except Exception:
            return False


def _safe_get(settings_obj: object, *names: str) -> str:
    """Try each attribute name in order, return the first non-empty value."""
    for name in names:
        try:
            value = getattr(settings_obj, name, None)
            if value:
                return str(value)
        except Exception:
            continue
    return ""
