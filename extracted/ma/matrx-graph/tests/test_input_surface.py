"""THE INPUT SURFACE (INPUT-SURFACE.md, ruled 2026-08-27) — engine contract.

Covers: the compiled name-unique surface (fields + folded variables, kind
mapping, sourcing rules, named variants, declared-kind passthrough), the
named collision refusal, {'$input': name} resolution (loud on undeclared
names, defaults, edge payloads never scanned), park-not-die (a headless
start missing a require/ask input returns AWAITING_INPUT — never a crash),
and the ask-needs-a-human-stamp rule.
"""

from __future__ import annotations

import pytest

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.errors import CompilationError, UnresolvedInputError
from matrx_graph.types.input_surface import InputSpec, unsatisfied_inputs
from matrx_graph.types.variables import input_ref, resolve_var_refs

from tests._fixtures import FakeEmitter, make_app_context


@pytest.fixture(scope="module", autouse=True)
def _register() -> None:
    register_builtin_nodes(overwrite=True)


def _input_node(node_id: str, fields: list[dict], **extra) -> dict:
    return {
        "id": node_id,
        "type": "io",
        "position": {"x": 0, "y": 0},
        "data": {"spec_type": "io.user_input", "config": {"fields": fields}, **extra},
    }


def _definition(nodes: list[dict], edges: list[dict] | None = None, **kw) -> Definition:
    return Definition.model_validate({"nodes": nodes, "edges": edges or [], **kw})


# ---------------------------------------------------------------------------
# The compiled surface
# ---------------------------------------------------------------------------


def test_surface_unions_fields_and_folds_variables() -> None:
    d = _definition(
        [
            _input_node(
                "in1",
                [
                    {"key": "topic", "label": "Topic", "type": "text", "required": True},
                    {"key": "count", "type": "number"},
                ],
            ),
            _input_node("in2", [{"key": "style", "type": "long_text"}]),
        ],
        variables=[{"name": "tone", "default": "friendly"}],
    )
    g = compile_graph(d)
    surface = g.input_surface
    assert set(surface) == {"topic", "count", "style", "tone"}
    # Kind mapping for the legacy 6 field types.
    assert surface["topic"].kind == "text"
    assert surface["count"].kind == "number"
    assert surface["style"].kind == "text"
    # Presentation is a named variant — and the name is the one the KIND
    # REGISTRY seeds on kind "text", never a compiler-local coinage
    # (test_input_surface_variant_registry.py pins the whole table).
    assert surface["style"].variant == "textarea"
    # Sourcing: required → require; optional → optional; folded variable with
    # a default → optional.
    assert surface["topic"].sourcing == "require"
    assert surface["count"].sourcing == "optional"
    assert surface["tone"].sourcing == "optional"
    assert surface["tone"].origin == "variable"
    assert surface["tone"].default == "friendly"
    # Field origin carries the declaring node for engine seeding.
    assert surface["topic"].node_id == "in1"
    assert surface["style"].node_id == "in2"


def test_explicit_kind_sourcing_and_variant_pass_through() -> None:
    d = _definition(
        [
            _input_node(
                "in1",
                [
                    {
                        "key": "brief",
                        "type": "text",
                        "kind": "markdown",
                        "sourcing": "ask",
                        "variant": "slider",
                    }
                ],
            )
        ]
    )
    surface = compile_graph(d).input_surface
    assert surface["brief"].kind == "markdown"  # declared slug passes through
    assert surface["brief"].sourcing == "ask"  # explicit ask is authorable
    assert surface["brief"].variant == "slider"  # stored as the string, validated later


def test_yes_no_and_choice_map_to_boolean_and_text() -> None:
    d = _definition(
        [
            _input_node(
                "in1",
                [
                    {"key": "confirm", "type": "yes_no"},
                    {"key": "pick", "type": "choice", "options": ["a", "b"]},
                ],
            )
        ]
    )
    surface = compile_graph(d).input_surface
    assert surface["confirm"].kind == "boolean"
    assert surface["pick"].kind == "text"
    # "dropdown" is the registry's seeded single-select variant on kind "text".
    assert surface["pick"].variant == "dropdown"
    assert surface["pick"].options == ["a", "b"]


def test_field_collision_is_named_compile_refusal() -> None:
    d = _definition(
        [
            _input_node("a", [{"key": "topic", "type": "text"}]),
            _input_node("b", [{"key": "topic", "type": "text"}]),
        ]
    )
    with pytest.raises(CompilationError, match="topic"):
        compile_graph(d)


def test_variable_shadowing_field_is_named_compile_refusal() -> None:
    d = _definition(
        [_input_node("a", [{"key": "topic", "type": "text"}])],
        variables=[{"name": "topic", "default": "x"}],
    )
    with pytest.raises(CompilationError, match="topic"):
        compile_graph(d)


# ---------------------------------------------------------------------------
# $input resolution
# ---------------------------------------------------------------------------


def _surface(**specs: InputSpec) -> dict[str, InputSpec]:
    return dict(specs)


def test_input_ref_resolves_from_landed_values() -> None:
    surface = _surface(topic=InputSpec(name="topic", kind="text", sourcing="require"))
    out = resolve_var_refs(
        {"prompt": input_ref("topic")},
        run_variables={},
        declared={},
        node_id="n1",
        run_inputs={"topic": "volcanoes"},
        input_surface=surface,
    )
    assert out == {"prompt": "volcanoes"}


def test_input_ref_falls_back_to_declared_default() -> None:
    surface = _surface(
        tone=InputSpec(name="tone", kind="text", sourcing="optional", default="friendly")
    )
    out = resolve_var_refs(
        {"style": input_ref("tone")},
        run_variables={},
        declared={},
        node_id="n1",
        run_inputs={},
        input_surface=surface,
    )
    assert out == {"style": "friendly"}


def test_undeclared_input_ref_fails_loudly() -> None:
    with pytest.raises(UnresolvedInputError, match="nope"):
        resolve_var_refs(
            {"x": input_ref("nope")},
            run_variables={},
            declared={},
            node_id="n1",
            run_inputs={"nope": "value-present-but-undeclared"},
            input_surface={},
        )


def test_missing_input_value_without_default_fails_loudly() -> None:
    surface = _surface(topic=InputSpec(name="topic", kind="text", sourcing="require"))
    with pytest.raises(UnresolvedInputError, match="topic"):
        resolve_var_refs(
            {"x": input_ref("topic")},
            run_variables={},
            declared={},
            node_id="n1",
            run_inputs={},
            input_surface=surface,
        )


def test_validation_rejects_undeclared_input_marker() -> None:
    d = _definition(
        [
            _input_node("in1", [{"key": "topic", "type": "text"}]),
            {
                "id": "log1",
                "type": "log",
                "position": {"x": 0, "y": 0},
                "data": {
                    "spec_type": "log.record",
                    "input": {"message": {"$input": "not_declared"}},
                },
            },
        ]
    )
    with pytest.raises(CompilationError, match="not_declared"):
        compile_graph(d)


# ---------------------------------------------------------------------------
# Sourcing-rule gate (unsatisfied_inputs)
# ---------------------------------------------------------------------------


def test_require_satisfied_by_any_source_including_default() -> None:
    surface = _surface(
        a=InputSpec(name="a", kind="text", sourcing="require", default="fallback"),
        b=InputSpec(name="b", kind="text", sourcing="require"),
    )
    gaps = unsatisfied_inputs(surface, {"b": "supplied"}, {"b": "caller"})
    assert gaps == []


def test_ask_satisfied_only_by_human_stamp() -> None:
    surface = _surface(q=InputSpec(name="q", kind="text", sourcing="ask", default="preset"))
    # A caller value does NOT satisfy ask; neither does the default.
    assert [g.name for g in unsatisfied_inputs(surface, {"q": "v"}, {"q": "caller"})] == ["q"]
    assert [g.name for g in unsatisfied_inputs(surface, {}, {})] == ["q"]
    # A human-stamped value does.
    assert unsatisfied_inputs(surface, {"q": "v"}, {"q": "human"}) == []


def test_gate_skips_unreferenced_variables_and_edge_fed_fields() -> None:
    surface = _surface(
        v=InputSpec(name="v", kind="text", sourcing="require", origin="variable", referenced=False),
        f=InputSpec(name="f", kind="text", sourcing="require", edge_fed=True),
    )
    assert unsatisfied_inputs(surface, {}, {}) == []


# ---------------------------------------------------------------------------
# Park-not-die — the scheduler-level guarantee
# ---------------------------------------------------------------------------


async def test_headless_start_missing_require_input_parks_not_dies() -> None:
    d = _definition(
        [_input_node("in1", [{"key": "topic", "type": "text", "required": True}])]
    )
    graph = compile_graph(d)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(FakeEmitter()))
    result = await scheduler.run(run_id="run-park-1", max_steps=10)
    assert result.status is RunStatus.AWAITING_INPUT
    assert result.interrupt is not None
    assert result.interrupt["kind"] == "awaiting_input"
    assert [m["name"] for m in result.interrupt["missing"]] == ["topic"]
    assert result.error is None  # a park is not a failure


async def test_start_with_surface_value_runs_to_completion() -> None:
    d = _definition(
        [_input_node("in1", [{"key": "topic", "type": "text", "required": True}])]
    )
    graph = compile_graph(d)
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        surface_inputs={"topic": "volcanoes"},
        input_provenance={"topic": "caller"},
    )
    result = await scheduler.run(run_id="run-park-2", max_steps=10)
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["in1"]["topic"] == "volcanoes"


async def test_legacy_node_inputs_still_satisfy_and_seed() -> None:
    """Compat: today's run-form channel (node_inputs) keeps working — the
    gate accepts it and the executor still receives the value."""
    d = _definition(
        [_input_node("in1", [{"key": "topic", "type": "text", "required": True}])]
    )
    graph = compile_graph(d)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(FakeEmitter()))
    result = await scheduler.run(
        run_id="run-park-3", max_steps=10, node_inputs={"in1": {"topic": "legacy"}}
    )
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["in1"]["topic"] == "legacy"


async def test_ask_input_parks_headless_even_with_caller_value() -> None:
    d = _definition(
        [_input_node("in1", [{"key": "q", "type": "text", "sourcing": "ask"}])]
    )
    graph = compile_graph(d)
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        surface_inputs={"q": "machine-supplied"},
        input_provenance={"q": "caller"},
    )
    result = await scheduler.run(run_id="run-park-4", max_steps=10)
    assert result.status is RunStatus.AWAITING_INPUT
    # And a human-stamped value releases it.
    scheduler2 = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        surface_inputs={"q": "typed by a person"},
        input_provenance={"q": "human"},
    )
    result2 = await scheduler2.run(run_id="run-park-5", max_steps=10)
    assert result2.status is RunStatus.COMPLETED, result2.error


# ---------------------------------------------------------------------------
# Input hints (third-party services L6a — INPUT-HINTS.md)
# ---------------------------------------------------------------------------


def test_input_hints_travel_from_field_to_surface() -> None:
    d = _definition(
        [
            _input_node(
                "in1",
                [
                    {
                        "key": "domain",
                        "label": "Website",
                        "required": True,
                        "primary": True,
                        "detect": ["domain", "url"],
                        "example": "ahrefs.com",
                    },
                    {
                        "key": "country",
                        "type": "choice",
                        "options": ["us", "gb"],
                        "default": "us",
                        "advanced": True,
                        "group": "Location",
                        "order": 2,
                        "choice_style": "chips",
                        "option_labels": {"us": "United States", "gb": "United Kingdom"},
                    },
                    {"key": "plain", "type": "text"},
                ],
            )
        ]
    )
    surface = compile_graph(d).input_surface
    domain, country, plain = surface["domain"], surface["country"], surface["plain"]
    assert domain.primary is True and domain.detect == ["domain", "url"]
    assert domain.example == "ahrefs.com"
    assert country.advanced is True and country.group == "Location" and country.order == 2
    assert country.choice_style == "chips"
    assert country.option_labels == {"us": "United States", "gb": "United Kingdom"}
    # Absent means "infer" — never a guessed value on the server.
    assert plain.primary is False and plain.advanced is None and plain.detect == []


def test_unknown_detect_type_is_refused_by_name() -> None:
    with pytest.raises(Exception, match="detect"):
        compile_graph(_definition([_input_node("in1", [{"key": "q", "detect": ["zipcode"]}])]))
