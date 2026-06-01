# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Registry rebuild operations.

This module provides the core logic for rebuilding the entire connector registry
by reading all connector metadata from a source GCS bucket and writing it to
a configurable output target (local directory, GCS bucket, or S3 bucket)
using fsspec for unified filesystem access.
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import fsspec
import gcsfs
import s3fs

from airbyte_ops_mcp.registry._constants import (
    METADATA_FOLDER,
    PROD_METADATA_SERVICE_BUCKET_NAME,
)
from airbyte_ops_mcp.registry._gcs_helpers import get_gcs_credentials_token

logger = logging.getLogger(__name__)

OutputMode = Literal["local", "gcs", "s3"]

_GCLOUD_CP_MAX_WORKERS = 80
"""Maximum number of parallel `gcloud storage cp` subprocesses."""


@dataclass
class RebuildResult:
    """Result of a registry rebuild operation."""

    source_bucket: str
    output_mode: OutputMode
    output_root: str
    connectors_processed: int = 0
    blobs_copied: int = 0
    blobs_skipped: int = 0
    errors: list[str] = field(default_factory=list)
    dry_run: bool = False

    @property
    def status(self) -> str:
        """Return the status of the rebuild operation."""
        if self.dry_run:
            return "dry-run"
        if self.errors:
            return "completed-with-errors"
        return "success"

    def summary(self) -> str:
        """Return a human-readable summary."""
        return (
            f"[{self.status}] Rebuilt {self.connectors_processed} connectors, "
            f"{self.blobs_copied} blobs copied, {self.blobs_skipped} skipped, "
            f"{len(self.errors)} errors. Output: {self.output_root}"
        )


def _validate_not_prod_bucket(bucket_name: str) -> None:
    """Raise ValueError if the bucket is the prod bucket."""
    if bucket_name == PROD_METADATA_SERVICE_BUCKET_NAME:
        raise ValueError(
            f"Writing to the production bucket '{PROD_METADATA_SERVICE_BUCKET_NAME}' "
            "is categorically disallowed by create-mirror."
        )


def _make_source_fs() -> tuple[gcsfs.GCSFileSystem, dict[str, str] | None]:
    """Create a gcsfs filesystem for reading from GCS.

    Returns:
        Tuple of (filesystem, token) for reuse on the output side if needed.
    """
    token = get_gcs_credentials_token()
    fs = gcsfs.GCSFileSystem(token=token)
    return fs, token


def _make_output_fs(
    output_mode: OutputMode,
    output_root: str,
    gcs_bucket: str | None = None,
    s3_bucket: str | None = None,
    gcs_token: dict[str, str] | None = None,
) -> tuple[fsspec.AbstractFileSystem, str]:
    """Create an fsspec filesystem for writing to the output target.

    Args:
        output_mode: "local", "gcs", or "s3".
        output_root: The resolved output root path (local dir or prefix).
        gcs_bucket: Target GCS bucket (required for gcs mode).
        s3_bucket: Target S3 bucket (required for s3 mode).
        gcs_token: GCS credentials token dict (reused from source if available).

    Returns:
        Tuple of (filesystem, base_path) for the output target.
    """
    if output_mode == "local":
        fs = fsspec.filesystem("file")
        return fs, output_root

    if output_mode == "gcs":
        if not gcs_bucket:
            raise ValueError("gcs_bucket is required for GCS output mode.")
        _validate_not_prod_bucket(gcs_bucket)
        token = gcs_token or get_gcs_credentials_token()
        fs = gcsfs.GCSFileSystem(token=token)
        prefix = f"{output_root.rstrip('/')}/" if output_root else ""
        return fs, f"{gcs_bucket}/{prefix}"

    # s3 mode
    if not s3_bucket:
        raise ValueError("s3_bucket is required for S3 output mode.")
    fs = s3fs.S3FileSystem()
    prefix = f"{output_root.rstrip('/')}/" if output_root else ""
    return fs, f"{s3_bucket}/{prefix}"


def _resolve_local_output_root(output_path_root: str | None) -> str:
    """Resolve the local output root path.

    If no path is provided, creates a new temp directory.
    """
    if output_path_root:
        path = Path(output_path_root)
        path.mkdir(parents=True, exist_ok=True)
        return str(path)

    return tempfile.mkdtemp(prefix="registry-rebuild-")


def rebuild_registry(
    source_bucket: str,
    output_mode: OutputMode,
    output_path_root: str | None = None,
    gcs_bucket: str | None = None,
    s3_bucket: str | None = None,
    dry_run: bool = False,
    connector_name: list[str] | None = None,
) -> RebuildResult:
    """Rebuild the entire registry from a source GCS bucket to an output target.

    Reads all connector metadata blobs from the source GCS bucket and copies
    them to the output target using fsspec for unified filesystem access.

    The output targets are:
    - local: Write to a local directory tree.
    - gcs: Copy to a GCS bucket (must not be the prod bucket).
    - s3: Copy to an S3 bucket.

    Args:
        source_bucket: The GCS bucket to read from (typically prod).
        output_mode: Where to write: "local", "gcs", or "s3".
        output_path_root: Root path/prefix for output. For local mode, if None
            creates a temp directory. For GCS/S3, prepended to all blob paths.
        gcs_bucket: Target GCS bucket name (required if output_mode="gcs").
        s3_bucket: Target S3 bucket name (required if output_mode="s3").
        dry_run: If True, report what would be done without writing.
        connector_name: If provided, only rebuild these connector names
            (e.g. ["source-faker", "destination-bigquery"]). If None, rebuilds all.

    Returns:
        RebuildResult with details of the operation.

    Raises:
        ValueError: If target is the prod bucket, or required bucket arg is missing.
    """
    if output_mode == "gcs" and gcs_bucket:
        _validate_not_prod_bucket(gcs_bucket)

    # Resolve output root for local mode
    effective_output_root = output_path_root or ""
    if output_mode == "local":
        effective_output_root = _resolve_local_output_root(output_path_root)

    result = RebuildResult(
        source_bucket=source_bucket,
        output_mode=output_mode,
        output_root=effective_output_root,
        dry_run=dry_run,
    )

    # Create source filesystem (always GCS)
    source_fs, gcs_token = _make_source_fs()
    source_base = f"{source_bucket}/{METADATA_FOLDER}"

    # List files under metadata/ in the source bucket
    if connector_name:
        _log_progress(
            "Listing blobs for %d connectors under gs://%s/...",
            len(connector_name),
            source_base,
        )
        source_paths: list[str] = []
        for name in connector_name:
            connector_prefix = f"{source_base}/airbyte/{name}"
            found = source_fs.find(connector_prefix)
            source_paths.extend(found)
            _log_progress("  %s: %d blobs", name, len(found))
    else:
        _log_progress("Listing all blobs under gs://%s/...", source_base)
        source_paths = source_fs.find(source_base)

    if not source_paths:
        _log_progress("No blobs found under gs://%s/", source_base)
        return result

    total_blobs = len(source_paths)
    _log_progress("Found %d blobs to process", total_blobs)

    # Create output filesystem
    output_fs, output_base = _make_output_fs(
        output_mode=output_mode,
        output_root=effective_output_root,
        gcs_bucket=gcs_bucket,
        s3_bucket=s3_bucket,
        gcs_token=gcs_token,
    )

    # Collect connector names and compute relative paths for all blobs.
    bucket_prefix = f"{source_bucket}/"
    blob_relative_paths: list[str] = []
    connector_names: set[str] = set()

    for source_path in source_paths:
        relative_path = source_path
        if source_path.startswith(bucket_prefix):
            relative_path = source_path[len(bucket_prefix) :]
        blob_relative_paths.append(relative_path)

        parts = relative_path.split("/")
        if len(parts) >= 3:
            connector_names.add(parts[2])

    if dry_run:
        result.blobs_copied = total_blobs
        result.connectors_processed = len(connector_names)
        _log_progress(
            "[DRY RUN] Would copy %d blobs (%d connectors)",
            total_blobs,
            len(connector_names),
        )
        _log_progress(result.summary())
        return result

    # Use GCS-native server-side copy for GCS→GCS mirrors.
    if output_mode == "gcs" and gcs_bucket:
        result = _gcs_native_copy(
            source_bucket=source_bucket,
            dest_bucket_name=gcs_bucket,
            dest_prefix=effective_output_root,
            blob_relative_paths=blob_relative_paths,
            connector_names=connector_names,
            gcs_token=gcs_token,
            result=result,
            connector_name_filter=connector_name,
        )
        return result

    # Fallback: fsspec-based copy for local and S3 output modes.
    result = _fsspec_copy(
        source_fs=source_fs,
        source_paths=source_paths,
        output_fs=output_fs,
        output_base=output_base,
        output_mode=output_mode,
        source_bucket=source_bucket,
        blob_relative_paths=blob_relative_paths,
        connector_names=connector_names,
        result=result,
    )
    return result


def _gcs_native_copy(
    source_bucket: str,
    dest_bucket_name: str,
    dest_prefix: str,
    blob_relative_paths: list[str],
    connector_names: set[str],
    gcs_token: dict[str, str] | None,
    result: RebuildResult,
    connector_name_filter: list[str] | None = None,
) -> RebuildResult:
    """Copy blobs using GCS-native server-side copy (no data through Python).

    Delegates to `gcloud storage cp` which uses built-in parallelism
    and server-side copy (no data transits through this machine) for
    same-provider GCS-to-GCS transfers.  This is significantly faster
    than issuing individual `copy_blob` API calls from the Python SDK.
    """
    token = gcs_token or get_gcs_credentials_token()
    total_blobs = len(blob_relative_paths)
    prefix_part = f"{dest_prefix.rstrip('/')}/" if dest_prefix else ""

    # Build (source, dest) pairs.
    # Per-connector pairs target metadata/airbyte/{name}/ on both sides.
    # The whole-registry pair targets the parent prefix because --recursive
    # preserves the source directory name (avoids double-nesting metadata/).
    pairs = (
        [
            (
                f"gs://{source_bucket}/{METADATA_FOLDER}/airbyte/{name}/",
                f"gs://{dest_bucket_name}/{prefix_part}{METADATA_FOLDER}/airbyte/{name}/",
            )
            for name in connector_name_filter
        ]
        if connector_name_filter
        else [
            (
                f"gs://{source_bucket}/{METADATA_FOLDER}/",
                f"gs://{dest_bucket_name}/{prefix_part}",
            )
        ]
    )

    _log_progress(
        "Starting gcloud storage copy: %d blobs -> gs://%s/%s",
        total_blobs,
        dest_bucket_name,
        prefix_part,
    )

    def _run_one_copy(
        pair: tuple[str, str],
        env: dict[str, str],
    ) -> str | None:
        """Run a single gcloud storage cp and return an error string or None."""
        src, dst = pair
        _log_progress("  Copying %s -> %s ...", src, dst)
        cmd = [
            "gcloud",
            "storage",
            "cp",
            "--recursive",
            "--continue-on-error",
            src,
            dst,
        ]
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
            stdin=subprocess.DEVNULL,
        )
        line_count = 0
        tail_buffer: list[str] = []  # keep only last 10 lines for errors
        assert proc.stdout is not None  # for type checkers
        for line in proc.stdout:
            stripped = line.rstrip()
            if stripped:
                line_count += 1
                tail_buffer.append(stripped)
                if len(tail_buffer) > 10:
                    tail_buffer.pop(0)
                if line_count % 500 == 0:
                    _log_progress(
                        "  gcloud progress (%s): %d operations...",
                        src.split("/")[-2],
                        line_count,
                    )
        rc = proc.wait()
        if rc != 0:
            tail = "\n".join(tail_buffer) if tail_buffer else "(no output)"
            return f"gcloud storage cp failed for {src} (exit {rc}):\n{tail}"
        return None

    # If we're using explicit service-account creds, write them to a temp file
    # and point gcloud at it via CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE.
    #
    # If we're using ADC (token is None), do NOT set the override; let gcloud
    # resolve credentials via its normal ADC mechanisms.
    creds_path: str | None = None
    gcloud_env = dict(os.environ)
    if token is not None:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            delete=False,
        ) as creds_fd:
            json.dump(token, creds_fd)
            creds_path = creds_fd.name
        gcloud_env["CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE"] = creds_path

    t_start = time.monotonic()

    try:
        # Run all copy operations in parallel.
        with ThreadPoolExecutor(
            max_workers=min(len(pairs), _GCLOUD_CP_MAX_WORKERS)
        ) as executor:
            futures = {executor.submit(_run_one_copy, p, gcloud_env): p for p in pairs}
            for future in as_completed(futures):
                error = future.result()
                if error:
                    result.errors.append(error)
                    _log_progress(error)
    finally:
        if creds_path:
            os.unlink(creds_path)

    elapsed = time.monotonic() - t_start

    # Each pair covers a connector prefix; estimate blobs per pair
    # proportionally so partial failures don't zero out the count.
    failed_pairs = len(result.errors)
    successful_pairs = len(pairs) - failed_pairs
    if len(pairs) > 0:
        result.blobs_copied = total_blobs * successful_pairs // len(pairs)
    else:
        result.blobs_copied = 0
    result.connectors_processed = len(connector_names)
    _log_progress(
        "%s [%.1fs elapsed, ~%.0f blobs/s]",
        result.summary(),
        elapsed,
        result.blobs_copied / elapsed if elapsed > 0 else 0,
    )

    return result


def _fsspec_copy(
    source_fs: gcsfs.GCSFileSystem,
    source_paths: list[str],
    output_fs: fsspec.AbstractFileSystem,
    output_base: str,
    output_mode: OutputMode,
    source_bucket: str,
    blob_relative_paths: list[str],
    connector_names: set[str],
    result: RebuildResult,
) -> RebuildResult:
    """Fallback copy using fsspec (read-through-Python) for non-GCS targets."""
    logger.info(
        "Starting fsspec copy from bucket %s to %s (%d blobs)",
        source_bucket,
        output_base,
        len(source_paths),
    )
    total_blobs = len(source_paths)

    for idx, (source_path, relative_path) in enumerate(
        zip(source_paths, blob_relative_paths)
    ):
        if output_mode == "local":
            output_path = f"{output_base}/{relative_path}"
        else:
            output_path = f"{output_base}{relative_path}"

        if output_mode == "local":
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        try:
            with source_fs.open(source_path, "rb") as src:
                content = src.read()
            with output_fs.open(output_path, "wb") as dst:
                dst.write(content)
            result.blobs_copied += 1
        except Exception as exc:
            result.errors.append(f"Failed to copy {source_path}: {exc}")
            logger.warning("Failed to copy %s: %s", source_path, exc)

        if (idx + 1) % 1000 == 0 or idx == 0:
            _log_progress(
                "Progress: %d/%d blobs copied (%d connectors)",
                result.blobs_copied,
                total_blobs,
                len(connector_names),
            )

    result.connectors_processed = len(connector_names)
    _log_progress(result.summary())
    return result


def _log_progress(msg: str, *args: object) -> None:
    """Log a progress message to both the logger and stderr."""
    logger.info(msg, *args)
    formatted = msg % args if args else msg
    print(formatted, file=sys.stderr, flush=True)
