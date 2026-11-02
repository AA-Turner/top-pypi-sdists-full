"""Built-in step settings — Only when · If skipped · Shape the result — and the list preset.

The live shape this replaces (Plan research keywords, 2026-10-27): "optionally let a person edit the
keyword list" took FIVE steps — render the list as lines, a transform feeding a conditional
connection, the pause, a split back into a list, and a merge picking the edited or the original
list. Here it is ONE pause step, and both paths run on the real engine.
"""

from __future__ import annotations

from typing import Any

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.step_settings import expand_step_settings, owner_of
from matrx_graph.validation import validate_definition

from tests._fixtures import FakeEmitter, make_app_context


def _transform(nid: str, expression: str) -> dict[str, Any]:
    return {"id": nid, "type": "data.transform", "position": {"x": 0, "y": 0},
            "data": {"config": {"expression": expression}}}


def _edit_step(**settings: Any) -> dict[str, Any]:
    return {
        "id": "edit",
        "type": "control.human_input",
        "position": {"x": 300, "y": 0},
        "data": {
            "label": "A person edits the keywords",
            "config": {"preset": "list", "title": "Edit the keywords", "prompt": "One keyword per line."},
            **settings,
        },
    }


_ALL_SETTINGS = {
    "when": "inputs['review']",
    "if_skipped": "{'keywords': inputs['items'], 'reviewed': False}",
    "shape": "{'keywords': inputs['answer'], 'reviewed': True}",
}


def _definition(review: bool, **settings: Any) -> dict[str, Any]:
    return {
        "nodes": [
            _transform("plan", f"{{'keywords': ['alpha', 'beta', 'gamma'], 'review': {review}}}"),
            _edit_step(**(settings or _ALL_SETTINGS)),
            _transform("result", "{'keywords': inputs['keywords'], 'reviewed': inputs['reviewed']}"),
        ],
        "edges": [
            {"id": "e_plan_edit", "source": "plan", "target": "edit",
             "data": {"kind": "data", "mappings": {"items": "keywords", "review": "review"}}},
            {"id": "e_edit_result", "source": "edit", "target": "result",
             "data": {"kind": "data", "mappings": {"keywords": "keywords", "reviewed": "reviewed"}}},
        ],
    }


def _registry() -> NodeRegistry:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    return registry


def _scheduler(defn: dict[str, Any]) -> tuple[Scheduler, MemoryCheckpointer]:
    registry = _registry()
    graph = compile_graph(Definition.model_validate(defn), registry=registry)
    checkpointer = MemoryCheckpointer()
    return Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry), checkpointer


async def test_when_says_no_the_step_never_runs_and_its_skipped_result_flows_on() -> None:
    scheduler, _ = _scheduler(_definition(review=False))
    result = await scheduler.run(run_id="settings-skip")
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["result"] == {"keywords": ["alpha", "beta", "gamma"], "reviewed": False}
    assert "edit" not in result.last_outputs, "the step ran although 'Only when' said no"


async def test_when_says_yes_the_person_edits_lines_and_the_shaped_list_flows_on() -> None:
    scheduler, checkpointer = _scheduler(_definition(review=True))
    paused = await scheduler.run(run_id="settings-ask")
    assert paused.status is RunStatus.INTERRUPTED, paused.error
    payload = paused.interrupt["payload"]
    assert payload["preset"] == "list"
    assert payload["default_answer"] == "alpha\nbeta\ngamma", "the person was not handed the list to edit"

    parked = await checkpointer.latest_checkpoint("settings-ask")
    resumed = await scheduler.resume(
        run_id="settings-ask",
        checkpoint_id=parked.checkpoint_id,
        resume_value={"answer": "  alpha \n\ndelta\n"},
    )
    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert resumed.last_outputs["result"] == {"keywords": ["alpha", "delta"], "reviewed": True}


async def test_only_when_without_if_skipped_prunes_like_a_connection_not_taken() -> None:
    defn = _definition(review=False, when="inputs['review']")
    defn["nodes"][2] = _transform("result", "{'n': len(inputs['all']), 'edited': 'answer' in inputs}")
    defn["edges"] = [
        defn["edges"][0],
        {"id": "e_edit_result", "source": "edit", "target": "result",
         "data": {"kind": "data", "mappings": {"answer": "answer"}}},
        {"id": "e_plan_result", "source": "plan", "target": "result",
         "data": {"kind": "data", "mappings": {"all": "keywords"}}},
    ]
    scheduler, _ = _scheduler(defn)
    result = await scheduler.run(run_id="settings-prune")
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["result"] == {"n": 3, "edited": False}


def test_the_authored_definition_keeps_one_card() -> None:
    authored = Definition.model_validate(_definition(review=True))
    expanded = expand_step_settings(authored)
    assert [n.id for n in authored.nodes] == ["plan", "edit", "result"], "expansion rewrote the author's JSON"
    helpers = {n.id for n in expanded.nodes} - {"plan", "edit", "result"}
    assert helpers == {"edit~when", "edit~shape", "edit~if_skipped"}
    assert {owner_of(h) for h in helpers} == {"edit"}
    assert owner_of("edit") is None


def test_a_skipped_result_without_only_when_is_refused_on_the_step() -> None:
    result = validate_definition(_definition(review=True, if_skipped="{'keywords': []}"), _registry())
    assert not result.valid
    assert [(i.node_id, "never skipped" in i.message) for i in result.issues] == [("edit", True)]


def test_a_problem_inside_a_setting_is_badged_on_the_step_the_author_wrote() -> None:
    result = validate_definition(_definition(review=True, when="inputs['review']", shape="__import__('os')"), _registry())
    bad = [i for i in result.issues if i.severity == "error"]
    assert bad, "a disallowed expression in 'Shape the result' passed validation"
    assert {i.node_id for i in bad} == {"edit"}, [(i.node_id, i.message) for i in bad]


def test_shaping_the_step_that_ends_the_workflow_is_refused_in_words() -> None:
    defn = _definition(review=True)
    defn["edges"] = defn["edges"][:1]
    defn["nodes"] = defn["nodes"][:2]
    issues = validate_definition(defn, _registry()).issues
    assert [(i.node_id, "ends the workflow" in i.message) for i in issues] == [("edit", True)]


def test_shaping_a_for_each_target_is_refused_naming_the_authors_step() -> None:
    defn = {
        "nodes": [
            _transform("items", "{'items': [1, 2]}"),
            {"id": "each", "type": "control.map", "position": {"x": 0, "y": 0},
             "data": {"config": {"target_node_id": "work", "items_path": "items"}}},
            {**_transform("work", "{'n': inputs['item']}"), "id": "work"},
        ],
        "edges": [{"id": "e1", "source": "items", "target": "each", "data": {"kind": "data"}}],
    }
    defn["nodes"][2]["data"]["shape"] = "{'n2': inputs['n']}"
    issues = validate_definition(defn, _registry()).issues
    assert [(i.node_id, "For each" in i.message) for i in issues] == [("work", True)]


def test_how_inputs_join_moves_to_the_gate_that_now_receives_them() -> None:
    defn = _definition(review=True, when="inputs['review']")
    defn["nodes"][1]["data"]["join_policy"] = "any"
    expanded = expand_step_settings(Definition.model_validate(defn))
    by_id = {n.id: n for n in expanded.nodes}
    assert by_id["edit~when"].data.get("join_policy") == "any"
    assert "join_policy" not in by_id["edit"].data


# --- Run once per item (data.for_each) ------------------------------------------------------


def _per_item(**for_each: Any) -> dict[str, Any]:
    return {
        "nodes": [
            _transform("pages", "{'pages': [{'url': 'a'}, {'url': 'b'}, {'url': 'c'}], 'topic': 'bread'}"),
            {"id": "read", "type": "data.transform", "position": {"x": 300, "y": 0},
             "data": {"label": "Read a page", "for_each": for_each,
                      "config": {"expression": "{'url': inputs['page']['url'], 'topic': inputs['topic']}"}}},
            _transform("report", "{'urls': [v['url'] for v in inputs['values']], 'n': inputs['n']}"),
        ],
        "edges": [
            {"id": "e1", "source": "pages", "target": "read",
             "data": {"kind": "data", "mappings": {"items": "pages", "topic": "topic"}}},
            {"id": "e2", "source": "read", "target": "report",
             "data": {"kind": "data", "mappings": {"values": "values", "n": "count"}}},
        ],
    }


async def test_a_step_set_to_run_once_per_item_gets_each_item_and_the_shared_inputs() -> None:
    scheduler, _ = _scheduler(_per_item(**{"as": "page"}))
    result = await scheduler.run(run_id="per-item")
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["report"] == {"urls": ["a", "b", "c"], "n": 3}


def test_run_once_per_item_keeps_one_card_and_its_helpers_badge_on_it() -> None:
    authored = Definition.model_validate(_per_item(**{"as": "page"}))
    expanded = expand_step_settings(authored)
    assert [n.id for n in authored.nodes] == ["pages", "read", "report"]
    assert {n.id for n in expanded.nodes} - {"pages", "read", "report"} == {"read~each", "read~gather"}
    assert {owner_of("read~each"), owner_of("read~gather")} == {"read"}


def test_run_once_per_item_without_a_list_named_items_is_refused_in_words() -> None:
    defn = _per_item()
    defn["edges"][0]["data"]["mappings"] = {"pages": "pages"}
    issues = validate_definition(defn, _registry()).issues
    assert [(i.node_id, "'items'" in i.message) for i in issues if i.severity == "error"] == [("read", True)]


def test_an_item_name_that_collides_with_a_shared_input_is_refused() -> None:
    defn = _per_item(**{"as": "topic"})
    issues = validate_definition(defn, _registry()).issues
    assert [(i.node_id, "name the item something else" in i.message) for i in issues if i.severity == "error"] == [("read", True)]


def _per_item_with_holes(**for_each: Any) -> dict[str, Any]:
    """'Read a page' fails on page 'b'; its failure is a hole, not the end of the run."""
    defn = _per_item(**for_each)
    read = defn["nodes"][1]
    read["data"]["on_item_failure"] = "hole"
    read["data"]["config"]["expression"] = "{'url': inputs['page']['url'], 'n': 1 // (0 if inputs['page']['url'] == 'b' else 1)}"
    defn["nodes"][2] = _transform("report", "inputs")
    defn["edges"][1]["data"]["mappings"] = {"pairs": "pairs", "holes": "holes", "values": "values"}
    return defn


async def test_run_once_per_item_with_pairs_hands_on_each_item_beside_its_result_and_names_every_hole() -> None:
    """Gap 9: 'Run once per item' can say which item each result (and each hole) came from, like a
    Gather's ``items_from`` — so the For each -> step -> Gather trio with items_from folds too."""
    scheduler, _ = _scheduler(_per_item_with_holes(**{"as": "page", "pairs": True}))
    result = await scheduler.run(run_id="per-item-pairs")
    assert result.status is RunStatus.COMPLETED, result.error
    report = result.last_outputs["report"]
    assert report["values"] == [{"url": "a", "n": 1}, {"url": "c", "n": 1}]
    assert [(p["item_index"], p["item"], p["value"]) for p in report["pairs"]] == [
        (0, {"url": "a"}, {"url": "a", "n": 1}),
        (2, {"url": "c"}, {"url": "c", "n": 1}),
    ]
    assert [(h["item_index"], h["item"]) for h in report["holes"]] == [(1, {"url": "b"})]


async def test_run_once_per_item_without_pairs_hands_on_no_items() -> None:
    scheduler, _ = _scheduler(_per_item_with_holes(**{"as": "page"}))
    result = await scheduler.run(run_id="per-item-no-pairs")
    assert result.status is RunStatus.COMPLETED, result.error
    report = result.last_outputs["report"]
    assert report["pairs"] == [] and [h.get("item") for h in report["holes"]] == [None]


def test_pairs_is_on_or_off_and_needs_one_list_connection() -> None:
    issues = validate_definition(_per_item(**{"pairs": "yes"}), _registry()).issues
    assert [(i.node_id, "true / false" in i.message) for i in issues if i.severity == "error"] == [("read", True)]
