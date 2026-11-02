"""Typed SSE parsing for SDK streams."""

from __future__ import annotations

from collections.abc import Iterable, Iterator

from labqoat.errors.api_error import ApiError
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.sse_fields import SseFields


class SseClient:
    """Parse SSE frames and event metadata."""

    @staticmethod
    def parse_stream(chunks: Iterable[bytes]) -> Iterator[JsonDocument]:
        """Parse SSE byte chunks into envelope dicts."""
        for frame in SseClient._frames(chunks):
            parsed = SseClient.parse_frame(frame)
            if parsed is not None:
                yield parsed

    @staticmethod
    def parse_events(chunks: Iterable[bytes]) -> Iterator[JsonDocument]:
        """Keep SSE metadata separate from the unmodified JSON event data."""
        import json

        for frame in SseClient._frames(chunks):
            fields = SseClient.split_fields(frame)
            if fields["data"]:
                try:
                    data = json.loads("\n".join(fields["data"]))
                except ValueError as error:
                    raise ApiError("Malformed JSON in server-sent event") from error
                yield JsonDocument({"event": fields["event"], "id": fields["id"], "data": data})

    @staticmethod
    def _frames(chunks: Iterable[bytes]) -> Iterator[bytes]:
        """Reassemble complete frames across arbitrary transport chunks."""
        buffer = b""
        for chunk in chunks:
            buffer += chunk
            while b"\n\n" in buffer:
                frame, buffer = buffer.split(b"\n\n", 1)
                yield frame

    @staticmethod
    def parse_frame(frame: bytes) -> JsonDocument | None:
        """Parse one SSE frame."""
        fields = SseClient.split_fields(frame)
        if not fields["data"]:
            return None
        return SseClient.decode_payload(fields)

    @staticmethod
    def split_fields(frame: bytes) -> SseFields:
        """Split a frame into id, event, and data lines."""
        fields: SseFields = {"id": None, "event": "message", "data": []}
        for raw_line in frame.decode("utf-8", errors="replace").splitlines():
            SseClient.apply_line(fields, raw_line)
        return fields

    @staticmethod
    def apply_line(fields: SseFields, raw_line: str) -> None:
        """Apply one SSE line to the field accumulator."""
        if raw_line.startswith(":"):
            return
        if raw_line.startswith("id:"):
            fields["id"] = raw_line[3:].strip()
        elif raw_line.startswith("event:"):
            fields["event"] = raw_line[6:].strip()
        elif raw_line.startswith("data:"):
            fields["data"].append(raw_line[5:].lstrip())

    @staticmethod
    def decode_payload(fields: SseFields) -> JsonDocument:
        """Decode data lines into an envelope dict."""
        import json

        try:
            payload = json.loads("\n".join(fields["data"]))
        except ValueError:
            result: JsonDocument = JsonDocument({"type": "parse_error", "event": fields["event"], "id": fields["id"]})
            return result
        if isinstance(payload, dict):
            payload.setdefault("cursor", fields["id"])
            payload.setdefault("type", fields["event"])
            return JsonDocument(payload)
        data: JsonValue = payload
        return JsonDocument({"type": fields["event"], "id": fields["id"], "data": data})
