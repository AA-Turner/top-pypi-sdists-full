"""Unit tests for services/feedback.py."""

from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.services.feedback import (
    _apply_bundle_size_limit,
    _dispatch_command_reporter,
    _dispatch_webhook_reporter,
    collect_bundle,
    redact_history,
    sanitize_turn_diagnostics,
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

    def test_space_manifest_omits_local_paths_and_instruction_text(self) -> None:
        config = _make_config()
        bundle = collect_bundle(
            config,
            "test",
            active_space={
                "id": "space-1",
                "name": "Main",
                "source_file": "/private/source-secret.yaml",
                "instructions": "internal prompt text",
            },
        )

        rendered = json.dumps(bundle["spaces"])
        assert bundle["spaces"]["active"] == {
            "id": "space-1",
            "name": "Main",
            "pack_count": 0,
            "source_count": 0,
        }
        assert "/private/source-secret.yaml" not in rendered
        assert "internal prompt text" not in rendered

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

    def test_turn_diagnostics_are_allowlisted_and_redacted(self) -> None:
        config = _make_config()
        bundle = collect_bundle(
            config,
            "test",
            turn_diagnostics={
                "stop_reason": "completed",
                "raw_prompt": "do not send this",
                "model": {"provider": "openai", "name": "gpt-test", "api_key": "sk-123456789012SECRET"},
                "tools": [
                    {
                        "name": "bash",
                        "status": "success",
                        "argument_shape": {"type": "object", "keys": ["command"]},
                        "raw_arguments": {"command": "cat secret.txt"},
                    }
                ],
                "errors": [{"code": "api_key=supersecret", "message": "Authorization: Bearer abc123"}],
            },
        )

        rendered = json.dumps(bundle)
        assert bundle["bundle_manifest"]["turn_diagnostics_included"] is True
        assert "raw_prompt" not in rendered
        assert "raw_arguments" not in rendered
        assert "supersecret" not in rendered
        assert "Bearer abc123" not in rendered
        assert "[redacted]" in rendered

    def test_sanitize_turn_diagnostics_handles_malformed_values_and_limits_lists(self) -> None:
        summary = {
            "unknown": "drop me",
            "tools": [{"name": f"tool-{i}", "raw_arguments": "drop me"} for i in range(60)],
            "usage": {"total_tokens": 10, "secret": "drop me"},
            "runtime_events": [{"kind": "error", "message": "api_key=supersecret"}],
        }

        sanitized = sanitize_turn_diagnostics(summary)

        assert sanitized is not None
        assert "unknown" not in sanitized
        assert len(sanitized["tools"]) == 50
        assert "raw_arguments" not in sanitized["tools"][0]
        assert sanitized["usage"] == {"total_tokens": 10}
        assert "supersecret" not in json.dumps(sanitized)
        assert sanitize_turn_diagnostics(None) is None

    def test_pack_artifact_attachment_manifests_exclude_content_values_and_paths(self, tmp_path: Any) -> None:
        from anteroom.db import init_db
        from anteroom.services.artifact_storage import create_artifact

        db = init_db(tmp_path / "test.db")
        now = "2026-04-26T00:00:00Z"
        try:
            db.execute(
                "INSERT INTO packs (id, name, namespace, version, description, source_path, installed_at, updated_at)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                ("pack-1", "diagnostics", "team", "1.2.3", "desc", "/private/pack-secret", now, now),
            )
            skill = create_artifact(
                db,
                "@team/skill/helper",
                "skill",
                "team",
                "helper",
                "artifact-secret-content",
                metadata={"safe_key": "metadata-secret-value"},
            )
            overlay = create_artifact(
                db,
                "@team/config_overlay/defaults",
                "config_overlay",
                "team",
                "defaults",
                "ai:\n  api_key: overlay-secret-value\n  request_timeout: 30\n",
            )
            db.execute("INSERT INTO pack_artifacts (pack_id, artifact_id) VALUES (?, ?)", ("pack-1", skill["id"]))
            db.execute("INSERT INTO pack_artifacts (pack_id, artifact_id) VALUES (?, ?)", ("pack-1", overlay["id"]))
            db.execute(
                "INSERT INTO pack_attachments (id, pack_id, project_path, space_id, scope, priority, created_at)"
                " VALUES (?, ?, ?, ?, ?, ?, ?)",
                ("att-1", "pack-1", None, None, "global", 20, now),
            )
            db.execute(
                "INSERT INTO pack_attachments (id, pack_id, project_path, space_id, scope, priority, created_at)"
                " VALUES (?, ?, ?, ?, ?, ?, ?)",
                ("att-2", "pack-1", str(tmp_path), None, "project", 10, now),
            )
            db.execute(
                "INSERT INTO conversations (id, title, type, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                ("conv-1", "Feedback", "chat", now, now),
            )
            db.execute(
                "INSERT INTO messages (id, conversation_id, role, content, created_at, position)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                ("msg-1", "conv-1", "user", "hello", now, 1),
            )
            db.execute(
                "INSERT INTO attachments (id, message_id, filename, mime_type, size_bytes, storage_path)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                ("upload-1", "msg-1", "file-secret.pdf", "application/pdf", 1234, "attachments/secret/file.pdf"),
            )
            db.commit()

            bundle = collect_bundle(
                _make_config(),
                "test",
                db=db,
                conversation_id="conv-1",
                project_path=str(tmp_path / "child"),
                max_bundle_bytes=1_000_000,
            )
        finally:
            db.close()

        assert bundle["packs"]["active_count"] == 1
        assert len(bundle["packs"]["active"][0]["attachments"]) == 2
        assert bundle["artifacts"]["active_count"] == 1
        assert bundle["artifacts"]["config_overlay_count"] == 1
        assert bundle["artifacts"]["config_overlays"][0]["keys"] == ["ai.api_key", "ai.request_timeout"]
        assert bundle["attachments"]["count"] == 1
        assert bundle["attachments"]["recent"] == [{"mime_type": "application/pdf", "size_bytes": 1234}]

        rendered = json.dumps(bundle)
        assert "artifact-secret-content" not in rendered
        assert "metadata-secret-value" not in rendered
        assert "/private/pack-secret" not in rendered
        assert "file-secret.pdf" not in rendered
        assert "attachments/secret/file.pdf" not in rendered
        assert "overlay-secret-value" not in rendered
        assert "content_hash" not in rendered

    def test_bundle_size_limit_drops_detail_sections_and_refreshes_manifest(self) -> None:
        bundle: dict[str, Any] = {
            "schema_version": "1",
            "history_included": True,
            "conversation_history": [{"role": "user", "content": "x" * 200}],
            "turn_diagnostics": {"runtime_events": [{"message": "x" * 200}]},
            "artifacts": {"active_count": 1, "config_overlay_count": 0, "active": [{"fqn": "x" * 200}]},
            "packs": {"active_count": 1, "installed_count": 1, "active": [{"name": "x" * 200}]},
            "attachments": {"count": 1, "recent": [{"mime_type": "text/plain", "size_bytes": 1}]},
            "spaces": {"active": {"name": "Main"}},
            "tools": {"available": ["bash"]},
            "bundle_manifest": {},
        }

        _apply_bundle_size_limit(bundle, 700)

        assert bundle["history_included"] is False
        assert "conversation_history" not in bundle
        assert "turn_diagnostics" not in bundle
        assert bundle["artifacts"]["active"] == []
        assert bundle["packs"]["active"] == []
        assert bundle["attachments"]["recent"] == []
        assert bundle["bundle_manifest"]["turn_diagnostics_included"] is False
        assert "bundle_manifest" not in bundle["bundle_manifest"]["sections"]


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

    def test_sanitizes_secret_patterns_in_content(self) -> None:
        msgs = [{"role": "user", "content": "api_key=supersecret Authorization: Bearer abc123"}]
        result = redact_history(msgs, max_messages=10)
        assert "supersecret" not in result[0]["content"]
        assert "Bearer abc123" not in result[0]["content"]
        assert "[redacted]" in result[0]["content"]


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
    async def test_no_reporter_rows_are_committed(self, tmp_path: Any) -> None:
        from anteroom.db import init_db

        db_path = tmp_path / "test.db"
        db = init_db(db_path)
        config = _make_config()
        config.app.data_dir = str(tmp_path)
        try:
            result = await submit_feedback("test bug", config, db)

            with sqlite3.connect(db_path) as other:
                row = other.execute("SELECT status, description FROM feedback_reports").fetchone()
        finally:
            db.close()

        assert result["status"] == "saved_locally"
        assert row == ("sent", "test bug")

    @pytest.mark.asyncio
    async def test_no_reporter_local_files_are_unique_with_same_timestamp(self, tmp_path: Any) -> None:
        class FixedDatetime(datetime):
            @classmethod
            def now(cls, tz: Any = None) -> datetime:
                return cls(2026, 4, 26, 12, 0, 0, tzinfo=tz or timezone.utc)

        config = _make_config()
        config.app.data_dir = str(tmp_path)
        db = _make_db()

        with (
            patch("anteroom.services.feedback.datetime", FixedDatetime),
            patch(
                "anteroom.services.feedback.uuid.uuid4",
                side_effect=[
                    uuid.UUID("00000000-0000-0000-0000-000000000001"),
                    uuid.UUID("00000000-0000-0000-0000-000000000002"),
                ],
            ),
        ):
            first = await submit_feedback("first bug", config, db)
            second = await submit_feedback("second bug", config, db)

        assert first["path"] != second["path"]
        assert first["path"].endswith("feedback-20260426T120000Z-00000000-0000-0000-0000-000000000001.json")
        assert second["path"].endswith("feedback-20260426T120000Z-00000000-0000-0000-0000-000000000002.json")
        assert len(list(tmp_path.glob("feedback-*.json"))) == 2

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
