"""Tests for the dataflow analysis module."""

import json
from pathlib import Path

from mistralai.workflows.core._dataflow import CONTROL_FLOW_VIEW, build_dataflow_views, expand_views
from mistralai.workflows.core._graph import build_graph_statically

_CF_PAYLOAD = {
    "version": 3,
    "workflow_name": "TestWorkflow",
    "view": "Control flow",
    "nodes": [{"id": "n1", "type": "activity", "name": "step"}],
    "edges": [],
    "files": {"test.py": {"begin": 0, "end": 100}},
    "incomplete": False,
}


# -- Error-path tests ---------------------------------------------------------


def test_produces_one_df_view():
    views = build_dataflow_views(_CF_PAYLOAD)
    assert len(views) == 1
    assert views[0]["view"] == "Data flow"


def test_error_view_has_required_fields():
    """Without sources, analysis fails gracefully -> empty nodes/edges."""
    views = build_dataflow_views(_CF_PAYLOAD)
    v = views[0]
    assert v["version"] == 3
    assert v["workflow_name"] == "TestWorkflow"
    assert v["nodes"] == []
    assert v["edges"] == []


def test_expand_views_stamps_control_flow():
    payload = {"version": 3, "workflow_name": "W"}
    all_views = expand_views(payload)
    assert len(all_views) == 2
    assert all_views[0]["view"] == CONTROL_FLOW_VIEW
    assert all_views[1]["view"] == "Data flow"
    assert "view" not in payload


# -- Integration tests on workflow_two_paths.py --------------------------------


def _get_views() -> list[dict]:
    """Build workflow_two_paths.py with the SDK static emitter."""
    workflow = Path(__file__).with_name("workflow_two_paths.py")
    graph = build_graph_statically(workflow.read_text(), str(workflow), lambda _path: None)[0]
    return expand_views(graph.to_dict(include_sources=True))


def _get_view(name: str) -> dict:
    views = _get_views()
    return next(v for v in views if v["view"] == name)


def test_two_paths_produces_two_views():
    views = _get_views()
    labels = [v["view"] for v in views]
    assert labels == ["Control flow", "Data flow"]


def test_two_paths_transform_nodes():
    df = _get_view("Data flow")
    transforms = [n for n in df["nodes"] if n["type"] == "transform"]
    names = {t["name"] for t in transforms}
    assert len(transforms) >= 1
    assert any("pypi_missing" in n for n in names)


def test_two_paths_data_dep_edges():
    df = _get_view("Data flow")
    data_edges = [e for e in df["edges"] if e["kind"] == "data_dep"]
    labels = {e.get("label") for e in data_edges}
    assert "all_pkgs" in labels
    assert "is_ok" in labels
    assert len(data_edges) >= 3


def test_two_paths_fan_out_group():
    df = _get_view("Data flow")
    parallels = [n for n in df["nodes"] if n["type"] == "parallel"]
    assert len(parallels) >= 1
    group = parallels[0]
    assert len(group.get("branches", [])) >= 2


# -- Source-redaction tests ----------------------------------------------------

_SECRET = "sk-live-DO-NOT-UPLOAD-abc123"  # noqa: S105

_LEAKY_WORKFLOW = f"""
from mistralai import workflows

@workflows.activity()
async def fetch() -> dict:
    return {{}}

@workflows.workflow.define(name="leaky")
class Leaky:
    @workflows.workflow.entrypoint
    async def run(self) -> dict:
        data = await fetch()
        api_key = "{_SECRET}"
        note = f"token={_SECRET}"
        result = {{**data, "k": api_key, "n": note}}
        return result
"""


def _leaky_views() -> list[dict]:
    graph = build_graph_statically(_LEAKY_WORKFLOW, "/tmp/leaky.py", lambda _path: None)[0]
    views = expand_views(graph.to_dict(include_sources=True))
    for view in views:
        view.pop("sources", None)
    return views


def test_string_literals_never_reach_the_payload():
    """Transform labels are rendered from source, so literals must be redacted.

    The analyser needs `include_sources=True`, and it re-emits assignment text as
    node names. Stripping the `sources` key alone left secrets in those names.
    """
    views = _leaky_views()
    body = json.dumps({**views[0], "views": views})

    assert _SECRET not in body


def test_transform_labels_stay_readable_after_redaction():
    """Redaction must blank literals without destroying the label's usefulness."""
    dataflow = next(v for v in _leaky_views() if v["view"] == "Data flow")
    names = {n["name"] for n in dataflow["nodes"] if n["type"] == "transform"}

    assert 'api_key = "…"' in names
    assert any(name.startswith("result = {**data,") for name in names), names


def test_transform_labels_are_length_capped():
    """A pathological one-liner must not blow up the payload through its label."""
    source = f"""
from mistralai import workflows

@workflows.activity()
async def fetch() -> int:
    return 1

@workflows.workflow.define(name="longline")
class LongLine:
    @workflows.workflow.entrypoint
    async def run(self) -> int:
        base = await fetch()
        {"total = base" + " + base" * 200}
        return total
"""
    graph = build_graph_statically(source, "/tmp/longline.py", lambda _path: None)[0]
    dataflow = next(v for v in expand_views(graph.to_dict(include_sources=True)) if v["view"] == "Data flow")
    names = [n["name"] for n in dataflow["nodes"] if n["type"] == "transform"]

    assert names, "expected at least one transform"
    assert all(len(name) <= 120 for name in names), max(names, key=len)
