"""Residential egress, proven end to end without a gateway, a device or a site.

Two halves, both real:

* `EgressAdapter` is exercised against an IN-PROCESS fake gateway — a real
  WebSocket server speaking the contract's consumer leg (first TEXT frame
  `{"ok":…}`, then binary both ways) which opens a real TCP connection to a
  real local origin. A `CONNECT` tunnel and an absolute-URL plain HTTP request
  both go through it, so the bytes this proxy speaks are the bytes a browser
  and httpx actually send.
* `orchestrator.scrape()` is exercised with a forced `cloudflare_block` and a
  fake ticket ext. The retry leg is NOT faked: it goes through the adapter, the
  fake gateway and the local origin, so "one residential retry happened" is a
  fact about the wire, not about a mock's call count.

Contract: `common-docs/systems/platform/residential-egress/FEATURE.md`.
"""

from __future__ import annotations

import asyncio
import json
import urllib.parse
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager

import httpx
import pytest

from matrx_scraper import _ext as ext_registry
from matrx_scraper.egress_adapter import EgressAdapter
from matrx_scraper.scraper import ContentType, FailureReason, RequestType, Response

pytestmark = pytest.mark.asyncio

DEVICE_NAME = "Arman's MacBook Pro"

_ARTICLE = (
    "<html><head><title>The page a stranger cannot read</title></head><body>"
    "<article><h1>The page a stranger cannot read</h1>"
    + "<p>"
    + (
        "This paragraph exists so the content-sanity gate sees a real article "
        "rather than a shell. It is deliberately long. "
    )
    * 12
    + "</p></article></body></html>"
)


# ── the fake gateway ────────────────────────────────────────────────────────


@asynccontextmanager
async def fake_gateway(*, refuse: dict | None = None) -> AsyncIterator[str]:
    """A real WebSocket server speaking the contract's consumer leg.

    Yields the `consume_url` an `EgressAdapter` takes. `refuse` makes it answer
    every stream with that refusal object instead of opening one, which is what
    a paused or offline computer looks like from here.
    """
    from websockets.asyncio.server import serve

    seen_headers: list[dict[str, str]] = []

    async def handler(websocket) -> None:
        request = websocket.request
        seen_headers.append(dict(request.headers))
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(request.path).query)
        host = query.get("host", [""])[0]
        port = int(query.get("port", ["0"])[0])

        if refuse is not None:
            await websocket.send(json.dumps(refuse))
            return

        try:
            reader, writer = await asyncio.open_connection(host, port)
        except OSError as exc:
            await websocket.send(
                json.dumps(
                    {
                        "ok": False,
                        "error": "refused",
                        "message": f"The computer could not reach that address ({exc.errno}).",
                    }
                )
            )
            return

        await websocket.send(json.dumps({"ok": True, "device_name": DEVICE_NAME}))

        async def ws_to_tcp() -> None:
            async for message in websocket:
                writer.write(message if isinstance(message, bytes) else message.encode())
                await writer.drain()

        async def tcp_to_ws() -> None:
            while True:
                chunk = await reader.read(65536)
                if not chunk:
                    return
                await websocket.send(chunk)

        up = asyncio.create_task(ws_to_tcp())
        down = asyncio.create_task(tcp_to_ws())
        try:
            await asyncio.wait({up, down}, return_when=asyncio.FIRST_COMPLETED)
        finally:
            for task in (up, down):
                task.cancel()
            await asyncio.gather(up, down, return_exceptions=True)
            writer.close()

    server = await serve(handler, "127.0.0.1", 0)
    port = server.sockets[0].getsockname()[1]
    try:
        yield f"ws://127.0.0.1:{port}/egress/consume"
    finally:
        server.close()
        await server.wait_closed()


@asynccontextmanager
async def echo_server() -> AsyncIterator[tuple[str, int]]:
    async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            while True:
                chunk = await reader.read(4096)
                if not chunk:
                    return
                writer.write(chunk)
                await writer.drain()
        finally:
            writer.close()

    server = await asyncio.start_server(handle, "127.0.0.1", 0)
    try:
        yield "127.0.0.1", server.sockets[0].getsockname()[1]
    finally:
        server.close()
        await server.wait_closed()


@asynccontextmanager
async def origin_server(body: str = _ARTICLE) -> AsyncIterator[str]:
    """A minimal HTTP/1.1 origin: one page, one connection, then close."""

    async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            await reader.readuntil(b"\r\n\r\n")
        except Exception:  # noqa: BLE001
            writer.close()
            return
        payload = body.encode()
        writer.write(
            b"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n"
            b"Content-Length: " + str(len(payload)).encode() + b"\r\n"
            b"Connection: close\r\n\r\n" + payload
        )
        await writer.drain()
        writer.close()

    server = await asyncio.start_server(handle, "127.0.0.1", 0)
    try:
        yield f"http://127.0.0.1:{server.sockets[0].getsockname()[1]}/story"
    finally:
        server.close()
        await server.wait_closed()


# ── the adapter ─────────────────────────────────────────────────────────────


async def test_connect_tunnel_carries_bytes_both_ways() -> None:
    async with echo_server() as (host, port), fake_gateway() as consume_url:
        adapter = await EgressAdapter.start("mxt_test_ticket", consume_url)
        try:
            assert adapter.proxy_url.startswith("http://127.0.0.1:")
            reader, writer = await asyncio.open_connection("127.0.0.1", adapter.port)
            writer.write(
                f"CONNECT {host}:{port} HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n".encode()
            )
            await writer.drain()
            status = await reader.readuntil(b"\r\n\r\n")
            assert status.startswith(b"HTTP/1.1 200 Connection Established")

            payload = b"ping over somebody's home internet"
            writer.write(payload)
            await writer.drain()
            echoed = await asyncio.wait_for(
                reader.readexactly(len(payload)), timeout=10
            )
            assert echoed == payload
            writer.close()
        finally:
            await adapter.close()

        assert adapter.device_name == DEVICE_NAME
        assert adapter.streams_opened == 1


async def test_plain_http_absolute_url_is_rewritten_and_relayed() -> None:
    async with origin_server() as url, fake_gateway() as consume_url:
        adapter = await EgressAdapter.start("mxt_test_ticket", consume_url)
        try:
            async with httpx.AsyncClient(proxy=adapter.proxy_url, timeout=15) as client:
                response = await client.get(url)
            assert response.status_code == 200
            assert "The page a stranger cannot read" in response.text
        finally:
            await adapter.close()


async def test_a_refusal_reaches_the_local_client_as_a_sentence() -> None:
    refusal = {
        "ok": False,
        "error": "device_offline",
        "message": "That computer is not connected right now.",
    }
    async with fake_gateway(refuse=refusal) as consume_url:
        adapter = await EgressAdapter.start("mxt_test_ticket", consume_url)
        try:
            reader, writer = await asyncio.open_connection("127.0.0.1", adapter.port)
            writer.write(b"CONNECT example.com:443 HTTP/1.1\r\nHost: example.com:443\r\n\r\n")
            await writer.drain()
            answer = await asyncio.wait_for(reader.read(4096), timeout=10)
            assert answer.startswith(b"HTTP/1.1 502")
            assert b"That computer is not connected right now." in answer
            writer.close()
        finally:
            await adapter.close()


async def test_this_module_never_logs_the_ticket(caplog: pytest.LogCaptureFixture) -> None:
    """The ticket is a bearer credential: it lives in ONE header and nowhere
    else. (The `websockets` library's own DEBUG logging prints every header it
    sends, which is its business and not a log line this package emits — so the
    claim under test is about `matrx_scraper`'s records and about the URL.)"""
    from matrx_scraper.egress_adapter import _consume_uri

    secret = "mxt_7f3a_this_must_never_be_logged"
    async with echo_server() as (host, port), fake_gateway() as consume_url:
        adapter = await EgressAdapter.start(secret, consume_url)
        try:
            with caplog.at_level("DEBUG"):
                reader, writer = await asyncio.open_connection("127.0.0.1", adapter.port)
                writer.write(f"CONNECT {host}:{port} HTTP/1.1\r\n\r\n".encode())
                await writer.drain()
                await reader.readuntil(b"\r\n\r\n")
                writer.close()
        finally:
            await adapter.close()
    ours = "\n".join(
        record.getMessage()
        for record in caplog.records
        if record.name.startswith("matrx_scraper")
    )
    assert secret not in ours
    assert secret not in _consume_uri(consume_url, "example.com", 443)


# ── the orchestrator's one retry ────────────────────────────────────────────


@pytest.fixture
def egress_exts() -> Callable[..., list[str]]:
    """Register the two host exts for one test, and remove them afterwards."""
    registered: list[str] = []

    def _register(**kwargs) -> list[str]:
        ext_registry.configure_ext(**kwargs)
        registered.extend(kwargs)
        return registered

    yield _register

    for key in registered:
        ext_registry._registry.pop(key, None)


def _blocked(url: str) -> Response:
    return Response(
        request_url=url,
        proxy_used=True,
        request_type=RequestType.NORMAL,
        content_type=ContentType.HTML,
        extension="",
        content_type_raw="text/html",
        response_url=url,
        response_headers={},
        status_code=403,
        content="",
        failed=True,
        failed_primary_reason=FailureReason.CLOUDFLARE_BLOCK,
        failed_reasons=[{FailureReason.CLOUDFLARE_BLOCK: "bot check"}],
    )


@pytest.fixture
def blocked_everywhere_but_home(monkeypatch: pytest.MonkeyPatch) -> dict[str, list[str]]:
    """Every datacenter fetch is a Cloudflare block; a proxied fetch is REAL.

    The proxied leg really goes out through whatever proxy it is handed, so the
    adapter, the gateway and the origin are all exercised — nothing about the
    retry is simulated except the block that provokes it.
    """
    from matrx_scraper import orchestrator

    seen: dict[str, list[str]] = {"direct": [], "proxied": []}

    async def fake_fetch(
        url: str,
        request_type: RequestType = RequestType.NORMAL,
        proxy: str | None = None,
        use_curl_cffi: bool = True,
        header_profile: dict | None = None,
        user_agent: str | None = None,
    ) -> Response:
        if proxy is None:
            seen["direct"].append(url)
            return _blocked(url)
        seen["proxied"].append(proxy)
        async with httpx.AsyncClient(proxy=proxy, timeout=15) as client:
            answer = await client.get(url)
        return Response(
            request_url=url,
            proxy_used=True,
            request_type=RequestType.NORMAL,
            content_type=ContentType.HTML,
            extension="",
            content_type_raw="text/html",
            response_url=str(answer.url),
            response_headers=dict(answer.headers),
            status_code=answer.status_code,
            content=answer.text,
        )

    async def fake_proxied(
        url: str, use_random_proxy: bool = True, user_agent: str | None = None
    ) -> Response:
        seen["direct"].append(url)
        return _blocked(url)

    monkeypatch.setattr(orchestrator, "fetch", fake_fetch)
    monkeypatch.setattr(orchestrator, "fetch_normally_with_proxy", fake_proxied)
    monkeypatch.setattr(orchestrator, "CHALLENGE_RETRY_DELAY_SECONDS", 0.0)
    return seen


def _residential_entries(result) -> list[dict]:
    return [entry for entry in result.rung_trail if entry["rung"] == "residential"]


async def test_a_blocked_page_is_retried_once_through_the_persons_computer(
    blocked_everywhere_but_home: dict[str, list[str]],
    egress_exts: Callable[..., list[str]],
) -> None:
    from matrx_scraper.orchestrator import scrape

    async with origin_server() as url, fake_gateway() as consume_url:
        tickets: list[tuple[str, str | None]] = []

        async def ticket_ext(acting_user_id: str, token: str | None) -> dict:
            tickets.append((acting_user_id, token))
            return {
                "ticket": "mxt_test_ticket",
                "consume_url": consume_url,
                "device_name": DEVICE_NAME,
            }

        async def reasons_ext() -> list[str]:
            return ["cloudflare_block", "bad_status:403"]

        egress_exts(
            residential_egress_ticket=ticket_ext,
            residential_egress_retry_reasons=reasons_ext,
        )

        result = await scrape(
            url,
            escalate=False,
            acting_user_id="11111111-2222-3333-4444-555555555555",
        )

    assert [user for user, _ in tickets] == ["11111111-2222-3333-4444-555555555555"]
    # EXACTLY ONE retry through the home computer — never a loop, never a second
    # ticket spent on the same page.
    assert len(blocked_everywhere_but_home["proxied"]) == 1
    assert result.success is True
    assert result.egress == "residential"
    assert result.egress_device_name == DEVICE_NAME
    assert result.escalation_note == (
        f"The site blocked our servers, so we fetched it through {DEVICE_NAME}."
    )
    assert result.to_dict()["egress"] == "residential"
    assert result.to_dict()["egress_device_name"] == DEVICE_NAME

    entries = _residential_entries(result)
    assert len(entries) == 1
    assert entries[0]["ok"] is True
    assert DEVICE_NAME in entries[0]["note"]
    # The ladder law still holds with the optional entry in the trail.
    from matrx_scraper.ladder import assert_no_skipped_rung

    assert_no_skipped_rung(result.rung_trail)


async def test_no_signed_in_person_means_no_retry_and_the_trail_says_why(
    blocked_everywhere_but_home: dict[str, list[str]],
    egress_exts: Callable[..., list[str]],
) -> None:
    from matrx_scraper.orchestrator import scrape

    async with origin_server() as url, fake_gateway() as consume_url:
        called: list[str] = []

        async def ticket_ext(acting_user_id: str, token: str | None) -> dict:
            called.append(acting_user_id)
            return {
                "ticket": "mxt_test_ticket",
                "consume_url": consume_url,
                "device_name": DEVICE_NAME,
            }

        egress_exts(residential_egress_ticket=ticket_ext)

        result = await scrape(url, escalate=False)  # no acting_user_id

    assert called == []
    assert blocked_everywhere_but_home["proxied"] == []
    assert result.success is False
    assert result.egress != "residential"
    entries = _residential_entries(result)
    assert len(entries) == 1
    assert entries[0]["ok"] is False
    assert "signed in" in entries[0]["note"]


async def test_a_do_not_proxy_domain_is_never_sent_out_of_a_home(
    blocked_everywhere_but_home: dict[str, list[str]],
    egress_exts: Callable[..., list[str]],
) -> None:
    from matrx_scraper.orchestrator import scrape

    class DirectOnlyDomains:
        def is_scrape_allowed(self, url: str) -> bool:
            return True

        def get_proxy_type(self, url: str) -> str:
            return "none"

    async with origin_server() as url, fake_gateway() as consume_url:
        called: list[str] = []

        async def ticket_ext(acting_user_id: str, token: str | None) -> dict:
            called.append(acting_user_id)
            return {
                "ticket": "mxt_test_ticket",
                "consume_url": consume_url,
                "device_name": DEVICE_NAME,
            }

        egress_exts(residential_egress_ticket=ticket_ext)

        result = await scrape(
            url,
            escalate=False,
            domain_config=DirectOnlyDomains(),
            acting_user_id="11111111-2222-3333-4444-555555555555",
        )

    assert called == []
    assert blocked_everywhere_but_home["proxied"] == []
    assert result.egress != "residential"
    entries = _residential_entries(result)
    assert len(entries) == 1
    assert entries[0]["ok"] is False
    assert "direct connection" in entries[0]["note"]


async def test_an_unwired_host_does_nothing_and_says_so(
    blocked_everywhere_but_home: dict[str, list[str]],
) -> None:
    from matrx_scraper.orchestrator import scrape

    assert not ext_registry.has_ext("residential_egress_ticket")

    async with origin_server() as url:
        result = await scrape(
            url,
            escalate=False,
            acting_user_id="11111111-2222-3333-4444-555555555555",
        )

    assert blocked_everywhere_but_home["proxied"] == []
    entries = _residential_entries(result)
    assert len(entries) == 1
    assert entries[0]["note"] == "residential egress is not wired on this host"
