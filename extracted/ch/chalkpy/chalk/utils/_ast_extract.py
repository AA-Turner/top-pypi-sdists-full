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
from typing import List, Set, Tuple

DEFINITION_NODE_TYPES: Tuple[type, ...] = (
    ast.Import,
    ast.ImportFrom,
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.Assign,
    ast.AnnAssign,
)
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
    def __init__(self) -> None:
        super().__init__()
        self._comprehension_locals: list[Set[str]] = []

    def visit_Lambda(self, node: ast.Lambda) -> None:
        for default in node.args.defaults:
            self.visit(default)
        for default in node.args.kw_defaults:
            if default is not None:
                self.visit(default)

    def _visit_comprehension(self, node: ast.ListComp | ast.SetComp | ast.DictComp | ast.GeneratorExp) -> None:
        self._comprehension_locals.append(set())
        try:
            for generator in node.generators:
                self.visit(generator.iter)
                self._comprehension_locals[-1].update(
                    child.id
                    for child in ast.walk(generator.target)
                    if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Store)
                )
                for condition in generator.ifs:
                    self.visit(condition)
            if isinstance(node, ast.DictComp):
                self.visit(node.key)
                self.visit(node.value)
            else:
                self.visit(node.elt)
        finally:
            self._comprehension_locals.pop()

    def visit_ListComp(self, node: ast.ListComp) -> None:
        self._visit_comprehension(node)

    def visit_SetComp(self, node: ast.SetComp) -> None:
        self._visit_comprehension(node)

    def visit_DictComp(self, node: ast.DictComp) -> None:
        self._visit_comprehension(node)

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        self.visit(node.generators[0].iter)

    def _is_comprehension_local(self, name: str) -> bool:
        return any(name in local_names for local_names in reversed(self._comprehension_locals))


class _ExpressionNameVisitor(_ScopedExpressionVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.loaded: Set[str] = set()
        self.bound: Set[str] = set()

    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, ast.Load):
            if not self._is_comprehension_local(node.id):
                self.loaded.add(node.id)
        elif isinstance(node.ctx, ast.Store):
            self.bound.add(node.id)

    def visit_NamedExpr(self, node: ast.NamedExpr) -> None:
        self.bound.add(node.target.id)
        self.visit(node.value)


def find_free_names(expression: ast.expr) -> Set[str]:
    """Return names loaded by an expression but not bound within it."""
    visitor = _ExpressionNameVisitor()
    visitor.visit(expression)
    return visitor.loaded - visitor.bound


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

    def visit_NamedExpr(self, node: ast.NamedExpr) -> None:
        self.bound.add(node.target.id)
        self.visit(node.value)


def names_bound_by(statement: ast.stmt) -> Set[str]:
    """Return names bound at module scope if ``statement`` executes.

    Nested function, lambda, class, and comprehension scopes are not traversed.
    Function and class names, imports, and walrus targets in module-scope
    expressions are included.
    """
    visitor = _BoundNameVisitor()
    visitor.visit(statement)
    return visitor.bound


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
