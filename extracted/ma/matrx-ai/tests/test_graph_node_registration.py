"""Registration hygiene for matrx-ai graph_nodes registered nodes."""


def test_no_action_prefix_in_registered_node_types() -> None:
    """The ``action.*`` spec_type namespace is ERADICATED (2026-08-08).

    Canonical spec_types are bare dotted names; the legacy ``action.<name>``
    spelling exists only as a read-side alias in the node registry for stored
    definitions. A registered node type carrying the prefix means someone
    reintroduced the namespace — see docs/workflow/NOMENCLATURE.md.
    """
    from matrx_graph.executor.registry import default_registry

    from matrx_ai.graph_nodes import register_with_graph

    register_with_graph()

    offenders = sorted(
        node_type
        for node_type in default_registry().all_types()
        if node_type.startswith("action.")
    )
    assert not offenders, (
        "These node types carry the eradicated 'action.' prefix — canonical "
        "spec_types are bare dotted names (docs/workflow/NOMENCLATURE.md):\n  "
        + "\n  ".join(offenders)
    )
