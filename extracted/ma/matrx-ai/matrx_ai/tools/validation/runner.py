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

from typing import Any

from matrx_ai.tools.declared import DeclaredTool, declared_families, declared_tools
from matrx_ai.tools.validation.engine import ValidationReport, validate

# Declaration modules that, when imported, populate the code registry via @tool.
# The matrx-ai generated module is always attempted; hosts add their own.
_DEFAULT_DECLARATION_MODULES = ("matrx_ai.tools._generated_declarations",)


def _load_declaration_module(module_path: str) -> object:
    """Load a registry-owned declaration module through THE declared-module seam.

    Hosts may supply declaration modules this package cannot enumerate in
    advance. ``matrx_utils.module_loading.load_declared_module`` keeps that
    extension seam open, mirrors normal import cache and failed-import cleanup,
    and refuses any provider SDK name — which is why the mandate/provider scan
    accepts it as a fact.
    """
    from matrx_utils.module_loading import load_declared_module

    return load_declared_module(module_path)


def import_declaration_modules(extra: tuple[str, ...] = ()) -> list[str]:
    """Import every declaration module so the @tool registry fills. Returns the
    list of failures (name + reason), for reporting.

    Two failure grains are reported, and BOTH must reach the boot drift gate:

    * the whole declaration module failed to import (``<module>: <exc>``);
    * the module imported but one of its per-tool ``_reg`` calls could not
      bind its implementation — a missing ``_MODULE_LOADERS`` entry or a
      broken implementation import. The generated module isolates those into
      its own ``IMPORT_FAILURES`` list so one bad tool never blocks the rest;
      harvesting that list here is what makes the isolation LOUD instead of
      silent. (Live incident 2026-09-12: five tools, ``memory`` among them,
      silently never registered and were dropped at request pre-flight while
      the gate reported a clean boot.)
    """
    failures: list[str] = []
    for mod in (*_DEFAULT_DECLARATION_MODULES, *extra):
        try:
            module = _load_declaration_module(mod)
        except Exception as exc:  # noqa: BLE001 - surfaced, not swallowed
            failures.append(f"{mod}: {exc!r}")
            continue
        failures.extend(declaration_tool_failures(module, module_name=mod))
    return failures


def declaration_tool_failures(module: object, *, module_name: str) -> list[str]:
    """Per-tool registration failures a declaration module isolated into its
    ``IMPORT_FAILURES`` list, rendered as ``<module>: <entry>`` lines."""
    entries = getattr(module, "IMPORT_FAILURES", None)
    if not isinstance(entries, list):
        return []
    return [f"{module_name}: {entry}" for entry in entries if isinstance(entry, str) and entry]


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
    # The ACTIVE subset, kept separately: `is_active` on a binding row is what routing
    # reads (`tool_resolve_for_request` joins `AND b.is_active = true`), so the engine
    # needs both — every binding, for ownership, and the live ones, for reachability.
    active_by_tool: dict[str, list[str]] = {}
    for b in bindings:
        tool_id = str(_row_value(b, "tool_id", "") or "")
        executor_name = _row_value(b, "executor_name")
        if tool_id and executor_name:
            executors_by_tool.setdefault(tool_id, []).append(str(executor_name))
            if bool(_row_value(b, "is_active", True)):
                active_by_tool.setdefault(tool_id, []).append(str(executor_name))

    rows: list[dict[str, Any]] = []
    for d in defs:
        tool_id = str(_row_value(d, "id", "") or "")
        rows.append(
            {
                "name": _row_value(d, "name"),
                "source_kind": _row_value(d, "source_kind"),
                "parameters": _row_value(d, "parameters"),
                "description": _row_value(d, "description"),
                # A soft-deleted definition (``deleted_at`` set) is retired, exactly like is_active=false: the
                # gate must not demand code for it (sandbox_maintenance, retired 2026-11-02, kept failing
                # every boot as missing_in_code).
                "is_active": bool(_row_value(d, "is_active", True)) and _row_value(d, "deleted_at") is None,
                "validation_exempt": _row_value(d, "validation_exempt", False),
                "executors": executors_by_tool.get(tool_id, []),
                "active_executors": active_by_tool.get(tool_id, []),
            }
        )
    return rows


def _tool_action_bodies(tool_name: str) -> list[Any]:
    """The work bodies of the Actions ``<tool_name>.*`` that a host declared as the tool's own
    (``declare_tool_action`` stores the body as ``tool_work`` on the Action's function)."""
    from matrx_graph.actions import default_action_registry

    out: list[Any] = []
    for spec in default_action_registry().all():
        if not spec.name.startswith(f"{tool_name}."):
            continue
        body = getattr(getattr(spec, "work", None), "tool_work", None)
        if body is not None:
            out.append(body)
    return out


def _closes_over(func: Any, model: Any) -> bool:
    """True when ``func`` closes over ``model`` itself (identity, not a name match)."""
    import inspect

    try:
        cells = inspect.getclosurevars(inspect.unwrap(func)).nonlocals.values()
    except (TypeError, ValueError):
        return False
    return any(value is model for value in cells)


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

    from matrx_ai.tools.action_door import action_for_tool, run_action_tool, tool_args_for
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
            # A decorated tool's source is the wrapped function, but its __globals__ are the
            # decorator's module, so unwrap first or its private implementation is never found.
            current = inspect.unwrap(pending.pop())
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
        # The Action tool door is one function behind every Action, so no model name can
        # appear in its source. It binds by construction: run_action validates the payload
        # against this same input_schema (or the host's narrower model of it, ``tool_args_for``: what
        # the model is offered when an Action's import-only fields are omitted). Only a door whose
        # Action no longer owns this model falls through to be reported.
        spec = action_for_tool(name)
        if dt.func is run_action_tool and spec is not None and tool_args_for(name, spec) is model:
            continue
        mname = getattr(model, "__name__", "") or ""
        src = _executable_source(dt.func)
        # A tool function that is only a door over its own Action (``tool_runner("x")``) runs
        # the Action's work body, which is where the args model is validated. Follow that real
        # body (``tool_work``, set by the host's ``declare_tool_action``) and, for a body that
        # takes the model as a parameter, accept the model object itself closed over by it.
        bodies = _tool_action_bodies(name)
        if bodies:
            src += "\n" + "\n".join(_executable_source(b) for b in bodies)
        door_binds_model = any(_closes_over(b, model) for b in bodies)
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
        bound = bound or door_binds_model
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
