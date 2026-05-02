import asyncio
from collections.abc import Callable, Awaitable
from typing import Never

from .auth import auth
from .connection import Connection
from .transport.stream import StreamTransport


async def serve(
    host: str,
    port: int,
    privkey_b: bytes,
    peer_pubkey_b: bytes,
    callback: Callable[[Connection], Awaitable[None | Never]]
) -> None:

    async def handle(
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter
    ) -> None:
        try:
            transport = StreamTransport(reader, writer)
            connection = await auth(transport, privkey_b, peer_pubkey_b)
            await callback(connection)
        finally:
            writer.close()
            await writer.wait_closed()

    server = await asyncio.start_server(handle, host, port)
    async with server:
        await server.serve_forever()
