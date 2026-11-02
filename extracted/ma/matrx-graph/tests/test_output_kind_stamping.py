"""SETTLEMENT STAMPING — a node payload SAYS what it is, on EVERY path.

THE `__kind` MARKER LAW (KINDS_EVERYWHERE_PLAN §4.2a) belongs to the payload,
not to the scheduler. 46 of the 89 registered nodes (measured 2026-09-09) have
payload models that predate ``KindModel`` and carry no marker of their own — 36
of those declare an ``output_kind``, so their identity has to be stamped from
the registration. It was, but only at the scheduler's settlement; the isolated
node-test path and ``tool.call``'s inner dispatch dump payloads settlement never
sees, and both shipped anonymous. Live symptom (feedback 901956d7): the Studio's
"Text to Data" Test Step (``data.parse_json``, declared kind ``value``) came back
"(root) must have required property '__kind'" on a step that worked.

One helper, ``matrx_graph.content_ir.envelope.stamp_kind_marker``, is now the
one place that decides identity, and these pin its three load-bearing rules
plus the real end-to-end scheduler behavior.
"""

from __future__ import annotations

import json

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.content_ir.envelope import stamp_kind_marker

from tests._fixtures import FakeEmitter, make_app_context

#: A parsed value that IS a kind instance — its own marker lives one level down
#: from the wrapper's and must survive every stamp untouched.
INNER = {"__kind": "directive_v1_create_task", "items": [{"name": "x"}]}


# ---------------------------------------------------------------------------
# The helper's rules
# ---------------------------------------------------------------------------


def test_stamps_the_declared_kind_on_an_anonymous_root():
    dump = {"archetype": "value", "value": 1}
    assert stamp_kind_marker(dump, "value")["__kind"] == "value"


def test_never_overwrites_a_marker_the_payload_declared_itself():
    # A KindModel payload already said what it is; the registration does not
    # get to overrule the data.
    dump = {"__kind": "web_result", "url": "https://x"}
    assert stamp_kind_marker(dump, "value")["__kind"] == "web_result"


def test_never_reaches_into_a_nested_marker():
    dump = {"archetype": "value", "value": dict(INNER)}
    stamp_kind_marker(dump, "value")
    assert dump["value"] == INNER, "a nested marker is the nested value's identity"


def test_json_is_a_format_word_and_never_an_identity():
    dump = {"a": 1}
    assert "__kind" not in stamp_kind_marker(dump, "json")


def test_an_undeclared_kind_stamps_nothing():
    dump = {"a": 1}
    assert "__kind" not in stamp_kind_marker(dump, None)


def test_a_non_dict_payload_is_returned_untouched():
    assert stamp_kind_marker([1, 2], "value") == [1, 2]


# ---------------------------------------------------------------------------
# The real thing: the reported node, through the real scheduler
# ---------------------------------------------------------------------------


async def test_text_to_data_settles_with_its_declared_kind_and_keeps_the_inner_one():
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    assert registry.get("data.parse_json").spec.output_kind == "value"

    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "parse-1",
                    "type": "data.parse_json",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}, "input": {"text": json.dumps(INNER)}},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(definition, registry=registry)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )
    result = await scheduler.run(run_id="stamp-1")

    assert result.status is RunStatus.COMPLETED
    settled = result.last_outputs["parse-1"]
    assert settled["__kind"] == "value"
    assert settled["value"] == INNER
