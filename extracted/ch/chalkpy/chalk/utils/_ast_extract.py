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
from typing import List, Tuple

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
