"""Review fixes for ``{"$run": …}`` in templates (e0aa927dad34 review).

Each test failed on e0aa927dad34 and passes after: a ``$format`` ``{run.…}`` refusal that
``$optional`` swallowed, a multi-key ``$run`` dict taken as a literal, a run-once step that
reads the run with no warning, three call sites reading the run three ways, and a no-run
refusal that never named the form that works.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from matrx_graph import NodeRegistry, register_builtin_nodes
from matrx_graph.errors import ExecutionError, UnresolvedInputError
from matrx_graph.nodes._template import TemplatePathMissing, substitute_template
from matrx_graph.types.variables import resolve_var_refs
from matrx_graph.validation import validate_definition

RUN = {"id": "run-42", "workflow_id": "wf-1", "step_id": "s"}


def _refused(template: object, run: dict | None) -> ExecutionError:
    with pytest.raises(ExecutionError) as caught:
        substitute_template(template, {}, index=0, run=run)
    assert not isinstance(caught.value, TemplatePathMissing), "a refusal $optional would absorb"
    return caught.value


def test_optional_does_not_swallow_a_format_run_refusal() -> None:
    _refused({"$optional": {"$format": "/runs/{run.id}"}, "default": None}, None)
    _refused({"$optional": {"$format": "/runs/{run.user}"}, "default": None}, RUN)


def test_format_optional_blanks_only_a_known_name_whose_value_is_null() -> None:
    _refused({"$format": "/runs/{run.user}", "optional": True}, RUN)
    _refused({"$format": "/runs/{run.id}", "optional": True}, None)
    unsaved = {**RUN, "workflow_id": None}
    assert substitute_template({"$format": "wf={run.workflow_id}", "optional": True}, {}, run=unsaved) == "wf="


def test_a_run_ref_with_a_key_beside_it_is_refused() -> None:
    _refused({"$run": "id", "default": "run-0"}, RUN)
    with pytest.raises(UnresolvedInputError, match="name"):
        resolve_var_refs(
            {"meta": {"$run": "id", "default": "run-0"}}, run_variables={}, declared={}, node_id="n",
            run_facts=RUN,
        )


def _definition(data: dict) -> dict:
    return {
        "version": "1",
        "nodes": [{"id": "shape", "type": "data.map_template", "position": {"x": 0, "y": 0},
                   "data": {"spec_type": "data.map_template", **data}}],
        "edges": [],
    }


def _once_warnings(data: dict) -> list[str]:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    result = validate_definition(_definition(data), reg)
    return [i.path for i in result.issues if i.severity == "warning" and "runs once per key" in i.message]


def test_a_run_once_step_that_reads_the_run_is_warned_at_save() -> None:
    once = {"once": {"key": ["items"], "scope": "workflow"}}
    reads_in_inputs = {"input": {"items": [], "run_id": {"$run": "id"}}, "config": {"template": "$item"}}
    reads_in_settings = {"input": {"items": []}, "config": {"template": {"r": {"$format": "{run.id}"}}}}
    assert _once_warnings({**once, **reads_in_inputs}) == ["nodes[shape].data.input"]
    assert _once_warnings({**once, **reads_in_settings}) == ["nodes[shape].data.config"]
    assert _once_warnings(reads_in_inputs) == []  # not run-once: nothing to warn


def test_every_template_step_reads_the_run_the_same_way() -> None:
    nodes = Path(__file__).resolve().parents[1] / "matrx_graph" / "nodes"
    for rel in ("data/map_template.py", "control/map.py", "control/work_queue.py"):
        text = (nodes / rel).read_text()
        assert "run=run_facts_of(ctx)" in text, rel
        assert "ctx.run_facts" not in text and 'getattr(ctx, "run_facts"' not in text, rel


def test_no_run_refusal_names_the_step_input_form() -> None:
    error = _refused({"key": {"$run": "id"}}, None)
    assert "step input" in str(error) and '{"$run": "id"}' in str(error)
