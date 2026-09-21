"""Wiring the Block Ledger into whatever process this package is running in.

🚨 **THE DEFECT THIS EXISTS TO CLOSE (board row H7).** `matrx_utils.block_sink.announce_block`
is a documented no-op until a host calls `configure_block_sink()`, and for the ledger's first
weeks that call happened in exactly ONE place: `aidream/package_integration.py`, which runs
only inside aidream's monolith boot. The hosted scraper service
(`scraper.app.matrxserver.com`) is built from `packages/matrx-scraper/Dockerfile`, which
installs `packages/` and deliberately NOT aidream — so it could never make that call. The
consequence was measured live: the same login wall recorded a row when it was hit in-process
inside aidream and recorded NOTHING when the identical wall was hit through the hosted
service's `/scraper/batch`.

The class fix is that the sink is configured by the PACKAGE'S OWN startup rather than by one
host's: :func:`configure_block_ledger` is called from `matrx_scraper.db.web` on BOTH database
binding paths (standalone `bootstrap_web_db` and hosted `bind_web_to_host`), so every
entrypoint of matrx-scraper that has a database has a ledger, and a new entrypoint cannot
forget to wire one.

**The transport is the database, not HTTP, and that is not a preference.** Every other durable
write this service makes — `web.*`, `scraper.*`, the canonical file rows, and
`matrx_orm.record_error`'s `system_error` capture wired one line away in the same lifespan —
goes straight to the ONE database with the service's own `SUPABASE_MATRIX_*` credentials.
There is no outbound call from the scraper service to aidream anywhere in this codebase; the
arrow points the other way (aidream calls the scraper through `MATRX_SCRAPER_URL`). Posting
blocks to an aidream `/blocks` intake would mean inventing a credential, an auth surface and a
new failure mode (aidream unreachable = the finding is lost) for a row this process can
already write correctly.

**Whose organization.** A package never knows what an organization is. The host's request
context does, and both hosts carry the SAME one — `matrx_connect.context.app_context`, which
`aidream.context.app_context` merely re-exports. So the org is READ off the carried context
and never resolved from a personal, system or parent default
(`common-docs/policies/context-is-carried-never-rebuilt.md`). A block that arrives with no
organization is refused with a logged sentence, which is `record_block`'s decision, not this
module's.
"""

from __future__ import annotations

import logging
from typing import Any

from matrx_utils.block_sink import (
    block_sink_configured,
    configure_block_sink,
    current_block_sink,
)

from matrx_scraper.blocks.record import record_block
from matrx_scraper.blocks.store import BlockStore, OrmBlockStore

__all__ = [
    "BlockSinkNotConfigured",
    "assert_block_sink_ready",
    "carried_organization_id",
    "configure_block_ledger",
    "installed_block_store",
    "make_block_sink",
]

_log = logging.getLogger("matrx_scraper.blocks")


class BlockSinkNotConfigured(RuntimeError):
    """Raised by :func:`assert_block_sink_ready` at a door that must not open without one."""


def carried_organization_id() -> str | None:
    """The organization on the context this work is already running inside, or None.

    Never resolves a default. No context is a normal answer here (a CLI, a worker, a test),
    not an error — the caller that passes an explicit `organization_id` always wins.

    🚨 **Dead for any caller reached through `matrx_utils.block_sink.announce_block`.**
    `announce_block` runs the sink inside `detached_task`, which deliberately runs in a
    FRESH `contextvars.Context` with no inherited state (found 2026-09-19 while wiring
    board row H8's sibling in `matrx_files/blocks/sink.py`) — so by the time THIS function
    runs, the caller's ambient AppContext is already gone and this always answers `None`.
    Every real caller of `announce_block` in this codebase already passes `organization_id`
    explicitly (`matrx_scraper.orchestrator._announce_the_wall`) for exactly this reason.
    This function still matters for a caller that reaches `record_block`/the sink directly,
    outside `announce_block`'s detach — but never assume it will see a caller's context
    through the `announce_block` door.
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
    """The `matrx_utils.block_sink` implementation, over the table access a host injects.

    A package announces with the same field names the ledger records, so this is a pass
    through and never a translation layer that could disagree with the direct callers.
    """

    async def sink(**fields: Any) -> None:
        if not fields.get("organization_id"):
            fields["organization_id"] = carried_organization_id()
        await record_block(**fields, store=store)

    # Carried ON the sink, never in a second global: a reader (the boot self-test) must read
    # back through the same seam that wrote, and whoever restores the sink restores this too.
    sink.block_store = store  # type: ignore[attr-defined]
    return sink


def configure_block_ledger(*, store: BlockStore | None = None, force: bool = False) -> bool:
    """Install this package's block sink. Returns True when this call is the one that did.

    Idempotent and deferential: a host that already wired a richer sink of its own (aidream
    writes through its generated manager and its own cache/DTO layer) keeps it, because both
    sinks land the same row in the same table and the host's is the one its own tests cover.
    `force=True` is for tests that need this exact sink.
    """
    if block_sink_configured() and not force:
        return False
    configure_block_sink(make_block_sink(store or OrmBlockStore()))
    _log.info("block ledger wired: acquisition failures in this process become rows")
    return True


def installed_block_store() -> BlockStore | None:
    """The store the CURRENTLY installed sink writes through, or None when a host wired its own.

    aidream's sink is built by the same `make_block_sink`, so in the monolith this answers
    aidream's manager-backed store — which is exactly what a self-test there should read.
    """
    return getattr(current_block_sink(), "block_store", None)


def assert_block_sink_ready() -> None:
    """Refuse to open a door that would swallow findings.

    This is the guard H7 asked for: an entrypoint of matrx-scraper that can hit a wall and has
    no sink is not a degraded service, it is a service that throws away the deliverable — and
    it did so silently for weeks. Loud at the door beats invisible for a month.
    """
    if not block_sink_configured():
        raise BlockSinkNotConfigured(
            "no block sink is configured, so every acquisition failure this process causes "
            "would be a silent no-op for the Block Ledger. matrx_scraper.db.web's binding "
            "functions install one; this process reached its door without calling either."
        )
