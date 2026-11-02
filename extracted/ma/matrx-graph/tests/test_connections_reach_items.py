"""A connection picks, renames, defaults and slices — so no step exists only to move data.

Live shape this replaces (Plan research keywords v65, 2026-10-27): of 11 steps only two
do work. A map_template read four fields with defaults ("Read the plan's fields"), a
transform chose "the planner's title, else the subject" ("The plan"), and two data.limit
steps cut the keyword list. Each is now a source on the connection:

    ``title ?? fallback_title``         either-or
    ``keywords ?? []``                  default
    ``keywords[0:3]`` / ``keywords[3:]``  slice
    ``pages[*].{id: page_id, title}``   pick + rename from each item

All driven through the real Scheduler and the real validator.
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
from matrx_graph.paths import path_syntax_problem, resolve_path
from matrx_graph.validation import validate_definition

from tests._fixtures import FakeEmitter, make_app_context

PLAN = {
    "title": None,
    "subject": "Solar storage",
    "keywords": ["batteries", "grid", "cost", "policy"],
    "pages": [
        {"page_id": "p1", "title": "Why batteries", "score": 9},
        {"page_id": "p2", "score": 3},
    ],
}


def _registry() -> NodeRegistry:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    return registry


def _transform(nid: str, expression: str) -> dict[str, Any]:
    return {"id": nid, "type": "data.transform", "position": {"x": 0, "y": 0},
            "data": {"config": {"expression": expression}}}


def _two_steps(mappings: dict[str, str]) -> dict[str, Any]:
    return {
        "nodes": [_transform("plan", repr(PLAN)), _transform("use", "inputs")],
        "edges": [{"id": "e", "source": "plan", "target": "use",
                   "data": {"kind": "data", "mappings": mappings}}],
    }


async def _delivered(mappings: dict[str, str]) -> dict[str, Any]:
    registry = _registry()
    graph = compile_graph(Definition.model_validate(_two_steps(mappings)), registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry)
    result = await scheduler.run(run_id="reach")
    assert result.status is RunStatus.COMPLETED, result.error
    return result.last_outputs["use"]


async def test_one_connection_does_what_four_reshape_steps_did() -> None:
    got = await _delivered({
        "title": "title ?? subject",
        "kept": "keywords[0:3]",
        "dropped": "keywords[3:]",
        "pages": "pages[*].{id: page_id, title: title ?? \"untitled\"}",
        "missing": "goals ?? {}",
    })
    assert got == {
        "title": "Solar storage",
        "kept": ["batteries", "grid", "cost"],
        "dropped": ["policy"],
        "pages": [{"id": "p1", "title": "Why batteries"}, {"id": "p2", "title": "untitled"}],
        "missing": {},
    }


async def test_each_item_becomes_a_record_with_at() -> None:
    got = await _delivered({"rows": "keywords[:2].{keyword: @, kind: 'search'}"})
    assert got == {"rows": [{"keyword": "batteries", "kind": "search"}, {"keyword": "grid", "kind": "search"}]}


@pytest.mark.parametrize("source,expected", [
    ("title ?? subject", "Solar storage"),
    ("title ?? \"\"", ""),
    ("nothing ?? other ?? 0", 0),
    ("subject ?? \"x\"", "Solar storage"),
    ("pages[*].{id: page_id}", [{"id": "p1"}, {"id": "p2"}]),
    ("{first: keywords[0], n: missing ?? 3}", {"first": "batteries", "n": 3}),
    ("keywords[-1]", "policy"),
])
def test_the_resolver_reads_every_form(source: str, expected: Any) -> None:
    assert path_syntax_problem(source) is None, path_syntax_problem(source)
    assert resolve_path(PLAN, source) == (True, expected)


def test_a_plain_path_reads_exactly_as_before() -> None:
    assert resolve_path(PLAN, "title") == (True, None)
    assert resolve_path(PLAN, "nope") == (False, None)
    assert resolve_path({"true": 1}, "true") == (True, 1), "a key named like a literal stopped reading"
    assert resolve_path({"a.b": 1}, "a\\.b") == (True, 1)


@pytest.mark.parametrize("bad", ["a ?? ", "a.{}", "a{b}", "a[1:x]", "a.{x: b[]}", "a.{x"])
def test_an_unreadable_source_is_refused(bad: str) -> None:
    assert path_syntax_problem(bad) is not None


def test_validation_refuses_a_typo_in_any_alternative_on_a_closed_output() -> None:
    defn = {
        "nodes": [
            {"id": "a", "type": "data.limit", "position": {"x": 0, "y": 0},
             "data": {"config": {"count": 2}}},
            _transform("b", "inputs"),
        ],
        "edges": [{"id": "e", "source": "a", "target": "b",
                   "data": {"kind": "data", "mappings": {"x": "items ?? itemz ?? []"}}}],
    }
    issues = [i for i in validate_definition(defn, _registry()).issues if i.severity == "error"]
    assert any("itemz" in i.message for i in issues), [i.message for i in issues]
    defn["edges"][0]["data"]["mappings"] = {"x": "items[0:1] ?? []"}
    issues = [i for i in validate_definition(defn, _registry()).issues if i.severity == "error"]
    assert not issues, [i.message for i in issues]


def test_a_pick_field_may_be_a_fixed_value() -> None:
    got = resolve_path(PLAN, 'pages.{url: page_id, error: null, status: "failed", n: 0}')
    assert got == (True, [
        {"url": "p1", "error": None, "status": "failed", "n": 0},
        {"url": "p2", "error": None, "status": "failed", "n": 0},
    ])


def test_a_list_template_section_repeats_for_each_nested_item() -> None:
    """Research one keyword spent For each → render → Gather (3 steps) per nested list
    (key facts, core findings, snippets); a section is that, inside one render step."""
    from matrx_graph.nodes._template import render_template_string

    analysis = {"title": "T", "age": "2d", "snippets": ["s1", "s2", "s3"],
                "facts": ["f1", "f2"], "findings": [{"finding": "F", "why": "S"}], "none": []}
    template = (
        "### {title}{#age} [{item}]{/age}{#snippets[0:2]}\n  {item}{/snippets[0:2]}\n"
        "{#facts.0}**Key facts:**\n{/facts.0}{#facts}- {item}\n{/facts}"
        "{#findings}- {finding} ({why})\n{/findings}{#none}never{/none}{^none}(no notes){/none}"
    )
    assert render_template_string(template, analysis)[0] == (
        "### T [2d]\n  s1\n  s2\n**Key facts:**\n- f1\n- f2\n- F (S)\n(no notes)"
    )


@pytest.mark.parametrize("source,expected", [
    ("trim(a)", "Hello World"),
    ("lower(trim(a))", "hello world"),
    ("upper(l)", [" X ", "Y", 3]),
    ("trim(n) ?? \"z\"", "z"),
    ("trim(missing ?? a)", "Hello World"),
])
def test_a_source_tidies_text(source: str, expected: Any) -> None:
    """Vision Interview had 6 text.case steps that only trimmed one answer."""
    data = {"a": "  Hello   World ", "l": [" X ", "y", 3], "n": None}
    assert path_syntax_problem(source) is None
    assert resolve_path(data, source) == (True, expected)


def test_a_bad_path_inside_a_function_is_refused() -> None:
    assert path_syntax_problem("trim()") is not None
    assert path_syntax_problem("trim(a[])") is not None


def test_hash_is_the_items_position() -> None:
    data = {"p": [{"u": "a"}, None, {"u": "b"}]}
    assert resolve_path(data, "p.{n: #, u}") == (True, [{"n": 0, "u": "a"}, {"n": 2, "u": "b"}])
    assert resolve_path(data, "p[*].{n: #, u}") == (True, [{"n": 0, "u": "a"}, {"n": 2, "u": "b"}])


async def test_join_fills_the_fields_an_unmatched_item_lacks() -> None:
    """Research one keyword: a candidate never read still carries status / good like a read one."""
    from matrx_graph.nodes.data.join import DataJoinExecutor, JoinConfig, JoinInput

    out = await DataJoinExecutor().execute(
        None,  # type: ignore[arg-type]
        JoinInput(items=[{"url": "a", "title": "A"}, {"url": "b", "title": "B"}],
                  other=[{"url": "a", "good": True, "status": "read"}]),
        JoinConfig(key="url", mode="merge", unmatched_fill={"good": False, "status": "not_read", "title": "x"}),
    )
    assert out.result.items == [
        {"url": "a", "title": "A", "good": True, "status": "read"},
        {"url": "b", "title": "B", "good": False, "status": "not_read"},
    ]


@pytest.mark.parametrize("source", [
    "title ?? subject ?? \"\"",
    "keywords[0:3]",
    "keywords[3:]",
    "keywords[0:3] ?? []",
    "pages[*].{id: page_id, title: title ?? \"untitled\"}",
    "pages.{n: #, url: page_id, error: null, kind: 'search'}",
    "keywords.{keyword: @}",
    "{first: keywords[0], n: missing ?? 3}",
    "trim(subject) ?? \"\"",
    "lower(trim(subject))",
])
def test_every_expression_form_saves_through_validation(source: str) -> None:
    """The ONE save check (validate_definition) accepts every form the resolver reads, so the
    path check and the resolver can never drift (2026-10-28: an old checker refused them)."""
    issues = validate_definition(_two_steps({"x": source}), _registry()).issues
    assert not [i for i in issues if i.severity == "error"], [i.message for i in issues]
