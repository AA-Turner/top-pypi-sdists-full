"""Frames of a service tunnel as the control plane writes and reads them."""

from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class ServiceFrame:
    """One typed frame of one stream: a kind byte, the stream's number and a payload.

    A caller's request arrives as ``OPEN`` (method, path and headers), ``DATA`` and ``FINISH``; the response
    goes back as ``HEAD``, ``DATA`` and ``FINISH``. Every ``DATA`` is answered by an ``ACK`` before the next
    is sent, and either side ends a stream early with ``RESET``.
    """

    OPEN: ClassVar[int] = 1
    DATA: ClassVar[int] = 2
    FINISH: ClassVar[int] = 3
    HEAD: ClassVar[int] = 4
    ACK: ClassVar[int] = 5
    RESET: ClassVar[int] = 6
    CHUNK: ClassVar[int] = 262_144

    kind: int
    stream: int
    payload: bytes = b""

    def encode(self) -> bytes:
        """Return the frame as it travels."""
        return bytes([self.kind]) + self.stream.to_bytes(8, "big") + self.payload

    @classmethod
    def decode(cls, data: bytes | str) -> "ServiceFrame":
        """Read a binary frame of a known kind; anything else is outside the protocol."""
        if isinstance(data, str) or len(data) < 9 or not cls.OPEN <= data[0] <= cls.RESET:
            raise ValueError("Service tunnel frame is outside the protocol")
        return cls(data[0], int.from_bytes(data[1:9], "big"), data[9:])
