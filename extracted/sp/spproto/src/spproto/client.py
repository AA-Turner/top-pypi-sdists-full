import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from .auth import auth
from .connection import Connection
from .transport.stream import StreamTransport


@asynccontextmanager
async def connect(
    host: str,
    port: int,
    privkey_b: bytes,
    peer_pubkey_b: bytes
) -> AsyncIterator[Connection]:
    reader, writer = await asyncio.open_connection(host, port)
    try:
        transport = StreamTransport(reader, writer)
        connection = await auth(transport, privkey_b, peer_pubkey_b)
        yield connection
    finally:
        writer.close()
        await writer.wait_closed()
