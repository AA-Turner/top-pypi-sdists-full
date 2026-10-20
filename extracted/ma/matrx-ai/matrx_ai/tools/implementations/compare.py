"""``compare`` tool — find, quote, and (only on the person's click) compare same-type things.

The agent's call NEVER starts a paid run. It looks the typed things up, quotes the points and returns
the found list; the chat card shows a Confirm button, and the person's click starts a durable run
(over HTTP, not through this tool). A run takes 30 seconds to 3 minutes, so nothing here waits for it.
With ``run_id`` the tool reads the outcome of a run already started: a short text, free, never a start.

What the model knows: the found list, the quote, and — only if it asks again with ``run_id`` — the
ranking. It is told the person watches the card fill in. The host (aidream
``services/comparison_chat``) supplies the doors through matrx-scraper's ext registry; matrx-ai never
imports aidream.
"""

from __future__ import annotations

import time
from typing import Any

from matrx_ai.tools.arg_models.web_args import CompareArgs
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

#: ext-registry keys the host fills (``async (items, kind, city, call_id) -> dict`` / ``async (run_id) -> dict``).
EXT_PLAN = "comparison_chat_plan"
EXT_STATUS = "comparison_chat_status"


def _fail(message: str, ctx: ToolContext, started_at: float) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type="execution", message=message, is_retryable=False),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="compare",
        call_id=ctx.call_id,
    )


async def compare(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = CompareArgs.model_validate(args)
    from matrx_scraper._ext import get_ext, has_ext

    wanted = EXT_STATUS if parsed.run_id else EXT_PLAN
    if not has_ext(wanted) or get_ext(wanted) is None:
        return _fail("Comparing is not set up on this server, so nothing was looked up or billed.", ctx, started_at)
    try:
        if parsed.run_id:
            output = await get_ext(EXT_STATUS)(parsed.run_id)
        else:
            items = [i if isinstance(i, str) else i.model_dump(exclude_none=True) for i in parsed.items or []]
            if len(items) < 2 and not (parsed.concept and parsed.concept.strip() and not items):
                return _fail("Give at least two things to compare (names, websites or links), or a concept to search.",
                             ctx, started_at)
            output = await get_ext(EXT_PLAN)(items, parsed.kind, parsed.city, ctx.call_id, parsed.concept)
    except Exception as exc:  # noqa: BLE001 - a host refusal (points, no organization) is a sentence
        words = getattr(exc, "user_message", None)
        if not words:
            raise
        return _fail(words, ctx, started_at)
    return ToolResult(success=True, output=output, started_at=started_at, completed_at=time.time(),
                      tool_name="compare", call_id=ctx.call_id)
