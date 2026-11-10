"""Server-sent events: the frames of a `text/event-stream` body, read line by line (twin: app/live)."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass


@dataclass(frozen=True)
class SseFrame:
    """One frame (fields up to a blank line). A frame with an `id` and no `data` moves the cursor and fires
    nothing: the live stream's open and keepalive frames."""

    id: str | None = None
    event: str | None = None
    data: str | None = None
    retry_ms: int | None = None

    def get_position(self) -> int | None:
        """The `id` as a seq, or None when there is none (or it is not a whole number)."""
        return int(self.id) if self.id is not None and self.id.isdigit() else None


def read_frames(lines: Iterable[str]) -> Iterator[SseFrame]:
    """The frames in `lines` (as `httpx.Response.iter_lines()` gives them); comments and unknown fields are
    skipped, as the SSE spec says."""
    fields: dict[str, str] = {}
    data: list[str] = []
    retry_ms: int | None = None
    for line in lines:
        if not line:
            if fields or data or retry_ms is not None:
                yield SseFrame(id=fields.get("id"), event=fields.get("event"),
                               data="\n".join(data) if data else None, retry_ms=retry_ms)
            fields, data, retry_ms = {}, [], None
            continue
        if line.startswith(":"):
            continue
        name, _, value = line.partition(":")
        value = value[1:] if value.startswith(" ") else value
        if name == "data":
            data.append(value)
        elif name == "event":
            fields["event"] = value
        elif name == "id" and "\0" not in value:
            fields["id"] = value
        elif name == "retry" and value.isdigit():
            retry_ms = int(value)
