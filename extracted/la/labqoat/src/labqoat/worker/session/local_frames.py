"""Length-prefixed local JSON messages carry no executable serialization."""

import asyncio
from collections.abc import Mapping
from typing import BinaryIO

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.worker.session.session_frames import SessionFrames
from labqoat.worker.worker_api_error import WorkerApiError


class LocalFrames:
    """Bound local control messages before allocating or reading invocation payloads."""

    @staticmethod
    def encode(document: Mapping[str, JsonValue]) -> bytes:
        """Prefix strict UTF-8 JSON with its unsigned network-order byte length."""
        content = SessionFrames.encode(document).encode()
        return len(content).to_bytes(4, "big") + content

    @staticmethod
    def size(header: bytes) -> int:
        """Reject truncated headers, empty messages and sizes outside the remote wire bound."""
        size = int.from_bytes(header, "big")
        if len(header) != 4 or not 0 < size <= SessionFrames.maximum:
            raise WorkerApiError("Local worker session frame is invalid", 502)
        return size

    @staticmethod
    def read(source: BinaryIO) -> JsonDocument:
        """Read exactly one bounded response from a blocking local socket file."""
        size = LocalFrames.size(source.read(4))
        content = source.read(size)
        if len(content) != size:
            raise WorkerApiError("Local worker session response was truncated")
        return SessionFrames.decode(content)

    @staticmethod
    async def read_async(source: asyncio.StreamReader) -> JsonDocument:
        """Cancellation interrupts local I/O immediately without leaving an executor thread."""
        size = LocalFrames.size(await source.readexactly(4))
        return SessionFrames.decode(await source.readexactly(size))
