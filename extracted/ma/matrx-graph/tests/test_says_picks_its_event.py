"""Guard (Says picks its event, 2026-11-19): a ``data.says`` row may pick each line's event from a DECLARED set.

``event_from`` (one placeholder) + ``events`` (value -> event name) + optional ``default``: the line carries the
declared name its value picks; a missing or undeclared value says the default, or nothing (flagged) — never a
failed run. ``each`` (one placeholder naming a list) says one line per element (``{each.x}``), so a step that
settles many things at once says a line per thing with no For each. Publish refuses a row whose names are not
declared. Real ``Scheduler`` + ``MemoryCheckpointer``; no doubles.
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
    validate_definition,
)
from matrx_graph import run_log
from matrx_graph.errors import CompilationError
from matrx_graph.run_log import RunLogEntry
from tests._fixtures import FakeEmitter, make_app_context

PICK = {"event_from": "{result.kind}", "events": {"done": "page_complete", "skip": "page_skipped"}}


def _definition(kinds: list[str], says_each: list[dict[str, Any]], says_list: list[dict[str, Any]]) -> dict[str, Any]:
    pages = "{'pages': [" + ", ".join(f"{{'n': {i}, 'kind': '{k}'}}" for i, k in enumerate(kinds)) + "]}"
    return {
        "nodes": [
            {"id": "pages", "type": "data.transform", "position": {"x": 0, "y": 0},
             "data": {"config": {"expression": pages}, "says": says_list}},
            {"id": "read", "type": "data.transform", "position": {"x": 300, "y": 0},
             "data": {"for_each": {"as": "page"}, "says": says_each,
                      "config": {"expression": "{'n': inputs['page']['n'], 'kind': inputs['page']['kind']}"}}},
        ],
        "edges": [{"id": "e1", "source": "pages", "target": "read",
                   "data": {"kind": "data", "mappings": {"items": "pages"}}}],
        "entry_nodes": ["pages"],
    }


def _registry() -> NodeRegistry:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    return registry


def _events(emitter: FakeEmitter, name: str) -> list[dict[str, Any]]:
    return [e for kind, e in emitter.events if kind == "data" and isinstance(e, dict) and e.get("event") == name]


class _Recorder:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    async def __call__(self, **kw: Any) -> RunLogEntry:
        self.rows.append(kw)
        return RunLogEntry(recorded=True, entry_id=str(len(self.rows)), label=kw["label"], needs_review=kw["needs_review"])


async def test_each_item_says_the_declared_event_its_value_picks_and_nothing_else() -> None:
    each = [{"on": "each_item", **PICK, "message": "Page {result.n}"}]
    # The list step says one line per element of its result, picked per element, with a declared default.
    listed = [{"on": "done", "each": "{result.pages}", "event_from": "{each.kind}",
               "events": {"done": "page_queued", "skip": "page_waiting"}, "default": "page_queued",
               "message": "Page {each.n}"}]
    definition = _definition(["done", "skip", "odd", "done"], each, listed)
    rec = _Recorder()
    run_log.configure_run_log_writer(rec)
    try:
        emitter = FakeEmitter()
        graph = compile_graph(Definition.model_validate(definition), registry=_registry())
        result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=_registry()).run(
            run_id="says-picks")
    finally:
        run_log.configure_run_log_writer(None)
    assert result.status is RunStatus.COMPLETED, result.error

    listed_lines = [e["says"] for e in _events(emitter, "node_completed") if e["node_id"] == "pages"]
    assert listed_lines == [[
        {"event": "page_queued", "message": "Page 0"}, {"event": "page_waiting", "message": "Page 1"},
        {"event": "page_queued", "message": "Page 2"},  # "odd" is not declared: the declared default
        {"event": "page_queued", "message": "Page 3"},
    ]], listed_lines

    by_item = {e["item_index"]: e["says"] for e in _events(emitter, "item_settled")}
    assert by_item[0] == [{"event": "page_complete", "message": "Page 0"}]
    assert by_item[1] == [{"event": "page_skipped", "message": "Page 1"}]
    assert by_item[3] == [{"event": "page_complete", "message": "Page 3"}]
    # "odd" picks nothing and there is no default: the item says nothing, the run goes on, flagged once.
    assert by_item[2] is None, by_item
    every = {line["event"] for e in _events(emitter, "item_settled") + _events(emitter, "node_completed")
             for line in (e.get("says") or [])}
    assert every <= {"page_complete", "page_skipped", "page_queued", "page_waiting"}, every
    flags = [r for r in rec.rows if r["label"] == "engine.says_failed"]
    assert len(flags) == 1 and "{result.kind}" in flags[0]["message"], flags


@pytest.mark.parametrize(("row", "words"), [
    ({"on": "each_item", "event_from": "{result.kind}", "message": ""}, "declares"),
    ({"on": "each_item", **PICK, "default": "page_gone", "message": ""}, "not one of the declared events"),
    ({"on": "each_item", "event_from": "{result.kind}", "events": {"a": "Not A Name"}, "message": ""},
     "is not an event name"),
    ({"on": "each_item", "event_from": "kind", "events": {"a": "x"}, "message": ""}, "one placeholder"),
    ({"on": "each_item", "event": "x", "events": {"a": "y"}, "message": ""}, "go with event_from"),
    ({"on": "each_item", "message": "no name"}, "one of the two"),
    ({"on": "each_item", "event": "x", "message": "{each.n}"}, "add each"),
    ({"on": "done", "each": "{each.n}", "event": "x", "message": ""}, "not {each.x}"),
])
def test_publish_refuses_a_row_whose_events_are_not_declared(row: dict[str, Any], words: str) -> None:
    definition = _definition(["done"], [row], [])
    with pytest.raises(CompilationError, match="says") as info:
        compile_graph(Definition.model_validate(definition), registry=_registry())
    assert words in str(info.value), (row, str(info.value))
    issues = [i for i in validate_definition(definition, registry=_registry()).issues if i.code == "says_invalid"]
    assert issues and words in issues[0].message, issues


def test_a_picked_row_is_held_to_its_row_type_like_any_row() -> None:
    """``event_from`` and ``each`` read placeholders too: ``{result.x}`` on start can never have a value."""
    definition = _definition(["done"], [{"on": "start", **PICK, "message": ""}],
                             [{"on": "start", "each": "{result.pages}", "event": "x", "message": ""}])
    found = [i.message for i in validate_definition(definition, registry=_registry()).issues
             if i.code == "says_never_has_a_value"]
    assert len(found) == 2 and all("{result." in f for f in found), found
    ok = _definition(["done"], [{"on": "each_item", **PICK, "message": ""}],
                     [{"on": "done", "each": "{result.pages}", "event": "x", "message": "{each.n}"}])
    compile_graph(Definition.model_validate(ok), registry=_registry())
