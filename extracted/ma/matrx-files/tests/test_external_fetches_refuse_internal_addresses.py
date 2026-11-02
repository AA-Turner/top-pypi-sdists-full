"""matrx-files never downloads a person- or model-supplied URL from inside our network.

Use case: a patient-intake agent at Harbor Dental is handed "the referral PDF"
and "the x-ray image" as links. The media resolver, the PDF handler and the
LLM-output writer each fetch genuinely external URLs themselves (our own
storage URLs are read through cloud credentials, never over HTTP). A link at
the metadata service or a VPC host must be refused before a byte is fetched.

DNS and the wire are stubbed beneath httpx (and ``requests`` for the old sync
download); the guarded clients stay real.
"""

from __future__ import annotations

import ipaddress
import socket
from typing import Any

import httpcore
import pytest

_DNS = {
    "referrals.harbordentalcare.com": "151.101.65.140",
    "pacs.harbordentalcare.com": "10.20.4.17",
}
_PDF = b"%PDF-1.7 referral for Marisol Ortega"


class _Wire:
    def __init__(self) -> None:
        self.sent: list[str] = []


@pytest.fixture
def wire(monkeypatch: pytest.MonkeyPatch) -> _Wire:
    w = _Wire()

    def getaddrinfo(host: Any, port: Any, *args: Any, **kwargs: Any):
        name = host.decode() if isinstance(host, bytes) else str(host)
        ip = _DNS.get(name, name)
        try:
            ipaddress.ip_address(ip)
        except ValueError as exc:
            raise socket.gaierror(socket.EAI_NONAME, "Name or service not known") from exc
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, int(port or 0)))]

    monkeypatch.setattr(socket, "getaddrinfo", getaddrinfo)

    def answer(request: httpcore.Request) -> httpcore.Response:
        w.sent.append(request.url.host.decode())
        return httpcore.Response(200, headers=[(b"content-type", b"application/pdf")], content=_PDF)

    async def apool(_self: Any, request: httpcore.Request) -> httpcore.Response:
        return answer(request)

    def spool(_self: Any, request: httpcore.Request) -> httpcore.Response:
        return answer(request)

    monkeypatch.setattr(httpcore.AsyncConnectionPool, "handle_async_request", apool)
    monkeypatch.setattr(httpcore.ConnectionPool, "handle_request", spool)

    import requests

    def send(_self: Any, prepared: Any, **kwargs: Any) -> Any:
        from urllib.parse import urlsplit

        w.sent.append(urlsplit(prepared.url).hostname or "")
        resp = requests.Response()
        resp.status_code = 200
        resp._content = _PDF
        resp.url = prepared.url
        return resp

    monkeypatch.setattr(requests.Session, "send", send)
    return w


INTERNAL = [
    "https://169.254.169.254/latest/meta-data/referral.pdf",
    "https://pacs.harbordentalcare.com/studies/8841/referral.pdf",
]


# ── MediaRef resolver: the one external fetch every media consumer shares ───


@pytest.mark.parametrize("url", INTERNAL)
async def test_media_resolver_refuses_an_internal_url_and_says_why(wire: _Wire, url: str) -> None:
    from matrx_files.cloud_sync._media_resolution import _fetch_external_url_into_ref
    from matrx_files.cloud_sync.media_ref import MediaRef

    ref = MediaRef(url=url)
    await _fetch_external_url_into_ref(ref)

    assert wire.sent == []
    assert ref.base64_data is None
    assert ref.is_resolved is True
    assert "private or internal" in (ref.resolver_error or "")


async def test_media_resolver_fetches_a_public_url_pinned(wire: _Wire) -> None:
    import base64

    from matrx_files.cloud_sync._media_resolution import _fetch_external_url_into_ref
    from matrx_files.cloud_sync.media_ref import MediaRef

    ref = MediaRef(url="https://referrals.harbordentalcare.com/2026/oct/referral-public.pdf")
    await _fetch_external_url_into_ref(ref)

    assert ref.resolver_error is None
    assert base64.b64decode(ref.base64_data or "") == _PDF
    assert wire.sent == ["151.101.65.140"]


# ── PDF handler ──────────────────────────────────────────────────────────────


@pytest.mark.parametrize("url", INTERNAL)
async def test_pdf_download_refuses_an_internal_url(wire: _Wire, url: str) -> None:
    from matrx_files.specific_handlers.pdf.handler import PDFHandler

    assert await PDFHandler(app_name="harbor_intake").fetch_remote(url) is None
    assert wire.sent == []


@pytest.mark.parametrize("url", INTERNAL)
async def test_pdf_file_object_refuses_an_internal_url(wire: _Wire, url: str) -> None:
    from matrx_files.specific_handlers.pdf.handler import PDFHandler

    handler = PDFHandler(app_name="harbor_intake")
    got = await handler.fetch_remote({"url": url, "details": {"extension": "pdf"}})
    assert got is None
    assert wire.sent == []


# ── writing what an LLM returned as a URL ────────────────────────────────────


class _Router:
    def __init__(self) -> None:
        self.written: list[tuple[str, bytes]] = []

    def write(self, uri: str, raw: bytes, **kwargs: Any) -> bool:
        self.written.append((uri, raw))
        return True

    async def write_async(self, uri: str, raw: bytes, **kwargs: Any) -> bool:
        self.written.append((uri, raw))
        return True


@pytest.mark.parametrize("url", INTERNAL)
async def test_push_from_llm_async_refuses_an_internal_url(wire: _Wire, url: str) -> None:
    from matrx_files.backends.llm_helpers import push_from_llm_async
    from matrx_utils.outbound_guard import OutboundUrlRefused

    router = _Router()
    with pytest.raises(Exception) as caught:
        await push_from_llm_async(url, "s3://harbor/referrals/r.pdf", router, source_format="url")
    assert wire.sent == []
    assert router.written == []
    assert isinstance(caught.value, OutboundUrlRefused)


@pytest.mark.parametrize("url", INTERNAL)
def test_push_from_llm_sync_refuses_an_internal_url(wire: _Wire, url: str) -> None:
    from matrx_files.backends.llm_helpers import push_from_llm

    router = _Router()
    with pytest.raises(ValueError, match="private or internal"):
        push_from_llm(url, "s3://harbor/referrals/r.pdf", router, source_format="url")
    assert wire.sent == []
    assert router.written == []


def test_push_from_llm_sync_downloads_a_public_url_pinned(wire: _Wire) -> None:
    from matrx_files.backends.llm_helpers import push_from_llm

    router = _Router()
    push_from_llm(
        "https://referrals.harbordentalcare.com/2026/oct/referral-public.pdf",
        "s3://harbor/referrals/r.pdf",
        router,
        source_format="url",
    )
    assert router.written == [("s3://harbor/referrals/r.pdf", _PDF)]
    assert wire.sent == ["151.101.65.140"]
