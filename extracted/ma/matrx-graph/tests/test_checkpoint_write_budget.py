"""Saving a run's progress survives a timeout, and fails HONESTLY when it can't.

THE LIVE FAILURE: run ``053e8b72-be54-4775-960f-c180c8b0e0d2`` (2026-09-12
21:27:39Z) died on one ``QueryTimeoutError`` writing its step-3
``workflow.checkpoint`` row — 1.1 MB, because the ``n_map`` fan-out stores every
item's full ``document`` input inline in ``next_invocations`` (measured live:
1,139,492 / 1,008,191 / 1,239,200 bytes on the same step of three sibling runs,
each written in 2-3s). The write had no retry and no ceiling of its own; the
pool's 10s ``command_timeout`` was the whole budget, and three paid-for node
outcomes were lost with nothing recoverable.
"""

from __future__ import annotations

import contextlib
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

import pytest

from matrx_graph import knobs
from matrx_graph.checkpoint import postgres as module
from matrx_graph.checkpoint.protocol import Checkpoint, NextInvocation
from matrx_graph.errors import CheckpointWriteFailedError
from matrx_graph.failure import Cause, failure_from_exception


class _QueryTimeoutError(Exception):
    __module__ = "matrx_orm.exceptions"


_QueryTimeoutError.__name__ = "QueryTimeoutError"


def _big_checkpoint(run_id: str, *, items: int = 4) -> Checkpoint:
    document = "LABEL: DOCUMENT 1 — First Amended Complaint … " + ("legal text " * 400)
    return Checkpoint(
        checkpoint_id=str(uuid4()),
        run_id=run_id,
        thread_id=run_id,
        parent_checkpoint_id=str(uuid4()),
        step=3,
        channel_values={},
        next_invocations=[
            NextInvocation(
                node_id="n_doc_ledger", inputs={"form": "Analysis", "document": document}
            )
            for _ in range(items)
        ],
    )


class _FakeModels:
    """The two host-injected models the checkpointer touches."""

    def __init__(self, *, fail_times: int, land_on_failure: bool = False) -> None:
        self.fail_times = fail_times
        self.land_on_failure = land_on_failure
        self.create_calls: list[dict[str, Any]] = []
        self.rows: dict[str, dict[str, Any]] = {}
        self.run_updates: list[dict[str, Any]] = []

    # --- WfCheckpoint -------------------------------------------------
    async def create(self, **kwargs: Any) -> None:
        self.create_calls.append(kwargs)
        if len(self.create_calls) <= self.fail_times:
            if self.land_on_failure:
                # The write committed; asyncpg gave up before hearing so.
                self.rows[str(kwargs["id"])] = kwargs
            raise _QueryTimeoutError("Query timed out during execute_query\n  Args: (…)")
        self.rows[str(kwargs["id"])] = kwargs

    async def insert_returning(
        self, data: dict[str, Any], *, returning: Any, statement_timeout: float | None = None
    ) -> dict[str, Any]:
        await self.create(**data, statement_timeout=statement_timeout)
        return {"id": data["id"]}

    def filter(self, **kwargs: Any) -> _FakeModels:
        self._filter = kwargs
        return self

    async def values(self, *columns: str) -> list[dict[str, Any]]:
        row_id = str(self._filter.get("id"))
        return [{"id": row_id}] if row_id in self.rows else []

    # --- WfRun --------------------------------------------------------
    def returning(self, *columns: str) -> _FakeModels:
        # The run row is never handed back whole (multi-MB on a child seeded with a large input).
        assert "*" not in columns and columns, columns
        return self

    async def update(self, **values: Any) -> None:
        self.run_updates.append({**self._filter, **values})

    async def get_or_none(self, *, id: str) -> Any:  # noqa: A002
        # Every write in this suite is a child of a run that carries an
        # organization — _organization_for_run() reads this to stamp it.
        import types

        return types.SimpleNamespace(organization_id="test-org-" + str(id)[:8])


@pytest.fixture(autouse=True)
def _fast_knobs(monkeypatch: pytest.MonkeyPatch) -> knobs.CheckpointWritePolicy:
    policy = knobs.CheckpointWritePolicy(
        statement_timeout_ms=30_000, max_retries=2, retry_backoff_ms=1, warn_bytes=1_024,
        # These pin the write budget for a big INLINE row; by-reference values
        # (MKT-111) have their own guard in test_checkpoint_rows_stay_small.py.
        inline_value_max_bytes=0,
    )

    async def _policy() -> knobs.CheckpointWritePolicy:
        return policy

    monkeypatch.setattr(module, "checkpoint_write_policy", _policy)
    return policy


@pytest.fixture
def wired(monkeypatch: pytest.MonkeyPatch) -> Any:
    """Replace the host models and matrx-orm's ``transaction`` context manager."""

    @contextlib.asynccontextmanager
    async def _transaction(*_a: Any, **_k: Any):
        yield None

    import sys
    import types

    stub = types.ModuleType("matrx_orm")
    stub.transaction = _transaction  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "matrx_orm", stub)

    def _use(models: _FakeModels) -> _FakeModels:
        monkeypatch.setattr(module, "get_model", lambda _key: models)
        return models

    return _use


@pytest.mark.asyncio
async def test_a_timed_out_checkpoint_write_is_retried_and_heals(wired: Any) -> None:
    models = wired(_FakeModels(fail_times=1))
    checkpoint = _big_checkpoint(str(uuid4()))

    await module.PostgresCheckpointer().save_checkpoint(checkpoint)

    assert len(models.create_calls) == 2, "the timed-out write was not re-issued"
    assert checkpoint.checkpoint_id in models.rows
    assert models.run_updates[-1]["last_checkpoint_id"] == checkpoint.checkpoint_id


@pytest.mark.asyncio
async def test_the_write_carries_its_own_statement_timeout(wired: Any) -> None:
    models = wired(_FakeModels(fail_times=0))
    await module.PostgresCheckpointer().save_checkpoint(_big_checkpoint(str(uuid4())))
    assert models.create_calls[0]["statement_timeout"] == 30.0


@pytest.mark.asyncio
async def test_a_write_that_actually_landed_is_never_written_twice(wired: Any) -> None:
    """The INSERT is keyed by checkpoint id: ambiguity is decided by READING it."""
    models = wired(_FakeModels(fail_times=1, land_on_failure=True))
    checkpoint = _big_checkpoint(str(uuid4()))

    await module.PostgresCheckpointer().save_checkpoint(checkpoint)

    assert len(models.create_calls) == 1, "we re-inserted a row that was already there"
    assert models.run_updates[-1]["last_checkpoint_id"] == checkpoint.checkpoint_id


@pytest.mark.asyncio
async def test_an_unsavable_checkpoint_fails_honestly_with_its_size(wired: Any) -> None:
    models = wired(_FakeModels(fail_times=99))
    checkpoint = _big_checkpoint(str(uuid4()))

    with pytest.raises(CheckpointWriteFailedError) as caught:
        await module.PostgresCheckpointer().save_checkpoint(checkpoint)

    exc = caught.value
    assert len(models.create_calls) == 3, "the retry budget was not spent"
    assert exc.payload_bytes > 10_000
    assert "save this run's progress" in exc.person_message
    assert "MB" in exc.person_message

    failure = failure_from_exception(exc, step_id="n_map", step_label="Document Ledger")
    assert failure.cause == Cause.PERSISTENCE_FAILED
    assert failure.message == exc.person_message
    assert failure.message != "This account needs an age check before AI can run."


@pytest.mark.asyncio
async def test_an_oversized_checkpoint_screams_with_the_nodes_that_grew_it(
    wired: Any, caplog: pytest.LogCaptureFixture
) -> None:
    wired(_FakeModels(fail_times=0))
    with caplog.at_level("ERROR", logger=module.logger.name):
        await module.PostgresCheckpointer().save_checkpoint(_big_checkpoint(str(uuid4())))
    screams = [r for r in caplog.records if "warn_bytes" in r.getMessage()]
    assert screams, "an over-size checkpoint wrote nothing to the log"
    assert "n_doc_ledger" in screams[0].getMessage()


@pytest.mark.asyncio
async def test_a_non_transient_write_failure_is_not_retried(wired: Any) -> None:
    class _NotNullViolation(Exception):
        __module__ = "matrx_orm.exceptions"

    _NotNullViolation.__name__ = "IntegrityError"

    class _Models(_FakeModels):
        async def create(self, **kwargs: Any) -> None:
            self.create_calls.append(kwargs)
            raise _NotNullViolation("null value in column violates not-null constraint")

    models = wired(_Models(fail_times=0))
    with pytest.raises(Exception) as caught:
        await module.PostgresCheckpointer().save_checkpoint(_big_checkpoint(str(uuid4())))
    assert caught.value.__class__.__name__ == "IntegrityError"
    assert len(models.create_calls) == 1


def test_created_at_default_is_not_required_by_this_suite() -> None:
    """Guard against the fixture drifting from the real Checkpoint shape."""
    checkpoint = _big_checkpoint(str(uuid4()), items=1)
    assert checkpoint.created_at is not None
    assert checkpoint.created_at <= datetime.now(UTC)
