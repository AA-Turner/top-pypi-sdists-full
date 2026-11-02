from __future__ import annotations

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)

from tests._fixtures import FakeEmitter, make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _user_input_node(node_id: str = "ask", required: bool = True) -> dict:
    return {
        "id": node_id,
        "type": "io.user_input",
        "position": {"x": 0, "y": 0},
        "data": {
            "config": {
                "title": "Study inputs",
                "fields": [
                    {
                        "key": "topic",
                        "label": "Topic",
                        "type": "text",
                        "required": required,
                    },
                    {
                        "key": "audience",
                        "label": "Audience",
                        "type": "choice",
                        "options": ["high school", "college"],
                    },
                ],
            }
        },
    }


def _data_events(emitter: FakeEmitter) -> list[dict]:
    return [p for k, p in emitter.events if k == "data" and isinstance(p, dict)]


async def test_user_input_seeds_run_and_routes_downstream():
    registry = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                _user_input_node("ask"),
                {
                    "id": "echo",
                    "type": "data.transform",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {"expression": "inputs['topic']"}},
                },
            ],
            "edges": [{"id": "e1", "source": "ask", "target": "echo"}],
        }
    )
    graph = compile_graph(definition, registry=registry)

    # The dynamic output schema is computed on the compiled node (run-form source).
    eff = graph.nodes["ask"].effective_output_schema
    assert eff is not None
    assert "topic" in eff["properties"]
    assert eff["required"] == ["topic"]

    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    result = await scheduler.run(
        run_id="run-ui-1",
        node_inputs={"ask": {"topic": "WW2", "audience": "college"}},
    )
    assert result.status is RunStatus.COMPLETED

    events = _data_events(emitter)
    # The user_input node was seeded with the form's values.
    started = [e for e in events if e.get("event") == "node_started" and e.get("node_id") == "ask"]
    assert started and started[0]["inputs"]["topic"] == "WW2"

    # Those values routed downstream unchanged.
    completed = [e for e in events if e.get("event") == "run_completed"][0]
    assert completed["last_outputs"]["echo"]["result"] == "WW2"


async def test_user_input_required_field_parks_run():
    registry = _registry()
    definition = Definition.model_validate(
        {"nodes": [_user_input_node("ask", required=True)], "edges": []}
    )
    graph = compile_graph(definition, registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    # No node_inputs → required 'topic' missing → the run PARKS awaiting_input
    # at the start gate (INPUT-SURFACE.md park-not-die) — never a crash, and
    # no node ever fires (the previous behavior parked ERRORED on the node).
    result = await scheduler.run(run_id="run-ui-missing")
    assert result.status is RunStatus.AWAITING_INPUT
    assert result.interrupt is not None and result.interrupt["kind"] == "awaiting_input"
    assert [m["name"] for m in result.interrupt["missing"]] == ["topic"]


def _number_input_node(node_id: str = "ask") -> dict:
    return {
        "id": node_id,
        "type": "io.user_input",
        "position": {"x": 0, "y": 0},
        "data": {
            "config": {
                "title": "Count",
                "fields": [
                    {
                        "key": "count",
                        "label": "Count",
                        "type": "number",
                        "required": True,
                    }
                ],
            }
        },
    }


def test_validate_instance_reports_every_bad_field():
    from matrx_graph.executor.schema_validation import validate_instance

    schema = {
        "type": "object",
        "properties": {
            "topic": {"type": "string"},
            "count": {"type": "number"},
            "audience": {"type": "string", "enum": ["high school", "college"]},
        },
        "required": ["topic"],
    }
    # Well-typed value → no errors.
    assert validate_instance(schema, {"topic": "WW2", "count": 3}) == []
    # One call reports ALL bad fields (missing required, wrong type, bad enum).
    joined = " ".join(validate_instance(schema, {"count": "x", "audience": "kg"}))
    assert "topic" in joined  # missing required
    assert "count" in joined  # string where number expected
    assert "audience" in joined  # outside the allowed enum


async def test_user_input_rejects_out_of_enum_choice():
    # `audience` allows only "high school"/"college". A value outside that set
    # used to pass silently (permissive input model) and corrupt the run;
    # now it parks the run on this node with a per-field message.
    registry = _registry()
    definition = Definition.model_validate(
        {"nodes": [_user_input_node("ask", required=True)], "edges": []}
    )
    graph = compile_graph(definition, registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    result = await scheduler.run(
        run_id="run-ui-badenum",
        node_inputs={"ask": {"topic": "WW2", "audience": "kindergarten"}},
    )
    assert result.status is RunStatus.ERRORED
    failed = [
        e
        for e in _data_events(emitter)
        if e.get("event") == "node_failed" and e.get("node_id") == "ask"
    ]
    assert failed, "expected the user_input node to fail validation"
    assert failed[0]["error_type"] == "NodeInputValidationError"
    assert "audience" in failed[0]["error_message"]


async def test_user_input_rejects_wrong_typed_number():
    registry = _registry()
    definition = Definition.model_validate({"nodes": [_number_input_node("ask")], "edges": []})
    graph = compile_graph(definition, registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    # A number field handed a non-numeric string is exactly the garbage that
    # used to flow downstream — now rejected at the boundary, before the node.
    result = await scheduler.run(
        run_id="run-ui-badnum", node_inputs={"ask": {"count": "not a number"}}
    )
    assert result.status is RunStatus.ERRORED
    failed = [
        e
        for e in _data_events(emitter)
        if e.get("event") == "node_failed" and e.get("node_id") == "ask"
    ]
    assert failed and failed[0]["error_type"] == "NodeInputValidationError"


async def test_user_input_accepts_valid_typed_input():
    registry = _registry()
    definition = Definition.model_validate({"nodes": [_number_input_node("ask")], "edges": []})
    graph = compile_graph(definition, registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    result = await scheduler.run(run_id="run-ui-goodnum", node_inputs={"ask": {"count": 42}})
    assert result.status is RunStatus.COMPLETED


async def test_to_frontend_emits_event_and_passes_through():
    registry = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                _user_input_node("ask", required=False),
                {
                    "id": "show",
                    "type": "output.to_frontend",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {"mode": "full", "title": "Your topic"}},
                },
                {
                    "id": "echo",
                    "type": "data.transform",
                    "position": {"x": 400, "y": 0},
                    "data": {"config": {"expression": "inputs['topic']"}},
                },
            ],
            "edges": [
                {"id": "e1", "source": "ask", "target": "show"},
                {"id": "e2", "source": "show", "target": "echo"},
            ],
        }
    )
    graph = compile_graph(definition, registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    result = await scheduler.run(run_id="run-emit-1", node_inputs={"ask": {"topic": "WW2"}})
    assert result.status is RunStatus.COMPLETED

    events = _data_events(emitter)
    emitted = [e for e in events if e.get("event") == "node_emitted"]
    assert len(emitted) == 1
    assert emitted[0]["mode"] == "full"
    assert emitted[0]["payload"]["topic"] == "WW2"
    assert emitted[0]["surface"] == "matrx-user/workflow"
    assert emitted[0]["title"] == "Your topic"
    # Default presentation: the step's normal window panel.
    assert emitted[0]["presentation"] == "panel"

    # Pass-through: the emit did NOT consume the payload — it reached `echo`.
    completed = [e for e in events if e.get("event") == "run_completed"][0]
    assert completed["last_outputs"]["echo"]["result"] == "WW2"


async def test_to_frontend_showcase_presentation_rides_the_event():
    """``presentation='showcase'`` is the author's "present this to the user"
    choice — it rides the node_emitted event unchanged (payload, mode, title
    all as before) so the Studio can open the dedicated presentation."""
    registry = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                _user_input_node("ask", required=False),
                {
                    "id": "show",
                    "type": "output.to_frontend",
                    "position": {"x": 200, "y": 0},
                    "data": {
                        "config": {
                            "mode": "full",
                            "title": "Your result",
                            "presentation": "showcase",
                        }
                    },
                },
            ],
            "edges": [{"id": "e1", "source": "ask", "target": "show"}],
        }
    )
    graph = compile_graph(definition, registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    result = await scheduler.run(run_id="run-emit-showcase", node_inputs={"ask": {"topic": "WW2"}})
    assert result.status is RunStatus.COMPLETED

    emitted = [e for e in _data_events(emitter) if e.get("event") == "node_emitted"]
    assert len(emitted) == 1
    assert emitted[0]["presentation"] == "showcase"
    assert emitted[0]["mode"] == "full"
    assert emitted[0]["payload"]["topic"] == "WW2"
    assert emitted[0]["title"] == "Your result"


async def test_to_frontend_emit_failure_is_swallowed():
    class RaiseOnEmit(FakeEmitter):
        async def send_data(self, payload):
            if hasattr(payload, "model_dump"):
                payload = payload.model_dump(mode="json")
            if isinstance(payload, dict) and payload.get("event") == "node_emitted":
                raise RuntimeError("emit channel down")
            await super().send_data(payload)

    registry = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                _user_input_node("ask", required=False),
                {
                    "id": "show",
                    "type": "output.to_frontend",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {"mode": "full"}},
                },
                {
                    "id": "echo",
                    "type": "data.transform",
                    "position": {"x": 400, "y": 0},
                    "data": {"config": {"expression": "inputs['topic']"}},
                },
            ],
            "edges": [
                {"id": "e1", "source": "ask", "target": "show"},
                {"id": "e2", "source": "show", "target": "echo"},
            ],
        }
    )
    graph = compile_graph(definition, registry=registry)
    emitter = RaiseOnEmit()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    # The emit raises, but it is best-effort: the run completes and routing holds.
    result = await scheduler.run(run_id="run-emit-fail", node_inputs={"ask": {"topic": "WW2"}})
    assert result.status is RunStatus.COMPLETED
    completed = [e for e in _data_events(emitter) if e.get("event") == "run_completed"][0]
    assert completed["last_outputs"]["echo"]["result"] == "WW2"


def test_to_frontend_shape_modes():
    from matrx_graph.nodes.output.to_frontend import ToFrontendConfig, ToFrontendExecutor

    payload = {"items": [1, 2, 3], "name": "x"}
    shape = ToFrontendExecutor._shape

    assert shape(ToFrontendConfig(mode="confirmation", message="Ready"), payload, payload) == {
        "message": "Ready"
    }
    assert shape(ToFrontendConfig(mode="full"), payload, payload) == payload
    # summary projects via a dict literal + subscripts (no function calls — sandbox).
    assert shape(
        ToFrontendConfig(
            mode="summary",
            transform_expression="{'name': inputs['name'], 'first': inputs['items'][0]}",
        ),
        payload,
        payload,
    ) == {"name": "x", "first": 1}
    # a non-dict transform result gets wrapped as {value: ...}.
    assert shape(
        ToFrontendConfig(mode="restructured", transform_expression="inputs['items'][0]"),
        payload,
        payload,
    ) == {"value": 1}
    # payload_key selects a sub-key (the executor extracts `data` before _shape).
    nested = {"result": {"a": 1}}
    assert shape(ToFrontendConfig(mode="full", payload_key="result"), nested, nested["result"]) == {
        "a": 1
    }



def test_to_frontend_payload_key_dotted_path():
    from matrx_graph.nodes.output.to_frontend import _pick

    payload = {"report": {"structured_output": {"__kind": "brief", "title": "x"}}, "a.b": 1}
    assert _pick(payload, "report.structured_output") == {"__kind": "brief", "title": "x"}
    # An exact top-level key wins over path-walking (keys may contain dots).
    assert _pick(payload, "a.b") == 1
    assert _pick(payload, "report.missing.deeper") is None
