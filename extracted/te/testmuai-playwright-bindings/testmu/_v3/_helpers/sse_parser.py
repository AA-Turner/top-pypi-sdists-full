from __future__ import annotations

# WHATWG HTML "server-sent events" wire-format parser (the `EventSource`
# byte-stream interpretation, https://html.spec.whatwg.org/#event-stream-interpretation).
# Used for fetch/XHR event-streams captured as raw bytes via CDP, where the
# browser does NOT pre-parse the frames (native EventSource is pre-parsed by the
# browser and uses Network.eventSourceMessageReceived instead — never this).
#
# feed(chunk: str) accepts an already-UTF-8-decoded text chunk (the caller owns
# one incremental decoder per connection so multibyte sequences split across
# network chunks decode cleanly) and returns the list of messages completed by
# that chunk. Partial lines and a lone trailing CR are buffered for the next feed.

_MAX_SSE_DATA = 65536


class SSEWireParser:
    def __init__(self) -> None:
        self._buffer = ""
        self._started = False
        # Per-dispatch buffers (reset after each message):
        self._data = ""
        self._event = ""
        # Persistent across messages (WHATWG: inherited until changed):
        self._last_event_id: str | None = None
        self._retry_ms: int | None = None

    def feed(self, chunk: str) -> list[dict]:
        if not self._started and chunk:
            # Only consume BOM-eligibility once a NON-EMPTY chunk is seen — the
            # incremental decoder can return "" for a split-multibyte first chunk
            # (incl. a BOM split across CDP events), and stripping must still apply
            # when the BOM materializes on a later feed.
            self._started = True
            if chunk.startswith("﻿"):
                chunk = chunk[1:]
        self._buffer += chunk

        events: list[dict] = []
        while True:
            line, rest = self._next_line(self._buffer)
            if line is None:
                break  # no complete line yet — keep buffering
            self._buffer = rest
            if line == "":
                ev = self._dispatch()
                if ev is not None:
                    events.append(ev)
            else:
                self._process_line(line)
        return events

    def _next_line(self, buf: str) -> tuple[str | None, str]:
        """Return (line, rest) for the first complete line, or (None, buf) if
        no terminator is present yet. Lines end on \\n, \\r\\n, or \\r. A lone
        trailing \\r is treated as incomplete (it may become \\r\\n next feed)."""
        n = len(buf)
        for i in range(n):
            c = buf[i]
            if c == "\n":
                return buf[:i], buf[i + 1:]
            if c == "\r":
                if i + 1 < n:
                    if buf[i + 1] == "\n":
                        return buf[:i], buf[i + 2:]
                    return buf[:i], buf[i + 1:]
                # lone trailing CR — ambiguous, wait for more input
                return None, buf
        return None, buf

    def _process_line(self, line: str) -> None:
        if line.startswith(":"):
            return  # comment line
        if ":" in line:
            field, _, value = line.partition(":")
            if value.startswith(" "):
                value = value[1:]  # strip exactly one leading space
        else:
            field = line
            value = ""

        if field == "data":
            self._data += value + "\n"
        elif field == "event":
            self._event = value
        elif field == "id":
            # WHATWG: ignore an id containing U+0000 NULL; otherwise set it.
            # We model "no id" as None, so an empty id resets to None.
            if "\x00" not in value:
                self._last_event_id = value or None
        elif field == "retry":
            # Only all-ASCII-digit values are valid; anything else is ignored.
            if value.isascii() and value.isdigit():
                self._retry_ms = int(value)

    def _dispatch(self) -> dict | None:
        data = self._data
        event = self._event
        # Reset per-dispatch buffers; keep last_event_id and retry_ms.
        self._data = ""
        self._event = ""

        if data == "":
            return None  # blank line with no data — emit nothing
        if data.endswith("\n"):
            data = data[:-1]  # strip the single trailing newline

        truncated = len(data) > _MAX_SSE_DATA
        return {
            "event": event or None,
            "data": data[:_MAX_SSE_DATA],
            "id": self._last_event_id,
            "retry": self._retry_ms,
            "truncated": truncated,
        }
