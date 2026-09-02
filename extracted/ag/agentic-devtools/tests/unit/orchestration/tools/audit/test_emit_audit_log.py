"""Tests for audit logging."""

import json
import logging

from agentic_devtools.orchestration.tools.audit import emit_audit_log


class TestEmitAuditLog:
    """Tests for emit_audit_log function."""

    def test_success_audit(self, caplog):
        """Audit entry emitted for successful invocation."""
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.tools.audit"):
            entry = emit_audit_log(
                tool_name="test_tool",
                inputs={"key": "value"},
                output={"result": "ok"},
                duration_ms=42.0,
                status="success",
                correlation_id="corr-123",
            )

        assert entry.tool_name == "test_tool"
        assert entry.status == "success"
        assert entry.duration_ms == 42.0
        assert entry.correlation_id == "corr-123"
        assert len(caplog.records) == 1
        # Verify JSON parseable
        parsed = json.loads(caplog.records[0].message)
        assert parsed["tool_name"] == "test_tool"
        assert parsed["status"] == "success"

    def test_error_audit(self, caplog):
        """Audit entry includes error fields."""
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.tools.audit"):
            entry = emit_audit_log(
                tool_name="failing_tool",
                inputs={},
                output=None,
                duration_ms=100.0,
                status="error",
                error_type="execution_error",
                error_message="boom",
            )

        assert entry.error_type == "execution_error"
        assert entry.error_message == "boom"

    def test_sensitive_keys_redacted(self, caplog):
        """Sensitive input keys are redacted."""
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.tools.audit"):
            entry = emit_audit_log(
                tool_name="auth_tool",
                inputs={"token": "secret123", "name": "visible"},
                output=None,
                duration_ms=1.0,
                status="success",
            )

        assert entry.input_summary["token"] == "[REDACTED]"
        assert entry.input_summary["name"] == "visible"

    def test_long_input_values_truncated(self, caplog):
        """Long input string values are truncated before logging."""
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.tools.audit"):
            entry = emit_audit_log(
                tool_name="filesystem_write_file",
                inputs={"content": "A" * 1000, "token": "secret123"},
                output=None,
                duration_ms=1.0,
                status="success",
                max_output_summary_length=50,
            )

        assert entry.input_summary["token"] == "[REDACTED]"
        assert entry.input_summary["content"] == ("A" * 50) + "..."
        parsed = json.loads(caplog.records[0].message)
        assert parsed["input_summary"]["content"] == ("A" * 50) + "..."

    def test_sensitive_output_keys_redacted(self, caplog):
        """Sensitive output keys are redacted before logging."""
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.tools.audit"):
            entry = emit_audit_log(
                tool_name="auth_tool",
                inputs={},
                output=[
                    {
                        "token": "secret123",
                        "nested": {"password": "pw"},
                        "items": [{"api_key": "abc"}],
                    }
                ],
                duration_ms=1.0,
                status="success",
            )

        parsed = json.loads(entry.output_summary)
        assert parsed[0]["token"] == "[REDACTED]"
        assert parsed[0]["nested"]["password"] == "[REDACTED]"
        assert parsed[0]["items"][0]["api_key"] == "[REDACTED]"

    def test_output_truncated(self, caplog):
        """Long output is truncated."""
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.tools.audit"):
            entry = emit_audit_log(
                tool_name="verbose",
                inputs={},
                output="x" * 1000,
                duration_ms=1.0,
                status="success",
                max_output_summary_length=50,
            )

        assert len(entry.output_summary) <= 53  # 50 + "..."

    def test_large_dict_value_truncated_before_serialisation(self, caplog):
        """Long string values inside a dict output are truncated before json.dumps.

        This verifies that emit_audit_log does not serialise a huge payload
        (e.g. file content returned by filesystem_read_file) only to throw
        most of it away after the fact.
        """
        large_content = "A" * 100_000
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.tools.audit"):
            entry = emit_audit_log(
                tool_name="filesystem_read_file",
                inputs={"path": "/tmp/big.txt"},
                output={"content": large_content, "size": 100_000},
                duration_ms=5.0,
                status="success",
                max_output_summary_length=200,
            )

        # The summary must be bounded — not the full 100 KB content
        assert len(entry.output_summary) <= 203  # 200 + "..."
        # Confirm the content key is present but truncated in the summary
        assert "content" in entry.output_summary
        assert large_content not in entry.output_summary

    def test_dry_run_skipped_status(self, caplog):
        """Dry-run skipped status recorded correctly."""
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.tools.audit"):
            entry = emit_audit_log(
                tool_name="mutator",
                inputs={"x": 1},
                output=None,
                duration_ms=0.1,
                status="dry_run_skipped",
            )

        assert entry.status == "dry_run_skipped"
