"""StoredChannel — outbound-only fallback that persists events to disk."""

import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import AsyncIterator

from .base import Channel, ChannelEvent, ChannelMessage, DeliveryResult


class StoredChannel(Channel):
    """Persists outbound events to ``.emdash/channels/pending.json``.

    Used as a fallback when no live channel is active, so messages are never
    lost.  The agent's ``_pre_run()`` hook reads and clears pending messages
    on the next interaction.
    """

    name = "stored"

    def __init__(self, emdash_dir: Path) -> None:
        self._file = emdash_dir / "channels" / "pending.json"
        self._lock = threading.Lock()

    # -- Lifecycle (no-ops for stored channel) --

    async def is_available(self) -> bool:
        return True

    # -- Inbound (not supported) --

    async def poll_messages(self) -> AsyncIterator[ChannelMessage]:
        return
        yield  # make this an async generator

    async def check_authorization(self, sender_id: str) -> bool:
        return True

    # -- Outbound --

    async def send_event(
        self, sender_id: str, event: ChannelEvent
    ) -> DeliveryResult:
        entry = {
            "sender_id": sender_id,
            "type": event.type,
            "content": event.content,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._append(entry)
        return DeliveryResult(success=True, channel="stored")

    # -- Read / clear interface --

    def get_and_clear(self) -> list[dict]:
        """Read and clear all pending messages.

        Called by the agent ``_pre_run()`` hook to inject stored
        notifications into short-term memory.
        """
        with self._lock:
            if not self._file.exists():
                return []
            try:
                data = json.loads(self._file.read_text())
            except (json.JSONDecodeError, OSError):
                data = []
            # Truncate the file
            self._file.write_text("[]")
            return data

    # -- Internal helpers --

    def _append(self, entry: dict) -> None:
        with self._lock:
            self._file.parent.mkdir(parents=True, exist_ok=True)
            try:
                data = json.loads(self._file.read_text()) if self._file.exists() else []
            except (json.JSONDecodeError, OSError):
                data = []
            data.append(entry)
            self._file.write_text(json.dumps(data, indent=2))
