"""Unit tests for services/feedback.py."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.services.feedback import (
    _dispatch_command_reporter,
    _dispatch_webhook_reporter,
    collect_bundle,
    redact_history,
    submit_feedback,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_config(
    reporters: list[dict[str, Any]] | None = None,
    include_history_default: bool = False,
    max_history_messages: int = 10,
    retry_attempts: int = 1,
    retry_backoff_seconds: float = 0.0,
    max_bundle_bytes: int = 1_000_000,
) -> Any:
    from anteroom.config import FeedbackConfig, FeedbackReporterConfig

    reporter_objs = []
    for r in reporters or []:
        try:
            timeout_val = max(1, min(30, int(r.get("timeout", 10))))
        except (ValueError, TypeError):
            timeout_val = 10
        reporter_objs.append(
            FeedbackReporterConfig(
                name=r.get("name", "default"),
                type=r.get("type", "command"),
                command=r.get("command", ""),
                url=r.get("url", ""),
                timeout=timeout_val,
                enabled=r.get("enabled", True),
            )
        )

    feedback_cfg = FeedbackConfig(
        reporters=reporter_objs,
        include_history_default=include_history_default,
        max_history_messages=max_history_messages,
        retry_attempts=retry_attempts,
        retry_backoff_seconds=retry_backoff_seconds,
        max_bundle_bytes=max_bundle_bytes,
    )

    ai = SimpleNamespace(
        model="test-model",
        base_url="http://localhost",
        system_prompt="",
        verify_ssl=True,
        request_timeout=120,
        api_key="sk-test-secret",
        allowed_domains=[],
        block_localhost_api=False,
    )
    app_settings = SimpleNamespace(
        host="127.0.0.1",
        port=8080,
        data_dir="/tmp/anteroom-test",
        tls=False,
    )
    safety = SimpleNamespace(
        approval_mode="ask_for_writes",
        denied_tools=[],
        allowed_tools=[],
        custom_patterns=[],
        custom_bash_patterns=[],
        sensitive_paths=[],
        tool_tiers={},
    )
    return SimpleNamespace(
        ai=ai,
        app=app_settings,
        safety=safety,
        feedback=feedback_cfg,
    )


def _make_db() -> MagicMock:
    db = MagicMock()
    db.execute = MagicMock()
    return db


# ---------------------------------------------------------------------------
# collect_bundle
# ---------------------------------------------------------------------------


class TestCollectBundle:
    def test_includes_required_fields(self) -> None:
        config = _make_config()
        bundle = collect_bundle(config, "test description")
        assert bundle["schema_version"] == "1"
        assert bundle["description"] == "test description"
        assert "generated_at" in bundle
        assert "system" in bundle
        assert "python_version" in bundle["system"]
        assert "platform" in bundle["system"]
        assert "package" in bundle
        assert "config" in bundle
        assert "safety" in bundle
        assert "tools" in bundle
        assert "spaces" in bundle

    def test_excludes_history_by_default(self) -> None:
        config = _make_config()
        bundle = collect_bundle(config, "test")
        assert bundle["history_included"] is False
        assert "conversation_history" not in bundle

    def test_includes_history_when_provided(self) -> None:
        config = _make_config(max_history_messages=5)
        messages = [{"role": "user", "content": f"msg {i}"} for i in range(10)]
        bundle = collect_bundle(config, "test", conversation_messages=messages, max_history_messages=5)
        assert bundle["history_included"] is True
        assert len(bundle["conversation_history"]) == 5

    def test_redacts_api_key_in_config(self) -> None:
        config = _make_config()
        bundle = collect_bundle(config, "test")
        api_key_value = bundle.get("config", {}).get("ai", {}).get("api_key", "")
        assert api_key_value == "****"

    def test_truncates_to_max_bundle_bytes(self) -> None:
        config = _make_config(max_bundle_bytes=500)
        large_messages = [{"role": "user", "content": "x" * 500} for _ in range(20)]
        bundle = collect_bundle(config, "test", conversation_messages=large_messages, max_bundle_bytes=500)
        assert bundle.get("truncated") is True

    def test_history_dropped_when_bundle_too_large(self) -> None:
        config = _make_config(max_bundle_bytes=100)
        messages = [{"role": "user", "content": "a" * 200}]
        bundle = collect_bundle(config, "test", conversation_messages=messages, max_bundle_bytes=100)
        assert "conversation_history" not in bundle
        assert bundle["history_included"] is False


# ---------------------------------------------------------------------------
# redact_history
# ---------------------------------------------------------------------------


class TestRedactHistory:
    def test_caps_to_max_messages(self) -> None:
        msgs = [{"role": "user", "content": f"msg {i}"} for i in range(20)]
        result = redact_history(msgs, max_messages=5)
        assert len(result) == 5
        assert result[0]["content"] == "msg 15"

    def test_keeps_only_safe_fields(self) -> None:
        msgs = [{"role": "user", "content": "hello", "api_key": "secret", "metadata": {"token": "xyz"}}]
        result = redact_history(msgs, max_messages=10)
        assert "api_key" not in result[0]
        assert "metadata" not in result[0]
        assert result[0]["role"] == "user"
        assert result[0]["content"] == "hello"

    def test_truncates_long_content(self) -> None:
        msgs = [{"role": "user", "content": "a" * 600}]
        result = redact_history(msgs, max_messages=10)
        assert len(result[0]["content"]) <= 520
        assert "(truncated)" in result[0]["content"]


# ---------------------------------------------------------------------------
# _dispatch_command_reporter
# ---------------------------------------------------------------------------


class TestDispatchCommandReporter:
    @pytest.mark.asyncio
    async def test_success(self) -> None:
        with patch("asyncio.create_subprocess_shell") as mock_shell:
            proc = AsyncMock()
            proc.communicate = AsyncMock(return_value=(b"", b""))
            proc.returncode = 0
            mock_shell.return_value = proc

            ok, err = await _dispatch_command_reporter("test", "echo ok", {"key": "val"}, 5.0)
            assert ok is True
            assert err == ""

    @pytest.mark.asyncio
    async def test_non_zero_exit(self) -> None:
        with patch("asyncio.create_subprocess_shell") as mock_shell:
            proc = AsyncMock()
            proc.communicate = AsyncMock(return_value=(b"", b"something failed"))
            proc.returncode = 1
            mock_shell.return_value = proc

            ok, err = await _dispatch_command_reporter("r", "false", {}, 5.0)
            assert ok is False
            assert "exited 1" in err

    @pytest.mark.asyncio
    async def test_timeout(self) -> None:
        import asyncio as _asyncio

        with patch("asyncio.create_subprocess_shell") as mock_shell:
            proc = AsyncMock()
            proc.communicate = AsyncMock(side_effect=_asyncio.TimeoutError())
            proc.kill = AsyncMock()
            proc.wait = AsyncMock()
            mock_shell.return_value = proc

            ok, err = await _dispatch_command_reporter("r", "sleep 999", {}, 0.01)
            assert ok is False
            assert "timed out" in err


# ---------------------------------------------------------------------------
# _dispatch_webhook_reporter
# ---------------------------------------------------------------------------


class TestDispatchWebhookReporter:
    @pytest.mark.asyncio
    async def test_blocked_by_egress(self) -> None:
        with patch("anteroom.services.egress_allowlist.check_egress_allowed", return_value=False):
            ok, err = await _dispatch_webhook_reporter("r", "http://blocked.example.com", {}, 5.0)
            assert ok is False
            assert "egress allowlist" in err

    @pytest.mark.asyncio
    async def test_http_error(self) -> None:
        mock_resp = MagicMock()
        mock_resp.status_code = 500

        with (
            patch("anteroom.services.egress_allowlist.check_egress_allowed", return_value=True),
            patch("httpx.AsyncClient") as mock_client_cls,
        ):
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_resp)
            mock_client_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)

            ok, err = await _dispatch_webhook_reporter("r", "http://ok.example.com", {}, 5.0)
            assert ok is False
            assert "500" in err

    @pytest.mark.asyncio
    async def test_success(self) -> None:
        mock_resp = MagicMock()
        mock_resp.status_code = 200

        with (
            patch("anteroom.services.egress_allowlist.check_egress_allowed", return_value=True),
            patch("httpx.AsyncClient") as mock_client_cls,
        ):
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_resp)
            mock_client_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)

            ok, err = await _dispatch_webhook_reporter("r", "http://ok.example.com", {}, 5.0)
            assert ok is True
            assert err == ""


# ---------------------------------------------------------------------------
# submit_feedback
# ---------------------------------------------------------------------------


class TestSubmitFeedback:
    @pytest.mark.asyncio
    async def test_no_reporters_writes_local_file(self, tmp_path: Any) -> None:
        config = _make_config()
        config.app.data_dir = str(tmp_path)
        db = _make_db()

        result = await submit_feedback("test bug", config, db)
        assert result["status"] == "saved_locally"
        assert result["reporter"] == "local"
        assert "path" in result
        # DB row updated to sent
        update_calls = [str(c) for c in db.execute.call_args_list]
        assert any("sent" in c for c in update_calls)

    @pytest.mark.asyncio
    async def test_empty_description_returns_failed(self, tmp_path: Any) -> None:
        config = _make_config()
        config.app.data_dir = str(tmp_path)
        db = _make_db()

        result = await submit_feedback("  ", config, db)
        assert result["status"] == "failed"
        assert "empty" in result["error"]

    @pytest.mark.asyncio
    async def test_command_reporter_success(self, tmp_path: Any) -> None:
        config = _make_config(reporters=[{"name": "gh", "type": "command", "command": "cat"}])
        config.app.data_dir = str(tmp_path)
        db = _make_db()

        with patch("anteroom.services.feedback._dispatch_command_reporter", new_callable=AsyncMock) as mock_disp:
            mock_disp.return_value = (True, "")
            result = await submit_feedback("test", config, db)

        assert result["status"] == "sent"
        assert result["reporter"] == "gh"

    @pytest.mark.asyncio
    async def test_reporter_failure_marks_db_failed(self, tmp_path: Any) -> None:
        config = _make_config(
            reporters=[{"name": "bad", "type": "command", "command": "false"}],
            retry_attempts=1,
        )
        config.app.data_dir = str(tmp_path)
        db = _make_db()

        with patch("anteroom.services.feedback._dispatch_command_reporter", new_callable=AsyncMock) as mock_disp:
            mock_disp.return_value = (False, "exit 1")
            result = await submit_feedback("test", config, db)

        assert result["status"] == "failed"
        update_calls = [str(c) for c in db.execute.call_args_list]
        assert any("failed" in c for c in update_calls)

    @pytest.mark.asyncio
    async def test_retry_increments_attempt_count(self, tmp_path: Any) -> None:
        config = _make_config(
            reporters=[{"name": "r", "type": "command", "command": "echo"}],
            retry_attempts=3,
            retry_backoff_seconds=0.0,
        )
        config.app.data_dir = str(tmp_path)
        db = _make_db()

        call_count = 0

        async def failing_dispatch(*args: Any, **kwargs: Any) -> tuple[bool, str]:
            nonlocal call_count
            call_count += 1
            return (False, "error")

        with patch("anteroom.services.feedback._dispatch_command_reporter", side_effect=failing_dispatch):
            result = await submit_feedback("test", config, db)

        assert call_count == 3
        assert result["status"] == "failed"

    @pytest.mark.asyncio
    async def test_history_passed_when_provided(self, tmp_path: Any) -> None:
        db = _make_db()
        messages = [{"role": "user", "content": f"msg {i}"} for i in range(10)]

        captured_bundle: dict[str, Any] = {}

        async def capturing_dispatch(
            reporter_name: str, command: str, bundle: dict[str, Any], timeout: float
        ) -> tuple[bool, str]:
            captured_bundle.update(bundle)
            return (True, "")

        with patch("anteroom.services.feedback._dispatch_command_reporter", side_effect=capturing_dispatch):
            config2 = _make_config(
                reporters=[{"name": "r", "type": "command", "command": "echo"}],
                max_history_messages=3,
            )
            config2.app.data_dir = str(tmp_path)
            result = await submit_feedback("test", config2, db, conversation_messages=messages)

        assert result["status"] == "sent"
        assert captured_bundle.get("history_included") is True
        assert len(captured_bundle.get("conversation_history", [])) == 3
