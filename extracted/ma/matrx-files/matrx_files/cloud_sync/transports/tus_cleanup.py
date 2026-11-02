"""Periodic cleanup of abandoned TUS resumable uploads.

When a TUS client (browser, agent, anything) creates a multipart upload and
never finalizes / aborts it (browser tab closed, network disappeared, OS
killed the process), the `files.uploads_inflight` row sits with
``status='in_progress'`` and the S3 multipart upload remains open. Each
abandoned multipart is real ongoing AWS storage cost — S3 charges for
uploaded parts until they're completed or aborted.

This module provides the cleanup loop that runs periodically (typically
hourly) and:

1. Finds every nonterminal row where ``expires_at < now()``.
2. For each row, calls :meth:`TUSSessionManager.abort_stale_async` which performs
   BOTH the S3 ``AbortMultipartUpload`` call AND the DB transition to
   ``status='aborted'`` atomically (well, sequentially — but together).
3. On per-row failure, logs and continues — one bad row can't block the
   rest of the sweep.

This is the **active S3 + DB cleanup**, distinct from the
``InFlightRegistry`` watchdog that only flips the DB status. The watchdog
serves as the alert/insight layer; this module is the actual janitor.

Usage (from a host application like aidream):

    from matrx_files.cloud_sync.transports.tus_cleanup import (
        run_tus_cleanup_loop,
    )

    # In your FastAPI lifespan or equivalent:
    cleanup_task = asyncio.create_task(
        run_tus_cleanup_loop(file_manager, interval_secs=3600)
    )

Why this lives in matrx-utils, not in aidream
---------------------------------------------
The cleanup is independent of any host-app concept and operates purely
through the matrx-utils ``SyncEngine`` + ``TUSSessionManager`` APIs.
Bundling it with the TUS implementation means every project that imports
the TUS transport gets the matching cleanup loop for free.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from matrx_utils import vcprint

from ..db import _models, _vals

if TYPE_CHECKING:
    from matrx_files.cloud_sync.sync_engine import SyncEngine

logger = logging.getLogger("matrx_utils.tus_cleanup")


DEFAULT_INTERVAL_SECS = 3600.0  # hourly sweep is plenty for upload abandonment
DEFAULT_BATCH_LIMIT = 100  # per-tick cap; rerun catches the rest


@dataclass(slots=True)
class TUSCleanupReport:
    """Per-tick summary returned by :func:`sweep_once`. For observability."""

    scanned: int = 0
    aborted: int = 0
    finalized: int = 0
    failed: int = 0
    errors: list[str] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.errors is None:
            self.errors = []


async def _find_expired_uploads(engine: SyncEngine, limit: int) -> list[dict[str, Any]]:
    """Return every nonterminal upload past its expires_at.

    Cheap query — uses the partial index
    ``idx_cld_uploads_inflight_expires`` (nonterminal states only).
    """
    mf, _ = _models()
    rows = await (
        mf.UploadsInflight.filter(
            status__in=[
                "in_progress",
                "uploading",
                "ready",
                "finalizing",
                "aborting",
            ],
            expires_at__lt=datetime.now(UTC),
        )
        .order_by("expires_at")
        .limit(limit)
        .values(
            "id",
            "owner_id",
            "status",
            "expires_at",
            "upload_length",
            "upload_offset",
            "multipart_upload_id",
        )
    )
    # Presigned-PUT pending rows have no multipart upload to abort; the
    # PresignedManager closes its own expired rows.
    return [r for r in _vals(rows) if r.get("multipart_upload_id") != "presigned"]


async def sweep_once(
    file_manager: Any,
    *,
    limit: int = DEFAULT_BATCH_LIMIT,
    finalize_ready: Callable[[Any, Any, str, str], Awaitable[Any]] | None = None,
) -> TUSCleanupReport:
    """One pass: find expired uploads, abort each one. Never raises."""
    report = TUSCleanupReport()

    # Resolve engine + TUS manager. Allow file_manager to be either the
    # FileManager facade or the SyncEngine directly so test code can pass
    # the engine in without spinning up the full file_manager.
    engine = getattr(file_manager, "sync_engine", None) or file_manager
    tus_manager = getattr(engine, "tus", None)
    if tus_manager is None:
        logger.warning("tus_cleanup: engine has no .tus attribute; cleanup skipped")
        return report

    try:
        rows = await _find_expired_uploads(engine, limit)
    except Exception as exc:
        report.errors.append(f"select failed: {type(exc).__name__}: {exc}")
        vcprint(
            f"[TUS Cleanup] SELECT failed: {type(exc).__name__}: {exc}",
            color="red",
        )
        return report

    report.scanned = len(rows)
    if not rows:
        return report

    for row in rows:
        upload_id = row["id"]
        owner_id = row["owner_id"]
        try:
            if row["status"] == "ready":
                if finalize_ready is None:
                    await tus_manager.finalize_async(
                        upload_id=upload_id,
                        owner_id=owner_id,
                    )
                else:
                    await finalize_ready(
                        file_manager,
                        tus_manager,
                        upload_id,
                        owner_id,
                    )
                report.finalized += 1
            else:
                await tus_manager.abort_stale_async(
                    upload_id=upload_id,
                    owner_id=owner_id,
                    expected_status=row["status"],
                )
                report.aborted += 1
        except Exception as exc:
            # abort_async raises UploadNotFound when the row's status is
            # already 'completed'/'aborted' — that's a benign race with the
            # producer, treat as success.
            err_name = type(exc).__name__
            if err_name in {"UploadNotFound", "UploadCompleted"}:
                report.aborted += 1
                continue
            report.failed += 1
            report.errors.append(f"{upload_id}: {err_name}: {exc}")
            logger.warning(
                "tus_cleanup: abort failed for %s (owner=%s): %s: %s",
                upload_id,
                owner_id,
                err_name,
                exc,
            )

    if report.aborted or report.finalized or report.failed:
        vcprint(
            f"[TUS Cleanup] Swept {report.scanned} expired upload(s): "
            f"{report.finalized} finalized, {report.aborted} aborted, "
            f"{report.failed} failed",
            color="green" if not report.failed else "yellow",
        )

    return report


async def run_tus_cleanup_loop(
    file_manager: Any,
    *,
    interval_secs: float = DEFAULT_INTERVAL_SECS,
    limit: int = DEFAULT_BATCH_LIMIT,
    finalize_ready: Callable[[Any, Any, str, str], Awaitable[Any]] | None = None,
) -> None:
    """Periodic loop. Cancel the task to stop.

    The outer try/except guarantees the loop never dies on a transient
    failure — sleep, retry. Only task cancellation stops it.
    """
    vcprint(
        f"[TUS Cleanup] Started (every {interval_secs:.0f}s, batch {limit})",
        color="green",
    )
    while True:
        try:
            await sweep_once(
                file_manager,
                limit=limit,
                finalize_ready=finalize_ready,
            )
        except asyncio.CancelledError:
            vcprint("[TUS Cleanup] Stopping", color="green")
            raise
        except Exception as exc:
            vcprint(
                f"[TUS Cleanup] Tick raised {type(exc).__name__}: {exc} "
                f"— continuing after interval",
                color="red",
            )
            logger.exception("tus_cleanup_tick_failed")
        try:
            await asyncio.sleep(interval_secs)
        except asyncio.CancelledError:
            vcprint(
                "[TUS Cleanup] Stopping",
                color="green",
            )
            raise


__all__ = [
    "DEFAULT_BATCH_LIMIT",
    "DEFAULT_INTERVAL_SECS",
    "TUSCleanupReport",
    "run_tus_cleanup_loop",
    "sweep_once",
]
