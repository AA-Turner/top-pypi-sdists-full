"""A declared output kind that arrives under ONE wrapper key settles as the kind.

Live defect (2026-11-03, workflow "Order follow-up" 0312625b, runs 62b1427a /
d19dd50b / 904cb6b2): the display step 'show' (``output.to_frontend``) declared
``output_kind: bouquet_followup_note`` while its edge mapped
``result: structured_output`` — the step passed ``{"result": {customer, bouquet,
follow_up_note}}`` through, enforcement checked the WRAPPER against the kind, and
every run died "'bouquet' / 'customer' / 'follow_up_note' are required; 'result'
was unexpected" although the value under 'result' was exactly the kind.

The rule: a declared kind nested under a single wrapper key is unwrapped when the
inner value passes on its own. A genuine mismatch still fails, and its message
names the step and what it actually handed over beside the kind's errors.
"""

from __future__ import annotations

import time
from typing import Any, ClassVar

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
from matrx_graph import kinds as kinds_mod
from matrx_graph.kinds import (
    KIND_ENFORCEMENT,
    KindEntry,
    describe_kind_mismatch,
    invalidate_kind_catalog_cache,
    single_wrapped_value,
)
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context

_KIND = "wrap_followup_note"
_SCHEMA = {
    "type": "object",
    "properties": {
        "__kind": {"const": _KIND},
        "customer": {"type": "string"},
        "bouquet": {"type": "string"},
        "follow_up_note": {"type": "string"},
    },
    "required": ["__kind", "customer", "bouquet", "follow_up_note"],
    "additionalProperties": False,
}


@pytest.fixture(autouse=True)
def _seeded_kind(monkeypatch):
    invalidate_kind_catalog_cache()
    monkeypatch.setitem(KIND_ENFORCEMENT, "workflow_io", True)
    kinds_mod._cache[_KIND] = (
        time.monotonic(),
        KindEntry(slug=_KIND, version=1, json_schema=_SCHEMA),
    )
    yield
    invalidate_kind_catalog_cache()


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Out(BaseModel):
    structured_output: dict[str, Any]


class _Cfg(BaseModel):
    pass


def _writer(note: dict[str, Any]) -> Any:
    class _Writer:
        spec: ClassVar[NodeSpec] = NodeSpec(
            type="test.wrap_writer",
            category=NodeCategory.DATA,
            display_name="Writer",
            description="Returns a structured_output like an AI step.",
            input_schema=_In,
            output_schema=_Out,
            config_schema=_Cfg,
            handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
            determinism=ActionTier.PURE,
        )

        async def execute(
            self, _ctx: NodeExecutionContext, _inputs: _In, _config: _Cfg
        ) -> NodeResult[_Out]:
            return success(_Out(structured_output=dict(note)))

    return _Writer()


async def _run(note: dict[str, Any], run_id: str):
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(_writer(note), overwrite=True)
    definition = Definition.model_validate(
        {
            "nodes": [
                {"id": "write_note", "type": "test.wrap_writer", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
                {
                    "id": "show",
                    "type": "output.to_frontend",
                    "position": {"x": 300, "y": 0},
                    "data": {"config": {"payload_key": "result"}, "output_kind": _KIND},
                },
            ],
            "edges": [
                {
                    "id": "e4",
                    "source": "write_note",
                    "target": "show",
                    "data": {"kind": "data", "mappings": {"result": "structured_output"}},
                }
            ],
        }
    )
    graph = compile_graph(definition, registry=reg)
    checkpointer = MemoryCheckpointer()
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, checkpointer, make_app_context(emitter), registry=reg)
    result = await scheduler.run(run_id=run_id)
    return result, emitter


def _events(emitter: FakeEmitter, event: str) -> list[dict[str, Any]]:
    return [p for (m, p) in emitter.events if m == "data" and isinstance(p, dict) and p.get("event") == event]


_NOTE = {"customer": "Ella Brooks", "bouquet": "White Peony Bouquet", "follow_up_note": "Hi Ella, thank you."}


async def test_the_kind_under_result_settles_as_the_kind() -> None:
    result, emitter = await _run(_NOTE, "wrap-ok")
    assert result.status is RunStatus.COMPLETED, _events(emitter, "node_failed")
    show = [e for e in _events(emitter, "node_completed") if e.get("node_id") == "show"]
    assert len(show) == 1
    assert show[0]["output"] == {**_NOTE, "__kind": _KIND}
    assert show[0]["output_kind_ok"] is True


async def test_a_real_mismatch_still_fails_and_names_what_it_got() -> None:
    bad = {"customer": "Ella Brooks", "bouquet": "White Peony Bouquet"}
    result, emitter = await _run(bad, "wrap-bad")
    assert result.status is not RunStatus.COMPLETED
    failed = [e for e in _events(emitter, "node_failed") if e.get("node_id") == "show"]
    assert len(failed) == 1
    assert failed[0]["error_type"] == "KindContractViolation"
    message = str(failed[0].get("error") or failed[0])
    assert "'show' handed over 'result'; inside 'result' it has 'bouquet', 'customer'." in message


def test_single_wrapped_value_sees_only_one_object_wrapper() -> None:
    assert single_wrapped_value({"result": {"a": 1}}) == ("result", {"a": 1})
    assert single_wrapped_value({"result": {"a": 1}, "__kind": "x"}) == ("result", {"a": 1})
    assert single_wrapped_value({"result": {"a": 1}, "other": 2}) is None
    assert single_wrapped_value({"result": "text"}) is None
    assert single_wrapped_value(["result"]) is None


def test_describe_kind_mismatch_names_the_fields() -> None:
    assert describe_kind_mismatch("show", {"a": 1, "b": 2}) == "'show' handed over 'a', 'b'."
    assert describe_kind_mismatch("show", "hi") == "'show' handed over text, not an object."
