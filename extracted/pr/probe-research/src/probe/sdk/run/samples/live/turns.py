"""WatchedTurns: a watched sample's turns as `live_turns` items, only while watched: scrubbed, cut to 64 KiB each
(keeping the end) and 1 MiB a call (keeping the newest), one seq per turn (rl-next B.4, D45)."""

from __future__ import annotations

import json
import threading
import time
from collections.abc import Callable, Iterable, Mapping
from datetime import datetime, timezone
from typing import Any

from .....generated.samples import MAX_LIVE_TURN_BYTES
from ..wire import cut_tail, replace_nul_text

#: One call's turns at most, in bytes of content: a watch's first snapshot keeps its newest turns.
MAX_SNAPSHOT_BYTES = 1024 * 1024
#: A turn's text is cut to this before the scrubber runs (its cost is about 0.5 s per MiB), then to 64 KiB.
_PRE_SCRUB_BYTES = 2 * MAX_LIVE_TURN_BYTES
MAX_ROLE_CHARS = 64
MAX_TOOL_NAME_CHARS = 256
#: Attempts whose seq counters are kept at once (the oldest is forgotten past it).
ATTEMPTS_REMEMBERED = 10_000


def to_text(content: Any) -> str:
    """A message's content as text: a string as it is, anything else (OpenAI content parts) as JSON."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    return json.dumps(content, default=str, ensure_ascii=False)


class WatchedTurns:
    """Which samples are watched until when, and each one's next turn seq. ``clock``: monotonic seconds."""

    def __init__(self, scrub: Callable[[str], str], clock: Callable[[], float] = time.monotonic) -> None:
        self._scrub = scrub
        self._clock = clock
        self._until: dict[str, float] = {}
        self._next_seq: dict[str, int] = {}
        self._lock = threading.Lock()

    def start_watch(self, key: str, seconds: float) -> None:
        """Send the sample's turns for ``seconds`` from now (a renewal moves the end, never back)."""
        with self._lock:
            self._until[key] = max(self._until.get(key, 0.0), self._clock() + seconds)

    def is_watched(self, key: str) -> bool:
        with self._lock:
            return self._clock() < self._until.get(key, 0.0)

    def forget(self, key: str) -> None:
        """The sample ended: no more turns."""
        with self._lock:
            self._until.pop(key, None)
            self._next_seq.pop(key, None)

    def make_items(self, key: str, turns: Iterable[Mapping[str, Any]]) -> list[dict]:
        """``turns`` (each `role`, `content`, and optionally `tool_name`, `tokens`, `at`, `weight_version`) as
        `LiveTurnIn` items with their seqs; [] when nobody watches the sample."""
        if not self.is_watched(key):
            return []
        items = [self._make_item(key, turn) for turn in turns]
        kept: list[dict] = []
        total = 0
        for item in reversed(items):
            total += len(item["content"].encode("utf-8"))
            if kept and total > MAX_SNAPSHOT_BYTES:
                break
            kept.append(item)
        kept.reverse()
        with self._lock:
            first = self._next_seq.get(key, 0)
            self._next_seq.pop(key, None)
            self._next_seq[key] = first + len(kept)
            while len(self._next_seq) > ATTEMPTS_REMEMBERED:
                self._next_seq.pop(next(iter(self._next_seq)))
        for offset, item in enumerate(kept):
            item["seq"] = first + offset
        return kept

    def _make_item(self, key: str, turn: Mapping[str, Any]) -> dict:
        text = cut_tail(replace_nul_text(to_text(turn.get("content"))), _PRE_SCRUB_BYTES)[0]
        item: dict[str, Any] = {
            "attempt_key": key,
            "at": _to_iso(turn.get("at")),
            "role": str(turn.get("role") or "assistant")[:MAX_ROLE_CHARS],
            "content": cut_tail(self._scrub(text), MAX_LIVE_TURN_BYTES)[0],
        }
        if turn.get("tool_name"):
            item["tool_name"] = str(turn["tool_name"])[:MAX_TOOL_NAME_CHARS]
        for name in ("tokens", "weight_version"):
            value = turn.get(name)
            if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
                item[name] = value
        return item


def _to_iso(value: Any) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, str) and value:
        return value
    return datetime.now(timezone.utc).isoformat()
