"""A turn that did real work and wrote no closing line (live walk 2026-11-17: after a steer mid-build the
Conductor's turn ended with its graph saved and no text, and the screen said "This run finished without
writing an answer").

The runtime cannot make a model write words, but it can refuse to let finished, saved work read as nothing.
A host registers a provider; when the final model turn of a run is blank the executor asks it, and a
non-empty answer is written as the turn's closing text (stored and streamed, so a reload shows the same),
marked as a system summary. Providers read host state only (what this turn committed); they never call a
model. Nothing registered, or a provider that raises or returns nothing, changes nothing.
"""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable
from typing import Any

#: Beginning of every closing line a provider writes, so no reader mistakes it for the model's own words.
SYSTEM_SUMMARY_PREFIX = "System summary: "

TurnClosingProvider = Callable[[], str | None | Awaitable[str | None]]

_PROVIDERS: list[TurnClosingProvider] = []


def register_turn_closing(provider: TurnClosingProvider) -> None:
    """Register once (idempotent): a callable returning the closing sentence for the running turn, or None."""
    if provider not in _PROVIDERS:
        _PROVIDERS.append(provider)


async def closing_summary_for_turn() -> str | None:
    """The first provider's non-empty summary, prefixed as a system summary; never raises."""
    for provider in list(_PROVIDERS):
        try:
            out: Any = provider()
            if inspect.isawaitable(out):
                out = await out
        except Exception:  # noqa: BLE001 — a closing aid never breaks the run it closes
            continue
        if isinstance(out, str) and out.strip():
            text = out.strip()
            return text if text.startswith(SYSTEM_SUMMARY_PREFIX) else f"{SYSTEM_SUMMARY_PREFIX}{text}"
    return None
