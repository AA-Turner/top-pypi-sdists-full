"""Immutable wire snapshots and bounded adjacent-frame compaction."""

import json

from labqoat.json_document import JsonValue


class TelemetryFrames:
    """Preserve arrival order while grouping compatible evidence into server-sized frames."""

    @staticmethod
    def encode(kind: str, entries: list[JsonValue]) -> bytes:
        """Validate and snapshot caller-owned values before asynchronous delivery."""
        body = json.dumps({"kind": kind, "entries": entries}, separators=(",", ":"), allow_nan=False).encode()
        if kind not in {"logs", "metrics"} or not 1 <= len(entries) <= 500 or len(body) > 1_048_576:
            raise ValueError("Telemetry requires a bounded logs or metrics frame")
        return len(body).to_bytes(4, "big") + body

    @staticmethod
    def combine(frames: list[bytes]) -> list[bytes]:
        """Coalesce frames of one kind, in arrival order, without crossing entry or encoded-byte limits.

        Logs and metrics are independent evidence, so interleaved producers still fill one frame per kind.
        """
        kinds: dict[str, list[tuple[int, list[JsonValue]]]] = {}
        for frame in frames:
            message = json.loads(frame[4:])
            kinds.setdefault(message["kind"], []).append((len(frame), message["entries"]))
        combined: list[bytes] = []
        for kind, batches in kinds.items():
            combined.extend(TelemetryFrames._compact(kind, batches))
        return combined

    @staticmethod
    def _compact(kind: str, batches: list[tuple[int, list[JsonValue]]]) -> list[bytes]:
        """Merge one kind's batches while a frame stays within limits and holds each replay identity once."""
        combined: list[bytes] = []
        entries: list[JsonValue] = []
        size = 0
        keys: set[str] = set()
        for length, batch in batches:
            incoming = TelemetryFrames._keys(kind, batch)
            full = len(entries) + len(batch) > 500 or size + length > 1_048_580
            if entries and (full or not keys.isdisjoint(incoming)):
                combined.append(TelemetryFrames.encode(kind, entries))
                entries, size, keys = [], 0, set()
            entries.extend(batch)
            size += length
            keys.update(incoming)
        combined.append(TelemetryFrames.encode(kind, entries))
        return combined

    @staticmethod
    def _keys(kind: str, entries: list[JsonValue]) -> set[str]:
        """Keep replayed identities in separate frames so server uniqueness checks remain valid."""
        fields = ("step", "name") if kind == "metrics" else ("seq",)
        return {json.dumps([entry.get(field) for field in fields]) for entry in entries if isinstance(entry, dict)}
