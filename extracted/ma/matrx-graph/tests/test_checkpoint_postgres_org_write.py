"""Regression: PostgresCheckpointer writes carry the parent run's organization_id.

workflow.checkpoint.organization_id and workflow.node_outcome.organization_id
are both NOT NULL, and neither table has an independent org source — they are
CHILDREN of workflow.run. Before this fix, save_checkpoint()/record_outcome()
built their INSERT/UPSERT payloads with no organization_id at all. This test
mocks the host-injected WfCheckpoint/WfNodeOutcome/WfRun models and asserts
the row handed to create()/upsert() carries the parent run's organization_id,
resolved via `_organization_for_run`.
"""
from __future__ import annotations

import contextlib
import sys
import types
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

import pytest

from matrx_graph import knobs
from matrx_graph.checkpoint import postgres as module
from matrx_graph.checkpoint.protocol import Checkpoint, NodeOutcome


def _checkpoint(run_id: str) -> Checkpoint:
    return Checkpoint(
        checkpoint_id=str(uuid4()),
        run_id=run_id,
        thread_id=run_id,
        parent_checkpoint_id=str(uuid4()),
        step=1,
        channel_values={},
        next_invocations=[],
    )


def _outcome(run_id: str) -> NodeOutcome:
    return NodeOutcome(
        id=str(uuid4()),
        run_id=run_id,
        step=1,
        node_id="n1",
        attempt=1,
        dispatch_id="d1",
        item_index=0,
        output={},
        channel_writes=[],
        sends=[],
        duration_ms=0,
        source="executor",
        completed_at=datetime.now(UTC),
    )


class _FakeWfCheckpoint:
    def __init__(self) -> None:
        self.create_calls: list[dict[str, Any]] = []

    async def create(self, **kwargs: Any) -> None:
        self.create_calls.append(kwargs)

    async def insert_returning(self, data: dict[str, Any], **_kw: Any) -> dict[str, Any]:
        self.create_calls.append(data)
        return {"id": data["id"]}


class _FakeWfNodeOutcome:
    _fields: dict[str, Any] = {}

    def __init__(self) -> None:
        self.upsert_calls: list[dict[str, Any]] = []

    async def upsert(self, payload: dict[str, Any], **_kw: Any) -> None:
        self.upsert_calls.append(payload)


class _FakeWfRun:
    def __init__(self, org_by_run: dict[str, str | None]) -> None:
        self._org_by_run = org_by_run

    async def get_or_none(self, *, id: str) -> Any:  # noqa: A002
        org = self._org_by_run.get(id)
        if org is None:
            return None
        return types.SimpleNamespace(organization_id=org)

    def filter(self, *, id: str) -> _FakeRunQuery:  # noqa: A002
        return _FakeRunQuery()


class _FakeRunQuery:
    def returning(self, *_cols: str) -> _FakeRunQuery:
        return self

    async def update(self, **_kw: Any) -> None:
        return None


@pytest.fixture(autouse=True)
def _fast_knobs(monkeypatch: pytest.MonkeyPatch) -> None:
    policy = knobs.CheckpointWritePolicy(
        statement_timeout_ms=30_000, max_retries=0, retry_backoff_ms=1, warn_bytes=10_000_000
    )

    async def _policy() -> knobs.CheckpointWritePolicy:
        return policy

    monkeypatch.setattr(module, "checkpoint_write_policy", _policy)


@pytest.fixture
def wired(monkeypatch: pytest.MonkeyPatch):
    @contextlib.asynccontextmanager
    async def _transaction(*_a: Any, **_k: Any):
        yield None

    stub = types.ModuleType("matrx_orm")
    stub.transaction = _transaction  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "matrx_orm", stub)

    def _use(*, checkpoint=None, outcome=None, run=None):
        checkpoint = checkpoint or _FakeWfCheckpoint()
        outcome = outcome or _FakeWfNodeOutcome()
        run = run or _FakeWfRun({})

        def _get_model(key: str) -> Any:
            return {"WfCheckpoint": checkpoint, "WfNodeOutcome": outcome, "WfRun": run}[key]

        monkeypatch.setattr(module, "get_model", _get_model)
        return checkpoint, outcome, run

    return _use


@pytest.mark.asyncio
async def test_save_checkpoint_carries_parent_run_organization_id(wired):
    run_id = str(uuid4())
    org_id = str(uuid4())
    fake_run = _FakeWfRun({run_id: org_id})
    checkpoint_mgr, _, _ = wired(run=fake_run)

    await module.PostgresCheckpointer().save_checkpoint(_checkpoint(run_id))

    assert len(checkpoint_mgr.create_calls) == 1
    assert checkpoint_mgr.create_calls[0].get("organization_id") == org_id


@pytest.mark.asyncio
async def test_save_checkpoint_refuses_when_run_has_no_organization(wired):
    run_id = str(uuid4())
    fake_run = _FakeWfRun({run_id: None})
    checkpoint_mgr, _, _ = wired(run=fake_run)

    with pytest.raises(ValueError):
        await module.PostgresCheckpointer().save_checkpoint(_checkpoint(run_id))

    assert checkpoint_mgr.create_calls == []


@pytest.mark.asyncio
async def test_record_outcome_carries_parent_run_organization_id(wired):
    run_id = str(uuid4())
    org_id = str(uuid4())
    fake_run = _FakeWfRun({run_id: org_id})
    _, outcome_mgr, _ = wired(run=fake_run)

    await module.PostgresCheckpointer().record_outcome(_outcome(run_id))

    assert len(outcome_mgr.upsert_calls) == 1
    assert outcome_mgr.upsert_calls[0].get("organization_id") == org_id


@pytest.mark.asyncio
async def test_record_outcome_refuses_when_run_has_no_organization(wired):
    run_id = str(uuid4())
    fake_run = _FakeWfRun({run_id: None})
    _, outcome_mgr, _ = wired(run=fake_run)

    with pytest.raises(ValueError):
        await module.PostgresCheckpointer().record_outcome(_outcome(run_id))

    assert outcome_mgr.upsert_calls == []
