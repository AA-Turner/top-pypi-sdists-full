"""matrx-ai never fetches a model- or person-supplied URL inside our own network.

Use case: an agent helping Harbor Dental's front desk is told (by a person, or
by text it read on a web page) to fetch "the docs" at an address that is really
the cloud metadata service or a VPC host. The llms.txt tool, the media
download fallback and the remote MCP client must refuse before a byte leaves.

DNS (``socket.getaddrinfo``) and the wire (``httpcore`` pools, plus
``requests`` for the old sync download) are stubbed; the httpx clients — where
the guard lives — stay real. Each test's break: "the request went out anyway".
"""

from __future__ import annotations

import ipaddress
import socket
from typing import Any

import httpcore
import pytest
from matrx_utils.outbound_guard import OutboundUrlRefused

_DNS = {
    "docs.harbordentalcare.com": "151.101.65.140",
    "mcp.harbordentalcare.com": "151.101.1.140",
    "docs-internal.harbordentalcare.com": "10.20.4.17",
}


class _Wire:
    def __init__(self) -> None:
        self.sent: list[str] = []

    def getaddrinfo(self, host: Any, port: Any, *args: Any, **kwargs: Any):
        name = host.decode() if isinstance(host, bytes) else str(host)
        ip = _DNS.get(name, name)
        try:
            ipaddress.ip_address(ip)
        except ValueError as exc:
            raise socket.gaierror(socket.EAI_NONAME, "Name or service not known") from exc
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, int(port or 0)))]


@pytest.fixture
def wire(monkeypatch: pytest.MonkeyPatch) -> _Wire:
    w = _Wire()
    monkeypatch.setattr(socket, "getaddrinfo", w.getaddrinfo)

    def answer(host: str) -> httpcore.Response:
        w.sent.append(host)
        return httpcore.Response(
            200,
            headers=[(b"content-type", b"text/plain")],
            content=b"# Harbor Dental\n> Patient intake API\n",
        )

    async def apool(_self: Any, request: httpcore.Request) -> httpcore.Response:
        return answer(request.url.host.decode())

    def spool(_self: Any, request: httpcore.Request) -> httpcore.Response:
        return answer(request.url.host.decode())

    monkeypatch.setattr(httpcore.AsyncConnectionPool, "handle_async_request", apool)
    monkeypatch.setattr(httpcore.ConnectionPool, "handle_request", spool)

    import requests

    def send(_self: Any, prepared: Any, **kwargs: Any) -> Any:
        from urllib.parse import urlsplit

        w.sent.append(urlsplit(prepared.url).hostname or "")
        resp = requests.Response()
        resp.status_code = 200
        resp._content = b"\x89PNG harbor logo"
        resp.url = prepared.url
        return resp

    monkeypatch.setattr(requests.Session, "send", send)
    return w


# ── llms_txt_fetch ───────────────────────────────────────────────────────────


def _ctx() -> Any:
    from matrx_ai.tools.models import ToolContext

    # No app context in this unit: the tool's progress stream has no emitter.
    return ToolContext(call_id="call-llms-1", tool_name="llms_txt_fetch")


@pytest.mark.parametrize(
    "url",
    [
        "https://169.254.169.254/latest/meta-data",
        "https://docs-internal.harbordentalcare.com",
        "localhost:8000",
    ],
)
async def test_llms_txt_fetch_refuses_an_internal_address(wire: _Wire, url: str) -> None:
    from matrx_ai.tools.implementations.code_ingest import llms_txt_fetch

    result = await llms_txt_fetch({"url": url}, _ctx())

    assert wire.sent == []
    assert result.success is False
    assert result.error.error_type == "not_allowed"
    assert result.error.is_retryable is False
    assert "private or internal" in result.error.message


async def test_llms_txt_fetch_reads_a_public_site_pinned(wire: _Wire) -> None:
    from matrx_ai.tools.implementations.code_ingest import llms_txt_fetch

    result = await llms_txt_fetch({"url": "docs.harbordentalcare.com"}, _ctx())

    assert result.success is True
    assert result.output.parsed.title == "Harbor Dental"
    assert wire.sent == ["151.101.65.140"]


# ── media download fallback (no cloud FileManager injected) ─────────────────


@pytest.fixture
def no_file_manager(monkeypatch: pytest.MonkeyPatch) -> None:
    import matrx_ai.media.media_persistence as mp

    monkeypatch.setattr(mp, "has_ext", lambda name: False)


@pytest.mark.parametrize(
    "url",
    ["https://169.254.170.2/v2/credentials", "https://docs-internal.harbordentalcare.com/logo.png"],
)
async def test_media_download_async_refuses_an_internal_address(
    wire: _Wire, no_file_manager: None, url: str
) -> None:
    from matrx_ai.media.media_persistence import AIMediaHandler

    with pytest.raises(Exception) as caught:
        await AIMediaHandler._resolve_url_to_bytes_async(url)
    assert wire.sent == []
    assert isinstance(caught.value, OutboundUrlRefused)


@pytest.mark.parametrize(
    "url",
    ["https://169.254.170.2/v2/credentials", "https://docs-internal.harbordentalcare.com/logo.png"],
)
def test_media_download_sync_refuses_an_internal_address(
    wire: _Wire, no_file_manager: None, url: str
) -> None:
    from matrx_ai.media.media_persistence import AIMediaHandler

    with pytest.raises(Exception) as caught:
        AIMediaHandler._resolve_url_to_bytes_sync(url)
    assert wire.sent == []
    assert isinstance(caught.value, OutboundUrlRefused)


async def test_media_download_from_a_public_host_still_works(
    wire: _Wire, no_file_manager: None
) -> None:
    from matrx_ai.media.media_persistence import AIMediaHandler

    data = await AIMediaHandler._resolve_url_to_bytes_async(
        "https://docs.harbordentalcare.com/logo.png"
    )
    assert data.startswith(b"# Harbor Dental")
    assert wire.sent == ["151.101.65.140"]


# ── remote MCP client ────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "url",
    ["https://169.254.169.254/mcp", "https://docs-internal.harbordentalcare.com/mcp"],
)
async def test_remote_mcp_refuses_an_internal_server_address(wire: _Wire, url: str) -> None:
    from matrx_ai.tools.external_mcp import ExternalMCPClient

    client = ExternalMCPClient(timeout=5.0)
    payload = client._build_request("tools/list", {})
    with pytest.raises(Exception) as caught:
        await client._send(url, payload)
    assert wire.sent == []
    assert isinstance(caught.value, OutboundUrlRefused)
