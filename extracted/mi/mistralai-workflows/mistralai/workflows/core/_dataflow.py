"""Build data-flow graph views from a control-flow wire format payload.

Takes a v3 wire format dict (with embedded source) and produces a
data-flow view alongside the original control-flow view.
"""

from __future__ import annotations

import bisect
import copy
from collections.abc import Mapping
from typing import Any

import libcst as cst
import libcst.metadata as meta
import structlog

logger = structlog.get_logger()

CONTROL_FLOW_VIEW = "Control flow"
DATA_FLOW_VIEW = "Data flow"
# Ceiling on source fed to the CST parse; a larger module risks OOM.
_MAX_SOURCE_BYTES = 512_000
_STRUCTURAL_TYPES = frozenset({"conditional", "loop", "try_except", "parallel"})
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


def build_retarget_map(cf: dict[str, Any]) -> dict[str, str]:
    """Map control-flow node ids to their data-flow transform replacements.

    Re-keys unknown/ellipsis node ids to transform ids by matching source
    ranges. This is the cheap subset of :func:`_build` (parse + assignment
    collection + ellipsis explosion only — no edge computation, fan-out
    detection, or suppression passes). Use on hot paths that only need the
    id re-keying, such as the LLM-summary broadcast.
    """
    try:
        sources: dict[str, str] = cf.get("sources") or {}
        primary_file: str | None = cf.get("primary_file")
        source_text = _pick_source(sources, primary_file)
        if source_text is None:
            return {}
        source_bytes = source_text.encode("utf-8")
        if len(source_bytes) > _MAX_SOURCE_BYTES:
            return {}
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
        workflow_name = cf.get("workflow_name", "")
        transforms, unknown_ids = _expand_unknown_nodes(
            nodes,
            collector.assignments,
            workflow_name,
        )
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
    """Find a non-structural leaf node on this line."""
    for _, _, node in index:
        if node.get("line") == line and node.get("type") not in (
            "workflow",
            "entrypoint",
            "conditional",
            "loop",
            "try_except",
            "parallel",
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
    def __init__(self) -> None:
        self.returns: list[cst.Return] = []

    def visit_Return(self, node: cst.Return) -> None:
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
    """Replace unknown nodes with transform nodes for each assignment inside."""
    unknown_nodes = [n for n in nodes if n["type"] == "unknown"]
    unknown_ids = {n["id"] for n in unknown_nodes}
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


def _collect_return_offsets(
    wrapper: meta.MetadataWrapper,
    positions: Mapping[cst.CSTNode, Any],
    line_starts: list[int],
) -> list[tuple[int, int]]:
    collector = _ReturnCollector()
    wrapper.visit(collector)
    ranges: list[tuple[int, int]] = []
    for ret_node in collector.returns:
        pos = positions.get(ret_node)
        if isinstance(pos, meta.CodeRange):
            b = _line_col_to_byte_offset(line_starts, pos.start.line, pos.start.column)
            e = _line_col_to_byte_offset(line_starts, pos.end.line, pos.end.column)
            ranges.append((b, e))
    return ranges


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

    return_offsets = _collect_return_offsets(wrapper, positions, line_starts)

    ep_id = f"{workflow_name}::entrypoint"
    node_by_id = {n["id"]: n for n in all_nodes}

    edges: list[dict[str, Any]] = []
    seen_edges: set[tuple[str, str, str]] = set()

    for scope in unique_scopes:
        for assignment in scope.assignments:
            if not isinstance(assignment, meta.Assignment):
                continue

            var_name = assignment.name
            def_cst = assignment.node

            def_offset = _cst_to_byte_offset(positions, def_cst, line_starts)
            if def_offset is None:
                continue

            def_graph = _find_node_at_offset(node_index, def_offset)
            if def_graph is None and entrypoint_info:
                ep_begin = entrypoint_info.get("begin", 0)
                ep_end = entrypoint_info.get("end", 0)
                if ep_begin <= def_offset < ep_end:
                    def_graph = node_by_id.get(ep_id)
            if def_graph is None:
                continue

            # Assignment target before the activity range lands on a container;
            # check if a leaf node on the same line should get credit
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
                    def_graph = same_line

            for access in assignment.references:
                use_offset = _cst_to_byte_offset(positions, access.node, line_starts)
                if use_offset is None:
                    continue

                use_graph = _find_node_at_offset(node_index, use_offset)

                # The output node is reached by control flow only, so a use
                # inside a return contributes no data edge.
                if use_graph is not None and use_graph["id"] == ep_id:
                    if any(rb <= use_offset < re for rb, re in return_offsets):
                        continue

                if use_graph is None:
                    continue

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

    _repoint_preamble_edges(edges, all_nodes)
    return edges


def _repoint_preamble_edges(
    edges: list[dict[str, Any]],
    all_nodes: list[dict[str, Any]],
) -> None:
    """Re-point data_dep fan-out edges from the def node to the last preamble
    block before the first fan-out consumer.

    A variable defined at the top of the spine (e.g. ``all_pkgs``) and consumed
    by a fan-out further down would otherwise draw an edge from the def over the
    whole preamble. Re-point each such edge to the spine node immediately before
    the first fan-out consumer so the fan-out reads as starting after the
    preamble. Edges into conditionals (guards), unlabeled edges, and
    mutation-chain vars (handled by :func:`_bridge_mutation_edges`) are left
    untouched.
    """
    # Skip mutation-chain vars: their init's edges must stay on the init
    # transform so _bridge_mutation_edges can copy them onto mutations.
    # Re-pointing them off the init would make bridging miss them entirely.
    target_var_counts: dict[str, int] = {}
    for n in all_nodes:
        if n.get("type") == "transform":
            tv = n.get("target_var")
            if tv:
                target_var_counts[tv] = target_var_counts.get(tv, 0) + 1
    mutation_vars = {v for v, c in target_var_counts.items() if c >= 2}

    # Top-level spine: nodes whose source range is not strictly contained in a
    # structural container, ordered by begin offset.
    containers = [n for n in all_nodes if n.get("type") in _STRUCTURAL_TYPES]
    raw_container_ranges = [
        ((c.get("source_range") or {}).get("begin"), (c.get("source_range") or {}).get("end")) for c in containers
    ]
    container_ranges = sorted(
        [(cb, ce) for cb, ce in raw_container_ranges if cb is not None and ce is not None],
        key=lambda r: r[0],
    )
    container_begins = [r[0] for r in container_ranges]

    def _is_top_level(n: dict[str, Any]) -> bool:
        sr = n.get("source_range") or {}
        b, e = sr.get("begin"), sr.get("end")
        if b is None or e is None:
            return True
        # Only containers starting before b can strictly contain [b, e);
        # bisect skips the rest, turning the scan into O(log c + k).
        idx = bisect.bisect_left(container_begins, b)
        for i in range(idx):
            if e <= container_ranges[i][1]:
                return False
        return True

    spine = sorted(
        [n for n in all_nodes if _is_top_level(n)],
        key=lambda n: (n.get("source_range") or {}).get("begin", 0),
    )
    if len(spine) < 3:
        return
    pos = {n["id"]: i for i, n in enumerate(spine)}
    node_by_id = {n["id"]: n for n in all_nodes}

    by_var: dict[str, list[dict[str, Any]]] = {}
    for e in edges:
        if e["kind"] == "data_dep":
            label = e.get("label", "")
            # Unlabeled data_dep edges have no variable to re-point by.
            if label:
                by_var.setdefault(label, []).append(e)

    for var, var_edges in by_var.items():
        if var in mutation_vars:
            continue
        by_src: dict[str, list[dict[str, Any]]] = {}
        for e in var_edges:
            by_src.setdefault(e["from"], []).append(e)
        for src, outs in by_src.items():
            if src not in pos:
                continue
            # Fan-out consumers: top-level, non-conditional targets of this def.
            consumers = [e for e in outs if e["to"] in pos and node_by_id.get(e["to"], {}).get("type") != "conditional"]
            if len(consumers) < 2:
                continue
            consumers.sort(key=lambda e: pos[e["to"]])
            # Walk back past structural nodes (a guard/loop doesn't produce the
            # var) to the last non-structural preamble block before the fan-out.
            # Landing on a conditional would make the guard appear to emit a var
            # it only reads.
            target_pos = pos[consumers[0]["to"]] - 1
            while target_pos > pos[src] and spine[target_pos].get("type") in _STRUCTURAL_TYPES:
                target_pos -= 1
            if target_pos <= pos[src]:
                continue  # no non-structural spine node between def and consumer
            target = spine[target_pos]["id"]
            for e in consumers:
                orig = e["from"]
                e["from"] = target
                # Keep the original source in the id so two producers re-pointed
                # to the same target for the same (to, var) don't collide.
                e["id"] = f"e-data-{target}-{e['to']}-{var}-{orig}"


# ---------------------------------------------------------------------------
# Step 4: Process group detection (fan-out)
# ---------------------------------------------------------------------------


def _detect_fan_out(
    nodes: list[dict[str, Any]],
    data_edges: list[dict[str, Any]],
    workflow_name: str,
) -> list[dict[str, Any]]:
    """Find fan-out patterns and emit parallel container nodes."""
    node_by_id = {n["id"]: n for n in nodes}
    _NON_FAN_TARGETS = frozenset({"output", "conditional"})

    outgoing: dict[str, list[dict[str, Any]]] = {}
    for e in data_edges:
        target = node_by_id.get(e["to"])
        if target and target["type"] not in _NON_FAN_TARGETS and e["from"] != e["to"]:
            outgoing.setdefault(e["from"], []).append(e)

    # Reachability check: drop targets downstream of another target
    data_dep_next: dict[str, set[str]] = {}
    for e in data_edges:
        if e["kind"] == "data_dep":
            data_dep_next.setdefault(e["from"], set()).add(e["to"])

    def reachable(start: str) -> set[str]:
        visited: set[str] = set()
        stack = [start]
        while stack:
            cur = stack.pop()
            for nxt in data_dep_next.get(cur, ()):
                if nxt not in visited:
                    visited.add(nxt)
                    stack.append(nxt)
        return visited

    groups: list[dict[str, Any]] = []
    for src_id, fan_edges in outgoing.items():
        targets = {e["to"] for e in fan_edges}
        if len(targets) < 2:
            continue

        src_node = node_by_id.get(src_id)
        if not src_node or src_node["type"] in _STRUCTURAL_TYPES:
            continue

        # Drop targets reachable from another target (not truly parallel)
        independent = set(targets)
        for t in targets:
            independent -= reachable(t)
        if len(independent) < 2:
            continue

        branches = [
            [t]
            for t in sorted(
                independent,
                key=lambda t: node_by_id.get(t, {}).get("line", 0),
            )
        ]
        fan_vars = sorted({e.get("label", "") for e in fan_edges if e.get("label") and e["to"] in independent})

        # Place group at the line of its first child so nodes between
        # the source and the group (e.g. initializations) sort before it
        child_lines = [node_by_id.get(t, {}).get("line", 0) for t in independent]
        group_line = min(child_lines) if child_lines else src_node.get("line", 0)

        groups.append(
            {
                "id": f"{workflow_name}::group_{src_id.split('::')[-1]}",
                "type": "parallel",
                "name": ", ".join(fan_vars) if fan_vars else "process",
                "line": group_line,
                "source_range": src_node.get("source_range", {"begin": 0, "end": 0}),
                "branches": branches,
                "children": [t for b in branches for t in b],
            }
        )

    return groups


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


def _build_sequential_spine(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    workflow_name: str,
    cf_rank: dict[str, int],
) -> list[dict[str, Any]]:
    """Chain top-level nodes with sequential edges so the tree builder can
    render them. Nodes inside containers (children, branch targets) are
    skipped — they're positioned by their parent."""
    # Collect nodes owned by containers
    owned: set[str] = set()
    for n in nodes:
        for c in n.get("children") or []:
            owned.add(c)
        for branch in n.get("branches") or []:
            for c in branch:
                owned.add(c)
    branch_targets = {e["to"] for e in edges if e["kind"] in ("branch_true", "branch_false")}
    owned |= branch_targets

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

    # Source line is not execution order: a node inlined from a helper carries
    # the helper's definition line, which may sit above the entrypoint. Order
    # by the control-flow chain where it knows the node, and keep nodes it does
    # not know (transforms split out of an ellipsis) beside the ranked node
    # they follow in the file.
    line_sorted = sorted(
        [n for n in nodes if n["id"] != wf_id and n["id"] not in owned],
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
    spine = [n for _, n in sorted(ordered, key=lambda t: t[0])]

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
            kids = sorted(
                [c for c in n["children"] if c not in branch_targets],
                key=lambda c: node_by_id.get(c, {}).get("line", 0),
            )
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
    valid_ids: set[str],
) -> None:
    """For each mutation transform (x.append), copy outgoing edges from x's
    initialization transform so the mutation participates in data flow."""
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
            if mid not in valid_ids:
                continue
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

    # Index consumers by (src, label) once for the last-write-wins pass below.
    consumers_by_src_label: dict[tuple[str, str], set[str]] = {}
    for e in edges:
        if e["kind"] == "data_dep":
            consumers_by_src_label.setdefault((e["from"], e.get("label", "")), set()).add(e["to"])

    # Last-write-wins: in a mutation chain (init + ≥1 mutation on the same
    # var), the last mutation carries the value that reaches downstream
    # consumers. Drop the init's and earlier mutations' edges to any consumer
    # the last mutation also feeds with this var, so each consumer reads a
    # single source per mutated var instead of a tangle of redundant writes.
    for var, group in by_var.items():
        if len(group) < 2:
            continue
        # Pick the textual-last valid mutation by source position, not
        # node-list order (which follows the walker's DFS, not source order).
        ordered = sorted(group, key=lambda t: (t.get("source_range") or {}).get("begin", 0))
        last = next((t for t in reversed(ordered) if t["id"] in valid_ids), None)
        if last is None:
            continue
        last_consumers = consumers_by_src_label.get((last["id"], var), set())
        if not last_consumers:
            continue
        superseded = {t["id"] for t in group if t["id"] != last["id"]}
        edges[:] = [
            e
            for e in edges
            if not (
                e["kind"] == "data_dep"
                and e["from"] in superseded
                and e["to"] in last_consumers
                and e.get("label") == var
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
        else:
            copy_e = {**e}
            seen[key] = copy_e
            deduped.append(copy_e)
    result["edges"] = deduped
    result.pop("node_summaries", None)
    if summaries:
        result["node_summaries"] = summaries
    return result


# ---------------------------------------------------------------------------
# Main build pipeline
# ---------------------------------------------------------------------------


def _build(cf: dict[str, Any]) -> dict[str, Any]:
    sources: dict[str, str] = cf.get("sources") or {}
    primary_file: str | None = cf.get("primary_file")
    # Deep-copy nodes to avoid mutating the CF payload's shared dicts
    nodes: list[dict[str, Any]] = copy.deepcopy(cf.get("nodes", []))
    entrypoint_info = cf.get("entrypoint")
    workflow_name: str = cf.get("workflow_name", "")

    source_text = _pick_source(sources, primary_file)
    if source_text is None:
        raise ValueError("No source text available for data-flow analysis")
    source_bytes = source_text.encode("utf-8")
    # Guard against pathologically large source that could OOM during CST parse
    if len(source_bytes) > _MAX_SOURCE_BYTES:
        raise ValueError(f"Source too large for data-flow analysis ({len(source_text)} chars)")

    line_starts = _build_line_starts(source_bytes)

    # Step 1: Parse source
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

    # Step 2: Explode ellipses into transforms
    transforms, unknown_ids = _expand_unknown_nodes(
        nodes,
        collector.assignments,
        workflow_name,
    )
    df_nodes = [n for n in nodes if n["id"] not in unknown_ids] + transforms
    node_index = _build_node_index(df_nodes)

    # Step 3: Compute data-dep edges
    data_edges = _compute_data_edges(
        wrapper,
        positions,
        line_starts,
        node_index,
        df_nodes,
        entrypoint_info,
        workflow_name,
    )

    # --- Full data-flow view ---
    keep_types = (
        frozenset(
            {
                "entrypoint",
                "activity",
                "output",
                "dispatch",
                "agent",
                "child_workflow",
                "human_input",
                "wait_condition",
                "sleep",
                "task",
                "memory_op",
                "transform",
            }
        )
        | _STRUCTURAL_TYPES
    )

    full_nodes = [n for n in df_nodes if n["type"] in keep_types]
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
    full_edges = [e for e in data_edges if e["from"] in full_ids and e["to"] in full_ids]

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

    _bridge_mutation_edges(full_edges, transforms, full_ids)

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
            for c in node.get("children") or []:
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
        if n.get("children"):
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

    # Drop data_dep edges that pierce a container the producer is not inside:
    # the line would cross the box boundary. Being inside *some* container is
    # not enough — an edge from one loop's body into another loop's body
    # crosses just as much as one from the top level. A container feeding its
    # own child counts too; the loop header already shows the loop variable.
    def _pierces_container(src: str, tgt: str) -> bool:
        return any(tgt in desc and src not in desc for desc in container_descendants.values())

    full_edges = [e for e in full_edges if not (e["kind"] == "data_dep" and _pierces_container(e["from"], e["to"]))]

    # Step 4: Detect fan-out process groups
    fan_out_groups = _detect_fan_out(full_nodes, full_edges, workflow_name)
    full_nodes = full_nodes + fan_out_groups
    full_ids = {n["id"] for n in full_nodes}

    # Adopt transforms into containers when all their data consumers
    # are inside that container (e.g. loop accumulator init before a loop).
    # Uses pre-suppression data_edges since cross-boundary edges were removed.
    node_by_id = {n["id"]: n for n in full_nodes}
    for t in [n for n in full_nodes if n["type"] == "transform"]:
        consumers = {
            e["to"] for e in data_edges if e["kind"] == "data_dep" and e["from"] == t["id"] and e["to"] in full_ids
        }
        if not consumers:
            continue
        for cid, desc in container_descendants.items():
            if consumers <= desc:
                container = node_by_id.get(cid)
                if container and t["id"] not in (container.get("children") or []):
                    container.setdefault("children", []).insert(0, t["id"])
                break

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

    # A standalone data_dep edge only earns its place when it shows a
    # data-based branch: with a single consumer the value just travels forward
    # and the spine already shows that. Two exemptions:
    #   - edges sharing a pair with a spine edge, which the renderer folds into
    #     the control-flow edge as a label rather than drawing a second line;
    #   - edges into a conditional, which carry the value the guard branches on.
    spine_pairs = {(e["from"], e["to"]) for e in full_edges if e["kind"] != "data_dep"}
    guard_ids = {n["id"] for n in full_nodes if n["type"] == "conditional"}
    consumers_by_producer: dict[str, set[str]] = {}
    for e in full_edges:
        if e["kind"] == "data_dep":
            consumers_by_producer.setdefault(e["from"], set()).add(e["to"])
    full_edges = [
        e
        for e in full_edges
        if e["kind"] != "data_dep"
        or e["to"] in guard_ids
        or (e["from"], e["to"]) in spine_pairs
        or len(consumers_by_producer[e["from"]]) >= 2
    ]

    # Carry LLM summaries from the control-flow view, re-keying any
    # unknown/ellipsis node ids to the transform ids that replaced them
    # (retarget maps by matching source range).
    df_summaries: dict[str, Any] = {}
    for old_id, summary in (cf.get("node_summaries") or {}).items():
        new_id = retarget.get(old_id, old_id)
        if new_id in full_ids:
            df_summaries[new_id] = summary

    return _assemble_view(cf, DATA_FLOW_VIEW, full_nodes, full_edges, df_summaries)
