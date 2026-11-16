"""The messages Miles pops from each sample right after its trajectory dump (`ray/rollout/debug_data.py:99-101`), one
line before Probe's log hook runs (`rollout_executor.py:288,296`): held here by reference so the hook still reads them
(D2). Only the latest dump's batch is held, and the hook clears it."""

from __future__ import annotations

import threading
from collections.abc import Iterable, Mapping
from typing import Any

#: Where Miles keeps a sample's messages as sent, only with `--save-debug-trajectory-data`: multi_turn's trajectory
#: (`generate_hub/multi_turn.py:74,92`) and a session's last record (`session/samples/merge.py:99-103`).
MESSAGES_KEY = "messages"


class MessagesStash:
    """`id(sample)` -> (the sample, its messages list). The sample is held too, so a reused id never reads another
    sample's messages; one batch at most."""

    def __init__(self) -> None:
        self._held: dict[int, tuple[Any, list]] = {}
        self._lock = threading.Lock()

    def keep(self, samples: Iterable[Any]) -> None:
        """Replace what is held with these samples' messages (before Miles pops them)."""
        held = {}
        for sample in samples or ():
            metadata = getattr(sample, "metadata", None)
            messages = metadata.get(MESSAGES_KEY) if isinstance(metadata, Mapping) else None
            if isinstance(messages, list):
                held[id(sample)] = (sample, messages)
        with self._lock:
            self._held = held

    def get(self, sample: Any) -> list | None:
        with self._lock:
            found = self._held.get(id(sample))
        return found[1] if found is not None and found[0] is sample else None

    def clear(self) -> None:
        with self._lock:
            self._held = {}


MESSAGES = MessagesStash()
