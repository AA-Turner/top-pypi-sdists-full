"""A LIVE FILE WITH NO LIVE THUMBNAIL HEALS ITSELF (Matrx Scan, 2026-11-20).

Live: 377 live files had every thumbnail variant soft-deleted (a test run's archive took variants its run had
re-rendered for an unstamped master). ``resolve_thumbnail_url_async`` answered None and rendered nothing, and
``read_thumbnail_async`` "never queues a render", so the Matrx Scan library showed gray tiles forever.

SUT: the real resolver doors and the real ``VariantsService`` catalog. Replaced: the DB's variant query (live rows
only, as the real one), the gated master read, and the render itself (a probe — ``generate_thumbnail_for_file`` —
that records which file it was asked to render). Remove the heal from either door → red. Remove the per-file read
guard → the second read queues again → red.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_files import gated_reads
from matrx_files.cloud_sync import thumbnail_resolver as sut
from matrx_files.cloud_sync.variants_service import VariantsService


@pytest.fixture(autouse=True)
def fresh_memo(monkeypatch):
    monkeypatch.setattr(sut, "_read_render_queued_at", {}, raising=False)


@pytest.fixture
def renders(monkeypatch) -> list[str]:
    import matrx_files.cloud_sync.processing as processing

    seen: list[str] = []

    async def probe(_fm: Any, file_id: str, **_: Any) -> bool:
        seen.append(file_id)
        return True

    monkeypatch.setattr(processing, "generate_thumbnail_for_file", probe)
    return seen


def _fm(variant_rows: list[dict[str, Any]]) -> Any:
    async def list_variants(_master_id: str, *, include_deleted: bool = False) -> list[dict[str, Any]]:
        return [r for r in variant_rows if include_deleted or r.get("deleted_at") is None]

    async def build_urls(row: dict[str, Any]) -> dict[str, Any]:
        return {"url": f"https://cdn/{row['id']}"}

    engine = SimpleNamespace(db=SimpleNamespace(list_variants_by_master_async=list_variants))
    return SimpleNamespace(
        sync_engine=SimpleNamespace(variants=VariantsService(engine), build_urls_for_record_async=build_urls)  # type: ignore[arg-type]
    )


TRASHED_THUMB = {
    "id": "v-trashed", "deleted_at": "2026-11-18T00:00:00Z", "storage_uri": "s3://b/v.jpg",
    "metadata": {"variant_key": "thumbnail_url", "derived_from": "m1"},
}


def _master(**over: Any) -> dict[str, Any]:
    return {"id": "m1", "owner_id": "u", "mime_type": "image/jpeg", "current_version": 1, "metadata": {},
            "deleted_at": None, **over}


async def _settle() -> None:
    for _ in range(5):
        await asyncio.sleep(0)


async def test_a_live_picture_whose_thumbnails_were_all_trashed_queues_its_render(renders) -> None:
    fm = _fm([TRASHED_THUMB])
    assert await sut.resolve_thumbnail_url_async(fm, _master()) is None  # the read never waits on the render
    await _settle()
    assert renders == ["m1"], "a live file with no live thumbnail renders nothing — its tile stays gray forever"


async def test_a_file_polled_again_queues_no_second_render(renders) -> None:
    fm = _fm([])
    for _ in range(5):
        await sut.resolve_thumbnail_url_async(fm, _master())
    await _settle()
    assert renders == ["m1"], f"one read render per file per window, got {renders}"


@pytest.mark.parametrize(
    "master",
    [
        _master(mime_type="text/plain"),
        _master(mime_type="application/zip"),
        _master(deleted_at="2026-11-19T00:00:00Z"),
        _master(metadata={"derived_from": "m0", "variant_key": "thumbnail_url"}),
        _master(derivation_kind="variant"),
    ],
    ids=["text", "archive", "trashed master", "variant by metadata", "variant by column"],
)
async def test_files_that_never_get_a_thumbnail_queue_nothing(renders, master) -> None:
    assert await sut.resolve_thumbnail_url_async(_fm([]), master) is None
    await _settle()
    assert renders == []


async def test_the_thumbnail_door_heals_a_live_file_too(renders, monkeypatch) -> None:
    master = _master()

    async def read_file_row(file_id: str, columns, *, user_id=None, **_: Any):
        return {k: master.get(k) for k in ("id", *columns)}

    monkeypatch.setattr(gated_reads, "read_file_row", read_file_row)
    assert await sut.read_thumbnail_async(_fm([TRASHED_THUMB]), "m1", user_id="u") is None
    await _settle()
    assert renders == ["m1"], "GET /files/{id}/thumbnail of a live file with no thumbnail renders nothing"


async def test_a_page_of_missing_thumbnails_never_runs_more_than_the_bound_at_once(monkeypatch) -> None:
    """A list page gathers every row: 20 thumbnail-less files must never mean 20 downloads + renders at once."""
    import matrx_files.cloud_sync.processing as processing

    monkeypatch.setattr(sut, "_render_gate", None)
    running = 0
    peak = 0
    finished: list[str] = []
    release = asyncio.Event()

    async def slow_render(_fm: Any, file_id: str, **_: Any) -> bool:
        nonlocal running, peak
        running += 1
        peak = max(peak, running)
        await release.wait()
        running -= 1
        finished.append(file_id)
        return True

    monkeypatch.setattr(processing, "generate_thumbnail_for_file", slow_render)
    records = [_master(id=f"m{i}") for i in range(20)]
    await sut.resolve_thumbnail_urls_async(_fm([]), records)
    await _settle()
    assert peak == sut.READ_RENDER_CONCURRENCY, f"{peak} renders ran at once (bound {sut.READ_RENDER_CONCURRENCY})"
    release.set()
    for _ in range(200):
        if len(finished) == 20:
            break
        await asyncio.sleep(0)
    assert sorted(finished) == sorted(r["id"] for r in records), "a waiting render was dropped instead of queued"
    assert peak <= sut.READ_RENDER_CONCURRENCY


async def test_a_render_that_never_started_is_retried_on_the_next_read(renders, monkeypatch) -> None:
    import matrx_utils

    real = matrx_utils.supervised_task
    calls = {"n": 0}

    def flaky(coro, **kw):
        calls["n"] += 1
        if calls["n"] == 1:
            coro.close()
            raise RuntimeError("no running loop")
        return real(coro, **kw)

    monkeypatch.setattr(matrx_utils, "supervised_task", flaky)
    fm = _fm([])
    await sut.resolve_thumbnail_url_async(fm, _master())
    await sut.resolve_thumbnail_url_async(fm, _master())
    await _settle()
    assert renders == ["m1"], "a spawn failure suppressed the file's render for the whole retry window"


def test_the_memo_evicts_its_oldest_in_one_batch(monkeypatch) -> None:
    monkeypatch.setattr(sut, "READ_RENDER_MEMO_MAX", 100)
    for i in range(101):
        assert sut._claim_read_render(f"f{i}")
    assert len(sut._read_render_queued_at) == 91, "past the cap the oldest tenth is dropped at once"
    assert "f0" not in sut._read_render_queued_at and "f100" in sut._read_render_queued_at
    for i in range(101, 110):
        sut._claim_read_render(f"f{i}")
    assert len(sut._read_render_queued_at) == 100, "no eviction (and no sort) until the cap is passed again"
