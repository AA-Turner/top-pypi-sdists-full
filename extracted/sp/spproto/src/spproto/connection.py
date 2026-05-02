from .protocol.abc import Protocol
from .transport.abc import Transport


class Connection:

    def __init__(self,
        transport: Transport,
        protocol: Protocol
    ) -> None:
        self._transport = transport
        self._protocol = protocol

    async def send(self,
        payload: bytes
    ) -> None:
        data = self._protocol.pack(payload)
        await self._transport.send(data)

    async def receive(self) -> bytes:
        data = await self._transport.receive()
        payload = self._protocol.unpack(data)
        return payload
