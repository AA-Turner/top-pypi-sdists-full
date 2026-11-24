from __future__ import annotations

import traceback
from typing import TYPE_CHECKING

from matrx_utils import vcprint
from pydantic import BaseModel

from matrx_ai.agents.named import NamedAgent
from matrx_ai.mandates import Offer, RunOptions, carried_principal, get_mandate_runner
from matrx_ai.tools.models import ToolContext
from matrx_ai.tools.tool_knobs import SUMMARIZE_MAX_INPUT_CHARS
from matrx_ai.utils.carried_failure import FailureText

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




def summarize_cut_marker(kept: int, total: int) -> str:
    """The mark on a cut summarizer input (the research pipeline's "[Page capped: …]" style)."""
    return (
        f"[Content capped for summarizing: {kept:,} of {total:,} characters kept — "
        "facts past this point were not read]"
    )


#: Every failure path below returns a string starting with this so callers
#: (web_read) can turn it into a real ToolResult failure instead of a "success".
SUMMARIZE_FAILURE_PREFIX = "[Summarization failed:"


async def summarize_content(
    content: str,
    instructions: str,
    ctx: ToolContext,
) -> tuple[str, list[TokenUsage]]:
    """Summarize content through the ``tools.summarize_content`` mandate.

    The mandate's agent owns the model. A model passed from here outranked
    it: every summary ran on gemini-3.5-flash while the agent named Gemini
    3.8 Flash (2026-10-23). Never add a model override here.

    The input is capped at this organization's ``agents.web_read / summarize_max_input_chars``
    knob; a cut is MARKED in the content the summarizer reads and said again on the summary, so
    no reader downstream takes a summary of the head for a summary of the whole.

    Returns ``(summary_text, usage_history)``.
    """
    from matrx_ai.tools.output_caps import cap_text
    from matrx_ai.tools.tool_knobs import tool_knob_int

    cap = await tool_knob_int(
        "summarize_max_input_chars", SUMMARIZE_MAX_INPUT_CHARS, getattr(ctx, "organization_id", None)
    )
    kept, info = cap_text(content, limit=cap)
    if info.truncated:
        kept += "\n\n" + summarize_cut_marker(info.shown_chars, info.total_chars)
    try:
        result = (
            await get_mandate_runner().run(
                SummarizeContentAgent.mandate_key,
                Offer.from_inputs(
                    SummarizeContentAgent,
                    inputs=SummarizeContentAgent.Inputs(
                        instructions=instructions,
                        content=kept,
                    ),
                    label="summarize_content",
                    source_feature="summarize_content",
                    # NESTED-AGENT STREAM LEAK: this runs INSIDE the web_read tool
                    # while the caller's agent is streaming to a user, so without a
                    # mute the summarizer's tokens ride the caller's user-facing
                    # NDJSON stream. suppress_stream gives it its own SilentEmitter;
                    # the summary still returns on AgentRunResult.output.
                    suppress_stream=True,
                ),
                who=carried_principal(),
                opts=RunOptions(door="named_agent"),
            )
        ).raw
        if not result.success:
            return (
                FailureText(f"[Summarization failed: {result.error}]", getattr(result, "exception", None)),
                list(result.usage_history),
            )
        summary = result.output
        if info.truncated:
            summary = f"{summary}\n\n{summarize_cut_marker(info.shown_chars, info.total_chars)}"
        return summary, list(result.usage_history)

    except ImportError as exc:
        # Raw page text is never a summary: a summarizer that cannot load is a declared failure.
        vcprint(
            f"The summarizer could not be loaded ({exc}); the call fails rather than pass raw text off as a summary",
            "[summarize_content] ImportError",
            color="red",
        )
        return FailureText(f"{SUMMARIZE_FAILURE_PREFIX} the summarizer could not be loaded ({exc})]", exc), []
    except Exception as exc:
        vcprint(
            f"Summarization failed: {exc}\n{traceback.format_exc()}",
            "[summarize_content] Unhandled exception",
            color="red",
        )
        return FailureText(f"[Summarization failed: {exc}]", exc), []
