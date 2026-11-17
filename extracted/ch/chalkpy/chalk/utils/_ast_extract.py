"""Shared AST primitives for shipping user-defined Python sources to a remote
container.

Both `chalk/utils/notebook.py` (training-script reconstruction from Jupyter
cell history) and `chalk/client/model_image.py` (``@model_handler`` image-build
staging) need to keep the same notion of "module-level definition" — anything
that introduces a name at module scope — and drop side-effect statements
(top-level calls, control flow, training loops) so the container doesn't
re-run them on import. The two consumers have different downstream shapes
(name-keyed dicts vs. an unparsed ``ast.Module``), so this module deliberately
exposes only the **primitives** they share; the assembly stays in each caller.
"""

from __future__ import annotations

import ast
from typing import Any, Dict, List, Optional, Set, Tuple

_TYPE_ALIAS: Optional[type] = getattr(ast, "TypeAlias", None)

DEFINITION_NODE_TYPES: Tuple[type, ...] = (
    ast.Import,
    ast.ImportFrom,
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.Assign,
    ast.AnnAssign,
) + ((_TYPE_ALIAS,) if _TYPE_ALIAS is not None else ())
"""Node kinds that introduce a name at module scope. Anything *not* in this
tuple is treated as a side-effect statement and dropped by staging."""


def is_module_level_definition(node: ast.stmt) -> bool:
    """True if ``node`` is a top-level definition we ship to a remote container.

    Drops ``If`` / ``For`` / ``While`` / ``Try`` / ``Expr`` and other
    side-effect statements so the container doesn't re-run training loops,
    ``main()`` calls, ``ChalkClient()`` instantiation, etc., on import.

    Also drops ``Assign`` / ``AnnAssign`` whose right-hand side contains a
    function call. Top-level assignments with calls are almost always
    side-effecting in scripts (``client = ChalkClient()``, ``rf =
    RandomForestRegressor()``, ``result = client.register_model_version(...)``).
    Re-executing them on container import either crashes (auth missing,
    GPU missing, data file missing) or silently re-runs training / re-issues
    API calls — both worse than just losing access to the bound name.
    Constants, names, tuples, lists, sets, dicts, and type aliases like
    ``MyType = List[int]`` (no ``Call``) still pass through.

    Notably *also* drops ``try: import torch except ImportError: ...`` patterns
    — the ``Try`` node isn't a definition. Users relying on those should
    refactor to a real module instead of a script.
    """
    if not isinstance(node, DEFINITION_NODE_TYPES):
        return False
    if isinstance(node, (ast.Assign, ast.AnnAssign)):
        value = node.value
        if value is not None and any(isinstance(n, ast.Call) for n in ast.walk(value)):
            return False
    return True


class _ScopedExpressionVisitor(ast.NodeVisitor):
    def visit_Lambda(self, node: ast.Lambda) -> None:
        for default in node.args.defaults:
            self.visit(default)
        for default in node.args.kw_defaults:
            if default is not None:
                self.visit(default)

    def _visit_comprehension(self, node: ast.ListComp | ast.SetComp | ast.DictComp | ast.GeneratorExp) -> None:
        for generator in node.generators:
            self.visit(generator.iter)
            for condition in generator.ifs:
                self.visit(condition)
        if isinstance(node, ast.DictComp):
            self.visit(node.key)
            self.visit(node.value)
        else:
            self.visit(node.elt)

    def visit_ListComp(self, node: ast.ListComp) -> None:
        self._visit_comprehension(node)

    def visit_SetComp(self, node: ast.SetComp) -> None:
        self._visit_comprehension(node)

    def visit_DictComp(self, node: ast.DictComp) -> None:
        self._visit_comprehension(node)

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        self.visit(node.generators[0].iter)


class _BoundNameVisitor(_ScopedExpressionVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.bound: Set[str] = set()

    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, ast.Store):
            self.bound.add(node.id)

    def _visit_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        self.bound.add(node.name)
        for decorator in node.decorator_list:
            self.visit(decorator)
        for default in node.args.defaults:
            self.visit(default)
        for default in node.args.kw_defaults:
            if default is not None:
                self.visit(default)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_function(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.bound.add(node.name)
        for decorator in node.decorator_list:
            self.visit(decorator)
        for base in node.bases:
            self.visit(base)
        for keyword in node.keywords:
            self.visit(keyword.value)

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.bound.add(alias.asname or alias.name.split(".", 1)[0])

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        for alias in node.names:
            if alias.name != "*":
                self.bound.add(alias.asname or alias.name)

    def visit_TypeAlias(self, node: Any) -> None:
        self.visit(node.name)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        if node.name is not None:
            self.bound.add(node.name)
        self.generic_visit(node)

    def visit_MatchAs(self, node: ast.MatchAs) -> None:
        if node.name is not None:
            self.bound.add(node.name)
        self.generic_visit(node)

    def visit_MatchStar(self, node: ast.MatchStar) -> None:
        if node.name is not None:
            self.bound.add(node.name)

    def visit_MatchMapping(self, node: ast.MatchMapping) -> None:
        if node.rest is not None:
            self.bound.add(node.rest)
        self.generic_visit(node)

    def visit_NamedExpr(self, node: ast.NamedExpr) -> None:
        self.bound.add(node.target.id)
        self.visit(node.value)


def names_bound_by(statement: ast.stmt) -> Set[str]:
    """Return names bound at module scope if ``statement`` executes.

    Nested function, lambda, class, and comprehension scopes are not traversed.
    Function and class names, imports, and walrus targets in module-scope
    expressions are included.
    """
    if isinstance(statement, ast.AnnAssign) and statement.value is None:
        return set()
    visitor = _BoundNameVisitor()
    visitor.visit(statement)
    return visitor.bound


class _FunctionBindingVisitor(_BoundNameVisitor):
    """Collect bindings in one function scope without entering child scopes."""

    def __init__(self) -> None:
        super().__init__()
        self.globals: Set[str] = set()
        self.nonlocals: Set[str] = set()

    def visit_Global(self, node: ast.Global) -> None:
        self.globals.update(node.names)

    def visit_Nonlocal(self, node: ast.Nonlocal) -> None:
        self.nonlocals.update(node.names)

    def _visit_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        super()._visit_function(node)
        for annotation in _function_annotations(node):
            self.visit(annotation)

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        self._visit_comprehension(node)


def _argument_names(arguments: ast.arguments) -> Set[str]:
    args = [*arguments.posonlyargs, *arguments.args, *arguments.kwonlyargs]
    names = {arg.arg for arg in args}
    if arguments.vararg is not None:
        names.add(arguments.vararg.arg)
    if arguments.kwarg is not None:
        names.add(arguments.kwarg.arg)
    return names


def _function_annotations(node: ast.FunctionDef | ast.AsyncFunctionDef) -> List[ast.expr]:
    annotations = [
        arg.annotation
        for arg in [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]
        if arg.annotation is not None
    ]
    if node.args.vararg is not None and node.args.vararg.annotation is not None:
        annotations.append(node.args.vararg.annotation)
    if node.args.kwarg is not None and node.args.kwarg.annotation is not None:
        annotations.append(node.args.kwarg.annotation)
    if node.returns is not None:
        annotations.append(node.returns)
    return annotations


class _StatementReferenceVisitor(ast.NodeVisitor):
    """Find references from one statement, preserving Python's lexical scopes."""

    def __init__(
        self,
        *,
        kind: str = "module",
        local_names: Set[str] | None = None,
        global_names: Set[str] | None = None,
        nonlocal_names: Set[str] | None = None,
        enclosing_function_locals: Tuple[Set[str], ...] = (),
        class_bound: Set[str] | None = None,
        annotations_are_deferred: bool = False,
        hard: Set[str] | None = None,
        late: Set[str] | None = None,
        soft: Set[str] | None = None,
        soft_context: bool = False,
        late_context: bool = False,
    ) -> None:
        super().__init__()
        self.kind = kind
        self.local_names = local_names if local_names is not None else set()
        self.global_names = global_names if global_names is not None else set()
        self.nonlocal_names = nonlocal_names if nonlocal_names is not None else set()
        self.enclosing_function_locals = enclosing_function_locals
        self.class_bound = class_bound if class_bound is not None else set()
        self.annotations_are_deferred = annotations_are_deferred
        self.hard = hard if hard is not None else set()
        self.late = late if late is not None else set()
        self.soft = soft if soft is not None else set()
        self.soft_context = soft_context
        self.late_context = late_context

    def _spawn(self, **changes: object) -> "_StatementReferenceVisitor":
        options: Dict[str, Any] = {
            "kind": self.kind,
            "local_names": self.local_names,
            "global_names": self.global_names,
            "nonlocal_names": self.nonlocal_names,
            "enclosing_function_locals": self.enclosing_function_locals,
            "class_bound": self.class_bound,
            "annotations_are_deferred": self.annotations_are_deferred,
            "hard": self.hard,
            "late": self.late,
            "soft": self.soft,
            "soft_context": self.soft_context,
            "late_context": self.late_context,
        }
        options.update(changes)
        return _StatementReferenceVisitor(**options)

    def _is_module_reference(self, name: str) -> bool:
        if self.kind == "module":
            return True
        if self.kind == "class":
            if name in self.class_bound:
                return False
            return not any(name in scope for scope in reversed(self.enclosing_function_locals))
        if name in self.global_names:
            return True
        if name in self.local_names or name in self.nonlocal_names:
            return False
        return not any(name in scope for scope in reversed(self.enclosing_function_locals))

    def _record(self, name: str) -> None:
        if not self._is_module_reference(name):
            return
        if self.soft_context:
            self.soft.add(name)
        elif self.late_context:
            self.late.add(name)
        else:
            self.hard.add(name)

    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, ast.Load):
            self._record(node.id)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        if isinstance(node.target, ast.Name):
            self._record(node.target.id)
        else:
            self.visit(node.target)
        self.visit(node.value)

    def visit_NamedExpr(self, node: ast.NamedExpr) -> None:
        self.visit(node.value)
        self.visit(node.target)

    def _visit_annotation(self, annotation: ast.expr) -> None:
        if self.annotations_are_deferred:
            self._spawn(soft_context=True).visit(annotation)
        else:
            self.visit(annotation)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if not isinstance(node.target, ast.Name):
            self.visit(node.target)
        if self.kind != "function":
            self._visit_annotation(node.annotation)
        if node.value is not None:
            self.visit(node.value)

    def visit_TypeAlias(self, node: Any) -> None:
        type_parameter_names = {parameter.name for parameter in node.type_params}
        child = self._spawn(kind="function", local_names=type_parameter_names)
        for parameter in node.type_params:
            bound = getattr(parameter, "bound", None)
            if bound is not None:
                child.visit(bound)
            default_value = getattr(parameter, "default_value", None)
            if default_value is not None:
                child.visit(default_value)
        child.visit(node.value)

    def _enclosing_locals_for_child(self) -> Tuple[Set[str], ...]:
        if self.kind in {"function", "comprehension"}:
            return (*self.enclosing_function_locals, self.local_names)
        return self.enclosing_function_locals

    def _visit_function_header(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        for decorator in node.decorator_list:
            self.visit(decorator)
        for default in node.args.defaults:
            self.visit(default)
        for default in node.args.kw_defaults:
            if default is not None:
                self.visit(default)
        for annotation in _function_annotations(node):
            self._visit_annotation(annotation)

    def _visit_function_body(
        self, arguments: ast.arguments, body: List[ast.stmt], *, lambda_body: ast.expr | None = None
    ) -> None:
        binding_visitor = _FunctionBindingVisitor()
        for statement in body:
            binding_visitor.visit(statement)
        if lambda_body is not None:
            binding_visitor.visit(lambda_body)
        local_names = _argument_names(arguments) | binding_visitor.bound
        local_names -= binding_visitor.globals | binding_visitor.nonlocals
        child = self._spawn(
            kind="function",
            local_names=local_names,
            global_names=binding_visitor.globals,
            nonlocal_names=binding_visitor.nonlocals,
            enclosing_function_locals=self._enclosing_locals_for_child(),
            class_bound=set(),
            soft_context=False,
            late_context=True,
        )
        if lambda_body is not None:
            child.visit(lambda_body)
        else:
            for statement in body:
                child.visit(statement)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_function_header(node)
        self._visit_function_body(node.args, node.body)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_function_header(node)
        self._visit_function_body(node.args, node.body)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        for default in node.args.defaults:
            self.visit(default)
        for default in node.args.kw_defaults:
            if default is not None:
                self.visit(default)
        self._visit_function_body(node.args, [], lambda_body=node.body)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        for decorator in node.decorator_list:
            self.visit(decorator)
        for base in node.bases:
            self.visit(base)
        for keyword in node.keywords:
            self.visit(keyword.value)

        class_bound: Set[str] = set()
        for statement in node.body:
            child = self._spawn(
                kind="class",
                local_names=set(),
                global_names=set(),
                nonlocal_names=set(),
                enclosing_function_locals=self._enclosing_locals_for_child(),
                class_bound=set(class_bound),
                soft_context=False,
            )
            child.visit(statement)
            class_bound.update(names_bound_by(statement))

    def _visit_comprehension(self, node: ast.ListComp | ast.SetComp | ast.DictComp | ast.GeneratorExp) -> None:
        self.visit(node.generators[0].iter)
        local_names: Set[str] = set()
        child = self._spawn(
            kind="comprehension",
            local_names=local_names,
            global_names=set(),
            nonlocal_names=set(),
            enclosing_function_locals=self._enclosing_locals_for_child(),
            class_bound=set(),
            soft_context=False,
        )
        for index, generator in enumerate(node.generators):
            if index > 0:
                child.visit(generator.iter)
            local_names.update(
                descendant.id
                for descendant in ast.walk(generator.target)
                if isinstance(descendant, ast.Name) and isinstance(descendant.ctx, ast.Store)
            )
            for condition in generator.ifs:
                child.visit(condition)
        if isinstance(node, ast.DictComp):
            child.visit(node.key)
            child.visit(node.value)
        else:
            child.visit(node.elt)

    visit_ListComp = _visit_comprehension
    visit_SetComp = _visit_comprehension
    visit_DictComp = _visit_comprehension
    visit_GeneratorExp = _visit_comprehension


def find_statement_free_names_with_context(
    statement: ast.stmt, annotations_are_deferred: bool
) -> Tuple[Set[str], Set[str], Set[str]]:
    """Return eager, function-body, and deferred-annotation references."""
    visitor = _StatementReferenceVisitor(annotations_are_deferred=annotations_are_deferred)
    visitor.visit(statement)
    visitor.late.difference_update(visitor.hard)
    visitor.soft.difference_update(visitor.hard | visitor.late)
    return visitor.hard, visitor.late, visitor.soft


def find_relative_imports(tree: ast.Module) -> List[ast.ImportFrom]:
    """Return module-level ``from .x import y`` / ``from ..x import y`` nodes.

    Chalk's `@model_handler` staging ships a single source file into the
    container, so sibling modules referenced via relative imports never arrive
    and the container hits ``ImportError`` at startup. Call sites should use
    this to fail fast at registration time with a clear message instead.

    Only inspects top-level statements; relative imports inside ``if
    TYPE_CHECKING:`` blocks or function bodies are not reported (they're
    typically harmless or already deferred to runtime imports).
    """
    return [node for node in tree.body if isinstance(node, ast.ImportFrom) and (node.level or 0) > 0]
