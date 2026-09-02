"""A capture may only report ``uploaded=True`` when bytes really landed.

Until 2026-08-23 this branch discarded the PNG and hard-coded ``uploaded=True``.
A durability claim nobody can fall back on is worse than no claim at all: the
control plane records it, ``browser.capture`` reads it, and a person later
opens a screenshot that was never stored.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import httpx
import pytest

from matrx_scraper.cloud_browser.worker import models as M
from matrx_scraper.cloud_browser.worker import runtime


class _CapturingClient:
    """Records the body actually PUT so a silent discard cannot pass."""

    sent: list[bytes] = []

    def __init__(self, response: httpx.Response, **_kwargs) -> None:
        self._response = response

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args) -> None:
        return None

    async def put(self, _url, *, headers=None, content=None) -> httpx.Response:  # noqa: ANN001
        del headers
        type(self).sent.append(content)
        return self._response


def _target() -> M.PresignedUpload:
    return M.PresignedUpload(
        method="PUT",
        url="https://capture-bucket.s3.amazonaws.com/shot.png?X-Amz-Signature=secret",
        headers={"Content-Type": "image/png"},
        expires_at=datetime.now(UTC) + timedelta(minutes=5),
    )


@pytest.mark.asyncio
async def test_presigned_upload_sends_the_bytes_and_reports_success(monkeypatch) -> None:
    _CapturingClient.sent = []
    ok = httpx.Response(200, request=httpx.Request("PUT", "https://capture-bucket/shot.png"))
    monkeypatch.setattr(
        runtime.httpx, "AsyncClient", lambda **kw: _CapturingClient(ok, **kw)
    )

    uploaded = await runtime._upload_presigned_bytes(_target(), b"PNGBYTES", what="capture")

    assert uploaded is True
    assert _CapturingClient.sent == [b"PNGBYTES"], "the payload was never transmitted"


@pytest.mark.asyncio
async def test_a_rejected_upload_is_never_reported_as_uploaded(monkeypatch, caplog) -> None:
    _CapturingClient.sent = []
    url = "https://capture-bucket.s3.amazonaws.com/shot.png?X-Amz-Signature=never-log-me"
    rejected = httpx.Response(
        403,
        request=httpx.Request("PUT", url),
        headers={"x-amz-request-id": "safe-request-id"},
        content=b"<Error><Code>AccessDenied</Code></Error>",
    )
    monkeypatch.setattr(
        runtime.httpx, "AsyncClient", lambda **kw: _CapturingClient(rejected, **kw)
    )

    with caplog.at_level("ERROR"):
        uploaded = await runtime._upload_presigned_bytes(_target(), b"PNGBYTES", what="capture")

    assert uploaded is False
    assert "AccessDenied" in caplog.text
    assert "never-log-me" not in caplog.text, "a presigned signature reached the log"


@pytest.mark.asyncio
async def test_transport_failure_reports_only_the_exception_class(monkeypatch, caplog) -> None:
    class _Boom:
        def __init__(self, **_kwargs) -> None:
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *_args) -> None:
            return None

        async def put(self, url, **_kwargs):  # noqa: ANN001
            raise httpx.ConnectError(f"failed connecting to {url}")

    monkeypatch.setattr(runtime.httpx, "AsyncClient", lambda **kw: _Boom(**kw))

    with caplog.at_level("ERROR"):
        uploaded = await runtime._upload_presigned_bytes(_target(), b"x", what="capture")

    assert uploaded is False
    assert "ConnectError" in caplog.text
    assert "X-Amz-Signature" not in caplog.text
