"""A mapping whose source path is missing in THIS output delivers the input absent; the target decides.

Live 2026-10-27 (Smart Add email unit, workflow 4df72f69, the empty-input run): ``parse.first`` is null when the
typed text is not an email, and the edge mapping ``domain <- first.domain`` stopped the whole run with "wiring
broken" (EdgeRoutingError). The path is legal — the source declares ``first`` (nullable) — the value is just not
there this time. Contract (scheduler ``_map_edge_payload``):

* the source's declared output PROVABLY lacks the path (a closed level, no such field) -> wiring error, as before
  (validation refuses it at save; a run that still meets it parks ERRORED attributed to the source);
* otherwise a miss (null on the way, key left out, list too short) -> the arg arrives ABSENT; an optional input
  takes its default, a required one fails at the target naming the input.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeCategory,
    NodeRegistry,
    NodeSpec,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.result import NodeResult, success
from matrx_graph.validation import validate_definition

from tests._fixtures import FakeEmitter, make_app_context


class _Parts(BaseModel):
    model_config = ConfigDict(extra="forbid")
    local: str
    domain: str


class _ParseOut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    first: _Parts | None = None
    found: int = 0


class _ParseCfg(BaseModel):
    text: str = ""


class _Parse:
    """Like ``text.regex_extract`` with ``first_only``: ``first`` is null when nothing matched."""

    spec = NodeSpec(
        type="test.parse_email",
        category=NodeCategory.CUSTOM,
        display_name="Parse email",
        output_schema=_ParseOut,
        config_schema=_ParseCfg,
        handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
    )

    async def execute(self, ctx: NodeExecutionContext, inputs, config) -> NodeResult[_ParseOut]:
        text = config.text if isinstance(config, _ParseCfg) else str((config or {}).get("text") or "")
        if "@" not in text:
            return success(_ParseOut())
        local, domain = text.split("@", 1)
        return success(_ParseOut(first=_Parts(local=local, domain=domain), found=1))


class _NeedsDomainIn(BaseModel):
    domain: str


class _NeedsDomainOut(BaseModel):
    looked_up: str


class _NeedsDomain:
    spec = NodeSpec(
        type="test.needs_domain",
        category=NodeCategory.CUSTOM,
        display_name="Needs a domain",
        input_schema=_NeedsDomainIn,
        output_schema=_NeedsDomainOut,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
    )

    async def execute(self, ctx: NodeExecutionContext, inputs, config) -> NodeResult[_NeedsDomainOut]:
        return success(_NeedsDomainOut(looked_up=inputs.domain))


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(_Parse())
    reg.register(_NeedsDomain())
    return reg


def _definition(text: str, *, target: str = "data.transform", source_path: str = "first.domain") -> dict:
    target_data = (
        {"config": {"expression": "{'domain': inputs['domain'] if 'domain' in inputs else ''}"}}
        if target == "data.transform"
        else {}
    )
    return {
        "nodes": [
            {"id": "parse", "type": "test.parse_email", "position": {"x": 0, "y": 0}, "data": {"config": {"text": text}}},
            {"id": "use", "type": target, "position": {"x": 200, "y": 0}, "data": target_data},
        ],
        "edges": [
            {"id": "e_domain", "source": "parse", "target": "use",
             "data": {"kind": "data", "mappings": {"domain": source_path}}},
        ],
        "entry_nodes": ["parse"],
    }


async def _run(defn: dict, run_id: str):
    registry = _registry()
    graph = compile_graph(Definition.model_validate(defn), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    result = await scheduler.run(run_id=run_id)
    errored = [e for k, e in emitter.events if k == "data" and isinstance(e, dict) and e.get("event") == "run_errored"]
    return result, errored


async def test_a_present_path_is_delivered():
    result, _ = await _run(_definition("press@patagonia.com"), "map-present")
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["use"] == {"domain": "patagonia.com"}


async def test_a_path_through_null_arrives_absent_and_the_run_completes():
    result, errored = await _run(_definition("not an email"), "map-null")
    assert result.status is RunStatus.COMPLETED, result.error
    assert not errored
    assert result.last_outputs["use"] == {"domain": ""}


async def test_a_required_input_left_absent_fails_at_the_target_not_as_wiring():
    result, errored = await _run(_definition("not an email", target="test.needs_domain"), "map-null-required")
    assert result.status is RunStatus.ERRORED
    assert len(errored) == 1
    assert errored[0]["node_id"] == "use"
    assert errored[0]["error_type"] != "EdgeRoutingError"
    assert "domain" in (result.error or "")


def test_a_path_the_declared_output_rules_out_is_refused_at_save():
    """The real wiring error never reaches a run: validate (and so compile) refuses it. A run that meets one anyway
    (a transform whose emitted keys are known only at compile) still parks ERRORED as EdgeRoutingError —
    ``test_scheduler_failsoft.py::test_edge_mapping_miss_parks_not_silent``."""
    import pytest

    from matrx_graph.errors import CompilationError

    defn = _definition("press@patagonia.com", source_path="nope.domain")
    findings = [i for i in validate_definition(defn, _registry()).issues if i.edge_id == "e_domain"]
    assert any(i.severity == "error" and "can never resolve" in i.message for i in findings), findings
    with pytest.raises(CompilationError):
        compile_graph(Definition.model_validate(defn), registry=_registry())
