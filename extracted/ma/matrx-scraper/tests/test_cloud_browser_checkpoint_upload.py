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
