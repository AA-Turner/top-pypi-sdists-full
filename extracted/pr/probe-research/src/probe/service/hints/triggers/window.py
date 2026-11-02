"""the time-driven window look: when one is due and the agent text it sends."""

from __future__ import annotations
from probe.service.hints.state import WINDOW_MAX_SEGMENTS
#: A window look comes due this long after the last window look or researcher
#: prompt (the lines' own stamps), at the agent's next step (a message or a
#: tool call), if it wrote a message since: the mailbox hands a long turn one
#: hint per 10 minutes (`mailbox.UNASKED_WINDOW_S`), so looking more often
#: only replaces a waiting one.
WINDOW_GAP_S = 600.0
#: One message, at most, as sent (the engine embeds 2,000 characters).
WINDOW_SEGMENT_CHARS = 2000
#: The most text a request carries (the contract's client limit).
MAX_TEXT_CHARS = 8000
#: Text kept past MAX_TEXT_CHARS for the secret scan, so a credential the cut
#: would split is found whole first (a PEM private key runs ~1.7 kB).
SCAN_MARGIN_CHARS = 4096


def window_due(stamp: float, since: float | None, messages) -> bool:
    """A window look is due at an agent step stamped `stamp`: WINDOW_GAP_S on the
    window clock (`since`: the last window look, the researcher's prompt or the
    turn's first step) and at least one agent message since (`messages`)."""
    return since is not None and bool(messages) and stamp - since >= WINDOW_GAP_S


def window_segments(messages) -> list[str]:
    """A window's `segments`: the agent's messages (kept oldest first), newest
    first, at most WINDOW_MAX_SEGMENTS, each stripped and kept to
    WINDOW_SEGMENT_CHARS plus the scan margin (`scrubbed` cuts it when sent)."""
    out: list[str] = []
    for message in reversed(list(messages)):
        message = (message or "").strip()
        if message:
            out.append(message[:WINDOW_SEGMENT_CHARS + SCAN_MARGIN_CHARS])
            if len(out) >= WINDOW_MAX_SEGMENTS:
                break
    return out


def window_text(segments) -> str:
    """A window's `text`: its segments (scanned already) joined, newest first,
    at most MAX_TEXT_CHARS (the server reads names from it)."""
    return "\n\n".join(segments)[:MAX_TEXT_CHARS]


def shows_mid_turn(adapter) -> bool:
    """Whether the harness hands a `[Probe]` message over after a tool call,
    mid-turn (`Capabilities.inject_tool`). A window hint needs it: on one that
    shows messages only at the next prompt (Kimi Code), the turn's end would
    withdraw every window hint before it is seen."""
    return bool(getattr(getattr(adapter, "capabilities", None), "inject_tool", False))
