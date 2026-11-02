"""Frames of a sandbox process's output stream as the host writes them."""

import json
from collections.abc import AsyncIterable, AsyncIterator, Iterable, Iterator
from dataclasses import dataclass
from typing import ClassVar

from labqoat.json_document import JsonDocument
from labqoat.sandbox.sandbox_process_state import SandboxProcessState
from labqoat.sandbox.sandbox_unavailable_error import SandboxUnavailableError


@dataclass(frozen=True)
class SandboxOutputFrame:
    """One frame: a kind byte, the absolute offset of its bytes in their stream, their length, and the bytes.

    Standard output and standard error frames carry output at the offset they name, which jumps forward
    when the host no longer kept the part asked for. A heartbeat keeps a quiet connection alive. The exit
    frame carries the process's final state and is always the last.
    """

    HEARTBEAT: ClassVar[int] = 0
    STDOUT: ClassVar[int] = 1
    STDERR: ClassVar[int] = 2
    EXIT: ClassVar[int] = 3
    HEADER_BYTES: ClassVar[int] = 13
    LONGEST_PAYLOAD: ClassVar[int] = 16_777_216

    kind: int
    offset: int
    payload: bytes

    @property
    def end(self) -> int:
        """Return the stream offset just past this frame's bytes."""
        return self.offset + len(self.payload)

    def state(self) -> SandboxProcessState:
        """Read the final state an exit frame carries; anything else is outside the protocol."""
        try:
            return SandboxProcessState.decode(JsonDocument.expect_dict(json.loads(self.payload)))
        except (KeyError, TypeError, ValueError) as error:
            raise SandboxUnavailableError("Sandbox host returned a malformed process state") from error

    @classmethod
    def parse(cls, chunks: Iterable[bytes]) -> Iterator["SandboxOutputFrame"]:
        """Yield each frame once its last byte has arrived, however the bytes were split."""
        buffer = bytearray()
        for chunk in chunks:
            buffer += chunk
            yield from cls._complete(buffer)

    @classmethod
    async def parse_async(cls, chunks: AsyncIterable[bytes]) -> AsyncIterator["SandboxOutputFrame"]:
        """Yield each frame once its last byte has arrived, without blocking the event loop."""
        buffer = bytearray()
        async for chunk in chunks:
            buffer += chunk
            for frame in cls._complete(buffer):
                yield frame

    @classmethod
    def _complete(cls, buffer: bytearray) -> list["SandboxOutputFrame"]:
        """Take every whole frame off the front of the buffer and leave a partial one in it."""
        frames = []
        while len(buffer) >= cls.HEADER_BYTES:
            kind, offset, length = buffer[0], int.from_bytes(buffer[1:9], "big"), int.from_bytes(buffer[9:13], "big")
            if kind > cls.EXIT or length > cls.LONGEST_PAYLOAD:
                raise SandboxUnavailableError("Sandbox host returned output outside the protocol")
            if len(buffer) < cls.HEADER_BYTES + length:
                break
            frames.append(cls(kind, offset, bytes(buffer[cls.HEADER_BYTES : cls.HEADER_BYTES + length])))
            del buffer[: cls.HEADER_BYTES + length]
        return frames
