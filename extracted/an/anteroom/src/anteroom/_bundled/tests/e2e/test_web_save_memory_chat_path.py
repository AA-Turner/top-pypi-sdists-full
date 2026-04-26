"""E2E tests for the save_memory tool over the actual web chat path (#217).

These tests address the senior-review gap from PR #1452: the original
``test_ui_save_memory.py`` posted candidates directly to
``/api/memory/candidates`` and never exercised ``routers/chat.py`` — the
exact interface code modified to thread ``config`` / ``user_id`` through
``_extra_context`` for the ``save_memory`` handler.

The tests below follow the ``test_mcp_approval.py`` pattern:

1. Boot a real server with ``approval_mode="ask_for_writes"`` and expose the
   FastAPI app object so the test can poll ``app.state.pending_approvals``.
2. Stub ``AIService.stream_chat`` to emit a single ``save_memory`` tool call.
3. Drive the conversation via ``POST /api/conversations/{id}/chat``.
4. Respond to the approval prompt over the real approval endpoint.
5. Verify: the SSE ``tool_call_end`` event reports success, AND the memory
   candidate was persisted via the governed promotion pipeline.

This exercises the full chat code path: the chat router assembles its
``_extra_context`` via ``build_tool_extra_context_web`` (including the
``config`` + ``user_id`` keys added for #217), ``call_tool`` translates
those unprefixed keys to the underscore-prefixed kwargs ``save_memory``
consumes, and the promotion service lands the candidate with agent
lineage tied to the request's session user.
"""

from __future__ import annotations

import socket
import threading
import time
from pathlib import Path
from typing import Any, Generator
from unittest.mock import patch

import httpx
import pytest
import uvicorn

from anteroom.config import (
    AIConfig,
    AppConfig,
    AppSettings,
    EmbeddingsConfig,
    MemoryConfig,
    MemoryPromotionConfig,
    SafetyConfig,
)
from anteroom.services import storage
from tests.e2e.conftest import (
    _NoopRateLimiter,
    mock_tool_call_stream,
    parse_sse_events,
)

pytestmark = [pytest.mark.e2e]


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class _Server:
    """Minimal uvicorn-in-thread harness matching the conftest pattern."""

    def __init__(self, app: Any, host: str, port: int) -> None:
        config = uvicorn.Config(app, host=host, port=port, log_level="warning")
        self._server = uvicorn.Server(config)
        self._thread = threading.Thread(target=self._server.run, daemon=True)

    def start(self) -> None:
        self._thread.start()
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            if self._server.started:
                return
            time.sleep(0.05)
        raise RuntimeError("Server did not start in time")

    def stop(self) -> None:
        self._server.should_exit = True
        self._thread.join(timeout=5)


@pytest.fixture(scope="module")
def save_memory_app_server(
    tmp_path_factory: pytest.TempPathFactory,
) -> Generator[tuple[str, Path, Any], None, None]:
    """Boot a self-contained server with ask_for_writes approval mode.

    Yields (base_url, data_dir, app). The ``app`` is the running FastAPI
    app so tests can poll ``app.state.pending_approvals`` directly.
    """
    data_dir = tmp_path_factory.mktemp("anteroom_save_memory_e2e")
    port = _free_port()

    config = AppConfig(
        ai=AIConfig(
            base_url="http://localhost:1/v1",
            api_key="test-key-not-real",
            model="gpt-4",
        ),
        app=AppSettings(host="127.0.0.1", port=port, data_dir=data_dir, tls=False),
        embeddings=EmbeddingsConfig(enabled=False),
        safety=SafetyConfig(approval_mode="ask_for_writes"),
    )

    from anteroom.app import create_app

    with patch("anteroom.app.RateLimitMiddleware", _NoopRateLimiter):
        app = create_app(config)

    server = _Server(app, "127.0.0.1", port)
    server.start()
    base_url = f"http://127.0.0.1:{port}"
    yield base_url, data_dir, app
    server.stop()


@pytest.fixture(scope="module")
def save_memory_cookies(save_memory_app_server: tuple[str, Path, Any]) -> dict[str, str]:
    base_url = save_memory_app_server[0]
    resp = httpx.get(f"{base_url}/", follow_redirects=True)
    resp.raise_for_status()
    return {cookie.name: cookie.value for cookie in resp.cookies.jar}


@pytest.fixture()
def save_memory_client(
    save_memory_app_server: tuple[str, Path, Any],
    save_memory_cookies: dict[str, str],
) -> Generator[httpx.Client, None, None]:
    base_url = save_memory_app_server[0]
    session_token = save_memory_cookies.get("anteroom_session", "")
    csrf_token = save_memory_cookies.get("anteroom_csrf", "")
    with httpx.Client(
        base_url=base_url,
        cookies={"anteroom_session": session_token, "anteroom_csrf": csrf_token},
        headers={"X-CSRF-Token": csrf_token},
        timeout=30,
    ) as client:
        yield client


@pytest.fixture()
def save_memory_conversation_id(save_memory_client: httpx.Client) -> str:
    resp = save_memory_client.post("/api/conversations", json={"title": "save_memory E2E"})
    resp.raise_for_status()
    return resp.json()["id"]


def _poll_pending_approval(app: Any, timeout: float = 15.0) -> str | None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        pending = getattr(app.state, "pending_approvals", {})
        if pending:
            return list(pending.keys())[0]
        time.sleep(0.1)
    return None


def _do_chat(
    client: httpx.Client,
    conversation_id: str,
    message: str,
    stream_fn: Any,
    result: dict,
) -> None:
    try:
        with patch("anteroom.services.ai_service.AIService.stream_chat", side_effect=stream_fn):
            resp = client.post(
                f"/api/conversations/{conversation_id}/chat",
                json={"message": message},
                headers={"Content-Type": "application/json", "Accept": "text/event-stream"},
            )
        result["response"] = resp
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {e}"


def _respond_to_approval(
    client: httpx.Client,
    approval_id: str,
    *,
    approved: bool,
    scope: str = "once",
) -> httpx.Response:
    return client.post(
        f"/api/approvals/{approval_id}/respond",
        json={"approved": approved, "scope": scope},
        headers={"Content-Type": "application/json"},
    )


# ---------------------------------------------------------------------------
# The chat-path round trip — the senior-review requirement.
# ---------------------------------------------------------------------------


class TestSaveMemoryChatPath:
    def test_explicit_memory_utterance_bypasses_invoke_skill(
        self,
        save_memory_client: httpx.Client,
        save_memory_conversation_id: str,
        save_memory_app_server: tuple[str, Path, Any],
    ) -> None:
        _, _, app = save_memory_app_server
        chat_result: dict = {}
        chat_thread = threading.Thread(
            target=_do_chat,
            args=(
                save_memory_client,
                save_memory_conversation_id,
                "save my name Troy Larson as a memorry",
                lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("AI should not be called")),
                chat_result,
            ),
            daemon=True,
        )
        chat_thread.start()

        approval_id = _poll_pending_approval(app)
        assert approval_id is not None
        resp = _respond_to_approval(save_memory_client, approval_id, approved=True, scope="once")
        assert resp.status_code == 200

        chat_thread.join(timeout=30)
        assert "response" in chat_result, f"Chat failed: {chat_result}"
        assert chat_result["response"].status_code == 200

        events = parse_sse_events(chat_result["response"])
        starts = [e for e in events if e["event"] == "tool_call_start"]
        assert [e["data"].get("tool_name") for e in starts] == ["save_memory"]
        assert all(e["data"].get("tool_name") != "invoke_skill" for e in starts)
        end_events = [e for e in events if e["event"] == "tool_call_end"]
        assert end_events
        assert end_events[0]["data"]["output"]["memory_status"] == "candidate"
        token_text = "".join(e["data"].get("content", "") for e in events if e["event"] == "token")
        assert "memory candidate" in token_text
        assert "not active or recallable until approved" in token_text
        assert "may" not in token_text.lower()
        assistant = [
            m for m in storage.list_messages(app.state.db, save_memory_conversation_id) if m["role"] == "assistant"
        ][0]
        assert assistant["metadata"]["memory_save"]["memory_status"] == "candidate"
        assert assistant["metadata"]["memory_save"]["recallable"] is False
        assert assistant["tool_calls"][0]["output"]["memory_status"] == "candidate"

    def test_explicit_memory_utterance_reports_active_when_auto_approved(
        self,
        save_memory_client: httpx.Client,
        save_memory_conversation_id: str,
        save_memory_app_server: tuple[str, Path, Any],
    ) -> None:
        _, _, app = save_memory_app_server
        original_memory_config = app.state.config.memory
        app.state.config.memory = MemoryConfig(promotion=MemoryPromotionConfig(local_auto_approve=True))
        chat_result: dict = {}
        try:
            chat_thread = threading.Thread(
                target=_do_chat,
                args=(
                    save_memory_client,
                    save_memory_conversation_id,
                    "save my name Active Larson as a memorry",
                    lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("AI should not be called")),
                    chat_result,
                ),
                daemon=True,
            )
            chat_thread.start()

            approval_id = _poll_pending_approval(app)
            assert approval_id is not None
            resp = _respond_to_approval(save_memory_client, approval_id, approved=True, scope="once")
            assert resp.status_code == 200

            chat_thread.join(timeout=30)
        finally:
            app.state.config.memory = original_memory_config

        assert "response" in chat_result, f"Chat failed: {chat_result}"
        assert chat_result["response"].status_code == 200
        events = parse_sse_events(chat_result["response"])
        end_events = [e for e in events if e["event"] == "tool_call_end"]
        assert end_events
        assert end_events[0]["data"]["output"]["memory_status"] == "active"
        token_text = "".join(e["data"].get("content", "") for e in events if e["event"] == "token")
        assert "active memory" in token_text
        assert "eligible for recall" in token_text
        assert "may" not in token_text.lower()
        assistant_messages = [
            m for m in storage.list_messages(app.state.db, save_memory_conversation_id) if m["role"] == "assistant"
        ]
        assistant = assistant_messages[-1]
        assert assistant["metadata"]["memory_save"]["memory_status"] == "active"
        assert assistant["metadata"]["memory_save"]["recallable"] is True
        assert assistant["tool_calls"][0]["output"]["memory_status"] == "active"

    def test_stubbed_llm_tool_call_approved_persists_candidate(
        self,
        save_memory_client: httpx.Client,
        save_memory_conversation_id: str,
        save_memory_app_server: tuple[str, Path, Any],
    ) -> None:
        """Full web chat path: stubbed AI -> save_memory tool call ->
        approval prompt -> user approves -> candidate in promotion queue.
        """
        _, _, app = save_memory_app_server

        stream_fn = mock_tool_call_stream(
            tool_name="save_memory",
            arguments={
                "content": "prefers four-space indent",
                "category": "preference",
                "scope": "user",
            },
            tool_call_id="call_save_mem_ok",
        )

        chat_result: dict = {}
        chat_thread = threading.Thread(
            target=_do_chat,
            args=(
                save_memory_client,
                save_memory_conversation_id,
                "Remember this",
                stream_fn,
                chat_result,
            ),
            daemon=True,
        )
        chat_thread.start()

        # WRITE-tier save_memory must trigger an approval prompt under
        # ask_for_writes. This is the heart of the chat-path assertion.
        approval_id = _poll_pending_approval(app)
        assert approval_id is not None, (
            "save_memory did not produce an approval prompt via the chat endpoint — "
            "either the tool is not registered in the running app, or the WRITE-tier "
            "gate was skipped."
        )

        resp = _respond_to_approval(save_memory_client, approval_id, approved=True, scope="once")
        assert resp.status_code == 200
        assert resp.json()["approved"] is True

        chat_thread.join(timeout=30)
        assert "response" in chat_result, f"Chat failed: {chat_result}"
        assert chat_result["response"].status_code == 200

        # Evidence-from-SSE: the tool_call for save_memory completed as success.
        # tool_call_end only carries ``id`` (not ``tool_name``) in the event
        # payload, so correlate the end event to the start event by id.
        events = parse_sse_events(chat_result["response"])
        save_memory_starts = [
            e for e in events if e["event"] == "tool_call_start" and e["data"].get("tool_name") == "save_memory"
        ]
        assert save_memory_starts, f"No save_memory tool_call_start event: {events}"
        save_memory_call_id = save_memory_starts[0]["data"]["id"]

        end_events = [e for e in events if e["event"] == "tool_call_end" and e["data"].get("id") == save_memory_call_id]
        assert end_events, f"No tool_call_end for save_memory id={save_memory_call_id}: {events}"
        assert end_events[0]["data"]["status"] == "success"
        tool_output = end_events[0]["data"].get("output", {})
        assert tool_output.get("memory_status") == "candidate"
        assert tool_output.get("fqn", "").startswith("@user/memory/")

        # Evidence-from-API: the candidate landed in the governed promotion queue
        # with proposer="agent" lineage stamped by the web session identity.
        candidates = save_memory_client.get("/api/memory/candidates").json()
        matching = [c for c in candidates if c.get("content") == "prefers four-space indent"]
        assert matching, f"Candidate not found in review queue: {[c.get('content') for c in candidates]}"
        lineage = matching[0].get("metadata", {}).get("lineage", [])
        assert lineage and lineage[0]["event"] == "proposed"
        assert lineage[0]["actor"] == "agent"

    def test_stubbed_llm_tool_call_denied_blocks_candidate(
        self,
        save_memory_client: httpx.Client,
        save_memory_conversation_id: str,
        save_memory_app_server: tuple[str, Path, Any],
    ) -> None:
        """Denied approval means nothing lands in the promotion queue."""
        _, _, app = save_memory_app_server

        stream_fn = mock_tool_call_stream(
            tool_name="save_memory",
            arguments={
                "content": "this should not be saved",
                "category": "preference",
                "scope": "user",
            },
            tool_call_id="call_save_mem_deny",
        )

        chat_result: dict = {}
        chat_thread = threading.Thread(
            target=_do_chat,
            args=(
                save_memory_client,
                save_memory_conversation_id,
                "Try to remember",
                stream_fn,
                chat_result,
            ),
            daemon=True,
        )
        chat_thread.start()

        approval_id = _poll_pending_approval(app)
        assert approval_id is not None

        resp = _respond_to_approval(save_memory_client, approval_id, approved=False, scope="once")
        assert resp.status_code == 200
        assert resp.json()["approved"] is False

        chat_thread.join(timeout=30)
        assert "response" in chat_result

        events = parse_sse_events(chat_result["response"])
        save_memory_starts = [
            e for e in events if e["event"] == "tool_call_start" and e["data"].get("tool_name") == "save_memory"
        ]
        assert save_memory_starts
        save_memory_call_id = save_memory_starts[0]["data"]["id"]

        end_events = [e for e in events if e["event"] == "tool_call_end" and e["data"].get("id") == save_memory_call_id]
        assert end_events
        output = end_events[0]["data"].get("output", {})
        assert "error" in output or "denied" in str(output).lower()

        # Governed pipeline must not have stored the denied candidate.
        candidates = save_memory_client.get("/api/memory/candidates").json()
        assert not any(c.get("content") == "this should not be saved" for c in candidates)
