"""THE deliverable rule + the publish gate (SPEC-workflow-ui-contract §2.2/§2.3).

These pin the behavior that ``GET /workflows/{id}/result-schema`` serves and
that ``DefinitionStore.publish`` refuses on — the SAME function, which is the
whole point: a second copy of this rule would let the endpoint advertise a
contract the validator does not enforce.
"""

from __future__ import annotations

from pydantic import BaseModel

from matrx_graph.types.compiled import CompiledGraph, CompiledNode
from matrx_graph.types.definition import Definition
from matrx_graph.types.deliverables import compute_deliverables, resolve_io_declaration


class _Cfg(BaseModel):
    pass


def _node(
    node_id: str,
    spec_type: str,
    *,
    output_kind: str | None = None,
    input_kind: str | None = None,
    outgoing: tuple[str, ...] = (),
) -> CompiledNode:
    return CompiledNode(
        node_id=node_id,
        spec_type=spec_type,
        config=_Cfg(),
        incoming_edge_ids=(),
        outgoing_edge_ids=outgoing,
        reads_channels=(),
        writes_channels=(),
        input_kind=input_kind,
        output_kind=output_kind,
    )


def _graph(*nodes: CompiledNode, entry: tuple[str, ...] = ()) -> CompiledGraph:
    return CompiledGraph(
        definition_hash="test",
        nodes={n.node_id: n for n in nodes},
        edges={},
        channels={},
        entry_node_ids=entry or tuple(n.node_id for n in nodes[:1]),
        topological_layers=(),
    )


def _definition(*specs: tuple[str, str, dict]) -> Definition:
    return Definition.model_validate(
        {
            "version": "1",
            "nodes": [
                {
                    "id": node_id,
                    "type": spec_type,
                    "position": {"x": 0, "y": 0},
                    "data": data,
                }
                for node_id, spec_type, data in specs
            ],
            "edges": [],
        }
    )


def test_output_nodes_are_the_declaration_even_when_not_terminal() -> None:
    """Rule 1: ≥1 output.* node → that set IS the deliverable set. Terminality
    is irrelevant — a mid-run showcase is still a deliverable."""
    graph = _graph(
        _node("show", "output.to_frontend", output_kind="recipe", outgoing=("e1",)),
        _node("tail", "data.transform", output_kind="text"),
    )
    definition = _definition(
        ("show", "output.to_frontend", {}), ("tail", "data.transform", {})
    )
    assert [d.node_id for d in compute_deliverables(graph, definition)] == ["show"]


def test_terminal_kind_declaring_nodes_are_the_fallback_set() -> None:
    """Rule 2: no output.* node → every terminal node with a non-null kind.
    A terminal node declaring NO kind is not a deliverable."""
    graph = _graph(
        _node("mid", "data.transform", output_kind="text", outgoing=("e1",)),
        _node("end", "data.transform", output_kind="recipe"),
        _node("kindless", "data.transform"),
    )
    definition = _definition(
        ("mid", "data.transform", {}),
        ("end", "data.transform", {}),
        ("kindless", "data.transform", {}),
    )
    assert [d.node_id for d in compute_deliverables(graph, definition)] == ["end"]


def test_node_data_deliverable_flag_overrides_membership_both_ways() -> None:
    """Rule 3: ``node.data.deliverable`` adds a node the rule excluded and
    removes one it included."""
    graph = _graph(
        _node("show", "output.to_frontend", output_kind="recipe"),
        _node("extra", "data.transform", output_kind="text", outgoing=("e1",)),
    )
    definition = _definition(
        ("show", "output.to_frontend", {"deliverable": False}),
        ("extra", "data.transform", {"deliverable": True}),
    )
    assert [d.node_id for d in compute_deliverables(graph, definition)] == ["extra"]


def test_single_deliverable_backfills_the_declaration() -> None:
    """§2.3: no declaration + exactly one deliverable → the server BACKFILLS."""
    graph = _graph(_node("show", "output.to_frontend", output_kind="recipe"))
    definition = _definition(("show", "output.to_frontend", {}))

    verdict = resolve_io_declaration(graph, definition)
    assert verdict.error is None
    assert verdict.output_kind == "recipe"
    assert verdict.output_kind_backfilled is True
    assert verdict.deliverables[0].is_primary is True


def test_multiple_deliverables_with_no_declaration_stay_null() -> None:
    """§2.3: NULL is THE answer — "the run's shape IS the collection". We
    never mint a wrapper kind to fill the hole."""
    graph = _graph(
        _node("a", "output.to_frontend", output_kind="recipe"),
        _node("b", "output.to_frontend", output_kind="text"),
    )
    definition = _definition(("a", "output.to_frontend", {}), ("b", "output.to_frontend", {}))

    verdict = resolve_io_declaration(graph, definition)
    assert verdict.error is None
    assert verdict.output_kind is None
    assert verdict.output_kind_backfilled is False
    assert not any(d.is_primary for d in verdict.deliverables)


def test_a_declaration_no_deliverable_produces_is_refused() -> None:
    """§2.3: the publish gate. The refusal NAMES the mismatch."""
    graph = _graph(
        _node("a", "output.to_frontend", output_kind="recipe"),
        _node("b", "output.to_frontend", output_kind="text"),
    )
    definition = _definition(("a", "output.to_frontend", {}), ("b", "output.to_frontend", {}))

    verdict = resolve_io_declaration(graph, definition, declared_output_kind="scraped_page")
    assert verdict.error is not None
    assert "scraped_page" in verdict.error
    assert "recipe" in verdict.error and "text" in verdict.error


def test_a_declaration_among_several_deliverables_picks_the_primary() -> None:
    """§2.3: a declaration + multiple deliverables → the matching one is THE
    primary, which is how a multi-deliverable workflow becomes eligible to
    hold a kind-contract Mandate."""
    graph = _graph(
        _node("a", "output.to_frontend", output_kind="recipe"),
        _node("b", "output.to_frontend", output_kind="text"),
    )
    definition = _definition(("a", "output.to_frontend", {}), ("b", "output.to_frontend", {}))

    verdict = resolve_io_declaration(graph, definition, declared_output_kind="text")
    assert verdict.error is None
    assert verdict.output_kind == "text"
    assert verdict.output_kind_backfilled is False
    assert [d.node_id for d in verdict.deliverables if d.is_primary] == ["b"]


def test_multiple_dynamic_deliverables_require_explicit_primary() -> None:
    graph = _graph(
        _node("a", "output.to_frontend"),
        _node("b", "output.to_frontend"),
    )
    definition = _definition(
        ("a", "output.to_frontend", {}),
        ("b", "output.to_frontend", {}),
    )

    ambiguous = resolve_io_declaration(
        graph, definition, declared_output_kind="quiz_set"
    )
    assert ambiguous.error is not None
    # FIX-Q5 — the sentence is for the workflow's AUTHOR: the editor's name for
    # the step and the titles they typed, never a JSON field with no control.
    assert "Show on Screen" in ambiguous.error
    assert "is_primary" not in ambiguous.error

    definition.nodes[1].data["is_primary"] = True
    selected = resolve_io_declaration(
        graph, definition, declared_output_kind="quiz_set"
    )
    assert selected.error is None
    assert [d.node_id for d in selected.deliverables if d.is_primary] == ["b"]


def test_input_kind_is_validated_against_entry_nodes_but_never_backfilled() -> None:
    """§2.3: NULL input_kind carries its own meaning — "collected via the run
    form" — so derivation serves it without ever writing the column back."""
    graph = _graph(
        _node("entry", "io.user_input", input_kind="recipe", outgoing=("e1",)),
        _node("end", "data.transform", output_kind="text"),
        entry=("entry",),
    )
    definition = _definition(("entry", "io.user_input", {}), ("end", "data.transform", {}))

    derived = resolve_io_declaration(graph, definition)
    assert derived.input_kind == "recipe"
    assert derived.input_kind_derived is True

    lying = resolve_io_declaration(graph, definition, declared_input_kind="scraped_page")
    assert lying.error is not None
    assert "scraped_page" in lying.error
