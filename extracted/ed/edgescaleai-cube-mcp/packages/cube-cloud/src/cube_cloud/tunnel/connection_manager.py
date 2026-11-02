"""Track active tunnel connections per user/session."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class StreamInfo:
    app_name: str
    created_at: float = field(default_factory=time.time)


class ConnectionManager:
    """Track active tunnel streams across all WebSocket connections."""

    def __init__(self) -> None:
        self._streams: dict[int, StreamInfo] = {}

    def add_stream(self, stream_id: int, app_name: str) -> None:
        self._streams[stream_id] = StreamInfo(app_name=app_name)
        logger.info("Stream added: %d -> %s (total: %d)", stream_id, app_name, len(self._streams))

    def remove_stream(self, stream_id: int) -> None:
        info = self._streams.pop(stream_id, None)
        if info:
            logger.info("Stream removed: %d (%s, total: %d)", stream_id, info.app_name, len(self._streams))

    @property
    def active_count(self) -> int:
        return len(self._streams)

    def status(self) -> dict:
        """Return status info for health checks."""
        return {
            "active_streams": self.active_count,
            "streams": {
                str(sid): {"app": info.app_name, "uptime_s": int(time.time() - info.created_at)}
                for sid, info in self._streams.items()
            },
        }
