"""Persistence protocol — the host injects a concrete impl.

The dispatcher only knows this protocol. aidream provides a matrx-orm
implementation; Matrx Local Desktop could plug in a SQLite one.

Two responsibilities:
  1. Write `file_analysis` (current state) and `file_analysis_result` (audit) rows.
  2. Offload "extended payload" blobs to S3 (or equivalent) when an inline
     JSONB result would exceed the configured threshold.
"""

from __future__ import annotations

import dataclasses
import datetime as _datetime
import decimal
import json
import pathlib
import uuid
from typing import Any, Protocol

from .context import ResolvedSettings
from .protocol import PageInfo


class PersistenceProtocol(Protocol):
    """Host-injected DB + extended-storage backend."""

    async def upsert_pages(
        self,
        *,
        file_id: str,
        owner_id: str,
        pages: list[PageInfo],
    ) -> dict[int, str]:
        """Upsert one `file_pages` row per page. Returns
        {source_page_index: page_id} for the dispatcher to resolve page_id
        on detector results. Called BEFORE any detector runs.

        Idempotent: re-running analysis on the same file updates existing
        rows without resetting user_modified / status fields.
        """
        ...

    async def upsert_analysis_start(
        self,
        *,
        file_id: str,
        owner_id: str,
        mime_type: str,
        analyzer_version: str,
        total_detectors: int,
    ) -> None: ...

    async def update_progress(
        self,
        *,
        file_id: str,
        complete: int,
        total: int,
        current_kind: str | None,
    ) -> None: ...

    async def record_detector_run(
        self,
        *,
        file_id: str,
        kind: str,
        version: str,
        status: str,
        started_at_iso: str | None,
        finished_at_iso: str | None,
        error: str | None,
    ) -> None: ...

    async def insert_result(
        self,
        *,
        file_id: str,
        detector_kind: str,
        detector_version: str,
        confidence_tier: str,
        status: str,
        text_sources: list[str],
        elapsed_ms: int,
        summary: dict[str, Any],
        payload: dict[str, Any] | None,
        payload_uri: str | None,
        payload_bytes: int,
        error: str | None,
        page_id: str | None = None,
    ) -> None: ...

    async def update_page_text_source(
        self,
        *,
        page_id: str,
        text_source: str,
        ocr_confidence: float | None = None,
    ) -> None:
        """Patch file_pages.text_source + ocr_confidence after text extraction lands."""
        ...

    async def is_page_user_locked(
        self,
        *,
        file_id: str,
        page_id: str,
        kind: str,
    ) -> bool:
        """True when the user has touched this page in a way that should
        suppress a re-emit of the given detector kind. Used by the dispatcher's
        override-protection logic."""
        ...

    async def write_extended_payload(
        self,
        *,
        file_id: str,
        owner_id: str,
        detector_kind: str,
        detector_version: str,
        confidence_tier: str,
        payload_json: str,
    ) -> str:
        """Returns the URI (e.g. ``s3://...``) where the payload was written."""
        ...

    async def finalize(
        self,
        *,
        file_id: str,
        status: str,
        summary_counts: dict[str, Any],
        classification: dict[str, Any] | None,
        page_count: int | None,
        text_source_map: dict[str, Any] | None,
        metadata: dict[str, Any] | None,
    ) -> None: ...

    async def stamp_cld_files_metadata(
        self,
        *,
        file_id: str,
        analysis_summary: dict[str, Any],
    ) -> None: ...


def _serialize(payload: dict[str, Any]) -> str:
    return json.dumps(payload, default=_json_default, ensure_ascii=False)


def _json_default(obj: Any) -> Any:
    """Best-effort JSON fallback for arbitrary detector-payload objects.

    Detectors emit a variety of library-specific types — PyMuPDF
    ``fitz.Point`` / ``fitz.Rect`` (coordinate tuples), pydantic models,
    dataclasses, ``Decimal`` financial numbers, ``Path`` filesystem refs,
    ``datetime`` timestamps, ``UUID``s, raw ``bytes``. ``json.dumps``
    calls this ``default=`` hook ONLY for non-builtins; we walk the
    common shapes in order of likelihood and fall back to ``repr(obj)``
    at the very end so a single weird object never crashes the whole
    detector pipeline (one row degrading to a string is recoverable;
    a 30-detector run blowing up is not).
    """
    # Pydantic v2 (preferred — gives the richest dict).
    if hasattr(obj, "model_dump") and callable(obj.model_dump):
        try:
            return obj.model_dump()
        except Exception:
            pass

    # Pydantic v1 / objects with a no-arg .dict() returning a mapping.
    if hasattr(obj, "dict") and callable(getattr(obj, "dict", None)):
        try:
            result = obj.dict()
            if isinstance(result, dict):
                return result
        except Exception:
            pass

    # Dataclass instances (the type itself isn't serializable; instances are).
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        try:
            return dataclasses.asdict(obj)
        except Exception:
            pass

    # Stdlib types with built-in serialization.
    if isinstance(obj, (set, frozenset)):
        return list(obj)
    if isinstance(obj, (bytes, bytearray, memoryview)):
        try:
            return bytes(obj).decode("utf-8", errors="replace")
        except Exception:
            return repr(obj)
    if isinstance(obj, (_datetime.datetime, _datetime.date, _datetime.time)):
        return obj.isoformat()
    if isinstance(obj, _datetime.timedelta):
        return obj.total_seconds()
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, decimal.Decimal):
        # Round-trippable text representation (json doesn't have Decimal).
        return str(obj)
    if isinstance(obj, pathlib.PurePath):
        return str(obj)

    # NamedTuple — has ``_asdict``.
    asdict = getattr(obj, "_asdict", None)
    if callable(asdict):
        try:
            result = asdict()
            if isinstance(result, dict):
                return result
        except Exception:
            pass

    # PyMuPDF fitz.Point / fitz.Rect / shapely geometries / many vector types
    # are iterable as coordinate tuples. Strings, dicts, lists, tuples, and
    # bytes never reach this branch because json.dumps handles them natively
    # before calling ``default=``.
    if hasattr(obj, "__iter__") and not isinstance(obj, type):
        try:
            return list(obj)
        except Exception:
            pass

    # Object with a public attribute bag — last structured attempt.
    if hasattr(obj, "__dict__"):
        try:
            return {k: v for k, v in vars(obj).items() if not k.startswith("_")}
        except Exception:
            pass

    # Final lifeline — never crash the pipeline for one weird detector value.
    # The payload loses fidelity here, but the run completes and the operator
    # can see the type in the log to add a proper handler.
    return repr(obj)


async def persist_one_result(
    persistence: PersistenceProtocol,
    *,
    file_id: str,
    owner_id: str,
    settings: ResolvedSettings,
    detector_kind: str,
    detector_version: str,
    confidence_tier: str,
    status: str,
    text_sources: list[str],
    elapsed_ms: int,
    summary: dict[str, Any],
    payload: dict[str, Any],
    error: str | None,
    page_id: str | None = None,
) -> None:
    """Inline-vs-overflow split + INSERT. Pure orchestration."""
    payload_json = _serialize(payload) if payload else ""
    size = len(payload_json.encode("utf-8")) if payload_json else 0

    inline: dict[str, Any] | None = payload
    uri: str | None = None
    if size > settings.inline_payload_limit_bytes:
        uri = await persistence.write_extended_payload(
            file_id=file_id,
            owner_id=owner_id,
            detector_kind=detector_kind,
            detector_version=detector_version,
            confidence_tier=confidence_tier,
            payload_json=payload_json,
        )
        inline = None

    await persistence.insert_result(
        file_id=file_id,
        detector_kind=detector_kind,
        detector_version=detector_version,
        confidence_tier=confidence_tier,
        status=status,
        text_sources=text_sources,
        elapsed_ms=elapsed_ms,
        summary=summary,
        payload=inline,
        payload_uri=uri,
        payload_bytes=size,
        error=error,
        page_id=page_id,
    )


__all__ = ["PersistenceProtocol", "persist_one_result"]
