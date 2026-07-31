"""Build the tree IR from Python source.

Source -> [_graph_builder] -> list[TreeNode] -> [_graph_flattener] -> flat dicts -> [_graph_emitter] -> AtlasWireFormat
          ^ this module
"""

from __future__ import annotations

import ast
import dataclasses
import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Literal, get_type_hints

from mistralai.workflows.core._graph_types import (
    _ACTIVITY_NODE_TYPES,
    _MEMORY_OPS,
    TreeNode,
    _AgentNode,
    _ConditionalNode,
    _ContinueAsNewNode,
    _decorator_leaf_name,
    _EllipsisNode,
    _FileIndex,
    _has_activity_decorator,
    _HumanInputNode,
    _LoopNode,
    _MemoryOpNode,
    _ParallelNode,
    _RaiseNode,
    _SleepNode,
    _SourceRange,
    _StepNode,
    _TreeCtx,
    _TryExceptHandler,
    _TryExceptNode,
    _WaitConditionNode,
)
from mistralai.workflows.core.activity import check_is_activity
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.definition.workflow_definition import get_workflow_definition

# Max indirection followed when resolving an awaitable to its underlying call. Real nesting is
# shallow (e.g. starred -> name -> comprehension -> call is 3 hops); 4 leaves headroom for one
# extra indirection while still terminating cycles from self-referential bindings (e.g. x = x or []).
_MAX_AWAITABLE_RESOLVE_DEPTH = 4


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


def _scoped_binding_ctx(ctx: _TreeCtx) -> _TreeCtx:
    """Return a child context whose local-function and name-binding dicts are isolated copies.

    Each statement block gets its own copy seeded from its parent, so bindings recorded while
    walking a block (incrementally, in source order — see _record_binding) stay local to that
    block: sibling if/else branches and inlined helpers cannot leak names to one another, and a
    binding is only visible to statements that follow it. Counters and other fields stay shared
    by reference so node ids remain unique across the walk.
    """
    return dataclasses.replace(ctx, local_funcs=dict(ctx.local_funcs), name_values=dict(ctx.name_values))


def _record_binding(stmt: ast.stmt, ctx: _TreeCtx) -> None:
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
    walk_lane: Callable[[list[ast.stmt]], list[TreeNode]],
    ctx: _TreeCtx,
    index: _FileIndex,
    file_ranges: dict[str, dict[str, int]],
    file_path: str,
    workflow_name: str,
) -> _ParallelNode | None:
    branches: list[list[TreeNode]] = []
    for lane_call in lane_exprs:
        wrapper = ast.Expr(
            value=lane_call,
            lineno=lane_call.lineno,
            col_offset=lane_call.col_offset,
            end_lineno=lane_call.end_lineno,
            end_col_offset=lane_call.end_col_offset,
        )
        lane_nodes: list[TreeNode] = [n for n in walk_lane([wrapper]) if not isinstance(n, _EllipsisNode)]
        if lane_nodes:
            branches.append(lane_nodes)
    if not branches:
        return None
    par_idx = ctx.parallel_counter[0]
    ctx.parallel_counter[0] += 1
    cb, ce = _ast_span(par_call, index)
    return _ParallelNode(
        id=f"{workflow_name}::parallel_{par_idx}",
        source_range=_abs_range(file_ranges, file_path, cb, ce, line=par_call.lineno),
        branches=branches,
    )


def _resolve(expr: ast.expr, module_ns: dict[str, Any]) -> Any:
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


def _resolve_call(call: ast.Call, module_ns: dict[str, Any]) -> Any:
    return _resolve(call.func, module_ns)


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


def _has_activity_nodes(nodes: list[TreeNode]) -> bool:
    for n in nodes:
        if isinstance(n, _ACTIVITY_NODE_TYPES):
            return True
        if isinstance(n, _ConditionalNode):
            if (
                _has_activity_nodes(n.true_branch)
                or _has_activity_nodes(n.false_branch)
                or _has_activity_nodes(n.rejoin)
            ):
                return True
        elif isinstance(n, _LoopNode):
            if _has_activity_nodes(n.children):
                return True
        elif isinstance(n, _TryExceptNode):
            if _has_activity_nodes(n.try_body) or _has_activity_nodes(n.finally_body):
                return True
            for h in n.handlers:
                if _has_activity_nodes(h.body):
                    return True
        elif isinstance(n, _ParallelNode):
            for branch in n.branches:
                if _has_activity_nodes(branch):
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


def _abs_range(
    file_ranges: dict[str, dict[str, int]], file_path: str, begin: int, end: int, line: int = 0
) -> _SourceRange:
    """Absolute byte offsets in the concatenated source blob for a per-file span."""
    fb = file_ranges.get(file_path, {}).get("begin", 0)
    return _SourceRange(begin=fb + begin, end=fb + end, line=line)


def _make_ellipsis_node(ctx: _TreeCtx, workflow_name: str, source_range: _SourceRange) -> _EllipsisNode:
    ell_idx = ctx.ellipsis_counter[0]
    ctx.ellipsis_counter[0] += 1
    return _EllipsisNode(
        id=f"{workflow_name}::ellipsis_{ell_idx}",
        source_range=source_range,
    )


def _register_source_file(
    file_path: str,
    source_text: str,
    sources: dict[str, str],
    file_ranges: dict[str, dict[str, int]],
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
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ast.ClassDef, str, str, dict[str, Any]] | None:
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
            module_ns: dict[str, Any] = vars(mod) if mod is not None else {}
            return fn, cls_def, src, file_path, module_ns
    return None


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
# Connector collection (mistralai connectors plugin) — duck-typed, no plugin import
# ---------------------------------------------------------------------------


def _connectors_from_func(func: Any) -> list[str]:
    """Connector names an activity depends on via ``Depends(connector(...))`` defaults.

    Duck-typed: a ``Depends(...)`` default exposes ``.dependency``, and a connector
    dependency (``ConnectorSlot``) exposes ``.connector_name``.
    """
    try:
        sig = inspect.signature(func)
    except (TypeError, ValueError):
        return []
    names: list[str] = []
    for param in sig.parameters.values():
        dependency = getattr(param.default, "dependency", None)
        connector_name = getattr(dependency, "connector_name", None)
        if isinstance(connector_name, str) and connector_name not in names:
            names.append(connector_name)
    return names


def _connector_name_from_call(call: ast.Call) -> str | None:
    """Return the connector name from a ``connector("name", ...)`` call."""
    if call.args and isinstance(call.args[0], ast.Constant) and isinstance(call.args[0].value, str):
        return call.args[0].value
    for kw in call.keywords:
        if kw.arg == "name" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
            return kw.value.value
    return None


_CONNECTOR_FACTORY_PREFIX = "mistralai.workflows.plugins.mistralai"
_WORKFLOWS_PREFIX = "mistralai.workflows"


def _import_aliases(module_ast: ast.Module, original_name: str, *, module_prefix: str | None = None) -> set[str]:
    """Local names bound to *original_name* via ``from ... import`` in *module_ast*."""
    names: set[str] = set()
    for stmt in module_ast.body:
        if not isinstance(stmt, ast.ImportFrom) or not stmt.module:
            continue
        if (
            module_prefix is not None
            and stmt.module != module_prefix
            and not stmt.module.startswith(module_prefix + ".")
        ):
            continue
        for alias in stmt.names:
            if alias.name == original_name:
                names.add(alias.asname or alias.name)
    return names


@dataclass(frozen=True)
class _ConnectorCallNames:
    """Local names by which a module can invoke the connectors ``connector(...)`` factory."""

    direct: frozenset[str]
    module: frozenset[str]


def _connector_call_names(module_ast: ast.Module) -> _ConnectorCallNames:
    """Names by which *module_ast* can invoke the connectors ``connector(...)`` factory."""
    direct = _import_aliases(module_ast, "connector", module_prefix=_CONNECTOR_FACTORY_PREFIX)
    module: set[str] = set()
    pkg = f"{_CONNECTOR_FACTORY_PREFIX}.connectors"
    for stmt in module_ast.body:
        if isinstance(stmt, ast.ImportFrom):
            if stmt.module == _CONNECTOR_FACTORY_PREFIX:
                module.update(alias.asname or alias.name for alias in stmt.names if alias.name == "connectors")
        elif isinstance(stmt, ast.Import):
            module.update(alias.asname for alias in stmt.names if alias.name == pkg and alias.asname)
    return _ConnectorCallNames(direct=frozenset(direct), module=frozenset(module))


def _depends_import_names(module_ast: ast.Module) -> set[str]:
    """Local names for the dependency-injection ``Depends`` marker in *module_ast*."""
    return {"Depends", *_import_aliases(module_ast, "Depends", module_prefix=_WORKFLOWS_PREFIX)}


def _uses_connectors_decorator_names(module_ast: ast.Module) -> set[str]:
    """Local names for the ``@uses_connectors`` decorator in *module_ast*."""
    return {"uses_connectors", *_import_aliases(module_ast, "uses_connectors", module_prefix=_CONNECTOR_FACTORY_PREFIX)}


def _module_bool_constants(module_ast: ast.Module) -> dict[str, bool]:
    """Module-level ``NAME = True``/``NAME = False`` assignments."""
    constants: dict[str, bool] = {}
    for stmt in module_ast.body:
        if not isinstance(stmt, ast.Assign) or len(stmt.targets) != 1:
            continue
        target = stmt.targets[0]
        if isinstance(target, ast.Name) and isinstance(stmt.value, ast.Constant) and isinstance(stmt.value.value, bool):
            constants[target.id] = stmt.value.value
    return constants


def _resolved_is_connector_factory(func_obj: object) -> bool:
    """True if *func_obj* is the connectors ``connector(...)`` factory."""
    if getattr(func_obj, "__name__", None) != "connector":
        return False
    module = getattr(func_obj, "__module__", "") or ""
    return "connectors" in module.split(".")


def _is_connector_call(call: ast.Call, names: _ConnectorCallNames) -> bool:
    """True if *call* invokes the connectors ``connector(...)`` factory."""
    func = call.func
    if isinstance(func, ast.Name):
        return func.id in names.direct
    if isinstance(func, ast.Attribute) and func.attr == "connector":
        return isinstance(func.value, ast.Name) and func.value.id in names.module
    return False


def _collect_connector_bindings(module_ast: ast.Module, names: _ConnectorCallNames) -> dict[str, str]:
    """Map module-level names bound to ``connector("x")`` calls to the connector name."""
    bindings: dict[str, str] = {}
    for stmt in module_ast.body:
        if not isinstance(stmt, ast.Assign) or len(stmt.targets) != 1:
            continue
        target = stmt.targets[0]
        if isinstance(target, ast.Name) and isinstance(stmt.value, ast.Call) and _is_connector_call(stmt.value, names):
            name = _connector_name_from_call(stmt.value)
            if name is not None:
                bindings[target.id] = name
    return bindings


def _connector_name_from_arg(
    arg: ast.expr,
    bindings: dict[str, str],
    names: _ConnectorCallNames,
    imported_slot_resolver: Callable[[str], str | None] | None = None,
) -> str | None:
    """Resolve a ``uses_connectors``/``Depends`` argument to a connector name."""
    if isinstance(arg, ast.Name):
        local = bindings.get(arg.id)
        if local is not None:
            return local
        return imported_slot_resolver(arg.id) if imported_slot_resolver is not None else None
    if isinstance(arg, ast.Call) and _is_connector_call(arg, names):
        return _connector_name_from_call(arg)
    return None


def _resolve_imported_connector_slot(
    local_name: str,
    symbols: dict[str, str],
    symbol_names: dict[str, str],
    file_resolver: Callable[[str], str | None],
    sources: dict[str, str],
    asts: dict[str, ast.Module],
) -> str | None:
    """Resolve a connector slot imported from another module to its connector name."""
    src_file = symbols.get(local_name)
    if src_file is None:
        return None
    if src_file not in sources:
        text = file_resolver(src_file)
        if text is None:
            return None
        sources[src_file] = text
    if src_file not in asts:
        try:
            asts[src_file] = ast.parse(sources[src_file])
        except SyntaxError:
            return None
    module_ast = asts[src_file]
    bindings = _collect_connector_bindings(module_ast, _connector_call_names(module_ast))
    return bindings.get(symbol_names.get(local_name, local_name))


def _collect_workflow_connectors_static(
    cls_def: ast.ClassDef,
    bindings: dict[str, str],
    call_names: _ConnectorCallNames,
    decorator_names: set[str],
    imported_slot_resolver: Callable[[str], str | None] | None = None,
) -> list[str]:
    """Connector names from a ``@uses_connectors(...)`` decorator on a workflow class."""
    names: list[str] = []
    for dec in cls_def.decorator_list:
        if not isinstance(dec, ast.Call) or _decorator_leaf_name(dec.func) not in decorator_names:
            continue
        for arg in dec.args:
            name = _connector_name_from_arg(arg, bindings, call_names, imported_slot_resolver)
            if name is not None and name not in names:
                names.append(name)
    return names


def _collect_workflow_on_behalf_of_static(cls_def: ast.ClassDef, bool_constants: dict[str, bool]) -> bool:
    """Read the ``on_behalf_of`` kwarg from the ``@*.define(...)`` decorator on a workflow class."""
    for dec in cls_def.decorator_list:
        if not isinstance(dec, ast.Call) or _decorator_leaf_name(dec.func) != "define":
            continue
        for kw in dec.keywords:
            if kw.arg == "on_behalf_of":
                if isinstance(kw.value, ast.Name):
                    return bool_constants.get(kw.value.id, False)
                try:
                    return bool(ast.literal_eval(kw.value))
                except (ValueError, SyntaxError):
                    return False
    return False


def _activity_connectors_from_ast(
    fn_def: ast.FunctionDef | ast.AsyncFunctionDef,
    bindings: dict[str, str],
    call_names: _ConnectorCallNames,
    depends_names: set[str],
    imported_slot_resolver: Callable[[str], str | None] | None = None,
) -> list[str]:
    """Connector names from ``Depends(connector(...))`` arg defaults on an activity fn AST."""
    args = fn_def.args
    positional = [*args.posonlyargs, *args.args]
    paired: list[tuple[ast.arg, ast.expr | None]] = []
    offset = len(positional) - len(args.defaults)
    for i, a in enumerate(positional):
        paired.append((a, args.defaults[i - offset] if i >= offset else None))
    paired.extend(zip(args.kwonlyargs, args.kw_defaults))

    names: list[str] = []
    for _arg, default in paired:
        if not isinstance(default, ast.Call) or _resolve_call_fn_name(default) not in depends_names or not default.args:
            continue
        name = _connector_name_from_arg(default.args[0], bindings, call_names, imported_slot_resolver)
        if name is not None and name not in names:
            names.append(name)
    return names


# ---------------------------------------------------------------------------
# ActivityResolver — parameterises _walk_body_tree for dynamic vs static mode
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _InlineTarget:
    fn_def: ast.FunctionDef | ast.AsyncFunctionDef
    cls_def: ast.ClassDef
    file_path: str
    resolver: ActivityResolver
    param_types: dict[str, type]


def _extract_wf_arg(call: ast.Call) -> ast.expr | None:
    return call.args[0] if call.args else next((kw.value for kw in call.keywords if kw.arg == "workflow"), None)


def _is_runner_run_call(call: ast.Call) -> bool:
    """Return True for ``Runner.run(...)`` or aliased ``mod.Runner.run(...)`` calls.

    Matches by name (like execute_workflow / asyncio.gather) so the same check
    works in both dynamic and static analysis without resolver support.
    """
    func = call.func
    if not isinstance(func, ast.Attribute) or func.attr != "run":
        return False
    receiver = func.value
    if isinstance(receiver, ast.Name):
        return receiver.id == "Runner"
    if isinstance(receiver, ast.Attribute):
        return receiver.attr == "Runner"
    return False


def _kwarg(call: ast.Call, name: str) -> ast.expr | None:
    return next((kw.value for kw in call.keywords if kw.arg == name), None)


def _tool_display_name(expr: ast.expr) -> str | None:
    """Display name for one entry of an Agent ``tools=[...]`` list.

    Activities/custom tools are passed as bare references (``Name``/``Attribute``);
    built-in tools are instantiated (``WebSearchTool()``), so a ``Call`` resolves
    to its constructor's leaf name.
    """
    if isinstance(expr, ast.Name):
        return expr.id
    if isinstance(expr, ast.Attribute):
        return expr.attr
    if isinstance(expr, ast.Call):
        return _tool_display_name(expr.func)
    return None


def _resolve_agent_call(expr: ast.expr, ctx: _TreeCtx) -> ast.Call | None:
    """Resolve an agent expression to its ``Agent(...)`` call, if any.

    Accepts an inline ``Agent(...)`` call directly, or a ``Name`` bound to one via
    a prior ``agent = Agent(...)`` assignment (recorded in ``ctx.name_values``).
    """
    if isinstance(expr, ast.Call):
        return expr
    if isinstance(expr, ast.Name):
        bound = ctx.name_values.get(expr.id)
        if isinstance(bound, ast.Call):
            return bound
    return None


def _agent_name(expr: ast.expr, agent_call: ast.Call | None) -> str:
    """Display name for an agent reference, given its already-resolved ``Agent(...)`` call.

    Prefers the ``Agent(name=...)`` keyword; falls back to the bound variable name,
    else ``ast.unparse`` of the expression.
    """
    if agent_call is not None:
        name_arg = _kwarg(agent_call, "name")
        if name_arg is not None:
            try:
                return str(ast.literal_eval(name_arg))
            except (ValueError, SyntaxError):
                return ast.unparse(name_arg)
    if isinstance(expr, ast.Name):
        return expr.id
    return ast.unparse(expr)


def _agent_display_name(expr: ast.expr, ctx: _TreeCtx) -> str:
    """Display name for an agent reference (e.g. a handoff entry), resolving it via ``ctx``."""
    return _agent_name(expr, _resolve_agent_call(expr, ctx))


def _extract_agent_node_info(call: ast.Call, ctx: _TreeCtx) -> tuple[str, list[str], list[str], list[ast.expr]]:
    """Return ``(agent_name, tool_names, handoff_names, connector_exprs)`` for a ``Runner.run`` call.

    ``connector_exprs`` are the raw ``Agent(connectors=[...])`` references; the caller resolves
    them to connector names via the resolver (which has the module/symbol context).
    """
    agent_expr = _kwarg(call, "agent") or (call.args[0] if call.args else None)
    if agent_expr is None:
        return "agent", [], [], []

    agent_call = _resolve_agent_call(agent_expr, ctx)
    name = _agent_name(agent_expr, agent_call)
    if agent_call is None:
        return name, [], [], []

    tools: list[str] = []
    tools_arg = _kwarg(agent_call, "tools")
    if isinstance(tools_arg, (ast.List, ast.Tuple, ast.Set)):
        tools = [n for e in tools_arg.elts if (n := _tool_display_name(e)) is not None]

    handoffs: list[str] = []
    handoffs_arg = _kwarg(agent_call, "handoffs")
    if isinstance(handoffs_arg, (ast.List, ast.Tuple, ast.Set)):
        handoffs = [_agent_display_name(e, ctx) for e in handoffs_arg.elts]

    connector_exprs: list[ast.expr] = []
    connectors_arg = _kwarg(agent_call, "connectors")
    if isinstance(connectors_arg, (ast.List, ast.Tuple, ast.Set)):
        connector_exprs = list(connectors_arg.elts)

    return name, tools, handoffs, connector_exprs


class ActivityResolver:
    __slots__ = ()

    def resolve_activity(
        self,
        call: ast.Call,
        sources: dict[str, str],
        asts: dict[str, ast.Module],
    ) -> str | None:
        raise NotImplementedError

    def resolve_activity_connectors(
        self,
        call: ast.Call,
        sources: dict[str, str],
        asts: dict[str, ast.Module],
    ) -> list[str]:
        """Connector names the called activity depends on. Base returns none."""
        return []

    def resolve_connector_names(
        self,
        exprs: list[ast.expr],
        sources: dict[str, str],
        asts: dict[str, ast.Module],
    ) -> list[str]:
        """Resolve ``connector(...)`` references (e.g. ``Agent(connectors=[...])``) to names."""
        return []

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

    def __init__(self, module_ns: dict[str, Any], workflow_cls: type | None = None) -> None:
        self._module_ns = module_ns
        self._workflow_cls = workflow_cls

    def resolve_activity(self, call: ast.Call, sources: dict[str, str], asts: dict[str, ast.Module]) -> str | None:
        resolved = _resolve_call(call, self._module_ns)
        if resolved is not None and check_is_activity(resolved):
            return str(resolved.__name__)
        return None

    def resolve_activity_connectors(
        self, call: ast.Call, sources: dict[str, str], asts: dict[str, ast.Module]
    ) -> list[str]:
        resolved = _resolve_call(call, self._module_ns)
        if resolved is None or not check_is_activity(resolved):
            return []
        return _connectors_from_func(getattr(resolved, "__original_func__", resolved))

    def resolve_connector_names(
        self, exprs: list[ast.expr], sources: dict[str, str], asts: dict[str, ast.Module]
    ) -> list[str]:
        names: list[str] = []
        for expr in exprs:
            name = None
            if isinstance(expr, ast.Call) and _resolved_is_connector_factory(_resolve(expr.func, self._module_ns)):
                name = _connector_name_from_call(expr)
            else:
                connector_name = getattr(_resolve(expr, self._module_ns), "connector_name", None)
                if isinstance(connector_name, str):
                    name = connector_name
            if name is not None and name not in names:
                names.append(name)
        return names

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
            # The registered workflow name (``@workflow.define(name=...)``), which is
            # what the API/Atlas route by — not the Python class name.
            return get_workflow_definition(wf_cls).name
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
    __slots__ = ("_symbols", "_symbol_names", "_file_resolver", "_cls_def", "_file_path", "_child_cls_def_cache")

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
        # A child workflow is resolved twice per call site (name + file); cache the
        # parsed ClassDef so its source file isn't read and parsed more than once.
        self._child_cls_def_cache: dict[tuple[str, str], ast.ClassDef | None] = {}

    def resolve_activity(self, call: ast.Call, sources: dict[str, str], asts: dict[str, ast.Module]) -> str | None:
        fn_name = _resolve_call_fn_name(call)
        if not fn_name or fn_name not in self._symbols:
            return None
        fn_def = _lookup_fn_in_file(fn_name, self._symbols[fn_name], self._file_resolver, sources, asts)
        if fn_def is not None and _has_activity_decorator(fn_def):
            return fn_name
        return None

    def resolve_activity_connectors(
        self, call: ast.Call, sources: dict[str, str], asts: dict[str, ast.Module]
    ) -> list[str]:
        fn_name = _resolve_call_fn_name(call)
        if not fn_name or fn_name not in self._symbols:
            return []
        file_path = self._symbols[fn_name]
        fn_def = _lookup_fn_in_file(fn_name, file_path, self._file_resolver, sources, asts)
        if fn_def is None or not _has_activity_decorator(fn_def):
            return []
        module_ast = asts.get(file_path)
        if module_ast is None:
            return []
        call_names = _connector_call_names(module_ast)
        bindings = _collect_connector_bindings(module_ast, call_names)
        depends_names = _depends_import_names(module_ast)
        symbols, symbol_names = _build_import_symbol_table(module_ast, file_path)

        def slot_resolver(local_name: str) -> str | None:
            return _resolve_imported_connector_slot(
                local_name, symbols, symbol_names, self._file_resolver, sources, asts
            )

        return _activity_connectors_from_ast(fn_def, bindings, call_names, depends_names, slot_resolver)

    def resolve_connector_names(
        self, exprs: list[ast.expr], sources: dict[str, str], asts: dict[str, ast.Module]
    ) -> list[str]:
        module_ast = asts.get(self._file_path)
        if module_ast is None:
            return []
        call_names = _connector_call_names(module_ast)
        bindings = _collect_connector_bindings(module_ast, call_names)

        def slot_resolver(local_name: str) -> str | None:
            return _resolve_imported_connector_slot(
                local_name, self._symbols, self._symbol_names, self._file_resolver, sources, asts
            )

        names: list[str] = []
        for expr in exprs:
            name = _connector_name_from_arg(expr, bindings, call_names, slot_resolver)
            if name is not None and name not in names:
                names.append(name)
        return names

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

        The class name is the original ``__name__`` (not the local import alias),
        used as a fallback identity when the registered ``@workflow.define(name=...)``
        can't be read; the file path is the candidate module, when known.
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

    def _resolve_child_workflow_cls_def(self, name: str, candidate: str | None) -> ast.ClassDef | None:
        """Find the child workflow's ``ClassDef`` in its candidate source file (memoized)."""
        if candidate is None:
            return None
        key = (name, candidate)
        if key in self._child_cls_def_cache:
            return self._child_cls_def_cache[key]
        result: ast.ClassDef | None = None
        src = self._file_resolver(candidate)
        if src is not None:
            try:
                tree = ast.parse(src)
            except SyntaxError:
                tree = None
            if tree is not None:
                result = next(
                    (
                        node
                        for node in tree.body
                        if isinstance(node, ast.ClassDef) and node.name == name and _is_workflow_cls_def(node)
                    ),
                    None,
                )
        self._child_cls_def_cache[key] = result
        return result

    def resolve_workflow_name(self, call: ast.Call) -> str | None:
        target = self._resolve_workflow_target(call)
        if target is None:
            return None
        class_name, candidate = target
        # Prefer the registered name from the child's ``@workflow.define(name=...)``;
        # fall back to the class name when the child's source isn't resolvable or the
        # decorator has no explicit name. Prefix it as runtime registration would so the
        # child_workflow_id matches the child's registered (dynamic/Atlas) identity.
        cls_def = self._resolve_child_workflow_cls_def(class_name, candidate)
        name = _workflow_define_name(cls_def) if cls_def is not None else None
        return _apply_workflow_name_prefix(name or class_name)

    def resolve_workflow_file(self, call: ast.Call) -> str | None:
        target = self._resolve_workflow_target(call)
        if target is None:
            return None
        name, candidate = target
        if self._resolve_child_workflow_cls_def(name, candidate) is not None:
            return candidate
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


def _walk_body_tree(
    stmts: list[ast.stmt],
    resolver: ActivityResolver,
    sources: dict[str, str],
    asts: dict[str, ast.Module],
    indices: dict[str, _FileIndex],
    file_path: str,
    workflow_name: str,
    ctx: _TreeCtx,
    file_ranges: dict[str, dict[str, int]],
) -> list[TreeNode]:
    src = sources.get(file_path, "")
    if not src:
        return []
    _register_source_file(file_path, src, sources, file_ranges)
    index = _get_index(file_path, sources, asts, indices)
    result: list[TreeNode] = []

    _gap_start: list[int | None] = [None]

    def _record_gap(stmt_idx: int) -> None:
        if _gap_start[0] is None:
            _gap_start[0] = stmt_idx

    def _flush_gap(up_to_stmt_idx: int) -> None:
        gs = _gap_start[0]
        if gs is None or up_to_stmt_idx < gs:
            return
        first_stmt = stmts[gs]
        last_stmt = stmts[up_to_stmt_idx]
        if getattr(first_stmt, "lineno", None) is None:
            _gap_start[0] = None
            return
        begin, _ = _ast_span(first_stmt, index)
        _, end = _ast_span(last_stmt, index)
        sr = _abs_range(file_ranges, file_path, begin, end, line=first_stmt.lineno)
        result.append(_make_ellipsis_node(ctx, workflow_name, sr))
        _gap_start[0] = None

    ctx = _scoped_binding_ctx(ctx)

    def _walk_lane(body: list[ast.stmt]) -> list[TreeNode]:
        return _walk_body_tree(body, resolver, sources, asts, indices, file_path, workflow_name, ctx, file_ranges)

    for idx, stmt in enumerate(stmts):
        _record_binding(stmt, ctx)

        if isinstance(stmt, ast.Return):
            _flush_gap(idx - 1)
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
                            _StepNode(
                                id=f"{workflow_name}::{name}@{ret_call.lineno}",
                                label=name,
                                source_range=_abs_range(file_ranges, file_path, cb, ce, line=ret_call.lineno),
                                connectors=resolver.resolve_activity_connectors(ret_call, sources, asts),
                            )
                        )
            return result

        if isinstance(stmt, ast.Raise):
            _flush_gap(idx - 1)
            raise_idx = ctx.raise_counter[0]
            ctx.raise_counter[0] += 1
            cb, ce = _ast_span(stmt, index)
            label = ast.unparse(stmt.exc) if stmt.exc is not None else "raise"
            if len(label) > 60:
                label = label[:59] + "…"
            result.append(
                _RaiseNode(
                    id=f"{workflow_name}::raise_{raise_idx}",
                    label=label,
                    source_range=_abs_range(file_ranges, file_path, cb, ce, line=stmt.lineno),
                )
            )
            return result

        if isinstance(stmt, ast.If):
            _flush_gap(idx - 1)
            cond_idx = ctx.cond_counter[0]
            ctx.cond_counter[0] += 1
            cb, ce = _ast_span(stmt, index)
            true_kind = _block_exit_kind(stmt.body)
            false_kind = _block_exit_kind(stmt.orelse)
            true_exits = true_kind is not None
            false_exits = false_kind is not None
            true_branch: list[TreeNode] = _walk_lane(stmt.body)
            false_branch: list[TreeNode] = _walk_lane(stmt.orelse if stmt.orelse else [])
            sr = _abs_range(file_ranges, file_path, cb, ce, line=stmt.lineno)
            if not true_exits and not bool(true_branch):
                true_branch = [_make_ellipsis_node(ctx, workflow_name, sr)]
            if stmt.orelse and not false_exits and not bool(false_branch):
                false_branch = [_make_ellipsis_node(ctx, workflow_name, sr)]
            rejoin = _walk_body_tree(
                stmts[idx + 1 :], resolver, sources, asts, indices, file_path, workflow_name, ctx, file_ranges
            )
            result.append(
                _ConditionalNode(
                    id=f"{workflow_name}::cond_{cond_idx}",
                    label=ast.unparse(stmt.test),
                    source_range=sr,
                    true_branch=true_branch,
                    true_exits=true_exits,
                    true_exit_error=true_kind == "raise",
                    false_branch=false_branch,
                    false_exits=false_exits,
                    false_exit_error=false_kind == "raise",
                    rejoin=rejoin,
                )
            )
            return result

        if isinstance(stmt, (ast.For, ast.AsyncFor, ast.While)):
            _flush_gap(idx - 1)
            cb, ce = _ast_span(stmt, index)
            if isinstance(stmt, ast.While):
                raw_label = f"while {ast.unparse(stmt.test)}"
            else:
                async_prefix = "async " if isinstance(stmt, ast.AsyncFor) else ""
                raw_label = f"{async_prefix}for {ast.unparse(stmt.target)} in {ast.unparse(stmt.iter)}"
            label = raw_label if len(raw_label) <= 60 else raw_label[:59] + "…"
            children = _walk_lane(stmt.body)
            sr = _abs_range(file_ranges, file_path, cb, ce, line=stmt.lineno)
            if not children:
                children = [_make_ellipsis_node(ctx, workflow_name, sr), *children]
            loop_idx = ctx.loop_counter[0]
            ctx.loop_counter[0] += 1
            result.append(
                _LoopNode(
                    id=f"{workflow_name}::loop_{loop_idx}",
                    label=label,
                    source_range=_abs_range(file_ranges, file_path, cb, ce, line=stmt.lineno),
                    children=children,
                )
            )
            continue

        if isinstance(stmt, (ast.With, ast.AsyncWith)):
            _flush_gap(idx - 1)
            result.extend(_walk_lane(stmt.body))
            continue

        if isinstance(stmt, ast.Try):
            _flush_gap(idx - 1)
            cb, ce = _ast_span(stmt, index)
            try_idx = ctx.try_counter[0]
            ctx.try_counter[0] += 1
            try_body: list[TreeNode] = _walk_lane(stmt.body)
            sr = _abs_range(file_ranges, file_path, cb, ce, line=stmt.lineno)
            if stmt.body and not try_body:
                try_body = [_make_ellipsis_node(ctx, workflow_name, sr)]
            handlers = [
                _TryExceptHandler(
                    exception_type=ast.unparse(h.type) if h.type else None,
                    body=_walk_lane(h.body),
                )
                for h in stmt.handlers
            ]
            finally_body = _walk_lane(stmt.finalbody) if stmt.finalbody else []
            result.append(
                _TryExceptNode(
                    id=f"{workflow_name}::try_{try_idx}",
                    source_range=sr,
                    try_body=try_body,
                    handlers=handlers,
                    finally_body=finally_body,
                )
            )
            continue

        call = _extract_call(stmt)
        if call is None:
            _record_gap(idx)
            continue

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

        if (
            isinstance(call.func, ast.Attribute)
            and call.func.attr == "wait_for_input"
            and isinstance(call.func.value, ast.Name)
            and call.func.value.id == "self"
        ):
            _flush_gap(idx - 1)
            hi_idx = ctx.human_input_counter[0]
            ctx.human_input_counter[0] += 1
            cb, ce = _ast_span(call, index)
            result.append(
                _HumanInputNode(
                    id=f"{workflow_name}::human_input_{hi_idx}",
                    label=_extract_hi_label(call) or "human_input",
                    source_range=_abs_range(file_ranges, file_path, cb, ce, line=call.lineno),
                )
            )
            continue

        if (
            isinstance(call.func, ast.Attribute)
            and isinstance(call.func.value, ast.Name)
            and call.func.value.id == "self"
            and call.func.attr != "wait_for_input"
        ):
            _flush_gap(idx - 1)
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
                        dataclasses.replace(
                            ctx,
                            cls_def=target.cls_def,
                            visited_methods=ctx.visited_methods | {method_name},
                            param_types=target.param_types,
                            local_funcs={},
                            name_values={},
                            inlined_funcs=frozenset(),
                        ),
                        file_ranges,
                    )
                    if bool(inlined) and _has_activity_nodes(inlined):
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

        if (
            isinstance(call.func, ast.Name)
            and call.func.id in ctx.local_funcs
            and call.func.id not in ctx.inlined_funcs
        ):
            _flush_gap(idx - 1)
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
            if bool(inlined) and _has_activity_nodes(inlined):
                result.extend(inlined)
            continue

        func_name = (
            call.func.attr
            if isinstance(call.func, ast.Attribute)
            else (call.func.id if isinstance(call.func, ast.Name) else None)
        )

        if func_name == "execute_workflow":
            _flush_gap(idx - 1)
            wf_name = resolver.resolve_workflow_name(call)
            cb, ce = _ast_span(call, index)
            if wf_name is not None:
                wf_file = resolver.resolve_workflow_file(call)
                result.append(
                    _StepNode(
                        id=f"{workflow_name}::{wf_name}@{call.lineno}",
                        label=wf_name,
                        child_workflow=True,
                        child_workflow_id=wf_name if wf_file is not None else None,
                        child_workflow_file=wf_file,
                        async_=fire_and_forget,
                        source_range=_abs_range(file_ranges, file_path, cb, ce, line=call.lineno),
                    )
                )
            else:
                sr = _abs_range(file_ranges, file_path, cb, ce, line=call.lineno)
                result.append(_make_ellipsis_node(ctx, workflow_name, sr))
            continue

        if _is_runner_run_call(call):
            _flush_gap(idx - 1)
            agent_idx = ctx.agent_counter[0]
            ctx.agent_counter[0] += 1
            agent_name, tools, handoffs, connector_exprs = _extract_agent_node_info(call, ctx)
            connectors = resolver.resolve_connector_names(connector_exprs, sources, asts)
            cb, ce = _ast_span(call, index)
            result.append(
                _AgentNode(
                    id=f"{workflow_name}::agent_{agent_idx}@{call.lineno}",
                    label=agent_name,
                    tools=tools,
                    handoffs=handoffs,
                    source_range=_abs_range(file_ranges, file_path, cb, ce, line=call.lineno),
                    connectors=connectors,
                )
            )
            continue

        if func_name == "continue_as_new":
            _flush_gap(idx - 1)
            cb, ce = _ast_span(call, index)
            result.append(
                _ContinueAsNewNode(
                    id=f"{workflow_name}::continue_as_new@{call.lineno}",
                    label="continue_as_new",
                    source_range=_abs_range(file_ranges, file_path, cb, ce, line=call.lineno),
                )
            )
            return result

        if isinstance(call.func, ast.Attribute) and call.func.attr == "wait_condition":
            _flush_gap(idx - 1)
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
                _WaitConditionNode(
                    id=f"{workflow_name}::wait_{wait_idx}",
                    label=label,
                    source_range=_abs_range(file_ranges, file_path, cb, ce, line=call.lineno),
                )
            )
            continue

        # Matches `workflow.sleep(...)` (and `temporalio.workflow.sleep(...)`) as well as
        # `asyncio.sleep(...)`. Temporal patches the workflow event loop so that
        # `asyncio.sleep` becomes a durable timer, so both are durable workflow timers.
        if isinstance(call.func, ast.Attribute) and call.func.attr == "sleep":
            _flush_gap(idx - 1)
            sleep_idx = ctx.sleep_counter[0]
            ctx.sleep_counter[0] += 1
            cb, ce = _ast_span(call, index)
            try:
                label = ast.unparse(call.args[0]) if call.args else "sleep"
            except Exception:
                label = "sleep"
            result.append(
                _SleepNode(
                    id=f"{workflow_name}::sleep_{sleep_idx}",
                    label=label,
                    source_range=_abs_range(file_ranges, file_path, cb, ce, line=call.lineno),
                )
            )
            continue

        if func_name == "execute_activities_in_parallel":
            _flush_gap(idx - 1)
            lane_exprs: list[ast.Call] = []
            if call.args and isinstance(call.args[0], ast.List):
                lane_exprs = _collect_lane_call_exprs(call.args[0].elts, ctx.name_values)
            par_node = _build_parallel_node(
                lane_exprs, call, _walk_lane, ctx, index, file_ranges, file_path, workflow_name
            )
            if par_node is not None:
                result.append(par_node)
            continue

        if (
            isinstance(call.func, ast.Attribute)
            and call.func.attr == "gather"
            and isinstance(call.func.value, ast.Name)
            and call.func.value.id == "asyncio"
        ):
            _flush_gap(idx - 1)
            lane_exprs = _collect_lane_call_exprs(call.args, ctx.name_values)
            par_node = _build_parallel_node(
                lane_exprs, call, _walk_lane, ctx, index, file_ranges, file_path, workflow_name
            )
            if par_node is not None:
                result.append(par_node)
            continue

        if isinstance(call.func, ast.Attribute) and call.func.attr in _MEMORY_OPS:
            _flush_gap(idx - 1)
            mem_idx = ctx.memory_counter[0]
            ctx.memory_counter[0] += 1
            cb, ce = _ast_span(call, index)
            result.append(
                _MemoryOpNode(
                    id=f"{workflow_name}::memory_{mem_idx}",
                    label=func_name or "memory_op",
                    source_range=_abs_range(file_ranges, file_path, cb, ce, line=call.lineno),
                )
            )
            continue

        name = resolver.resolve_activity(call, sources, asts)
        if name is not None:
            _flush_gap(idx - 1)
            cb, ce = _ast_span(call, index)
            result.append(
                _StepNode(
                    id=f"{workflow_name}::{name}@{call.lineno}",
                    label=name,
                    source_range=_abs_range(file_ranges, file_path, cb, ce, line=call.lineno),
                    connectors=resolver.resolve_activity_connectors(call, sources, asts),
                )
            )
            continue

        result_len_before = len(result)
        for awaited in _awaited_calls_in_order(stmt):
            awaited_name = resolver.resolve_activity(awaited, sources, asts)
            if awaited_name is not None:
                _flush_gap(idx - 1)
                cb, ce = _ast_span(awaited, index)
                result.append(
                    _StepNode(
                        id=f"{workflow_name}::{awaited_name}@{awaited.lineno}:{awaited.col_offset}",
                        label=awaited_name,
                        source_range=_abs_range(file_ranges, file_path, cb, ce, line=awaited.lineno),
                        connectors=resolver.resolve_activity_connectors(awaited, sources, asts),
                    )
                )

        if len(result) == result_len_before:
            _record_gap(idx)

    _flush_gap(len(stmts) - 1)
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


def _is_workflow_cls_def(cls_def: ast.ClassDef) -> bool:
    """Return True if the class has a @*.define(...) decorator (workflow class)."""
    for dec in cls_def.decorator_list:
        inner = dec.func if isinstance(dec, ast.Call) else dec
        if _decorator_leaf_name(inner) == "define":
            return True
    return False


def _workflow_define_name(cls_def: ast.ClassDef) -> str | None:
    """Return the registered name from a class's ``@*.define(...)`` decorator.

    Prefers the ``name=`` keyword, else the first positional argument. Returns
    ``None`` when there is no ``define(...)`` call decorator (e.g. a bare
    ``@workflow.define``) or the name is not a string literal — callers fall back
    to the class name.
    """
    for dec in cls_def.decorator_list:
        if not isinstance(dec, ast.Call) or _decorator_leaf_name(dec.func) != "define":
            continue
        name_expr = next((kw.value for kw in dec.keywords if kw.arg == "name"), None)
        if name_expr is None and dec.args:
            name_expr = dec.args[0]
        if name_expr is None:
            return None
        try:
            value = ast.literal_eval(name_expr)
        except (ValueError, SyntaxError):
            return None
        return value if isinstance(value, str) else None
    return None


def _apply_workflow_name_prefix(name: str) -> str:
    """Prefix ``name`` the way runtime registration does (see ``workflow.define``).

    Static graphs read names from the AST, but at runtime ``get_workflow_definition``
    reports names with ``workflow_name_prefix`` applied. Applying it here keeps static
    and dynamic workflow identities aligned (top-level names, child workflow IDs, and
    Atlas listing / ``/select``) when a prefix is configured.
    """
    return f"{config.worker.workflow_name_prefix}{name}"
