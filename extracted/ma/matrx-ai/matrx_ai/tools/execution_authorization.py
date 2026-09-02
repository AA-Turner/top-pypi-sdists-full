"""Host-injected, execution-time authorization for consequential tool calls.

This seam never edits the model-visible tool set.  A host may require a
durable human confirmation for one concrete invocation; the executor then
uses the existing delegated-tool suspend/resume protocol instead of running
the tool.  A later identical invocation may be authorized by the host.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

from matrx_ai.tools.models import ToolContext, ToolDefinition


@dataclass(frozen=True)
class ToolAuthorizationDecision:
    requires_confirmation: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


ToolAuthorizationHook = Callable[
    [ToolDefinition, dict[str, Any], ToolContext],
    Awaitable[ToolAuthorizationDecision],
]


async def evaluate_tool_authorization(
    tool_def: ToolDefinition,
    arguments: dict[str, Any],
    ctx: ToolContext,
) -> ToolAuthorizationDecision:
    """Ask the configured host policy, defaulting to normal execution."""
    from matrx_ai._ext import get_ext, has_ext

    if not has_ext("tool_authorization_hook"):
        return ToolAuthorizationDecision()
    hook = get_ext("tool_authorization_hook")
    decision = await hook(tool_def, arguments, ctx)
    if not isinstance(decision, ToolAuthorizationDecision):
        raise TypeError("tool_authorization_hook must return ToolAuthorizationDecision")
    return decision
