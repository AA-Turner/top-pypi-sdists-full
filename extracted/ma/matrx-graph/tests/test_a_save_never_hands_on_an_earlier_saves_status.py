"""A checkpoint save hands the next boundary ONLY the status it read itself.

``_remember_run_status`` is set by a save's successful write. A save that ends on the
timed-out-but-landed path (the attempt committed, the client stopped waiting) writes no
status — and the entry an EARLIER save left (a park or final save nobody popped) used to
survive, so the next boundary took that stale status as its pause/cancel poll. Red before
the fix: ``pop_run_status`` returned the earlier save's ``running`` after a landed save.
"""

from __future__ import annotations

import types
from typing import Any

import pytest

from matrx_graph import knobs
from matrx_graph.checkpoint import postgres as module
from matrx_graph.checkpoint.protocol import Checkpoint

pytestmark = pytest.mark.asyncio

RUN = "33333333-3333-3333-3333-333333333333"


class QueryTimeoutError(Exception):
    """Named like matrx-orm's: retryable by class name."""


async def test_a_landed_but_timed_out_save_leaves_no_stale_status(monkeypatch: pytest.MonkeyPatch) -> None:
    policy = knobs.CheckpointWritePolicy(
        statement_timeout_ms=30_000, max_retries=0, retry_backoff_ms=1, warn_bytes=10_000_000,
        inline_value_max_bytes=4096,
    )

    async def _policy() -> knobs.CheckpointWritePolicy:
        return policy

    async def _timed_out(*_a: Any, **_k: Any) -> None:
        raise QueryTimeoutError("canceling statement due to statement timeout")

    async def _landed(*_a: Any, **_k: Any) -> bool:
        return True

    monkeypatch.setattr(module, "checkpoint_write_policy", _policy)
    monkeypatch.setattr(module, "_value_store_available", lambda: False)
    monkeypatch.setattr(module.PostgresCheckpointer, "_write_checkpoint_once", _timed_out)
    monkeypatch.setattr(module.PostgresCheckpointer, "_checkpoint_landed", _landed)

    # An earlier save (a park, the final save) read 'running' and nobody took it.
    module._remember_run_status(RUN, types.SimpleNamespace(updated_rows=[{"status": "running"}]))

    checkpointer = module.PostgresCheckpointer()
    await checkpointer.save_checkpoint(
        Checkpoint(checkpoint_id="44444444-4444-4444-4444-444444444444", run_id=RUN, thread_id=RUN,
                   step=2, channel_values={})
    )

    assert checkpointer.pop_run_status(RUN) is None, (
        "a save that read no status handed the next boundary an EARLIER save's status — "
        "a pause/cancel requested since then is missed"
    )
