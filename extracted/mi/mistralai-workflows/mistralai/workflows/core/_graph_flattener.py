"""Flatten the tree IR into wire-format nodes and edges.

Source -> [_graph_builder] -> list[TreeNode] -> [_graph_flattener] -> flat dicts -> [_graph_emitter] -> AtlasWireFormat
                                                 ^ this module
"""

from __future__ import annotations

from typing import Any, Union

import structlog

from mistralai.workflows.core._graph_types import (
    TreeNode,
    _AgentNode,
    _ConditionalNode,
    _ContinueAsNewNode,
    _EllipsisNode,
    _HumanInputNode,
    _LoopNode,
    _MemoryOpNode,
    _ParallelNode,
    _RaiseNode,
    _SleepNode,
    _StepNode,
    _TryExceptNode,
    _WaitConditionNode,
)

logger = structlog.get_logger(__name__)


class GraphValidationError(ValueError):
    pass


def _apply_step_node_fields(flat: dict[str, Any], node: _StepNode) -> dict[str, Any]:
    if node.connectors:
        flat["connectors"] = node.connectors
    if not node.child_workflow:
        return flat
    flat["type"] = "child_workflow"
    if node.child_workflow_id is not None:
        flat["child_workflow_id"] = node.child_workflow_id
    if node.child_workflow_file is not None:
        flat["child_workflow_file"] = node.child_workflow_file
    if node.async_:
        flat["async"] = True
    return flat


_FLAT_TYPE_MAP: dict[type, str] = {
    _StepNode: "activity",
    _HumanInputNode: "human_input",
    _WaitConditionNode: "wait_condition",
    _SleepNode: "sleep",
    _MemoryOpNode: "memory_op",
    _ContinueAsNewNode: "continue_as_new",
    _EllipsisNode: "unknown",
    _AgentNode: "agent",
}

_LeafNode = Union[
    _StepNode,
    _HumanInputNode,
    _WaitConditionNode,
    _SleepNode,
    _MemoryOpNode,
    _ContinueAsNewNode,
    _EllipsisNode,
    _AgentNode,
]


def _leaf_to_flat(node: _LeafNode) -> dict[str, Any]:
    flat: dict[str, Any] = {
        "id": node.id,
        "type": _FLAT_TYPE_MAP[type(node)],
        "name": "..." if isinstance(node, _EllipsisNode) else node.label,
        "line": node.source_range.line,
        "source_range": node.source_range.to_dict(),
    }
    if isinstance(node, _StepNode):
        flat = _apply_step_node_fields(flat, node)
    elif isinstance(node, _AgentNode):
        flat["tools"] = node.tools
        flat["handoffs"] = node.handoffs
        if node.connectors:
            flat["connectors"] = node.connectors
    return flat


class _Flattener:
    def __init__(self) -> None:
        self.flat_nodes: list[dict[str, Any]] = []
        self.flat_edges: list[dict[str, Any]] = []
        self._seen_edge_ids: set[str] = set()
        self._seen_edge_pairs: set[tuple[str, str]] = set()
        self._seen_node_ids: set[str] = set()
        self._conditional_ids: set[str] = set()
        self._loop_ids: set[str] = set()
        self._loop_first_child: dict[str, str] = {}
        self._terminal_exit_ids: set[str] = set()
        self._terminating_conditionals: set[str] = set()
        self._out_id: str = ""

    def _add_node(self, node: dict[str, Any]) -> None:
        if node["id"] not in self._seen_node_ids:
            self._seen_node_ids.add(node["id"])
            self.flat_nodes.append(node)

    def _add_edge(self, edge: dict[str, Any]) -> None:
        if edge["from"] == edge["to"]:
            return
        if edge["id"] not in self._seen_edge_ids:
            self._seen_edge_ids.add(edge["id"])
            self._seen_edge_pairs.add((edge["from"], edge["to"]))
            self.flat_edges.append(edge)

    def _has_edge_between(self, from_id: str, to_id: str) -> bool:
        return (from_id, to_id) in self._seen_edge_pairs

    def _resolve_sink(self, sink: str) -> str:
        """If *sink* is a loop node, redirect to its first child (loop-back)."""
        if sink in self._loop_ids:
            return self._loop_first_child.get(sink, sink)
        return sink

    def _emit_branch_merge(self, last_id: str, cond_id: str, sink: str, suffix: str) -> None:
        if last_id != cond_id:
            # loops iterate implicitly; suppress merge-back edges
            if sink in self._loop_ids:
                return
            if last_id not in self._conditional_ids and not self._has_edge_between(last_id, sink):
                self._add_edge(
                    {
                        "id": f"e-merge-{cond_id}-{sink}-branch_{suffix}",
                        "from": last_id,
                        "to": sink,
                        "kind": "branch_merge",
                    }
                )
        else:
            # skip edge — don't redirect when it would create a self-loop
            resolved = self._resolve_sink(sink)
            target = resolved if resolved != cond_id else sink
            self._add_edge(
                {
                    "id": f"e-skip-{cond_id}-{target}-branch_{suffix}",
                    "from": cond_id,
                    "to": target,
                    "kind": f"branch_{suffix}_skip",
                }
            )

    def _emit_early_exit(self, from_id: str, cond_id: str, is_true: bool, is_error: bool = False) -> None:
        suffix = "true" if is_true else "false"
        exit_node_id = f"{cond_id}::exit_{suffix}"
        self._add_node(
            {
                "id": exit_node_id,
                "type": "output",
                "name": "raises" if is_error else "exit",
                "is_error": is_error,
                "line": 1,
                "source_range": {"begin": 0, "end": 0, "line": 1},
            }
        )
        self._terminal_exit_ids.add(exit_node_id)
        self._add_edge(
            {
                "id": f"e-exit-{suffix}-{from_id}-{exit_node_id}",
                "from": from_id,
                "to": exit_node_id,
                "kind": f"branch_exit_{suffix}",
            }
        )

    def _emit_inner_node(self, child: TreeNode, child_ids: list[str], sink: str | None = None) -> None:
        child_id = child.id
        sr = child.source_range.to_dict()
        child_line = child.source_range.line
        if isinstance(
            child,
            (
                _StepNode,
                _HumanInputNode,
                _WaitConditionNode,
                _SleepNode,
                _MemoryOpNode,
                _ContinueAsNewNode,
                _EllipsisNode,
                _AgentNode,
            ),
        ):
            self._add_node(_leaf_to_flat(child))
        elif isinstance(child, _RaiseNode):
            self._add_node(
                {
                    "id": child_id,
                    "type": "output",
                    "name": child.label,
                    "is_error": True,
                    "line": child_line,
                    "source_range": sr,
                }
            )
            self._terminal_exit_ids.add(child_id)
        elif isinstance(child, _ConditionalNode):
            if sink is None:
                logger.warning("conditional dropped: no sink provided", conditional_id=child_id)
                return
            self._emit_contained_conditional(child, child_ids, sink)
            return
        elif isinstance(child, _LoopNode):
            self._loop_ids.add(child_id)
            first = self._first_emittable_id(child.children)
            if first is not None:
                self._loop_first_child[child_id] = first
            inner_ids: list[str] = []
            for grandchild in child.children:
                self._emit_inner_node(grandchild, inner_ids, child_id)
            self._add_node(
                {
                    "id": child_id,
                    "type": "loop",
                    "name": child.label,
                    "line": child_line,
                    "source_range": sr,
                    "children": inner_ids,
                }
            )
        elif isinstance(child, _TryExceptNode):
            te_inner_ids: list[str] = []
            for tb in child.try_body:
                self._emit_inner_node(tb, te_inner_ids, child_id)
            for handler in child.handlers:
                for hc in handler.body:
                    self._emit_inner_node(hc, te_inner_ids, child_id)
            for fc in child.finally_body:
                self._emit_inner_node(fc, te_inner_ids, child_id)
            if te_inner_ids:
                self._add_node(
                    {
                        "id": child_id,
                        "type": "try_except",
                        "name": "except",
                        "line": child_line,
                        "source_range": sr,
                        "children": te_inner_ids,
                    }
                )
            else:
                return
        else:
            assert isinstance(child, _ParallelNode)
            par_branch_ids: list[list[str]] = []
            for branch in child.branches:
                lane_ids: list[str] = []
                for grandchild in branch:
                    self._emit_inner_node(grandchild, lane_ids, child_id)
                par_branch_ids.append(lane_ids)
            self._add_node(
                {
                    "id": child_id,
                    "type": "parallel",
                    "name": "parallel",
                    "line": child_line,
                    "source_range": sr,
                    "branches": par_branch_ids,
                }
            )
        child_ids.append(child_id)

    def _emit_contained_conditional(self, node: _ConditionalNode, child_ids: list[str], sink: str) -> None:
        cond_id = node.id
        self._conditional_ids.add(cond_id)
        sr = node.source_range.to_dict()
        self._add_node(
            {
                "id": cond_id,
                "type": "conditional",
                "name": node.label,
                "line": node.source_range.line,
                "source_range": sr,
            }
        )

        branch_sink = self._first_emittable_id(node.rejoin) or sink

        def emit_branch(
            branch_nodes: list[TreeNode],
            suffix: str,
            exits: bool,
            is_error: bool = False,
        ) -> tuple[list[str], list[str]]:
            ids: list[str] = []
            branch_start = len(self.flat_nodes)
            for bn in branch_nodes:
                self._emit_inner_node(bn, ids, branch_sink)
            descendants = [self.flat_nodes[i]["id"] for i in range(branch_start, len(self.flat_nodes))]
            if ids:
                self._add_edge(
                    {
                        "id": f"e-{cond_id}-{ids[0]}-branch_{suffix}",
                        "from": cond_id,
                        "to": ids[0],
                        "kind": f"branch_{suffix}",
                    }
                )
                for from_id, to_id in zip(ids, ids[1:]):
                    self._add_edge({"id": f"e-{from_id}-{to_id}", "from": from_id, "to": to_id, "kind": "sequential"})
                self._wire_branch(ids[-1], exits, suffix == "true", branch_sink, cond_id, is_error)
            else:
                self._wire_branch(cond_id, exits, suffix == "true", branch_sink, cond_id, is_error)
            return ids, descendants

        true_ids, true_descendants = emit_branch(node.true_branch, "true", node.true_exits, node.true_exit_error)
        false_ids, false_descendants = emit_branch(node.false_branch, "false", node.false_exits, node.false_exit_error)
        cond_flat = next(n for n in self.flat_nodes if n["id"] == cond_id)
        cond_flat["branchTrue"] = true_ids
        cond_flat["branchFalse"] = false_ids
        cond_flat["branchDescendants"] = true_descendants + false_descendants
        child_ids.append(cond_id)

        for rj in node.rejoin:
            if isinstance(rj, _ConditionalNode):
                self._emit_contained_conditional(rj, child_ids, sink)
            else:
                self._emit_inner_node(rj, child_ids, sink)

    def _first_emittable_id(self, nodes: list[TreeNode]) -> str | None:
        for node in nodes:
            if isinstance(node, _TryExceptNode):
                inner = self._first_emittable_id(node.try_body)
                if inner is not None:
                    return inner
            else:
                return node.id
        return None

    def _process_list(
        self, nodes: list[TreeNode], prev_id: str, first_kind: str, terminal_id: str | None = None
    ) -> str:
        for node_idx, node in enumerate(nodes):
            node_id = node.id
            sr = node.source_range.to_dict()
            line = node.source_range.line

            if isinstance(
                node,
                (
                    _StepNode,
                    _HumanInputNode,
                    _WaitConditionNode,
                    _SleepNode,
                    _MemoryOpNode,
                    _ContinueAsNewNode,
                    _EllipsisNode,
                ),
            ):
                self._add_node(_leaf_to_flat(node))
                self._add_edge({"id": f"e-{prev_id}-{node_id}", "from": prev_id, "to": node_id, "kind": first_kind})
                prev_id = node_id
                first_kind = "sequential"

            elif isinstance(node, _RaiseNode):
                self._add_node(
                    {
                        "id": node_id,
                        "type": "output",
                        "name": node.label,
                        "is_error": True,
                        "line": line,
                        "source_range": sr,
                    }
                )
                self._add_edge({"id": f"e-{prev_id}-{node_id}", "from": prev_id, "to": node_id, "kind": first_kind})
                self._terminal_exit_ids.add(node_id)
                prev_id = node_id
                first_kind = "sequential"

            elif isinstance(node, _TryExceptNode):
                try_body_last_id = self._process_list(node.try_body, prev_id, first_kind, terminal_id)
                prev_id = try_body_last_id
                handler_child_ids: list[str] = []
                for handler in node.handlers:
                    for child in handler.body:
                        self._emit_inner_node(child, handler_child_ids, node_id)
                if handler_child_ids:
                    self._add_node(
                        {
                            "id": node_id,
                            "type": "try_except",
                            "name": "except",
                            "line": line,
                            "source_range": sr,
                            "children": handler_child_ids,
                        }
                    )
                    if try_body_last_id not in self._terminal_exit_ids:
                        self._add_edge(
                            {
                                "id": f"e-{try_body_last_id}-{node_id}",
                                "from": try_body_last_id,
                                "to": node_id,
                                "kind": "sequential",
                            }
                        )
                    prev_id = node_id
                if node.finally_body:
                    prev_id = self._process_list(node.finally_body, prev_id, "sequential", terminal_id)
                first_kind = "sequential"

            elif isinstance(node, _AgentNode):
                self._add_node(_leaf_to_flat(node))
                self._add_edge({"id": f"e-{prev_id}-{node_id}", "from": prev_id, "to": node_id, "kind": first_kind})
                prev_id = node_id
                first_kind = "sequential"

            elif isinstance(node, _ParallelNode):
                child_ids: list[str] = []
                branch_ids: list[list[str]] = []
                for branch in node.branches:
                    lane_ids: list[str] = []
                    for child in branch:
                        self._emit_inner_node(child, lane_ids, node_id)
                    branch_ids.append(lane_ids)
                    child_ids.extend(lane_ids)
                self._add_node(
                    {
                        "id": node_id,
                        "type": "parallel",
                        "name": "parallel",
                        "line": line,
                        "source_range": sr,
                        "branches": branch_ids,
                    }
                )
                self._add_edge({"id": f"e-{prev_id}-{node_id}", "from": prev_id, "to": node_id, "kind": first_kind})
                prev_id = node_id
                first_kind = "sequential"

            elif isinstance(node, _LoopNode):
                self._loop_ids.add(node_id)
                first = self._first_emittable_id(node.children)
                if first is not None:
                    self._loop_first_child[node_id] = first
                child_ids_loop: list[str] = []
                for child in node.children:
                    self._emit_inner_node(child, child_ids_loop, node_id)
                self._add_node(
                    {
                        "id": node_id,
                        "type": "loop",
                        "name": node.label,
                        "line": line,
                        "source_range": sr,
                        "children": child_ids_loop,
                    }
                )
                self._add_edge({"id": f"e-{prev_id}-{node_id}", "from": prev_id, "to": node_id, "kind": first_kind})
                prev_id = node_id
                first_kind = "sequential"

            else:
                assert isinstance(node, _ConditionalNode)
                cond_id = node_id
                self._conditional_ids.add(cond_id)

                cond_flat: dict[str, Any] = {
                    "id": cond_id,
                    "type": "conditional",
                    "name": node.label,
                    "line": line,
                    "source_range": sr,
                }
                self._add_node(cond_flat)
                self._add_edge({"id": f"e-{prev_id}-{cond_id}", "from": prev_id, "to": cond_id, "kind": first_kind})

                if node.rejoin:
                    branch_sink = self._first_emittable_id(node.rejoin) or terminal_id
                else:
                    remaining = nodes[node_idx + 1 :]
                    branch_sink = self._first_emittable_id(remaining) or terminal_id

                true_start = len(self.flat_nodes)
                true_last = self._process_list(node.true_branch, cond_id, "branch_true", branch_sink)
                true_end = len(self.flat_nodes)

                false_start = len(self.flat_nodes)
                false_last = self._process_list(node.false_branch, cond_id, "branch_false", branch_sink)
                false_end = len(self.flat_nodes)

                # ponytail: transitive — includes nested conditional descendants, not just direct children
                cond_flat["branchDescendants"] = [
                    self.flat_nodes[i]["id"]
                    for i in (*range(true_start, true_end), *range(false_start, false_end))
                    if self.flat_nodes[i]["id"] not in self._terminal_exit_ids
                ]

                self._wire_branch(true_last, node.true_exits, True, branch_sink, cond_id, node.true_exit_error)
                self._wire_branch(false_last, node.false_exits, False, branch_sink, cond_id, node.false_exit_error)

                if node.rejoin:
                    rejoin_start = branch_sink if branch_sink is not None else cond_id
                    prev_id = self._process_list(node.rejoin, rejoin_start, "sequential", terminal_id)
                else:
                    if node.true_exits and node.false_exits:
                        self._terminating_conditionals.add(cond_id)
                    prev_id = cond_id

                first_kind = "sequential"

        return prev_id

    def _wire_branch(
        self, last_id: str, exits: bool, is_true: bool, sink: str | None, cond_id: str, is_error: bool = False
    ) -> None:
        suffix = "true" if is_true else "false"
        if exits:
            if last_id in self._terminal_exit_ids or (last_id in self._conditional_ids and last_id != cond_id):
                return
            if is_error:
                self._emit_early_exit(last_id, cond_id, is_true, is_error)
            else:
                self._add_edge(
                    {
                        "id": f"e-exit-{suffix}-{last_id}-{self._out_id}",
                        "from": last_id,
                        "to": self._out_id,
                        "kind": f"branch_exit_{suffix}",
                    }
                )
        elif sink is not None:
            self._emit_branch_merge(last_id, cond_id, sink, suffix)

    def flatten(
        self,
        tree_nodes: list[TreeNode],
        wf_name: str,
        output_type: str | None,
        *,
        ep_name: str | None = None,
        ep_begin: int | None = None,
        ep_end: int | None = None,
        ep_line: int | None = None,
        ep_end_line: int | None = None,
        ep_param_type: str | None = None,
        ep_param_fields: list[dict[str, str]] | None = None,
        wf_begin: int | None = None,
        wf_end: int | None = None,
        wf_line: int | None = None,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        root_line = wf_line or 1
        root_begin = wf_begin if wf_begin is not None else 0
        root_end = wf_end if wf_end is not None else 0
        self._add_node(
            {
                "id": wf_name,
                "type": "workflow",
                "name": wf_name,
                "line": root_line,
                "source_range": {"begin": root_begin, "end": root_end, "line": root_line},
            }
        )
        chain_start = wf_name

        if ep_name is not None and ep_begin is not None:
            ep_id = f"{wf_name}::entrypoint"
            ep_line_ = ep_line or 1
            ep_node: dict[str, Any] = {
                "id": ep_id,
                "type": "entrypoint",
                "name": ep_name,
                "line": ep_line_,
                "source_range": {"begin": ep_begin, "end": ep_end or ep_begin, "line": ep_line_},
            }
            if ep_param_type is not None:
                ep_node["param_type"] = ep_param_type
            if ep_param_fields is not None:
                ep_node["param_fields"] = ep_param_fields
            self._add_node(ep_node)
            self._add_edge({"id": f"e-{wf_name}-{ep_id}", "from": wf_name, "to": ep_id, "kind": "sequential"})
            chain_start = ep_id

        self._out_id = f"{wf_name}::output"
        out_label = output_type or "exit"
        out_line = ep_end_line or 1
        out_byte = ep_end if ep_end is not None else 0

        last_id = self._process_list(tree_nodes, chain_start, "sequential", self._out_id)

        body_falls_through = last_id not in self._terminal_exit_ids and last_id not in self._terminating_conditionals
        out_referenced = any(e["to"] == self._out_id for e in self.flat_edges)
        if body_falls_through or out_referenced:
            self._add_node(
                {
                    "id": self._out_id,
                    "type": "output",
                    "name": out_label,
                    "line": out_line,
                    "source_range": {"begin": out_byte, "end": out_byte, "line": out_line},
                }
            )
        if body_falls_through:
            self._add_edge(
                {"id": f"e-{last_id}-{self._out_id}", "from": last_id, "to": self._out_id, "kind": "sequential"}
            )

        assert len(self.flat_nodes) == len(self._seen_node_ids), "duplicate node IDs in flat graph"
        return self.flat_nodes, self.flat_edges


def _flatten_tree(
    tree_nodes: list[TreeNode],
    wf_name: str,
    output_type: str | None,
    *,
    ep_name: str | None = None,
    ep_begin: int | None = None,
    ep_end: int | None = None,
    ep_line: int | None = None,
    ep_end_line: int | None = None,
    ep_param_type: str | None = None,
    ep_param_fields: list[dict[str, str]] | None = None,
    wf_begin: int | None = None,
    wf_end: int | None = None,
    wf_line: int | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    return _Flattener().flatten(
        tree_nodes,
        wf_name,
        output_type,
        ep_name=ep_name,
        ep_begin=ep_begin,
        ep_end=ep_end,
        ep_line=ep_line,
        ep_end_line=ep_end_line,
        ep_param_type=ep_param_type,
        ep_param_fields=ep_param_fields,
        wf_begin=wf_begin,
        wf_end=wf_end,
        wf_line=wf_line,
    )


def _validate_flat_graph(wf_name: str, flat_nodes: list[dict[str, Any]], flat_edges: list[dict[str, Any]]) -> None:
    """Assert every conditional node has exactly 1 true output and 1 false output."""
    from_index: dict[str, list[dict[str, Any]]] = {}
    for e in flat_edges:
        from_index.setdefault(e["from"], []).append(e)
    for node in flat_nodes:
        if node["type"] != "conditional":
            continue
        n_id = node["id"]
        out_edges = from_index.get(n_id, [])
        true_out = [e for e in out_edges if e["kind"] in ("branch_true", "branch_exit_true", "branch_true_skip")]
        false_out = [e for e in out_edges if e["kind"] in ("branch_false", "branch_exit_false", "branch_false_skip")]
        if len(true_out) != 1:
            raise GraphValidationError(
                f"[{wf_name}] Conditional {n_id!r} has {len(true_out)} true output(s), expected 1"
            )
        if len(false_out) != 1:
            raise GraphValidationError(
                f"[{wf_name}] Conditional {n_id!r} has {len(false_out)} false output(s), expected 1"
            )
