"""Per-STREAM reasoning-wrapper state — the one place providers keep it.

🚨 A provider client object is memoized PROCESS-WIDE
(``unified_client._provider_client_cache``: "the shared cache keeps each
provider's pool alive for the process lifetime"), so ONE ``AnthropicChat`` /
``OpenAIChat`` instance parses EVERY concurrent stream in the process. Anything
a stream parser keeps on ``self`` is therefore shared by unrelated users' turns.

That is not theoretical. The inline ``<reasoning>`` wrapper used to live on
``self._reasoning_open``, and with two turns thinking at once:

  * the second turn's wrapper never OPENED (the flag was already True), so its
    chain-of-thought streamed to the user as visible prose and its
    ``</reasoning>`` printed as literal message content, and
  * the first turn's wrapper never CLOSED (the flag was already False), so the
    client's thinking region stayed open and the entire visible ANSWER rendered
    inside the collapsed "Thought process" block — the assistant message read
    as empty. Observed live in three separate turns, 2026-09-12
    (matrx-frontend ``docs/handoffs/canonical-stream-and-surface-writeback.md``
    § "Cross-cutting defect").

So the state is keyed by the STREAM's emitter — one emitter per user turn,
alive exactly as long as the stream — and never by the parser instance. New
provider parsers that need per-stream state use this module; they never add an
attribute to ``self``.
"""

from __future__ import annotations

from collections.abc import MutableMapping
from typing import Any
from weakref import WeakKeyDictionary

_STATE_ATTR = "_matrx_reasoning_stream_state"


class ReasoningStreamState:
    """One stream's reasoning bookkeeping.

    ``open`` / ``signaled`` serve providers with a single thinking block in
    flight (Anthropic's sequential content blocks); ``started_ids`` /
    ``signaled_ids`` serve providers that id their reasoning items (OpenAI's
    Responses API). Both live here so a provider never invents a third home.
    """

    __slots__ = ("open", "signaled", "started_ids", "signaled_ids")

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.open: bool = False
        self.signaled: bool = False
        self.started_ids: dict[str, bool] = {}
        self.signaled_ids: set[str] = set()


_states: MutableMapping[Any, ReasoningStreamState] = WeakKeyDictionary()


def reasoning_state_for(emitter: Any) -> ReasoningStreamState:
    """The state for THIS stream, created on first use.

    Keyed weakly on the emitter so it disappears with the stream. An emitter
    that cannot be weak-referenced (``__slots__`` without ``__weakref__``)
    carries its state as an attribute instead — still per-stream, never shared.
    """
    try:
        state = _states.get(emitter)
        if state is None:
            state = ReasoningStreamState()
            _states[emitter] = state
        return state
    except TypeError:
        state = getattr(emitter, _STATE_ATTR, None)
        if state is None:
            state = ReasoningStreamState()
            setattr(emitter, _STATE_ATTR, state)
        return state


def reset_reasoning_state(emitter: Any) -> ReasoningStreamState:
    """Clear THIS stream's wrapper state at the top of a provider call.

    Scoped to one emitter: a turn starting while another turn is mid-think can
    never strand that turn's open wrapper.
    """
    state = reasoning_state_for(emitter)
    state.reset()
    return state
