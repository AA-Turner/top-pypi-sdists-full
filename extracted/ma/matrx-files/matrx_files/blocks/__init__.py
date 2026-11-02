# File: matrx_files/blocks/__init__.py
"""This package's half of the platform Block Ledger. See `sink.py` for why it
exists (board row H8) and `record.py` for the write path.

Announce a wall from anywhere in matrx-files with
`matrx_utils.block_sink.announce_block(...)` — never call `record_block` here
directly from a reader; that would bind the reader to whichever store happens
to be configured. The sink is host-neutral by design.
"""

from __future__ import annotations

from matrx_files.blocks.sink import (
    BlockSinkNotConfigured,
    assert_block_sink_ready,
    configure_block_ledger,
    installed_block_store,
    make_block_sink,
)

__all__ = [
    "BlockSinkNotConfigured",
    "assert_block_sink_ready",
    "configure_block_ledger",
    "installed_block_store",
    "make_block_sink",
]
