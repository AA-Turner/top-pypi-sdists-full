"""A VARIANT LIVES AS LONG AS ITS MASTER: its test stamp is the master's, never the writing session's (2026-11-20).

Live: a real organisation's two files lost every thumbnail. A test session re-rendered their variants; the database
trigger stamped the new variant rows with the SESSION's ``test_run_id`` / ``test_expires_at`` while the unstamped
master stayed unstamped; the run's archive then trashed the variants and left the master live (377 such files).

SUT: ``write_variant_as_its_master`` and the two ``VariantsService`` write doors over a recording engine whose
``managed_write_async`` notes the test run it runs under (the value the session-context provider would turn into
``app.test_run`` → the trigger's stamp). The registered test-run carrier is the standalone service's
(``matrx_files.standalone.test_stamp``). Write the variant inline again → the unstamped master's variant is
written under the run → red.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_files.cloud_sync.variants import write_variant_as_its_master
from matrx_files.cloud_sync.variants_service import VariantsService
from matrx_files.standalone import test_stamp

RUN = "0b7f0a52-3f2e-4a43-9d0c-6f1f7d3c9a11"
MASTER_RUN = "5c1a3d6e-8a0b-4f6e-9e7c-2d4b1a0c9f88"


@pytest.fixture
def in_a_test_session():
    token = test_stamp._current.set(RUN)
    try:
        yield
    finally:
        test_stamp._current.reset(token)


def _master(test_run_id: str | None) -> dict[str, Any]:
    return {"id": "m1", "owner_id": "u", "storage_uri": "s3://b/m1", "current_version": 1, "metadata": {},
            "organization_id": "org-1", "test_run_id": test_run_id}


async def test_an_unstamped_masters_variant_is_written_outside_the_test_run(in_a_test_session) -> None:
    async def write() -> str | None:
        return test_stamp.current_test_run_id()

    assert await write_variant_as_its_master(_master(None), write) is None, (
        "a person's file got a test-stamped variant: the run's archive will trash its thumbnail"
    )


async def test_a_stamped_masters_variant_keeps_the_session_that_stamped_it(in_a_test_session) -> None:
    async def write() -> str | None:
        return test_stamp.current_test_run_id()

    assert await write_variant_as_its_master(_master(MASTER_RUN), write) == RUN


async def test_a_failed_variant_write_still_reaches_the_caller(in_a_test_session) -> None:
    async def write() -> None:
        raise RuntimeError("disk full")

    with pytest.raises(RuntimeError, match="disk full"):
        await write_variant_as_its_master(_master(None), write)


class _Engine:
    def __init__(self) -> None:
        self.written_under: list[str | None] = []
        self.db = SimpleNamespace(list_variants_by_master_async=self._none)
        self.router = SimpleNamespace(read_async=self._bytes)
        self.fm = SimpleNamespace(
            image_handler=SimpleNamespace(
                _render_variants=lambda _b, specs: [(s["key"], s.get("suffix", s["key"]), "JPEG", b"jpg") for s in specs]
            )
        )

    async def _none(self, *_a: Any, **_k: Any) -> list[dict[str, Any]]:
        return []

    async def _bytes(self, _uri: str) -> bytes:
        return b"master"

    async def managed_write_async(self, path: str, data: bytes, **_: Any) -> Any:
        self.written_under.append(test_stamp.current_test_run_id())
        return SimpleNamespace(file_id=f"v-{len(self.written_under)}", size_bytes=len(data), url=None,
                               cdn_url=None, download_url=None)


@pytest.mark.parametrize("door", ["render_async", "persist_prerendered_async"])
async def test_both_variant_doors_follow_the_master(in_a_test_session, door) -> None:
    engine = _Engine()
    variants = VariantsService(engine)  # type: ignore[arg-type]
    for master in (_master(None), _master(MASTER_RUN)):
        if door == "render_async":
            await variants.render_async(master, variants_specs=[{"key": "thumbnail_url", "width": 400}])
        else:
            await variants.persist_prerendered_async(
                master, variant_key="page1_url", content=b"png", mime_type="image/png"
            )
    assert engine.written_under == [None, RUN], engine.written_under


async def test_a_master_that_does_not_say_is_never_treated_as_unstamped(in_a_test_session) -> None:
    """matrx-ai's fallback master record (media_persistence.py) carries no ``test_run_id``: it may be this run's own
    fresh file, so its variant is written under the session, never stripped of the run."""
    async def write() -> str | None:
        return test_stamp.current_test_run_id()

    partial = {"id": "m1", "owner_id": "u", "storage_uri": "s3://b/m1", "published_to_web": False}
    assert await write_variant_as_its_master(partial, write) == RUN
