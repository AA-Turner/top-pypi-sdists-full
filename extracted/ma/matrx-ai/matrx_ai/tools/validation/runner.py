"""Live-DB orchestration for tool validation.

This layer does the I/O the pure engine refuses to do: import the modules that
register code tools, pull ``tool_def`` + ``tool_binding`` from the database
through the host-injected ORM managers, and hand both sides to
:func:`matrx_ai.tools.validation.validate`.

It is import-tolerant on purpose: the generated declaration modules may not
exist yet (first run, or matrx-ai consumed standalone), and the host may pass
extra declaration modules to import. Anything that fails to import is reported,
not fatal.
"""

from __future__ import annotations

import importlib
from typing import Any

from matrx_ai.tools.declared import DeclaredTool, declared_families, declared_tools
from matrx_ai.tools.validation.engine import ValidationReport, validate

# Declaration modules that, when imported, populate the code registry via @tool.
# The matrx-ai generated module is always attempted; hosts add their own.
_DEFAULT_DECLARATION_MODULES = ("matrx_ai.tools._generated_declarations",)


def import_declaration_modules(extra: tuple[str, ...] = ()) -> list[str]:
    """Import every declaration module so the @tool registry fills. Returns the
    list of modules that failed to import (name + reason), for reporting."""
    failures: list[str] = []
    for mod in (*_DEFAULT_DECLARATION_MODULES, *extra):
        try:
            importlib.import_module(mod)
        except Exception as exc:  # noqa: BLE001 - surfaced, not swallowed
            failures.append(f"{mod}: {exc!r}")
    return failures


def _row_value(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


async def fetch_db_rows() -> list[dict[str, Any]]:
    """Read ``tool_def`` joined to ``tool_binding`` executor names via the
    ORM managers.
    """
    from matrx_ai.tools.tool_binding_db import tool_binding_manager_instance
    from matrx_ai.tools.tool_def_db import tool_def_manager_instance

    defs = await tool_def_manager_instance.load_all_tools()
    bindings = await tool_binding_manager_instance.load_all()

    executors_by_tool: dict[str, list[str]] = {}
    for b in bindings:
        tool_id = str(_row_value(b, "tool_id", "") or "")
        executor_name = _row_value(b, "executor_name")
        if tool_id and executor_name:
            executors_by_tool.setdefault(tool_id, []).append(str(executor_name))

    rows: list[dict[str, Any]] = []
    for d in defs:
        tool_id = str(_row_value(d, "id", "") or "")
        rows.append(
            {
                "name": _row_value(d, "name"),
                "source_kind": _row_value(d, "source_kind"),
                "parameters": _row_value(d, "parameters"),
                "description": _row_value(d, "description"),
                "is_active": _row_value(d, "is_active", True),
                "validation_exempt": _row_value(d, "validation_exempt", False),
                "executors": executors_by_tool.get(tool_id, []),
            }
        )
    return rows


def find_unverified_tools(
    code: dict[str, DeclaredTool], owner_executors: set[str]
) -> list[dict[str, str]]:
    """Return owned tools whose function does NOT actually reference its registered
    args model — i.e. the model is a DB-shaped mirror the code ignores, so diffing it
    against the DB is circular and PROVES NOTHING. These are the tools the gate
    cannot honestly claim to verify.

    Reliable signal for the dispatcher-tool false-green: a tool that truly binds to
    its contract uses the model (its class name appears in the function source,
    e.g. ``FsReadArgs(**args)``); an ``args: dict`` + ``args.get(...)`` dispatcher
    that delegates to unregistered per-action models does not.

    ``owner_executors`` filters by the declared tool's ``executor`` — pass the
    set of executor names that THIS codebase owns (typically
    ``{"matrx-ai-core", "aidream"}``). A declaration whose executor is anywhere
    else (or unset) is treated as external to this repo and skipped.
    """
    import ast
    import inspect
    import textwrap

    from matrx_ai.tools.declared import NoArgs
    from matrx_ai.tools.validation.schema import discriminated_union_members

    def _executable_source(func: Any) -> str:
        # Result-kind wrappers delegate validation to a private implementation.
        # Follow only statically named, same-module calls; arbitrary globals and
        # dynamic dispatch remain untrusted.
        pending = [func]
        seen: set[int] = set()
        chunks: list[str] = []
        while pending:
            current = pending.pop()
            if id(current) in seen:
                continue
            seen.add(id(current))
            try:
                source = inspect.getsource(current)
            except (OSError, TypeError):
                continue
            chunks.append(source)
            try:
                tree = ast.parse(textwrap.dedent(source))
            except SyntaxError:
                continue
            namespace = getattr(current, "__globals__", {})
            current_module = getattr(current, "__module__", None)
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
                    continue
                target = namespace.get(node.func.id)
                if (
                    inspect.isfunction(target)
                    and getattr(target, "__module__", None) == current_module
                    and id(target) not in seen
                ):
                    pending.append(target)
        return "\n".join(chunks)

    out: list[dict[str, str]] = []
    for name, dt in sorted(code.items()):
        if dt.executor not in owner_executors:
            continue
        model = dt.args_model
        if model is NoArgs:
            continue  # no arguments → nothing to verify
        mname = getattr(model, "__name__", "") or ""
        src = _executable_source(dt.func)
        # A dispatcher binds its contract either by validating the registered
        # RootModel union (its class name appears in the body) OR by constructing
        # the per-action member models directly — both prove the code actually runs
        # the declared per-action contract.
        union = discriminated_union_members(model)
        if union is not None:
            members = list(union[1].values())
            bound = (bool(mname) and mname in src) or (
                bool(members) and all((getattr(m, "__name__", "") or "\0") in src for m in members)
            )
        else:
            bound = bool(mname) and mname in src
        if not bound:
            out.append(
                {
                    "tool_name": name,
                    "model": mname or "(unknown)",
                    "function_path": dt.function_path,
                }
            )
    return out


async def run_validation(
    *,
    owner_executors: set[str],
    extra_declaration_modules: tuple[str, ...] = (),
    db_rows: list[dict[str, Any]] | None = None,
) -> tuple[ValidationReport, list[str]]:
    """Full pass: import declarations, fetch DB, diff. Returns (report, import_failures).

    Beyond drift, this flags tools whose code does not actually bind to its registered
    contract (``report.unverified``) — a green result requires BOTH no drift AND no
    unverified tools (``report.fully_verified``).

    ``owner_executors`` defines the set of executor names that THIS repo owns.
    A DB row is "missing in code" only if it has an active binding to one of
    those executors but no @tool declaration exists locally. A code declaration
    is "missing in DB" only if its declared executor is in this set."""
    import_failures = import_declaration_modules(extra_declaration_modules)
    if db_rows is None:
        db_rows = await fetch_db_rows()
    code = declared_tools()
    report = validate(
        code,
        db_rows,
        owner_executors=owner_executors,
        families=declared_families(),
    )
    report.unverified = find_unverified_tools(code, owner_executors)
    return report, import_failures
