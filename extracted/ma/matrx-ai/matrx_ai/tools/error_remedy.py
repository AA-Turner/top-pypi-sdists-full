"""What a tool failure MEANS, said to the agent that has to act on it.

A tool result is read by a model, and the model then tells a person what
happened. So an error envelope that carries only the database's wording is not
neutral — it is the sentence the person hears.

2026-09-12 23:24: the Masterwork Conductor tried to change how a desk's Writer
thinks. The write hit ``agent.definition``'s provenance CHECK — *"This write
declares actor_tier=code, but names no actor_system … x-matrx-actor-system on
the client channel, or the app.actor_system GUC on a server channel"* — which is
a missing HEADER on OUR write path. The envelope handed the model that text plus
the executor's generic *"Check the error details and try with different
parameters"*, and the Conductor told the Expert:

    "I am blocked by system policy … edits to any agent's contract must come
    from an authorized human channel."

Nothing about her request was disallowed. So: a failure class we can NAME gets
one line of cause and one line of remedy attached here, in front of the raw
text, and the raw text is still carried verbatim after it. Matching runs over
:func:`matrx_utils.error_text.classification_text` — never ``str(exc)`` — because
the rendered text can carry the caller's own payload (a document, a transcript),
and a ladder that matches on a payload tells a person something false about
their own words.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from matrx_utils.error_text import classification_text


@dataclass(frozen=True)
class ErrorRemedy:
    """One line of cause, one line of remedy, for a failure class we know."""

    cause: str
    remedy: str

    def prefix(self, raw_message: str) -> str:
        """The envelope message: the diagnosis first, the raw text kept after it."""
        return f"{self.cause} {self.remedy}\n\nUnderlying error: {raw_message}"


#: A write that reached Postgres without naming the system that made it. The
#: CHECK is right (an AI write must say which agent/system it is); the write path
#: forgot to declare. Never a permission, policy or entitlement refusal.
UNDECLARED_ACTOR_SYSTEM = ErrorRemedy(
    cause=(
        "This failed on a PLATFORM DEFECT, not on policy or permission: the write "
        "reached the database without naming which system made it (the "
        "app.actor_system declaration is missing on this code path). Nothing about "
        "the request is disallowed, and no approval, human channel or extra "
        "authorization is required."
    ),
    remedy=(
        "Retry the identical call once. If it fails the same way, say plainly that a "
        "platform defect is blocking the change (the tool's write path must declare "
        "its actor system) and report it — never tell the person the edit is "
        "forbidden, needs a human channel, or needs approval."
    ),
)

_UNDECLARED_ACTOR_MARKERS: tuple[str, ...] = (
    "names no actor_system",
    "actor_system on a server channel",
    "x-matrx-actor-system",
)


def error_remedy_for(message: str | None) -> ErrorRemedy | None:
    """The remedy for a failure class we can name, or None.

    ``message`` is any rendered error text; only its bounded
    :func:`classification_text` head is ever matched.
    """
    if not message:
        return None
    text = classification_text(str(message)).lower()
    if any(marker.lower() in text for marker in _UNDECLARED_ACTOR_MARKERS):
        return UNDECLARED_ACTOR_SYSTEM
    return None


def annotate_tool_error(error: Any) -> Any:
    """Attach cause + remedy to a ``ToolError`` whose class we recognise.

    Mutates and returns the error so the caller can inline it. A class we do not
    recognise is left exactly as it was — this never invents a diagnosis.
    """
    remedy = error_remedy_for(getattr(error, "message", None))
    if remedy is None:
        return error
    error.message = remedy.prefix(error.message)
    error.suggested_action = remedy.remedy
    error.is_retryable = True
    return error


__all__ = [
    "UNDECLARED_ACTOR_SYSTEM",
    "ErrorRemedy",
    "annotate_tool_error",
    "error_remedy_for",
]
