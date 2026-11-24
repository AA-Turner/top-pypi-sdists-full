"""THE SPEAKER'S FIRST WORDS — what an agent said before it first reached for a tool.

One rule, shared by every emitter that carries a person's turn (the headless
``CaptureEmitter`` behind SMS and voice, the live ``StreamEmitter`` behind the
web door): at the FIRST tool event of a run, the words the agent said before it
are complete (the model finished that text and moved to a tool), so the door can
act on them before the tool runs. ``""`` means it said nothing first; that is the
moment a door sends its fallback acknowledgement, never after the tool has used
up the acknowledgement window (Personal Staff, Arman 2026-10-22: "The Chief";
staff-flow live proof 2026-10-30).

The callback is a courtesy: one that raises is logged and the run continues.
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable

logger = logging.getLogger(__name__)

FirstWordsCallback = Callable[[str], Awaitable[None]]


class FirstWordsBeforeFirstTool:
    """Fires ``callback(words)`` once, at the first tool event."""

    __slots__ = ("_callback", "words")

    def __init__(self) -> None:
        self.words: str | None = None
        self._callback: FirstWordsCallback | None = None

    def on_words(self, callback: FirstWordsCallback | None) -> None:
        self._callback = callback

    async def at_tool_event(self, said: Callable[[], str]) -> None:
        """Call at the top of ``send_tool_event``, BEFORE the tool event is emitted."""
        if self.words is not None:
            return
        self.words = (said() or "").strip()
        callback = self._callback
        if callback is None:
            return
        try:
            await callback(self.words)
        except Exception:  # noqa: BLE001 — a courtesy never breaks the turn
            logger.exception("[first-words] the first-words callback failed; the turn continues")


__all__ = ["FirstWordsBeforeFirstTool", "FirstWordsCallback"]
