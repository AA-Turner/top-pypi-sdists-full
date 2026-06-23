from mistralai.workflows.core._graph import build_graph_statically
from mistralai.workflows.core.wire_format import AtlasWireFormat, FlatEdge, FlatNode


def test_static_analysis_reads_keyword_only_handler_param_type() -> None:
    source = """
from mistralai.workflows import workflow


@workflow.define
class StaticWorkflow:
    @workflow.entrypoint
    async def run(self) -> None:
        pass

    @workflow.signal(name="kw_signal")
    async def handle_signal(self, *, payload: str) -> None:
        pass
"""

    graphs = build_graph_statically(source, "/tmp/workflow.py", lambda path: None)

    assert graphs[0].signals[0].param_type == "str"


# ---------------------------------------------------------------------------
# asyncio.gather / nested local function inlining (parallel fan-out)
# ---------------------------------------------------------------------------


def _parallel_lane_labels(graph: AtlasWireFormat) -> list[list[str]]:
    """Return, for each parallel node, the activity labels reachable in its lanes."""
    by_id = {n.id: n for n in graph.nodes}
    lanes: list[list[str]] = []
    for node in graph.nodes:
        if node.type != "parallel":
            continue
        for branch in node.branches or []:
            lanes.append([by_id[cid].name for cid in branch if cid in by_id])
    return lanes


def test_gather_over_comprehension_of_nested_fn_emits_parallel() -> None:
    """gather(*[_fetch(x) for x in xs]) where _fetch wraps an activity behind a semaphore."""
    source = """
import asyncio
from mistralai.workflows import workflow, activity


@activity
async def fetch_one(n: int) -> int:
    return n


@workflow.define
class FanoutWorkflow:
    @workflow.entrypoint
    async def run(self, items: list[int]) -> None:
        sem = asyncio.Semaphore(4)

        async def _fetch(n: int) -> int:
            async with sem:
                return await fetch_one(n)

        results = await asyncio.gather(*[_fetch(n) for n in items])
"""

    graphs = build_graph_statically(source, "/tmp/workflow.py", lambda path: None)

    assert _parallel_lane_labels(graphs[0]) == [["fetch_one"]]


def test_gather_over_tasks_variable_emits_parallel() -> None:
    """gather(*tasks) where tasks is a comprehension of direct activity calls."""
    source = """
import asyncio
from mistralai.workflows import workflow, activity


@activity
async def ocr(url: str) -> str:
    return url


@workflow.define
class TasksWorkflow:
    @workflow.entrypoint
    async def run(self, urls: list[str]) -> None:
        tasks = [ocr(u) for u in urls]
        results = await asyncio.gather(*tasks)
"""

    graphs = build_graph_statically(source, "/tmp/workflow.py", lambda path: None)

    assert _parallel_lane_labels(graphs[0]) == [["ocr"]]


def test_gather_over_direct_activity_calls_emits_parallel_lanes() -> None:
    """gather(a(), b()) produces one lane per distinct activity call."""
    source = """
import asyncio
from mistralai.workflows import workflow, activity


@activity
async def left() -> int:
    return 1


@activity
async def right() -> int:
    return 2


@workflow.define
class TwoLaneWorkflow:
    @workflow.entrypoint
    async def run(self) -> None:
        a, b = await asyncio.gather(left(), right())
"""

    graphs = build_graph_statically(source, "/tmp/workflow.py", lambda path: None)

    assert _parallel_lane_labels(graphs[0]) == [["left"], ["right"]]


def _count_parallels(graph: AtlasWireFormat) -> int:
    return sum(1 for n in graph.nodes if n.type == "parallel")


def test_gather_does_not_resolve_forward_reference() -> None:
    """A gather over *tasks above the tasks assignment must not render a parallel.

    Such code would raise NameError at runtime, so the graph should not invent a fan-out.
    """
    source = """
import asyncio
from mistralai.workflows import workflow, activity


@activity
async def work(i: int) -> int:
    return i


@workflow.define
class ForwardRefWorkflow:
    @workflow.entrypoint
    async def run(self, items: list[int]) -> None:
        results = await asyncio.gather(*tasks)
        tasks = [work(i) for i in items]
"""

    graphs = build_graph_statically(source, "/tmp/workflow.py", lambda path: None)

    assert _count_parallels(graphs[0]) == 0


def test_local_helper_does_not_leak_across_conditional_branches() -> None:
    """A helper defined only in the if-branch must not resolve in the else-branch."""
    source = """
import asyncio
from mistralai.workflows import workflow, activity


@activity
async def work(i: int) -> int:
    return i


@workflow.define
class BranchScopeWorkflow:
    @workflow.entrypoint
    async def run(self, flag: bool, items: list[int]) -> None:
        if flag:
            async def _run(i: int) -> int:
                return await work(i)

            await asyncio.gather(*[_run(i) for i in items])
        else:
            await asyncio.gather(*[_run(i) for i in items])
"""

    graphs = build_graph_statically(source, "/tmp/workflow.py", lambda path: None)

    # Only the if-branch defines _run, so only it yields a parallel fan-out.
    assert _count_parallels(graphs[0]) == 1


# ---------------------------------------------------------------------------
# Activities awaited inside a larger expression, e.g. results.append(await act())
# ---------------------------------------------------------------------------


def _activity_labels(graph: AtlasWireFormat) -> list[str]:
    return [n.name for n in graph.nodes if n.type == "activity"]


def test_awaited_activity_nested_in_call_is_recognized() -> None:
    """An activity awaited as an argument to another call (results.append(await act()))
    is surfaced as a step, not hidden behind the outer call."""
    source = """
from mistralai.workflows import workflow, activity


@activity
async def publish(title: str) -> str:
    return title


@workflow.define
class AppendWorkflow:
    @workflow.entrypoint
    async def run(self, titles: list[str]) -> list[str]:
        results: list[str] = []
        results.append(await publish(titles[0]))
        return results
"""

    graphs = build_graph_statically(source, "/tmp/workflow.py", lambda path: None)

    assert _activity_labels(graphs[0]) == ["publish"]


def test_same_line_nested_awaits_of_same_activity_are_distinct_steps() -> None:
    source = """
from mistralai.workflows import workflow, activity


@activity
async def publish(title: str) -> str:
    return title


@workflow.define
class SameLineWorkflow:
    @workflow.entrypoint
    async def run(self, titles: list[str]) -> list[str]:
        results: list[str] = []
        results.extend([await publish(titles[0]), await publish(titles[1])])
        return results
"""

    graph = build_graph_statically(source, "/tmp/workflow.py", lambda path: None)[0]

    publish_nodes = [n for n in graph.nodes if n.type == "activity" and n.name == "publish"]
    assert len(publish_nodes) == 2
    assert len({n.id for n in publish_nodes}) == 2


def test_awaited_activity_inside_lambda_body_is_not_a_step() -> None:
    # `await` inside a lambda body is a compile-time SyntaxError, but `ast.parse`
    # (which the static analyzer uses) accepts it. This exercises the parse-level
    # guard in `_awaited_calls_in_order` that skips lambda bodies. The structural
    # assertion guards against a swallowed parse error silently yielding an empty
    # graph (which would make the `== []` activity check pass vacuously).
    source = """
from mistralai.workflows import workflow, activity


@activity
async def publish(title: str) -> str:
    return title


@workflow.define
class CallbackWorkflow:
    @workflow.entrypoint
    async def run(self, title: str) -> None:
        configure(lambda: await publish(title))
"""

    graphs = build_graph_statically(source, "/tmp/workflow.py", lambda path: None)

    assert {n.type for n in graphs[0].nodes} == {"workflow", "entrypoint", "output"}
    assert _activity_labels(graphs[0]) == []


def test_awaited_activity_nested_inside_loop_conditional_is_recognized() -> None:
    """The activity in `results.append(await publish(...))` inside a for/if must be
    recognized as a loop child rather than collapsing to an ellipsis."""
    source = """
from mistralai.workflows import workflow, activity


@activity
async def publish(title: str) -> str:
    return title


@workflow.define
class LoopWorkflow:
    @workflow.entrypoint
    async def run(self, titles: list[str]) -> list[str]:
        results: list[str] = []
        for title in titles:
            if title:
                results.append(await publish(title))
            else:
                results.append("skipped")
        return results
"""

    graph = build_graph_statically(source, "/tmp/workflow.py", lambda path: None)[0]

    # The conditional is preserved as a loop child (not flattened); publish lives
    # in its true branch.
    assert "publish" in _activity_labels(graph)
    loop = next(n for n in graph.nodes if n.type == "loop")
    cond = next(n for n in graph.nodes if n.type == "conditional")
    publish_id = next(n.id for n in graph.nodes if n.name == "publish")
    assert loop.children == [cond.id]
    assert cond.branchTrue == [publish_id]


# ---------------------------------------------------------------------------
# Conditionals inside loops are preserved (not flattened)
# ---------------------------------------------------------------------------


def _edges_from(graph: AtlasWireFormat, node_id: str) -> list[FlatEdge]:
    return [e for e in graph.edges if e.from_ == node_id]


def test_conditional_inside_loop_keeps_branch_edges() -> None:
    source = """
from mistralai.workflows import workflow, activity


@activity
async def publish(title: str) -> str:
    return title


@workflow.define
class LoopWorkflow:
    @workflow.entrypoint
    async def run(self, titles: list[str]) -> list[str]:
        results: list[str] = []
        for title in titles:
            if title:
                results.append(await publish(title))
            else:
                results.append("skipped")
        return results
"""

    graph = build_graph_statically(source, "/tmp/workflow.py", lambda path: None)[0]

    cond = next(n for n in graph.nodes if n.type == "conditional")
    assert cond.branchTrue is not None and len(cond.branchTrue) == 1
    assert cond.branchFalse is not None and len(cond.branchFalse) == 1
    assert cond.branchDescendants is not None
    assert len(cond.branchDescendants) == 2

    kinds = sorted(e.kind for e in _edges_from(graph, cond.id))
    assert kinds == ["branch_false", "branch_true"]


def test_nested_conditional_inside_loop_branch_is_preserved() -> None:
    source = """
from mistralai.workflows import workflow, activity


@activity
async def publish(title: str) -> str:
    return title


@workflow.define
class LoopWorkflow:
    @workflow.entrypoint
    async def run(self, titles: list[str]) -> None:
        for title in titles:
            if title:
                if title.startswith("a"):
                    await publish(title)
"""

    graph = build_graph_statically(source, "/tmp/workflow.py", lambda path: None)[0]

    loop = next(n for n in graph.nodes if n.type == "loop")
    outer = next(n for n in graph.nodes if n.type == "conditional" and n.name == "title")
    inner = next(n for n in graph.nodes if n.type == "conditional" and n.id != outer.id)
    publish_id = next(n.id for n in graph.nodes if n.name == "publish")

    assert loop.children == [outer.id]
    assert outer.branchTrue == [inner.id]
    assert inner.branchTrue == [publish_id]


def test_conditional_without_else_inside_loop_emits_skip_edge() -> None:
    """A missing else inside a loop still yields exactly one false output (a skip),
    so _validate_flat_graph (run inside build_graph_statically) does not raise."""
    source = """
from mistralai.workflows import workflow, activity


@activity
async def publish(title: str) -> str:
    return title


@workflow.define
class LoopWorkflow:
    @workflow.entrypoint
    async def run(self, titles: list[str]) -> list[str]:
        for title in titles:
            if title:
                await publish(title)
"""

    graph = build_graph_statically(source, "/tmp/workflow.py", lambda path: None)[0]

    cond = next(n for n in graph.nodes if n.type == "conditional")
    node_ids = {n.id for n in graph.nodes}
    out_kinds = {e.kind for e in _edges_from(graph, cond.id)}
    false_skip = next(e for e in _edges_from(graph, cond.id) if e.kind == "branch_false_skip")
    assert "branch_true" in out_kinds
    assert "branch_false_skip" in out_kinds
    assert false_skip.to in node_ids


def test_conditional_inside_loop_branch_descendants_include_parallel_children() -> None:
    source = """
import asyncio
from mistralai.workflows import workflow, activity


@activity
async def publish(title: str) -> str:
    return title


@activity
async def notify(title: str) -> str:
    return title


@workflow.define
class LoopWorkflow:
    @workflow.entrypoint
    async def run(self, titles: list[str]) -> None:
        for title in titles:
            if title:
                await asyncio.gather(publish(title), notify(title))
"""

    graph = build_graph_statically(source, "/tmp/workflow.py", lambda path: None)[0]

    cond = next(n for n in graph.nodes if n.type == "conditional")
    parallel = next(n for n in graph.nodes if n.type == "parallel")
    publish_id = next(n.id for n in graph.nodes if n.name == "publish")
    notify_id = next(n.id for n in graph.nodes if n.name == "notify")

    assert cond.branchTrue == [parallel.id]
    assert cond.branchDescendants is not None
    assert parallel.id in cond.branchDescendants
    assert publish_id in cond.branchDescendants
    assert notify_id in cond.branchDescendants


# ---------------------------------------------------------------------------
# execute_workflow → child_workflow nodes
# ---------------------------------------------------------------------------

_CHILD_WORKFLOW = """
from mistralai.workflows import workflow


@workflow.define
class ChildWorkflow:
    @workflow.entrypoint
    async def run(self, x: str) -> str:
        return x
"""

_PARENT_WORKFLOW = """
import asyncio
from mistralai.workflows import workflow
from child import ChildWorkflow


@workflow.define
class ParentWorkflow:
    @workflow.entrypoint
    async def run(self, x: str) -> str:
        result = await workflow.execute_workflow(workflow=ChildWorkflow, params=x)
        asyncio.create_task(workflow.execute_workflow(workflow=ChildWorkflow, params=x))
        return result
"""


def _child_resolver(path: str) -> str | None:
    return _CHILD_WORKFLOW if path.endswith("child.py") else None


def _parent_child_nodes() -> list[FlatNode]:
    graphs = build_graph_statically(_PARENT_WORKFLOW, "/work/parent.py", _child_resolver)
    assert graphs
    return [n for n in graphs[0].nodes if n.type == "child_workflow"]


def test_execute_workflow_emits_child_workflow_nodes() -> None:
    children = _parent_child_nodes()
    # One awaited + one fire-and-forget call, both rendered as child_workflow.
    assert len(children) == 2
    assert all(n.name == "ChildWorkflow" for n in children)


def test_awaited_child_workflow_links_to_child() -> None:
    awaited = [n for n in _parent_child_nodes() if not n.is_async]
    assert len(awaited) == 1
    node = awaited[0]
    assert node.child_workflow_id == "ChildWorkflow"
    assert node.child_workflow_file == "/work/child.py"


def test_fire_and_forget_child_workflow_is_async() -> None:
    fire_and_forget = [n for n in _parent_child_nodes() if n.is_async]
    assert len(fire_and_forget) == 1
    node = fire_and_forget[0]
    assert node.is_async is True
    assert node.child_workflow_id == "ChildWorkflow"
    assert node.child_workflow_file == "/work/child.py"


_PARENT_ALIASED_CHILD_WORKFLOW = """
from mistralai.workflows import workflow
from child import ChildWorkflow as ImportedChildWorkflow


@workflow.define
class ParentWorkflow:
    @workflow.entrypoint
    async def run(self, x: str) -> str:
        result = await workflow.execute_workflow(workflow=ImportedChildWorkflow, params=x)
        return result
"""


def test_aliased_child_workflow_links_by_class_name() -> None:
    """An aliased import must link by the child's real class __name__ (which Atlas
    registers and navigates by), not the local alias."""
    graphs = build_graph_statically(_PARENT_ALIASED_CHILD_WORKFLOW, "/work/parent.py", _child_resolver)
    assert graphs
    children = [n for n in graphs[0].nodes if n.type == "child_workflow"]
    assert len(children) == 1
    node = children[0]
    assert node.name == "ChildWorkflow"
    assert node.child_workflow_id == "ChildWorkflow"
    assert node.child_workflow_file == "/work/child.py"


_PARENT_AWAITED_CREATE_TASK = """
import asyncio
from mistralai.workflows import workflow
from child import ChildWorkflow


@workflow.define
class ParentWorkflow:
    @workflow.entrypoint
    async def run(self, x: str) -> str:
        result = await asyncio.create_task(workflow.execute_workflow(workflow=ChildWorkflow, params=x))
        return result
"""


def test_awaited_create_task_child_workflow_is_not_async() -> None:
    """`await asyncio.create_task(execute_workflow(...))` is awaited, so the child
    is not fire-and-forget and must not be marked async."""
    graphs = build_graph_statically(_PARENT_AWAITED_CREATE_TASK, "/work/parent.py", _child_resolver)
    assert graphs
    children = [n for n in graphs[0].nodes if n.type == "child_workflow"]
    assert len(children) == 1
    assert not children[0].is_async
    assert children[0].child_workflow_id == "ChildWorkflow"


_PARENT_UNKNOWN_CHILD = """
from mistralai.workflows import workflow


@workflow.define
class ParentWorkflow:
    @workflow.entrypoint
    async def run(self, x: str) -> str:
        result = await workflow.execute_workflow(workflow=ExternalWorkflow, params=x)
        return result
"""


def test_child_workflow_not_in_scanned_set_has_no_link() -> None:
    graphs = build_graph_statically(_PARENT_UNKNOWN_CHILD, "/work/parent.py", lambda path: None)
    assert graphs
    children = [n for n in graphs[0].nodes if n.type == "child_workflow"]
    assert len(children) == 1
    node = children[0]
    # Still rendered as a child_workflow node, just not navigable.
    assert node.name == "ExternalWorkflow"
    assert node.child_workflow_id is None
    assert node.child_workflow_file is None
