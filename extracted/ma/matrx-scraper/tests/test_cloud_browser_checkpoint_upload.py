from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta

import httpx
import pytest

from matrx_scraper.cloud_browser.worker import models as M
from matrx_scraper.cloud_browser.worker import runtime


class _FakeAsyncClient:
    def __init__(self, response: httpx.Response, **_kwargs) -> None:
        self._response = response

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args) -> None:
        return None

    async def put(self, *_args, **_kwargs) -> httpx.Response:
        return self._response


@pytest.mark.asyncio
async def test_rejected_checkpoint_upload_logs_s3_facts_without_presigned_query(
    monkeypatch, caplog
) -> None:
    secret_marker = "must-never-reach-logs"
    url = (
        "https://checkpoint-bucket.s3.amazonaws.com/profile/archive.bin"
        f"?X-Amz-Credential={secret_marker}&X-Amz-Signature={secret_marker}"
    )
    request = httpx.Request("PUT", url)
    response = httpx.Response(
        400,
        request=request,
        headers={"x-amz-request-id": "safe-request-id"},
        content=(
            b"<Error><Code>InvalidRequest</Code>"
            b"<Message>Signature Version 4 is required.</Message></Error>"
        ),
    )
    monkeypatch.setattr(
        runtime.httpx,
        "AsyncClient",
        lambda **kwargs: _FakeAsyncClient(response, **kwargs),
    )
    target = M.PresignedUpload(
        method="PUT",
        url=url,
        expires_at=datetime.now(UTC) + timedelta(minutes=5),
    )

    with caplog.at_level(logging.ERROR, logger=runtime.__name__):
        uploaded = await runtime._upload_checkpoint_ciphertext(target, b"ciphertext")

    assert uploaded is False
    assert "status=400" in caplog.text
    assert "code=InvalidRequest" in caplog.text
    assert "request_id=safe-request-id" in caplog.text
    assert secret_marker not in caplog.text
    assert "X-Amz-" not in caplog.text


@pytest.mark.asyncio
async def test_streaming_checkpoint_upload_really_reaches_a_real_httpx_async_client(
    tmp_path, caplog
) -> None:
    """The streaming save must work through a REAL ``httpx.AsyncClient``.

    This guard exists because the previous test in this file replaces
    ``httpx.AsyncClient`` with a fake whose ``put`` accepts anything. Under that
    fake, a body httpx itself refuses looks perfectly healthy. Production shipped
    exactly that: ``_upload_checkpoint_file`` handed a plain (sync) generator to
    an ``AsyncClient``, httpx classified the request as sync and raised
    ``RuntimeError: Attempted to send an sync request with an AsyncClient
    instance``, so 100% of checkpoint uploads failed and every browser stop
    answered HTTP 500 ``checkpoint_failed``.

    ``MockTransport`` replaces only the network, never the client, so the whole
    request-construction path — the part that rejected the sync body — runs for
    real. Run this against the pre-fix code and it fails.
    """
    payload = b"x" * 5000
    archive = tmp_path / "profile.tar"
    archive.write_bytes(payload)

    seen: dict[str, object] = {}

    def _handle(request: httpx.Request) -> httpx.Response:
        seen["body"] = request.read()
        seen["content_length"] = request.headers.get("content-length")
        return httpx.Response(200, request=request)

    transport = httpx.MockTransport(_handle)
    real_async_client = httpx.AsyncClient
    # Keep the real client; swap only its transport.
    original_init = real_async_client.__init__

    def _init(self, *args, **kwargs):  # noqa: ANN001, ANN202
        kwargs["transport"] = transport
        original_init(self, *args, **kwargs)

    target = M.PresignedUpload(
        method="PUT",
        url="https://checkpoint-bucket.s3.amazonaws.com/profile/archive.bin",
        expires_at=datetime.now(UTC) + timedelta(minutes=5),
    )

    real_async_client.__init__ = _init  # type: ignore[method-assign]
    try:
        with caplog.at_level(logging.ERROR, logger=runtime.__name__):
            uploaded = await runtime._upload_checkpoint_file(
                target, str(archive), len(payload)
            )
    finally:
        real_async_client.__init__ = original_init  # type: ignore[method-assign]

    assert uploaded is True, f"streaming checkpoint upload failed; logs: {caplog.text}"
    assert seen["body"] == payload
    assert seen["content_length"] == str(len(payload))
