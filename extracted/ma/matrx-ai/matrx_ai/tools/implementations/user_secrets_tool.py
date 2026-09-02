"""user_secret_set — agent-callable handler for the user-secrets vault.

Lets the agent save a secret on the user's behalf during a chat
("save my GitHub token: ghp_…"). Upserts into `users.user_secrets` via the
matrx-orm secrets battery (`matrx_orm.secrets_battery`) — the one canonical vault
implementation, bound by the host at startup (`configure_secrets`).

Package independence: matrx-orm is not a hard dep of matrx-ai — deferred
import, same pattern as `ctx_write`; the tool degrades cleanly in a
deployment without matrx-orm. Logged in cx_tool_trace as
`error_type=feature_unavailable` so it's distinguishable from a real
failure.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from matrx_ai.tools.arg_models.user_secrets_args import UserSecretSetArgs
from matrx_ai.tools.declared import tool
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

logger = logging.getLogger(__name__)


def _mask_for_log(value: str) -> str:
    """Don't dump a full secret to the cx_tool_trace logs. Mirror the
    same masking shape the UI uses."""
    if not value:
        return ""
    if len(value) <= 8:
        return "•••"
    return f"{value[:4]}…{value[-4:]}"


@tool(
    name="user_secret_set",
    source_kind="native",
    args=UserSecretSetArgs,
    executor="aidream",
)
async def user_secret_set(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Save or rotate a secret on the user's account. Idempotent upsert."""
    started_at = time.time()
    parsed = UserSecretSetArgs(**args)

    if not ctx.user_id:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="auth_required",
                message="user_secret_set requires an authenticated user — "
                "no user_id on the request context.",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="user_secret_set",
            call_id=ctx.call_id,
        )

    # Deferred import so matrx-ai stays importable without matrx-orm
    # (the host-injection pattern documented in CLAUDE.md →
    # "capability-within, injection-without").
    try:
        from matrx_orm.secrets_battery import create_user_secret
    except ImportError as exc:
        logger.warning(
            "[user_secret_set] matrx_orm.secrets_battery unavailable: %s — "
            "the host application must install matrx-orm for this tool to work.",
            exc,
        )
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="feature_unavailable",
                message="The user-secrets vault is only available when "
                "matrx-orm (with the secrets battery configured) is installed.",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="user_secret_set",
            call_id=ctx.call_id,
        )

    try:
        row = await create_user_secret(
            user_id=ctx.user_id,
            key=parsed.key,
            value=parsed.value,
            description=parsed.description,
            category=parsed.category or "custom",
            inject_into_sandbox=parsed.inject_into_sandbox,
            upsert=True,
        )
    except ValueError as exc:
        return ToolResult(
            success=False,
            error=ToolError(error_type="model_error", message=str(exc)),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="user_secret_set",
            call_id=ctx.call_id,
        )
    except Exception as exc:  # pragma: no cover — DB / pool failures
        logger.exception("[user_secret_set] upsert failed")
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,
                error_type="database",
                message=f"Failed to save secret: {exc}",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="user_secret_set",
            call_id=ctx.call_id,
        )

    # Package-hosted tool: the declared result kind is instantiated inline
    # (the `sql` precedent — no aidream stamp funnel is importable from here).
    from matrx_ai.tools.kinds.user_secrets import UserSecretReceipt

    return ToolResult(
        success=True,
        output=UserSecretReceipt(
            saved=True,
            key=row.key,
            value_hint=row.value_hint,
            category=row.category,
            inject_into_sandbox=row.inject_into_sandbox,
            note=(
                "Stored encrypted. Available as an env var in every new "
                "sandbox you create. Existing sandboxes are not retroactively "
                "updated — restart them to pick up the new value."
            ),
        ).model_dump(mode="json"),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="user_secret_set",
        call_id=ctx.call_id,
    )


__all__ = ["user_secret_set"]
