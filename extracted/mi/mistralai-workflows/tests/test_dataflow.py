"""Tests for the dataflow analysis module."""

import json
from pathlib import Path

from mistralai.workflows.core._dataflow import (
    CONTROL_FLOW_VIEW,
    _contained_nodes,
    analyze,
    build_dataflow_views,
    expand_views,
    nodes_skipped,
    rendered_order,
)
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
    assert len(data_edges) >= 2


def test_two_paths_split_is_drawn_as_a_fan_out_and_a_fan_in():
    """The producer fans into the box and the chains fan out of it.

    A `return` composes both chains' results, so the terminus is what they
    reconverge on. Reads inside a return land on the entrypoint, which is not a
    data sink — crediting them to the terminus instead is what gives the split
    a join, and the join is what the box's bottom means.
    """
    df = _get_view("Data flow")
    box = next(n for n in df["nodes"] if n["type"] == "lineage")["id"]
    producer = next(n for n in df["nodes"] if n["name"] == "fetch_all_packages")["id"]
    out = next(n for n in df["nodes"] if n["type"] == "output")["id"]
    edges = [(e["from"], e["to"], e.get("label")) for e in df["edges"] if e["kind"] == "data_dep"]

    assert (producer, box, "all_pkgs") in edges, "the producer fans out into the box"

    leaving = [e for e in edges if e[0] == box]
    assert len(leaving) == 1, f"the chains reconverge as one fan-in, got {leaving}"
    assert leaving[0][1] == out
    assert set(leaving[0][2].split(", ")) == {"pypi_missing", "npm_unscoped"}


def test_two_paths_splits_into_tracks():
    """`all_pkgs.python` feeds the loop and `all_pkgs.npm` feeds the filter, and
    the chains rejoin on the result. Two tracks in one box, with the value that
    splits named on the way in."""
    df = _get_view("Data flow")
    box = next(n for n in df["nodes"] if n["type"] == "lineage")
    assert box["name"] == "all_pkgs"
    assert len(box["branches"]) == 2, "one track per chain"
    assert {len(b) for b in box["branches"]} == {1}, "a loop on one side, an activity on the other"


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


# -- Containment-aware reachability (Bug 2) -----------------------------------


# -- Nested-helper read resolution (Bug 3) -----------------------------------

_NESTED_HELPER_WORKFLOW = """
import asyncio
from mistralai import workflows

@workflows.activity()
async def fetch_items() -> list:
    return []

@workflows.activity()
async def process(item: str) -> str:
    return item

@workflows.workflow.define(name="nested_helper")
class NestedHelper:
    @workflows.workflow.entrypoint
    async def run(self) -> list:
        items = await fetch_items()
        sem = asyncio.Semaphore(5)

        async def _work(x: str) -> str:
            async with sem:
                return await process(x)

        results = await asyncio.gather(*[_work(i) for i in items])
        return results
"""


def test_nested_helper_reads_resolve_to_caller():
    """A read of an outer var inside a nested helper creates an edge to the
    node that *calls* the helper, not to the entrypoint or nowhere."""
    graph = build_graph_statically(_NESTED_HELPER_WORKFLOW, "/tmp/nested.py", lambda _: None)[0]
    df = next(v for v in expand_views(graph.to_dict(include_sources=True)) if v["view"] == "Data flow")

    sem_edges = [e for e in df["edges"] if e["kind"] == "data_dep" and e["label"] == "sem"]
    assert sem_edges, "expected a data_dep edge for 'sem'"
    targets = {e["to"] for e in sem_edges}
    assert not any("entrypoint" in t for t in targets), f"sem edge should not target entrypoint: {targets}"


def test_nested_helper_reads_resolve_to_every_caller():
    source = _NESTED_HELPER_WORKFLOW.replace(
        "results = await asyncio.gather(*[_work(i) for i in items])\n        return results",
        """first = await asyncio.gather(*[_work(i) for i in items])
        second = await asyncio.gather(*[_work(i) for i in items])
        return first + second""",
    )
    graph = build_graph_statically(source, "/tmp/nested_twice.py", lambda _: None)[0]
    raw = analyze(graph.to_dict(include_sources=True))

    parallel_ids = {n["id"] for n in raw.df_nodes if n["type"] == "parallel"}
    sem_targets = {e["to"] for e in raw.data_edges if e["kind"] == "data_dep" and e.get("label") == "sem"}

    assert sem_targets == parallel_ids


# -- Nearest-preceding-writer (Bug 4) ----------------------------------------

_MUTATION_CHAIN_WORKFLOW = """
from mistralai import workflows

@workflows.activity()
async def get_expense() -> dict:
    return {}

@workflows.activity()
async def ask_manager(amount: float) -> dict:
    return {}

@workflows.activity()
async def ask_director(amount: float) -> dict:
    return {}

@workflows.workflow.define(name="mutation_chain")
class MutationChain:
    @workflows.workflow.entrypoint
    async def run(self) -> float:
        expense = await get_expense()
        current_amount = expense["amount"]

        mgr = await ask_manager(current_amount)
        if mgr["approved"]:
            current_amount = mgr["approved_amount"]

        director = await ask_director(current_amount)
        if director["approved"]:
            current_amount = director["approved_amount"]

        return current_amount
"""


def test_mutation_chain_nearest_preceding_writer():
    """Each reader of a mutation-chain var should be fed by its nearest
    preceding writer, not the textually-last one."""
    graph = build_graph_statically(_MUTATION_CHAIN_WORKFLOW, "/tmp/mutation.py", lambda _: None)[0]
    df = next(v for v in expand_views(graph.to_dict(include_sources=True)) if v["view"] == "Data flow")

    ca_edges = [e for e in df["edges"] if e["kind"] == "data_dep" and e.get("label") and "current_amount" in e["label"]]
    assert ca_edges, "expected data_dep edges for current_amount"

    sources = {e["from"].split("::")[-1] for e in ca_edges}
    assert len(sources) > 1, f"all current_amount edges come from a single writer: {sources}"


# -- Analysis/policy boundary (Step 1) ---------------------------------------


def test_dependency_graph_is_assertable_without_monkeypatching():
    """The raw graph is a first-class value: tests assert on its edges directly,
    no monkeypatching `_compute_data_edges`. The mutation-chain workflow's raw
    edges include a current_amount fan-out from multiple writers."""
    graph = build_graph_statically(_MUTATION_CHAIN_WORKFLOW, "/tmp/mutation.py", lambda _: None)[0]
    raw = analyze(graph.to_dict(include_sources=True))

    ca = [e for e in raw.data_edges if e["kind"] == "data_dep" and "current_amount" in (e.get("label") or "")]
    assert ca, "raw graph should have current_amount edges before any policy"
    assert len(raw.df_nodes) > 0
    assert any(n["type"] == "transform" for n in raw.transforms)


def test_dependency_graph_is_not_corrupted_by_build():
    """Display policy mutates edges and nodes in place; the raw graph a caller
    holds must stay pristine. This is the boundary that makes display changes
    unable to corrupt the analysis."""
    import copy as _copy

    graph = build_graph_statically(_MUTATION_CHAIN_WORKFLOW, "/tmp/mutation.py", lambda _: None)[0]
    cf = graph.to_dict(include_sources=True)
    raw = analyze(cf)

    edges_snapshot = _copy.deepcopy(raw.data_edges)
    nodes_snapshot = _copy.deepcopy(raw.df_nodes)

    build_dataflow_views(cf)

    assert raw.data_edges == edges_snapshot, "policy corrupted raw.data_edges"
    assert raw.df_nodes == nodes_snapshot, "policy corrupted raw.df_nodes"


# -- The display rule --------------------------------------------------------


def _view(name: str, source: str) -> dict:
    wire = build_graph_statically(source, f"/tmp/{name}.py", lambda _: None)[0]
    return build_dataflow_views(wire.model_dump(by_alias=True))[0]


def test_return_edge_is_dropped_when_it_skips_a_node():
    source = """\
from mistralai.workflows import workflow

@workflow.activity()
async def produce() -> str:
    return "x"

@workflow.activity()
async def consume(value: str) -> None:
    pass

@workflow.define(name="reader-then-return")
class ReaderThenReturn:
    @workflow.entrypoint
    async def run(self) -> str:
        x = await produce()
        await consume(x)
        return x
"""
    dataflow = _view("reader_then_return", source)
    producer_id = next(n["id"] for n in dataflow["nodes"] if n.get("name") == "produce")
    consumer_id = next(n["id"] for n in dataflow["nodes"] if n.get("name") == "consume")
    output_id = next(n["id"] for n in dataflow["nodes"] if n["type"] == "output")
    data_edges = [e for e in dataflow["edges"] if e["kind"] == "data_dep"]

    assert not [e for e in data_edges if e["to"] == output_id]
    assert any(e["from"] == producer_id and e["to"] == consumer_id and e.get("label") == "x" for e in data_edges)


def test_standalone_data_dep_requires_a_branch_or_a_join():
    source = """\
from mistralai.workflows import workflow

@workflow.activity()
async def make() -> str:
    return "v"

@workflow.activity()
async def use_one(value: str) -> None:
    pass

@workflow.activity()
async def use_two(value: str) -> None:
    pass

@workflow.define(name="fanout-vs-chain")
class FanoutVsChain:
    @workflow.entrypoint
    async def run(self) -> None:
        a = await make()
        b = await make()
        await use_one(b)
        await use_two(b)
        await use_one(a)
        c = await make()
        await use_two(c)
"""
    dataflow = _view("fanout_vs_chain", source)
    labels = {e.get("label") for e in dataflow["edges"] if e["kind"] == "data_dep"}

    assert "a" not in labels
    assert "b" in labels
    assert "c" in labels


def test_multi_statement_ellipsis_keeps_transforms_in_their_loop():
    source = """\
from mistralai.workflows import workflow

@workflow.activity()
async def fetch(item: str) -> list[str]:
    return []

@workflow.define(name="trailing-body-statements")
class TrailingBodyStatements:
    @workflow.entrypoint
    async def run(self, items: list[str]) -> None:
        collected: list[str] = []
        for item in items:
            found = await fetch(item)
            kept = [f for f in found if f]
            collected.append((item, kept))
"""
    dataflow = _view("trailing_body", source)
    loop = next(n for n in dataflow["nodes"] if n["type"] == "loop")
    children = set(loop.get("children") or [])
    loop_begin = loop["source_range"]["begin"]
    body_transforms = {
        n["id"] for n in dataflow["nodes"] if n["type"] == "transform" and n["source_range"]["begin"] > loop_begin
    }

    assert body_transforms
    assert body_transforms <= children
    assert not [
        e for e in dataflow["edges"] if e["kind"] == "data_dep" and e["from"] == loop["id"] and e["to"] in children
    ]


def test_non_ascii_before_identifier_maps_correct_byte_range():
    source = """\
from mistralai.workflows import workflow

@workflow.activity()
async def step() -> int:
    return 1

@workflow.define(name="non-ascii-col")
class NonAsciiCol:
    @workflow.entrypoint
    async def run(self) -> int:
        é = 1; value = 2 + 2
        return value
"""
    wire = build_graph_statically(source, "/tmp/non_ascii_col.py", lambda _: None)[0]
    raw = analyze(wire.model_dump(by_alias=True))
    transform = next(n for n in raw.transforms if n.get("name", "").startswith("value"))

    assert transform["source_range"]["begin"] == source.encode().index(b"value")
    assert transform["name"] == "value = 2 + 2"


def test_inlined_helper_keeps_control_flow_spine_order():
    source = """\
from mistralai.workflows import workflow

@workflow.activity()
async def step() -> None:
    pass

@workflow.define(name="helper-above-entrypoint")
class HelperAboveEntrypoint:
    async def _body(self) -> None:
        for _ in range(3):
            await step()

    @workflow.entrypoint
    async def run(self) -> None:
        await self._body()
"""
    wire = build_graph_statically(source, "/tmp/helper_above_entrypoint.py", lambda _: None)[0]
    cf = wire.model_dump(by_alias=True)
    dataflow = build_dataflow_views(cf)[0]

    def chain(view: dict) -> list[str]:
        nxt = {e["from"]: e["to"] for e in view["edges"] if e["kind"] == "sequential"}
        order, current = [], "helper-above-entrypoint"
        while current is not None and current not in order:
            order.append(current)
            current = nxt.get(current)
        return order

    df_chain = chain(dataflow)
    loop_id = next(n["id"] for n in dataflow["nodes"] if n["type"] == "loop")
    entrypoint_id = next(n["id"] for n in dataflow["nodes"] if n["type"] == "entrypoint")

    assert df_chain == chain(cf)
    assert df_chain.index(entrypoint_id) < df_chain.index(loop_id)


def test_a_guard_passes_a_value_on_without_claiming_to_make_it():
    source = """\
from mistralai.workflows import workflow

@workflow.activity()
async def make() -> str:
    return "v"

@workflow.activity()
async def note(value: str) -> None:
    pass

@workflow.activity()
async def use_one(value: str) -> None:
    pass

@workflow.activity()
async def use_two(value: str) -> None:
    pass

@workflow.define(name="merging-guard")
class MergingGuard:
    @workflow.entrypoint
    async def run(self) -> None:
        v = await make()
        if v:
            await note(v)
        await use_one(v)
        await use_two(v)
"""
    dataflow = _view("merging_guard", source)
    conds = {n["id"] for n in dataflow["nodes"] if n["type"] == "conditional"}
    maker = next(n["id"] for n in dataflow["nodes"] if n.get("name") == "make")
    data_edges = [e for e in dataflow["edges"] if e["kind"] == "data_dep"]

    assert [e for e in data_edges if e["from"] == maker and e["to"] in conds]


_SPLIT_WORKFLOW = """\
from mistralai.workflows import workflow

@workflow.activity()
async def fetch() -> list:
    return []

@workflow.activity()
async def use_py(v: list) -> None:
    pass

@workflow.activity()
async def use_npm(v: list) -> None:
    pass

@workflow.activity()
async def report(a: list, b: list) -> None:
    pass

@workflow.define(name="split-then-join")
class SplitThenJoin:
    @workflow.entrypoint
    async def run(self) -> None:
        all_pkgs = await fetch()
        py = [p for p in all_pkgs if p]
        npm = [p for p in all_pkgs if not p]
        await use_py(py)
        await use_npm(npm)
        await report(py, npm)
"""


def test_no_data_edge_is_drawn_past_a_node():
    """The rule, as an invariant rather than a filter.

    A data edge earns its place as a fan-out into a box or a fan-in out of one,
    both a single step. Anything drawn past a node is a dependency the structure
    failed to express, and no amount of routing makes it read right (P3).
    """
    view = _view("split_then_join", _SPLIT_WORKFLOW)
    order = rendered_order(view["nodes"], view["edges"], view["workflow_name"])
    inside = _contained_nodes(view["nodes"], view["edges"])
    for e in view["edges"]:
        if e["kind"] != "data_dep":
            continue
        assert nodes_skipped(e, order, inside) == 0, f"{e['from']} -> {e['to']} is drawn past a node"


def test_a_split_becomes_tracks_not_long_lines():
    """`all_pkgs` derives into a python chain and an npm chain that reconverge
    on `report`. The chains become tracks in one box, so the dependency is said
    by containment instead of by two lines running the length of the diagram."""
    view = _view("split_then_join", _SPLIT_WORKFLOW)
    box = next(n for n in view["nodes"] if n["type"] == "lineage")
    assert len(box["branches"]) == 2, "one track per chain"
    assert box["name"] == "all_pkgs", "the box is named for the value that splits"

    crossing = [
        e for e in view["edges"] if e["kind"] == "data_dep" and (e["from"] == box["id"]) != (e["to"] == box["id"])
    ]
    assert len(crossing) == 2, "exactly a fan-out and a fan-in cross the wall"
    assert {e["to"] == box["id"] for e in crossing} == {True, False}


def test_tracks_keep_control_order_so_they_claim_no_concurrency():
    """Tracks are a claim about derivation. Vertical position stays control
    order — reordering rows is the concurrency claim P6 forbids, and only
    `parallel`, emitted from a real gather, is entitled to make it."""
    view = _view("split_then_join", _SPLIT_WORKFLOW)
    box = next(n for n in view["nodes"] if n["type"] == "lineage")
    by_id = {n["id"]: n for n in view["nodes"]}
    order = rendered_order(view["nodes"], view["edges"], view["workflow_name"])
    rows = [order[c] for b in box["branches"] for c in b]
    assert len(rows) == len(set(rows)), "no two track members share a row"
    member_lines = [by_id[c]["line"] for c in box["children"]]
    assert member_lines == sorted(member_lines)
    assert not [n for n in view["nodes"] if n["type"] == "parallel"], "no gather in the source"


def test_a_split_without_a_join_is_not_boxed():
    source = """\
from mistralai.workflows import workflow

@workflow.activity()
async def fetch() -> str:
    return "value"

@workflow.activity()
async def one(value: str) -> None:
    pass

@workflow.activity()
async def two(value: str) -> None:
    pass

@workflow.define(name="unjoined-split")
class UnjoinedSplit:
    @workflow.entrypoint
    async def run(self) -> None:
        value = await fetch()
        await one(value)
        await two(value)
"""
    view = _view("unjoined_split", source)

    assert not [n for n in view["nodes"] if n["type"] == "lineage"]


# -- Trivial-transform revert -------------------------------------------------


def _views(source: str, name: str = "wf") -> tuple[dict, dict]:
    wire = build_graph_statically(source, f"/tmp/{name}.py", lambda _: None)[0]
    expanded = expand_views(wire.to_dict(include_sources=True))
    cf = next(v for v in expanded if v["view"] == "Control flow")
    df = next(v for v in expanded if v["view"] == "Data flow")
    return cf, df


_NO_DATA_FLOW_WORKFLOW = """\
import logging

from mistralai.workflows import workflow

logger = logging.getLogger(__name__)


@workflow.activity()
async def step() -> None:
    pass


@workflow.define(name="no-flow")
class NoFlow:
    @workflow.entrypoint
    async def run(self) -> str:
        logger.info("starting")
        self._state = "ready"
        await step()
        return self._state
"""


def test_no_data_flow_reverts_to_control_flow():
    """When no `data_dep` edge (bar `self`) survives suppression, exploding
    ellipses into transforms reshapes the graph for nothing. The view reverts:
    every ellipsis is kept, so the data-flow view tracks control flow
    node-for-node, sequential chain included."""
    cf, df = _views(_NO_DATA_FLOW_WORKFLOW, "no-flow")
    assert len(df["nodes"]) == len(cf["nodes"]), "DF should track CF node-for-node"
    assert not [n for n in df["nodes"] if n["type"] == "transform"]
    cf_seq = {e["from"]: e["to"] for e in cf["edges"] if e["kind"] == "sequential"}
    df_seq = {e["from"]: e["to"] for e in df["edges"] if e["kind"] == "sequential"}
    assert df_seq == cf_seq, "reverted ellipses keep their CF sequential edges"


def test_self_edge_does_not_keep_the_view_exploded():
    """`self`-into-the-first-assignment is universal method noise, so a
    `self`-labelled edge does not count as data flow. The `self._state` write
    below is an attribute, not a scope binding, so it yields only a `self`
    edge — and the view still reverts."""
    cf, df = _views(_NO_DATA_FLOW_WORKFLOW, "no-flow")
    assert not [n for n in df["nodes"] if n["type"] == "transform"]
    assert not [e for e in df["edges"] if e["kind"] == "data_dep" and e.get("label") == "self"], (
        "the self edge disappears with the reverted transform"
    )
    assert len(df["nodes"]) == len(cf["nodes"])


_WITH_DATA_FLOW_WORKFLOW = """\
from mistralai.workflows import workflow


@workflow.activity()
async def fetch() -> int:
    return 1


@workflow.define(name="with-flow")
class WithFlow:
    @workflow.entrypoint
    async def run(self) -> int:
        base = await fetch()
        doubled = base + base
        return doubled
"""


def test_real_data_flow_keeps_transforms_exploded():
    """A transform whose `data_dep` edge survives suppression stays exploded,
    so the view shows the derivation instead of collapsing to control flow."""
    _cf, df = _views(_WITH_DATA_FLOW_WORKFLOW, "with-flow")
    transforms = [n for n in df["nodes"] if n["type"] == "transform"]
    assert any(n["name"].startswith("doubled") for n in transforms), [n["name"] for n in transforms]
    labels = {e.get("label") for e in df["edges"] if e["kind"] == "data_dep"}
    assert "base" in labels, f"the fetch -> doubled edge should survive: {labels}"


_SIDE_EFFECT_STEP_WORKFLOW = """\
import logging

from mistralai.workflows import workflow

logger = logging.getLogger(__name__)


@workflow.activity()
async def fetch() -> int:
    return 1


@workflow.define(name="side-effects")
class SideEffects:
    @workflow.entrypoint
    async def run(self) -> int:
        logger.info("starting")
        base = await fetch()
        doubled = base + base
        logger.info("done")
        return doubled
"""


def test_a_statement_with_no_assignment_keeps_its_node():
    """An ellipsis holding only a bare call explodes into nothing, and must
    therefore keep its own node rather than vanish.

    The view has real data flow here, so the transforms stay exploded and the
    whole-view revert does not fire. Both `logger.info(...)` lines are still
    steps the workflow runs; dropping them left `kyc-prefill-workflow` showing
    10 of its 22 nodes, every `self._update_step(...)` gone.
    """
    cf, df = _views(_SIDE_EFFECT_STEP_WORKFLOW, "side-effects")
    assert any(n["type"] == "transform" for n in df["nodes"]), "expected the exploded view"
    assert len(df["nodes"]) >= len(cf["nodes"]), (
        f"data-flow view lost nodes: {sorted({n['id'] for n in cf['nodes']} - {n['id'] for n in df['nodes']})}"
    )


_CONTINUE_AS_NEW_WORKFLOW = """\
from mistralai.workflows import workflow


@workflow.activity()
async def step() -> None:
    pass


@workflow.define(name="restart-guard")
class RestartGuard:
    @workflow.entrypoint
    async def run(self) -> str:
        should_restart = True
        if should_restart:
            workflow.continue_as_new(self.run, {})
        await step()
        return "done"
"""


def test_continue_as_new_survives_into_the_data_flow_view():
    """A `continue_as_new` node must appear in the data-flow view, not be
    dropped by the keep-type filter. Dropping it strips the `branch_true` edge
    and `branchDescendants` off any conditional guarding a restart, leaving
    the conditional rendered with no expandable branch."""
    _cf, df = _views(_CONTINUE_AS_NEW_WORKFLOW, "restart-guard")
    types = {n["type"] for n in df["nodes"]}
    assert "continue_as_new" in types, f"continue_as_new missing from DF: {types}"
    # The guard conditional keeps its branch_descendant so the branch renders.
    conds = [n for n in df["nodes"] if n["type"] == "conditional"]
    assert conds, "expected the restart guard conditional"
    assert any(conds[0].get("branchDescendants")), "guard lost its branchDescendants"


def test_data_flow_preserves_new_executable_node_types():
    """The analyzed node list is authoritative; a new walker node type must
    not need a second registration in the data-flow builder."""
    wire = build_graph_statically(
        _CONTINUE_AS_NEW_WORKFLOW,
        "/tmp/restart-guard.py",
        lambda _: None,
    )[0]
    cf = wire.to_dict(include_sources=True)
    step = next(n for n in cf["nodes"] if n["type"] == "activity")
    step["type"] = "future_step"

    df = build_dataflow_views(cf)[0]

    assert step["id"] in {n["id"] for n in df["nodes"]}
