"""Put the test's fake API on the container network without opening the host firewall.

The fake server runs inside pytest and listens on a UNIX socket that is bind-mounted
into this container at RELAY_SOCKET. This relay accepts TCP on :80 and TLS on :443
and pipes every connection to that socket. Containers reach it as ``api`` (and as
``r2.test``, the host the fake hands out for presigned and multipart uploads).

Why not listen on the host: the box's firewall drops container-to-host traffic, and
opening it is a change to shared infrastructure. A socket file crosses the network
namespace boundary without either.
"""

from __future__ import annotations

import asyncio
import os
import ssl

SOCKET = os.environ.get("RELAY_SOCKET", "/relay/fake.sock")
CERT = os.environ.get("RELAY_CERT", "/relay/server.pem")
KEY = os.environ.get("RELAY_KEY", "/relay/server.key")


async def _pipe(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    try:
        while True:
            data = await reader.read(1 << 16)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    except (ConnectionError, asyncio.IncompleteReadError, ssl.SSLError):
        pass
    finally:
        try:
            if writer.can_write_eof():
                writer.write_eof()
            else:
                writer.close()
        except (OSError, RuntimeError):
            pass


async def _handle(client_r: asyncio.StreamReader, client_w: asyncio.StreamWriter) -> None:
    try:
        up_r, up_w = await asyncio.open_unix_connection(SOCKET)
    except OSError:
        client_w.close()
        return
    await asyncio.gather(_pipe(client_r, up_w), _pipe(up_r, client_w))
    for w in (up_w, client_w):
        try:
            w.close()
        except (OSError, RuntimeError):
            pass


async def main() -> None:
    servers = [await asyncio.start_server(_handle, "0.0.0.0", 80)]
    if os.path.exists(CERT):
        ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ctx.load_cert_chain(CERT, KEY)
        servers.append(await asyncio.start_server(_handle, "0.0.0.0", 443, ssl=ctx))
    print(f"relay up: {len(servers)} listener(s) -> {SOCKET}", flush=True)
    await asyncio.gather(*(s.serve_forever() for s in servers))


if __name__ == "__main__":
    asyncio.run(main())
