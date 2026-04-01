"""Slack notification helpers for durable stages."""

from __future__ import annotations

import contextvars
import logging
import os
from collections.abc import Callable

import httpx

from plato.chronos.api.slack import send_slack_message
from plato.chronos.models import SendSlackMessageRequest

logger = logging.getLogger(__name__)

# Callback type: (stage_name, output_type_name, elapsed_seconds, base_path) -> message or None
SlackFormatter = Callable[[str, str, float, str], str | None]


def _default_formatter(stage_name: str, output_type: str, elapsed: float, base_path: str) -> str:
    return f":white_check_mark: Stage `{stage_name}` completed in {elapsed:.1f}s (output: `{output_type}`)"


# Context var: when set, durable stages send slack notifications on completion.
# Value is (base_url, api_key, formatter).
_slack_notify_ctx: contextvars.ContextVar[tuple[str, str | None, SlackFormatter] | None] = contextvars.ContextVar(
    "_slack_notify_ctx", default=None
)


def enable_slack_notifications(
    api_key: str | None = None,
    base_url: str | None = None,
    formatter: SlackFormatter | None = None,
) -> contextvars.Token[tuple[str, str | None, SlackFormatter] | None]:
    """Enable Slack notifications for durable stages in the current context.

    Args:
        api_key: Chronos API key. Defaults to PLATO_API_KEY env var.
        base_url: Chronos base URL. Defaults to CHRONOS_URL env var or https://chronos.plato.so.
        formatter: Custom message formatter. Receives (stage_name, output_type, elapsed_secs, base_path).
    """
    if api_key is None:
        api_key = os.environ.get("PLATO_API_KEY")
    if base_url is None:
        base_url = os.environ.get("CHRONOS_URL", "https://chronos.plato.so")
    fmt = formatter or _default_formatter
    return _slack_notify_ctx.set((base_url, api_key, fmt))


def disable_slack_notifications(
    token: contextvars.Token[tuple[str, str | None, SlackFormatter] | None],
) -> None:
    """Disable Slack notifications by resetting the context var."""
    _slack_notify_ctx.reset(token)


async def notify_stage_complete(
    stage_name: str,
    output_type: str,
    elapsed: float,
    base_path: str,
) -> None:
    """Send a Slack notification for a completed durable stage. No-op if not enabled."""
    ctx = _slack_notify_ctx.get()
    if ctx is None:
        return

    url, api_key, formatter = ctx
    try:
        message = formatter(stage_name, output_type, elapsed, base_path)
        if message is None:
            return
        async with httpx.AsyncClient(
            base_url=url,
            timeout=5.0,
            headers={"X-API-Key": api_key} if api_key else {},
        ) as client:
            await send_slack_message.asyncio(
                client,
                body=SendSlackMessageRequest(message=message),
            )
    except Exception:
        logger.error("Failed to send Slack notification for stage %s", stage_name, exc_info=True)
