"""Every action of every registered tool — derived, never hand-kept.

The surface-write census (``matrx_ai.tools.surface_write``) classifies each
``tool`` / ``tool:action`` as a text write, a structured write or not a write.
This module produces the list it classifies, from the code itself:

* a tool whose dispatch field (``action`` / ``command`` / ``op`` /
  ``operation``) is a ``Literal`` in its argument model — the Literal values;
* a tool whose dispatch field is a plain ``str`` — the string constants its
  implementation actually dispatches on: comparisons (``action == "get"``,
  ``action in ("a", "b")``), ``match action: case "x"``, and
  ``{"x": impl, ...}[action]`` dispatch tables, following the implementation's
  same-module helpers and any local name assigned from the dispatch field;
* a dispatcher whose actions live in a registry (``data_action``'s named
  operations) — the registry, read at import time (``REGISTRY_DISPATCH``).

A str-typed dispatcher whose actions cannot be derived is reported as
``<underivable>`` so the guard fails loudly instead of trusting a list someone
typed. Only the caller imports the declaration modules; this module has no host
imports (package boundary).
"""

from __future__ import annotations

import ast
import importlib.util
import typing
from pathlib import Path

from pydantic import BaseModel

from matrx_ai.tools.declared import declared_tools
from matrx_utils.module_loading import load_declared_module

DISPATCH_FIELDS = ("action", "command", "op", "operation")

#: Dispatchers whose actions are a registry's entries: tool -> (module,
#: callable returning the entries, attribute holding each entry's name, extra
#: fixed actions the dispatcher handles before the registry). The HOST
#: registers its own (``register_registry_dispatch``) — this package names no
#: host module. An unregistered registry dispatcher derives nothing and is
#: reported ``UNDERIVABLE``, so forgetting to register fails loudly.
REGISTRY_DISPATCH: dict[str, tuple[str, str, str, tuple[str, ...]]] = {}


def register_registry_dispatch(tool: str, module: str, fn: str, attr: str, fixed: tuple[str, ...] = ()) -> None:
    REGISTRY_DISPATCH[tool] = (module, fn, attr, fixed)

#: Tools with a str field named like a dispatcher that is NOT one — with why.
NOT_A_DISPATCHER: dict[str, str] = {
    "shell_execute": "`command` is the shell command line itself, not an action name",
}

UNDERIVABLE = "<underivable: its str dispatch field is compared to no constant>"


def _literals(tp: object) -> list[str]:
    if typing.get_origin(tp) is typing.Literal:
        return [str(a) for a in typing.get_args(tp)]
    out: list[str] = []
    for arg in typing.get_args(tp) or ():
        out += _literals(arg)
    return out


def _models(tp: object) -> list[type[BaseModel]]:
    if isinstance(tp, type) and issubclass(tp, BaseModel):
        return [tp]
    out: list[type[BaseModel]] = []
    for arg in typing.get_args(tp) or ():
        out += _models(arg)
    return out


def _variants(model: type[BaseModel]) -> list[type[BaseModel]]:
    root = model.model_fields.get("root")
    return _models(root.annotation) if root is not None else [model]


def _consts(node: ast.AST | None) -> list[str]:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, ast.Tuple | ast.List | ast.Set):
        return [c for e in node.elts for c in _consts(e)]
    return []


def _mentions_field(node: ast.AST, field: str, names: set[str]) -> bool:
    for sub in ast.walk(node):
        if isinstance(sub, ast.Attribute) and sub.attr == field:
            return True
        if isinstance(sub, ast.Name) and sub.id in names:
            return True
        if isinstance(sub, ast.Constant) and sub.value == field:
            # args["action"] / args.get("action")
            return True
    return False


def _is_dispatch(node: ast.AST, field: str, names: set[str]) -> bool:
    # `x`, `a.action`, `x.strip().lower()`, `(a.action or "").strip()`
    while isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
        node = node.func.value
    if isinstance(node, ast.BoolOp):
        return any(_is_dispatch(v, field, names) for v in node.values)
    if isinstance(node, ast.Name):
        return node.id in names
    if isinstance(node, ast.Attribute):
        return node.attr == field
    if isinstance(node, ast.Subscript):
        return _consts(node.slice) == [field]
    return False


def derive_str_actions(module: str, func: str, field: str) -> set[str]:
    """String constants ``func`` (and its same-module helpers) dispatch ``field`` on."""
    spec = importlib.util.find_spec(module)
    if spec is None or spec.origin is None:
        return set()
    tree = ast.parse(Path(spec.origin).read_text(encoding="utf-8"))
    defs = {n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef | ast.AsyncFunctionDef)}
    names = {field}
    found: set[str] = set()
    seen: set[str] = set()
    frontier = [func]
    for _ in range(5):
        nxt: list[str] = []
        for name in frontier:
            if name in seen or name not in defs:
                continue
            seen.add(name)
            body = defs[name]
            for sub in ast.walk(body):  # local aliases of the dispatch field
                if isinstance(sub, ast.Assign) and _mentions_field(sub.value, field, names):
                    names.update(t.id for t in sub.targets if isinstance(t, ast.Name))
            for sub in ast.walk(body):
                if isinstance(sub, ast.Compare) and _is_dispatch(sub.left, field, names):
                    for comp in sub.comparators:
                        found.update(_consts(comp))
                elif isinstance(sub, ast.Match) and _is_dispatch(sub.subject, field, names):
                    for case in sub.cases:
                        for pat in ast.walk(case.pattern):
                            if isinstance(pat, ast.MatchValue):
                                found.update(_consts(pat.value))
                elif isinstance(sub, ast.Subscript) and isinstance(sub.value, ast.Dict) and _is_dispatch(
                    sub.slice, field, names
                ):
                    found.update(k.value for k in sub.value.keys if isinstance(k, ast.Constant))
                elif isinstance(sub, ast.Call):
                    f = sub.func
                    callee = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else None
                    if callee:
                        nxt.append(callee)
        frontier = nxt
    return found


def _registry_actions(tool: str) -> list[str]:
    module, fn, attr, fixed = REGISTRY_DISPATCH[tool]
    entries = getattr(load_declared_module(module), fn)()
    return sorted({*fixed, *(str(getattr(e, attr)) for e in entries)})


def tool_actions() -> dict[str, list[str] | None]:
    """tool -> its actions; ``None`` when the tool is a single operation."""
    found: dict[str, list[str] | None] = {}
    for name, declared in declared_tools().items():
        literal: set[str] = set()
        str_field: str | None = None
        for variant in _variants(declared.args_model):
            for field in DISPATCH_FIELDS:
                info = variant.model_fields.get(field)
                if info is None:
                    continue
                lits = _literals(info.annotation)
                if lits:
                    literal.update(lits)
                elif info.annotation is str:
                    str_field = field
        if literal:
            found[name] = sorted(literal)
        elif name in REGISTRY_DISPATCH:
            found[name] = _registry_actions(name)
        elif str_field and name not in NOT_A_DISPATCHER:
            derived = derive_str_actions(declared.module, declared.qualname, str_field)
            found[name] = sorted(derived) if derived else [UNDERIVABLE]
        else:
            found[name] = None
    return found


def census_keys() -> list[str]:
    keys: list[str] = []
    for tool, actions in tool_actions().items():
        keys += [tool] if actions is None else [f"{tool}:{a}" for a in actions]
    return keys
