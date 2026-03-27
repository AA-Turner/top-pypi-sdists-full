"""CLI integration test for tiktoken usage fallback (#1006).

Verifies the full estimation pipeline: ai_service yields estimated usage,
the REPL event handler stores it, and the DB has non-NULL token counts.
Uses a mock OpenAI server that omits streaming usage.
"""

from __future__ import annotations

import json
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

import pytest

from anteroom.config import AIConfig
from anteroom.db import init_db
from anteroom.services.ai_service import AIService


class _NoUsageMockHandler(BaseHTTPRequestHandler):
    """Mock OpenAI-compatible server that omits usage from streaming chunks."""

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
                "choices": [
                    {"index": 0, "delta": {"content": "Hello! I can help you with that."}, "finish_reason": None}
                ],
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


@pytest.fixture()
def mock_server():
    server = HTTPServer(("127.0.0.1", 0), _NoUsageMockHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}/v1"
    server.shutdown()


@pytest.fixture()
def db() -> Any:
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn
        conn.close()


class TestUsageFallbackIntegration:
    """Integration test: real HTTP mock → real AIService → verify usage event."""

    @pytest.mark.asyncio
    async def test_stream_yields_estimated_usage_when_api_omits(self, mock_server: str) -> None:
        """Connect AIService to a mock that omits usage, verify the fallback
        estimation fires and yields a usage event with estimated=True."""
        config = AIConfig(
            base_url=mock_server,
            api_key="test",
            model="test-model",
            system_prompt="You are helpful.",
        )
        service = AIService(config)

        messages = [{"role": "user", "content": "Say hello"}]
        events: list[dict[str, Any]] = []

        async for event in service.stream_chat(messages):
            events.append(event)

        # Should have token events, a usage event, and a done event
        event_types = [e["event"] for e in events]
        assert "token" in event_types, f"No token events: {event_types}"
        assert "done" in event_types, f"No done event: {event_types}"
        assert "usage" in event_types, f"No usage event — fallback did not fire: {event_types}"

        usage_event = next(e for e in events if e["event"] == "usage")
        usage = usage_event["data"]
        assert usage["prompt_tokens"] > 0, f"prompt_tokens should be > 0: {usage}"
        assert usage["completion_tokens"] > 0, f"completion_tokens should be > 0: {usage}"
        assert usage["total_tokens"] == usage["prompt_tokens"] + usage["completion_tokens"]
        assert usage["model"] == "test-model"
        assert usage["estimated"] is True

    @pytest.mark.asyncio
    async def test_full_pipeline_stores_estimated_tokens(self, mock_server: str, db: Any) -> None:
        """Full pipeline: AIService → event handler → storage.

        Simulates the REPL event handler logic: capture usage event,
        create message, update_message_usage, merge metadata.
        """
        from anteroom.services.storage import (
            create_conversation,
            create_message,
            merge_message_metadata,
            update_message_usage,
        )

        config = AIConfig(
            base_url=mock_server,
            api_key="test",
            model="test-model",
            system_prompt="You are helpful.",
        )
        service = AIService(config)
        messages = [{"role": "user", "content": "What is 2+2?"}]

        # Collect events (simulating the REPL event loop)
        pending_usage = None
        response_content = ""

        async for event in service.stream_chat(messages):
            if event["event"] == "token":
                response_content += event["data"]["content"]
            elif event["event"] == "usage":
                pending_usage = event["data"]

        assert pending_usage is not None, "No usage event received"
        assert response_content, "No response content"

        # Simulate REPL storage path
        conv = create_conversation(db, "test")
        msg = create_message(db, conv["id"], "assistant", response_content)
        update_message_usage(
            db,
            msg["id"],
            pending_usage.get("prompt_tokens", 0),
            pending_usage.get("completion_tokens", 0),
            pending_usage.get("total_tokens", 0),
            pending_usage.get("model", ""),
        )
        if pending_usage.get("estimated"):
            merge_message_metadata(db, msg["id"], {"usage_estimated": True})

        # Verify DB state
        row = db.execute_fetchone(
            "SELECT prompt_tokens, completion_tokens, total_tokens, model, metadata FROM messages WHERE id = ?",
            (msg["id"],),
        )
        assert row["prompt_tokens"] > 0
        assert row["completion_tokens"] > 0
        assert row["total_tokens"] > 0
        assert row["model"] == "test-model"
        meta = json.loads(row["metadata"])
        assert meta["usage_estimated"] is True
