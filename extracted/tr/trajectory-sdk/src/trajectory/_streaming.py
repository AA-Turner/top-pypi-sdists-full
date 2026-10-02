# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

import json
import re
from collections.abc import Iterator
from types import TracebackType
from typing import Any, Generic, TypeVar, cast

import httpx

from trajectory._exceptions import APIError
from trajectory._models import FinalRequestOptions

ChunkT = TypeVar("ChunkT")


class Stream(Generic[ChunkT]):
  """Iterate over a synchronous server-sent event response."""

  def __init__(
    self,
    cast_to: type[ChunkT],
    response: httpx.Response,
    client: Any,
    options: FinalRequestOptions | None = None,
  ) -> None:
    self.response = response
    self._cast_to = cast_to
    self._client = client
    self._options = options
    self._decoder = client._make_sse_decoder()
    self._iterator = self._stream()

  def __next__(self) -> ChunkT:
    return next(self._iterator)

  def __iter__(self) -> Iterator[ChunkT]:
    yield from self._iterator

  def _iter_events(self) -> Iterator["ServerSentEvent"]:
    yield from self._decoder.iter_bytes(self.response.iter_bytes())

  def _stream(self) -> Iterator[ChunkT]:
    cast_to = cast(Any, self._cast_to)
    try:
      for event in self._iter_events():
        if event.data.startswith("[DONE]"):
          break
        data = event.json()
        if isinstance(data, dict) and data.get("error"):
          error = data["error"]
          message = error.get("message") if isinstance(error, dict) else None
          raise APIError(
            message=message if isinstance(message, str) else "An error occurred during streaming",
            request=self.response.request,
            body=error,
          )
        processed_data = (
          {"event": event.event, "data": data}
          if self._options is not None and self._options.synthesize_event_and_data
          else data
        )
        yield self._client._process_response_data(
          data=processed_data,
          cast_to=cast_to,
          response=self.response,
        )
    finally:
      self.response.close()

  def __enter__(self) -> "Stream[ChunkT]":
    return self

  def __exit__(
    self,
    exc_type: type[BaseException] | None,
    exc_value: BaseException | None,
    traceback: TracebackType | None,
  ) -> None:
    self.close()

  def close(self) -> None:
    self.response.close()


class ServerSentEvent:
  def __init__(
    self,
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
    return (
      f"ServerSentEvent(event={self.event}, data={self.data}, id={self.id}, retry={self.retry})"
    )


_SSE_LINE_END = re.compile(b"[\r\n]")


class _SSELineDecoder:
  """Split CR, LF, and CRLF across arbitrary byte chunks."""

  def __init__(self) -> None:
    self._buffer = bytearray()
    self._skip_lf = False

  def _append(self, chunk: bytes, start: int, end: int) -> None:
    self._buffer.extend(memoryview(chunk)[start:end])

  def feed(self, chunk: bytes) -> Iterator[bytes]:
    start = 0
    for match in _SSE_LINE_END.finditer(chunk):
      end = match.start()
      if self._skip_lf and end == start and chunk[end] == 10:
        self._skip_lf = False
        start = end + 1
        continue
      self._skip_lf = False
      self._append(chunk, start, end)
      line = bytes(self._buffer)
      self._buffer.clear()
      self._skip_lf = chunk[end] == 13
      start = end + 1
      yield line
    if start < len(chunk):
      self._skip_lf = False
      self._append(chunk, start, len(chunk))

  def finish(self) -> Iterator[bytes]:
    if self._buffer:
      line = bytes(self._buffer)
      self._buffer.clear()
      yield line


class SSEDecoder:
  """Decode SSE fields without imposing a line or event size limit."""

  def __init__(self) -> None:
    self._reset()

  def _reset(self) -> None:
    self._is_first_line = True
    self._event: str | None = None
    self._data: list[str] = []
    self._last_event_id: str | None = None
    self._retry: int | None = None

  def _decode_lines(self, lines: Iterator[bytes]) -> Iterator[ServerSentEvent]:
    for raw_line in lines:
      line = raw_line.decode("utf-8")
      if self._is_first_line:
        self._is_first_line = False
        line = line.removeprefix("\ufeff")
      event = self.decode(line)
      if event is not None:
        yield event

  def iter_bytes(self, iterator: Iterator[bytes]) -> Iterator[ServerSentEvent]:
    line_decoder = _SSELineDecoder()
    try:
      for chunk in iterator:
        yield from self._decode_lines(line_decoder.feed(chunk))
      yield from self._decode_lines(line_decoder.finish())
    finally:
      self._reset()

  def decode(self, line: str) -> ServerSentEvent | None:
    if not line:
      if not self._data:
        self._event = None
        self._retry = None
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

    field_name, _, value = line.partition(":")
    if value.startswith(" "):
      value = value[1:]
    if field_name == "event":
      self._event = value
    elif field_name == "data":
      self._data.append(value)
    elif field_name == "id" and "\0" not in value:
      self._last_event_id = value
    elif field_name == "retry":
      try:
        self._retry = int(value)
      except ValueError:
        pass
    return None
