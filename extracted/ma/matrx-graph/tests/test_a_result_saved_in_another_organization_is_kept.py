"""A step set to run in another organization (``data.in_organization``) with ``data.once`` SAVES its result.

2026-10-28, runs 08bfe86c (``text.slug``) and f725c0f9 (``settings.read``): the member's run lived in
organization A, the step ran in organization B, and its result is keyed to B (a saved result never
crosses organizations). Settling wrote ``origin_run_id`` = the run in A onto the row in B, and the
database's same-organization rule (``platform.assert_same_org('origin_run_id', 'workflow.run')``)
refused it: ``IntegrityError``, nothing saved, every re-run paid again.

A row never points across organizations: when the producing run lives in another organization than
the saved result, the ``origin_run_id`` column stays empty and the origin rides in the row's
system-owned ``metadata`` — still read back, so the reuse resolves the origin run's held values.
"""

from __future__ import annotations

import dataclasses
import time
import uuid
from collections.abc import Iterator
from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_graph import Definition, MemoryCheckpointer, RunStatus, Scheduler, compile_graph
from matrx_graph.once import (
    MemoryStepResultStore,
    PostgresStepResultStore,
    StepResultKey,
    StoredResult,
    configure_step_result_store,
)
from tests._fixtures import FakeEmitter, make_app_context
from tests.test_in_organization import (  # the same real executor + admission seam
    ORG_MEMBER,
    ORG_RUN,
    PERSON,
    _once_in,
    _registry,
    _Where,
    admission,  # noqa: F401 — pytest fixture
)

RUN_IN_A = "44444444-4444-4444-8444-444444444444"
KEY_IN_B = StepResultKey(
    organization_id=ORG_MEMBER, scope="organization", scope_id=ORG_MEMBER, step_type="text.slug", result_key="k",
)


class _SameOrgModel:
    """``workflow.step_result`` with its same-organization trigger: ``origin_run_id`` may only name a
    run of the row's own organization."""

    RUN_ORGS = {RUN_IN_A: ORG_RUN}

    def __init__(self) -> None:
        self.row: dict[str, Any] = {"id": str(uuid.uuid4()), "organization_id": ORG_MEMBER, "claim_token": None}

    def filter(self, **_kw: Any) -> Any:
        row = self.row

        class _Q:
            async def values(self, *cols: str) -> list[dict[str, Any]]:
                return [{c: row.get(c) for c in cols}]

        return _Q()

    async def update_where(self, filters: dict[str, Any], **fields: Any) -> Any:
        if filters.get("claim_token") != self.row.get("claim_token"):
            return SimpleNamespace(rows_affected=0)
        origin = fields.get("origin_run_id")
        if origin is not None and self.RUN_ORGS.get(str(origin), self.row["organization_id"]) != self.row["organization_id"]:
            raise RuntimeError("IntegrityError: assert_same_org: step_result.origin_run_id points at another organization")
        self.row.update(fields)
        return SimpleNamespace(rows_affected=1)


def _result(**kw: Any) -> StoredResult:
    return StoredResult(
        input_digest="d", output={"slug": "a-b"}, output_kind=None, verdict={}, emissions={},
        origin_run_id=RUN_IN_A, origin_node_id="slug", origin_step=0, origin_dispatch_id="",
        origin_item_index=0, origin_attempt=1, succeeded_at=datetime.now(UTC), expires_at=None, **kw,
    )


async def test_a_result_produced_by_a_run_in_another_organization_is_saved_and_read_back() -> None:
    model = _SameOrgModel()
    model.row["claim_token"] = token = str(uuid.uuid4())
    store = PostgresStepResultStore()
    store._model = lambda: model  # type: ignore[method-assign]

    async def _intern(_run: str, output: dict[str, Any]) -> dict[str, Any]:
        return output

    store._intern_output = _intern  # type: ignore[method-assign]

    assert await store.settle(KEY_IN_B, token=token, result=_result(origin_organization_id=ORG_RUN))
    assert model.row["origin_run_id"] is None, "the row in B points at a run in A"
    back = await store.read(KEY_IN_B)
    assert back is not None and back.result is not None, "the saved result does not read back"
    assert back.result.origin_run_id == RUN_IN_A


async def test_a_same_organization_result_keeps_its_origin_column() -> None:
    model = _SameOrgModel()
    model.row["organization_id"] = ORG_RUN
    model.row["claim_token"] = token = str(uuid.uuid4())
    store = PostgresStepResultStore()
    store._model = lambda: model  # type: ignore[method-assign]

    async def _intern(_run: str, output: dict[str, Any]) -> dict[str, Any]:
        return output

    store._intern_output = _intern  # type: ignore[method-assign]
    key = dataclasses.replace(KEY_IN_B, organization_id=ORG_RUN, scope_id=ORG_RUN)
    assert await store.settle(key, token=token, result=_result(origin_organization_id=ORG_RUN))
    assert model.row["origin_run_id"] == RUN_IN_A


@pytest.fixture
def once_store() -> Iterator[MemoryStepResultStore]:
    from matrx_graph import knobs

    s = MemoryStepResultStore()
    configure_step_result_store(s)
    knobs._cache[knobs.ONCE_FEATURE] = (
        time.monotonic() + 10**9,
        {"lease_seconds": 5, "wait_poll_seconds": 1, "keep_days_default": 30, "miss_compare_limit": 10},
    )
    try:
        yield s
    finally:
        configure_step_result_store(None)
        knobs._cache.pop(knobs.ONCE_FEATURE, None)


async def test_the_engine_says_which_organization_the_producing_run_lives_in(admission, once_store):  # noqa: F811
    step = _Where("test.where")
    reg = _registry(step)
    graph = compile_graph(Definition.model_validate(_once_in({"organization_id": ORG_MEMBER}, {"text": "q"}, shared=True)), registry=reg)
    app = dataclasses.replace(make_app_context(FakeEmitter()), organization_id=ORG_RUN, user_id=PERSON)
    result = await Scheduler(graph, MemoryCheckpointer(), app, registry=reg).run(run_id=f"run-{uuid.uuid4().hex[:8]}")
    assert result.status is RunStatus.COMPLETED, result.error
    saved = [(k, row.result) for k, row in once_store.rows().items() if row.result is not None]
    assert len(saved) == 1
    key, stored = saved[0]
    assert key.organization_id == ORG_MEMBER
    assert stored.origin_organization_id == ORG_RUN
