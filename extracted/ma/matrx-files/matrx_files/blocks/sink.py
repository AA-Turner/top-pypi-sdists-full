# File: matrx_files/blocks/sink.py
"""Wiring this package's half of the Block Ledger into whatever process runs it.

🚨 **THE DEFECT THIS CLOSES (board row H8).** `matrx_utils.block_sink.announce_block`
is a documented no-op until a host calls `configure_block_sink()`. Every file
reader in this package raises `ProtectedEbookError` / an unsupported-format
error / an empty-file error / a missing-OCR-binary error, and until this
module existed NOTHING in matrx-files ever called `announce_block` at all —
so the standalone `matrx_files.standalone.app` service (which cannot import
`matrx_scraper` and therefore cannot use its sink) announced every one of
those walls into a documented no-op it never wired in the first place.

Hosted-in-aidream, this sink is DEFERENTIAL exactly like matrx-scraper's:
aidream wires its own richer sink (`aidream/services/block_ledger/`) at boot,
before this package's own `configure_block_ledger()` gets a chance to run, so
`configure_block_ledger()` here backs off and never overwrites it. Standalone,
this IS the sink, and `matrx_files.standalone.app` refuses to boot without it
— same posture as the organization seam (`_assert_organization_seam`, the
2026-09-19 outage this module's neighbour fixed).
"""

from __future__ import annotations

import logging
from typing import Any

from matrx_utils.block_sink import (
    block_sink_configured,
    configure_block_sink,
    current_block_sink,
)

from matrx_files.blocks.record import record_block
from matrx_files.blocks.store import BlockStore, OrmBlockStore

__all__ = [
    "BlockSinkNotConfigured",
    "assert_block_sink_ready",
    "carried_organization_id",
    "configure_block_ledger",
    "installed_block_store",
    "make_block_sink",
]

_log = logging.getLogger("matrx_files.blocks")


class BlockSinkNotConfigured(RuntimeError):
    """Raised by :func:`assert_block_sink_ready` at a door that must not open without one."""


def carried_organization_id() -> str | None:
    """The organization on the context this work is already running inside, or None.

    Never resolves a default. No context is a normal answer here (a CLI, a
    worker, a test), not an error — an explicit `organization_id` from the
    caller always wins.

    🚨 **Dead for any caller reached through `matrx_utils.block_sink.announce_block`**
    — see `matrx_scraper.blocks.sink.carried_organization_id`'s docstring for
    the full finding (`detached_task` runs the sink in a context-stripped
    task, so this always answers `None` there). ALWAYS resolve
    `matrx_utils.ctx.get_active_organization_id()` synchronously in the
    caller and pass it as an explicit `organization_id=` field to
    `announce_block` — see `specific_handlers/pdf/analyze/text_extraction.py`'s
    OCR-binary-missing announcement for the pattern.
    """
    try:
        from matrx_connect.context.app_context import try_get_app_context

        ctx = try_get_app_context()
    except Exception:  # noqa: BLE001 — no context is an answer, not a failure
        return None
    if ctx is None:
        return None
    return str(getattr(ctx, "organization_id", "") or "") or None


def make_block_sink(store: BlockStore) -> Any:
    """The `matrx_utils.block_sink` implementation, over the table access a host injects."""

    async def sink(**fields: Any) -> None:
        if not fields.get("organization_id"):
            fields["organization_id"] = carried_organization_id()
        await record_block(**fields, store=store)

    # Carried ON the sink, never in a second global — mirrors
    # `matrx_scraper.blocks.sink.make_block_sink`.
    sink.block_store = store  # type: ignore[attr-defined]
    return sink


def configure_block_ledger(*, store: BlockStore | None = None, force: bool = False) -> bool:
    """Install this package's block sink. Returns True when this call is the one that did.

    Idempotent and deferential: a host that already wired a richer sink of
    its own (aidream, or matrx-scraper when both packages share a process)
    keeps it, because both sinks land the same row in the same table.
    `force=True` is for tests that need this exact sink.
    """
    if block_sink_configured() and not force:
        return False
    configure_block_sink(make_block_sink(store or OrmBlockStore()))
    _log.info("matrx-files block ledger wired: file-reader walls in this process become rows")
    return True


def installed_block_store() -> BlockStore | None:
    """The store the CURRENTLY installed sink writes through, or None when a host wired its own."""
    return getattr(current_block_sink(), "block_store", None)


def assert_block_sink_ready() -> None:
    """Refuse to open a door that would swallow findings.

    A process of this package that can hit a wall and has no sink is not a
    degraded service, it is a service that throws away the deliverable —
    exactly what H7 found for the hosted scraper, one layer earlier.
    """
    if not block_sink_configured():
        raise BlockSinkNotConfigured(
            "no block sink is configured, so every file-reader wall this process "
            "hits would be a silent no-op for the Block Ledger. "
            "matrx_files.standalone.app calls configure_block_ledger() at boot; a "
            "process that reached this assertion skipped that call."
        )
