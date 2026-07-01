from __future__ import annotations

import json
from collections.abc import Iterable, Iterator
from dataclasses import dataclass


@dataclass(frozen=True)
class DurableRunEvent:
    event: str
    data: object
    raw_data: str
    id: str | None = None
    retry: int | None = None


class DurableSseParseError(ValueError):
    def __init__(self, message: str, raw_event: str) -> None:
        super().__init__(message)
        self.raw_event = raw_event


def parse_sse_text(text: str) -> list[DurableRunEvent]:
    parser = _SseParser()
    return [*parser.push(text), *parser.finish()]


def iter_sse_lines(lines: Iterable[str]) -> Iterator[DurableRunEvent]:
    parser = _SseParser()
    for line in lines:
        yield from parser.push(line)
    yield from parser.finish()


class _SseParser:
    def __init__(self) -> None:
        self._buffer = ""

    def push(self, chunk: str) -> list[DurableRunEvent]:
        self._buffer += chunk
        events: list[DurableRunEvent] = []

        while True:
            separator = self._find_separator()
            if separator is None:
                break

            index, length = separator
            frame = self._buffer[:index]
            self._buffer = self._buffer[index + length :]
            event = _parse_frame(frame)
            if event is not None:
                events.append(event)

        return events

    def finish(self) -> list[DurableRunEvent]:
        if not self._buffer.strip():
            self._buffer = ""
            return []

        event = _parse_frame(self._buffer)
        self._buffer = ""
        return [event] if event is not None else []

    def _find_separator(self) -> tuple[int, int] | None:
        crlf = self._buffer.find("\r\n\r\n")
        lf = self._buffer.find("\n\n")

        if crlf >= 0 and (lf < 0 or crlf < lf):
            return crlf, 4
        if lf >= 0:
            return lf, 2
        return None


def _parse_frame(frame: str) -> DurableRunEvent | None:
    data_lines: list[str] = []
    event_name = "message"
    event_id: str | None = None
    retry: int | None = None

    for line in frame.replace("\r\n", "\n").split("\n"):
        if not line or line.startswith(":"):
            continue

        field, _, raw_value = line.partition(":")
        value = raw_value[1:] if raw_value.startswith(" ") else raw_value

        if field == "event":
            event_name = value or "message"
        elif field == "data":
            data_lines.append(value)
        elif field == "id":
            event_id = value
        elif field == "retry":
            try:
                retry = int(value)
            except ValueError:
                retry = None

    if not data_lines:
        return None

    raw_data = "\n".join(data_lines)
    try:
        data = json.loads(raw_data)
    except json.JSONDecodeError as error:
        raise DurableSseParseError(f"Malformed Durable SSE payload: {error}", frame) from error

    return DurableRunEvent(event=event_name, data=data, raw_data=raw_data, id=event_id, retry=retry)
