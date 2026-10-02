"""The one rule of the raw-payload backfill: write → verify → NULL, in that order.

These pin the safety property, not the plumbing. `matrx_seo.payload_backfill`
reaches the live `seo.*` models directly (it is a batch job over rows that
already exist), so the models are replaced here with in-memory doubles and the
real ``offload_one_raw_payload`` is exercised against them.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

import matrx_seo
from matrx_seo.payload_backfill import (
    BackfillReport,
    backfill_inline_payloads,
    canonical_payload_bytes,
    offload_one_raw_payload,
)
from matrx_seo import StoredPayloadReceipt

PAYLOAD: dict[str, Any] = {"items": [{"rank": 1, "url": "https://example.com"}], "ok": True}


class _FakeRow:
    def __init__(self, row_id: str, payload: Any) -> None:
        encoded, checksum = canonical_payload_bytes(payload)
        self.id = row_id
        self.run_id = "run-1"
        self.payload = payload
        self.checksum = checksum
        self.size_bytes = len(encoded)
        self.cloud_file_id = None
        self.content_type = None
        self.offload_error = None

    async def update(self, **fields: Any) -> None:
        for key, value in fields.items():
            setattr(self, key, value)


class _FakeRun:
    id = "run-1"
    organization_id = "11111111-1111-1111-1111-111111111111"
    created_by = "22222222-2222-2222-2222-222222222222"
    capability = "serp_rank"
    operation = "serp_google_organic"
    target_ref = "example.com"
    observation_period = "2026-08-01"
    provider = "dataforseo"


@pytest.fixture
def rows(monkeypatch: pytest.MonkeyPatch) -> dict[str, _FakeRow]:
    store: dict[str, _FakeRow] = {}

    class _RawPayload:
        @staticmethod
        async def load_by_id_or_none(row_id: str) -> _FakeRow | None:
            return store.get(row_id)

    class _CollectionRun:
        @staticmethod
        async def load_by_id_or_none(_run_id: str) -> _FakeRun:
            return _FakeRun()

    from matrx_seo import payload_backfill

    monkeypatch.setattr(payload_backfill.m, "RawPayload", _RawPayload, raising=False)
    monkeypatch.setattr(payload_backfill.m, "CollectionRun", _CollectionRun, raising=False)
    return store


def _configure_store(uploaded: dict[str, bytes], *, corrupt_read: bool = False) -> None:
    async def payload_store(_request, _provider, content, checksum):
        uploaded["file-1"] = content
        return StoredPayloadReceipt(
            cloud_file_id="file-1",
            checksum=checksum,
            size_bytes=len(content),
            content_type="application/json",
        )

    async def payload_fetcher(cloud_file_id: str) -> bytes:
        content = uploaded[cloud_file_id]
        return content[:-1] if corrupt_read else content

    matrx_seo.configure(payload_store=payload_store, payload_fetcher=payload_fetcher)


@pytest.mark.asyncio
async def test_verified_upload_is_the_only_thing_that_clears_a_payload(rows) -> None:
    rows["a"] = _FakeRow("a", PAYLOAD)
    uploaded: dict[str, bytes] = {}
    _configure_store(uploaded)

    report = BackfillReport()
    await offload_one_raw_payload("a", report)

    assert report.offloaded == 1
    assert rows["a"].payload is None
    assert rows["a"].cloud_file_id == "file-1"
    assert rows["a"].offload_error is None
    # The bytes in the store are exactly the canonical encoding of what the row
    # held — a backfilled row is indistinguishable from one offloaded at capture.
    assert json.loads(uploaded["file-1"]) == PAYLOAD


@pytest.mark.asyncio
async def test_unverifiable_upload_keeps_the_payload_and_records_why(rows) -> None:
    rows["a"] = _FakeRow("a", PAYLOAD)
    _configure_store({}, corrupt_read=True)

    report = BackfillReport()
    await offload_one_raw_payload("a", report)

    assert report.failed == 1
    assert report.offloaded == 0
    # The read-back disagreed, so nothing was deleted. This is the whole point.
    assert rows["a"].payload == PAYLOAD
    assert rows["a"].cloud_file_id is None
    assert rows["a"].offload_error["type"] == "RuntimeError"


@pytest.mark.asyncio
async def test_checksum_drift_is_refused_rather_than_rewritten(rows) -> None:
    row = _FakeRow("a", PAYLOAD)
    row.checksum = "not-the-checksum-of-this-payload"
    rows["a"] = row
    uploaded: dict[str, bytes] = {}
    _configure_store(uploaded)

    report = BackfillReport()
    await offload_one_raw_payload("a", report)

    assert report.skipped_checksum_drift == 1
    assert not uploaded
    assert rows["a"].payload == PAYLOAD
    assert rows["a"].cloud_file_id is None


@pytest.mark.asyncio
async def test_an_already_offloaded_row_is_never_touched_again(rows) -> None:
    row = _FakeRow("a", PAYLOAD)
    row.cloud_file_id = "already-there"
    row.payload = None
    rows["a"] = row
    uploaded: dict[str, bytes] = {}
    _configure_store(uploaded)

    report = BackfillReport()
    await offload_one_raw_payload("a", report)

    assert report.scanned == 0
    assert not uploaded
    assert rows["a"].cloud_file_id == "already-there"


@pytest.mark.asyncio
async def test_a_concurrent_pass_offloads_every_row_exactly_once(rows, monkeypatch) -> None:
    for index in range(12):
        rows[str(index)] = _FakeRow(str(index), {**PAYLOAD, "n": index})
    uploads: list[bytes] = []

    async def payload_store(_request, _provider, content, checksum):
        uploads.append(content)
        return StoredPayloadReceipt(
            cloud_file_id=f"file-{len(uploads)}",
            checksum=checksum,
            size_bytes=len(content),
            content_type="application/json",
        )

    async def payload_fetcher(cloud_file_id: str) -> bytes:
        return uploads[int(cloud_file_id.split("-")[1]) - 1]

    matrx_seo.configure(payload_store=payload_store, payload_fetcher=payload_fetcher)

    from matrx_seo import payload_backfill

    async def _pending_ids(batch_size: int) -> list[str]:
        return [key for key, row in rows.items() if row.payload is not None][:batch_size]

    monkeypatch.setattr(payload_backfill, "_pending_ids", _pending_ids)

    report = await backfill_inline_payloads(batch_size=60, concurrency=6)

    assert report.offloaded == 12
    assert len(uploads) == 12
    assert all(row.payload is None and row.cloud_file_id for row in rows.values())


@pytest.mark.asyncio
async def test_the_walk_only_claims_rows_the_knob_says_belong_in_the_store(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A row at or under the ceiling is not pending work — it is correctly
    inline. Walking it anyway is what made the walk stall short of dry: it kept
    re-selecting rows it was never supposed to move (69 such rows live, none
    over 30 KB), reported no progress, and stopped."""
    from matrx_seo import payload_backfill

    selected: dict[str, Any] = {}

    class _Query:
        def __init__(self, **filters: Any) -> None:
            selected.update(filters)

        def order_by(self, *_a: Any) -> _Query:
            return self

        def limit(self, *_a: Any) -> _Query:
            return self

        async def values(self, *_a: Any) -> list[dict[str, Any]]:
            return []

        async def count(self) -> int:
            return 0

    class _RawPayload:
        @staticmethod
        def filter(**filters: Any) -> _Query:
            return _Query(**filters)

    monkeypatch.setattr(payload_backfill.m, "RawPayload", _RawPayload, raising=False)

    async def _ceiling(_feature: str, _key: str) -> int:
        return 32768

    monkeypatch.setattr(payload_backfill, "int_knob", _ceiling)

    assert await payload_backfill.pending_inline_count() == 0
    # The ceiling is part of the predicate — not applied after the fact.
    assert selected["size_bytes__gt"] == 32768
    assert selected["cloud_file_id__isnull"] is True
    assert selected["payload__isnull"] is False
