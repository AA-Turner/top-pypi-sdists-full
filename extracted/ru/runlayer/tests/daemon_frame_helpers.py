"""Blocking frame I/O for tests that stand in for a daemon peer.

Production transports are a deadline-driven socket, an overlapped pipe handle,
and an anyio stream; none of them read blocking file objects. These helpers
exist only so tests can drive the real protocol from a plain binary stream.
"""

from __future__ import annotations

from typing import Protocol

from runlayer_cli.hook.daemon_protocol import (
    FRAME_PREFIX_SIZE,
    FrameError,
    decode_frame,
    encode_frame,
    frame_body_length,
)


class BlockingFrameStream(Protocol):
    def read(self, size: int | None = -1) -> bytes | None: ...

    def write(self, data: bytes) -> int | None: ...

    def flush(self) -> None: ...


def read_frame(stream: BlockingFrameStream) -> object:
    """Read one complete frame from a blocking binary stream."""
    length = frame_body_length(_read_exactly(stream, FRAME_PREFIX_SIZE))
    return decode_frame(_read_exactly(stream, length))


def write_frame(stream: BlockingFrameStream, payload: object) -> None:
    """Write and flush one complete frame to a blocking binary stream."""
    framed = encode_frame(payload)
    offset = 0
    while offset < len(framed):
        written = stream.write(framed[offset:])
        if written is None or written <= 0:
            raise FrameError("frame write made no progress")
        offset += written
    stream.flush()


def _read_exactly(stream: BlockingFrameStream, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise FrameError("frame ended before declared length")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)
