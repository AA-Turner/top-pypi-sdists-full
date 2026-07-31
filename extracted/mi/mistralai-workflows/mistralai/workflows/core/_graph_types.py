"""Shared types for the workflow graph pipeline.

Source -> [_graph_builder] -> list[TreeNode] -> [_graph_flattener] -> flat dicts -> [_graph_emitter] -> AtlasWireFormat
                              ^ this module: types used across all phases
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import Union

_MEMORY_OPS: frozenset[str] = frozenset({"save_memory", "load_memory", "load_history"})

# Connector metadata stamped by the mistralai connectors plugin (@uses_connectors / connector()).
# Duck-typed here so core does not import the plugin: the workflow class carries plugin metadata at
# `__plugin_metadata__["mistralai"]["connectors"]`, and a connector dependency exposes `connector_name`.
# The two keys mirror MISTRALAI_PLUGIN_KEY / CONNECTORS_KEY in
# mistralai.workflows.plugins.mistralai.connectors.constants — keep them in sync.
_PLUGIN_META_ATTR = "__plugin_metadata__"
_MISTRALAI_PLUGIN_KEY = "mistralai"
_CONNECTORS_META_KEY = "connectors"


# ---------------------------------------------------------------------------
# Typed tree IR — discriminated union for the 14 node kinds produced by
# _walk_body_tree and consumed by _Flattener.
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class _SourceRange:
    begin: int
    end: int
    line: int

    def to_dict(self) -> dict[str, int]:
        return {"begin": self.begin, "end": self.end, "line": self.line}


@dataclass(slots=True)
class _StepNode:
    id: str
    label: str
    source_range: _SourceRange
    child_workflow: bool = False
    # Routing id of the child: its registered workflow name (the class name when
    # unresolvable). None when the child is not in the scanned set.
    child_workflow_id: str | None = None
    child_workflow_file: str | None = None
    async_: bool = False
    connectors: list[str] = field(default_factory=list)


@dataclass(slots=True)
class _EllipsisNode:
    id: str
    source_range: _SourceRange


@dataclass(slots=True)
class _ConditionalNode:
    id: str
    label: str
    source_range: _SourceRange
    true_branch: list[TreeNode]
    true_exits: bool
    true_exit_error: bool
    false_branch: list[TreeNode]
    false_exits: bool
    false_exit_error: bool
    rejoin: list[TreeNode]


@dataclass(slots=True)
class _LoopNode:
    id: str
    label: str
    source_range: _SourceRange
    children: list[TreeNode]


@dataclass(slots=True)
class _TryExceptHandler:
    exception_type: str | None
    body: list[TreeNode]


@dataclass(slots=True)
class _TryExceptNode:
    id: str
    source_range: _SourceRange
    try_body: list[TreeNode]
    handlers: list[_TryExceptHandler]
    finally_body: list[TreeNode]


@dataclass(slots=True)
class _HumanInputNode:
    id: str
    label: str
    source_range: _SourceRange


@dataclass(slots=True)
class _WaitConditionNode:
    id: str
    label: str
    source_range: _SourceRange


@dataclass(slots=True)
class _SleepNode:
    id: str
    label: str
    source_range: _SourceRange


@dataclass(slots=True)
class _MemoryOpNode:
    id: str
    label: str
    source_range: _SourceRange


@dataclass(slots=True)
class _ContinueAsNewNode:
    id: str
    label: str
    source_range: _SourceRange


@dataclass(slots=True)
class _RaiseNode:
    id: str
    label: str
    source_range: _SourceRange


@dataclass(slots=True)
class _ParallelNode:
    id: str
    source_range: _SourceRange
    branches: list[list[TreeNode]]


@dataclass(slots=True)
class _AgentNode:
    id: str
    label: str
    tools: list[str]
    handoffs: list[str]
    source_range: _SourceRange
    connectors: list[str] = field(default_factory=list)


TreeNode = Union[
    _StepNode,
    _EllipsisNode,
    _ConditionalNode,
    _LoopNode,
    _TryExceptNode,
    _HumanInputNode,
    _WaitConditionNode,
    _SleepNode,
    _MemoryOpNode,
    _ContinueAsNewNode,
    _RaiseNode,
    _ParallelNode,
    _AgentNode,
]


@dataclass
class _FileIndex:
    line_byte_starts: list[int]
    lines: list[str]
    fn_by_line: dict[int, ast.FunctionDef | ast.AsyncFunctionDef]


@dataclass
class _TreeCtx:
    """Simplified walk context for building the v2 tree format — no edge tracking."""

    # ponytail: list[int] so dataclasses.replace shares the counter by reference across scopes
    cond_counter: list[int] = field(default_factory=lambda: [0])
    human_input_counter: list[int] = field(default_factory=lambda: [0])
    ellipsis_counter: list[int] = field(default_factory=lambda: [0])
    loop_counter: list[int] = field(default_factory=lambda: [0])
    try_counter: list[int] = field(default_factory=lambda: [0])
    parallel_counter: list[int] = field(default_factory=lambda: [0])
    wait_counter: list[int] = field(default_factory=lambda: [0])
    sleep_counter: list[int] = field(default_factory=lambda: [0])
    memory_counter: list[int] = field(default_factory=lambda: [0])
    raise_counter: list[int] = field(default_factory=lambda: [0])
    agent_counter: list[int] = field(default_factory=lambda: [0])
    cls_def: ast.ClassDef | None = None
    workflow_cls: type | None = None
    visited_methods: set[str] = field(default_factory=set[str])
    param_types: dict[str, type] = field(default_factory=dict[str, type])
    # Nested local functions (def/async def) defined in the current scope, and simple
    # name -> value bindings, so calls to local helpers and `*tasks` spreads passed to
    # asyncio.gather can be resolved. inlined_funcs guards against infinite recursion.
    local_funcs: dict[str, ast.FunctionDef | ast.AsyncFunctionDef] = field(
        default_factory=lambda: dict[str, ast.FunctionDef | ast.AsyncFunctionDef]()
    )
    name_values: dict[str, ast.expr] = field(default_factory=dict[str, ast.expr])
    inlined_funcs: frozenset[str] = field(default_factory=frozenset[str])


_ACTIVITY_NODE_TYPES = (
    _StepNode,
    _HumanInputNode,
    _WaitConditionNode,
    _SleepNode,
    _MemoryOpNode,
    _ContinueAsNewNode,
    _AgentNode,
)


def _decorator_leaf_name(node: ast.expr) -> str:
    """Return the leaf identifier of a decorator expression (last segment)."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return ""


def _has_activity_decorator(fn_def: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """Return True if the function has an @activity() or @*.activity() decorator."""
    for dec in fn_def.decorator_list:
        inner = dec.func if isinstance(dec, ast.Call) else dec
        if _decorator_leaf_name(inner) == "activity":
            return True
    return False
