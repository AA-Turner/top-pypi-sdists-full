"""The CHEAP FIRST LINE against a turn-only change reaching the stored chat (CGU-10 IMG9 #2).

The real guarantee is behavioural: ``UnifiedConfig.to_storage_dict`` stores the route baseline
whenever the model, class pin or device moved outside the sanctioned doors, and says so
(``stored_route_unsanctioned_write``). This static scan only catches the obvious shapes early, in
review, before anything runs.

It is scope-aware by construction: no line-order heuristic. A stand-in model is written ONLY by the
helpers in ``matrx_ai.config.unified_config`` (``model_this_turn_only`` / ``swap_model_this_turn_only``,
which open the snapshot and write in one call), and a chosen model only by ``apply_overrides`` /
``adopt_model_for_conversation``. So ANY other write to a config's route — whatever came before it in
the function — is a finding. Shapes: assignment (plain, augmented, annotated, tuple), ``setattr``
(constant, computed, through a lambda or a ``getattr``-fetched setter), ``__dict__`` updates,
``dataclasses.replace`` / ``model_copy(update=...)`` naming a route field, and every one of them
through an alias (``cfg = r.config``) — and through ANY name that is a config by type or flow
(CGU-10 AND-IMG11): a parameter or annotated name typed ``UnifiedConfig``, a ``UnifiedConfig(...)`` /
``UnifiedConfig.<factory>(...)`` result, or a copy of a config (``uc = deepcopy(config)``). Belt fields (``tools`` / ``custom_tools``) are scanned only
where the STORED config is handed over mid-turn (``belt=True``): assignment and in-place list
mutation (``append``, ``remove``, ``clear``, ``extend``, ``insert``, ``pop``, slice assignment).
"""

from __future__ import annotations

import ast
import re
from collections.abc import Iterable
from pathlib import Path

ROUTE_FIELDS = frozenset({"model", "offering_id", "runtime_offering_id", "served_via"})
BELT_FIELDS = frozenset({"tools", "custom_tools"})
_LIST_MUTATORS = frozenset({"append", "remove", "clear", "extend", "insert", "pop"})
#: A name that holds a config (``config``, ``request_config``, ``cfg``, ``self._cfg`` — AND-IMG12 #4).
_CONFIG_NAME = re.compile(r"(^|_)(config|cfg)$")
#: A name that holds SEVERAL configs (``configs``, ``child_configs``): ``configs[0]`` and a loop variable
#: over it are configs (AND-IMG12 #4).
_CONFIGS_NAME = re.compile(r"(^|_)(configs|cfgs)$")


def _is_configs_expr(node: ast.AST) -> bool:
    if isinstance(node, ast.Attribute):
        return bool(_CONFIGS_NAME.search(node.attr))
    return isinstance(node, ast.Name) and bool(_CONFIGS_NAME.search(node.id))


def _is_config_expr(node: ast.AST, aliases: set[str]) -> bool:
    if isinstance(node, ast.Attribute):
        return node.attr == "config" or bool(_CONFIG_NAME.search(node.attr))
    if isinstance(node, ast.Name):
        return bool(_CONFIG_NAME.search(node.id)) or node.id in aliases
    if isinstance(node, ast.Subscript):
        return _is_configs_expr(node.value)
    return False


#: The config TYPE (CGU-10 AND-IMG11): a name is a config by what it IS, not only what it is called —
#: ``uc: UnifiedConfig``, ``uc = UnifiedConfig(...)``, ``uc = UnifiedConfig.from_dict(...)``,
#: ``uc = copy.deepcopy(config)``, ``uc = config.model_copy()``.
_CONFIG_TYPES = frozenset({"UnifiedConfig"})
_COPIERS = frozenset({"deepcopy", "copy", "model_copy", "clone"})


def _annotation_is_config(annotation: ast.AST | None) -> bool:
    if annotation is None:
        return False
    for leaf in ast.walk(annotation):
        if isinstance(leaf, ast.Name) and leaf.id in _CONFIG_TYPES:
            return True
        if isinstance(leaf, ast.Attribute) and leaf.attr in _CONFIG_TYPES:
            return True
        if isinstance(leaf, ast.Constant) and isinstance(leaf.value, str):
            try:
                if _annotation_is_config(ast.parse(leaf.value, mode="eval").body):
                    return True
            except SyntaxError:
                continue
    return False


def _is_config_type(node: ast.AST) -> bool:
    return (isinstance(node, ast.Name) and node.id in _CONFIG_TYPES) or (
        isinstance(node, ast.Attribute) and node.attr in _CONFIG_TYPES
    )


def _makes_config(value: ast.AST, aliases: set[str]) -> bool:
    """A value that IS a config: a config expression, ``UnifiedConfig(...)`` / ``UnifiedConfig.<factory>(...)``,
    or a copy of a config (``deepcopy(cfg)``, ``copy.copy(cfg)``, ``cfg.model_copy()``)."""
    if _is_config_expr(value, aliases):
        return True
    if isinstance(value, ast.Await):
        return _makes_config(value.value, aliases)
    if not isinstance(value, ast.Call):
        return False
    callee = value.func
    if _is_config_type(callee):
        return True
    if isinstance(callee, ast.Attribute) and _is_config_type(callee.value):
        return True  # UnifiedConfig.from_dict / model_validate / model_construct …
    name = callee.attr if isinstance(callee, ast.Attribute) else getattr(callee, "id", "")
    if name in _COPIERS:
        if isinstance(callee, ast.Attribute) and name in ("model_copy", "copy", "clone") and _is_config_expr(callee.value, aliases):
            return True
        return bool(value.args) and _is_config_expr(value.args[0], aliases)
    return False


def typed_config_names(func: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    """The function's parameters annotated as a config (``uc: UnifiedConfig``, ``"UnifiedConfig | None"``)."""
    args = func.args
    params = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    return {a.arg for a in params if _annotation_is_config(a.annotation)}


def _aliases(func: ast.AST, seed: Iterable[str] = ()) -> set[str]:
    """Names bound (anywhere in the function) to a config: ``cfg = r.config``, a parameter or an annotated
    name typed ``UnifiedConfig``, a ``UnifiedConfig(...)`` / factory result, a copy of a config."""
    found: set[str] = set(seed)
    changed = True
    while changed:
        changed = False
        for node in ast.walk(func):
            targets: list[ast.AST] = []
            if isinstance(node, ast.Assign) and _makes_config(node.value, found):
                targets = list(node.targets)
            elif isinstance(node, ast.AnnAssign) and (
                _annotation_is_config(node.annotation) or (node.value is not None and _makes_config(node.value, found))
            ):
                targets = [node.target]
            elif isinstance(node, ast.NamedExpr) and _makes_config(node.value, found):
                targets = [node.target]
            elif (
                isinstance(node, ast.Assign)
                and isinstance(node.value, ast.Tuple)
                and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Tuple)
                and len(node.targets[0].elts) == len(node.value.elts)
            ):
                # ``uc, n = config, 1`` (AND-IMG12 #4): pairwise.
                targets = [t for t, v in zip(node.targets[0].elts, node.value.elts, strict=True) if _makes_config(v, found)]
            elif isinstance(node, (ast.For, ast.AsyncFor)) and _is_configs_expr(node.iter):
                targets = [node.target]  # ``for uc in configs``
            elif isinstance(node, (ast.With, ast.AsyncWith)):
                targets = [
                    item.optional_vars
                    for item in node.items
                    if item.optional_vars is not None and _makes_config(item.context_expr, found)
                ]
            for target in targets:
                if isinstance(target, ast.Name) and target.id not in found:
                    found.add(target.id)
                    changed = True
    return found


def _constant_loop_names(func: ast.AST) -> dict[str, set[str]]:
    """``for name in ("a", "b"):`` — the loop variable can only be those names."""
    found: dict[str, set[str]] = {}
    for node in ast.walk(func):
        if isinstance(node, (ast.For, ast.AsyncFor)) and isinstance(node.target, ast.Name):
            if isinstance(node.iter, (ast.Tuple, ast.List, ast.Set)) and all(
                _const(e) is not None for e in node.iter.elts
            ):
                found.setdefault(node.target.id, set()).update(_const(e) for e in node.iter.elts)  # type: ignore[misc]
    return found


def _setter_aliases(func: ast.AST, aliases: set[str]) -> set[str]:
    """``s = getattr(config, "__setattr__")`` / ``s = config.__setattr__`` /
    ``s = functools.partial(setattr, config)``: calling ``s`` writes the config."""
    found: set[str] = set()
    for node in ast.walk(func):
        if not (isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)):
            continue
        value = node.value
        fetched = (
            isinstance(value, ast.Attribute) and value.attr == "__setattr__" and _is_config_expr(value.value, aliases)
        ) or (
            isinstance(value, ast.Call)
            and isinstance(value.func, ast.Name)
            and value.func.id == "getattr"
            and len(value.args) >= 2
            and _is_config_expr(value.args[0], aliases)
            and _const(value.args[1]) == "__setattr__"
        ) or (
            isinstance(value, ast.Call)
            and getattr(value.func, "attr", getattr(value.func, "id", "")) == "partial"
            and len(value.args) >= 2
            and isinstance(value.args[0], ast.Name)
            and value.args[0].id == "setattr"
            and _is_config_expr(value.args[1], aliases)
        )
        if fetched:
            found.add(node.targets[0].id)
    return found


def _const(node: ast.AST | None) -> str | None:
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def _findings_in_function(
    func: ast.AST, label: str, *, fields: frozenset[str], belt: bool, typed: Iterable[str] = ()
) -> list[str]:
    aliases = _aliases(func, typed)
    setters = _setter_aliases(func, aliases)
    loop_names = _constant_loop_names(func)
    out: list[str] = []

    def hit(line: int, what: str) -> None:
        out.append(f"{label}:{line} {what}")

    for node in ast.walk(func):
        # Assignment shapes (incl. tuple targets and slice assignment of a belt list).
        if isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                for leaf in ast.walk(target):
                    # ``vars(config)["model"] = …`` / ``config.__dict__["model"] = …`` (AND-IMG12 #4).
                    if isinstance(leaf, ast.Subscript) and _const(leaf.slice) in fields and (
                        (
                            isinstance(leaf.value, ast.Call)
                            and getattr(leaf.value.func, "id", "") == "vars"
                            and leaf.value.args
                            and _is_config_expr(leaf.value.args[0], aliases)
                        )
                        or (
                            isinstance(leaf.value, ast.Attribute)
                            and leaf.value.attr == "__dict__"
                            and _is_config_expr(leaf.value.value, aliases)
                        )
                    ):
                        hit(node.lineno, f"writes config.__dict__[{_const(leaf.slice)!r}] directly")
                    if isinstance(leaf, ast.Attribute) and _is_config_expr(leaf.value, aliases):
                        if leaf.attr in fields:
                            hit(node.lineno, f"writes config.{leaf.attr} outside the turn-only helpers")
                        elif belt and leaf.attr in BELT_FIELDS:
                            hit(node.lineno, f"writes config.{leaf.attr} bare")
        if not isinstance(node, ast.Call):
            continue
        func_node = node.func
        if isinstance(func_node, ast.Name) and func_node.id in setters:
            field = _const(node.args[0]) if node.args else None
            if (field is None and belt) or (field is not None and (field in fields or (belt and field in BELT_FIELDS))):
                hit(node.lineno, f"a fetched setter writes config.{field or '<computed>'} outside the turn-only helpers")
        # setattr(config, "model", …) / setattr(config, name, …) / a lambda or alias of setattr.
        is_setattr = (isinstance(func_node, ast.Name) and func_node.id == "setattr") or (
            isinstance(func_node, ast.Attribute) and func_node.attr in ("__setattr__",)
        )
        # ``object.__setattr__(config, "model", …)`` passes the config first, like ``setattr`` (AND-IMG12 #4).
        unbound = (
            isinstance(func_node, ast.Attribute)
            and func_node.attr == "__setattr__"
            and isinstance(func_node.value, ast.Name)
            and func_node.value.id in ("object", "type", "super")
        )
        if is_setattr and node.args:
            positional = isinstance(func_node, ast.Name) or unbound
            target = node.args[0] if positional else func_node.value
            name_arg = node.args[1] if positional and len(node.args) > 1 else (
                node.args[0] if not positional else None
            )
            if _is_config_expr(target, aliases):
                field = _const(name_arg)
                if field is None and isinstance(name_arg, ast.Name) and name_arg.id in loop_names:
                    names = loop_names[name_arg.id]
                    hits = sorted(names & (fields | (BELT_FIELDS if belt else frozenset())))
                    if hits:
                        hit(node.lineno, f"setattr(config, {hits[0]}, …) outside the turn-only helpers")
                    continue
                # A computed name (a settings loop) is flagged only where the STORED config is handed
                # over mid-turn (``belt``); elsewhere the behavioural layer judges what it wrote.
                if (field is None and belt) or (field is not None and (field in fields or (belt and field in BELT_FIELDS))):
                    hit(node.lineno, f"setattr(config, {field or '<computed>'!s}, …) outside the turn-only helpers")
        # config.__dict__.update(...) / vars(config).update(...)
        if (
            isinstance(func_node, ast.Attribute)
            and func_node.attr in ("update", "__setitem__", "setdefault")
            and (
                (
                    isinstance(func_node.value, ast.Attribute)
                    and func_node.value.attr == "__dict__"
                    and _is_config_expr(func_node.value.value, aliases)
                )
                or (
                    isinstance(func_node.value, ast.Call)
                    and getattr(func_node.value.func, "id", "") == "vars"
                    and func_node.value.args
                    and _is_config_expr(func_node.value.args[0], aliases)
                )
            )
        ):
            hit(node.lineno, "writes config.__dict__ directly")
        # replace(config, model=…) / config.model_copy(update={"model": …}).
        callee = func_node.attr if isinstance(func_node, ast.Attribute) else getattr(func_node, "id", "")
        if callee in ("replace", "evolve") and node.args and _is_config_expr(node.args[0], aliases):
            named = {kw.arg for kw in node.keywords}
            if named & fields:
                hit(node.lineno, f"{callee}(config, {', '.join(sorted(named & fields))}=…) outside the turn-only helpers")
        if callee == "model_copy" and isinstance(func_node, ast.Attribute) and _is_config_expr(func_node.value, aliases):
            for kw in node.keywords:
                if kw.arg == "update" and isinstance(kw.value, ast.Dict):
                    keys = {_const(k) for k in kw.value.keys}
                    if keys & fields:
                        hit(node.lineno, "model_copy(update=…) moves the route outside the turn-only helpers")
        # In-place belt mutation: config.tools.append(...) etc.
        if (
            belt
            and isinstance(func_node, ast.Attribute)
            and func_node.attr in _LIST_MUTATORS
            and isinstance(func_node.value, ast.Attribute)
            and func_node.value.attr in BELT_FIELDS
            and _is_config_expr(func_node.value.value, aliases)
        ):
            hit(node.lineno, f"mutates config.{func_node.value.attr}.{func_node.attr}() in place")
    # A setter fetched or wrapped: ``s = getattr(config, "__setattr__")`` / ``lambda: setattr(config, …)``
    # are covered by the walk above (the lambda body is walked; a fetched ``__setattr__`` is a call
    # on an alias of ``config``).
    return out


def scan_source(
    source: str,
    module_label: str,
    *,
    functions: Iterable[str] | None = None,
    belt: bool = False,
    allowed: dict[str, str] | None = None,
    fields: frozenset[str] = ROUTE_FIELDS,
) -> list[str]:
    """Every route write (and, with ``belt``, belt write) in ``source`` outside the helpers.

    ``functions`` limits the scan to those function names; ``allowed`` maps a
    ``"<module>.<function>"`` to the reason it may write (each entry must still be found, so a
    stale waiver fails — see :func:`stale_waivers`)."""
    tree = ast.parse(source)
    only = set(functions) if functions is not None else None
    allowed = allowed or {}
    out: list[str] = []
    for func in ast.walk(tree):
        if not isinstance(func, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if only is not None and func.name not in only:
            continue
        if f"{module_label}.{func.name}" in allowed:
            continue
        # Only the function's own body: a nested def is scanned as its own function.
        body = ast.Module(
            body=[n for n in func.body if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))],
            type_ignores=[],
        )
        out += _findings_in_function(
            body, f"{module_label}.{func.name}", fields=fields, belt=belt, typed=typed_config_names(func)
        )
    return sorted(set(out))


def scan_tree(
    root: Path,
    package_label: str,
    *,
    allowed: dict[str, str] | None = None,
    skip_modules: Iterable[str] = (),
    skip_parts: Iterable[str] = ("tests", "__pycache__"),
) -> list[str]:
    """Scan every ``.py`` under ``root`` (tests skipped). Labels are dotted module names."""
    skip = set(skip_modules)
    parts_skip = set(skip_parts)
    out: list[str] = []
    for path in sorted(root.rglob("*.py")):
        rel = path.relative_to(root)
        if parts_skip & set(rel.parts) or rel.name.startswith("test_") or rel.name == "conftest.py":
            continue
        label = ".".join((package_label, *rel.with_suffix("").parts)).removesuffix(".__init__")
        if label in skip:
            continue
        out += scan_source(path.read_text(encoding="utf-8"), label, allowed=allowed)
    return out


def stale_waivers(root: Path, package_label: str, allowed: dict[str, str]) -> list[str]:
    """Waivers that no longer name a function that writes the route (delete them)."""
    stale: list[str] = []
    for key in allowed:
        module, _, function = key.rpartition(".")
        if not module.startswith(package_label):
            continue
        rel = Path(*module.split(".")[1:])
        candidates = [root / rel.with_suffix(".py"), root / rel / "__init__.py"]
        path = next((p for p in candidates if p.exists()), None)
        if path is None or not scan_source(path.read_text(encoding="utf-8"), module, functions=[function]):
            stale.append(key)
    return stale


__all__ = ["BELT_FIELDS", "ROUTE_FIELDS", "scan_source", "scan_tree", "stale_waivers"]
