"""Forcing-function tests for ``log.record`` — the workflow's own diagnostics.

Arman, 2026-08-23: a workflow that hits a serious problem and works around it
must be able to SAY SO. Before this node its only options were "fail the whole
run" or "say nothing", and the Agent Foundry took the second while shipping no
component.

These tests bind the four properties that decide whether an author ever
reaches for it again:

1. It WRITES — with the real row content, not a "logged it" string.
2. It NEVER fails the run — a broken database gets `recorded=false` and a
   reason, and the workflow keeps going. A recorder that can break the thing
   it reports on is worse than no recorder.
3. It returns a TYPED receipt whose first field is the confirmation key, so a
   downstream step can branch on it (the same rule Arman applied to agents:
   "one of them being a key that confirms success").
4. An explicit organization is required on every write (db-rules §0.9) — no
   org means `recorded=false`, never a row the database scoped by guessing.

The forcing function throughout is a FAKE MODEL that records what it was
handed: a test asserting only "no exception" would pass just as happily
against a node that wrote nothing at all.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph import run_log as record_mod

from tests._fixtures import make_app_context


class _FakeRunLogModel:
    """Stands in for the generated ``WfRunLog``; keeps every write."""

    def __init__(self) -> None:
        self.writes: list[dict[str, Any]] = []

    def filter(self, **_kw: Any) -> "_FakeRunLogModel":
        return self

    async def count(self) -> int:
        # The cap is DURABLE: it counts the rows already written.
        return len(self.writes)

    async def create_item(self, **kwargs: Any) -> Any:
        self.writes.append(kwargs)

        class _Row:
            id = "11111111-2222-3333-4444-555555555555"

        return _Row()


class _ExplodingRunLogModel:
    def filter(self, **_kw: Any) -> "_ExplodingRunLogModel":
        return self

    async def count(self) -> int:
        return 0

    async def create_item(self, **kwargs: Any) -> Any:
        raise RuntimeError("connection refused")


class _FakeRunModel:
    def filter(self, **_kw: Any) -> "_FakeRunModel":
        return self

    async def values(self, *_a: Any) -> list[dict[str, Any]]:
        return [
            {
                "definition_id": "99999999-8888-7777-6666-555555555555",
                "organization_id": "org-from-the-run",
            }
        ]


class _OrglessRunModel:
    def filter(self, **_kw: Any) -> "_OrglessRunModel":
        return self

    async def values(self, *_a: Any) -> list[dict[str, Any]]:
        return [{"definition_id": None, "organization_id": None}]


def _install(monkeypatch, log_model: Any, run_model: Any | None = None) -> None:
    def _get_model(key: str) -> Any:
        if key == "WfRunLog":
            return log_model
        if key == "WfRun":
            return run_model or _FakeRunModel()
        raise KeyError(key)

    monkeypatch.setattr("matrx_graph.db._registry.get_model", _get_model, raising=False)


def _app_with_org(org: str | None) -> Any:
    """AppContext is a FROZEN dataclass — build it with the org, never mutate."""
    import dataclasses

    return dataclasses.replace(make_app_context(), organization_id=org)


def _definition(inputs: dict[str, Any], config: dict[str, Any] | None = None) -> Definition:
    data: dict[str, Any] = {"input": inputs}
    if config is not None:
        data["config"] = config
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "note",
                    "type": "log.record",
                    "position": {"x": 0, "y": 0},
                    "data": data,
                }
            ],
            "edges": [],
        }
    )


async def _run(
    inputs: dict[str, Any],
    *,
    org: str | None = "org-1",
    config: dict[str, Any] | None = None,
):
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    # The node DECLARES its inputs (W68); the run below delivers the same
    # values over the broadcast channel, last-writer-wins.
    graph = compile_graph(_definition(inputs, config), registry=registry)
    app = _app_with_org(org)
    scheduler = Scheduler(graph, MemoryCheckpointer(), app, registry=registry)
    return await scheduler.run(run_id="run-log-test", inputs=inputs)


@pytest.mark.asyncio
async def test_it_writes_the_real_row(monkeypatch):
    model = _FakeRunLogModel()
    _install(monkeypatch, model)

    result = await _run(
        {
            "label": "component_not_written",
            "message": "Both artisans refused to build.",
            "severity": "error",
            "payload": {"artisan_a": "refused", "artisan_b": "refused"},
            "payload_kind": "component_design_brief_pair",
        }
    )

    assert result.status is RunStatus.COMPLETED
    # THE FORCING FUNCTION: exactly one row, with the content — not a log line.
    assert len(model.writes) == 1, model.writes
    row = model.writes[0]
    assert row["label"] == "component_not_written"
    assert row["severity"] == "error"
    assert row["message"] == "Both artisans refused to build."
    assert row["payload"] == {"artisan_a": "refused", "artisan_b": "refused"}
    assert row["payload_kind"] == "component_design_brief_pair"
    # Provenance the diagnosis is useless without.
    assert row["node_id"] == "note"
    assert row["run_id"] == "run-log-test"
    assert row["definition_id"] == "99999999-8888-7777-6666-555555555555"
    # THE ORG IS THE RUN'S. Reading it off AppContext refused to write on the
    # first real run — a detached workflow context legitimately has none.
    assert row["organization_id"] == "org-from-the-run"


@pytest.mark.asyncio
async def test_the_receipt_confirms_success_and_is_branchable(monkeypatch):
    _install(monkeypatch, _FakeRunLogModel())
    result = await _run({"label": "x", "message": "y"})
    out = result.last_outputs["note"]
    dump = out if isinstance(out, dict) else out.model_dump(mode="json")
    # "a key that confirms success, and that is the key you read" — Arman.
    assert dump["recorded"] is True
    assert dump["entry_id"] == "11111111-2222-3333-4444-555555555555"
    assert dump["not_recorded_reason"] is None


@pytest.mark.asyncio
async def test_a_dead_database_never_fails_the_run(monkeypatch):
    _install(monkeypatch, _ExplodingRunLogModel())
    result = await _run({"label": "component_not_written"})

    # The run survives — this node exists for the case where the workflow
    # WORKED AROUND the problem; breaking that run would be perverse.
    assert result.status is RunStatus.COMPLETED
    out = result.last_outputs["note"]
    dump = out if isinstance(out, dict) else out.model_dump(mode="json")
    assert dump["recorded"] is False
    # ...and it says WHY. A receipt that says "no" without a reason is the
    # shrug this whole node exists to end.
    assert "connection refused" in (dump["not_recorded_reason"] or "")


@pytest.mark.asyncio
async def test_the_step_config_severity_is_reachable(monkeypatch):
    """An input default must never mask the author's own configuration.

    Caught on the FIRST live run: a step configured `severity: error` recorded
    a `warning`, because `inputs.severity or config.severity` can never see
    past a non-null input default. Absence has to be representable.
    """
    model = _FakeRunLogModel()
    _install(monkeypatch, model)
    await _run({"label": "refused"}, config={"severity": "error"})
    assert model.writes[0]["severity"] == "error"

    # ...and an explicit input still wins over the config.
    model.writes.clear()
    await _run({"label": "refused", "severity": "critical"}, config={"severity": "error"})
    assert model.writes[0]["severity"] == "critical"


@pytest.mark.asyncio
async def test_no_organization_anywhere_means_no_row(monkeypatch):
    model = _FakeRunLogModel()
    _install(monkeypatch, model, run_model=_OrglessRunModel())
    result = await _run({"label": "orphan"}, org=None)

    assert result.status is RunStatus.COMPLETED
    # db-rules §0.9 — the database never chooses an organization. A row nobody
    # can read is not a record, so we refuse to write one and say so.
    assert model.writes == []
    out = result.last_outputs["note"]
    dump = out if isinstance(out, dict) else out.model_dump(mode="json")
    assert dump["recorded"] is False
    assert "organization" in (dump["not_recorded_reason"] or "")


@pytest.mark.asyncio
async def test_a_runaway_loop_is_capped_not_unbounded(monkeypatch):
    model = _FakeRunLogModel()
    _install(monkeypatch, model)

    from matrx_graph.nodes.log.record import (
        RecordIssueConfig,
        RecordIssueExecutor,
        RecordIssueInput,
    )
    from matrx_graph.run_log import MAX_ENTRIES_PER_RUN
    from matrx_graph.types.context import NodeExecutionContext

    app = _app_with_org("org-1")
    executor = RecordIssueExecutor()
    for i in range(MAX_ENTRIES_PER_RUN + 5):
        ctx = NodeExecutionContext(
            app=app,
            run_id="looping-run",
            thread_id="looping-thread",
            node_id="note",
            step=i,
            attempt=1,
            channels=None,  # type: ignore[arg-type]
            checkpointer=MemoryCheckpointer(),
        )
        await executor.execute(ctx, RecordIssueInput(label="loop"), RecordIssueConfig())

    # One runaway step must not be able to write a million rows.
    assert len(model.writes) == MAX_ENTRIES_PER_RUN, len(model.writes)


@pytest.mark.asyncio
async def test_fat_evidence_is_truncated_not_refused(monkeypatch):
    model = _FakeRunLogModel()
    _install(monkeypatch, model)
    huge = {"blob": "x" * (record_mod.MAX_PAYLOAD_CHARS + 5_000)}
    result = await _run({"label": "big", "payload": huge})

    assert result.status is RunStatus.COMPLETED
    assert len(model.writes) == 1
    stored = model.writes[0]["payload"]
    # Losing the whole record because the evidence was fat is the wrong trade.
    assert stored.get("truncated") is True
    assert stored["original_chars"] > record_mod.MAX_PAYLOAD_CHARS
    out = result.last_outputs["note"]
    dump = out if isinstance(out, dict) else out.model_dump(mode="json")
    assert dump["recorded"] is True
    assert "truncated" in dump["message"]


def test_the_node_declares_its_receipt_kind():
    from matrx_graph.nodes.log.record import RecordIssueExecutor

    # A node that reports problems as prose cannot be branched on — the same
    # rule this whole change applies to the artisans.
    assert RecordIssueExecutor.spec.output_kind == "run_log_entry"
    assert RecordIssueExecutor.spec.dynamic_output is False


@pytest.mark.asyncio
async def test_the_cap_is_durable_not_per_process(monkeypatch):
    """A restarted worker starts with an EMPTY process — the cap must still hold.

    The old cap was a module dict; a new process (or a second worker) started a
    fresh budget. The writer now counts the run's rows in the table itself.
    """
    from matrx_graph.run_log import MAX_ENTRIES_PER_RUN, write_run_log

    model = _FakeRunLogModel()
    model.writes.extend({"label": "earlier"} for _ in range(MAX_ENTRIES_PER_RUN))
    _install(monkeypatch, model)
    entry = await write_run_log(
        run_id="run-1", node_id="n", step=1, attempt=1, label="one more",
        organization_id="org-1",
    )
    assert entry.recorded is False
    assert str(MAX_ENTRIES_PER_RUN) in (entry.not_recorded_reason or "")
    assert len(model.writes) == MAX_ENTRIES_PER_RUN
