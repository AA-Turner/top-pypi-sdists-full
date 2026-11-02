"""The runtime wrapper kinds on the wire — the packet, and the elision rule.

Plan of record: ``common-docs/systems/architecture/content-ir/FEATURE.md``
§10b item 8. These pin the two properties a consumer depends on: the packet is
self-describing all the way down, and a payload is never serialized twice.
"""

from __future__ import annotations

import json

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.runtime_view import (
    OUTPUT_REF_OUTPUT,
    node_outcome_view,
    output_ref_for_key,
    run_result_view,
)
from matrx_graph.content_ir.wrappers import NodeOutcomeWrapper, RunResultWrapper


class _WebResult(KindModel, kind="web_result"):
    url: str
    title: str = ""


class _SearchResults(KindModel, kind="search_results"):
    query: str
    web: list[_WebResult] = []


def test_the_packet_is_self_describing_all_the_way_down() -> None:
    """Which workflow, which node, and inside it — what the data IS."""
    view = node_outcome_view(
        run_id="run-1",
        node_id="search",
        workflow_id="wf-9",
        step=2,
        duration_ms=140,
        output_kind="search_results",
        output_kind_ok=True,
        output=_SearchResults(query="q", web=[_WebResult(url="https://a", title="A")]).model_dump(),
    )
    assert view["__kind"] == "node_outcome"
    assert (view["run_id"], view["node_id"], view["workflow_id"]) == (
        "run-1",
        "search",
        "wf-9",
    )
    assert view["output"]["__kind"] == "search_results"
    assert view["output"]["web"][0]["__kind"] == "web_result"
    # Round-trips through the model: a view IS a kind instance, not a lookalike.
    assert NodeOutcomeWrapper(**view).model_dump() == view


def test_elision_never_serializes_the_payload_twice() -> None:
    payload = {"__kind": "search_results", "query": "q", "web": []}
    view = node_outcome_view(
        run_id="r",
        node_id="n",
        output=payload,
        output_kind="search_results",
        output_ref=OUTPUT_REF_OUTPUT,
    )
    assert view["output"] is None
    assert view["output_ref"] == "output"
    assert "query" not in json.dumps(view)


def test_output_ref_for_key_refuses_an_unaddressable_key() -> None:
    assert output_ref_for_key("output", "search") == "output.search"
    # A dot in the key would make the path ambiguous — inline instead of guess.
    assert output_ref_for_key("output", "a.b") is None
    assert output_ref_for_key("output", "") is None


def test_run_result_nests_one_node_outcome_per_terminal() -> None:
    terminal = node_outcome_view(
        run_id="run-1",
        node_id="report",
        workflow_id="wf-9",
        output_kind="markdown",
        output_kind_ok=True,
        output={"__kind": "markdown", "text": "# Done"},
        output_ref=output_ref_for_key(OUTPUT_REF_OUTPUT, "report"),
    )
    view = run_result_view(
        run_id="run-1",
        workflow_id="wf-9",
        status="completed",
        output_kind="markdown",
        outputs=[terminal],
        output_ref=OUTPUT_REF_OUTPUT,
    )
    assert view["__kind"] == "run_result"
    assert view["output"] is None and view["output_ref"] == "output"
    nested = view["outputs"][0]
    assert nested["__kind"] == "node_outcome"
    assert nested["node_id"] == "report"
    assert nested["output_ref"] == "output.report"
    assert RunResultWrapper(**view).model_dump() == view
    # Nothing about the run's payloads is repeated on the wire.
    assert "# Done" not in json.dumps(view)
