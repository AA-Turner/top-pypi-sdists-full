import asyncio
import struct

from .abc import Transport


class StreamTransport(Transport):
    """
    --------------------
    | Length | Payload |
    --------------------
    """
    _LENGTH_STRUCT = struct.Struct('<Q')

    def __init__(self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter
    ) -> None:
        self._reader = reader
        self._writer = writer

    async def send(self,
        payload: bytes
    ) -> None:
        length_b = self._LENGTH_STRUCT.pack(len(payload))
        data = length_b + payload
        self._writer.write(data)
        await self._writer.drain()

    async def receive(self) -> bytes:
        length_b = await self._reader.readexactly(self._LENGTH_STRUCT.size)
        length, = self._LENGTH_STRUCT.unpack(length_b)
        payload = await self._reader.readexactly(length)
        return payload
