"""Server-sent event decoding."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator, Iterator
from typing import Any, Protocol


class ServerSentEvent:
    def __init__(
        self,
        *,
        event: str | None = None,
        data: str | None = None,
        id: str | None = None,
        retry: int | None = None,
    ) -> None:
        self._event = event or None
        self._data = data or ""
        self._id = id
        self._retry = retry

    @property
    def event(self) -> str | None:
        return self._event

    @property
    def data(self) -> str:
        return self._data

    @property
    def id(self) -> str | None:
        return self._id

    @property
    def retry(self) -> int | None:
        return self._retry

    def json(self) -> Any:
        return json.loads(self.data)

    def __repr__(self) -> str:
        return f"ServerSentEvent(event={self.event}, data={self.data}, id={self.id}, retry={self.retry})"


class SSEDecoder:
    def __init__(self) -> None:
        self._event: str | None = None
        self._data: list[str] = []
        self._last_event_id: str | None = None
        self._retry: int | None = None

    def iter_bytes(self, iterator: Iterator[bytes]) -> Iterator[ServerSentEvent]:
        for chunk in self._iter_chunks(iterator):
            for raw_line in chunk.splitlines():
                event = self.decode(raw_line.decode("utf-8"))
                if event is not None:
                    yield event

    def _iter_chunks(self, iterator: Iterator[bytes]) -> Iterator[bytes]:
        data = b""
        for chunk in iterator:
            for line in chunk.splitlines(keepends=True):
                data += line
                if data.endswith((b"\r\r", b"\n\n", b"\r\n\r\n")):
                    yield data
                    data = b""
        if data:
            yield data

    async def aiter_bytes(self, iterator: AsyncIterator[bytes]) -> AsyncIterator[ServerSentEvent]:
        async for chunk in self._aiter_chunks(iterator):
            for raw_line in chunk.splitlines():
                event = self.decode(raw_line.decode("utf-8"))
                if event is not None:
                    yield event

    async def _aiter_chunks(self, iterator: AsyncIterator[bytes]) -> AsyncIterator[bytes]:
        data = b""
        async for chunk in iterator:
            for line in chunk.splitlines(keepends=True):
                data += line
                if data.endswith((b"\r\r", b"\n\n", b"\r\n\r\n")):
                    yield data
                    data = b""
        if data:
            yield data

    def decode(self, line: str) -> ServerSentEvent | None:
        if not line:
            if not self._event and not self._data and not self._last_event_id and self._retry is None:
                return None
            event = ServerSentEvent(
                event=self._event,
                data="\n".join(self._data),
                id=self._last_event_id,
                retry=self._retry,
            )
            self._event = None
            self._data = []
            self._retry = None
            return event

        if line.startswith(":"):
            return None

        field, _, value = line.partition(":")
        if value.startswith(" "):
            value = value[1:]
        if field == "event":
            self._event = value
        elif field == "data":
            self._data.append(value)
        elif field == "id" and "\0" not in value:
            self._last_event_id = value
        elif field == "retry":
            try:
                self._retry = int(value)
            except ValueError:
                pass
        return None


class SSEBytesDecoder(Protocol):
    def iter_bytes(self, iterator: Iterator[bytes]) -> Iterator[ServerSentEvent]: ...

    def aiter_bytes(self, iterator: AsyncIterator[bytes]) -> AsyncIterator[ServerSentEvent]: ...
