from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from anteroom.services.diagnostics_bundle import BundleOptions, create_diagnostics_bundle, parse_since


def _make_config(tmp_path: Path) -> SimpleNamespace:
    return SimpleNamespace(
        app=SimpleNamespace(host="127.0.0.1", port=8080, data_dir=tmp_path, tls=False),
        ai=SimpleNamespace(
            model="test-model",
            base_url="http://localhost:1234/v1",
            system_prompt="x" * 500,
            verify_ssl=True,
            request_timeout=120,
            api_key="sk-test-secret",
        ),
        safety=SimpleNamespace(
            approval_mode="ask_for_writes",
            allowed_tools=[],
            denied_tools=[],
            custom_patterns=[],
            sensitive_paths=[],
            tool_tiers={},
        ),
        audit=SimpleNamespace(enabled=False, log_path="", redact_content=True, retention_days=90),
        diagnostics_bundle=SimpleNamespace(
            max_files=8,
            max_entries=20,
            max_source_bytes=20_000,
            max_bundle_bytes=500_000,
            max_time_window_hours=168,
        ),
    )


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_bundle_writes_core_files_and_missing_source_warnings(tmp_path: Path) -> None:
    config = _make_config(tmp_path)

    result = create_diagnostics_bundle(config)

    assert result.path.is_dir()
    assert (result.path / "manifest.json").is_file()
    assert (result.path / "runtime.json").is_file()
    assert (result.path / "config-summary.json").is_file()
    manifest = _read_json(result.path / "manifest.json")
    assert manifest["local_only"] is True
    assert manifest["redaction"]["raw_prompts"] == "omitted"
    assert any("source absent" in warning for warning in result.warnings)
    assert any("diagnostics_log source" in warning for warning in result.warnings)


def test_diagnostics_entries_are_filtered_bounded_and_redacted(tmp_path: Path) -> None:
    config = _make_config(tmp_path)
    diagnostics_dir = tmp_path / "diagnostics"
    diagnostics_dir.mkdir()
    now = datetime.now(timezone.utc)
    rows = [
        {
            "timestamp": (now - timedelta(minutes=5)).isoformat(),
            "level": "error",
            "conversation_id": "conv-1",
            "turn_id": "turn-1",
            "request_id": "req-1",
            "message": "failed with api_key=abc123 and sk-test-secret-1234567890",
            "prompt": "raw user prompt",
            "tool_output": "raw tool output",
            "details": {"token": "secret", "status_code": 500, "request_id": "req-1"},
        },
        {
            "timestamp": (now - timedelta(minutes=4)).isoformat(),
            "level": "error",
            "conversation_id": "conv-2",
            "message": "other conversation",
        },
    ]
    (diagnostics_dir / "diagnostics-errors.jsonl").write_text(
        "\n".join(json.dumps(row) for row in rows) + "\n",
        encoding="utf-8",
    )

    result = create_diagnostics_bundle(
        config,
        BundleOptions(conversation_id="conv-1", max_entries=1),
    )

    text = (result.path / "diagnostics-errors.jsonl").read_text(encoding="utf-8")
    assert "conv-1" in text
    assert "conv-2" not in text
    assert "raw user prompt" not in text
    assert "raw tool output" not in text
    assert "abc123" not in text
    assert "sk-test-secret" not in text
    assert "[redacted]" in text


def test_bundle_reads_daily_diagnostics_error_log_pattern(tmp_path: Path) -> None:
    config = _make_config(tmp_path)
    diagnostics_dir = tmp_path / "diagnostics"
    diagnostics_dir.mkdir()
    now = datetime.now(timezone.utc)
    row = {
        "timestamp": now.isoformat(),
        "level": "error",
        "conversation_id": "conv-1",
        "turn_id": "turn-1",
        "request_id": "req-1",
        "message": "provider timeout",
        "summary": {"prompt": "raw user prompt", "stop_reason": "provider_timeout"},
    }
    (diagnostics_dir / "diagnostics-2026-04-26.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")

    result = create_diagnostics_bundle(config, BundleOptions(conversation_id="conv-1"))

    text = (result.path / "diagnostics-errors.jsonl").read_text(encoding="utf-8")
    assert "conv-1" in text
    assert "provider timeout" in text
    assert "raw user prompt" not in text


def test_latest_failure_selects_newest_failure(tmp_path: Path) -> None:
    config = _make_config(tmp_path)
    path = tmp_path / "diagnostics-log.jsonl"
    now = datetime.now(timezone.utc)
    rows = [
        {"timestamp": (now - timedelta(minutes=10)).isoformat(), "status": "failed", "code": "old"},
        {"timestamp": (now - timedelta(minutes=1)).isoformat(), "status": "failed", "code": "new"},
    ]
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")

    result = create_diagnostics_bundle(config, BundleOptions(latest_failure=True))

    lines = (result.path / "diagnostics-errors.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["code"] == "new"


def test_audit_refs_include_metadata_only(tmp_path: Path) -> None:
    config = _make_config(tmp_path)
    audit_dir = tmp_path / "audit"
    audit_dir.mkdir()
    row = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "tool_calls.completed",
        "severity": "info",
        "conversation_id": "conv-1",
        "tool_name": "bash",
        "details": {"tool_input": "cat secrets.txt", "request_id": "req-1", "status": "ok"},
    }
    (audit_dir / "audit-2026-04-26.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")

    result = create_diagnostics_bundle(config, BundleOptions(conversation_id="conv-1"))

    text = (result.path / "audit-refs.jsonl").read_text(encoding="utf-8")
    assert "tool_calls.completed" in text
    assert "req-1" in text
    assert "cat secrets" not in text


def test_debug_summaries_keep_safe_shapes_and_omit_raw_fields(tmp_path: Path) -> None:
    config = _make_config(tmp_path)
    debug_dir = tmp_path / "debug-diagnostics"
    debug_dir.mkdir()
    row = {
        "version": 1,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "stop_reason": "completed",
        "usage": {"prompt_tokens": 10, "completion_tokens": 4},
        "tools": [
            {
                "id": "tool-1",
                "name": "bash",
                "status": "ok",
                "argument_shape": {"type": "object", "keys": ["cmd"]},
                "arguments": {"cmd": "cat secret.txt"},
                "output": "raw command output",
            }
        ],
        "redaction": {"raw_tool_arguments": "omitted", "raw_tool_output": "omitted"},
    }
    (debug_dir / "debug-summaries.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")

    result = create_diagnostics_bundle(config)

    text = (result.path / "debug-summaries.jsonl").read_text(encoding="utf-8")
    assert "prompt_tokens" in text
    assert "bash" in text
    assert "argument_shape" in text
    assert "cat secret" not in text
    assert "raw command output" not in text


def test_zip_format_creates_zip_without_uploading(tmp_path: Path) -> None:
    config = _make_config(tmp_path)
    output = tmp_path / "bundle-output.zip"

    result = create_diagnostics_bundle(config, BundleOptions(output=output, bundle_format="zip"))

    assert result.path == output
    assert result.path.is_file()
    assert result.format == "zip"


def test_core_files_are_always_written_when_max_files_is_low(tmp_path: Path) -> None:
    config = _make_config(tmp_path)
    config.diagnostics_bundle.max_files = 1

    result = create_diagnostics_bundle(config)

    assert (result.path / "manifest.json").is_file()
    assert (result.path / "runtime.json").is_file()
    assert (result.path / "config-summary.json").is_file()


def test_parse_since_relative_and_invalid() -> None:
    now = datetime(2026, 4, 26, 12, tzinfo=timezone.utc)

    assert parse_since("2h", now=now) == now - timedelta(hours=2)
    with pytest.raises(ValueError):
        parse_since("soon")
