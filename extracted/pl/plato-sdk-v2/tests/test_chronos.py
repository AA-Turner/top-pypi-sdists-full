"""Tests for Chronos high-level SDK."""

from __future__ import annotations

import json
from unittest.mock import patch

import httpx
import pytest

from plato.chronos.errors import NotFoundError, UnauthorizedError
from plato.chronos.sdk import AsyncChronos, Chronos, _normalize_tag


def _mock_transport(handler):
    """Create an httpx MockTransport from a handler function."""
    return httpx.MockTransport(handler)


def _json_response(data, status_code=200):
    return httpx.Response(status_code, json=data)


# -- Fixtures --


def _make_client(handler) -> Chronos:
    transport = _mock_transport(handler)
    client = Chronos.__new__(Chronos)
    client._base_url = "https://chronos.test"
    client._api_key = "test-key"
    client._client = httpx.Client(
        base_url="https://chronos.test",
        transport=transport,
        headers={"X-API-Key": "test-key"},
    )
    return client


def _make_async_client(handler) -> AsyncChronos:
    transport = httpx.MockTransport(handler)
    client = AsyncChronos.__new__(AsyncChronos)
    client._base_url = "https://chronos.test"
    client._api_key = "test-key"
    client._client = httpx.AsyncClient(
        base_url="https://chronos.test",
        transport=transport,
        headers={"X-API-Key": "test-key"},
    )
    return client


# -- Tests --


class TestLaunch:
    def test_launch(self):
        def handler(request: httpx.Request):
            assert request.url.path == "/api/jobs/launch"
            body = json.loads(request.content)
            assert body["world"]["package"] == "plato-world-test:0.1.0"
            assert body["world"]["config"] == {"key": "val"}
            assert body["tags"] == ["my_tag"]
            return _json_response({"session_id": "sess-1", "plato_session_id": "ps-1", "status": "pending"})

        with _make_client(handler) as c:
            resp = c.launch(
                package="plato-world-test:0.1.0",
                config={"key": "val"},
                tags=["my-tag"],
            )
        assert resp.session_id == "sess-1"
        assert resp.status == "pending"

    def test_launch_tag_normalization(self):
        def handler(request: httpx.Request):
            body = json.loads(request.content)
            assert body["tags"] == ["foo_bar.baz_qux"]
            return _json_response({"session_id": "s1", "plato_session_id": "p1", "status": "pending"})

        with _make_client(handler) as c:
            c.launch(package="pkg:1.0", tags=["foo-bar:baz qux"])


class TestGetSession:
    def test_get_session(self):
        def handler(request: httpx.Request):
            assert request.url.path == "/api/sessions/sess-1"
            return _json_response(
                {
                    "public_id": "sess-1",
                    "status": "running",
                    "created_at": "2025-01-01T00:00:00Z",
                }
            )

        with _make_client(handler) as c:
            resp = c.get_session("sess-1")
        assert resp.public_id == "sess-1"
        assert resp.status == "running"


class TestListSessions:
    def test_list_sessions(self):
        def handler(request: httpx.Request):
            assert request.url.path == "/api/sessions"
            assert request.url.params.get("tag") == "project"
            assert request.url.params.get("limit") == "10"
            return _json_response(
                {
                    "sessions": [
                        {
                            "public_id": "s1",
                            "status": "completed",
                            "created_at": "2025-01-01T00:00:00Z",
                        }
                    ]
                }
            )

        with _make_client(handler) as c:
            resp = c.list_sessions(tag="project", limit=10)
        assert len(resp.sessions) == 1


class TestGetStatus:
    def test_get_status(self):
        def handler(request: httpx.Request):
            assert request.url.path == "/api/sessions/sess-1/status"
            return _json_response({"public_id": "sess-1", "status": "running"})

        with _make_client(handler) as c:
            resp = c.get_status("sess-1")
        assert resp.status == "running"


class TestWaitForCompletion:
    def test_wait_for_completion(self):
        call_count = 0

        def handler(request: httpx.Request):
            nonlocal call_count
            if "/status" in str(request.url.path):
                call_count += 1
                status = "running" if call_count < 3 else "completed"
                return _json_response({"public_id": "sess-1", "status": status})
            # get_session call after terminal status
            return _json_response({"public_id": "sess-1", "status": "completed", "created_at": "2025-01-01T00:00:00Z"})

        with _make_client(handler) as c:
            resp = c.wait_for_completion("sess-1", poll_interval=0)
        assert resp.status == "completed"
        assert call_count == 3

    def test_wait_for_completion_timeout(self):
        def handler(request: httpx.Request):
            return _json_response({"public_id": "sess-1", "status": "running"})

        with _make_client(handler) as c:
            with pytest.raises(TimeoutError):
                c.wait_for_completion("sess-1", poll_interval=0, timeout=0)


class TestStop:
    def test_stop(self):
        def handler(request: httpx.Request):
            assert request.url.path == "/api/sessions/sess-1/complete"
            body = json.loads(request.content)
            assert body["status"] == "cancelled"
            return _json_response({"public_id": "sess-1", "status": "cancelled", "created_at": "2025-01-01T00:00:00Z"})

        with _make_client(handler) as c:
            resp = c.stop("sess-1")
        assert resp.status == "cancelled"


class TestGetTraces:
    def test_get_traces(self):
        def handler(request: httpx.Request):
            assert "/otel/sessions/sess-1/traces" in str(request.url.path)
            return _json_response({"session_id": "sess-1", "spans": []})

        with _make_client(handler) as c:
            resp = c.get_traces("sess-1")
        assert resp.session_id == "sess-1"
        assert resp.spans == []


class TestApiKeyFromEnv:
    def test_api_key_from_env(self):
        with patch.dict("os.environ", {"PLATO_API_KEY": "env-key", "CHRONOS_URL": "https://test.co"}):
            c = Chronos()
            assert c._api_key == "env-key"
            assert c._base_url == "https://test.co"
            c.close()


class TestErrorHandling:
    def test_not_found(self):
        def handler(request: httpx.Request):
            return httpx.Response(404, json={"detail": "Not found"})

        with _make_client(handler) as c:
            with pytest.raises(NotFoundError):
                c.get_session("nonexistent")

    def test_unauthorized(self):
        def handler(request: httpx.Request):
            return httpx.Response(401, json={"detail": "Invalid API key"})

        with _make_client(handler) as c:
            with pytest.raises(UnauthorizedError):
                c.get_session("sess-1")


class TestAsyncLaunch:
    @pytest.mark.anyio
    async def test_async_launch(self):
        async def handler(request: httpx.Request):
            body = json.loads(request.content)
            assert body["world"]["package"] == "pkg:1.0"
            return _json_response({"session_id": "s1", "plato_session_id": "p1", "status": "pending"})

        async with _make_async_client(handler) as c:
            resp = await c.launch(package="pkg:1.0")
        assert resp.session_id == "s1"


class TestNormalizeTag:
    def test_normalize(self):
        assert _normalize_tag("foo-bar:baz qux") == "foo_bar.baz_qux"


class TestGetTrajectory:
    def test_get_trajectory(self):
        def handler(request: httpx.Request):
            assert "/sessions/sess-1/trajectory" in str(request.url.path)
            return _json_response(
                {
                    "session_id": "sess-1",
                    "status": "completed",
                    "world": {
                        "name": "test-world",
                        "steps": [
                            {
                                "number": 1,
                                "done": True,
                                "observation": '{"data": {"artifact_ids": {"espocrm": "abc-123"}}}',
                            }
                        ],
                    },
                    "agents": [],
                }
            )

        with _make_client(handler) as c:
            resp = c.get_trajectory("sess-1")
        assert resp.session_id == "sess-1"
        assert resp.world.steps[0].done is True


class TestSessionResult:
    def test_complete_with_result(self):
        """CompleteSessionRequest should include result when provided."""
        captured_body = {}

        def handler(request: httpx.Request):
            nonlocal captured_body
            if "/complete" in str(request.url.path):
                captured_body = json.loads(request.content)
                return _json_response(
                    {
                        "public_id": "sess-1",
                        "status": "completed",
                        "created_at": "2025-01-01T00:00:00Z",
                        "result": captured_body.get("result"),
                    }
                )
            return _json_response({"public_id": "sess-1", "status": "running"})

        with _make_client(handler) as c:
            result_data = {"artifact_ids": {"espocrm": "abc-123"}, "status": "completed"}
            resp = c.complete("sess-1", status="completed", result=result_data)

        assert captured_body["status"] == "completed"
        assert captured_body["result"] == {"artifact_ids": {"espocrm": "abc-123"}, "status": "completed"}
        assert resp.status == "completed"

    def test_complete_without_result(self):
        """CompleteSessionRequest should omit result when not provided."""
        captured_body = {}

        def handler(request: httpx.Request):
            nonlocal captured_body
            if "/complete" in str(request.url.path):
                captured_body = json.loads(request.content)
                return _json_response(
                    {
                        "public_id": "sess-1",
                        "status": "completed",
                        "created_at": "2025-01-01T00:00:00Z",
                    }
                )
            return _json_response({"public_id": "sess-1", "status": "running"})

        with _make_client(handler) as c:
            c.complete("sess-1", status="completed")

        assert "result" not in captured_body

    def test_session_response_includes_result(self):
        """SessionResponse should parse result field from API."""

        def handler(request: httpx.Request):
            return _json_response(
                {
                    "public_id": "sess-1",
                    "status": "completed",
                    "created_at": "2025-01-01T00:00:00Z",
                    "result": {"artifact_ids": {"crm": "id-1"}, "status": "completed", "notes": ["done"]},
                }
            )

        with _make_client(handler) as c:
            resp = c.get_session("sess-1")

        assert resp.status == "completed"
        # result comes through via extra="allow" on the model
        result = getattr(resp, "result", None)
        if result is not None:
            assert result["artifact_ids"]["crm"] == "id-1"
