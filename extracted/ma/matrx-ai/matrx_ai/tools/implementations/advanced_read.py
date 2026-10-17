"""``advanced_read`` tool — read pages our own reader could not open, through the paid advanced readers.

The door lives in the host (aidream ``services/data_fetch/advanced_read.py``), reached through
matrx-scraper's ``advanced_reader`` hook (matrx-ai never imports aidream). Every page is metered in
the person's points by the host's observers and refused by its usage gate; the answer says which
reader opened each page, in how many seconds and for how many points. The tool is fast-only: the door is always called with
``allow="fast"`` (slow structured data is a person's click on the page button, never the agent's choice).

Any URL is accepted, not only pages that failed earlier in this conversation: the agent learns of
this tool from the failed-pages hint, a person may paste a page they already know is walled, and the
points meter + usage gate are the real control (refusing a URL would only waste a turn).
"""

from __future__ import annotations

import time
from typing import Any

from matrx_ai.tools.arg_models.web_args import AdvancedReadArgs
from matrx_ai.tools.implementations._web_read_caps import (
    RESULT_BUDGET_CHARS,
    enforce_result_budget,
    per_url_budget,
    window_page_content,
)
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult
from matrx_ai.tools.streaming import ToolStreamManager


def _fail(message: str, ctx: ToolContext, started_at: float, *, retryable: bool = False,
          action: str | None = None) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type="execution", message=message, is_retryable=retryable, suggested_action=action),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="advanced_read",
        call_id=ctx.call_id,
    )


async def advanced_read(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = AdvancedReadArgs.model_validate(args)
    from matrx_scraper._ext import get_ext, has_ext
    from matrx_scraper.coverage import EXT_READER

    if not has_ext(EXT_READER) or get_ext(EXT_READER) is None:
        return _fail("The advanced reader is not set up on this server, so nothing was read or billed.", ctx,
                     started_at, action="Use another source for these pages.")
    stream = ToolStreamManager(ctx.emitter, ctx.call_id, "advanced_read")
    await stream.progress(f"Opening {len(parsed.urls)} page{'s' if len(parsed.urls) != 1 else ''} with the advanced reader")
    try:
        items: list[dict[str, Any]] = await get_ext(EXT_READER)(parsed.urls, "fast")
    except Exception as exc:  # noqa: BLE001 - a host refusal (points, no organization) is a sentence
        words = getattr(exc, "user_message", None)
        if not words:
            raise
        code = getattr(exc, "code", "")
        return _fail(words, ctx, started_at,
                     action=("Do not retry. Tell the user their points are used up." if code == "usage_limit"
                             else None))
    budget = per_url_budget(len(items))
    pages: list[dict[str, Any]] = []
    for item in items:
        page = window_page_content(item.get("text") or "", url=item.get("url") or "", offset=0, chars=budget,
                                   per_url_budget=budget, success=bool(item.get("ok")),
                                   error=None if item.get("ok") else (item.get("message") or "Not read."))
        page.update({k: item.get(k) for k in ("reader", "seconds", "points", "message", "title", "record_count")
                     if item.get(k) is not None})
        pages.append(page)
    output = enforce_result_budget(
        {
            "pages": pages,
            "count": len(pages),
            "succeeded": sum(1 for i in items if i.get("ok")),
            "failed": sum(1 for i in items if not i.get("ok")),
            "points_total": sum(int(i.get("points") or 0) for i in items),
        },
        budget=RESULT_BUDGET_CHARS,
    )
    return ToolResult(success=True, output=output, started_at=started_at, completed_at=time.time(),
                      tool_name="advanced_read", call_id=ctx.call_id, output_self_capped=True)
