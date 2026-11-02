from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.orchestration.safety.operation_log import OperationLog, OperationLogRecord


class TestAppendFallback:
    """Tests for append fallback paths."""

    def test_append_creates_file_when_locked_file_fails_first_call(self, tmp_path: Path) -> None:
        """FileNotFoundError on first locked_file call triggers mkdir + retry."""
        log = OperationLog(tmp_path, "run-1")
        record = OperationLogRecord(operation_id="op-1", run_id="run-1", tool_name="tool", status="pending")

        from agentic_devtools.file_locking import locked_file as real_locked_file

        call_count = {"n": 0}

        def side_effect_fn(*args, **kwargs):
            call_count["n"] += 1
            if call_count["n"] == 1:
                raise FileNotFoundError("simulated missing file")
            return real_locked_file(*args, **kwargs)

        with patch("agentic_devtools.orchestration.safety.operation_log.locked_file", side_effect=side_effect_fn):
            log.append(record)

        content = log.log_path.read_text(encoding="utf-8").strip()
        assert json.loads(content)["operation_id"] == "op-1"
        assert log.lookup("op-1") == record

    def test_append_fallback_uses_locked_file(self, tmp_path: Path) -> None:
        """The FileNotFoundError fallback uses locked_file (NFR-002), not plain open.

        Also asserts that a second append after the fallback does not truncate
        or overwrite the first record (NDJSON append-only contract).
        """
        log = OperationLog(tmp_path, "run-1")
        record1 = OperationLogRecord(operation_id="op-1", run_id="run-1", tool_name="tool", status="pending")
        record2 = OperationLogRecord(operation_id="op-2", run_id="run-1", tool_name="tool", status="completed")

        from agentic_devtools.file_locking import locked_file as real_locked_file

        call_count = {"n": 0}
        fallback_called_with_locked = {"value": False}

        def side_effect_fn(*args, **kwargs):
            call_count["n"] += 1
            if call_count["n"] == 1:
                raise FileNotFoundError("simulated")
            fallback_called_with_locked["value"] = True
            return real_locked_file(*args, **kwargs)

        with patch("agentic_devtools.orchestration.safety.operation_log.locked_file", side_effect=side_effect_fn):
            log.append(record1)

        assert fallback_called_with_locked["value"] is True

        # Second append must not truncate the first record (NDJSON append-only contract).
        log.append(record2)
        lines = [ln for ln in log.log_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
        assert len(lines) == 2, f"Expected 2 NDJSON records, got {len(lines)}"
        assert json.loads(lines[0])["operation_id"] == "op-1"
        assert json.loads(lines[1])["operation_id"] == "op-2"
