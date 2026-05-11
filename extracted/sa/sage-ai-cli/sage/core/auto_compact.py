"""Item #8 — Auto-summarize long sessions."""

from __future__ import annotations

__all__ = ["should_compact", "build_compact_prompt"]


def should_compact(*, current_tokens: int, context_window: int,
                   threshold: float = 0.7) -> bool:
    if context_window <= 0:
        return False
    return current_tokens / context_window >= threshold


def build_compact_prompt(*, prior_messages: list[dict]) -> str:
    msgs_text = "\n".join(
        f"{m.get('role', '?')}: {m.get('content', '')[:500]}"
        for m in prior_messages[-30:]
    )
    return (
        "Summarize the conversation so far. Output the summary in this format:\n\n"
        "## Decisions made\n- key choices the user/agent committed to\n\n"
        "## Files changed\n- path: summary of what changed\n\n"
        "## Open questions\n- unresolved items\n\n"
        "## Tests / validation\n- what passed, what failed, what's pending\n\n"
        f"--- conversation ---\n{msgs_text}"
    )
