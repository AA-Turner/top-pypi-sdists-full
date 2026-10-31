"""The TOOL door of an Action — generated from the one declaration, never a second one.

An Action (``matrx_graph.actions.declare_action``) that names the ``tool`` door is
offered to agents as the tool ``tool_name_for(action.name)`` (dots → underscores).
ONE function backs every such tool, :func:`run_action_tool`: it finds the Action by
the tool name the executor is dispatching and calls ``run_action`` — the same router
the step, directive and mcp doors call, which sends it to the Action's engine — inside the AppContext the tool path
already carries (``get_app_context()``).

THE DB-FIRST DRIFT LAW HOLDS. A tool exists for agents only once its
``tool.definition`` row exists. Until a row lands, the door declares the tool with
``validate=False`` — the honest exemption: the arg model is registered for runtime
validation, and the drift gate does not report a row that is, correctly, missing.
The HOST names the Action tools whose row HAS landed (``open_tool_door(rowed=...)``);
those validate. matrx-ai never hard-codes a host's tool names.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.actions import (
    ActionFailed,
    default_action_registry,
    dump_result,
    run_action,
    tool_name_for,
)
from matrx_graph.actions.registry import ActionRegistry
from matrx_graph.actions.spec import ActionSpec

from matrx_ai.tools.declared import get_declared_tool, tool

#: Action tools whose ``tool.definition`` row exists, as the host said (``open_tool_door``).
_ROWED: set[str] = set()

_BY_TOOL_NAME: dict[str, ActionSpec] = {}


def action_for_tool(tool_name: str) -> ActionSpec | None:
    return _BY_TOOL_NAME.get(tool_name)


def tool_idempotency_key(name: str, payload: Any, ctx: Any) -> str | None:
    """The tool call's own id — a provider retry of the same call carries it again.
    With no call id there is NO key, so no dedupe: hashing the arguments would return week
    1's result to an identical call a week later (Arman, 2026-10-30)."""
    call_id = getattr(ctx, "call_id", "") or ""
    return f"tool:{call_id}" if call_id else None


async def run_action_tool(args: Any, ctx: Any) -> Any:
    """The ONE tool function behind every Action's tool door."""
    from matrx_connect.context.app_context import get_app_context
    from matrx_graph.actions import REPLAY_MESSAGE, last_run_replayed

    from matrx_ai.tools.models import ToolResult

    name = getattr(ctx, "tool_name", "") or ""
    spec = _BY_TOOL_NAME.get(name)
    if spec is None:
        raise LookupError(
            f"No Action backs tool {name!r}; the Action tools are {sorted(_BY_TOOL_NAME)}."
        )
    from pydantic import ValidationError

    from matrx_ai.tools.models import ToolError

    payload = args.model_dump() if hasattr(args, "model_dump") else (args or {})
    try:
        out = await run_action(
            spec, payload, app=get_app_context(), idempotency_key=tool_idempotency_key(name, payload, ctx),
            door="tool",
        )
    except ActionFailed as exc:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type=exc.error_type,
                message=exc.message,
                is_retryable=False,
                suggested_action=exc.suggested_action or None,
            ),
        )
    except (ValidationError, ValueError) as exc:
        # The model sent arguments the Action refuses: it reads why and can call again.
        return ToolResult(
            success=False,
            error=ToolError.from_exception(exc, error_type="validation", message=str(exc)),
        )
    output = dump_result(spec, out)
    if last_run_replayed():
        output = {**output, "replayed": True, "message": REPLAY_MESSAGE}
    return ToolResult(success=True, output=output)


def open_tool_door(
    registry: ActionRegistry | None = None, *, rowed: frozenset[str] | set[str] = frozenset()
) -> list[str]:
    """Declare every Action with the ``tool`` door as a tool. Idempotent — the host calls
    it again once lazily-imported Actions (workflow steps) are declared.

    ``rowed``: the tool names whose ``tool.definition`` row exists (host-supplied); those
    validate against it. Returns the tool names declared. A tool name already declared by another
    function is a hard error (``ToolDeclarationError``) — one name, one Action.
    """
    _ROWED.update(rowed)
    opened: list[str] = []
    for spec in (registry or default_action_registry()).all():
        if "tool" not in spec.doors or spec.work is None:
            continue
        name = tool_name_for(spec.name)
        _BY_TOOL_NAME[name] = spec
        existing = get_declared_tool(name)
        if existing is None or existing.func is not run_action_tool or existing.validate != (name in _ROWED):
            tool(
                name=name,
                source_kind="native",
                args=spec.input_schema,
                executor="aidream",
                validate=name in _ROWED,
            )(run_action_tool)
        opened.append(name)
    return opened


__all__ = ["action_for_tool", "open_tool_door", "run_action_tool"]
