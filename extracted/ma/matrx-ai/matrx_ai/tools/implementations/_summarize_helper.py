from __future__ import annotations

import traceback
from typing import TYPE_CHECKING

from matrx_utils import vcprint
from pydantic import BaseModel

from matrx_ai.agents.named import NamedAgent
from matrx_ai.mandates import run_mandated
from matrx_ai.tools.models import ToolContext

if TYPE_CHECKING:
    from matrx_ai.config import TokenUsage


class SummarizeContentAgent(NamedAgent):
    """Mandated: ``mandate.definition`` (key ``tools.summarize_content``) owns
    which agent runs. A hardcoded ``source`` next to ``mandate_key`` is refused
    by ``NamedAgent._check_definition`` — that exact refusal made every
    ``web`` ``summarize=true`` call return a "[Summarization failed: ...]"
    shell until 2026-09-08. Never add a source here."""

    name = "summarize_content"
    mandate_key = "tools.summarize_content"

    class Inputs(BaseModel):
        instructions: str
        content: str


#: Every failure path below returns a string starting with this so callers
#: (web_read) can turn it into a real ToolResult failure instead of a "success".
SUMMARIZE_FAILURE_PREFIX = "[Summarization failed:"


async def summarize_content(
    content: str,
    instructions: str,
    ctx: ToolContext,
    model_id: str = "gemini-3.5-flash",
) -> tuple[str, list[TokenUsage]]:
    """Summarize content using the unified AI system.

    Returns ``(summary_text, usage_history)``.
    """
    try:
        result = await run_mandated(
            SummarizeContentAgent,
            inputs=SummarizeContentAgent.Inputs(
                instructions=instructions,
                content=content[:100000],
            ),
            label="summarize_content",
            source_feature="summarize_content",
            config_overrides={"model": model_id},
        )
        if not result.success:
            return f"[Summarization failed: {result.error}]", list(result.usage_history)
        return result.output, list(result.usage_history)

    except ImportError:
        vcprint(
            "Agent modules not available; returning raw content truncated",
            "[summarize_content] ImportError",
            color="red",
        )
        return content[:2000], []
    except Exception as exc:
        vcprint(
            f"Summarization failed: {exc}\n{traceback.format_exc()}",
            "[summarize_content] Unhandled exception",
            color="red",
        )
        return f"[Summarization failed: {exc}]", []
