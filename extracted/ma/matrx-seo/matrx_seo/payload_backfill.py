"""Move already-persisted inline raw payloads out of Postgres and into the store.

Why this exists
---------------
``seo.raw_payload`` holds one immutable provider response per collection. The
collect path has always been able to offload a payload to the host's file
pipeline and keep only a ``cloud_file_id`` — but the size ceiling that decided
*when* was a 1 MB constant, and the average payload is 892 KB. Almost everything
therefore stayed inline: 6,552 rows, 2.5 GB, **8.8% of the entire platform
database** (measured 2026-08-21). Lowering the ceiling to the
``seo.inline_payload_max_bytes`` knob fixes every FUTURE capture. This module
fixes the ones already written.

The one rule
------------
**Write → verify → NULL, in that order, always.** A payload is deleted from
Postgres only after the bytes have been read BACK out of the store and matched,
byte for byte, against what was uploaded. There is no path through this module
that clears a payload it has not personally re-read; a failed or unverified
upload leaves the row exactly as it was, with the reason recorded in
``offload_error``.

Bounded and resumable
---------------------
One call does at most ``batch_size`` rows, oldest first, and its selection
predicate (``cloud_file_id IS NULL AND payload IS NOT NULL``) is exactly what a
successful row stops matching. Re-running is therefore always safe and always
makes progress: nothing is claimed, nothing is leased, and a crash mid-batch
costs at most one duplicate upload of a row that never got promoted.

Rows carrying an ``offload_error`` are not a separate case — an errored row
still holds its inline payload, so it is picked up by the same walk and retried
through the same path. The error clears when the offload succeeds.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field
from typing import Any

from .config import get_payload_fetcher, get_payload_store
from .contracts import CollectionRequest, SeoCapability
from .db import models_seo as m
from .identity import stable_hash
from .knobs import int_knob


def canonical_payload_bytes(payload: Any) -> tuple[bytes, str]:
    """The exact encoding + checksum the collect path produced for this payload.

    Identical to ``service._prepare_provider_response`` on purpose: a backfilled
    row must be indistinguishable from a row that offloaded at capture time."""
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode()
    return encoded, stable_hash(payload)


@dataclass
class BackfillReport:
    """What one bounded pass actually did. Every count is a real row."""

    scanned: int = 0
    offloaded: int = 0
    bytes_offloaded: int = 0
    skipped_checksum_drift: int = 0
    skipped_empty: int = 0
    failed: int = 0
    failures_by_type: dict[str, int] = field(default_factory=dict)
    failure_examples: list[str] = field(default_factory=list)
    drift_examples: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "scanned": self.scanned,
            "offloaded": self.offloaded,
            "bytes_offloaded": self.bytes_offloaded,
            "skipped_checksum_drift": self.skipped_checksum_drift,
            "skipped_empty": self.skipped_empty,
            "failed": self.failed,
            "failures_by_type": dict(self.failures_by_type),
            "failure_examples": list(self.failure_examples),
            "drift_examples": list(self.drift_examples),
        }


def _request_for_run(run: Any) -> CollectionRequest:
    """Rebuild the collection request the payload store needs for provenance.

    The store keys the file by owner, organization, operation and capability —
    all of which the run row still carries, so a backfilled file lands with the
    same identity it would have had at capture time."""
    return CollectionRequest(
        organization_id=str(run.organization_id),
        created_by=str(run.created_by),
        capability=SeoCapability(str(run.capability)),
        operation=str(run.operation),
        target_ref=str(run.target_ref),
        observation_period=str(run.observation_period),
    )


async def _offload_ceiling() -> int:
    """The SAME ceiling the collect path applies. The backfill exists to catch
    up to the knob, never to invent its own idea of what belongs in S3."""
    return await int_knob("seo", "inline_payload_max_bytes")


async def _pending_ids(batch_size: int) -> list[str]:
    """Oldest-first ids of rows holding an inline payload ABOVE the ceiling.

    Rows at or under the knob are not pending work — they are correctly inline,
    and walking them is what turns "re-run until dry" into a loop that stalls on
    rows it was never supposed to move (69 such rows live today, none over
    30 KB).

    Ids only: hydrating a batch of ~900 KB payloads in one query times the
    statement out (measured against the live table)."""
    rows = await (
        m.RawPayload.filter(
            cloud_file_id__isnull=True,
            payload__isnull=False,
            size_bytes__gt=await _offload_ceiling(),
        )
        .order_by("created_at")
        .limit(batch_size)
        .values("id")
    )
    return [str(row["id"]) for row in rows]


async def offload_one_raw_payload(raw_payload_id: str, report: BackfillReport) -> None:
    """Write → verify → NULL for exactly one row. Never raises for one bad row.

    Every early return leaves the payload untouched in Postgres, which is the
    correct outcome for anything this function could not prove."""
    row = await m.RawPayload.load_by_id_or_none(raw_payload_id)
    if row is None or row.cloud_file_id:
        return
    report.scanned += 1
    payload = row.payload
    if not isinstance(payload, dict | list):
        report.skipped_empty += 1
        return

    encoded, checksum = canonical_payload_bytes(payload)
    if checksum != str(row.checksum) or len(encoded) != int(row.size_bytes):
        # The row's checksum is its identity within the run (the dedup key) and
        # its evidence fingerprint. If re-encoding the stored JSONB no longer
        # reproduces it, we cannot claim the object in S3 is what the row says
        # it is — so we say so and leave the payload alone, rather than quietly
        # rewriting the fingerprint to match whatever we happened to upload.
        report.skipped_checksum_drift += 1
        if len(report.drift_examples) < 10:
            report.drift_examples.append(
                f"{row.id}: stored size={row.size_bytes} recomputed={len(encoded)}"
            )
        return

    run = await m.CollectionRun.load_by_id_or_none(str(row.run_id))
    if run is None:
        report.failed += 1
        report.failures_by_type["OrphanedRun"] = report.failures_by_type.get("OrphanedRun", 0) + 1
        return

    try:
        stored = await get_payload_store()(
            _request_for_run(run), str(run.provider), encoded, checksum
        )
        # VERIFY: read the bytes back out of the store before anything is
        # deleted. An upload that "succeeded" but cannot be read is data loss
        # waiting for the DELETE that follows it.
        fetched = await get_payload_fetcher()(stored.cloud_file_id)
        if fetched != encoded:
            raise RuntimeError(
                f"read-back mismatch for {stored.cloud_file_id}: "
                f"uploaded {len(encoded)} bytes, read back {len(fetched)}"
            )
        if stored.checksum != checksum or int(stored.size_bytes) != len(encoded):
            raise RuntimeError(
                f"store receipt disagrees with the payload: receipt "
                f"checksum={stored.checksum} size={stored.size_bytes}"
            )
    except Exception as exc:  # noqa: BLE001 — one bad row never stops the batch
        report.failed += 1
        name = type(exc).__name__
        report.failures_by_type[name] = report.failures_by_type.get(name, 0) + 1
        if len(report.failure_examples) < 10:
            report.failure_examples.append(f"{row.id}: {name}: {exc}"[:400])
        await row.update(offload_error={"type": name, "message": str(exc)[:2000]})
        return

    # Verified. Only now does the payload leave Postgres.
    await row.update(
        cloud_file_id=stored.cloud_file_id,
        content_type=stored.content_type,
        payload=None,
        offload_error=None,
    )
    report.offloaded += 1
    report.bytes_offloaded += len(encoded)


async def backfill_inline_payloads(*, batch_size: int = 50, concurrency: int = 1) -> BackfillReport:
    """One bounded, resumable pass. Returns what it did; re-run until dry.

    ``concurrency`` is transport parallelism, nothing more. One row costs ~10
    seconds almost entirely in the file pipeline's round trips (measured live
    2026-08-22: a 2.9 MB payload uploads in 9.8 s, a 3 KB payload in 10.2 s — it
    is per-call latency, not bandwidth), so a serial walk of the backlog would
    have run for ~20 hours. Rows are independent — each one is its own
    write → verify → NULL against its own row — so overlapping them changes the
    clock and nothing else. The report is mutated from several tasks, which is
    safe: this is one event loop, and every mutation is a whole statement.
    """
    report = BackfillReport()
    ids = await _pending_ids(batch_size)
    if concurrency <= 1:
        for raw_payload_id in ids:
            await offload_one_raw_payload(raw_payload_id, report)
        return report

    limit = asyncio.Semaphore(concurrency)

    async def _one(raw_payload_id: str) -> None:
        async with limit:
            await offload_one_raw_payload(raw_payload_id, report)

    await asyncio.gather(*(_one(raw_payload_id) for raw_payload_id in ids))
    return report


async def pending_inline_count() -> int:
    """Rows still holding an inline payload the knob says belongs in S3.

    The loop's stop condition, and it reaches zero: a row at or under the
    ceiling is not counted, because it is not pending — it is done."""
    return await m.RawPayload.filter(
        cloud_file_id__isnull=True,
        payload__isnull=False,
        size_bytes__gt=await _offload_ceiling(),
    ).count()


__all__ = [
    "BackfillReport",
    "backfill_inline_payloads",
    "canonical_payload_bytes",
    "offload_one_raw_payload",
    "pending_inline_count",
]
