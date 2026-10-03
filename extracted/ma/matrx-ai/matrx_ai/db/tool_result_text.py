"""A tool call's result as the model received it, from its ``chat.tool_call`` row alone.

No database or model-registry imports: the turn rebuild (``_conversation_rebuild_impl``) and a
host's read-only viewers (aidream's context viewer) both import it.
"""

from __future__ import annotations

from typing import Any


def tool_result_text_as_received(tc: Any) -> str | None:
    """The stored output (``tool_output_text`` — the bytes sent live) followed by the
    notices the live turn appended (they ride ``execution_events``). The ONE provider-neutral
    record of a tool result: the turn rebuild replays it, and the host's context viewer serves
    it (a provider's wire may carry no result ids — Gemini's does not). None when the row holds
    no output."""
    content = getattr(tc, "output", None)
    notices = _model_notices(tc)
    if notices:
        content = f"{content}\n\n" + "\n".join(notices) if content else "\n".join(notices)
    return content


def _model_notices(tc: Any) -> list[str]:
    events = getattr(tc, "execution_events", None)
    if not isinstance(events, list) or not events:
        return []
    from matrx_ai.tools.executor import MODEL_NOTICE_STEP

    return [
        str(e.get("message"))
        for e in events
        if isinstance(e, dict)
        and e.get("event") == "tool_step"
        and isinstance(e.get("data"), dict)
        and e["data"].get("step") == MODEL_NOTICE_STEP
        and e.get("message")
    ]


__all__ = ["tool_result_text_as_received"]
