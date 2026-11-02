# File: matrx_files/blocks/tests/test_record_and_sink.py
"""Board row H8 — the write path exists at all, and behaves the way the
platform-wide contract requires.

Every test here is a proof against `matrx_files.blocks.testing.FakeBlockStore`
(no database needed), mirroring the same three rules H7 proved for
`matrx_scraper.blocks.record`: an org-less block is refused and logged, never
silently written; a repeat is a count, not a duplicate; a genuine race on the
unique index is read back as the winner, not a crash.
"""

from __future__ import annotations

import pytest

from matrx_files.blocks.record import record_block
from matrx_files.blocks.testing import FakeBlockStore

pytestmark = pytest.mark.asyncio


async def test_a_block_with_no_organization_is_refused_not_written():
    store = FakeBlockStore()

    result = await record_block(
        organization_id=None,
        input_ref="file-123",
        error_class="drm_protected",
        error_sentence="This file is protected.",
        store=store,
    )

    assert result is None
    assert store.rows == {}


async def test_an_unknown_error_class_is_refused_not_written():
    store = FakeBlockStore()

    result = await record_block(
        organization_id="org-1",
        input_ref="file-123",
        error_class="not_a_real_error_class",
        error_sentence="whatever",
        store=store,
    )

    assert result is None
    assert store.rows == {}


async def test_a_first_block_is_created_with_the_lawful_route():
    store = FakeBlockStore()

    block_id = await record_block(
        organization_id="org-1",
        input_ref="file-123",
        input_label="My Book.epub",
        error_class="drm_protected",
        error_sentence="This file is protected by Adobe DRM.",
        store=store,
    )

    assert block_id is not None
    row = store.rows[block_id]
    assert row.organization_id == "org-1"
    assert row.engine == "file_reader"
    assert row.source_type == "file"
    assert row.occurrence_count == 1
    assert row.status == "decision"  # drm_protected is a decision route
    assert row.lawful_route == "decision"
    assert "DRM-free copy" in row.unblock_note


async def test_a_repeat_is_a_count_not_a_second_row():
    store = FakeBlockStore()

    first_id = await record_block(
        organization_id="org-1",
        input_ref="file-123",
        error_class="empty_file",
        error_sentence="no readable text",
        store=store,
    )
    second_id = await record_block(
        organization_id="org-1",
        input_ref="file-123",
        error_class="empty_file",
        error_sentence="no readable text (again)",
        store=store,
    )

    assert first_id == second_id
    assert len(store.rows) == 1
    assert store.rows[first_id].occurrence_count == 2


async def test_a_genuine_race_on_the_unique_index_is_read_back_as_the_winner():
    store = FakeBlockStore()
    # Simulate a concurrent caller that already won the race for this exact
    # (org, source_type, error_class, input_ref) key.
    winner_id = await record_block(
        organization_id="org-1",
        input_ref="file-123",
        error_class="unsupported_format",
        error_sentence="cannot decode",
        store=store,
    )
    store.raise_conflict_once = True

    block_id = await record_block(
        organization_id="org-1",
        input_ref="file-123",
        error_class="unsupported_format",
        error_sentence="cannot decode (second caller)",
        store=store,
    )

    # The "loser" of the race still gets a row id back — the winner's — never
    # an exception. THE ONE RULE: recording a block never raises into the
    # read path that hit the wall.
    assert block_id == winner_id
    assert store.rows[block_id].occurrence_count == 2


async def test_recording_never_raises_even_when_the_store_is_broken():
    class ExplodingStore:
        async def find_open(self, **kwargs):
            raise RuntimeError("the database fell over")

    result = await record_block(
        organization_id="org-1",
        input_ref="file-123",
        error_class="unsupported_format",
        error_sentence="cannot decode",
        store=ExplodingStore(),
    )

    assert result is None
