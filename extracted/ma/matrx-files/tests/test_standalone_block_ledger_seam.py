"""Board row H8 — the standalone service refuses to boot with no Block Ledger.

Mirrors `tests/test_request_organization_seam.py`'s pattern for the
organization seam (the sibling outage this file's neighbour fixed): a source
check that `create_app()` actually calls the guard, plus a direct test of the
guard's two states. Before this file's production code existed, NEITHER of
these was true — `matrx_files.standalone.app` never imported `matrx_files.blocks`
at all, so a DRM wall, an unsupported format, an empty file, or a missing OCR
binary hit by that service became a silent no-op nobody could ever discover
short of noticing the Blocks screen had zero file-reader rows.
"""

from __future__ import annotations

from pathlib import Path

import pytest


def test_standalone_host_wires_the_block_ledger():
    source = (
        Path(__import__("matrx_files").__file__).parent / "standalone" / "app.py"
    ).read_text()
    assert "configure_block_ledger()" in source
    assert "_assert_block_ledger_seam()" in source


def test_boot_guard_refuses_a_host_with_no_block_sink(monkeypatch):
    from matrx_files.blocks.sink import BlockSinkNotConfigured
    from matrx_files.standalone import app as standalone_app
    from matrx_utils.block_sink import configure_block_sink

    configure_block_sink(None)
    try:
        with pytest.raises(BlockSinkNotConfigured, match="no block sink is configured"):
            standalone_app._assert_block_ledger_seam()
    finally:
        configure_block_sink(None)


def test_boot_guard_passes_once_a_sink_is_wired(monkeypatch):
    from matrx_files.blocks.sink import make_block_sink
    from matrx_files.blocks.testing import FakeBlockStore
    from matrx_files.standalone import app as standalone_app
    from matrx_utils.block_sink import configure_block_sink

    configure_block_sink(make_block_sink(FakeBlockStore()))
    try:
        standalone_app._assert_block_ledger_seam()  # does not raise
    finally:
        configure_block_sink(None)
