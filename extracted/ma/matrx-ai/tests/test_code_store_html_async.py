from __future__ import annotations

import asyncio

import httpx
import pytest

from matrx_ai.tools.implementations import code as code_tools
from matrx_ai.tools.models import ToolContext


@pytest.mark.asyncio
async def test_code_store_html_does_not_block_the_event_loop(monkeypatch) -> None:
    entered = asyncio.Event()
    release = asyncio.Event()

    class FakeAsyncClient:
        def __init__(self, **kwargs) -> None:
            assert kwargs["timeout"] == 15

        async def __aenter__(self):
            return self

        async def __aexit__(self, *_args) -> None:
            return None

        async def post(self, url: str, *, json: dict[str, str]) -> httpx.Response:
            assert url.endswith("/store-html")
            assert json == {"html": "<h1>hello</h1>"}
            entered.set()
            await release.wait()
            return httpx.Response(
                200,
                json={"id": "stored-1"},
                request=httpx.Request("POST", url),
            )

    monkeypatch.setattr(httpx, "AsyncClient", FakeAsyncClient)

    task = asyncio.create_task(
        code_tools.code_store_html(
            {"html_input": "<h1>hello</h1>"},
            ToolContext(call_id="store-html-test", tool_name="code_store_html"),
        )
    )
    await asyncio.wait_for(entered.wait(), timeout=0.1)
    assert not task.done()
    release.set()

    result = await asyncio.wait_for(task, timeout=0.1)
    assert result.success is True
    assert result.output == {"id": "stored-1"}


@pytest.mark.asyncio
async def test_code_store_html_returns_http_failures(monkeypatch) -> None:
    class FakeAsyncClient:
        def __init__(self, **_kwargs) -> None:
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *_args) -> None:
            return None

        async def post(self, url: str, *, json: dict[str, str]) -> httpx.Response:
            raise httpx.ConnectError("unreachable", request=httpx.Request("POST", url))

    monkeypatch.setattr(httpx, "AsyncClient", FakeAsyncClient)
    result = await code_tools.code_store_html(
        {"html_input": "<h1>hello</h1>"},
        ToolContext(call_id="store-html-failure", tool_name="code_store_html"),
    )

    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "execution"
