"""VSCode IDE state tool.

Provides the model with on-demand access to the IDE snapshot that was sent
with the originating request.  The snapshot is stored in AppContext.metadata
by the router and is available for the full lifetime of the request, across
all turns of a conversation.

The model calls this tool when it needs editor state it does not already have
in context — for example, on turn 2 when the agent's variable substitution
has already run and the original vsc_* values are no longer visible.
"""

from __future__ import annotations

import traceback
from typing import Any

from matrx_ai.tools.kinds.ide import IdeStateFields
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

_VALID_FIELDS = frozenset(
    {
        "vsc_active_file_path",
        "vsc_active_file_content",
        "vsc_active_file_language",
        "vsc_active_file_all",
        "vsc_selected_text",
        "vsc_diagnostics",
        "vsc_workspace_name",
        "vsc_workspace_folders",
        "vsc_workspace_all",
        "vsc_git_branch",
        "vsc_git_status",
        "vsc_git_all",
        "vsc_editor",
        "vsc_all",
    }
)


async def vsc_get_state(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Return requested VSCode IDE state fields from the current request context."""
    from matrx_ai.tools._generated_declarations import VscGetStateArgs
    VscGetStateArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    try:
        from matrx_ai.context.app_context import get_app_context
        from matrx_ai._ext import get_ext
        IdeState = get_ext("IdeState")

        fields_requested: list[str] = args.get("fields", [])

        if not fields_requested:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message="fields is required and must be a non-empty list.",
                    suggested_action=(
                        f"Provide one or more field names from: {sorted(_VALID_FIELDS)}"
                    ),
                ),
            )

        unknown = [f for f in fields_requested if f not in _VALID_FIELDS]
        if unknown:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message=f"Unknown field(s): {unknown}",
                    suggested_action=(
                        f"Valid fields are: {sorted(_VALID_FIELDS)}"
                    ),
                ),
            )

        app_ctx = get_app_context()
        raw = app_ctx.metadata.get("ide_state")

        if raw is None:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="not_found",
                    message="No IDE state is available for this request.",
                    suggested_action=(
                        "The calling client must include ide_state in the request body."
                    ),
                ),
            )

        state = IdeState.model_validate(raw)
        variables = state.to_variables()

        result: dict[str, str | None] = {}
        for field in fields_requested:
            result[field] = variables.get(field)

        # KindModel result (KIND_TOOL_LEDGER): the 14-name field set is closed
        # (_VALID_FIELDS), so every key is declared; None = not requested or
        # not carried by the snapshot.
        return ToolResult(
            success=True, output=IdeStateFields(**result).model_dump(mode="json")
        )

    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution",
                message=f"Failed to retrieve IDE state: {e}",
                traceback=traceback.format_exc(),
                is_retryable=False,
            ),
        )
