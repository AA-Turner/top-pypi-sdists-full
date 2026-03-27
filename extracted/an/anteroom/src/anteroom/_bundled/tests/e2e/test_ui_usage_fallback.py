"""Playwright browser E2E test for usage fallback (#1006).

Starts a real Anteroom server backed by a mock OpenAI server that omits
streaming usage. Drives the browser to send a message, waits for the
assistant response to render, then verifies GET /api/usage returns
non-zero estimated tokens.
"""

from __future__ import annotations

import json
import socket
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Generator
from unittest.mock import patch

import httpx
import pytest

HAS_PLAYWRIGHT = True
try:
    from playwright.sync_api import Page
except ImportError:
    HAS_PLAYWRIGHT = False

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="playwright not installed"),
]


class _NoUsageMockAI(BaseHTTPRequestHandler):
    """Mock OpenAI server that returns content but omits usage."""

    def do_POST(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        chunks = [
            {
                "id": "chatcmpl-test",
                "object": "chat.completion.chunk",
                "model": "test-model",
                "choices": [{"index": 0, "delta": {"role": "assistant", "content": ""}, "finish_reason": None}],
            },
            {
                "id": "chatcmpl-test",
                "object": "chat.completion.chunk",
                "model": "test-model",
                "choices": [{"index": 0, "delta": {"content": "The answer is 4."}, "finish_reason": None}],
            },
            {
                "id": "chatcmpl-test",
                "object": "chat.completion.chunk",
                "model": "test-model",
                "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
            },
        ]
        for chunk in chunks:
            self.wfile.write(f"data: {json.dumps(chunk)}\n\n".encode())
            self.wfile.flush()
        self.wfile.write(b"data: [DONE]\n\n")
        self.wfile.flush()

    def log_message(self, format: str, *args: object) -> None:
        pass


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def usage_test_server() -> Generator[str, None, None]:
    """Start a real Anteroom server backed by a no-usage mock AI."""
    from anteroom.app import create_app
    from anteroom.config import AIConfig, AppConfig, AppSettings, EmbeddingsConfig

    mock = HTTPServer(("127.0.0.1", 0), _NoUsageMockAI)
    mock_port = mock.server_address[1]
    threading.Thread(target=mock.serve_forever, daemon=True).start()

    data_dir = Path(tempfile.mkdtemp())
    port = _free_port()

    config = AppConfig(
        ai=AIConfig(
            base_url=f"http://127.0.0.1:{mock_port}/v1",
            api_key="test",
            model="test-model",
        ),
        app=AppSettings(host="127.0.0.1", port=port, data_dir=data_dir, tls=False),
        embeddings=EmbeddingsConfig(enabled=False),
    )

    try:
        from tests.e2e.conftest import _NoopRateLimiter
    except ImportError:

        class _NoopRateLimiter:  # type: ignore[no-redef]
            def __init__(self, app: Any, **kw: Any) -> None:
                self.app = app

            async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
                await self.app(scope, receive, send)

    with patch("anteroom.app.RateLimitMiddleware", _NoopRateLimiter):
        app = create_app(config)

    import uvicorn

    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    base_url = f"http://127.0.0.1:{port}"
    for _ in range(30):
        try:
            httpx.get(f"{base_url}/", timeout=1)
            break
        except httpx.ConnectError:
            time.sleep(0.2)

    yield base_url

    server.should_exit = True
    mock.shutdown()


class TestUsageFallbackBrowser:
    """Playwright browser test: type a message, wait for the assistant
    response to render in the DOM, then verify usage API has non-zero
    estimated tokens."""

    def test_chat_produces_estimated_usage(self, page: Page, usage_test_server: str) -> None:
        """Drive a conversation through the browser and verify estimated usage."""
        base_url = usage_test_server

        # Navigate and wait for app to load
        page.goto(base_url)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_selector("#btn-send", timeout=10000)

        # Click "New Chat" to start fresh
        new_chat_btn = page.locator("button:has-text('New Chat')")
        if new_chat_btn.count() > 0:
            new_chat_btn.click()
            page.wait_for_timeout(500)

        # Type a message and send
        input_field = page.locator("#message-input")
        input_field.fill("What is 2+2?")
        page.click("#btn-send")

        # Wait for assistant response to appear in the DOM
        # The mock returns "The answer is 4." — wait for it to render
        page.wait_for_selector(".message.assistant", timeout=15000)
        page.wait_for_timeout(1000)  # Allow storage write to complete

        # Verify assistant content rendered
        assistant_msg = page.locator(".message.assistant").last
        content = assistant_msg.inner_text()
        assert "answer" in content.lower() or "4" in content, f"Expected assistant response, got: {content}"

        # Check usage API via fetch from the browser context
        usage_data = page.evaluate(
            """async () => {
                const resp = await fetch('/api/usage');
                return resp.json();
            }"""
        )
        all_time = usage_data.get("All time", {})
        assert all_time.get("total_tokens", 0) > 0, (
            f"Expected non-zero total_tokens from tiktoken fallback. Mock AI omits usage. Got: {usage_data}"
        )
