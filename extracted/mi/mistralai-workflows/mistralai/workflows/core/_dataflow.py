"""Build data-flow graph views from a control-flow wire format payload.

Takes a v3 wire format dict (with embedded source) and produces a
data-flow view alongside the original control-flow view.
"""

from __future__ import annotations

import bisect
import copy
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

import libcst as cst
import libcst.metadata as meta
import structlog

logger = structlog.get_logger()

CONTROL_FLOW_VIEW = "Control flow"
DATA_FLOW_VIEW = "Data flow"
# Ceiling on source fed to the CST parse; a larger module risks OOM.
_MAX_SOURCE_BYTES = 512_000
# Boxes whose children sit in side-by-side tracks. ``parallel`` is a real
# ``asyncio.gather``; ``lineage`` is a split :func:`_detect_lineage_tracks`
# found in the data. Same geometry, different claim — only ``parallel`` asserts
# concurrency, which is why a track keeps its row in control order.
_LANE_CONTAINER_TYPES = frozenset({"parallel", "lineage"})
_STRUCTURAL_TYPES = frozenset({"conditional", "loop", "try_except"}) | _LANE_CONTAINER_TYPES
_NON_VALUE_BINDINGS = (cst.FunctionDef, cst.ClassDef, cst.Import, cst.ImportFrom)
_CF_BRANCH_KINDS = frozenset(
    {
        "branch_true",
        "branch_false",
        "branch_merge",
        "branch_true_skip",
        "branch_false_skip",
        "branch_exit_true",
        "branch_exit_false",
    }
)


def build_dataflow_views(
    control_flow: dict[str, Any],
) -> list[dict[str, Any]]:
    """Return a data-flow view payload from a control-flow payload."""
    try:
        return [_build(control_flow)]
    except Exception as exc:
        logger.warning("Data-flow analysis failed", exc_info=exc)
        # Only the exception type crosses the boundary: libcst's ParserSyntaxError
        # renders the offending source line, which would persist customer source
        # into the graphs API. The full message stays in the worker's own logs.
        return [_error_payload(control_flow, type(exc).__name__)]


def expand_views(cf_payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Return control-flow payload (with view field) plus dataflow views."""
    cf = {**cf_payload, "view": CONTROL_FLOW_VIEW}
    return [cf, *build_dataflow_views(cf)]


def _explode_unknowns(
    cf: dict[str, Any],
) -> tuple[list[dict[str, Any]], set[str], list[dict[str, Any]]]:
    """Return (transforms, unknown_ids, nodes) for a control-flow payload.

    The cheap subset of :func:`_build` — parse, assignment collection and
    ellipsis explosion only, with no edge computation, fan-out detection or
    suppression passes. Use on hot paths that only need the transform nodes.
    """
    sources: dict[str, str] = cf.get("sources") or {}
    primary_file: str | None = cf.get("primary_file")
    source_text = _pick_source(sources, primary_file)
    if source_text is None:
        return [], set(), []
    source_bytes = source_text.encode("utf-8")
    if len(source_bytes) > _MAX_SOURCE_BYTES:
        return [], set(), []
    line_starts = _build_line_starts(source_bytes)
    wrapper = meta.MetadataWrapper(cst.parse_module(source_text))
    positions = wrapper.resolve(meta.PositionProvider)
    collector = _AssignmentCollector()
    wrapper.visit(collector)
    for info in collector.assignments:
        code_range = positions.get(info["cst_node"])
        if code_range and isinstance(code_range, meta.CodeRange):
            info["line"] = code_range.start.line
            info["byte_offset"] = _line_col_to_byte_offset(
                line_starts,
                code_range.start.line,
                code_range.start.column,
            )
            info["byte_length"] = (
                _line_col_to_byte_offset(
                    line_starts,
                    code_range.end.line,
                    code_range.end.column,
                )
                - info["byte_offset"]
            )
    nodes = copy.deepcopy(cf.get("nodes", []))
    transforms, unknown_ids = _expand_unknown_nodes(
        nodes,
        collector.assignments,
        cf.get("workflow_name", ""),
    )
    return transforms, unknown_ids, nodes


def dataflow_only_nodes(
    cf: dict[str, Any],
    views: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Nodes the data-flow views add on top of the control-flow graph.

    Two kinds: transforms (one per assignment split out of an ellipsis) and
    fan-out groups. The summariser never sees them otherwise, because it runs
    on the control-flow graph.
    """
    known = {n["id"] for n in cf.get("nodes") or []}
    by_id: dict[str, dict[str, Any]] = {}
    for view in views:
        for node in view.get("nodes") or []:
            by_id.setdefault(node["id"], node)

    out: list[dict[str, Any]] = []
    for node in by_id.values():
        if node["id"] in known:
            continue
        out.append({k: v for k, v in node.items() if k != "target_var"})
    return out


def attach_summaries(views: list[dict[str, Any]], summaries: dict[str, Any]) -> None:
    """Give each view the subset of *summaries* keyed to nodes it contains."""
    for view in views:
        ids = {n["id"] for n in view.get("nodes") or []}
        subset = {nid: s for nid, s in summaries.items() if nid in ids}
        if subset:
            view["node_summaries"] = subset
        else:
            view.pop("node_summaries", None)


def build_summary_nodes(cf: dict[str, Any]) -> list[dict[str, Any]]:
    """Data-flow-only nodes for a control-flow payload, building the views.

    For callers that have no built views to hand. Where the views are already
    being built, pass them to :func:`dataflow_only_nodes` instead of paying for
    a second analysis.
    """
    try:
        return dataflow_only_nodes(cf, build_dataflow_views(cf))
    except Exception as exc:
        logger.warning("Data-flow summary node collection failed", exc_info=exc)
        return []


def build_retarget_map(cf: dict[str, Any]) -> dict[str, str]:
    """Map control-flow node ids to their data-flow transform replacements.

    Re-keys unknown/ellipsis node ids to transform ids by matching source
    ranges. Only single-statement ellipses match exactly; a multi-statement one
    explodes into several transforms and is left unmapped, which is why
    transforms are summarised directly (see :func:`dataflow_only_nodes`).
    """
    try:
        transforms, unknown_ids, nodes = _explode_unknowns(cf)
        sr_to_transform: dict[tuple[int, int], str] = {}
        for t in transforms:
            sr = t.get("source_range", {})
            sr_to_transform[(sr.get("begin", 0), sr.get("end", 0))] = t["id"]
        retarget: dict[str, str] = {}
        for n in nodes:
            if n["id"] in unknown_ids:
                sr = n.get("source_range", {})
                key = (sr.get("begin", 0), sr.get("end", 0))
                if key in sr_to_transform:
                    retarget[n["id"]] = sr_to_transform[key]
        return retarget
    except Exception as exc:
        logger.warning("Retarget map failed", exc_info=exc)
        return {}


def _error_payload(cf: dict[str, Any], msg: str) -> dict[str, Any]:
    out = {**cf, "view": DATA_FLOW_VIEW, "nodes": [], "edges": [], "error": msg}
    out.pop("node_summaries", None)
    return out


# ---------------------------------------------------------------------------
# Source helpers
# ---------------------------------------------------------------------------


def _pick_source(sources: dict[str, str], primary_file: str | None) -> str | None:
    if not sources:
        return None
    if primary_file and primary_file in sources:
        return sources[primary_file]
    return next(iter(sources.values()), None)


class _LineStarts(list):
    """Line-start byte offsets with the source bytes attached.

    LibCST reports columns in *characters* while ``line_starts`` are *byte*
    offsets, so :func:`_line_col_to_byte_offset` needs the line's UTF-8 bytes to
    map a character column to a byte offset (they diverge whenever a multi-byte
    char precedes the column on the same line).
    """

    source_bytes: bytes

    def __init__(self, source_bytes: bytes) -> None:
        super().__init__()
        self.source_bytes = source_bytes


def _build_line_starts(source_bytes: bytes) -> _LineStarts:
    """Byte offset of each line start. Index 0 = line 1."""
    starts = _LineStarts(source_bytes)
    starts.append(0)
    for i, b in enumerate(source_bytes):
        if b == ord(b"\n"):
            starts.append(i + 1)
    return starts


def _line_col_to_byte_offset(line_starts: list[int], line: int, col: int) -> int:
    """Convert 1-based line and 0-based character column to a UTF-8 byte offset."""
    if not (1 <= line <= len(line_starts)):
        return line_starts[-1] if line_starts else 0
    line_start = line_starts[line - 1]
    source_bytes = getattr(line_starts, "source_bytes", None)
    if source_bytes is None:
        return line_start + col
    line_end = line_starts[line] if line < len(line_starts) else len(source_bytes)
    line_text = source_bytes[line_start:line_end].decode("utf-8", errors="replace")
    return line_start + len(line_text[:col].encode("utf-8"))


def _offset_to_line(line_starts: list[int], offset: int) -> int:
    """Convert byte offset to 1-based line number."""
    return bisect.bisect_right(line_starts, offset)


def _node_span(n: dict[str, Any]) -> tuple[int, int] | None:
    sr = n.get("source_range") or {}
    begin, end = sr.get("begin"), sr.get("end")
    if begin is None or end is None:
        return None
    return begin, end


# ---------------------------------------------------------------------------
# Node index — maps byte offsets to graph nodes
# ---------------------------------------------------------------------------


def _build_node_index(
    nodes: list[dict[str, Any]],
) -> list[tuple[int, int, dict[str, Any]]]:
    """Sorted (begin, end, node) list for range lookups."""
    result = []
    for n in nodes:
        sr = n.get("source_range", {})
        begin = sr.get("begin")
        end = sr.get("end")
        if begin is not None and end is not None and end > begin:
            result.append((begin, end, n))
    result.sort(key=lambda t: (t[0], -(t[1])))
    return result


def _find_node_at_offset(
    index: list[tuple[int, int, dict[str, Any]]],
    offset: int,
) -> dict[str, Any] | None:
    """Find the tightest (smallest range) node containing offset."""
    # Index is sorted by (begin, -end). Use bisect to skip entries starting
    # after offset, then scan candidates for tightest fit.
    hi = bisect.bisect_right(index, (offset + 1,))
    best: dict[str, Any] | None = None
    best_size = float("inf")
    for i in range(hi):
        begin, end, node = index[i]
        if begin <= offset < end:
            size = end - begin
            if size < best_size:
                best = node
                best_size = size
    return best


def _find_node_on_line(
    index: list[tuple[int, int, dict[str, Any]]],
    line: int,
) -> dict[str, Any] | None:
    """Find the node on this line that can produce a value.

    ``parallel`` is eligible even though it is structural: an
    ``await asyncio.gather(...)`` node covers only the call expression, so the
    enclosing assignment's target sits outside its range and would otherwise be
    credited to whatever container the gather lives in.
    """
    for _, _, node in index:
        if node.get("line") == line and node.get("type") not in (
            "workflow",
            "entrypoint",
            "conditional",
            "loop",
            "try_except",
        ):
            return node
    return None


# ---------------------------------------------------------------------------
# CST visitors
# ---------------------------------------------------------------------------


def _extract_name(node: cst.BaseExpression) -> str | None:
    if isinstance(node, cst.Name):
        return node.value
    if isinstance(node, cst.Attribute):
        return node.attr.value
    if isinstance(node, cst.Subscript):
        return _extract_name(node.value)
    if isinstance(node, cst.Tuple):
        names = [_extract_name(el.value) for el in node.elements if isinstance(el, cst.Element)]
        valid = [n for n in names if n]
        return ", ".join(valid) if valid else None
    return None


class _AssignmentCollector(cst.CSTVisitor):
    """Collect assignment targets with their CST nodes for position resolution."""

    def __init__(self) -> None:
        self.assignments: list[dict[str, Any]] = []

    def visit_Assign(self, node: cst.Assign) -> None:
        for target in node.targets:
            name = _extract_name(target.target)
            if name:
                self._add(name, node)

    def visit_AnnAssign(self, node: cst.AnnAssign) -> None:
        if node.value is not None and node.target:
            name = _extract_name(node.target)
            if name:
                self._add(name, node)

    def visit_AugAssign(self, node: cst.AugAssign) -> None:
        name = _extract_name(node.target)
        if name:
            self._add(name, node)

    def visit_Call(self, node: cst.Call) -> None:
        # x.append(v), x.extend(v) etc. treated as write to x
        if not isinstance(node.func, cst.Attribute):
            return
        if node.func.attr.value not in (
            "append",
            "extend",
            "add",
            "update",
            "insert",
        ):
            return
        name = _extract_name(node.func.value)
        if name:
            self._add(name, node)

    def _add(self, name: str, node: cst.CSTNode) -> None:
        self.assignments.append(
            {
                "target": name,
                "cst_node": node,
                "line": 0,
                "byte_offset": 0,
                "byte_length": 0,
            }
        )


class _ReturnCollector(cst.CSTVisitor):
    """Collect ``return <value>`` statements, whose reads leave the workflow."""

    def __init__(self) -> None:
        self.returns: list[cst.Return] = []

    def visit_Return(self, node: cst.Return) -> None:
        if node.value is not None:
            self.returns.append(node)


def _cst_to_byte_offset(
    positions: Mapping[cst.CSTNode, Any],
    node: cst.CSTNode,
    line_starts: list[int],
) -> int | None:
    pos = positions.get(node)
    if isinstance(pos, meta.CodeRange):
        return _line_col_to_byte_offset(line_starts, pos.start.line, pos.start.column)
    return None


# ---------------------------------------------------------------------------
# Step 2: Ellipsis explosion
# ---------------------------------------------------------------------------

_MAX_TRANSFORM_NAME = 120
_REDACTED_LITERAL = '"…"'


class _LiteralRedactor(cst.CSTTransformer):
    """Blank out string literals in a transform label.

    Transform labels are rendered from workflow source and uploaded to the
    graphs API, so a literal secret (`API_KEY = "sk-live-..."`) would leave the
    worker verbatim. Identifiers and operators are kept — they are what makes
    the label readable, and the control-flow view already exposes them.
    """

    def leave_SimpleString(self, original_node: cst.SimpleString, updated_node: cst.SimpleString) -> cst.BaseExpression:
        return cst.SimpleString(value=_REDACTED_LITERAL)

    def leave_FormattedString(
        self, original_node: cst.FormattedString, updated_node: cst.FormattedString
    ) -> cst.BaseExpression:
        return cst.SimpleString(value=_REDACTED_LITERAL)


def _transform_label(node: cst.CSTNode, fallback: str) -> str:
    """Render a redacted, length-capped one-line label for an assignment."""
    try:
        redacted = node.visit(_LiteralRedactor())
        if not isinstance(redacted, cst.CSTNode):
            return fallback
        code = " ".join(cst.Module([]).code_for_node(redacted).split())
    except Exception:
        return fallback
    if not code:
        return fallback
    if len(code) > _MAX_TRANSFORM_NAME:
        code = code[: _MAX_TRANSFORM_NAME - 1] + "…"
    return code


def _expand_unknown_nodes(
    nodes: list[dict[str, Any]],
    assignments: list[dict[str, Any]],
    workflow_name: str,
) -> tuple[list[dict[str, Any]], set[str]]:
    """Replace unknown nodes with transform nodes for each assignment inside.

    Returns the transforms and the ids of the unknowns they replace. An ellipsis
    holding no assignment — a bare `self._update_step(...)` or `logger.info(...)`
    — explodes into nothing, so it is not replaced and keeps its own node. It is
    still a step the workflow runs, and dropping it would leave the data-flow
    view with fewer rows than the control-flow view it is meant to re-describe.
    """
    unknown_nodes = [n for n in nodes if n["type"] == "unknown"]
    unknown_ids: set[str] = set()
    transforms: list[dict[str, Any]] = []
    seen_tids: dict[str, int] = {}

    for unode in unknown_nodes:
        sr = unode.get("source_range", {})
        begin, end = sr.get("begin", 0), sr.get("end", 0)

        for ainfo in assignments:
            a_off = ainfo["byte_offset"]
            a_end = a_off + ainfo["byte_length"]
            if begin <= a_off < end and ainfo["line"] > 0:
                base = f"{workflow_name}::transform_{ainfo['line']}"
                count = seen_tids.get(base, 0)
                seen_tids[base] = count + 1
                tid = base if count == 0 else f"{base}_{count}"
                unknown_ids.add(unode["id"])
                transforms.append(
                    {
                        "id": tid,
                        "type": "transform",
                        "name": _transform_label(ainfo["cst_node"], ainfo["target"]),
                        "target_var": ainfo["target"],
                        "line": ainfo["line"],
                        "source_range": {"begin": a_off, "end": a_end},
                    }
                )

    return transforms, unknown_ids


# ---------------------------------------------------------------------------
# Step 3: Data-dep edges
# ---------------------------------------------------------------------------


def _credit_nested_helper(
    node: dict[str, Any] | None,
    offset: int,
    nested_fn_callers: list[tuple[int, int, list[dict[str, Any]]]],
) -> list[dict[str, Any]]:
    """Re-credit a position inside a nested helper to its calling nodes.

    No emitted node covers a helper body, so an offset in one resolves to
    whichever container encloses the ``def`` — usually the entrypoint, which
    spans the whole workflow. A node that genuinely sits inside the helper keeps
    the credit; anything wider escaped, and belongs to every caller.
    """
    for fn_begin, fn_end, callers in nested_fn_callers:
        if not callers or not (fn_begin <= offset < fn_end):
            continue
        span = _node_span(node) if node is not None else None
        if node is not None and span is not None and fn_begin <= span[0] and span[1] <= fn_end:
            return [node]
        return callers
    return [node] if node is not None else []


def _compute_data_edges(
    wrapper: meta.MetadataWrapper,
    positions: Mapping[cst.CSTNode, Any],
    line_starts: list[int],
    node_index: list[tuple[int, int, dict[str, Any]]],
    all_nodes: list[dict[str, Any]],
    entrypoint_info: dict[str, Any] | None,
    workflow_name: str,
) -> list[dict[str, Any]]:
    scopes = wrapper.resolve(meta.ScopeProvider)

    seen_scopes: set[int] = set()
    unique_scopes: list[meta.Scope] = []
    for scope_val in scopes.values():
        if isinstance(scope_val, meta.Scope) and id(scope_val) not in seen_scopes:
            seen_scopes.add(id(scope_val))
            unique_scopes.append(scope_val)

    ep_id = f"{workflow_name}::entrypoint"
    out_id = f"{workflow_name}::output"
    node_by_id = {n["id"]: n for n in all_nodes}

    # Spans of every `return <value>`. The emitter gives the output terminus a
    # zero-width range at the end of the body, so `_build_node_index` drops it
    # and no read ever resolves to it — see the entrypoint check below.
    return_spans: list[tuple[int, int]] = []
    if out_id in node_by_id:
        returns = _ReturnCollector()
        wrapper.visit(returns)
        for ret in returns.returns:
            ret_pos = positions.get(ret)
            if isinstance(ret_pos, meta.CodeRange):
                return_spans.append(
                    (
                        _line_col_to_byte_offset(line_starts, ret_pos.start.line, ret_pos.start.column),
                        _line_col_to_byte_offset(line_starts, ret_pos.end.line, ret_pos.end.column),
                    )
                )

    # Map nested function body ranges to the emitted nodes that call them.
    # A read of an outer variable inside a nested helper (e.g. `semaphore`
    # inside `_check`) should resolve to the node that *invokes* the helper,
    # not be dropped because no emitted node covers the helper body.
    nested_fn_callers: list[tuple[int, int, list[dict[str, Any]]]] = []
    for scope in unique_scopes:
        for assignment in scope.assignments:
            if not isinstance(assignment, meta.Assignment):
                continue
            if not isinstance(assignment.node, cst.FunctionDef):
                continue
            pos = positions.get(assignment.node)
            if not isinstance(pos, meta.CodeRange):
                continue
            fn_begin = _line_col_to_byte_offset(line_starts, pos.start.line, pos.start.column)
            fn_end = _line_col_to_byte_offset(line_starts, pos.end.line, pos.end.column)
            callers: dict[str, dict[str, Any]] = {}
            for ref in assignment.references:
                ref_off = _cst_to_byte_offset(positions, ref.node, line_starts)
                if ref_off is None:
                    continue
                caller_node = _find_node_at_offset(node_index, ref_off)
                if caller_node is not None:
                    callers[caller_node["id"]] = caller_node
            nested_fn_callers.append((fn_begin, fn_end, list(callers.values())))

    edges: list[dict[str, Any]] = []
    seen_edges: set[tuple[str, str, str]] = set()

    for scope in unique_scopes:
        for assignment in scope.assignments:
            if not isinstance(assignment, meta.Assignment):
                continue

            var_name = assignment.name
            def_cst = assignment.node

            # A nested `def`/`class`/import binds a name but carries no workflow
            # value; crediting the enclosing node with producing it invents a
            # data edge (and, with two such bindings, a phantom fan-out group).
            if isinstance(def_cst, _NON_VALUE_BINDINGS):
                continue

            def_offset = _cst_to_byte_offset(positions, def_cst, line_starts)
            if def_offset is None:
                continue

            def_graphs = _credit_nested_helper(
                _find_node_at_offset(node_index, def_offset),
                def_offset,
                nested_fn_callers,
            )
            if not def_graphs and entrypoint_info:
                ep_begin = entrypoint_info.get("begin", 0)
                ep_end = entrypoint_info.get("end", 0)
                if ep_begin <= def_offset < ep_end:
                    def_graphs = [node_by_id[ep_id]]
            if not def_graphs:
                continue

            # Assignment target before the activity range lands on a container;
            # check if a leaf node on the same line should get credit
            for i, def_graph in enumerate(def_graphs):
                if def_graph.get("type") in (
                    "entrypoint",
                    "loop",
                    "try_except",
                    "conditional",
                    "parallel",
                ):
                    def_line = _offset_to_line(line_starts, def_offset)
                    same_line = _find_node_on_line(node_index, def_line)
                    if same_line is not None:
                        def_graphs[i] = same_line

            for access in assignment.references:
                use_offset = _cst_to_byte_offset(positions, access.node, line_starts)
                if use_offset is None:
                    continue

                use_graphs = _credit_nested_helper(
                    _find_node_at_offset(node_index, use_offset),
                    use_offset,
                    nested_fn_callers,
                )

                for use_graph in use_graphs:
                    # The entrypoint's range spans the whole body, so it absorbs
                    # every read no tighter node covers — a `return`, an `async
                    # with` header, an f-string in a context manager argument.
                    # Nothing runs before the entrypoint, so an edge into it is
                    # temporally backwards no matter which read produced it.
                    #
                    # A read inside a `return` is the one exception: that value
                    # genuinely leaves the workflow, and the output terminus is
                    # the node that says so. Credit it there instead of dropping
                    # it — this is what gives a lineage split a join to fan in
                    # to. A return nested in a conditional or a loop resolves to
                    # that container, not the entrypoint, so it never reaches
                    # here.
                    if use_graph["id"] == ep_id:
                        if not any(begin <= use_offset < end for begin, end in return_spans):
                            continue
                        use_graph = node_by_id[out_id]

                    for def_graph in def_graphs:
                        from_id = def_graph["id"]
                        to_id = use_graph["id"]
                        if from_id == to_id:
                            continue

                        key = (from_id, to_id, var_name)
                        if key in seen_edges:
                            continue
                        seen_edges.add(key)

                        edges.append(
                            {
                                "id": f"e-data-{from_id}-{to_id}-{var_name}",
                                "from": from_id,
                                "to": to_id,
                                "kind": "data_dep",
                                "label": var_name,
                            }
                        )

    # libcst hands back a scope's assignments, and an assignment's references,
    # as sets, so the order edges are appended in follows the hash seed and
    # changes between processes. Every later pass groups off this list — which
    # node seeds a fan-out, the order of a group's branches — so the whole view
    # would shift with it. `seen_edges` makes the key unique, so this is a total
    # order.
    edges.sort(key=lambda e: (e["from"], e["to"], e.get("label") or ""))

    return edges


def _lift_edges_onto_tracks(
    edges: list[dict[str, Any]],
    nodes: list[dict[str, Any]],
    groups: list[dict[str, Any]],
    boundaries: dict[str, tuple[str | None, str | None]],
) -> None:
    """Reduce every edge crossing a box wall to the fan-out and the fan-in.

    Both ends move: a node anywhere inside a track — including deep in a loop
    body — resolves to the box, and the outside end snaps to the row adjacent to
    it. That is what makes the two edges one step each, which is the whole point
    of boxing the split. Edges with both ends inside the same box vanish; the
    box already says they belong together.
    """
    container_of = _build_container_of(nodes)
    terminus = {n["id"] for n in nodes if n["type"] == "output"}
    members = {c: g["id"] for g in groups for c in g.get("children") or []}
    _track_of = {c: (g["id"], i) for g in groups for i, branch in enumerate(g.get("branches") or []) for c in branch}

    def box_of(nid: str) -> str | None:
        cur, seen = nid, set()
        while cur not in members and cur in container_of and cur not in seen:
            seen.add(cur)
            cur = container_of[cur]
        return members.get(cur)

    resolved: dict[str, str | None] = {}
    for edge in edges:
        for end in ("from", "to"):
            if edge[end] not in resolved:
                resolved[edge[end]] = box_of(edge[end])
        src_box, tgt_box = resolved[edge["from"]], resolved[edge["to"]]
        if edge["kind"] != "data_dep":
            # Control flow enters the box at the top and leaves at the bottom,
            # and the box's own spine edges say so. A branch edge reaching from
            # inside past the wall draws a second connector competing with them,
            # and the renderer picks that one — so the flow appears to leave from
            # whichever conditional happens to sit at the end of a track.
            if src_box != tgt_box and edge["kind"] in _CF_BRANCH_KINDS:
                edge["kind"] = "_drop"
            continue
        if src_box == tgt_box and src_box is not None:
            # Inside one box. Between two tracks the box already says it; along
            # a track it is an ordinary hop, and the step rule below decides.
            if _track_of.get(edge["from"]) != _track_of.get(edge["to"]):
                edge["kind"] = "_drop"
            continue
        src, tgt = edge["from"], edge["to"]
        label = edge.get("label") or ""
        if tgt_box is not None:
            before, _ = boundaries[tgt_box]
            # Which track member actually reads the value. The box edge is the
            # honest one-step statement while the box is shut, but with it open
            # the reader can see the tracks and wants the line to reach the one
            # that consumes it. Keep the member so the renderer can fan.
            edge["lifted_to"] = {tgt: [label]} if label else {tgt: []}
            tgt = tgt_box
            if before is not None and src != before:
                src = before
        elif src_box is not None:
            _, after = boundaries[src_box]
            edge["lifted_from"] = {src: [label]} if label else {src: []}
            src = src_box
            # Snapping the far end to the row after the box says the box's
            # result continues there. A value read only by the final `return`
            # bypasses that row, so moving the edge onto it would claim a
            # consumer that never reads the value; leave it bound for the
            # terminus and let the distance rule decide.
            if after is not None and tgt != after and tgt not in terminus:
                tgt = after
        if (src, tgt) == (edge["from"], edge["to"]):
            continue
        edge["from"], edge["to"] = src, tgt
        edge["id"] = f"e-data-{src}-{tgt}-{edge.get('label', '')}"

    edges[:] = [e for e in edges if e["kind"] != "_drop"]


# ---------------------------------------------------------------------------
# Containment-aware reachability
# ---------------------------------------------------------------------------


def _build_container_of(nodes: list[dict[str, Any]]) -> dict[str, str]:
    """Map each node to the container that encloses it.

    Declared ``children``/``branches`` first, then source-range nesting for
    whatever they miss. Neither alone is enough, and neither subsumes the other:
    a gather's range covers only the call expression, so its tasks sit outside
    it and can only come from ``children``; a conditional links just the first
    statement of each branch and ``_build`` drops its ``branchTrue`` fields, so
    the rest of a branch body can only come from the ranges.
    """
    container_of: dict[str, str] = {}
    for n in nodes:
        for c in n.get("children") or []:
            container_of[c] = n["id"]
        for branch in n.get("branches") or []:
            for c in branch:
                container_of[c] = n["id"]

    boxes: list[tuple[int, int, str]] = []
    for n in nodes:
        span = _node_span(n)
        if span is not None and n.get("type") in _STRUCTURAL_TYPES:
            boxes.append((span[0], span[1], n["id"]))
    boxes.sort(key=lambda b: b[1] - b[0])

    for n in nodes:
        span = _node_span(n)
        if span is None or n["id"] in container_of:
            continue
        begin, end = span
        for bb, be, bid in boxes:
            if bid != n["id"] and bb <= begin and end <= be and (be - bb) > (end - begin):
                container_of[n["id"]] = bid
                break
    return container_of


# ---------------------------------------------------------------------------
# Step 4: Process group detection (fan-out)
# ---------------------------------------------------------------------------


def _top_level_of(
    spine_ids: set[str],
    container_of: dict[str, str],
) -> dict[str, str]:
    """Map every node to the top-level spine node that positions it."""
    top: dict[str, str] = {}
    for nid in list(container_of) + list(spine_ids):
        cur, seen = nid, set()
        while cur not in spine_ids and cur in container_of and cur not in seen:
            seen.add(cur)
            cur = container_of[cur]
        if cur in spine_ids:
            top[nid] = cur
    return top


def _detect_lineage_tracks(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    spine: list[dict[str, Any]],
    workflow_name: str,
) -> tuple[list[dict[str, Any]], dict[str, tuple[str | None, str | None]]]:
    """Box each lineage split as side-by-side tracks running fork to join.

    A value that derives into separate chains is shape 3 of the vocabulary, and
    the honest way to draw it is the shape itself: the chains sit in tracks, the
    producer fans out into the box, and the box fans in to whatever they
    reconverge on. Nothing else crosses the wall, so no line has to travel the
    length of the diagram to say what the box already says by containing it.

    Vertical order inside the box stays control order — the tracks are a claim
    about derivation, not about running at the same time, and reordering them
    would be the concurrency claim P6 forbids. Only ``parallel``, which the
    walker emits from a real ``gather``, asserts that.
    """
    pos = {n["id"]: i for i, n in enumerate(spine)}
    node_by_id = {n["id"]: n for n in nodes}
    top_of = _top_level_of(set(pos), _build_container_of(nodes))

    # Data adjacency between top-level nodes: an edge into a loop body is an
    # edge into the loop, because the loop is what occupies a row.
    data_next: dict[str, set[str]] = {}
    fan_label: dict[tuple[str, str], set[str]] = {}
    for e in edges:
        if e["kind"] != "data_dep":
            continue
        a, b = top_of.get(e["from"]), top_of.get(e["to"])
        if a is None or b is None or a == b:
            continue
        data_next.setdefault(a, set()).add(b)
        if e.get("label"):
            fan_label.setdefault((a, b), set()).add(e["label"])

    def downstream(start: str) -> set[str]:
        seen: set[str] = set()
        stack = [start]
        while stack:
            cur = stack.pop()
            for nxt in data_next.get(cur, ()):
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return seen

    groups: list[dict[str, Any]] = []
    boundaries: dict[str, tuple[str | None, str | None]] = {}
    claimed: set[str] = set()
    for src in spine:
        src_id = src["id"]
        if src["type"] in _STRUCTURAL_TYPES:
            continue
        # The workflow input reaches everything below it, so its readers do not
        # form tracks — the box would span most of the workflow and claim a
        # split where there is only "everything uses the arguments".
        if src["type"] == "entrypoint":
            continue
        # A guard reads the value to pick a path and a return hands it back;
        # neither derives anything from it, so neither starts a track. Without
        # this a gate on the whole split counts as a third track, and the three
        # never reconverge.
        heads = sorted(
            (
                t
                for t in data_next.get(src_id, ())
                if pos[t] > pos[src_id] and node_by_id.get(t, {}).get("type") not in ("conditional", "output")
            ),
            key=lambda t: pos[t],
        )
        # A head reachable from another head is a continuation of that chain,
        # not a track of its own.
        tracks = [h for h in heads if not any(h in downstream(o) for o in heads if o != h)]
        if len(tracks) < 2 or any(t in claimed for t in tracks):
            continue

        reach = {h: {h} | downstream(h) for h in tracks}
        start = min(pos[h] for h in tracks)
        # Only a split that reconverges can be bounded. Without a join the box
        # would have no bottom and would run to the end of the workflow,
        # swallowing rows that have nothing to do with the split.
        common = [c for c in set.intersection(*reach.values()) - set(tracks) if pos.get(c, -1) > start]
        if not common:
            continue
        join = min(common, key=lambda c: pos[c])
        stop = pos[join]
        members = [n for n in spine[start:stop] if n["id"] not in claimed]
        if len(members) < 2:
            continue

        # Assign each row to a track. A row no track derives is placed with the
        # track that consumes it (a semaphore feeding one branch's gather);
        # failing that, with its nearest neighbour above.
        lane_of: dict[str, int] = {}
        for m in members:
            owning = [i for i, h in enumerate(tracks) if m["id"] in reach[h]]
            if owning:
                lane_of[m["id"]] = owning[0]
        for m in members:
            if m["id"] in lane_of:
                continue
            consumers = [lane_of[c] for c in data_next.get(m["id"], ()) if c in lane_of]
            lane_of[m["id"]] = min(consumers) if consumers else 0
        branches = [[m["id"] for m in members if lane_of[m["id"]] == i] for i in range(len(tracks))]
        branches = [b for b in branches if b]
        if len(branches) < 2:
            continue

        claimed.update(m["id"] for m in members)
        fan_vars = sorted({v for h in tracks for v in fan_label.get((src_id, h), set())})
        spans = [_node_span(node_by_id[m["id"]]) for m in members if m["id"] in node_by_id]
        valid = [s for s in spans if s is not None]
        gid = f"{workflow_name}::group_{src_id.split('::')[-1]}"
        boundaries[gid] = (
            spine[start - 1]["id"] if start > 0 else None,
            join,
        )
        groups.append(
            {
                "id": gid,
                "type": "lineage",
                "name": ", ".join(fan_vars) if fan_vars else "process",
                "line": min(m.get("line", 0) for m in members),
                "source_range": (
                    {"begin": min(b for b, _ in valid), "end": max(e for _, e in valid)}
                    if valid
                    else src.get("source_range", {"begin": 0, "end": 0})
                ),
                "branches": branches,
                "children": [m["id"] for m in members],
            }
        )

    return groups, boundaries


# ---------------------------------------------------------------------------
# Sequential spine — minimal tree structure for the Flow renderer
# ---------------------------------------------------------------------------


def _cf_spine_rank(cf: dict[str, Any], retarget: dict[str, str], wf_id: str) -> dict[str, int]:
    """Execution order of top-level nodes, walked off the control-flow chain."""
    nxt: dict[str, str] = {}
    for e in cf.get("edges") or []:
        if e.get("kind") == "sequential":
            src = retarget.get(e["from"], e["from"])
            nxt[src] = retarget.get(e["to"], e["to"])
    rank: dict[str, int] = {}
    cur: str | None = wf_id
    while cur is not None and cur not in rank:
        rank[cur] = len(rank)
        cur = nxt.get(cur)
    return rank


def _owned_by_containers(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> set[str]:
    """Nodes a container positions, so the top-level spine must skip them."""
    owned: set[str] = set()
    for n in nodes:
        for c in n.get("children") or []:
            owned.add(c)
        for branch in n.get("branches") or []:
            for c in branch:
                owned.add(c)
    owned |= {e["to"] for e in edges if e["kind"] in ("branch_true", "branch_false")}
    return owned


def _spine_order(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    workflow_name: str,
    cf_rank: dict[str, int],
) -> list[dict[str, Any]]:
    """Top-level nodes in the order they will render, container children elided.

    Source line is not execution order: a node inlined from a helper carries the
    helper's definition line, which may sit above the entrypoint. Order by the
    control-flow chain where it knows the node, and keep nodes it does not know
    (transforms split out of an ellipsis) beside the ranked node they follow in
    the file.
    """
    owned = _owned_by_containers(nodes, edges)
    line_sorted = sorted(
        [n for n in nodes if n["id"] != workflow_name and n["id"] not in owned],
        key=lambda n: n.get("line", 0),
    )
    ordered: list[tuple[tuple[int, int, int], dict[str, Any]]] = []
    last_rank = -1
    for i, n in enumerate(line_sorted):
        rank = cf_rank.get(n["id"])
        if rank is None:
            ordered.append(((last_rank, 1, i), n))
            continue
        last_rank = rank
        ordered.append(((rank, 0, i), n))
    return [n for _, n in sorted(ordered, key=lambda t: t[0])]


def _build_sequential_spine(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    workflow_name: str,
    cf_rank: dict[str, int],
) -> list[dict[str, Any]]:
    """Chain top-level nodes with sequential edges so the tree builder can
    render them. Nodes inside containers (children, branch targets) are
    skipped — they're positioned by their parent."""
    branch_targets = {e["to"] for e in edges if e["kind"] in ("branch_true", "branch_false")}

    wf_id = workflow_name
    # Ensure workflow root exists
    has_root = any(n["id"] == wf_id for n in nodes)
    if not has_root:
        nodes.insert(
            0,
            {
                "id": wf_id,
                "type": "workflow",
                "name": workflow_name,
                "line": 0,
                "source_range": {"begin": 0, "end": 0},
            },
        )

    spine = _spine_order(nodes, edges, workflow_name, cf_rank)

    seq_edges: list[dict[str, Any]] = []
    chain = [wf_id] + [n["id"] for n in spine]
    for i in range(len(chain) - 1):
        src, tgt = chain[i], chain[i + 1]
        seq_edges.append(
            {
                "id": f"e-seq-{src}-{tgt}",
                "from": src,
                "to": tgt,
                "kind": "sequential",
            }
        )

    # Chain children inside containers (loops, try_except)
    node_by_id = {n["id"]: n for n in nodes}
    for n in nodes:
        if n["type"] in ("loop", "try_except") and n.get("children"):
            runs = [[c for c in n["children"] if c not in branch_targets]]
        elif n["type"] in _LANE_CONTAINER_TYPES and n.get("branches"):
            # Each track is its own run: a track's members follow one another,
            # and the tracks do not follow each other.
            runs = [[c for c in branch if c not in branch_targets] for branch in n["branches"]]
        else:
            continue
        for run in runs:
            kids = sorted(run, key=lambda c: node_by_id.get(c, {}).get("line", 0))
            for i in range(len(kids) - 1):
                seq_edges.append(
                    {
                        "id": f"e-seq-{kids[i]}-{kids[i + 1]}",
                        "from": kids[i],
                        "to": kids[i + 1],
                        "kind": "sequential",
                    }
                )

    return seq_edges


# ---------------------------------------------------------------------------
# Mutation bridging
# ---------------------------------------------------------------------------


def _bridge_mutation_edges(
    edges: list[dict[str, Any]],
    transforms: list[dict[str, Any]],
    all_nodes: list[dict[str, Any]],
) -> None:
    """For each mutation transform (x.append), copy outgoing edges from x's
    initialization transform so the mutation participates in data flow, then
    credit each consumer to the writer nearest before it.

    Soundness, not display: an edge attributed to the wrong writer of a mutated
    name is temporally backwards, so this belongs in :func:`analyze`.
    """
    by_var: dict[str, list[dict[str, Any]]] = {}
    for t in transforms:
        var = t.get("target_var", t["name"])
        by_var.setdefault(var, []).append(t)

    outgoing: dict[str, list[dict[str, Any]]] = {}
    for e in edges:
        outgoing.setdefault(e["from"], []).append(e)

    seen = {(e["from"], e["to"], e.get("label", "")) for e in edges}
    new_edges: list[dict[str, Any]] = []

    for var, group in by_var.items():
        if len(group) < 2:
            continue
        init = group[0]
        for mutation in group[1:]:
            mid = mutation["id"]
            for e in outgoing.get(init["id"], []):
                # Only bridge consumers of the mutated variable itself. The
                # init transform may carry re-pointed edges for other vars
                # (e.g. all_pkgs threaded through a preamble init); copying
                # those onto the mutation would draw spurious data_deps.
                if e.get("label") != var:
                    continue
                key = (mid, e["to"], e.get("label", ""))
                if key not in seen and e["to"] != mid:
                    seen.add(key)
                    new_edges.append(
                        {
                            "id": f"e-data-{mid}-{e['to']}-{e.get('label', '')}",
                            "from": mid,
                            "to": e["to"],
                            "kind": "data_dep",
                            "label": e.get("label"),
                        }
                    )

    edges.extend(new_edges)

    # Nearest-preceding-writer: each consumer of a mutation-chain variable
    # should be fed by the writer whose source position is closest before it,
    # not the textually-last writer.
    node_begin: dict[str, int] = {}
    for n in all_nodes:
        sr = n.get("source_range") or {}
        if "begin" in sr:
            node_begin[n["id"]] = sr["begin"]

    for var, group in by_var.items():
        if len(group) < 2:
            continue
        writers = sorted(group, key=lambda t: (t.get("source_range") or {}).get("begin", 0))
        writer_ids = {t["id"] for t in writers}
        writer_begins = [(t["id"], (t.get("source_range") or {}).get("begin", 0)) for t in writers]

        # Collect all consumers reached by any writer of this var.
        consumers: set[str] = set()
        for e in edges:
            if e["kind"] == "data_dep" and e.get("label") == var and e["from"] in writer_ids:
                consumers.add(e["to"])

        # For each consumer, find the nearest preceding writer.
        keep: set[tuple[str, str]] = set()  # (writer_id, consumer_id)
        for cid in consumers:
            c_begin = node_begin.get(cid, 0)
            # Nearest preceding = largest writer begin that is ≤ consumer begin
            # A writer is never its own source: `x.append(v)` reads x before it
            # writes it, so its feeder is the write before, not itself.
            best: str | None = None
            for wid, wb in writer_begins:
                if wb <= c_begin and wid != cid:
                    best = wid
            # No preceding writer → loop-carried: keep the last writer
            if best is None:
                best = writer_begins[-1][0]
            keep.add((best, cid))

        edges[:] = [
            e
            for e in edges
            if not (
                e["kind"] == "data_dep"
                and e.get("label") == var
                and e["from"] in writer_ids
                and (e["from"], e["to"]) not in keep
            )
        ]


# ---------------------------------------------------------------------------
# View assembly
# ---------------------------------------------------------------------------


def _assemble_view(
    cf: dict[str, Any],
    view_label: str,
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    summaries: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result = {**cf}
    result["view"] = view_label
    result["nodes"] = [{k: v for k, v in n.items() if k != "target_var"} for n in nodes]
    # Deduplicate data_dep edges per (from, to), merging labels
    seen: dict[tuple[str, str], dict[str, Any]] = {}
    deduped: list[dict[str, Any]] = []
    for e in edges:
        if e["kind"] != "data_dep":
            deduped.append(e)
            continue
        key = (e["from"], e["to"])
        if key in seen:
            existing = seen[key]
            old_label = existing.get("label", "")
            new_label = e.get("label", "")
            if new_label and new_label not in (old_label or "").split(", "):
                existing["label"] = f"{old_label}, {new_label}" if old_label else new_label
            for field in ("lifted_from", "lifted_to"):
                for member, labels in (e.get(field) or {}).items():
                    into = existing.setdefault(field, {}).setdefault(member, [])
                    into.extend(v for v in labels if v not in into)
        else:
            copy_e = {**e}
            for field in ("lifted_from", "lifted_to"):
                if field in copy_e:
                    copy_e[field] = {m: list(v) for m, v in copy_e[field].items()}
            seen[key] = copy_e
            deduped.append(copy_e)
    result["edges"] = deduped
    result.pop("node_summaries", None)
    if summaries:
        result["node_summaries"] = summaries
    return result


# ---------------------------------------------------------------------------
# Analysis boundary — the sound intermediate, exposed and assertable
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DependencyGraph:
    """The sound part of data-flow analysis: nodes and raw data edges before any
    display policy is applied.

    Exposed so tests can assert on the analysis directly. ``_build`` deep-copies
    the mutable fields before mutating them, so a ``DependencyGraph`` a test (or
    a caller) holds stays pristine regardless of which suppression passes run
    on top of it. That boundary is what makes display changes unable to corrupt
    the analysis — the failure mode that produced the five-exemption pile.
    """

    # CF nodes deep-copied from the input payload (read-only downstream).
    nodes: list[dict[str, Any]]
    # CF nodes with ellipses replaced by transform nodes (mutated by `_build`;
    # the field holds the pristine copy, `_build` works on a deep copy).
    df_nodes: list[dict[str, Any]]
    # Raw data-dep edges from `_compute_data_edges`, pre-suppression. The edge
    # dicts are never mutated in place by `_build` — policy works on copies.
    data_edges: list[dict[str, Any]]
    # Transform nodes split out of ellipses (read-only downstream).
    transforms: list[dict[str, Any]]


def analyze(cf: dict[str, Any]) -> DependencyGraph:
    """Run the sound analysis and return the raw graph.

    Parse the source, explode ellipses into transforms, and compute the raw
    data-dep edges. Nothing here is display policy: no suppression, no fan-out
    groups, no guard routing. Policy is applied in `_build` on a copy.
    """
    sources: dict[str, str] = cf.get("sources") or {}
    primary_file: str | None = cf.get("primary_file")
    nodes: list[dict[str, Any]] = copy.deepcopy(cf.get("nodes", []))
    entrypoint_info = cf.get("entrypoint")
    workflow_name: str = cf.get("workflow_name", "")

    source_text = _pick_source(sources, primary_file)
    if source_text is None:
        raise ValueError("No source text available for data-flow analysis")
    source_bytes = source_text.encode("utf-8")
    if len(source_bytes) > _MAX_SOURCE_BYTES:
        raise ValueError(f"Source too large for data-flow analysis ({len(source_text)} chars)")

    line_starts = _build_line_starts(source_bytes)
    wrapper = meta.MetadataWrapper(cst.parse_module(source_text))
    positions = wrapper.resolve(meta.PositionProvider)

    collector = _AssignmentCollector()
    wrapper.visit(collector)
    for info in collector.assignments:
        code_range = positions.get(info["cst_node"])
        if code_range and isinstance(code_range, meta.CodeRange):
            info["line"] = code_range.start.line
            info["byte_offset"] = _line_col_to_byte_offset(
                line_starts,
                code_range.start.line,
                code_range.start.column,
            )
            end_offset = _line_col_to_byte_offset(
                line_starts,
                code_range.end.line,
                code_range.end.column,
            )
            info["byte_length"] = end_offset - info["byte_offset"]

    transforms, unknown_ids = _expand_unknown_nodes(nodes, collector.assignments, workflow_name)
    df_nodes = [n for n in nodes if n["id"] not in unknown_ids] + transforms
    node_index = _build_node_index(df_nodes)

    data_edges = _compute_data_edges(
        wrapper,
        positions,
        line_starts,
        node_index,
        df_nodes,
        entrypoint_info,
        workflow_name,
    )
    _bridge_mutation_edges(data_edges, transforms, df_nodes)

    return DependencyGraph(
        nodes=nodes,
        df_nodes=df_nodes,
        data_edges=data_edges,
        transforms=transforms,
    )


# ---------------------------------------------------------------------------
# Display policy — the one rule
# ---------------------------------------------------------------------------


def rendered_order(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    workflow_name: str,
) -> dict[str, int]:
    """Row number of every node once containers are drawn inline.

    The order a reader's eye travels, which is what the rule is stated in terms
    of — not the analysis order, and not the control-flow chain.
    """
    nxt: dict[str, str] = {}
    for e in edges:
        if e["kind"] == "sequential":
            nxt.setdefault(e["from"], e["to"])
    by_id = {n["id"]: n for n in nodes}
    kids = _declared_children(nodes, edges)

    order: dict[str, int] = {}

    def place(nid: str) -> None:
        if nid in order or nid not in by_id:
            return
        order[nid] = len(order)
        for c in kids.get(nid, []):
            place(c)

    cur: str | None = workflow_name
    while cur is not None and cur not in order:
        place(cur)
        cur = nxt.get(cur)
    for n in nodes:
        place(n["id"])
    return order


def _declared_children(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, list[str]]:
    kids: dict[str, list[str]] = {}
    for n in nodes:
        inner = list(n.get("children") or []) + [c for b in n.get("branches") or [] for c in b]
        if inner:
            kids[n["id"]] = inner
    for e in edges:
        if e["kind"] in ("branch_true", "branch_false"):
            kids.setdefault(e["from"], []).append(e["to"])
    return kids


def _contained_nodes(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, set[str]]:
    """Transitive contents of every container."""
    kids = _declared_children(nodes, edges)
    out: dict[str, set[str]] = {}
    for n in nodes:
        seen: set[str] = set()
        stack = list(kids.get(n["id"], []))
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            stack.extend(kids.get(cur, []))
        out[n["id"]] = seen
    return out


def nodes_skipped(
    edge: dict[str, Any],
    order: dict[str, int],
    inside: dict[str, set[str]],
) -> int:
    """How many nodes an edge is drawn past.

    The one rule: this must be zero. A data edge earns its place as a fan-out
    into a box or a fan-in out of one — a single step the reader can follow.
    Anything drawn past a node is a dependency the structure failed to express,
    and routing it around what sits between reads as connecting the wrong
    things (P3), so the answer is to fix the structure, not the line.

    A node the endpoints themselves contain does not count: a box sits directly
    above whatever follows it however many rows its tracks occupy.
    """
    a, b = order.get(edge["from"]), order.get(edge["to"])
    if a is None or b is None:
        return 0
    lo, hi = min(a, b), max(a, b)
    own = inside.get(edge["from"], set()) | inside.get(edge["to"], set()) | {edge["from"], edge["to"]}
    return sum(1 for nid, i in order.items() if lo < i < hi and nid not in own)


# ---------------------------------------------------------------------------
# Main build pipeline
# ---------------------------------------------------------------------------


def _build(cf: dict[str, Any]) -> dict[str, Any]:
    graph = analyze(cf)

    # Build the fully-exploded view once. If any `data_dep` edge (bar `self`)
    # survives every suppression pass, the view has data flow to show and the
    # restructure earns its place. Otherwise the explosion reshapes the graph
    # for nothing — keep every ellipsis so the data-flow view tracks control
    # flow node-for-node. `self`-into-the-first-assignment is universal method
    # noise, true of every method, so it never counts as data flow.
    probe = _build_view(graph, cf, graph.df_nodes)
    has_data_flow = any(e["kind"] == "data_dep" and e.get("label") != "self" for e in probe.get("edges") or [])
    if has_data_flow:
        return probe

    df_nodes = [copy.deepcopy(n) for n in graph.df_nodes if n["type"] != "transform"]
    # An ellipsis that explodes into nothing is already in `df_nodes`; only the
    # ones a transform replaced need putting back.
    kept = {n["id"] for n in df_nodes}
    df_nodes.extend(copy.deepcopy(n) for n in graph.nodes if n["type"] == "unknown" and n["id"] not in kept)
    return _build_view(graph, cf, df_nodes)


def _build_view(
    graph: DependencyGraph,
    cf: dict[str, Any],
    df_nodes_in: list[dict[str, Any]],
) -> dict[str, Any]:
    workflow_name: str = cf.get("workflow_name", "")

    # Policy mutates node and edge dicts; work on deep copies so the raw
    # `DependencyGraph` a caller or test holds is not corrupted.
    nodes = graph.nodes
    df_nodes = copy.deepcopy(df_nodes_in)
    data_edges = graph.data_edges

    # ``analyze`` already replaced exploded ellipses and preserved every other
    # control-flow node. Its node list is authoritative: filtering it here
    # makes each new executable type require a second registration.
    full_nodes = df_nodes
    full_ids = {n["id"] for n in full_nodes}
    cond_ids = {n["id"] for n in full_nodes if n["type"] == "conditional"}

    # Retarget: map removed CF nodes to replacement transforms by source range
    sr_to_transform: dict[tuple[int, int], str] = {}
    for n in full_nodes:
        if n["type"] == "transform":
            sr = n.get("source_range", {})
            sr_to_transform[(sr.get("begin", 0), sr.get("end", 0))] = n["id"]
    retarget: dict[str, str] = {}
    for n in nodes:
        if n["id"] not in full_ids:
            sr = n.get("source_range", {})
            key = (sr.get("begin", 0), sr.get("end", 0))
            if key in sr_to_transform:
                retarget[n["id"]] = sr_to_transform[key]

    # An ellipsis spanning several statements explodes into several transforms,
    # so none matches its range exactly and `retarget` has no entry for it.
    # Fall back to every transform inside its range, otherwise the container
    # drops the child and those transforms escape to the top level.
    transform_ranges = sorted(
        (
            (n.get("source_range") or {}).get("begin", 0),
            (n.get("source_range") or {}).get("end", 0),
            n["id"],
        )
        for n in full_nodes
        if n["type"] == "transform"
    )
    removed_ranges = {
        n["id"]: (
            (n.get("source_range") or {}).get("begin"),
            (n.get("source_range") or {}).get("end"),
        )
        for n in nodes
        if n["id"] not in full_ids
    }

    def _replacements(child_id: str) -> list[str]:
        if child_id in full_ids:
            return [child_id]
        if child_id in retarget:
            return [retarget[child_id]]
        begin, end = removed_ranges.get(child_id, (None, None))
        if begin is None or end is None:
            return []
        return [t for tb, te, t in transform_ranges if tb >= begin and te <= end]

    def _remap(ids: list[str]) -> list[str]:
        out: list[str] = []
        for c in ids:
            for r in _replacements(c):
                if r not in out:
                    out.append(r)
        return out

    # Strip removed nodes from children/branches. For conditionals, drop the
    # branch pointers: branches are spine siblings (rendered as a scope box via
    # branchDescendants), not embedded children. The fields are deleted rather
    # than nulled so the frontend can rebuild them from the carried-over
    # branch_true/branch_false edges (a `null` value blocks that rebuild).
    for n in full_nodes:
        if n.get("children"):
            n["children"] = _remap(n["children"])
        if n["type"] == "conditional":
            n.pop("branchTrue", None)
            n.pop("branchFalse", None)
        for field in ("branchTrue", "branchFalse", "branchDescendants"):
            if n.get(field):
                n[field] = _remap(n[field])

    # Keep data_dep edges to conditionals: a guard's condition variable needs
    # an incoming edge so the data-flow view shows what feeds the guard.
    # Deep-copy the edge dicts: the policy passes below re-point `from`/`to` in
    # place, and without the copy that would corrupt `DependencyGraph.data_edges`.
    full_edges = [copy.deepcopy(e) for e in data_edges if e["from"] in full_ids and e["to"] in full_ids]

    # Carry over branch/merge edges from CF for conditionals
    cf_edges = cf.get("edges") or []
    for e in cf_edges:
        if e.get("kind") not in _CF_BRANCH_KINDS:
            continue
        src = retarget.get(e["from"], e["from"])
        tgt = retarget.get(e["to"], e["to"])
        if src in cond_ids or e["kind"] == "branch_merge":
            if src in full_ids and tgt in full_ids:
                full_edges.append({**e, "from": src, "to": tgt})

    # Suppress data_dep edges where the target is inside a container.
    # Build the set of all descendants for each container (iterative BFS
    # with visited set to handle cycles in malformed input).
    node_by_id = {n["id"]: n for n in full_nodes}
    branch_targets_by_node: dict[str, list[str]] = {}
    for e in full_edges:
        if e["kind"] in ("branch_true", "branch_false"):
            branch_targets_by_node.setdefault(e["from"], []).append(e["to"])

    def _collect_descendants(nid: str) -> set[str]:
        result: set[str] = set()
        stack = [nid]
        while stack:
            cur = stack.pop()
            node = node_by_id.get(cur)
            if not node:
                continue
            # A gather declares its lanes in `branches`, not `children`, so
            # reading only `children` leaves its own tasks outside it.
            for c in (node.get("children") or []) + [c for b in node.get("branches") or [] for c in b]:
                if c not in result:
                    result.add(c)
                    stack.append(c)
            if node.get("type") == "conditional":
                for t in branch_targets_by_node.get(cur, []):
                    if t not in result:
                        result.add(t)
                        stack.append(t)
        return result

    container_descendants: dict[str, set[str]] = {}
    for n in full_nodes:
        if n.get("children") or n.get("branches"):
            container_descendants[n["id"]] = _collect_descendants(n["id"])

    # Flatten all descendants for a quick "is inside any container" check
    all_contained: set[str] = set()
    for desc in container_descendants.values():
        all_contained |= desc

    # A conditional's guard reads its condition variables before the branch
    # body runs (e.g. cond_2 tests `pypi_missing or npm_unscoped`, then
    # post_alert@79 receives them as call args). When a producer feeds both
    # the guard and a DIRECT branch body with the same var, the data edge
    # that matters is the one into the guard — the direct body inherits the
    # value along the control-flow branch. Drop the direct-body edge, keep
    # the guard's. Constructs NESTED inside the branch (a loop, a try/except)
    # read the var directly from the producer, not via the guard, so their
    # edges stay — only direct branch_true/branch_false targets are dropped.
    by_prod_var: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for e in full_edges:
        if e["kind"] == "data_dep":
            by_prod_var.setdefault((e["from"], e.get("label", "")), []).append(e)
    redundant_branch_body: set[tuple[str, str, str]] = set()
    for (prod, var), outs in by_prod_var.items():
        consumers = {e["to"] for e in outs}
        for e in outs:
            if e["to"] not in cond_ids:
                continue
            for d in branch_targets_by_node.get(e["to"], []):
                if d in consumers:
                    redundant_branch_body.add((prod, d, var))
    full_edges = [
        e
        for e in full_edges
        if not (e["kind"] == "data_dep" and (e["from"], e["to"], e.get("label", "")) in redundant_branch_body)
    ]

    # Structural constraint, not an exemption to the display rule: no line may
    # cross a box wall, because a line that does reads as connecting the box
    # rather than the node inside it. Being inside *some* container is not
    # enough — an edge from one loop's body into another loop's body crosses
    # just as much as one from the top level. A container feeding its own child
    # counts too; the loop header already shows the loop variable.
    def _pierces_container(src: str, tgt: str) -> bool:
        return any(tgt in desc and src not in desc for desc in container_descendants.values())

    full_edges = [e for e in full_edges if not (e["kind"] == "data_dep" and _pierces_container(e["from"], e["to"]))]

    # Adopt transforms into containers when all their data consumers are inside
    # that container. Moving a transform off the spine keeps a lineage box's
    # edge-lifting honest: the row above the box becomes the guard that tests
    # the value, not the accumulator init. So adoption only helps containers
    # that sit inside a lineage split — detect the tracks first (on the
    # non-adopted graph) and restrict adoption to their members. A standalone
    # loop keeps its preamble at the top level (the init runs once before the
    # loop, not each iteration); adopting it would draw it inside the box and
    # misrepresent the control flow.
    cf_rank = _cf_spine_rank(cf, retarget, workflow_name)
    _pre_tracks, _ = _detect_lineage_tracks(
        full_nodes,
        full_edges,
        _spine_order(full_nodes, full_edges, workflow_name, cf_rank),
        workflow_name,
    )
    lineage_containers = {c for g in _pre_tracks for c in g.get("children") or []}

    node_by_id = {n["id"]: n for n in full_nodes}
    for t in [n for n in full_nodes if n["type"] == "transform"]:
        consumers = {
            e["to"] for e in data_edges if e["kind"] == "data_dep" and e["from"] == t["id"] and e["to"] in full_ids
        }
        if not consumers:
            continue
        for cid, desc in container_descendants.items():
            if cid not in lineage_containers:
                continue
            if consumers <= desc:
                container = node_by_id.get(cid)
                if container and t["id"] not in (container.get("children") or []):
                    container.setdefault("children", []).insert(0, t["id"])
                break

    tracks, boundaries = _detect_lineage_tracks(
        full_nodes,
        full_edges,
        _spine_order(full_nodes, full_edges, workflow_name, cf_rank),
        workflow_name,
    )
    full_nodes = full_nodes + tracks
    full_ids = {n["id"] for n in full_nodes}

    # Everything the box spans is now inside it, so the only data edges left
    # crossing its wall are the fan-out that feeds the tracks and the fan-in to
    # whatever they reconverge on. Land both on the box: that is what makes them
    # one step, and the box says the rest by containing it.
    _lift_edges_onto_tracks(full_edges, full_nodes, tracks, boundaries)

    full_nodes = [{**n, "name": "input"} if n["type"] == "entrypoint" else n for n in full_nodes]

    # Build sequential spine for the tree renderer
    full_edges.extend(
        _build_sequential_spine(
            full_nodes,
            full_edges,
            workflow_name,
            _cf_spine_rank(cf, retarget, workflow_name),
        )
    )

    # The rule, in full: a data edge may only join consecutive rows. Boxing a
    # split turns its long-range dependencies into a fan-out and a fan-in, both
    # one step, and anything still jumping rows is a dependency the structure
    # failed to express — drawing it would only route a line around everything
    # in between and read as connecting the wrong things (P3).
    order = rendered_order(full_nodes, full_edges, workflow_name)
    inside = _contained_nodes(full_nodes, full_edges)
    full_edges = [e for e in full_edges if e["kind"] != "data_dep" or nodes_skipped(e, order, inside) == 0]

    # Carry LLM summaries from the control-flow view, re-keying any
    # unknown/ellipsis node ids to the transform ids that replaced them
    # (retarget maps by matching source range).
    df_summaries: dict[str, Any] = {}
    for old_id, summary in (cf.get("node_summaries") or {}).items():
        new_id = retarget.get(old_id, old_id)
        if new_id in full_ids:
            df_summaries[new_id] = summary

    return _assemble_view(cf, DATA_FLOW_VIEW, full_nodes, full_edges, df_summaries)
