from __future__ import annotations

import json
import logging
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.orchestration.safety.operation_log import OperationLog, OperationLogRecord


class TestBuildIndexErrorHandling:
    """Tests for build-index recovery branches."""

    def test_build_index_handles_oserror_while_reading(self, tmp_path: Path, caplog) -> None:
        log_file = tmp_path / "operation-log.ndjson"
        log_file.write_text("{}\n", encoding="utf-8")

        with patch("pathlib.Path.read_text", side_effect=OSError("permission denied")):
            with caplog.at_level(logging.WARNING):
                log = OperationLog(tmp_path, "run-1")

        assert log.lookup("op-1") is None
        assert "Failed to read operation log" in caplog.text

    def test_build_index_skips_blank_lines(self, tmp_path: Path) -> None:
        record = OperationLogRecord(operation_id="op-1", run_id="run-1", tool_name="tool", status="completed")
        log_file = tmp_path / "operation-log.ndjson"
        log_file.write_text(f"\n\n{json.dumps(record.to_dict())}\n\n", encoding="utf-8")

        log = OperationLog(tmp_path, "run-1")

        assert log.lookup("op-1") == record
