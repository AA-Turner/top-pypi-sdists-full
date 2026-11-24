"""Guard (FIX-L6, 2026-11-03): a text-only input provably fed a whole object is named at save.

Live, release 36eaeafb684: Company Setup built "Send pickup reminders" — Find Ready orders
(``table.row.list``) -> For each (``control.map``, ``payload_template: {"prompt": "$item"}``) ->
Write the reminder (``ai.llm.chat``). Every item was a whole Row (id, values, version …) landing on
the TEXT ``prompt``; the save said nothing and every run stopped with ``string_type``. The run's
refusal is right; the save-time offer was missing. This pins, on the one validator every save /
publish / apply-patch door runs:

* the live shape (a whole record, and a whole list, into a text input — per-item template AND
  edge mapping) is a WARNING that names the input, the shape and the ``$format`` fix — never an error
  (validation offers, never blocks);
* the fixed shapes (``$format``, a text field path) are silent, and so is an undescribed element;
* the run-time refusal says it got a whole record, not just "it expects text";
* AT RUN the bakery shape (For each ``$item`` Row -> a text ``prompt``) COMPLETES: the step gets the
  whole record as JSON text (what ``{"$format": "{item}"}`` sends) and carries a visible note
  (an ``engine.sent_whole_value_as_text.prompt`` review flag) — never converted silently.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from matrx_graph.actions import register_node
from matrx_graph.actions.registry import ActionRegistry
from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph, run_log
from matrx_graph.executor.registry import default_registry
from matrx_graph.failure import problems_from_validation_error, problems_from_validation_text
from matrx_graph.nodes import register_builtin_nodes
from matrx_graph.nodes._template import substitute_template
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.result import NodeResult, success
from matrx_graph.validation import validate_definition
from tests._fixtures import FakeEmitter, make_app_context


class _Row(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    values: dict[str, Any] = Field(description="Every column by name.")
    version: int | None = None


class _RowPage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    rows: list[_Row]
    loose: list[Any] = []
    total: int = 0


class _ListIn(BaseModel):
    model_config = ConfigDict(extra="allow")


class _ChatIn(BaseModel):
    model_config = ConfigDict(extra="allow")
    prompt: str = Field(min_length=1)
    system_instruction: str | None = None


class _ChatOut(BaseModel):
    text: str = ""


def _register() -> None:
    register_builtin_nodes(overwrite=True)

    @register_node(name="testing.rows", description="rows", input_schema=_ListIn,
                   output_schema=_RowPage, node_registry=default_registry(),
                   action_registry=ActionRegistry(), overwrite=True)
    async def rows(ctx: NodeExecutionContext, inputs: _ListIn) -> NodeResult[_RowPage]:
        return success(_RowPage(rows=[]))

    @register_node(name="testing.chat", description="chat", input_schema=_ChatIn,
                   output_schema=_ChatOut, node_registry=default_registry(),
                   action_registry=ActionRegistry(), overwrite=True)
    async def chat(ctx: NodeExecutionContext, inputs: _ChatIn) -> NodeResult[_ChatOut]:
        return success(_ChatOut())


def _node(nid: str, spec: str, config: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"id": nid, "type": spec, "position": {"x": 0, "y": 0},
            "data": {"label": nid, "config": config or {}, "input": {}}}


def _edge(eid: str, s: str, t: str, mappings: dict[str, str] | None = None) -> dict[str, Any]:
    data: dict[str, Any] = {"kind": "data"}
    if mappings is not None:
        data["mappings"] = mappings
    return {"id": eid, "source": s, "target": t, "data": data}


def _pickup_reminders(prompt: Any, items_from: str = "rows") -> dict[str, Any]:
    """The live definition 3f1960e3, on test steps with the same declared shapes."""
    return {
        "nodes": [
            _node("ready", "testing.rows"),
            _node("each", "control.map", {"target_node_id": "write", "payload_template": {"prompt": prompt}}),
            _node("write", "testing.chat"),
        ],
        "edges": [_edge("e1", "ready", "each", {"items": items_from})],
    }


def _text_issues(raw: dict[str, Any]) -> list[Any]:
    _register()
    return [i for i in validate_definition(raw).issues if "takes text for" in i.message]


def test_the_live_shape_warns_and_names_the_fix() -> None:
    issues = _text_issues(_pickup_reminders("$item"))
    assert len(issues) == 1, issues
    (issue,) = issues
    assert issue.severity == "warning", "validation offers, never blocks"
    assert issue.node_id == "each"
    assert issue.path == "nodes[each].data.config.payload_template.prompt"
    assert "'write' takes text for 'prompt'" in issue.message
    assert "whole record" in issue.message and "'values'" in issue.message
    assert '{"$format": "{item}"}' in issue.message, issue.message


def test_a_nested_object_or_list_path_warns_too() -> None:
    (issue,) = _text_issues(_pickup_reminders("$item.values"))
    assert "whole record" in issue.message


def test_fixed_shapes_and_undescribed_elements_are_silent() -> None:
    assert _text_issues(_pickup_reminders({"$format": "{item}"})) == []
    assert _text_issues(_pickup_reminders("$item.id")) == []
    assert _text_issues(_pickup_reminders("$item", items_from="loose")) == []


def test_an_edge_mapping_a_list_onto_a_text_input_warns() -> None:
    raw = {
        "nodes": [_node("ready", "testing.rows"), _node("write", "testing.chat")],
        "edges": [_edge("e1", "ready", "write", {"prompt": "rows"})],
    }
    (issue,) = _text_issues(raw)
    assert issue.severity == "warning" and issue.edge_id == "e1"
    assert "'rows' on 'ready' is a whole list" in issue.message
    raw["edges"][0]["data"]["mappings"] = {"prompt": "rows.0.id"}
    assert _text_issues(raw) == []


def test_the_suggested_format_really_renders_the_record_as_text() -> None:
    """The fix the warning hands over must be a real one: $format turns the record into JSON text."""
    row = {"id": "r1", "values": {"Customer": "Tom"}}
    out = substitute_template({"prompt": {"$format": "{item}"}}, row, index=0)
    assert isinstance(out["prompt"], str) and '"Customer": "Tom"' in out["prompt"]


def test_the_run_time_refusal_says_it_got_a_whole_record() -> None:
    try:
        _ChatIn.model_validate({"prompt": {"id": "r1", "values": {}}})
    except ValidationError as e:
        (live,) = problems_from_validation_error(e)
        (text,) = problems_from_validation_text(str(e))
    assert "not a whole record" in (live.expected or ""), live
    assert "not a whole record" in (text.expected or ""), text
    _ChatIn.model_validate({"prompt": "fine"})


# ── AT RUN: the bakery shape completes, and says what it did ─────────────────


async def test_the_bakery_shape_completes_and_the_step_says_it_got_json_text() -> None:
    seen: list[str] = []
    flags: list[dict[str, Any]] = []

    async def record(**kw: Any) -> Any:
        flags.append(kw)
        return run_log.RunLogEntry(recorded=True, entry_id=str(len(flags)), label=kw["label"],
                                   needs_review=kw["needs_review"])

    reg = NodeRegistry()
    register_builtin_nodes(reg)

    @register_node(name="testing.run_rows", description="rows", input_schema=_ListIn,
                   output_schema=_RowPage, node_registry=reg, action_registry=ActionRegistry(),
                   overwrite=True)
    async def run_rows(ctx: NodeExecutionContext, inputs: _ListIn) -> NodeResult[_RowPage]:
        return success(_RowPage(rows=[_Row(id="r1", values={"Customer": "Tom Becker"}),
                                      _Row(id="r2", values={"Customer": "Ana Ruiz"})]))

    @register_node(name="testing.run_chat", description="chat", input_schema=_ChatIn,
                   output_schema=_ChatOut, node_registry=reg, action_registry=ActionRegistry(),
                   overwrite=True)
    async def run_chat(ctx: NodeExecutionContext, inputs: _ChatIn) -> NodeResult[_ChatOut]:
        seen.append(inputs.prompt)
        return success(_ChatOut(text="ok"))

    definition = {
        "nodes": [
            _node("ready", "testing.run_rows"),
            _node("each", "control.map", {"target_node_id": "write", "payload_template": {"prompt": "$item"}}),
            _node("write", "testing.run_chat"),
        ],
        "edges": [_edge("e1", "ready", "each", {"items": "rows"})],
    }
    run_log.configure_run_log_writer(record)
    try:
        graph = compile_graph(Definition.model_validate(definition), registry=reg)
        result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(FakeEmitter()),
                                 registry=reg).run(run_id="fix-l6-bakery")
    finally:
        run_log.configure_run_log_writer(None)

    assert result.status is RunStatus.COMPLETED, result.error
    assert len(seen) == 2 and all(isinstance(p, str) for p in seen)
    assert '"Customer": "Tom Becker"' in seen[0] or '"Customer": "Tom Becker"' in seen[1], seen
    notes = [f for f in flags if f["label"] == "engine.sent_whole_value_as_text.prompt"]
    assert len(notes) == 2, flags
    assert notes[0]["node_id"] == "write" and notes[0]["needs_review"]
    assert "sent the whole record as text" in notes[0]["message"]
    assert "pick fields" in notes[0]["message"]
