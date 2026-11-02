"""Connection budgets apply to real HTTP requests, independently of WebSockets."""

import asyncio

import pytest

from runta import AsyncRunta, Runta


@pytest.mark.parametrize("client_type", [Runta, AsyncRunta])
@pytest.mark.parametrize("size", [True, False, 0, -1, 1.5, "250"])
def test_invalid_pool_size(client_type, size):
    with pytest.raises(ValueError, match="connection_pool_maxsize"):
        client_type(token="test", connection_pool_maxsize=size)


@pytest.mark.parametrize("size", [250, 1, 10, None])
def test_sync_connection_limits(size):
    with Runta(token="test", connection_pool_maxsize=size) as client:
        limits = client._http._client._httpx_args["limits"]
        assert limits.max_connections == size
        assert limits.max_keepalive_connections is None
        assert limits.keepalive_expiry == 30.0


@pytest.mark.asyncio
@pytest.mark.parametrize("size", [250, 1, 10, None])
async def test_async_connection_limits(size):
    async with AsyncRunta(token="test", connection_pool_maxsize=size) as client:
        connector = client._http._get_session().connector
        assert connector.limit == (0 if size is None else size)
        assert connector.limit_per_host == 0
        assert connector._keepalive_timeout == 30.0


@pytest.mark.asyncio
async def test_default_connection_limits():
    with Runta(token="test") as sync:
        assert sync._http._client._httpx_args["limits"].max_connections == 250
    async with AsyncRunta(token="test") as client:
        assert client._http._get_session().connector.limit == 250


@pytest.mark.asyncio
@pytest.mark.parametrize("size", [1, None])
async def test_http_pool_waits_until_connection_is_released(size):
    arrived = asyncio.Queue()
    release = asyncio.Event()
    handlers = set()

    async def handler(reader, writer):
        task = asyncio.current_task()
        handlers.add(task)
        try:
            await reader.readuntil(b"\r\n\r\n")
            arrived.put_nowait(True)
            await release.wait()
            writer.write(
                b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
            )
            await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()
            handlers.remove(task)

    server = await asyncio.start_server(handler, "127.0.0.1", 0)
    port = server.sockets[0].getsockname()[1]
    try:
        async with AsyncRunta(
            token="test",
            endpoint=f"http://127.0.0.1:{port}",
            connection_pool_maxsize=size,
        ) as client:
            tasks = [asyncio.create_task(client.health())]
            try:
                await asyncio.wait_for(arrived.get(), 2)
                tasks.append(asyncio.create_task(client.health()))
                if size == 1:
                    with pytest.raises(asyncio.TimeoutError):
                        await asyncio.wait_for(arrived.get(), 0.1)
                    release.set()
                    await asyncio.wait_for(arrived.get(), 2)
                else:
                    await asyncio.wait_for(arrived.get(), 2)
                    release.set()
                await asyncio.gather(*tasks)
            finally:
                release.set()
                for task in tasks:
                    task.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
    finally:
        release.set()
        server.close()
        await server.wait_closed()
        for task in list(handlers):
            await task
