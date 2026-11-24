"""A step key nothing reads is SAID by the validator (L-REPLAY2, 2026-11-10).

``on_failure: continue`` sat in the ``data`` of 274 live steps and did nothing: ``NodeDef.data`` is free-form, so
the engine accepted and ignored it, and a refused analyst failed the whole page run the author thought was
guarded. The rule is generic (any key outside ``STEP_DATA_KEYS``), a warning (a save is never refused for it),
and the list cannot fall behind the engine: every ``data.get("...")`` the engine's own source makes is in it.
Red before: ``validate_definition`` returned no issue naming ``on_failure``.
"""

from __future__ import annotations

import re
from pathlib import Path

import matrx_graph
from matrx_graph.types.definition import STEP_DATA_KEYS, Definition
from matrx_graph.validation import _unknown_step_key_issues


def _definition(data: dict, **on_the_step: object) -> Definition:
    return Definition.model_validate({"nodes": [
        {"id": "ask", "type": "action", "position": {"x": 0, "y": 0}, "data": data, **on_the_step}]})


def test_a_key_nothing_reads_is_named_as_a_warning() -> None:
    (issue,) = _unknown_step_key_issues(_definition({"spec_type": "ai.mandate.start", "on_failure": "continue"}))
    assert issue.severity == "warning" and issue.node_id == "ask" and issue.path == "nodes[ask].data.on_failure"
    assert "'on_failure'" in issue.message and "does nothing" in issue.message


def test_any_unknown_key_is_said_not_one_listed_name() -> None:
    issues = _unknown_step_key_issues(_definition({"config": {}, "retry_on_error": 3, "onFailure": "x"}))
    assert [i.path for i in issues] == ["nodes[ask].data.onFailure", "nodes[ask].data.retry_on_error"]


def test_a_step_key_written_beside_data_is_told_where_it_belongs() -> None:
    (issue,) = _unknown_step_key_issues(_definition({"config": {}}, is_primary=True, measured={"width": 1}))
    assert issue.path == "nodes[ask].is_primary" and "data.is_primary" in issue.message


def test_the_keys_saved_workflows_carry_are_quiet() -> None:
    data = {key: None for key in STEP_DATA_KEYS}
    assert _unknown_step_key_issues(_definition(data)) == []


def test_every_key_the_engine_reads_is_a_known_key() -> None:
    read: set[str] = set()
    for path in Path(matrx_graph.__file__).parent.rglob("*.py"):
        read |= set(re.findall(r"""\bdata\.get\(\s*["']([A-Za-z_]+)["']""", path.read_text()))
    assert read and not (read - STEP_DATA_KEYS), f"read by the engine, missing from STEP_DATA_KEYS: {sorted(read - STEP_DATA_KEYS)}"


def test_the_helper_steps_a_step_setting_writes_out_carry_no_unknown_key() -> None:
    """The engine's own helper steps (`ask~when`, `ask~each`, ...) are checked too: publish runs this rule on the
    expanded definition. They carried `step_setting_of`, which nothing reads (a helper's owner is read from its
    id, ``step_settings.owner_of``), so every step with Only when / Shape / If skipped / For each warned
    "Unknown step key 'step_setting_of'" on a key no author wrote (plan workflow 1bb1290c: ask, ask_pick, pause)."""
    from matrx_graph.step_settings import STEP_SETTING_KEYS, expand_step_settings, owner_of

    step = {"spec_type": "data.transform", "config": {"expression": "{'x': 1}"}}
    source = {"id": "src", "type": "data", "position": {"x": 0, "y": 0},
              "data": {"spec_type": "data.transform", "config": {"expression": "{'items': [1]}"}}}
    expanded = expand_step_settings(Definition.model_validate({
        "nodes": [source,
                  {"id": "ask", "type": "data", "position": {"x": 0, "y": 0},
                   "data": {**step, **{key: "inputs['x']" for key in STEP_SETTING_KEYS}}},
                  {"id": "per", "type": "data", "position": {"x": 0, "y": 0}, "data": {**step, "for_each": {}}},
                  {"id": "end", "type": "data", "position": {"x": 0, "y": 0}, "data": step}],
        "edges": [{"id": "e1", "source": "src", "target": "ask", "data": {"mappings": {"x": "items"}}},
                  {"id": "e2", "source": "src", "target": "per", "data": {"mappings": {"items": "items"}}},
                  {"id": "e3", "source": "ask", "target": "end", "data": {"mappings": {"a": "x"}}},
                  {"id": "e4", "source": "per", "target": "end", "data": {"mappings": {"b": "results"}}}]}))
    helpers = sorted(n.id for n in expanded.nodes if owner_of(n.id))
    assert helpers == sorted([*(f"ask~{key}" for key in STEP_SETTING_KEYS), "per~each", "per~gather"]), helpers
    assert [i.path for i in _unknown_step_key_issues(expanded)] == []


def test_an_empty_width_and_height_beside_data_is_not_a_warning():
    """Live 2026-11-18: every workflow.graph.create answered eight "'height' is written on the step itself" warnings —
    the shared graph wire always carries width/height, null when unset. A null key writes nothing."""
    from matrx_graph.types.definition import Definition
    from matrx_graph.validation import validate_definition

    empty = Definition.model_validate({"nodes": [{"id": "a", "type": "io.user_input", "position": {"x": 0, "y": 0},
                                                  "width": None, "height": None, "data": {"label": "A"}}], "edges": []})
    said = [i.message for i in validate_definition(empty).issues if "written on the step itself" in i.message]
    assert said == []
    real = Definition.model_validate({"nodes": [{"id": "a", "type": "io.user_input", "position": {"x": 0, "y": 0},
                                                 "width": 240, "data": {"label": "A"}}], "edges": []})
    assert any("'width' is written on the step itself" in i.message for i in validate_definition(real).issues)
