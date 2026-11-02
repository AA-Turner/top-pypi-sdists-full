"""No client-bound failure carries a terminal banner, SQL, or bound args.

Live 2026-09-17, Matrx Studio (workflows.aimatrx.com), a "Save Table Row" step:
the database refused the INSERT with the platform's honest access refusal
(SQLSTATE P0002 — "dataset … is not available to this account"). matrx-orm had
no catch for ``NoDataFoundError``, wrapped it as ``UnknownDatabaseError``, and
the engine used ``str(exc)`` as the node's message. The node inspector showed
the person ANSI color codes, a ``Matrx ORM | UnknownDatabaseError`` rule, the
traceback tail, the exact ``INSERT INTO workbench.udt_dataset_rows`` with its
bound ``Args:`` (their user id and row data), and hints about editing
``async_db_manager.py``. The persisted run said "finished its work but couldn't
save the result" — a refusal reported as a save failure.

Every assertion reads what the ENGINE produced on a real run of a real graph
whose node raised a REAL matrx-orm exception built the way the ORM builds it.
"""

from __future__ import annotations

import asyncpg
from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.db.run_store import RunStore
from matrx_graph.failure import Cause
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.events import NodeFailedEvent, RunErroredEvent
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory, RetryPolicy
from matrx_graph.types.result import NodeResult, failure
from matrx_orm.exceptions import RecordNotAvailableError, UnknownDatabaseError
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context

_QUERY = (
    "INSERT INTO workbench.udt_dataset_rows (table_id, data, user_id) "
    "VALUES ($1, $2, $3) RETURNING *"
)
_SECRET_USER = "4cf62e4e-2679-484c-a1ab-0e62d4e1c3aa"
_ARGS = ["fe025317-0000-4000-8000-000000000000", '{"note": "private row"}', _SECRET_USER]
_REFUSAL = (
    "dataset fe025317-0000-4000-8000-000000000000 is not available to this account "
    "— it may not exist, or your access may not reach it"
)

#: Anything here in a client-bound string is the defect.
_FORBIDDEN = (
    "\x1b",
    "[91m",
    "[0m",
    "Args:",
    "Query:",
    "INSERT INTO",
    "Traceback",
    "Hint:",
    "async_db_manager",
    "Matrx ORM",
    "-" * 20,
    _SECRET_USER,
    "private row",
)


def _assert_clean(label: str, text: object) -> None:
    assert isinstance(text, str), f"{label}: expected a string, got {text!r}"
    for needle in _FORBIDDEN:
        assert needle not in text, f"{label} leaks {needle!r}:\n{text}"


def _unknown_db_error() -> UnknownDatabaseError:
    """Built exactly as async_db_manager.execute_query's catch-all builds it."""
    try:
        raise asyncpg.exceptions.NoDataFoundError(_REFUSAL)
    except Exception as e:  # noqa: BLE001
        import traceback

        return UnknownDatabaseError(
            model=None,
            operation="execute_query",
            query=_QUERY,
            args=_ARGS,
            traceback=traceback.format_exc(),
            original_error=e,
        )


def _record_not_available() -> RecordNotAvailableError:
    return RecordNotAvailableError(
        original_error=asyncpg.exceptions.NoDataFoundError(_REFUSAL),
        query=_QUERY,
        args=_ARGS,
    )


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Out(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = "ok"


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _DbNode:
    def __init__(self, node_type: str, make_exc, *, returns: bool = False) -> None:
        self.spec = NodeSpec(
            type=node_type,
            category=NodeCategory.DATA,
            display_name="Save Table Row",
            description="raises a real matrx-orm error",
            input_schema=_In,
            output_schema=_Out,
            config_schema=_Cfg,
            handles=(
                HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
                HandleSpec(id="out", direction=HandleDirection.OUTPUT),
            ),
            determinism=ActionTier.SIDE_EFFECT,
            retry=RetryPolicy(max_attempts=1),
        )
        self._make_exc = make_exc
        self._returns = returns

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        exc = self._make_exc()
        if self._returns:
            # The returned-envelope path: a node that stringified the ORM error.
            return failure("db_error", str(exc))
        raise exc


async def _run(node: _DbNode, run_id: str):
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(node, overwrite=True)
    definition = {
        "nodes": [
            {
                "id": "save",
                "type": node.spec.node_type,
                "position": {"x": 0, "y": 0},
                "data": {"label": "Save Table Row", "config": {}},
            }
        ],
        "edges": [],
    }
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    result = await scheduler.run(run_id=run_id)
    return result, scheduler, emitter


def _events(emitter: FakeEmitter, name: str) -> list[dict]:
    return [
        e for k, e in emitter.events if k == "data" and isinstance(e, dict) and e.get("event") == name
    ]


async def _assert_every_client_surface_clean(result, scheduler, emitter, run_id: str) -> dict:
    assert result.status is RunStatus.ERRORED
    failed = _events(emitter, "node_failed")
    assert len(failed) == 1
    event = failed[0]
    _assert_clean("node_failed.error_message", event["error_message"])
    for key in ("message", "technical"):
        _assert_clean(f"node_failed.error.{key}", event["error"][key])
    _assert_clean("node_failed.wrapper.error.message", event["wrapper"]["error"]["message"])
    _assert_clean("node_failed.wrapper.error.technical", event["wrapper"]["error"]["technical"])

    outcome = await scheduler.checkpointer.get_outcome(run_id=run_id, step=0, node_id="save", attempt=1)
    assert outcome is not None and outcome.error is not None
    _assert_clean("node_outcome.error.message", outcome.error["message"])
    _assert_clean("node_outcome.error.technical", outcome.error["technical"])

    errored = _events(emitter, "run_errored")
    assert errored
    _assert_clean("run_errored.error_message", errored[0]["error_message"])
    _assert_clean("RunResult.error", result.error)
    _assert_clean("RunResult.failure.message", result.failure.message)
    _assert_clean("RunResult.failure.technical", result.failure.technical)
    return event


async def test_raised_orm_banner_never_reaches_a_client_surface():
    node = _DbNode("test.redact_unknown_db", _unknown_db_error)
    result, scheduler, emitter = await _run(node, "redact-unknown")
    event = await _assert_every_client_surface_clean(result, scheduler, emitter, "redact-unknown")
    # Honest and non-empty: a sentence, not a blank.
    assert event["error_message"].strip()


async def test_returned_failure_built_from_the_banner_is_redacted_too():
    node = _DbNode("test.redact_returned", _unknown_db_error, returns=True)
    result, scheduler, emitter = await _run(node, "redact-returned")
    await _assert_every_client_surface_clean(result, scheduler, emitter, "redact-returned")


async def test_access_refusal_reads_as_a_refusal_with_a_remedy():
    node = _DbNode("test.redact_refusal", _record_not_available)
    result, scheduler, emitter = await _run(node, "redact-refusal")
    event = await _assert_every_client_surface_clean(result, scheduler, emitter, "redact-refusal")
    message = event["error_message"]
    assert "is not available to this account" in message
    assert "ask its owner to share it" in message
    assert event["error"]["cause"] == Cause.NOT_AUTHORIZED
    assert event["error"]["code"] == "RecordNotAvailableError"
    # Never the save-failure lie.
    assert "couldn't save" not in result.failure.message
    assert result.failure.cause == Cause.NOT_AUTHORIZED


def test_event_models_redact_at_construction():
    """A host that builds an event from ``str(exc)`` still cannot leak it."""
    banner = str(_unknown_db_error())
    assert "Args:" in banner and "\x1b" in banner  # the input really is the defect
    node_failed = NodeFailedEvent(
        run_id="r",
        step=0,
        node_id="n",
        spec_type="t",
        attempt=1,
        error_type="UnknownDatabaseError",
        error_message=banner,
        error={"message": banner, "technical": banner, "details": {"technical_message": banner}},
    ).model_dump(mode="json")
    _assert_clean("NodeFailedEvent.error_message", node_failed["error_message"])
    _assert_clean("NodeFailedEvent.error.message", node_failed["error"]["message"])
    _assert_clean("NodeFailedEvent.error.technical", node_failed["error"]["technical"])
    _assert_clean(
        "NodeFailedEvent.error.details.technical_message",
        node_failed["error"]["details"]["technical_message"],
    )
    errored = RunErroredEvent(
        run_id="r", steps_executed=0, node_id="n", step=0, attempt=1,
        error_type="UnknownDatabaseError", error_message=banner,
    ).model_dump(mode="json")
    _assert_clean("RunErroredEvent.error_message", errored["error_message"])


def test_run_error_column_gate_redacts_prose_but_keeps_the_persons_values():
    banner = str(_unknown_db_error())
    stored = RunStore._sanitize_error(
        {"message": banner, "technical": banner, "got": "Query: my own words", "cause": "x"}
    )
    _assert_clean("run.error.message", stored["message"])
    _assert_clean("run.error.technical", stored["technical"])
    # ``got`` is the person's own value — never rewritten.
    assert stored["got"] == "Query: my own words"
