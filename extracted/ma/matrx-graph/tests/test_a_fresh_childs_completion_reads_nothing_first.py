"""A called child's completion, when its leg created the row, writes without reading the row first (P8-RUNS).

A completion MERGES its output into the row and sizes the merge against what the row already holds
(``_output_by_reference``), so it read ``workflow.run.output`` before the terminal UPDATE — one more round trip on
the critical path of every Run Workflow call, though a leg that created the child row and ran it to its end
without a park KNOWS the row holds no output. ``apply_result(prior_output={})`` says so: zero reads, one write.
A caller that does not know (a resumed leg, a worker's own run) still reads.
Red before: 1 read of the output column with ``prior_output={}`` (the parameter did not exist).
"""

from __future__ import annotations

import types
from typing import Any

import pytest

from matrx_graph.checkpoint import value_store
from matrx_graph.db import run_store as module
from matrx_graph.db.run_store import RunStore
from matrx_graph.types.primitives import RunStatus

pytestmark = pytest.mark.asyncio

RUN = "22222222-2222-4222-8222-222222222222"


class _Query:
    def __init__(self, log: list[str]) -> None:
        self.log = log

    async def values(self, *cols: Any) -> list[dict[str, Any]]:
        self.log.append("read:" + ",".join(str(c) for c in cols))
        return [{"output": None, "status": "running", "error": None}]


class _WfRun:
    def __init__(self, log: list[str]) -> None:
        self.log = log

    def filter(self, *_a: Any, **_k: Any) -> _Query:
        return _Query(self.log)

    async def update_where(self, filters: dict[str, Any], **updates: Any) -> Any:
        self.log.append("write:" + str(updates.get("status")))
        return types.SimpleNamespace(rows_affected=1, updated_rows=[])


@pytest.fixture
def log(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    entries: list[str] = []
    model = _WfRun(entries)
    monkeypatch.setattr(module, "get_model", lambda _key: model)

    async def _limit() -> int:
        return 1_000_000

    async def _by_reference(_run_id: str, output: Any, **_k: Any) -> Any:
        return output

    async def _settled(*_a: Any, **_k: Any) -> None:
        return None

    monkeypatch.setattr(value_store, "run_output_limit", _limit)
    monkeypatch.setattr(value_store, "output_by_reference", _by_reference)
    monkeypatch.setattr(module, "_announce_settled", _settled)
    return entries


async def _complete(**extra: Any) -> bool:
    return await RunStore().apply_result(
        RUN, status=RunStatus.COMPLETED, steps_executed=3, output={"result": {"answer": 1}},
        interrupt=None, error=None, last_checkpoint_id=None, **extra,
    )


async def test_a_leg_that_knows_the_row_is_empty_completes_in_one_write(log: list[str]) -> None:
    assert await _complete(prior_output={})
    assert log == ["write:completed"], log


async def test_a_leg_that_does_not_know_still_reads_what_the_row_holds(log: list[str]) -> None:
    assert await _complete()
    assert log == ["read:output", "write:completed"], log
