"""A worker never claims — and never errors — a run whose graph needs a node type it lacks.

Every server shares one database (2026-10-12): a run started on a newer local build
(``brand.setup.land_logo``) was claimed by a deployed worker and errored with
"Unknown node type". These tests pin the three halves of the fix:

1. ``claim_one(capabilities=...)`` filters on the job's stamped requirement, and the
   filter's SQL semantics are right (contained → claimable; missing → not; nothing
   stamped → claimable, the pre-capability behavior).
2. A job runner that discovers the gap at run time (``JobNeedsCapability``) hands the
   job back — no ``fail``, no ``complete``, no spent attempt — and marks the run waiting.
3. ``required_node_types`` canonicalises legacy spellings and never requires a removed
   node type (such a run must fail with its removal message, not wait forever).
"""

from __future__ import annotations

import json
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest

from matrx_graph.workers import capability as cap
from matrx_graph.workers import queue as queue_module
from matrx_graph.workers import runner as runner_module
from matrx_graph.workers.queue import Job


class _CapturingJobModel:
    def __init__(self) -> None:
        self.kwargs: dict[str, Any] = {}

    async def claim_batch(self, **kwargs: Any) -> list[dict[str, Any]]:
        self.kwargs = kwargs
        return []


class _RunModel:
    def filter(self, *args: Any, **kwargs: Any) -> Any:
        return SimpleNamespace(args=args, kwargs=kwargs)


@pytest.fixture
def captured(monkeypatch: pytest.MonkeyPatch) -> _CapturingJobModel:
    from matrx_graph.db import _registry

    job_model = _CapturingJobModel()
    run_model = _RunModel()
    monkeypatch.setattr(
        _registry, "get_model", lambda name: job_model if name == "WfJob" else run_model
    )
    return job_model


async def test_claim_carries_the_capability_filter(captured: _CapturingJobModel) -> None:
    await queue_module.claim_one(capabilities=["io.user_input", "ai.agent.start"])
    predicate = captured.kwargs["predicate"]
    # The capability leg is the right-hand side of the AND the claim builds.
    leg = getattr(predicate, "right", None) or predicate.children[-1]
    params: list[Any] = []
    sql = leg.as_sql(params)
    assert "j.metadata" in sql and "<@" in sql and "COALESCE" in sql, sql
    assert params[0] == cap.REQUIRED_NODE_TYPES_KEY
    assert json.loads(params[-1]) == ["ai.agent.start", "io.user_input"]


def _leaves(predicate: Any) -> list[Any]:
    children = getattr(predicate, "children", None)
    if not children:
        return [predicate]
    return [leaf for child in children for leaf in _leaves(child)]


async def test_claim_without_capabilities_is_unfiltered(captured: _CapturingJobModel) -> None:
    from matrx_orm import JsonbContainedBy

    await queue_module.claim_one()
    assert not any(isinstance(p, JsonbContainedBy) for p in _leaves(captured.kwargs["predicate"]))


def test_capability_predicate_sql_shape() -> None:
    params: list[Any] = []
    sql = cap.capability_predicate(["b", "a", "a"], metadata_column="j.metadata").as_sql(params)
    assert sql == "COALESCE((j.metadata -> $1), '[]'::jsonb) <@ $2::jsonb"
    assert params == ["required_node_types", json.dumps(["a", "b"])]


async def _live_contained(required: Any, caps: list[str]) -> bool:
    """Evaluate the REAL predicate SQL in Postgres against a literal metadata row."""
    from matrx_graph.db.pool import acquire

    params: list[Any] = []
    metadata = {} if required is None else {"required_node_types": required}
    params.append(json.dumps(metadata))
    clause = cap.capability_predicate(caps, metadata_column="x.metadata").as_sql(params)
    async with acquire() as conn:
        return bool(await conn.fetchval(f"SELECT {clause} FROM (SELECT $1::jsonb AS metadata) x", *params))


async def test_capability_semantics_in_postgres() -> None:
    try:
        from matrx_graph.db.pool import acquire

        async with acquire() as conn:
            await conn.fetchval("SELECT 1")
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"no database for the live predicate check: {exc}")
    prod = ["io.user_input", "ai.agent.start", "brand.discovery.curate_stage"]
    assert await _live_contained(["io.user_input"], prod) is True
    assert await _live_contained(["io.user_input", "brand.setup.land_logo"], prod) is False
    assert await _live_contained([], prod) is True
    assert await _live_contained(None, prod) is True  # nothing stamped → anyone may claim


async def test_runner_hands_back_a_job_it_cannot_run(monkeypatch: pytest.MonkeyPatch) -> None:
    run_id, job_id = str(uuid4()), str(uuid4())
    calls: dict[str, Any] = {}

    async def _claim_one(**kwargs: Any) -> Job:
        calls["claim_kwargs"] = kwargs
        return Job(job_id=job_id, run_id=run_id, kind="resume", attempt=1, claimed_by="w:1")

    async def _never(*_a: Any, **_k: Any) -> None:
        raise AssertionError("an incapable worker must neither fail nor complete the job")

    async def _defer(jid: str, *, required_node_types: list[str], claimed_by: str | None) -> None:
        calls["defer"] = (jid, required_node_types, claimed_by)

    async def _mark(rid: str, *, missing: list[str], worker_id: str) -> None:
        calls["mark"] = (rid, list(missing))

    async def _runner(job: Job, app: Any) -> None:
        raise cap.JobNeedsCapability(
            required=["io.user_input", "brand.setup.land_logo"], missing=["brand.setup.land_logo"]
        )

    async def _app(job: Job) -> Any:
        return object()

    monkeypatch.setattr(runner_module, "claim_one", _claim_one)
    monkeypatch.setattr(runner_module, "fail", _never)
    monkeypatch.setattr(runner_module, "complete", _never)
    monkeypatch.setattr(runner_module, "defer_for_capability", _defer)
    monkeypatch.setattr(runner_module, "mark_run_awaiting_capability", _mark)

    assert await runner_module.run_single_job(_runner, _app) is True
    assert calls["claim_kwargs"].get("capabilities") is not None  # always filtered
    assert calls["defer"] == (job_id, ["brand.setup.land_logo", "io.user_input"], "w:1")
    assert calls["mark"] == (run_id, ["brand.setup.land_logo"])


def test_required_node_types_canonicalises_and_skips_removed() -> None:
    from matrx_graph.validation import REMOVED_NODE_TYPES

    removed = next(iter(REMOVED_NODE_TYPES))
    nodes = [
        SimpleNamespace(spec_type="action.ai.agent.start"),
        SimpleNamespace(spec_type="ai.agent.start"),
        SimpleNamespace(spec_type="brand.setup.land_logo"),
        SimpleNamespace(spec_type=removed),
    ]
    assert cap.required_node_types(SimpleNamespace(nodes=nodes)) == [
        "ai.agent.start",
        "brand.setup.land_logo",
    ]


def test_missing_node_types_reads_the_registry() -> None:
    from matrx_graph.executor.registry import NodeRegistry

    reg = NodeRegistry()
    reg._executors["io.user_input"] = object()  # type: ignore[assignment]
    assert cap.missing_node_types(["io.user_input", "brand.setup.land_logo"], reg) == [
        "brand.setup.land_logo"
    ]
