"""The metered upstream proxy: Chrome's paid-exit traffic is counted and
authenticated — proven over real sockets against a stand-in upstream proxy."""

from __future__ import annotations

import asyncio
import base64

import pytest

from matrx_scraper.upstream_proxy_meter import MeteredUpstreamProxy


async def _fake_upstream(seen: list[bytes]):
    async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        head = await reader.readuntil(b"\r\n\r\n")
        seen.append(head)
        if head.startswith(b"CONNECT"):
            writer.write(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            await writer.drain()
            data = await reader.read(1024)
            writer.write(b"echo:" + data)
        else:
            writer.write(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nok")
        await writer.drain()
        writer.close()

    server = await asyncio.start_server(handle, host="127.0.0.1", port=0)
    return server, server.sockets[0].getsockname()[1]


@pytest.mark.asyncio
async def test_connect_is_authenticated_upstream_and_every_byte_is_counted():
    seen: list[bytes] = []
    server, port = await _fake_upstream(seen)
    meter = await MeteredUpstreamProxy.start(f"http://127.0.0.1:{port}", "login", "pw")
    try:
        host, local_port = meter.proxy_url.removeprefix("http://").split(":")
        reader, writer = await asyncio.open_connection(host, int(local_port))
        writer.write(b"CONNECT site.example:443 HTTP/1.1\r\nHost: site.example:443\r\n\r\n")
        await writer.drain()
        established = await reader.readuntil(b"\r\n\r\n")
        writer.write(b"hello")
        await writer.drain()
        echoed = await reader.read(1024)
        writer.close()
    finally:
        await meter.close()
        server.close()

    assert established.startswith(b"HTTP/1.1 200")
    assert echoed == b"echo:hello"
    token = base64.b64encode(b"login:pw")
    assert b"Proxy-Authorization: Basic " + token in seen[0]
    assert meter.bytes_total >= len(seen[0]) + len(b"hello") + len(echoed)
    assert meter.connections_opened == 1


@pytest.mark.asyncio
async def test_plain_http_closes_so_no_unauthenticated_second_request_rides_it():
    seen: list[bytes] = []
    server, port = await _fake_upstream(seen)
    meter = await MeteredUpstreamProxy.start(f"http://login:pw@127.0.0.1:{port}")
    try:
        host, local_port = meter.proxy_url.removeprefix("http://").split(":")
        reader, writer = await asyncio.open_connection(host, int(local_port))
        writer.write(
            b"GET http://site.example/ HTTP/1.1\r\nHost: site.example\r\n"
            b"Proxy-Connection: keep-alive\r\n\r\n"
        )
        await writer.drain()
        body = await reader.read()
        writer.close()
    finally:
        await meter.close()
        server.close()

    assert body.endswith(b"ok")
    assert b"Connection: close" in seen[0]
    assert b"keep-alive" not in seen[0]
    assert b"Proxy-Authorization: Basic" in seen[0]
    assert meter.bytes_total > 0
