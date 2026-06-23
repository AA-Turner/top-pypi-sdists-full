import ast
import dataclasses
import inspect
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Literal, get_type_hints

import structlog

from mistralai.workflows.core.activity import check_is_activity
from mistralai.workflows.core.wire_format import AtlasWireFormat

logger = structlog.get_logger(__name__)

# Node kinds that count as "visible content" inside a loop or conditional branch.
# Used to decide whether to prepend a synthetic ellipsis when the body is empty.
_RENDERABLE_KINDS: frozenset[str] = frozenset(
    {
        "step",
        "ellipsis",
        "conditional",
        "loop",
        "try_except",
        "human_input",
        "wait_condition",
        "dispatch",
        "memory_op",
        "raise",
        "parallel",
    }
)
_MEMORY_OPS: frozenset[str] = frozenset({"save_memory", "load_memory", "load_history"})

# Max indirection followed when resolving an awaitable to its underlying call. Real nesting is
# shallow (e.g. starred -> name -> comprehension -> call is 3 hops); 4 leaves headroom for one
# extra indirection while still terminating cycles from self-referential bindings (e.g. x = x or []).
_MAX_AWAITABLE_RESOLVE_DEPTH = 4


@dataclass
class _FileIndex:
    line_byte_starts: list[int]
    lines: list[str]
    fn_by_line: dict[int, ast.FunctionDef | ast.AsyncFunctionDef]


def _extract_call(stmt: ast.stmt) -> ast.Call | None:
    """Extract the innermost Call from an expression or assignment statement."""
    if isinstance(stmt, ast.Expr):
        v = stmt.value
        if isinstance(v, ast.Await) and isinstance(v.value, ast.Call):
            return v.value
        if isinstance(v, ast.Call):
            return v
    if isinstance(stmt, (ast.Assign, ast.AnnAssign)):
        v = stmt.value  # type: ignore[assignment]
        if v is None:
            return None
        if isinstance(v, ast.Await) and isinstance(v.value, ast.Call):
            return v.value
        if isinstance(v, ast.Call):
            return v
    return None


def _awaited_calls_in_order(stmt: ast.stmt) -> list[ast.Call]:
    """Return the call expressions that are directly awaited anywhere within a statement,
    ordered by source position.

    Surfaces activities awaited inside a larger expression — e.g. the ``publish_article``
    call in ``results.append(await publish_article(title))`` — which ``_extract_call`` does
    not see because it only yields the statement's outermost call.
    """
    awaited: list[ast.Call] = []

    class AwaitedCallVisitor(ast.NodeVisitor):
        def visit_Await(self, node: ast.Await) -> None:
            if isinstance(node.value, ast.Call):
                awaited.append(node.value)
            self.generic_visit(node)

        def visit_Lambda(self, node: ast.Lambda) -> None:
            self.visit(node.args)

    AwaitedCallVisitor().visit(stmt)
    awaited.sort(key=lambda c: (c.lineno, c.col_offset))
    return awaited


def _collect_lane_call_exprs(
    awaitables: list[ast.expr],
    name_values: dict[str, ast.expr],
) -> list[ast.Call]:
    """Resolve a list of awaitable expressions (e.g. asyncio.gather args, or the list passed
    to execute_activities_in_parallel) to their underlying call expressions.

    Unwraps starred spreads (``*tasks``), comprehensions, list/tuple/set literals, and simple
    name references bound to any of those via ``name_values``. A comprehension contributes a
    single representative lane (its element call), since the whole comprehension is a fan-out
    of the same operation. Duplicate Call nodes are returned only once.
    """
    calls: list[ast.Call] = []
    seen: set[int] = set()

    def visit(expr: ast.expr, depth: int) -> None:
        if depth > _MAX_AWAITABLE_RESOLVE_DEPTH:
            return
        if isinstance(expr, ast.Starred):
            visit(expr.value, depth + 1)
        elif isinstance(expr, ast.Call):
            if id(expr) not in seen:
                seen.add(id(expr))
                calls.append(expr)
        elif isinstance(expr, (ast.ListComp, ast.GeneratorExp, ast.SetComp)):
            visit(expr.elt, depth + 1)
        elif isinstance(expr, (ast.List, ast.Tuple, ast.Set)):
            for elt in expr.elts:
                visit(elt, depth + 1)
        elif isinstance(expr, ast.Name):
            bound = name_values.get(expr.id)
            if bound is not None:
                visit(bound, depth + 1)

    for a in awaitables:
        visit(a, 0)
    return calls


def _scoped_binding_ctx(ctx: "_TreeCtx") -> "_TreeCtx":
    """Return a child context whose local-function and name-binding dicts are isolated copies.

    Each statement block gets its own copy seeded from its parent, so bindings recorded while
    walking a block (incrementally, in source order — see _record_binding) stay local to that
    block: sibling if/else branches and inlined helpers cannot leak names to one another, and a
    binding is only visible to statements that follow it. Counters and other fields stay shared
    by reference so node ids remain unique across the walk.
    """
    return dataclasses.replace(ctx, local_funcs=dict(ctx.local_funcs), name_values=dict(ctx.name_values))


def _record_binding(stmt: ast.stmt, ctx: "_TreeCtx") -> None:
    """Record a nested function def or simple name binding so later statements can resolve it.

    Lets calls to local helpers and ``*tasks`` spreads passed to asyncio.gather be resolved.
    """
    if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
        ctx.local_funcs[stmt.name] = stmt
    elif isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
        ctx.name_values[stmt.targets[0].id] = stmt.value


def _build_parallel_node(
    lane_exprs: list[ast.Call],
    par_call: ast.Call,
    walk_lane: Callable[[list[ast.stmt]], list[dict]],
    ctx: "_TreeCtx",
    index: "_FileIndex",
    file_ranges: dict[str, dict],
    file_path: str,
    workflow_name: str,
) -> dict | None:
    """Build a tree ``parallel`` node from a set of lane call expressions.

    Each lane is walked back through ``walk_lane`` (the caller's own body walker) so every
    call kind — activity, human_input, execute_workflow, nested local helper — is recognised
    uniformly. Returns None when no lane yields renderable content. A comprehension yields a
    single representative lane (a fan-out).
    """
    branches: list[list[dict]] = []
    for lane_call in lane_exprs:
        lane_nodes = [n for n in walk_lane([ast.Expr(value=lane_call)]) if n.get("kind") in _RENDERABLE_KINDS]
        if lane_nodes:
            branches.append(lane_nodes)
    if not branches:
        return None
    par_idx = ctx.parallel_counter[0]
    ctx.parallel_counter[0] += 1
    cb, ce = _ast_span(par_call, index)
    return {
        "kind": "parallel",
        "id": f"{workflow_name}::parallel_{par_idx}",
        "source_range": _abs_range(file_ranges, file_path, cb, ce, line=par_call.lineno),
        "branches": branches,
    }


def _resolve(expr: ast.expr, module_ns: dict) -> Any:
    if isinstance(expr, ast.Name):
        return module_ns.get(expr.id)
    if isinstance(expr, ast.Attribute):
        obj = _resolve(expr.value, module_ns)
        if obj is None:
            return None
        try:
            return getattr(obj, expr.attr)
        except Exception:
            return None
    return None


def _resolve_call(call: ast.Call, module_ns: dict) -> Any:
    return _resolve(call.func, module_ns)


_ACTIVITY_KINDS = frozenset({"step", "human_input", "wait_condition", "dispatch", "memory_op"})


def _has_renderable_nodes(nodes: list[dict]) -> bool:
    """Return True if any top-level node is visible in the rendered graph."""
    return any(n.get("kind") in _RENDERABLE_KINDS for n in nodes)


def _block_exit_kind(stmts: list[ast.stmt]) -> Literal["return", "raise"] | None:
    """Return how a statement block terminates: 'return', 'raise', or None.

    Inspects the last statement and recurses into transparent compound statements
    (with-blocks, and if/else where both branches exit) so a return or raise nested
    inside e.g. a ``with`` is still detected.
    """
    if not stmts:
        return None
    last = stmts[-1]
    if isinstance(last, ast.Raise):
        return "raise"
    if isinstance(last, ast.Return):
        return "return"
    if isinstance(last, (ast.With, ast.AsyncWith)):
        return _block_exit_kind(last.body)
    if isinstance(last, ast.If) and last.orelse:
        true_kind = _block_exit_kind(last.body)
        false_kind = _block_exit_kind(last.orelse)
        if true_kind is not None and false_kind is not None:
            return "raise" if true_kind == "raise" and false_kind == "raise" else "return"
    return None


_BRANCH_KEYS = ("true_branch", "false_branch", "rejoin", "children", "try_body", "finally_body")


def _has_activity_nodes(nodes: list[dict]) -> bool:
    """Return True if any node (recursively) is a workflow activity.

    Used to distinguish guard-only helpers (pure conditionals / assignments)
    from helpers that contain real workflow steps.  A helper whose inlined
    tree passes _has_renderable_nodes but fails this check is treated as
    empty and replaced with a synthetic ellipsis.
    """
    for n in nodes:
        if n.get("kind") in _ACTIVITY_KINDS:
            return True
        for key in _BRANCH_KEYS:
            if _has_activity_nodes(n.get(key) or []):
                return True
        for h in n.get("handlers") or []:
            if _has_activity_nodes(h.get("body") or []):
                return True
        for branch in n.get("branches") or []:
            if _has_activity_nodes(branch):
                return True
    return False


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


def _ast_span(node: ast.expr | ast.stmt, index: _FileIndex) -> tuple[int, int]:
    """Return (begin_byte, end_byte) for the AST node using UTF-8 byte positions."""

    def to_byte(lineno: int, col: int) -> int:
        line_start = index.line_byte_starts[lineno - 1]
        return line_start + len(index.lines[lineno - 1][:col].encode("utf-8"))

    # mypy stubs declare end_lineno/end_col_offset as int | None, but ast.parse() always
    # populates them for every expr/stmt node on CPython.
    return to_byte(node.lineno, node.col_offset), to_byte(node.end_lineno, node.end_col_offset)  # type: ignore[arg-type]


@dataclass
class _TreeCtx:
    """Simplified walk context for building the v2 tree format — no edge tracking."""

    cond_counter: list[int] = field(default_factory=lambda: [0])
    human_input_counter: list[int] = field(default_factory=lambda: [0])
    dispatch_counter: list[int] = field(default_factory=lambda: [0])
    ellipsis_counter: list[int] = field(default_factory=lambda: [0])
    loop_counter: list[int] = field(default_factory=lambda: [0])
    try_counter: list[int] = field(default_factory=lambda: [0])
    parallel_counter: list[int] = field(default_factory=lambda: [0])
    wait_counter: list[int] = field(default_factory=lambda: [0])
    memory_counter: list[int] = field(default_factory=lambda: [0])
    task_counter: list[int] = field(default_factory=lambda: [0])
    raise_counter: list[int] = field(default_factory=lambda: [0])
    cls_def: ast.ClassDef | None = None
    workflow_cls: type | None = None
    visited_methods: set[str] = field(default_factory=set)
    param_types: dict[str, type] = field(default_factory=dict)
    # Nested local functions (def/async def) defined in the current scope, and simple
    # name → value bindings, so calls to local helpers and `*tasks` spreads passed to
    # asyncio.gather can be resolved. inlined_funcs guards against infinite recursion.
    local_funcs: dict[str, ast.FunctionDef | ast.AsyncFunctionDef] = field(default_factory=dict)
    name_values: dict[str, ast.expr] = field(default_factory=dict)
    inlined_funcs: frozenset[str] = field(default_factory=frozenset)


@dataclass
class _WalkCtx:
    """Walk context for _walk_body (v3 flat graph format — tracks edges as it goes)."""

    prev_id: str
    first_edge_kind: str
    between_edge_kind: str
    exit_edge_kind: str
    output_id: str
    # list[int] is intentional: the list is shared by reference across recursive _WalkCtx
    # instances, so mutations in a branch are visible to the caller — a plain int would not be.
    cond_counter: list[int] = field(default_factory=lambda: [0])
    human_input_counter: list[int] = field(default_factory=lambda: [0])
    dispatch_counter: list[int] = field(default_factory=lambda: [0])
    cls_def: ast.ClassDef | None = None
    workflow_cls: type | None = None
    visited_methods: set[str] = field(default_factory=set)
    param_types: dict[str, type] = field(default_factory=dict)


def _abs_range(file_ranges: dict[str, dict], file_path: str, begin: int, end: int, line: int = 0) -> dict:
    """Absolute byte offsets in the concatenated source blob for a per-file span."""
    fb = file_ranges.get(file_path, {}).get("begin", 0)
    return {"begin": fb + begin, "end": fb + end, "line": line}


def _make_ellipsis_node(ctx: _TreeCtx, workflow_name: str, source_range: dict) -> dict:
    ell_idx = ctx.ellipsis_counter[0]
    ctx.ellipsis_counter[0] += 1
    return {
        "kind": "ellipsis",
        "id": f"{workflow_name}::ellipsis_{ell_idx}",
        "source_range": source_range,
    }


def _register_source_file(
    file_path: str,
    source_text: str,
    sources: dict[str, str],
    file_ranges: dict[str, dict],
) -> None:
    """Append file_path to the source accumulator if not already registered."""
    if file_path in file_ranges:
        return
    if file_path not in sources:
        sources[file_path] = source_text
    current_end = max((r["end"] for r in file_ranges.values()), default=0)
    byte_len = len(sources[file_path].encode("utf-8"))
    file_ranges[file_path] = {"begin": current_end, "end": current_end + byte_len}


def _get_ast(file_path: str, sources: dict[str, str], asts: dict[str, ast.Module]) -> ast.Module:
    """Return a cached ast.Module for file_path, parsing and reading from disk as needed."""
    if file_path not in asts:
        if file_path not in sources:
            sources[file_path] = Path(file_path).read_text()
        asts[file_path] = ast.parse(sources[file_path])
    return asts[file_path]


def _build_index(source_text: str, tree: ast.Module) -> _FileIndex:
    lines = source_text.splitlines(keepends=True)
    starts: list[int] = []
    pos = 0
    for line in lines:
        starts.append(pos)
        pos += len(line.encode("utf-8"))
    fn_by_line: dict[int, ast.FunctionDef | ast.AsyncFunctionDef] = {
        n.lineno: n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    return _FileIndex(line_byte_starts=starts, lines=lines, fn_by_line=fn_by_line)


def _get_index(
    file_path: str,
    sources: dict[str, str],
    asts: dict[str, ast.Module],
    indices: dict[str, _FileIndex],
) -> _FileIndex:
    if file_path not in indices:
        tree = _get_ast(file_path, sources, asts)
        indices[file_path] = _build_index(sources[file_path], tree)
    return indices[file_path]


def _find_method_in_mro(
    workflow_cls: type,
    method_name: str,
    sources: dict[str, str],
    asts: dict[str, ast.Module],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ast.ClassDef, str, str, dict] | None:
    """Search workflow_cls.__mro__ for method_name and return its AST + context."""
    for base_cls in workflow_cls.__mro__:
        try:
            file_path = inspect.getfile(base_cls)
        except (TypeError, OSError):
            continue
        tree = _get_ast(file_path, sources, asts)
        src = sources[file_path]
        cls_def = next(
            (n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == base_cls.__name__),
            None,
        )
        if cls_def is None:
            continue
        fn = next(
            (
                n
                for n in cls_def.body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == method_name
            ),
            None,
        )
        if fn is not None:
            mod = inspect.getmodule(base_cls)
            return fn, cls_def, src, file_path, vars(mod) if mod is not None else {}
    return None


def _edge(from_id: str, to_id: str, kind: str, source_id: str, begin: int, end: int, line: int) -> dict:
    return {
        "from": from_id,
        "to": to_id,
        "source_id": source_id,
        "source_offset": begin,
        "source_length": end - begin,
        "line": line,
        "kind": kind,
    }


def _resolve_activity_span(
    resolved: Any,
    sources: dict[str, str],
    asts: dict[str, ast.Module],
    indices: dict[str, _FileIndex],
    callsite_begin: int,
    callsite_end: int,
    callsite_file: str,
) -> tuple[str, int, int]:
    """Return (source_id, begin, end) for an activity; falls back to call-site span on failure."""
    try:
        orig_func = resolved.__original_func__
        act_file = inspect.getfile(orig_func)
        target_line = orig_func.__code__.co_firstlineno
        index = _get_index(act_file, sources, asts, indices)
        fn_node = index.fn_by_line.get(target_line)
        if fn_node is not None:
            return act_file, *_ast_span(fn_node, index)
    except Exception:
        pass
    return callsite_file, callsite_begin, callsite_end


def _scan_activity_subworkflows(
    resolved_activity: Any,
    activity_node_id: str,
    sources: dict[str, str],
    asts: dict[str, ast.Module],
    indices: dict[str, _FileIndex],
) -> tuple[list[dict], list[dict]]:
    """Scan an activity's body for execute_workflow calls and emit child workflow nodes."""
    nodes: list[dict] = []
    edges: list[dict] = []
    try:
        orig_func = resolved_activity.__original_func__
        act_mod = inspect.getmodule(orig_func)
        if act_mod is None:
            return nodes, edges
        act_ns = vars(act_mod)

        act_file = inspect.getfile(orig_func)
        target_line = orig_func.__code__.co_firstlineno
        index = _get_index(act_file, sources, asts, indices)
        fn_def = index.fn_by_line.get(target_line)
        if fn_def is None:
            return nodes, edges

        for node in ast.walk(fn_def):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            func_name = (
                func.attr if isinstance(func, ast.Attribute) else (func.id if isinstance(func, ast.Name) else None)
            )
            if func_name != "execute_workflow" or not node.args:
                continue
            wf_cls = _resolve(node.args[0], act_ns)
            if wf_cls is None or not hasattr(wf_cls, "__workflows_workflow_def"):
                continue

            child_id = f"{activity_node_id}::sub_{wf_cls.__name__}"
            call_begin, call_end = _ast_span(node, index)
            nodes.append(
                {
                    "id": child_id,
                    "type": "workflow",
                    "name": wf_cls.__name__,
                    "source_id": act_file,
                    "source_offset": call_begin,
                    "source_length": call_end - call_begin,
                    "line": node.lineno,
                }
            )
            edges.append(
                {
                    "from": activity_node_id,
                    "to": child_id,
                    "source_id": act_file,
                    "source_offset": call_begin,
                    "source_length": call_end - call_begin,
                    "line": node.lineno,
                    "kind": "call",
                }
            )
    except Exception:
        pass
    return nodes, edges


def _all_subclasses(cls: type) -> list[type]:
    result = []
    for sub in cls.__subclasses__():
        result.append(sub)
        result.extend(_all_subclasses(sub))
    return result


def _activity_callees_in_method(cls: type, method_name: str) -> list[str]:
    """Return names of @activity functions awaited inside cls.method_name."""
    raw = cls.__dict__.get(method_name)
    if raw is None:
        return []
    method_obj = getattr(raw, "__func__", raw)
    try:
        source = textwrap.dedent(inspect.getsource(method_obj))
        tree = ast.parse(source)
    except Exception:
        return []

    module_globals: dict = vars(sys.modules.get(cls.__module__, type(None)))
    callees: list[str] = []
    seen: set[str] = set()

    for node in ast.walk(tree):
        if not (isinstance(node, ast.Await) and isinstance(node.value, ast.Call)):
            continue
        call = node.value
        fn: Any = None
        func = call.func
        if isinstance(func, ast.Name):
            fn = module_globals.get(func.id)
        elif isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
            mod = module_globals.get(func.value.id)
            if mod is not None:
                fn = getattr(mod, func.attr, None)
        if fn is None:
            continue
        try:
            if check_is_activity(fn) and fn.__name__ not in seen:
                callees.append(fn.__name__)
                seen.add(fn.__name__)
        except Exception:
            pass

    return callees


def _find_dispatch_callees(
    obj_name: str,
    attr_name: str,
    method_name: str,
    param_types: dict[str, type],
) -> tuple[list[str], str] | None:
    """Find @activity names called across all concrete implementations of the dispatched method.

    Returns None if no activities are found (e.g. the method is sync or calls no activities).
    """
    obj_type = param_types.get(obj_name)
    if obj_type is None:
        return None
    attr_type = getattr(obj_type, "__annotations__", {}).get(attr_name)
    if attr_type is None:
        return None

    all_callees: list[str] = []
    seen: set[str] = set()
    for sub in _all_subclasses(attr_type):
        if method_name not in sub.__dict__:
            continue
        for name in _activity_callees_in_method(sub, method_name):
            if name not in seen:
                all_callees.append(name)
                seen.add(name)

    if not all_callees:
        return None
    return all_callees, f"selected by {obj_type.__name__}.{attr_name}"


def _walk_body(
    stmts: list[ast.stmt],
    module_ns: dict,
    source_text: str,
    sources: dict[str, str],
    asts: dict[str, ast.Module],
    indices: dict[str, _FileIndex],
    file_path: str,
    workflow_name: str,
    ctx: _WalkCtx,
) -> tuple[str | None, list[dict], list[dict]]:
    """
    Walk statements collecting nodes and edges (v3 flat format).
    Returns (last_id, nodes, edges); last_id is None if the block ends with return.
    """
    if file_path not in sources:
        sources[file_path] = source_text
    index = _get_index(file_path, sources, asts, indices)

    nodes: list[dict] = []
    edges: list[dict] = []
    prev_id = ctx.prev_id
    edge_kind = ctx.first_edge_kind
    between_kind = ctx.between_edge_kind

    for stmt in stmts:
        # --- return statement (may contain an activity call) ---
        if isinstance(stmt, ast.Return):
            ret_call = None
            if stmt.value is not None:
                v = stmt.value
                if isinstance(v, ast.Await) and isinstance(v.value, ast.Call):
                    ret_call = v.value
                elif isinstance(v, ast.Call):
                    ret_call = v

            if ret_call is not None:
                resolved = _resolve_call(ret_call, module_ns)
                if resolved is not None and check_is_activity(resolved):
                    node_id = f"{workflow_name}::{resolved.__name__}@{ret_call.lineno}"
                    call_begin, call_end = _ast_span(ret_call, index)
                    act_source_id, act_begin, act_end = _resolve_activity_span(
                        resolved, sources, asts, indices, call_begin, call_end, file_path
                    )
                    nodes.append(
                        {
                            "id": node_id,
                            "type": "activity",
                            "name": resolved.__name__,
                            "source_id": act_source_id,
                            "source_offset": act_begin,
                            "source_length": act_end - act_begin,
                            "line": ret_call.lineno,
                        }
                    )
                    edges.append(
                        _edge(
                            prev_id,
                            node_id,
                            edge_kind,
                            file_path,
                            call_begin,
                            call_end,
                            ret_call.lineno,
                        )
                    )
                    edges.append(_edge(node_id, ctx.output_id, ctx.exit_edge_kind, file_path, 0, 0, stmt.lineno))
                    sub_nodes, sub_edges = _scan_activity_subworkflows(resolved, node_id, sources, asts, indices)
                    nodes.extend(sub_nodes)
                    edges.extend(sub_edges)
                    return None, nodes, edges

            ret_begin, ret_end = _ast_span(stmt, index)
            edges.append(
                _edge(
                    prev_id,
                    ctx.output_id,
                    ctx.exit_edge_kind,
                    file_path,
                    ret_begin,
                    ret_end,
                    stmt.lineno,
                )
            )
            return None, nodes, edges

        # --- conditional ---
        if isinstance(stmt, ast.If):
            cond_idx = ctx.cond_counter[0]
            ctx.cond_counter[0] += 1
            cond_id = f"{workflow_name}::cond_{cond_idx}"
            cond_begin, cond_end = _ast_span(stmt, index)
            cond_node = {
                "id": cond_id,
                "type": "conditional",
                "name": "if",
                "source_id": file_path,
                "source_offset": cond_begin,
                "source_length": cond_end - cond_begin,
                "line": stmt.lineno,
            }
            nodes.append(cond_node)
            edges.append(_edge(prev_id, cond_id, edge_kind, file_path, cond_begin, cond_end, stmt.lineno))

            # true branch
            true_last, tn, te = _walk_body(
                stmt.body,
                module_ns,
                source_text,
                sources,
                asts,
                indices,
                file_path,
                workflow_name,
                dataclasses.replace(
                    ctx,
                    prev_id=cond_id,
                    first_edge_kind="branch_true",
                    between_edge_kind="branch_sequential",
                    exit_edge_kind="branch_exit_true",
                ),
            )
            nodes.extend(tn)
            edges.extend(te)

            # false branch
            if stmt.orelse:
                false_last, fn_, fe = _walk_body(
                    stmt.orelse,
                    module_ns,
                    source_text,
                    sources,
                    asts,
                    indices,
                    file_path,
                    workflow_name,
                    dataclasses.replace(
                        ctx,
                        prev_id=cond_id,
                        first_edge_kind="branch_false",
                        between_edge_kind="branch_sequential",
                        exit_edge_kind="branch_exit_false",
                    ),
                )
                nodes.extend(fn_)
                edges.extend(fe)

            prev_id = cond_id
            edge_kind = between_kind
            continue

        # --- for / while / async-for: recurse into loop body ---
        if isinstance(stmt, (ast.For, ast.AsyncFor, ast.While)):
            dummy_exit = f"__loop_exit_{id(stmt)}"
            _, inner_nodes, inner_edges = _walk_body(
                stmt.body,
                module_ns,
                source_text,
                sources,
                asts,
                indices,
                file_path,
                workflow_name,
                dataclasses.replace(
                    ctx,
                    prev_id=prev_id,
                    first_edge_kind=edge_kind,
                    between_edge_kind=between_kind,
                    exit_edge_kind="sequential",
                    output_id=dummy_exit,
                ),
            )
            nodes.extend(inner_nodes)
            edges.extend(e for e in inner_edges if e["to"] != dummy_exit)
            if inner_nodes and inner_nodes[-1]["type"] != "conditional":
                prev_id = inner_nodes[-1]["id"]
            edge_kind = between_kind
            continue

        # --- with / async-with: recurse into body ---
        if isinstance(stmt, (ast.With, ast.AsyncWith)):
            dummy_exit = f"__with_exit_{id(stmt)}"
            _, inner_nodes, inner_edges = _walk_body(
                stmt.body,
                module_ns,
                source_text,
                sources,
                asts,
                indices,
                file_path,
                workflow_name,
                dataclasses.replace(
                    ctx,
                    prev_id=prev_id,
                    first_edge_kind=edge_kind,
                    between_edge_kind=between_kind,
                    exit_edge_kind="sequential",
                    output_id=dummy_exit,
                ),
            )
            nodes.extend(inner_nodes)
            edges.extend(e for e in inner_edges if e["to"] != dummy_exit)
            if inner_nodes:
                prev_id = inner_nodes[-1]["id"]
            edge_kind = between_kind
            continue

        # --- try/except: walk happy path (body only, skip handlers) ---
        if isinstance(stmt, ast.Try):
            try_last, try_nodes, try_edges = _walk_body(
                stmt.body,
                module_ns,
                source_text,
                sources,
                asts,
                indices,
                file_path,
                workflow_name,
                dataclasses.replace(
                    ctx,
                    prev_id=prev_id,
                    first_edge_kind=edge_kind,
                    between_edge_kind=between_kind,
                ),
            )
            nodes.extend(try_nodes)
            edges.extend(try_edges)
            if try_last is not None:
                prev_id = try_last
            edge_kind = between_kind
            continue

        # --- activity / sub-workflow call ---
        call = _extract_call(stmt)
        if call is None:
            continue

        # human_input: await self.wait_for_input(...)
        if (
            isinstance(call.func, ast.Attribute)
            and call.func.attr == "wait_for_input"
            and isinstance(call.func.value, ast.Name)
            and call.func.value.id == "self"
        ):
            idx = ctx.human_input_counter[0]
            ctx.human_input_counter[0] += 1
            node_id = f"{workflow_name}::human_input_{idx}"
            call_begin, call_end = _ast_span(call, index)
            nodes.append(
                {
                    "id": node_id,
                    "type": "human_input",
                    "name": "human_input",
                    "source_id": file_path,
                    "source_offset": call_begin,
                    "source_length": call_end - call_begin,
                    "line": call.lineno,
                }
            )
            edges.append(_edge(prev_id, node_id, edge_kind, file_path, call_begin, call_end, call.lineno))
            prev_id = node_id
            edge_kind = between_kind
            continue

        # --- helper method inlining: self.method_name(...) ---
        if (
            ctx.workflow_cls is not None
            and isinstance(call.func, ast.Attribute)
            and isinstance(call.func.value, ast.Name)
            and call.func.value.id == "self"
            and call.func.attr != "wait_for_input"
        ):
            method_name = call.func.attr
            if method_name not in ctx.visited_methods:
                result = _find_method_in_mro(ctx.workflow_cls, method_name, sources, asts)
                if result is not None:
                    fn_def, mixin_cls_def, mixin_src, mixin_file, mixin_ns = result
                    helper_param_types: dict[str, type] = {}
                    try:
                        for base in ctx.workflow_cls.__mro__:
                            if method_name in base.__dict__:
                                raw = base.__dict__[method_name]
                                method_obj = getattr(raw, "__func__", raw)
                                hints = get_type_hints(method_obj)
                                helper_param_types = {k: v for k, v in hints.items() if k != "return"}
                                break
                    except Exception:
                        pass
                    helper_exit_id = f"{workflow_name}::helper_{method_name}::__exit__"
                    helper_last, h_nodes, h_edges = _walk_body(
                        fn_def.body,
                        mixin_ns,
                        mixin_src,
                        sources,
                        asts,
                        indices,
                        mixin_file,
                        f"{workflow_name}::helper_{method_name}",
                        dataclasses.replace(
                            ctx,
                            prev_id=prev_id,
                            first_edge_kind=edge_kind,
                            between_edge_kind="sequential",
                            exit_edge_kind="sequential",
                            output_id=helper_exit_id,
                            cls_def=mixin_cls_def,
                            visited_methods=ctx.visited_methods | {method_name},
                            param_types=helper_param_types,
                        ),
                    )
                    h_edges = [e for e in h_edges if e["to"] != helper_exit_id]
                    nodes.extend(h_nodes)
                    edges.extend(h_edges)
                    if helper_last is not None:
                        prev_id = helper_last
                    elif h_nodes:
                        prev_id = h_nodes[-1]["id"]
                    edge_kind = between_kind
                    continue

        # sub-workflow: execute_workflow(WorkflowCls, ...)
        func = call.func
        func_name = func.attr if isinstance(func, ast.Attribute) else (func.id if isinstance(func, ast.Name) else None)
        if func_name == "execute_workflow" and call.args:
            wf_cls = _resolve(call.args[0], module_ns)
            if wf_cls is not None and hasattr(wf_cls, "__workflows_workflow_def"):
                node_id = f"{workflow_name}::{wf_cls.__name__}@{call.lineno}"
                call_begin, call_end = _ast_span(call, index)
                nodes.append(
                    {
                        "id": node_id,
                        "type": "workflow",
                        "name": wf_cls.__name__,
                        "source_id": file_path,
                        "source_offset": call_begin,
                        "source_length": call_end - call_begin,
                        "line": call.lineno,
                    }
                )
                edges.append(_edge(prev_id, node_id, edge_kind, file_path, call_begin, call_end, call.lineno))
                prev_id = node_id
                edge_kind = between_kind
                continue

        # --- protocol dispatch: ctx.attr.method(...) ---
        if (
            ctx.param_types
            and isinstance(call.func, ast.Attribute)
            and isinstance(call.func.value, ast.Attribute)
            and isinstance(call.func.value.value, ast.Name)
        ):
            obj_name = call.func.value.value.id
            attr_name = call.func.value.attr
            method_name_d = call.func.attr
            dr = _find_dispatch_callees(obj_name, attr_name, method_name_d, ctx.param_types)
            if dr is not None:
                callees, dispatch_label = dr
                idx = ctx.dispatch_counter[0]
                ctx.dispatch_counter[0] += 1
                node_id = f"{workflow_name}::dispatch_{idx}"
                call_begin, call_end = _ast_span(call, index)
                nodes.append(
                    {
                        "id": node_id,
                        "type": "dispatch",
                        "name": f"{attr_name}.{method_name_d}",
                        "callees": callees,
                        "dispatch_label": dispatch_label,
                        "source_id": file_path,
                        "source_offset": call_begin,
                        "source_length": call_end - call_begin,
                        "line": call.lineno,
                    }
                )
                edges.append(_edge(prev_id, node_id, edge_kind, file_path, call_begin, call_end, call.lineno))
                prev_id = node_id
                edge_kind = between_kind
                continue

        resolved = _resolve_call(call, module_ns)
        if resolved is None:
            continue

        if not check_is_activity(resolved):
            continue

        node_id = f"{workflow_name}::{resolved.__name__}@{call.lineno}"
        call_begin, call_end = _ast_span(call, index)
        act_source_id, act_begin, act_end = _resolve_activity_span(
            resolved, sources, asts, indices, call_begin, call_end, file_path
        )

        nodes.append(
            {
                "id": node_id,
                "type": "activity",
                "name": resolved.__name__,
                "source_id": act_source_id,
                "source_offset": act_begin,
                "source_length": act_end - act_begin,
                "line": call.lineno,
            }
        )
        edges.append(_edge(prev_id, node_id, edge_kind, file_path, call_begin, call_end, call.lineno))
        sub_nodes, sub_edges = _scan_activity_subworkflows(resolved, node_id, sources, asts, indices)
        nodes.extend(sub_nodes)
        edges.extend(sub_edges)
        prev_id = node_id
        edge_kind = between_kind

    return prev_id, nodes, edges


def _extract_hi_label(call: ast.Call) -> str | None:
    """Extract the label string from a wait_for_input(label=...) call."""
    for kw in call.keywords:
        if kw.arg == "label":
            try:
                return str(ast.literal_eval(kw.value))
            except ValueError:
                return ast.unparse(kw.value)
    return None


# ---------------------------------------------------------------------------
# ActivityResolver — parameterises _walk_body_tree for dynamic vs static mode
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _InlineTarget:
    fn_def: ast.FunctionDef | ast.AsyncFunctionDef
    cls_def: ast.ClassDef
    file_path: str
    resolver: "ActivityResolver"
    param_types: dict[str, type]


def _extract_wf_arg(call: ast.Call) -> ast.expr | None:
    return call.args[0] if call.args else next((kw.value for kw in call.keywords if kw.arg == "workflow"), None)


class ActivityResolver:
    __slots__ = ()

    def resolve_activity(
        self,
        call: ast.Call,
        sources: dict[str, str],
        asts: dict[str, ast.Module],
    ) -> str | None:
        raise NotImplementedError

    def find_method_to_inline(
        self,
        method_name: str,
        sources: dict[str, str],
        asts: dict[str, ast.Module],
    ) -> _InlineTarget | None:
        raise NotImplementedError

    def resolve_workflow_name(self, call: ast.Call) -> str | None:
        raise NotImplementedError

    def resolve_workflow_file(self, call: ast.Call) -> str | None:
        """Absolute path of the child workflow class's source file, if resolvable.

        Used to link a child_workflow node to the child's graph. The base
        implementation returns ``None`` (no link); resolvers with enough symbol
        information — the static resolver's import table or the dynamic
        resolver's imported module namespace — can resolve the defining file.
        """
        return None


class _DynamicResolver(ActivityResolver):
    __slots__ = ("_module_ns", "_workflow_cls")

    def __init__(self, module_ns: dict, workflow_cls: type | None = None) -> None:
        self._module_ns = module_ns
        self._workflow_cls = workflow_cls

    def resolve_activity(self, call: ast.Call, sources: dict[str, str], asts: dict[str, ast.Module]) -> str | None:
        resolved = _resolve_call(call, self._module_ns)
        if resolved is not None and check_is_activity(resolved):
            return str(resolved.__name__)
        return None

    def find_method_to_inline(
        self, method_name: str, sources: dict[str, str], asts: dict[str, ast.Module]
    ) -> _InlineTarget | None:
        if self._workflow_cls is None:
            return None
        result = _find_method_in_mro(self._workflow_cls, method_name, sources, asts)
        if result is None:
            return None
        fn_def, mixin_cls_def, _src, mixin_file, mixin_ns = result
        param_types: dict[str, type] = {}
        try:
            for base in self._workflow_cls.__mro__:
                if method_name in base.__dict__:
                    raw = base.__dict__[method_name]
                    method_obj = getattr(raw, "__func__", raw)
                    hints = get_type_hints(method_obj)
                    param_types = {k: v for k, v in hints.items() if k != "return"}
                    break
        except Exception:
            pass
        return _InlineTarget(
            fn_def=fn_def,
            cls_def=mixin_cls_def,
            file_path=mixin_file,
            resolver=_DynamicResolver(module_ns=mixin_ns, workflow_cls=self._workflow_cls),
            param_types=param_types,
        )

    def resolve_workflow_name(self, call: ast.Call) -> str | None:
        wf_arg = _extract_wf_arg(call)
        if wf_arg is None:
            return None
        wf_cls = _resolve(wf_arg, self._module_ns)
        if wf_cls is not None and hasattr(wf_cls, "__workflows_workflow_def"):
            return str(wf_cls.__name__)
        return None

    def resolve_workflow_file(self, call: ast.Call) -> str | None:
        wf_arg = _extract_wf_arg(call)
        if wf_arg is None:
            return None
        wf_cls = _resolve(wf_arg, self._module_ns)
        if wf_cls is None or not hasattr(wf_cls, "__workflows_workflow_def"):
            return None
        try:
            return str(Path(inspect.getfile(wf_cls)).resolve())
        except TypeError:
            return None


class _StaticResolver(ActivityResolver):
    __slots__ = ("_symbols", "_symbol_names", "_file_resolver", "_cls_def", "_file_path")

    def __init__(
        self,
        symbols: dict[str, str],
        symbol_names: dict[str, str],
        file_resolver: Callable[[str], str | None],
        cls_def: ast.ClassDef,
        file_path: str,
    ) -> None:
        self._symbols = symbols
        self._symbol_names = symbol_names
        self._file_resolver = file_resolver
        self._cls_def = cls_def
        self._file_path = file_path

    def resolve_activity(self, call: ast.Call, sources: dict[str, str], asts: dict[str, ast.Module]) -> str | None:
        fn_name = _resolve_call_fn_name(call)
        if not fn_name or fn_name not in self._symbols:
            return None
        fn_def = _lookup_fn_in_file(fn_name, self._symbols[fn_name], self._file_resolver, sources, asts)
        if fn_def is not None and _has_activity_decorator(fn_def):
            return fn_name
        return None

    def find_method_to_inline(
        self, method_name: str, sources: dict[str, str], asts: dict[str, ast.Module]
    ) -> _InlineTarget | None:
        fn = next(
            (
                n
                for n in self._cls_def.body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == method_name
            ),
            None,
        )
        if fn is None:
            return None
        return _InlineTarget(
            fn_def=fn,
            cls_def=self._cls_def,
            file_path=self._file_path,
            resolver=self,
            param_types={},
        )

    def _resolve_workflow_target(self, call: ast.Call) -> tuple[str, str | None] | None:
        """Resolve a child workflow reference to (class name, defining file path).

        The class name is the original ``__name__`` Atlas registers by, not the
        local import alias; the file path is the candidate module, when known.
        """
        wf_arg = _extract_wf_arg(call)
        if wf_arg is None:
            return None
        if isinstance(wf_arg, ast.Name):
            return self._symbol_names.get(wf_arg.id, wf_arg.id), self._symbols.get(wf_arg.id)
        if isinstance(wf_arg, ast.Attribute):
            # `module.WorkflowClass` — attribute access uses the real class name;
            # resolve the file via the module alias when it is a known import.
            if isinstance(wf_arg.value, ast.Name):
                candidate = self._symbols.get(wf_arg.value.id)
                if candidate is not None:
                    return wf_arg.attr, candidate
            return wf_arg.attr, self._symbols.get(wf_arg.attr)
        return None

    def resolve_workflow_name(self, call: ast.Call) -> str | None:
        target = self._resolve_workflow_target(call)
        return target[0] if target is not None else None

    def resolve_workflow_file(self, call: ast.Call) -> str | None:
        target = self._resolve_workflow_target(call)
        if target is None:
            return None
        name, candidate = target
        if candidate is None:
            return None
        src = self._file_resolver(candidate)
        if src is None:
            return None
        try:
            tree = ast.parse(src)
        except SyntaxError:
            return None
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name == name and _is_workflow_cls_def(node):
                return candidate
        return None


def _walk_body_tree(
    stmts: list[ast.stmt],
    resolver: ActivityResolver,
    sources: dict[str, str],
    asts: dict[str, ast.Module],
    indices: dict[str, _FileIndex],
    file_path: str,
    workflow_name: str,
    ctx: _TreeCtx,
    file_ranges: dict[str, dict],
) -> list[dict]:
    """Walk statements and return tree nodes.

    Resolution strategy (activity detection, method inlining, execute_workflow)
    is delegated to ``resolver``, allowing the same walker to be used for both
    dynamic (imported module) and static (pure-AST) analysis.
    """
    src = sources.get(file_path, "")
    if not src:
        return []
    _register_source_file(file_path, src, sources, file_ranges)
    index = _get_index(file_path, sources, asts, indices)
    result: list[dict] = []

    ctx = _scoped_binding_ctx(ctx)

    def _walk_lane(body: list[ast.stmt]) -> list[dict]:
        return _walk_body_tree(body, resolver, sources, asts, indices, file_path, workflow_name, ctx, file_ranges)

    for idx, stmt in enumerate(stmts):
        _record_binding(stmt, ctx)

        # --- return: check for return await act() before stopping ---
        if isinstance(stmt, ast.Return):
            if stmt.value is not None:
                v = stmt.value
                ret_call: ast.Call | None = None
                if isinstance(v, ast.Await) and isinstance(v.value, ast.Call):
                    ret_call = v.value
                elif isinstance(v, ast.Call):
                    ret_call = v
                if ret_call is not None:
                    name = resolver.resolve_activity(ret_call, sources, asts)
                    if name is not None:
                        cb, ce = _ast_span(ret_call, index)
                        result.append(
                            {
                                "kind": "step",
                                "id": f"{workflow_name}::{name}@{ret_call.lineno}",
                                "label": name,
                                "source_range": _abs_range(file_ranges, file_path, cb, ce, line=ret_call.lineno),
                            }
                        )
            return result

        # --- raise: terminates the block as an error exit ---
        if isinstance(stmt, ast.Raise):
            raise_idx = ctx.raise_counter[0]
            ctx.raise_counter[0] += 1
            cb, ce = _ast_span(stmt, index)
            label = ast.unparse(stmt.exc) if stmt.exc is not None else "raise"
            if len(label) > 60:
                label = label[:59] + "…"
            result.append(
                {
                    "kind": "raise",
                    "id": f"{workflow_name}::raise_{raise_idx}",
                    "label": label,
                    "source_range": _abs_range(file_ranges, file_path, cb, ce, line=stmt.lineno),
                }
            )
            return result

        # --- conditional ---
        if isinstance(stmt, ast.If):
            cond_idx = ctx.cond_counter[0]
            ctx.cond_counter[0] += 1
            cb, ce = _ast_span(stmt, index)
            true_kind = _block_exit_kind(stmt.body)
            false_kind = _block_exit_kind(stmt.orelse)
            true_exits = true_kind is not None
            false_exits = false_kind is not None
            true_branch = _walk_lane(stmt.body)
            false_branch = _walk_lane(stmt.orelse if stmt.orelse else [])
            sr = _abs_range(file_ranges, file_path, cb, ce, line=stmt.lineno)
            if not true_exits and not _has_renderable_nodes(true_branch):
                true_branch = [_make_ellipsis_node(ctx, workflow_name, sr)]
            if stmt.orelse and not false_exits and not _has_renderable_nodes(false_branch):
                false_branch = [_make_ellipsis_node(ctx, workflow_name, sr)]
            rejoin = _walk_body_tree(
                stmts[idx + 1 :], resolver, sources, asts, indices, file_path, workflow_name, ctx, file_ranges
            )
            result.append(
                {
                    "kind": "conditional",
                    "id": f"{workflow_name}::cond_{cond_idx}",
                    "label": ast.unparse(stmt.test),
                    "source_range": sr,
                    "true_branch": true_branch,
                    "true_exits": true_exits,
                    "true_exit_error": true_kind == "raise",
                    "false_branch": false_branch,
                    "false_exits": false_exits,
                    "false_exit_error": false_kind == "raise",
                    "rejoin": rejoin,
                }
            )
            return result

        # --- for / async for / while ---
        if isinstance(stmt, (ast.For, ast.AsyncFor, ast.While)):
            cb, ce = _ast_span(stmt, index)
            if isinstance(stmt, ast.While):
                raw_label = f"while {ast.unparse(stmt.test)}"
            else:
                async_prefix = "async " if isinstance(stmt, ast.AsyncFor) else ""
                raw_label = f"{async_prefix}for {ast.unparse(stmt.target)} in {ast.unparse(stmt.iter)}"
            label = raw_label if len(raw_label) <= 60 else raw_label[:59] + "…"
            children = _walk_lane(stmt.body)
            sr = _abs_range(file_ranges, file_path, cb, ce, line=stmt.lineno)
            if not any(c["kind"] in _RENDERABLE_KINDS for c in children):
                children = [_make_ellipsis_node(ctx, workflow_name, sr)] + children
            loop_idx = ctx.loop_counter[0]
            ctx.loop_counter[0] += 1
            result.append(
                {
                    "kind": "loop",
                    "id": f"{workflow_name}::loop_{loop_idx}",
                    "label": label,
                    "source_range": _abs_range(file_ranges, file_path, cb, ce, line=stmt.lineno),
                    "children": children,
                }
            )
            continue

        # --- with / async with: transparent ---
        if isinstance(stmt, (ast.With, ast.AsyncWith)):
            result.extend(_walk_lane(stmt.body))
            continue

        # --- try / except ---
        if isinstance(stmt, ast.Try):
            cb, ce = _ast_span(stmt, index)
            try_idx = ctx.try_counter[0]
            ctx.try_counter[0] += 1
            try_body = _walk_lane(stmt.body)
            sr = _abs_range(file_ranges, file_path, cb, ce, line=stmt.lineno)
            if stmt.body and not any(c["kind"] in _RENDERABLE_KINDS for c in try_body):
                try_body = [_make_ellipsis_node(ctx, workflow_name, sr)]
            handlers = [
                {
                    "exception_type": ast.unparse(h.type) if h.type else None,
                    "body": _walk_lane(h.body),
                }
                for h in stmt.handlers
            ]
            finally_body = _walk_lane(stmt.finalbody) if stmt.finalbody else []
            result.append(
                {
                    "kind": "try_except",
                    "id": f"{workflow_name}::try_{try_idx}",
                    "source_range": sr,
                    "try_body": try_body,
                    "handlers": handlers,
                    "finally_body": finally_body,
                }
            )
            continue

        call = _extract_call(stmt)
        if call is None:
            logger.debug("unrecognised stmt %s", type(stmt).__name__)
            continue

        # --- create_task / ensure_future unwrapping ---
        # A child workflow spawned via create_task/ensure_future is
        # fire-and-forget (not awaited); record that for execute_workflow below.
        # `await asyncio.create_task(...)` is awaited, so it is not fire-and-forget.
        call_is_awaited = isinstance(stmt, (ast.Expr, ast.Assign, ast.AnnAssign)) and isinstance(
            getattr(stmt, "value", None), ast.Await
        )
        fire_and_forget = False
        if (
            isinstance(call.func, ast.Attribute)
            and call.func.attr in ("create_task", "ensure_future")
            and len(call.args) == 1
            and isinstance(call.args[0], ast.Call)
        ):
            fire_and_forget = not call_is_awaited
            call = call.args[0]

        # --- human_input: await self.wait_for_input(...) ---
        if (
            isinstance(call.func, ast.Attribute)
            and call.func.attr == "wait_for_input"
            and isinstance(call.func.value, ast.Name)
            and call.func.value.id == "self"
        ):
            hi_idx = ctx.human_input_counter[0]
            ctx.human_input_counter[0] += 1
            cb, ce = _ast_span(call, index)
            result.append(
                {
                    "kind": "human_input",
                    "id": f"{workflow_name}::human_input_{hi_idx}",
                    "label": _extract_hi_label(call) or "human_input",
                    "source_range": _abs_range(file_ranges, file_path, cb, ce, line=call.lineno),
                }
            )
            continue

        # --- helper method inlining: self.method(...) ---
        if (
            isinstance(call.func, ast.Attribute)
            and isinstance(call.func.value, ast.Name)
            and call.func.value.id == "self"
            and call.func.attr != "wait_for_input"
        ):
            method_name = call.func.attr
            if method_name not in ctx.visited_methods:
                target = resolver.find_method_to_inline(method_name, sources, asts)
                if target is not None:
                    inlined = _walk_body_tree(
                        target.fn_def.body,
                        target.resolver,
                        sources,
                        asts,
                        indices,
                        target.file_path,
                        f"{workflow_name}::helper_{method_name}",
                        _TreeCtx(
                            cond_counter=ctx.cond_counter,
                            human_input_counter=ctx.human_input_counter,
                            dispatch_counter=ctx.dispatch_counter,
                            ellipsis_counter=ctx.ellipsis_counter,
                            loop_counter=ctx.loop_counter,
                            try_counter=ctx.try_counter,
                            raise_counter=ctx.raise_counter,
                            cls_def=target.cls_def,
                            workflow_cls=ctx.workflow_cls,
                            visited_methods=ctx.visited_methods | {method_name},
                            param_types=target.param_types,
                        ),
                        file_ranges,
                    )
                    if _has_renderable_nodes(inlined) and _has_activity_nodes(inlined):
                        result.extend(inlined)
                    else:
                        cb, ce = _ast_span(call, index)
                        sr = _abs_range(file_ranges, file_path, cb, ce, line=call.lineno)
                        result.append(_make_ellipsis_node(ctx, workflow_name, sr))
                else:
                    cb, ce = _ast_span(call, index)
                    sr = _abs_range(file_ranges, file_path, cb, ce, line=call.lineno)
                    result.append(_make_ellipsis_node(ctx, workflow_name, sr))
            continue

        # --- nested local function inlining ---
        if (
            isinstance(call.func, ast.Name)
            and call.func.id in ctx.local_funcs
            and call.func.id not in ctx.inlined_funcs
        ):
            fn_def = ctx.local_funcs[call.func.id]
            inlined = _walk_body_tree(
                fn_def.body,
                resolver,
                sources,
                asts,
                indices,
                file_path,
                workflow_name,
                dataclasses.replace(ctx, inlined_funcs=ctx.inlined_funcs | {call.func.id}),
                file_ranges,
            )
            if _has_renderable_nodes(inlined) and _has_activity_nodes(inlined):
                result.extend(inlined)
            continue

        func_name = (
            call.func.attr
            if isinstance(call.func, ast.Attribute)
            else (call.func.id if isinstance(call.func, ast.Name) else None)
        )

        # --- sub-workflow: execute_workflow(WorkflowCls, ...) ---
        if func_name == "execute_workflow":
            wf_name = resolver.resolve_workflow_name(call)
            cb, ce = _ast_span(call, index)
            if wf_name is not None:
                cw_node: dict = {
                    "kind": "step",
                    "id": f"{workflow_name}::{wf_name}@{call.lineno}",
                    "label": wf_name,
                    "child_workflow": True,
                    "source_range": _abs_range(file_ranges, file_path, cb, ce, line=call.lineno),
                }
                wf_file = resolver.resolve_workflow_file(call)
                if wf_file is not None:
                    # Child is a resolvable workflow → link the node to its graph.
                    cw_node["child_workflow_id"] = wf_name
                    cw_node["child_workflow_file"] = wf_file
                if fire_and_forget:
                    cw_node["async"] = True
                result.append(cw_node)
            else:
                sr = _abs_range(file_ranges, file_path, cb, ce, line=call.lineno)
                result.append(_make_ellipsis_node(ctx, workflow_name, sr))
            continue

        # --- continue_as_new: terminates the branch ---
        if func_name == "continue_as_new":
            cb, ce = _ast_span(call, index)
            result.append(
                {
                    "kind": "step",
                    "id": f"{workflow_name}::continue_as_new@{call.lineno}",
                    "label": "continue_as_new",
                    "source_range": _abs_range(file_ranges, file_path, cb, ce, line=call.lineno),
                }
            )
            return result

        # --- wait_condition ---
        if isinstance(call.func, ast.Attribute) and call.func.attr == "wait_condition":
            wait_idx = ctx.wait_counter[0]
            ctx.wait_counter[0] += 1
            cb, ce = _ast_span(call, index)
            try:
                label = ast.unparse(call.args[0]) if call.args else "wait_condition"
                if call.args and isinstance(call.args[0], ast.Lambda):
                    label = ast.unparse(call.args[0].body)
            except Exception:
                label = "wait_condition"
            result.append(
                {
                    "kind": "wait_condition",
                    "id": f"{workflow_name}::wait_{wait_idx}",
                    "label": label,
                    "source_range": _abs_range(file_ranges, file_path, cb, ce, line=call.lineno),
                }
            )
            continue

        # --- execute_activities_in_parallel ---
        if func_name == "execute_activities_in_parallel":
            lane_exprs: list[ast.Call] = []
            if call.args and isinstance(call.args[0], ast.List):
                lane_exprs = _collect_lane_call_exprs(call.args[0].elts, ctx.name_values)
            par_node = _build_parallel_node(
                lane_exprs, call, _walk_lane, ctx, index, file_ranges, file_path, workflow_name
            )
            if par_node is not None:
                result.append(par_node)
            continue

        # --- asyncio.gather as parallel ---
        if (
            isinstance(call.func, ast.Attribute)
            and call.func.attr == "gather"
            and isinstance(call.func.value, ast.Name)
            and call.func.value.id == "asyncio"
        ):
            lane_exprs = _collect_lane_call_exprs(call.args, ctx.name_values)
            par_node = _build_parallel_node(
                lane_exprs, call, _walk_lane, ctx, index, file_ranges, file_path, workflow_name
            )
            if par_node is not None:
                result.append(par_node)
            continue

        # --- memory ops ---
        if isinstance(call.func, ast.Attribute) and call.func.attr in _MEMORY_OPS:
            mem_idx = ctx.memory_counter[0]
            ctx.memory_counter[0] += 1
            op = "save" if func_name == "save_memory" else ("load_history" if func_name == "load_history" else "load")
            cb, ce = _ast_span(call, index)
            result.append(
                {
                    "kind": "memory_op",
                    "id": f"{workflow_name}::memory_{mem_idx}",
                    "label": func_name,
                    "op": op,
                    "source_range": _abs_range(file_ranges, file_path, cb, ce, line=call.lineno),
                }
            )
            continue

        # --- activity step recognition ---
        name = resolver.resolve_activity(call, sources, asts)
        if name is not None:
            cb, ce = _ast_span(call, index)
            result.append(
                {
                    "kind": "step",
                    "id": f"{workflow_name}::{name}@{call.lineno}",
                    "label": name,
                    "source_range": _abs_range(file_ranges, file_path, cb, ce, line=call.lineno),
                }
            )
            continue

        # --- activities awaited inside a larger expression, e.g. results.append(await act()) ---
        for awaited in _awaited_calls_in_order(stmt):
            awaited_name = resolver.resolve_activity(awaited, sources, asts)
            if awaited_name is not None:
                cb, ce = _ast_span(awaited, index)
                result.append(
                    {
                        "kind": "step",
                        "id": f"{workflow_name}::{awaited_name}@{awaited.lineno}:{awaited.col_offset}",
                        "label": awaited_name,
                        "source_range": _abs_range(file_ranges, file_path, cb, ce, line=awaited.lineno),
                    }
                )

    return result


def _resolve_call_fn_name(call: ast.Call) -> str | None:
    """Return the simple (leaf) name of the called function, or None."""
    func = call.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _lookup_fn_in_file(
    fn_name: str,
    file_path: str,
    resolver: Callable[[str], str | None],
    sources: dict[str, str],
    asts: dict[str, ast.Module],
) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    """Find a function definition by name in a file, resolving it lazily via resolver."""
    if file_path not in sources:
        src = resolver(file_path)
        if src is None:
            return None
        sources[file_path] = src
    if file_path not in asts:
        try:
            asts[file_path] = ast.parse(sources[file_path])
        except SyntaxError:
            return None
    for node in ast.walk(asts[file_path]):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == fn_name:
            return node
    return None


_HANDLER_ATTRS: frozenset[str] = frozenset({"signal", "update", "query"})


def _handler_name(node: ast.FunctionDef | ast.AsyncFunctionDef, dec: ast.expr) -> str:
    """Return the decorator's name= kwarg value if present, else the method name."""
    if isinstance(dec, ast.Call):
        for kw in dec.keywords:
            if kw.arg == "name":
                try:
                    return str(ast.literal_eval(kw.value))
                except (ValueError, SyntaxError):
                    return ast.unparse(kw.value)
    return node.name


def _handler_param_type(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str | None:
    """Return the annotation of the first non-self parameter, or None."""
    params = [a for a in (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs) if a.arg != "self"]
    if params and params[0].annotation is not None:
        return ast.unparse(params[0].annotation)
    return None


def _handler_return_type(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str | None:
    """Return the function's return annotation, or None."""
    return ast.unparse(node.returns) if node.returns is not None else None


def _scan_class_handlers(
    cls_def: ast.ClassDef, index: _FileIndex, file_offset: int = 0
) -> tuple[list[dict], list[dict], list[dict]]:
    """Scan a class AST for @workflow.signal(), @workflow.update(), @workflow.query() methods."""
    signals: list[dict] = []
    updates: list[dict] = []
    queries: list[dict] = []
    by_kind = {"signal": signals, "update": updates, "query": queries}
    for node in cls_def.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for dec in node.decorator_list:
            dec_inner = dec.func if isinstance(dec, ast.Call) else dec
            if not isinstance(dec_inner, ast.Attribute) or dec_inner.attr not in _HANDLER_ATTRS:
                continue
            kind = dec_inner.attr
            begin, end = _ast_span(node, index)
            by_kind[kind].append(
                {
                    "kind": kind,
                    "name": _handler_name(node, dec),
                    "param_type": _handler_param_type(node),
                    "return_type": _handler_return_type(node),
                    "source_range": {"begin": file_offset + begin, "end": file_offset + end},
                }
            )
            break
    return signals, updates, queries


# Marker attribute (set by the @workflow.signal/update/query decorators) -> handler kind.
_HANDLER_DEF_ATTRS: dict[str, str] = {
    "__wf_signal_def": "signal",
    "__wf_update_def": "update",
    "__wf_query_def": "query",
}


def _format_runtime_type(annotation: object) -> str | None:
    """Render a resolved type hint as the same display string the AST scanner emits."""
    if annotation is None or annotation is type(None):
        return "None"
    if isinstance(annotation, type):
        return annotation.__name__
    return str(annotation).replace("typing.", "")


def _collect_class_handlers_runtime(
    workflow_cls: type, cls_def: ast.ClassDef, index: _FileIndex
) -> tuple[list[dict], list[dict], list[dict]]:
    """Collect signal/update/query handlers from the live class via decorator metadata.

    Unlike _scan_class_handlers (static AST), this reads the authoritative runtime markers
    the decorators stamp on each handler wrapper, so it resolves dynamic handler names and
    sees handlers inherited from base classes. Source ranges are attached only for handlers
    defined directly in this class' file; inherited handlers carry no range.
    """
    signals: list[dict] = []
    updates: list[dict] = []
    queries: list[dict] = []
    by_kind = {"signal": signals, "update": updates, "query": queries}

    ast_methods: dict[str, ast.FunctionDef | ast.AsyncFunctionDef] = {
        node.name: node for node in cls_def.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    seen: set[int] = set()
    for attr_name in dir(workflow_cls):
        try:
            member = getattr(workflow_cls, attr_name)
        except Exception:
            continue
        if id(member) in seen:
            continue

        for def_attr, kind in _HANDLER_DEF_ATTRS.items():
            handler_def = getattr(member, def_attr, None)
            if handler_def is None:
                continue
            seen.add(id(member))

            meta = getattr(member, "__wf_handler_meta", None)
            if meta is not None and meta.is_internal:
                break

            original = meta.original_func if meta is not None else member

            param_type: str | None = None
            if meta is not None and meta.user_params_dict:
                param_type = _format_runtime_type(next(iter(meta.user_params_dict.values())))

            try:
                return_type = _format_runtime_type(get_type_hints(original).get("return"))
            except Exception:
                return_type = None

            entry: dict = {
                "kind": kind,
                "name": handler_def.name,
                "param_type": param_type,
                "return_type": return_type,
            }
            ast_node = ast_methods.get(getattr(original, "__name__", ""))
            if ast_node is not None:
                begin, end = _ast_span(ast_node, index)
                entry["source_range"] = {"begin": begin, "end": end}

            by_kind[kind].append(entry)
            break

    def _sort_key(entry: dict) -> tuple[int, object]:
        sr = entry.get("source_range")
        return (0, sr["begin"]) if sr is not None else (1, entry["name"])

    for handlers in (signals, updates, queries):
        handlers.sort(key=_sort_key)

    return signals, updates, queries


class GraphValidationError(ValueError):
    pass


def _apply_child_workflow_fields(flat: dict, tree_node: dict) -> dict:
    """Promote a step flat node to a child_workflow node, copying link fields.

    execute_workflow calls are emitted as ``step`` tree nodes tagged with
    ``child_workflow`` so they reuse the normal step wiring; here that tag is
    turned into the child_workflow wire type plus the optional cross-file
    navigation fields and the fire-and-forget ``async`` flag.
    """
    if not tree_node.get("child_workflow"):
        return flat
    flat["type"] = "child_workflow"
    if "child_workflow_id" in tree_node:
        flat["child_workflow_id"] = tree_node["child_workflow_id"]
    if "child_workflow_file" in tree_node:
        flat["child_workflow_file"] = tree_node["child_workflow_file"]
    if tree_node.get("async"):
        flat["async"] = True
    return flat


def _flatten_tree(
    tree_nodes: list[dict],
    wf_name: str,
    ep_name: str | None,
    ep_begin: int | None,
    ep_end: int | None,
    ep_line: int | None,
    output_type: str | None,
    file_ranges: dict[str, dict],
) -> tuple[list[dict], list[dict]]:
    """Convert hierarchical tree from _walk_body_tree into flat nodes + edges."""
    flat_nodes: list[dict] = []
    flat_edges: list[dict] = []
    seen_edge_ids: set[str] = set()
    seen_edge_pairs: set[tuple[str, str]] = set()
    seen_node_ids: set[str] = set()
    conditional_ids: set[str] = set()
    # Nodes that are themselves terminal exits (raise outputs + early-exit outputs).
    # A branch/body ending in one of these is already terminated, so it is not
    # re-wired to a merge sink or the normal workflow output.
    terminal_exit_ids: set[str] = set()

    def add_node(node: dict) -> None:
        if node["id"] not in seen_node_ids:
            seen_node_ids.add(node["id"])
            flat_nodes.append(node)

    def add_edge(edge: dict) -> None:
        if edge["from"] == edge["to"]:
            return
        if edge["id"] not in seen_edge_ids:
            seen_edge_ids.add(edge["id"])
            seen_edge_pairs.add((edge["from"], edge["to"]))
            flat_edges.append(edge)

    def has_edge_between(from_id: str, to_id: str) -> bool:
        return (from_id, to_id) in seen_edge_pairs

    def emit_early_exit(from_id: str, cond_id: str, is_true: bool, is_error: bool = False) -> None:
        suffix = "true" if is_true else "false"
        exit_node_id = f"{cond_id}::exit_{suffix}"
        add_node(
            {
                "id": exit_node_id,
                "type": "output",
                "name": "raises" if is_error else "exit",
                "is_error": is_error,
                "line": 1,
                "source_range": {"begin": 0, "end": 0, "line": 1},
            }
        )
        terminal_exit_ids.add(exit_node_id)
        edge_kind = f"branch_exit_{suffix}"
        add_edge(
            {
                "id": f"e-exit-{suffix}-{from_id}-{exit_node_id}",
                "from": from_id,
                "to": exit_node_id,
                "kind": edge_kind,
            }
        )

    def emit_inner_node(child: dict, child_ids: list[str], sink: str | None = None) -> None:
        """Emit a node that lives inside a container (no sequential edges)."""
        kind = child["kind"]
        child_id = child["id"]
        child_line = child["source_range"]["line"]
        if kind == "step":
            add_node(
                _apply_child_workflow_fields(
                    {
                        "id": child_id,
                        "type": "activity",
                        "name": child.get("label", child_id),
                        "line": child_line,
                        "source_range": child["source_range"],
                    },
                    child,
                )
            )
        elif kind == "human_input":
            add_node(
                {
                    "id": child_id,
                    "type": "human_input",
                    "name": child.get("label", "human_input"),
                    "line": child_line,
                    "source_range": child["source_range"],
                }
            )
        elif kind == "wait_condition":
            add_node(
                {
                    "id": child_id,
                    "type": "wait_condition",
                    "name": child.get("label", "wait"),
                    "line": child_line,
                    "source_range": child["source_range"],
                }
            )
        elif kind == "task":
            add_node(
                {
                    "id": child_id,
                    "type": "task",
                    "name": child.get("label", child_id),
                    "line": child_line,
                    "source_range": child["source_range"],
                }
            )
        elif kind == "memory_op":
            add_node(
                {
                    "id": child_id,
                    "type": "memory_op",
                    "name": child.get("label", child_id),
                    "line": child_line,
                    "source_range": child["source_range"],
                }
            )
        elif kind == "raise":
            add_node(
                {
                    "id": child_id,
                    "type": "output",
                    "name": child.get("label", "raise"),
                    "is_error": True,
                    "line": child_line,
                    "source_range": child["source_range"],
                }
            )
            terminal_exit_ids.add(child_id)
        elif kind == "ellipsis":
            add_node(
                {
                    "id": child_id,
                    "type": "unknown",
                    "name": "...",
                    "line": child_line,
                    "source_range": child["source_range"],
                }
            )
        elif kind == "dispatch":
            add_node(
                {
                    "id": child_id,
                    "type": "dispatch",
                    "name": child.get("label", child_id),
                    "line": child_line,
                    "source_range": child["source_range"],
                    "callees": child.get("callees", []),
                    "dispatch_label": child.get("dispatch_label", ""),
                }
            )
        elif kind == "conditional":
            if sink is None:
                return
            emit_contained_conditional(child, child_ids, sink)
            return
        elif kind == "loop":
            inner_ids: list[str] = []
            for grandchild in child.get("children", []):
                emit_inner_node(grandchild, inner_ids, child_id)
            add_node(
                {
                    "id": child_id,
                    "type": "loop",
                    "name": child.get("label", "loop"),
                    "line": child_line,
                    "source_range": child["source_range"],
                    "children": inner_ids,
                }
            )
        elif kind == "try_except":
            te_inner_ids: list[str] = []
            for tb in child.get("try_body", []):
                emit_inner_node(tb, te_inner_ids, child_id)
            for handler in child.get("handlers", []):
                for hc in handler.get("body", []):
                    emit_inner_node(hc, te_inner_ids, child_id)
            for fc in child.get("finally_body", []):
                emit_inner_node(fc, te_inner_ids, child_id)
            if te_inner_ids:
                add_node(
                    {
                        "id": child_id,
                        "type": "try_except",
                        "name": "except",
                        "line": child_line,
                        "source_range": child["source_range"],
                        "children": te_inner_ids,
                    }
                )
            else:
                return
        elif kind == "parallel":
            par_branch_ids: list[list[str]] = []
            for branch in child.get("branches", []):
                lane_ids: list[str] = []
                for grandchild in branch:
                    emit_inner_node(grandchild, lane_ids, child_id)
                par_branch_ids.append(lane_ids)
            add_node(
                {
                    "id": child_id,
                    "type": "parallel",
                    "name": "parallel",
                    "line": child_line,
                    "source_range": child["source_range"],
                    "branches": par_branch_ids,
                }
            )
        else:
            return
        child_ids.append(child_id)

    def emit_contained_conditional(node: dict, child_ids: list[str], sink: str) -> None:
        """Emit a conditional that lives inside a container (e.g. a loop body).

        Unlike top-level conditionals (handled by process_list), the conditional is
        positioned by the container's own layout pass, so it carries no incoming
        sequential edge. Its branches are emitted as contained nodes with branch
        edges between them; ``branchTrue``/``branchFalse`` record each branch's node
        ids so the container layout can place them side by side, and an empty branch
        emits a ``branch_*_skip`` edge to ``sink`` so the conditional keeps exactly
        one true and one false output (see _validate_flat_graph)."""
        cond_id = node["id"]
        conditional_ids.add(cond_id)
        add_node(
            {
                "id": cond_id,
                "type": "conditional",
                "name": node.get("label", cond_id),
                "line": node["source_range"]["line"],
                "source_range": node["source_range"],
            }
        )

        branch_sink = _first_emittable_id(node.get("rejoin", [])) or sink

        def emit_branch(branch_nodes: list[dict], suffix: str) -> tuple[list[str], list[str]]:
            ids: list[str] = []
            branch_start = len(flat_nodes)
            for bn in branch_nodes:
                emit_inner_node(bn, ids, branch_sink)
            descendants = [flat_nodes[i]["id"] for i in range(branch_start, len(flat_nodes))]
            if ids:
                add_edge(
                    {
                        "id": f"e-{cond_id}-{ids[0]}-branch_{suffix}",
                        "from": cond_id,
                        "to": ids[0],
                        "kind": f"branch_{suffix}",
                    }
                )
                for from_id, to_id in zip(ids, ids[1:]):
                    add_edge(
                        {
                            "id": f"e-{from_id}-{to_id}",
                            "from": from_id,
                            "to": to_id,
                            "kind": "sequential",
                        }
                    )
            else:
                add_edge(
                    {
                        "id": f"e-skip-{cond_id}-{branch_sink}-branch_{suffix}",
                        "from": cond_id,
                        "to": branch_sink,
                        "kind": f"branch_{suffix}_skip",
                    }
                )
            return ids, descendants

        true_ids, true_descendants = emit_branch(node.get("true_branch", []), "true")
        false_ids, false_descendants = emit_branch(node.get("false_branch", []), "false")
        cond_node = next(n for n in flat_nodes if n["id"] == cond_id)
        cond_node["branchTrue"] = true_ids
        cond_node["branchFalse"] = false_ids
        cond_node["branchDescendants"] = true_descendants + false_descendants
        child_ids.append(cond_id)

        # Statements after the if within the same loop body (rejoin) follow the
        # conditional as further container children.
        for rj in node.get("rejoin", []):
            if rj["kind"] == "conditional":
                emit_contained_conditional(rj, child_ids, sink)
            else:
                emit_inner_node(rj, child_ids)

    def _first_emittable_id(nodes: list[dict]) -> str | None:
        # try_except is transparent (no flat node emitted); skip into its body.
        for node in nodes:
            if node["kind"] == "try_except":
                inner = _first_emittable_id(node.get("try_body", []))
                if inner is not None:
                    return inner
            else:
                return str(node["id"])
        return None

    def process_list(nodes: list[dict], prev_id: str, first_kind: str, terminal_id: str | None = None) -> str:
        for node_idx, node in enumerate(nodes):
            kind = node["kind"]
            node_id = node["id"]
            line = node["source_range"]["line"]

            if kind in ("step", "human_input", "wait_condition", "task", "memory_op", "ellipsis"):
                type_map = {
                    "step": "activity",
                    "human_input": "human_input",
                    "wait_condition": "wait_condition",
                    "task": "task",
                    "memory_op": "memory_op",
                    "ellipsis": "unknown",
                }
                name_map = {
                    "step": node.get("label", node_id),
                    "human_input": node.get("label", "human_input"),
                    "wait_condition": node.get("label", "wait"),
                    "task": node.get("label", node_id),
                    "memory_op": node.get("label", node_id),
                    "ellipsis": "...",
                }
                flat = {
                    "id": node_id,
                    "type": type_map[kind],
                    "name": name_map[kind],
                    "line": line,
                    "source_range": node["source_range"],
                }
                if kind == "step":
                    flat = _apply_child_workflow_fields(flat, node)
                add_node(flat)
                add_edge(
                    {
                        "id": f"e-{prev_id}-{node_id}",
                        "from": prev_id,
                        "to": node_id,
                        "kind": first_kind,
                    }
                )
                prev_id = node_id
                first_kind = "sequential"

            elif kind == "raise":
                add_node(
                    {
                        "id": node_id,
                        "type": "output",
                        "name": node.get("label", "raise"),
                        "is_error": True,
                        "line": line,
                        "source_range": node["source_range"],
                    }
                )
                add_edge(
                    {
                        "id": f"e-{prev_id}-{node_id}",
                        "from": prev_id,
                        "to": node_id,
                        "kind": first_kind,
                    }
                )
                terminal_exit_ids.add(node_id)
                prev_id = node_id
                first_kind = "sequential"

            elif kind == "try_except":
                try_body_last_id = process_list(node["try_body"], prev_id, first_kind, terminal_id)
                prev_id = try_body_last_id
                handler_child_ids: list[str] = []
                for handler in node.get("handlers", []):
                    for child in handler.get("body", []):
                        emit_inner_node(child, handler_child_ids)
                if handler_child_ids:
                    add_node(
                        {
                            "id": node_id,
                            "type": "try_except",
                            "name": "except",
                            "line": line,
                            "source_range": node["source_range"],
                            "children": handler_child_ids,
                        }
                    )
                    if try_body_last_id not in terminal_exit_ids:
                        add_edge(
                            {
                                "id": f"e-{try_body_last_id}-{node_id}",
                                "from": try_body_last_id,
                                "to": node_id,
                                "kind": "sequential",
                            }
                        )
                    prev_id = node_id
                finally_body = node.get("finally_body", [])
                if finally_body:
                    prev_id = process_list(finally_body, prev_id, "sequential", terminal_id)
                first_kind = "sequential"

            elif kind == "dispatch":
                add_node(
                    {
                        "id": node_id,
                        "type": "dispatch",
                        "name": node.get("label", node_id),
                        "line": line,
                        "source_range": node["source_range"],
                        "callees": node.get("callees", []),
                        "dispatch_label": node.get("dispatch_label", ""),
                    }
                )
                add_edge(
                    {
                        "id": f"e-{prev_id}-{node_id}",
                        "from": prev_id,
                        "to": node_id,
                        "kind": first_kind,
                    }
                )
                prev_id = node_id
                first_kind = "sequential"

            elif kind == "parallel":
                child_ids: list[str] = []
                branch_ids: list[list[str]] = []
                for branch in node.get("branches", []):
                    lane_ids: list[str] = []
                    for child in branch:
                        emit_inner_node(child, lane_ids)
                    branch_ids.append(lane_ids)
                    child_ids.extend(lane_ids)
                add_node(
                    {
                        "id": node_id,
                        "type": "parallel",
                        "name": "parallel",
                        "line": line,
                        "source_range": node["source_range"],
                        "branches": branch_ids,
                    }
                )
                add_edge(
                    {
                        "id": f"e-{prev_id}-{node_id}",
                        "from": prev_id,
                        "to": node_id,
                        "kind": first_kind,
                    }
                )
                prev_id = node_id
                first_kind = "sequential"

            elif kind == "loop":
                child_ids = []
                loop_sink = node_id
                for child in node.get("children", []):
                    emit_inner_node(child, child_ids, loop_sink)
                add_node(
                    {
                        "id": node_id,
                        "type": "loop",
                        "name": node.get("label", "loop"),
                        "line": line,
                        "source_range": node["source_range"],
                        "children": child_ids,
                    }
                )
                add_edge(
                    {
                        "id": f"e-{prev_id}-{node_id}",
                        "from": prev_id,
                        "to": node_id,
                        "kind": first_kind,
                    }
                )
                prev_id = node_id
                first_kind = "sequential"

            else:
                # conditional
                cond_id = node_id
                conditional_ids.add(cond_id)
                true_exits = node.get("true_exits", False)
                false_exits = node.get("false_exits", False)
                rejoin = node.get("rejoin", [])
                true_branch = node.get("true_branch", [])
                false_branch = node.get("false_branch", [])

                cond_node: dict = {
                    "id": cond_id,
                    "type": "conditional",
                    "name": node.get("label", cond_id),
                    "line": line,
                    "source_range": node["source_range"],
                }
                add_node(cond_node)
                add_edge(
                    {
                        "id": f"e-{prev_id}-{cond_id}",
                        "from": prev_id,
                        "to": cond_id,
                        "kind": first_kind,
                    }
                )

                if rejoin:
                    branch_sink = _first_emittable_id(rejoin) or terminal_id
                else:
                    remaining = nodes[node_idx + 1 :]
                    branch_sink = _first_emittable_id(remaining) or terminal_id

                true_start = len(flat_nodes)
                true_last = process_list(true_branch, cond_id, "branch_true", branch_sink)
                true_end = len(flat_nodes)

                false_start = len(flat_nodes)
                false_last = process_list(false_branch, cond_id, "branch_false", branch_sink)
                false_end = len(flat_nodes)

                # Terminal exits (raise outputs, early-exit outputs) are branch boundaries,
                # not collapsible inner content. Excluding them keeps a raise-exit branch
                # consistent with a return-exit branch (whose synthetic exit node is added
                # after this snapshot) — both yield empty branchDescendants.
                cond_node["branchDescendants"] = [
                    flat_nodes[i]["id"]
                    for i in (*range(true_start, true_end), *range(false_start, false_end))
                    if flat_nodes[i]["id"] not in terminal_exit_ids
                ]

                def wire_branch(
                    last_id: str, exits: bool, is_true: bool, sink: str | None, is_error: bool = False
                ) -> None:
                    suffix = "true" if is_true else "false"
                    if exits:
                        # Terminal nodes and nested conditionals already emitted their exit edges.
                        if last_id in terminal_exit_ids or (last_id in conditional_ids and last_id != cond_id):
                            return
                        emit_early_exit(last_id, cond_id, is_true, is_error)
                    elif sink is not None:
                        if last_id != cond_id:
                            if last_id not in conditional_ids and not has_edge_between(last_id, sink):
                                add_edge(
                                    {
                                        "id": f"e-merge-{cond_id}-{sink}-branch_{suffix}",
                                        "from": last_id,
                                        "to": sink,
                                        "kind": "branch_merge",
                                    }
                                )
                        else:
                            skip_kind = f"branch_{suffix}_skip"
                            add_edge(
                                {
                                    "id": f"e-skip-{cond_id}-{sink}-branch_{suffix}",
                                    "from": cond_id,
                                    "to": sink,
                                    "kind": skip_kind,
                                }
                            )

                wire_branch(true_last, true_exits, True, branch_sink, node.get("true_exit_error", False))
                wire_branch(false_last, false_exits, False, branch_sink, node.get("false_exit_error", False))

                if rejoin:
                    rejoin_start = branch_sink if branch_sink is not None else cond_id
                    prev_id = process_list(rejoin, rejoin_start, "sequential", terminal_id)
                else:
                    prev_id = cond_id

                first_kind = "sequential"

        return prev_id

    # Synthetic workflow root
    add_node(
        {
            "id": wf_name,
            "type": "workflow",
            "name": wf_name,
            "line": 1,
            "source_range": {"begin": 0, "end": 0, "line": 1},
        }
    )
    chain_start = wf_name

    if ep_name is not None and ep_begin is not None:
        ep_id = f"{wf_name}::entrypoint"
        ep_line_ = ep_line or 1
        add_node(
            {
                "id": ep_id,
                "type": "entrypoint",
                "name": ep_name,
                "line": ep_line_,
                "source_range": {"begin": ep_begin, "end": ep_end or ep_begin, "line": ep_line_},
            }
        )
        add_edge({"id": f"e-{wf_name}-{ep_id}", "from": wf_name, "to": ep_id, "kind": "sequential"})
        chain_start = ep_id

    out_id = f"{wf_name}::output"
    out_label = output_type or "exit"

    last_id = process_list(tree_nodes, chain_start, "sequential", out_id)

    # Suppress the normal "exit" node when nothing reaches it (e.g. the whole body
    # ends in a raise): only the red error terminal should be shown.
    body_falls_through = last_id not in terminal_exit_ids
    out_referenced = any(e["to"] == out_id for e in flat_edges)
    if body_falls_through or out_referenced:
        add_node(
            {
                "id": out_id,
                "type": "output",
                "name": out_label,
                "line": 1,
                "source_range": {"begin": 0, "end": 0, "line": 1},
            }
        )
    if body_falls_through:
        add_edge({"id": f"e-{last_id}-{out_id}", "from": last_id, "to": out_id, "kind": "sequential"})

    return flat_nodes, flat_edges


def _validate_flat_graph(wf_name: str, flat_nodes: list[dict], flat_edges: list[dict]) -> None:
    """Assert every conditional node has exactly 1 true output and 1 false output."""
    from_index: dict[str, list[dict]] = {}
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


def build_graph_dynamically(workflow_cls: type) -> AtlasWireFormat:
    from mistralai.workflows.core.definition.workflow_definition import (
        _get_workflow_entrypoint_method,
    )

    file_path = inspect.getfile(workflow_cls)
    source_text = Path(file_path).read_text()
    sources: dict[str, str] = {file_path: source_text}
    asts: dict[str, ast.Module] = {}
    indices: dict[str, _FileIndex] = {}
    ast_tree = _get_ast(file_path, sources, asts)

    cls_def = next(
        (n for n in ast_tree.body if isinstance(n, ast.ClassDef) and n.name == workflow_cls.__name__),
        None,
    )
    if cls_def is None:
        raise ValueError(f"Class {workflow_cls.__name__} not found in {file_path}")

    entrypoint_fn = _get_workflow_entrypoint_method(workflow_cls)
    if entrypoint_fn is None:
        raise ValueError(f"No entrypoint method for {workflow_cls.__name__}")

    ep_name = entrypoint_fn.__name__
    ep_def = next(
        (n for n in cls_def.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == ep_name),
        None,
    )
    if ep_def is None:
        raise ValueError(f"Entrypoint method {ep_name} not found in {workflow_cls.__name__}")

    workflow_name = workflow_cls.__name__
    byte_len = len(source_text.encode("utf-8"))
    file_ranges: dict[str, dict] = {file_path: {"begin": 0, "end": byte_len}}

    module_ns = vars(inspect.getmodule(entrypoint_fn))
    resolver = _DynamicResolver(module_ns=module_ns, workflow_cls=workflow_cls)

    tree_nodes = _walk_body_tree(
        ep_def.body,
        resolver,
        sources,
        asts,
        indices,
        file_path,
        workflow_name,
        _TreeCtx(cls_def=cls_def, workflow_cls=workflow_cls),
        file_ranges,
    )

    index = _get_index(file_path, sources, asts, indices)
    ep_begin, ep_end = _ast_span(ep_def, index)
    output_type: str | None = ast.unparse(ep_def.returns) if ep_def.returns is not None else None

    signals, updates, queries = _collect_class_handlers_runtime(workflow_cls, cls_def, index)

    flat_nodes, flat_edges = _flatten_tree(
        tree_nodes,
        workflow_name,
        ep_name,
        ep_begin,
        ep_end,
        ep_def.lineno,
        output_type,
        file_ranges,
    )
    _validate_flat_graph(workflow_name, flat_nodes, flat_edges)

    return AtlasWireFormat.model_validate(
        {
            "version": 3,
            "workflow_name": workflow_name,
            "files": file_ranges,
            "primary_file": next(iter(file_ranges), ""),
            "nodes": flat_nodes,
            "edges": flat_edges,
            "incomplete": False,
            "entrypoint": {"name": ep_name, "begin": ep_begin, "end": ep_end},
            "output_type": output_type,
            "signals": signals,
            "updates": updates,
            "queries": queries,
            "schedule": None,
        }
    )


def _is_workflow_cls_def(cls_def: ast.ClassDef) -> bool:
    """Return True if the class has a @*.define(...) decorator (workflow class)."""
    for dec in cls_def.decorator_list:
        inner = dec.func if isinstance(dec, ast.Call) else dec
        if _decorator_leaf_name(inner) == "define":
            return True
    return False


def _find_entrypoint_method_ast(
    cls_def: ast.ClassDef,
) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    """Find the workflow entrypoint method by @*.entrypoint decorator or name 'run'."""
    for node in cls_def.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for dec in node.decorator_list:
            inner = dec.func if isinstance(dec, ast.Call) else dec
            if _decorator_leaf_name(inner) == "entrypoint":
                return node
    for node in cls_def.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "run":
            return node
    return None


def _build_import_symbol_table(
    module_ast: ast.Module,
    file_path: str,
) -> tuple[dict[str, str], dict[str, str]]:
    """Map local symbols to candidate file paths and to their original names.

    Returns ``(paths, names)`` where ``paths`` maps a locally-bound name (which
    may be an import alias) to a candidate source file, and ``names`` maps that
    local name back to the original defined/imported name — the class ``__name__``
    Atlas registers and navigates by.
    """
    file_dir = Path(file_path).parent
    result: dict[str, str] = {}
    symbol_names: dict[str, str] = {}

    def add_symbol(local_name: str, original_name: str, candidate_path: str) -> None:
        if local_name not in result:
            result[local_name] = candidate_path
            symbol_names[local_name] = original_name

    for node in module_ast.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if _has_activity_decorator(node):
                add_symbol(node.name, node.name, file_path)

    for stmt in module_ast.body:
        if not isinstance(stmt, ast.ImportFrom):
            continue
        level = stmt.level or 0
        module = stmt.module or ""
        base = file_dir
        for _ in range(level - 1):
            base = base.parent
        if level > 0:
            if module:
                candidate = base / module.replace(".", "/")
                candidate_path = str(candidate.with_suffix(".py"))
                for alias in stmt.names:
                    local_name = alias.asname or alias.name
                    add_symbol(local_name, alias.name, candidate_path)
            else:
                # from . import name  — each alias is a separate sibling module
                for alias in stmt.names:
                    local_name = alias.asname or alias.name
                    candidate_path = str((base / alias.name).with_suffix(".py"))
                    add_symbol(local_name, alias.name, candidate_path)
        else:
            candidate = file_dir / module.replace(".", "/")
            candidate_path = str(candidate.with_suffix(".py"))
            for alias in stmt.names:
                local_name = alias.asname or alias.name
                add_symbol(local_name, alias.name, candidate_path)

    return result, symbol_names


def build_graph_statically(
    source: str,
    path: str,
    file_resolver: Callable[[str], str | None],
) -> list[AtlasWireFormat]:
    """Parse *source* and return one :class:`AtlasWireFormat` per workflow class found.

    ``path`` is the absolute path used for source-range anchoring and import resolution.
    ``file_resolver`` is called lazily with an absolute path and returns the source text
    of that file, or ``None`` when the file is unavailable.
    """
    try:
        module_ast = ast.parse(source)
    except SyntaxError:
        return []

    sources: dict[str, str] = {path: source}
    asts: dict[str, ast.Module] = {path: module_ast}
    indices: dict[str, _FileIndex] = {}
    symbols, symbol_names = _build_import_symbol_table(module_ast, path)
    results: list[AtlasWireFormat] = []

    for node in module_ast.body:
        if not isinstance(node, ast.ClassDef):
            continue
        if not _is_workflow_cls_def(node):
            continue

        cls_def = node
        workflow_name = cls_def.name
        ep_def = _find_entrypoint_method_ast(cls_def)
        if ep_def is None:
            continue

        byte_len = len(source.encode("utf-8"))
        file_ranges: dict[str, dict] = {path: {"begin": 0, "end": byte_len}}

        index = _get_index(path, sources, asts, indices)
        ep_begin, ep_end = _ast_span(ep_def, index)
        output_type: str | None = ast.unparse(ep_def.returns) if ep_def.returns is not None else None

        resolver = _StaticResolver(
            symbols=symbols,
            symbol_names=symbol_names,
            file_resolver=file_resolver,
            cls_def=cls_def,
            file_path=path,
        )
        tree_nodes = _walk_body_tree(
            ep_def.body,
            resolver,
            sources,
            asts,
            indices,
            path,
            workflow_name,
            _TreeCtx(cls_def=cls_def),
            file_ranges,
        )

        file_offset = file_ranges[path]["begin"]
        signals, updates, queries = _scan_class_handlers(cls_def, index, file_offset)

        flat_nodes, flat_edges = _flatten_tree(
            tree_nodes,
            workflow_name,
            ep_def.name,
            ep_begin,
            ep_end,
            ep_def.lineno,
            output_type,
            file_ranges,
        )

        try:
            _validate_flat_graph(workflow_name, flat_nodes, flat_edges)
            incomplete = False
        except GraphValidationError:
            logger.exception("Graph validation failed for %s", workflow_name)
            incomplete = True

        results.append(
            AtlasWireFormat.model_validate(
                {
                    "version": 3,
                    "workflow_name": workflow_name,
                    "files": file_ranges,
                    "primary_file": next(iter(file_ranges), ""),
                    "nodes": flat_nodes,
                    "edges": flat_edges,
                    "incomplete": incomplete,
                    "entrypoint": {"name": ep_def.name, "begin": ep_begin, "end": ep_end},
                    "output_type": output_type,
                    "signals": signals,
                    "updates": updates,
                    "queries": queries,
                    "schedule": None,
                }
            )
        )

    return results
