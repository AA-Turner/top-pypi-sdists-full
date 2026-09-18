"""The boot self-test: announce a real block, prove it landed, take it back out.

H7's lesson is that "the sink is wired" is not the same claim as "a block lands". The wiring
was a one-line call in one host and nobody noticed for weeks that a whole hosted service could
not make it; a boolean saying `block_sink_configured()` would have been just as silent if the
table, the grant or the pool had been the thing that was wrong.

So this exercises the WHOLE seam the way an engine does — `announce_block()`, the detached
task, the configured sink, `record_block`'s dedupe and vocabulary, the store, the row — and
then asserts the row is really there by reading it back. It is run at startup by the hosted
scraper service and in CI by `tests/test_every_scraper_entrypoint_wires_the_block_sink.py`.

The probe row is removed again before this returns. It is not a finding, and an operator
reading the ledger to decide what to go and get should never see one row per container boot.
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from typing import Any

from matrx_utils.block_sink import announce_block

from matrx_scraper.blocks.sink import assert_block_sink_ready, installed_block_store
from matrx_scraper.blocks.store import BlockStore, OrmBlockStore

__all__ = ["BlockSinkSelfTestFailed", "self_test_block_ledger"]

_log = logging.getLogger("matrx_scraper.blocks")

#: The org every org-less platform capture belongs to (`matrx_orm.session.fallback`), which is
#: the right owner for a row about the health of the platform itself.
_SYSTEM_ORGANIZATION_ID = "39c38960-d30c-4840-b0c1-c9960de95582"

#: The probe's own error class. Deliberately not a real one: it has no lawful route, so even
#: if a row ever escaped cleanup it says plainly that it is a self-test and not a wall.
_SELF_TEST_ERROR_CLASS = "block_sink_self_test"


class BlockSinkSelfTestFailed(RuntimeError):
    """The sink is configured and a block still did not become a row."""


async def self_test_block_ledger(
    *,
    store: BlockStore | None = None,
    organization_id: str = _SYSTEM_ORGANIZATION_ID,
    timeout_seconds: float = 20.0,
) -> str:
    """Announce one block, wait for its row, delete it, return the row id it had.

    Raises `BlockSinkNotConfigured` when nothing is listening and
    :class:`BlockSinkSelfTestFailed` when something is listening and the row never appears.
    """
    assert_block_sink_ready()
    # Read back through the SAME seam the sink writes through, or this proves nothing: a
    # reader pointed at a different store could answer for a row the sink never wrote.
    reader: Any = store or installed_block_store() or OrmBlockStore()

    # Unique per run, so this never collides with a previous boot's probe through the dedupe
    # index and never counts a second occurrence onto a row somebody is looking at.
    input_ref = f"matrx-scraper://block-sink-self-test/{uuid.uuid4()}"

    announce_block(
        organization_id=organization_id,
        input_ref=input_ref,
        input_label="Block ledger self-test",
        source_type="web_page",
        engine="scraper",
        rung="http",
        error_class=_SELF_TEST_ERROR_CLASS,
        error_sentence=(
            "This is the scraper service proving at startup that a failed acquisition "
            "becomes a row. It is not a wall and nothing is wrong."
        ),
        detail={"self_test": True},
    )

    deadline = asyncio.get_running_loop().time() + timeout_seconds
    row = None
    while row is None:
        row = await reader.find_open(
            organization_id=organization_id,
            input_ref=input_ref,
            source_type="web_page",
            error_class=_SELF_TEST_ERROR_CLASS,
        )
        if row is not None:
            break
        if asyncio.get_running_loop().time() >= deadline:
            raise BlockSinkSelfTestFailed(
                "a block sink is configured, but an announced block did not become a row in "
                f"platform.acquisition_block within {timeout_seconds:.0f}s. Every acquisition "
                "failure this process causes is being lost. Check that the ONE database is "
                "bound and that this service's credentials may INSERT that table."
            )
        await asyncio.sleep(0.25)

    block_id = str(getattr(row, "id", "") or "")
    hard_delete = getattr(reader, "hard_delete", None)
    try:
        if hard_delete is not None:
            await hard_delete(block_id)
        else:
            from datetime import UTC, datetime

            await reader.update(block_id, deleted_at=datetime.now(UTC))
    except Exception:  # noqa: BLE001 — cleanup never fails a boot that already proved itself
        _log.warning(
            "block ledger self-test row %s could not be removed; it is soft evidence, not a "
            "finding, and can be deleted by hand",
            block_id,
        )
    return block_id
