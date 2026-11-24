"""The person's answer to one asked question, in THEIR words — the ONE extraction every ask consumer uses.

The answer shape is the user-tool wire contract (``USER_TOOL_WIRE_CONTRACT.md``): ``answer`` / ``selected`` /
``confirmed`` / ``action`` / ``freeform`` / ``note`` / ``cancelled``. When the person takes the card's own escape
("Other", then types), the UI puts its OWN label ``"Other"`` into ``selected`` (or ``action``) beside the typed
``freeform``. That label is the card's, never the person's: stored as words it read "Other — About $45k a month"
(review 11, I5). Here it is dropped whenever the person typed something, so every reader (the Understanding card
writer, the agent's answer summary, the chat title) gets exactly what they wrote.
"""

from __future__ import annotations

from typing import Any

#: The label the ask UI writes for its free-text escape (``selected`` / ``action``) — the card's word, not the person's.
OTHER_ESCAPE = "Other"


def _typed(answer: dict[str, Any]) -> str | None:
    value = answer.get("freeform")
    return value.strip() if isinstance(value, str) and value.strip() else None


def picked_words(answer: dict[str, Any]) -> list[str]:
    """What the person picked, without the UI's escape label when they typed instead."""
    selected = answer.get("selected")
    if not isinstance(selected, list):
        return []
    picked = [str(s).strip() for s in selected if str(s).strip()]
    if _typed(answer) is not None:
        picked = [s for s in picked if s != OTHER_ESCAPE]
    return picked


def answer_words(answer: Any) -> str | None:
    """The person's answer to one question, in words; None = skipped or empty.

    Picks (comma-joined), else a typed answer, else yes/no, else a pressed button (never the escape label); then
    their typed ``freeform`` and ``note`` when they add something. Parts join with " — "."""
    if not isinstance(answer, dict) or answer.get("cancelled"):
        return None
    parts: list[str] = []
    picked = picked_words(answer)
    if picked:
        parts.append(", ".join(picked))
    elif isinstance(answer.get("answer"), str) and answer["answer"].strip():
        parts.append(answer["answer"].strip())
    elif isinstance(answer.get("confirmed"), bool):
        parts.append("Yes" if answer["confirmed"] else "No")
    elif isinstance(answer.get("action"), str) and answer["action"].strip() and not (
        answer["action"].strip() == OTHER_ESCAPE and _typed(answer) is not None
    ):
        parts.append(answer["action"].strip())
    for extra in ("freeform", "note"):
        value = answer.get(extra)
        if isinstance(value, str) and value.strip() and value.strip() not in parts:
            parts.append(value.strip())
    text = " — ".join(parts).strip()
    return text or None


__all__ = ["OTHER_ESCAPE", "answer_words", "picked_words"]
