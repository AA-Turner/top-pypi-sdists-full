# File: matrx_files/blocks/tests/test_sink.py
"""Board row H8 — the sink is host-neutral, deferential, and refuses to boot
a process that never wired one.

Before `matrx_files.blocks` existed, `matrx_files.standalone.app` never
called `configure_block_sink()` at all, so `assert_block_sink_ready()` would
have raised on every boot of that service — these tests pin both the
"nobody configured me" failure and the "I am configured, and deferential to
a richer host sink" success, the same two states H7 pinned for
`matrx_scraper.blocks.sink`.
"""

from __future__ import annotations

import pytest

from matrx_files.blocks.sink import (
    BlockSinkNotConfigured,
    assert_block_sink_ready,
    configure_block_ledger,
    installed_block_store,
    make_block_sink,
)
from matrx_files.blocks.testing import FakeBlockStore
from matrx_utils.block_sink import configure_block_sink, current_block_sink

pytestmark = pytest.mark.asyncio


@pytest.fixture(autouse=True)
def _reset_sink():
    configure_block_sink(None)
    yield
    configure_block_sink(None)


async def test_assert_block_sink_ready_refuses_an_unwired_process():
    with pytest.raises(BlockSinkNotConfigured):
        assert_block_sink_ready()


async def test_configure_block_ledger_wires_a_sink_and_ready_stops_refusing():
    installed = configure_block_ledger(store=FakeBlockStore())

    assert installed is True
    assert_block_sink_ready()  # does not raise


async def test_configure_block_ledger_is_deferential_to_an_existing_sink():
    richer_store = FakeBlockStore()
    configure_block_sink(make_block_sink(richer_store))

    installed = configure_block_ledger(store=FakeBlockStore())

    assert installed is False
    assert installed_block_store() is richer_store


async def test_configure_block_ledger_force_overrides_an_existing_sink():
    configure_block_sink(make_block_sink(FakeBlockStore()))
    new_store = FakeBlockStore()

    installed = configure_block_ledger(store=new_store, force=True)

    assert installed is True
    assert installed_block_store() is new_store


async def test_announce_block_reaches_this_packages_store_end_to_end():
    from matrx_utils.block_sink import announce_block

    store = FakeBlockStore()
    configure_block_ledger(store=store)

    announce_block(
        organization_id="org-1",
        input_ref="file-123",
        source_type="file",
        engine="file_reader",
        error_class="ocr_binary_missing",
        error_sentence="Tesseract is not installed on this host",
    )

    # announce_block fires a detached task; poll briefly rather than assuming
    # one tick is enough (flake-proof against scheduler timing).
    import asyncio

    for _ in range(50):
        if store.rows:
            break
        await asyncio.sleep(0.01)

    assert len(store.rows) == 1
    row = next(iter(store.rows.values()))
    assert row.error_class == "ocr_binary_missing"
    assert row.organization_id == "org-1"
