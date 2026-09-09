from mistralai.workflows.core._graph import build_graph_statically
from mistralai.workflows.core.wire_format import AtlasWireFormat, FlatNode

_PRELUDE = """
from mistralai.workflows import workflow, activity


@activity()
async def do_it() -> str:
    return "ok"
"""


_HEADER = """

@workflow.define
class W:
    @workflow.entrypoint
    async def run(self, x: int) -> str:
"""


def _source(body: str) -> str:
    return _PRELUDE + _HEADER + body


def _analyze(body: str) -> AtlasWireFormat:
    graphs = build_graph_statically(_source(body), "/tmp/workflow.py", lambda path: None)
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
    # A normal early return terminates the arm on a non-error exit node.
    early = next(n for n in _outputs(graph) if n.id == "W::cond_0::exit_true")
    assert any(e.to == early.id for e in graph.edges)


def test_early_return_gets_its_own_terminal() -> None:
    # WFL-2751: a guard that returns while the main flow continues must terminate on
    # its own "returns" node beside the diamond, not on the shared workflow output.
    graph = _analyze(
        """
        if x < 0:
            return "skipped"
        await do_it()
        return "done"
"""
    )

    assert graph.incomplete is False
    assert _error_outputs(graph) == []

    outputs = {n.id: n for n in _outputs(graph)}
    assert set(outputs) == {"W::cond_0::exit_true", "W::output"}

    early = outputs["W::cond_0::exit_true"]
    assert early.name == "returns"
    assert early.is_error is False
    assert early.is_early_exit is True
    # The workflow output stays the fall-through terminal, not an early exit.
    assert outputs["W::output"].is_early_exit is None

    # Wired as branch content (like a `raise` in the arm), so renderers that walk the
    # branch chain lay it out. `branch_exit_*` targets are outside that chain.
    assert any(e.from_ == "W::cond_0" and e.to == early.id and e.kind == "branch_true" for e in graph.edges)
    assert not any(e.kind.startswith("branch_exit_") for e in graph.edges)

    # The main flow is untouched: it still runs the activity and falls through to the
    # workflow output rather than being short-circuited by the guard.
    assert any(e.to == "W::output" and e.kind == "sequential" for e in graph.edges)


def test_early_return_terminal_points_at_the_return_statement() -> None:
    body = """
        if x < 0:
            return "skipped"
        return await do_it()
"""
    graph = _analyze(body)

    early = next(n for n in _outputs(graph) if n.id == "W::cond_0::exit_true")
    source = _source(body).encode()
    assert source[early.source_range.begin : early.source_range.end] == b'return "skipped"'
    assert early.source_range.line == source[: early.source_range.begin].count(b"\n") + 1


def test_early_return_in_else_arm_gets_a_false_side_terminal() -> None:
    graph = _analyze(
        """
        if x > 0:
            await do_it()
        else:
            return "negative"
        return "positive"
"""
    )

    assert graph.incomplete is False
    early = next(n for n in _outputs(graph) if n.id == "W::cond_0::exit_false")
    assert early.name == "returns"
    assert any(e.to == early.id and e.kind == "branch_false" for e in graph.edges)


def test_early_return_inside_a_loop_gets_its_own_terminal() -> None:
    graph = _analyze(
        """
        for i in range(3):
            if i == x:
                return "found"
            await do_it()
        return "none"
"""
    )

    assert graph.incomplete is False
    early = next(n for n in _outputs(graph) if n.id == "W::cond_0::exit_true")
    assert early.name == "returns"
    assert early.is_error is False

    # A contained conditional carries its own branch lists, so the renderer never
    # falls back to walking the edges: the terminal has to be on them to be drawn.
    cond = next(n for n in graph.nodes if n.id == "W::cond_0")
    assert cond.branchTrue == [early.id]
    assert early.id in (cond.branchDescendants or [])

    # It stays out of the loop's own children -- the conditional frame places it.
    loop = next(n for n in graph.nodes if n.type == "loop")
    assert early.id not in (loop.children or [])


def test_mixed_raise_and_return_arms_keep_distinct_terminals() -> None:
    graph = _analyze(
        """
        if x < 0:
            raise ValueError("bad")
        else:
            return "ok"
        """
    )

    assert graph.incomplete is False
    names = {n.id: (n.name, n.is_error) for n in _outputs(graph)}
    assert names["W::raise_0"][1] is True
    # Nothing follows the conditional, so the returning arm is the workflow output.
    assert "W::output" in names
    assert "W::cond_0::exit_false" not in names


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
    assert any(
        e.from_ == "W::cond_0" and e.to == "W::cond_0::exit_true" and e.kind == "branch_true" for e in graph.edges
    )


def test_both_branches_return_converge_to_single_output() -> None:
    # WFL-1853: a trivial conditional where both arms `return await <activity>()`
    # must converge on a single workflow output node — no spurious extra output
    # ("int") node and no duplicate per-branch "exit" nodes.
    graph = _analyze(
        """
        if x == 0:
            return await do_it()
        else:
            return await do_it()
"""
    )

    assert graph.incomplete is False

    outputs = _outputs(graph)
    assert len(outputs) == 1
    assert not outputs[0].is_error
    out_id = outputs[0].id

    # Both arms reach the single output through branch-exit edges.
    exit_kinds = {e.kind for e in graph.edges if e.to == out_id}
    assert exit_kinds == {"branch_exit_true", "branch_exit_false"}

    # No spurious sequential fall-through straight from the conditional to the output.
    cond_id = next(n.id for n in graph.nodes if n.type == "conditional")
    assert not any(e.from_ == cond_id and e.to == out_id and e.kind == "sequential" for e in graph.edges)


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


def test_nested_both_return_arms_do_not_converge_when_work_follows() -> None:
    # Both arms of the *inner* conditional return, but the workflow continues after
    # the outer one. They exit early -- converging them on the shared output would
    # draw the returns as flowing into work they actually skip.
    graph = _analyze(
        """
        if x > 0:
            if x == 1:
                return await do_it()
            else:
                return "two"
        await do_it()
        return "done"
"""
    )

    assert graph.incomplete is False
    assert {n.id for n in _outputs(graph)} >= {"W::cond_1::exit_true", "W::cond_1::exit_false"}
    assert not [e for e in graph.edges if e.kind.startswith("branch_exit_")]
