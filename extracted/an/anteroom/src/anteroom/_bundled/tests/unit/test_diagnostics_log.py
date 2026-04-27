from __future__ import annotations

import json
from pathlib import Path

from anteroom.config import load_config
from anteroom.services.diagnostics_log import (
    DiagnosticsLogWriter,
    create_diagnostics_log_writer,
    should_log_summary,
)


def _summary(**overrides: object) -> dict[str, object]:
    summary: dict[str, object] = {
        "version": 1,
        "stop_reason": "provider_timeout",
        "final_phase": "waiting",
        "model": {"provider": "openai", "name": "gpt-test"},
        "usage": {"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 12},
        "retries": [{"attempt": 2, "reason": "timeout"}],
        "tools": [],
        "active_tools": [],
        "runtime_events": [],
        "errors": [{"code": "timeout", "message": "stream timed out"}],
        "redaction": {"raw_tokens": "omitted"},
    }
    summary.update(overrides)
    return summary


def test_should_log_summary_is_failure_only_by_default() -> None:
    assert should_log_summary(_summary()) is True
    assert should_log_summary({"stop_reason": "completed", "errors": [], "runtime_events": []}) is False
    assert should_log_summary({"stop_reason": "completed", "errors": []}, log_successful_debug_turns=True) is True
    assert should_log_summary({"stop_reason": "completed", "tools": [{"status": "error"}]}) is True


def test_writer_appends_redacted_jsonl_entry(tmp_path: Path) -> None:
    writer = DiagnosticsLogWriter(tmp_path, max_entry_bytes=32_768)
    secret = "sk-testsecret1234567890"
    result = writer.write_summary(
        _summary(
            stop_reason="provider_error",
            prompt=f"do not write {secret}",
            errors=[{"code": "provider_error", "message": f"failed token={secret}"}],
            tools=[
                {
                    "name": "bash",
                    "status": "error",
                    "arguments": {"command": f"echo {secret}"},
                    "output": {"stdout": secret},
                }
            ],
        ),
        interface="cli",
        conversation_id="conv-1",
    )

    assert result.written is True
    assert result.path is not None
    line = result.path.read_text().strip()
    entry = json.loads(line)
    rendered = json.dumps(entry)
    assert entry["interface"] == "cli"
    assert entry["conversation_id"] == "conv-1"
    assert entry["stop_reason"] == "provider_error"
    assert secret not in rendered
    assert "raw_tool_arguments" in rendered
    assert entry["summary"]["prompt"]["redacted"] is True
    assert entry["summary"]["tools"][0]["arguments"]["redacted"] is True


def test_writer_bounds_oversized_entries(tmp_path: Path) -> None:
    writer = DiagnosticsLogWriter(tmp_path, max_entry_bytes=1_024)
    result = writer.write_summary(
        _summary(
            runtime_events=[{"kind": "error", "message": "x" * 10_000} for _ in range(100)],
            tools=[{"name": f"tool-{i}", "status": "error", "output_shape": {"type": "string"}} for i in range(100)],
        ),
        interface="web",
        conversation_id="conv-2",
    )

    assert result.written is True
    assert result.path is not None
    line = result.path.read_bytes().strip()
    assert len(line) <= writer.max_entry_bytes
    entry = json.loads(line)
    assert entry["summary"]["diagnostics_truncated"] is True


def test_writer_rotates_and_purges_old_logs(tmp_path: Path) -> None:
    writer = DiagnosticsLogWriter(tmp_path, rotate_size_bytes=128, retention_days=1)
    first = writer.write_summary(_summary(), interface="cli")
    assert first.written is True
    second = writer.write_summary(_summary(), interface="cli")
    assert second.written is True
    assert len(list(tmp_path.glob("diagnostics-*.jsonl*"))) >= 2

    old = tmp_path / "diagnostics-2000-01-01.jsonl"
    old.write_text("{}\n")
    old.touch()
    import os
    import time

    stale = time.time() - (3 * 86400)
    os.utime(old, (stale, stale))
    assert writer.purge_old_logs() >= 1
    assert not old.exists()


def test_writer_write_failure_is_best_effort(tmp_path: Path, monkeypatch) -> None:
    writer = DiagnosticsLogWriter(tmp_path)

    def fail_open(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise OSError("disk full")

    monkeypatch.setattr("builtins.open", fail_open)
    result = writer.write_summary(_summary(), interface="cli")

    assert result.written is False
    assert "write failed" in result.reason


def test_factory_uses_default_diagnostics_dir(tmp_path: Path) -> None:
    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text(
        """
ai:
  base_url: https://api.example.com/v1
  api_key: sk-test
app:
  data_dir: "{data_dir}"
""".format(data_dir=tmp_path.as_posix())
    )
    config, _ = load_config(cfg_path)

    writer = create_diagnostics_log_writer(config)

    assert writer.log_dir == tmp_path / "diagnostics"
