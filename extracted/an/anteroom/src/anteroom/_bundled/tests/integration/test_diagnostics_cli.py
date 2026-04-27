from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from anteroom.cli.diagnostics_cli import _run_diagnostics


def _make_config(tmp_path: Path) -> SimpleNamespace:
    return SimpleNamespace(
        app=SimpleNamespace(host="127.0.0.1", port=8080, data_dir=tmp_path, tls=False),
        ai=SimpleNamespace(
            model="test-model",
            base_url="http://localhost:1234/v1",
            system_prompt="",
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


def test_diagnostics_bundle_cli_prints_path_size_and_warning(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    config = _make_config(tmp_path)
    path = tmp_path / "diagnostics-log.jsonl"
    path.write_text(
        json.dumps(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": "error",
                "conversation_id": "conv-1",
                "request_id": "req-1",
                "message": "request failed",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    output = tmp_path / "support-bundle"
    args = argparse.Namespace(
        diagnostics_action="bundle",
        conversation_id="conv-1",
        turn_id=None,
        request_id=None,
        since="2h",
        latest_failure=False,
        output=str(output),
        bundle_format="directory",
        max_files=None,
        max_entries=None,
        max_source_bytes=None,
        max_bundle_bytes=None,
    )

    _run_diagnostics(config, args)

    captured = capsys.readouterr()
    assert f"Diagnostics bundle: {output}" in captured.out
    assert "Size:" in captured.out
    assert "Inspect the bundle before sharing" in captured.out
    assert (output / "manifest.json").is_file()
    assert (output / "diagnostics-errors.jsonl").is_file()


def test_diagnostics_bundle_cli_rejects_invalid_since(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    config = _make_config(tmp_path)
    args = argparse.Namespace(
        diagnostics_action="bundle",
        conversation_id=None,
        turn_id=None,
        request_id=None,
        since="yesterday-ish",
        latest_failure=False,
        output=None,
        bundle_format="directory",
        max_files=None,
        max_entries=None,
        max_source_bytes=None,
        max_bundle_bytes=None,
    )

    with pytest.raises(SystemExit) as exc_info:
        _run_diagnostics(config, args)

    assert exc_info.value.code == 1
    assert "Invalid --since" in capsys.readouterr().err
