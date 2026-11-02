"""Accessor paths — the half that makes a picker selection resolve to values.

Without this, `AvailableKind.reference()` is a catalog that selects nothing
and every selection still needs an extraction node — the exact thing §7.7a
retires. These pin the semantics of `[]` (the only multiplicity operator),
holes (absence, never a None in a typed list), wrapper unwrapping, and the
loud-but-non-fatal failure posture.
"""

from __future__ import annotations

from matrx_graph.content_ir.accessor import (
    parse_reference,
    resolve_path,
    resolve_reference,
    unwrap_runtime_wrapper,
)
from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.wrappers import AgentResultWrapper, NodeOutcomeWrapper


class Rating(KindModel, kind="rating"):
    value: float


class WebResult(KindModel, kind="web_result"):
    url: str
    rating: Rating | None = None


class SearchResults(KindModel, kind="search_results"):
    query: str
    web: list[WebResult] = []


def _payload() -> dict:
    return SearchResults(
        query="pizza",
        web=[
            WebResult(url="a", rating=Rating(value=4.5)),
            WebResult(url="b"),
            WebResult(url="c", rating=Rating(value=3.0)),
        ],
    ).model_dump()


def test_whole_output_is_one_value() -> None:
    resolution = resolve_path(_payload(), "")
    assert len(resolution.values) == 1
    assert resolution.values[0]["query"] == "pizza"


def test_scalar_path() -> None:
    assert resolve_path(_payload(), "query").values == ["pizza"]


def test_collection_segment_yields_every_item() -> None:
    resolution = resolve_path(_payload(), "web[]")
    assert [v["url"] for v in resolution.values] == ["a", "b", "c"]


def test_a_hole_is_an_absence_not_a_none() -> None:
    # 'b' has no rating. A None in the middle of a typed list would make every
    # consumer defensive; the value simply is not there, and the reason is
    # RECORDED so an author can see 1 of 3 was missing.
    resolution = resolve_path(_payload(), "web[].rating")
    assert [v["value"] for v in resolution.values] == [4.5, 3.0]
    assert any("absent on 1" in note for note in resolution.notes)


def test_missing_key_is_a_note_never_an_exception() -> None:
    resolution = resolve_path(_payload(), "nope.deeper")
    assert resolution.values == []
    assert resolution.notes


def test_collection_operator_on_a_scalar_is_loud_and_still_usable() -> None:
    # The producing kind and the reference disagree — a real contract defect.
    # Silently returning nothing would send an author hunting the wrong node.
    resolution = resolve_path({"query": "pizza"}, "query[]")
    assert resolution.values == ["pizza"]
    assert any("declared as a collection" in note for note in resolution.notes)


def test_models_resolve_by_wire_name() -> None:
    # A path authored against serialized data must resolve against the model:
    # the two halves of the boundary spell fields differently.
    resolution = resolve_path(SearchResults(query="x", web=[WebResult(url="a")]), "web[].url")
    assert resolution.values == ["a"]


def test_node_outcome_wrapper_is_unwrapped_at_the_root() -> None:
    # Persisted run data carries the wrapper; edges carry the data kind. A
    # path must mean ONE thing against both, so unwrapping happens once, here.
    outcome = NodeOutcomeWrapper(run_id="r", node_id="search", output=_payload()).model_dump()
    assert resolve_path(outcome, "query").values == ["pizza"]
    assert unwrap_runtime_wrapper(outcome)["query"] == "pizza"


def test_agent_result_unwraps_to_its_content_list() -> None:
    wrapper = AgentResultWrapper(content=[_payload()]).model_dump()
    # content IS the payload, in document order — so `[]`-less addressing of
    # the list works, and each element addresses normally.
    assert resolve_path(wrapper, "").values == [[_payload()]]
    assert resolve_path(wrapper, "[]") is not None


def test_empty_wrapper_says_the_step_produced_nothing() -> None:
    outcome = NodeOutcomeWrapper(run_id="r", node_id="n", output=None).model_dump()
    resolution = resolve_path(outcome, "query")
    assert resolution.values == []
    assert any("produced nothing" in note for note in resolution.notes)


def test_reference_resolution_against_a_runs_node_outputs() -> None:
    outputs = {"search": _payload()}
    resolution = resolve_reference("search.web[].rating", outputs)
    assert [v["value"] for v in resolution.values] == [4.5, 3.0]
    assert resolution.reference == "search.web[].rating"


def test_unknown_node_is_distinguished_from_a_missing_key() -> None:
    resolution = resolve_reference("ghost.query", {"search": _payload()})
    assert resolution.root_missing is True
    assert resolution.values == []


def test_node_ids_containing_dots_parse_when_the_graph_is_known() -> None:
    parsed = parse_reference("my.node.id.web[]", known_node_ids=["my.node.id"])
    assert parsed.node_id == "my.node.id"
    assert parsed.segments == ("web[]",)
