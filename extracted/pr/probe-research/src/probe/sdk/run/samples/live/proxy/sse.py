"""Server-sent events in a whole response body, as the proxy's observer reads them (the stream itself is passed on
untouched). A last frame with no blank line after it still counts: a cut stream keeps what came."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SseFrame:
    event: str | None = None
    data: str | None = None


def read_frames(text: str) -> list[SseFrame]:
    """The frames of a `text/event-stream` body; comments and unknown fields are skipped."""
    frames: list[SseFrame] = []
    event: str | None = None
    data: list[str] = []
    for line in text.splitlines():
        if not line:
            if event is not None or data:
                frames.append(SseFrame(event, "\n".join(data) if data else None))
            event, data = None, []
            continue
        if line.startswith(":"):
            continue
        name, _, value = line.partition(":")
        value = value[1:] if value.startswith(" ") else value
        if name == "data":
            data.append(value)
        elif name == "event":
            event = value
    if event is not None or data:
        frames.append(SseFrame(event, "\n".join(data) if data else None))
    return frames
