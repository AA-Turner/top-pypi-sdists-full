from mistralai.workflows.core._graph import build_graph_statically
from mistralai.workflows.core.wire_format import AtlasWireFormat, FlatNode

_PRELUDE = """
from mistralai.workflows import workflow, activity


@activity()
async def do_it() -> str:
    return "ok"
"""


def _analyze(body: str) -> AtlasWireFormat:
    source = (
        _PRELUDE
        + """

@workflow.define
class W:
    @workflow.entrypoint
    async def run(self, x: int) -> str:
"""
        + body
    )
    graphs = build_graph_statically(source, "/tmp/workflow.py", lambda path: None)
    return graphs[0]


def _outputs(graph: AtlasWireFormat) -> list[FlatNode]:
    return [n for n in graph.nodes if n.type == "output"]


def _error_outputs(graph: AtlasWireFormat) -> list[FlatNode]:
    return [n for n in _outputs(graph) if n.is_error]


def test_standalone_raise_is_an_error_exit() -> None:
    graph = _analyze(
        """
        await do_it()
        raise RuntimeError("boom")
"""
    )

    assert graph.incomplete is False
    errors = _error_outputs(graph)
    assert len(errors) == 1
    assert "RuntimeError" in errors[0].name

    # The activity must not connect to a normal exit node; the only terminal is the raise.
    error_id = errors[0].id
    assert any(e.to == error_id for e in graph.edges)
    assert not any(n.id == "W::output" for n in graph.nodes)


def test_raise_in_branch_is_error_and_validates() -> None:
    graph = _analyze(
        """
        if x < 0:
            raise ValueError("bad")
        return await do_it()
"""
    )

    # incomplete stays False => the conditional still has exactly one true/one false output.
    assert graph.incomplete is False
    errors = _error_outputs(graph)
    assert len(errors) == 1
    assert "ValueError" in errors[0].name


def test_deep_raise_under_with_is_detected() -> None:
    graph = _analyze(
        """
        with open("f"):
            raise RuntimeError("deep")
"""
    )

    assert graph.incomplete is False
    assert len(_error_outputs(graph)) == 1


def test_reraise_in_except_handler_is_error_exit() -> None:
    graph = _analyze(
        """
        try:
            await do_it()
        except ValueError:
            raise RuntimeError("reraise")
        return "done"
"""
    )

    assert graph.incomplete is False
    errors = _error_outputs(graph)
    assert len(errors) == 1

    # The error terminal lives inside the try/except container.
    try_nodes = [n for n in graph.nodes if n.type == "try_except"]
    assert try_nodes
    assert errors[0].id in try_nodes[0].children


def test_raise_at_end_of_try_body_does_not_link_to_except_container() -> None:
    graph = _analyze(
        """
        try:
            await do_it()
            raise RuntimeError("boom")
        except RuntimeError:
            await do_it()
        return "done"
"""
    )

    assert graph.incomplete is False
    error_id = _error_outputs(graph)[0].id
    assert not any(e.from_ == error_id for e in graph.edges)


def test_early_return_remains_a_normal_exit() -> None:
    graph = _analyze(
        """
        if x == 0:
            return await do_it()
        return "other"
"""
    )

    assert graph.incomplete is False
    assert _error_outputs(graph) == []
    # A normal early return still produces a non-error branch exit edge.
    assert any(e.kind == "branch_exit_true" for e in graph.edges)


def test_literal_early_return_in_branch_validates() -> None:
    graph = _analyze(
        """
        if x == 0:
            return "done"
        return await do_it()
"""
    )

    assert graph.incomplete is False
    assert _error_outputs(graph) == []
    assert any(e.from_ == "W::cond_0" and e.kind == "branch_exit_true" for e in graph.edges)


def test_nested_if_with_exiting_arms_validates() -> None:
    graph = _analyze(
        """
        if x > 0:
            if x == 1:
                return await do_it()
            else:
                raise RuntimeError("boom")
        return "done"
"""
    )

    assert graph.incomplete is False
    inner_edges = [e for e in graph.edges if e.from_ == "W::cond_1"]
    true_edges = [e for e in inner_edges if e.kind in ("branch_true", "branch_exit_true", "branch_true_skip")]
    false_edges = [e for e in inner_edges if e.kind in ("branch_false", "branch_exit_false", "branch_false_skip")]
    assert len(true_edges) == 1
    assert len(false_edges) == 1
