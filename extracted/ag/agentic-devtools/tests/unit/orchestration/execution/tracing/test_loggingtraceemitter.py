"""Tests for LoggingTraceEmitter emit and failure handling."""

import logging

import pytest

from agentic_devtools.orchestration.execution.tracing import (
    LoggingTraceEmitter,
    TraceEvent,
)


class TestLoggingTraceEmitter:
    def test_emit_logs_json(self, caplog: pytest.LogCaptureFixture) -> None:
        emitter = LoggingTraceEmitter()
        event = TraceEvent(
            timestamp=1234.0,
            node_name="test_node",
            operation_type="reasoning",
            model_id="gpt-4",
        )
        with caplog.at_level(logging.DEBUG, logger="agentic_devtools.orchestration.execution.tracing"):
            emitter.emit(event)
        assert len(caplog.records) == 1
        assert "test_node" in caplog.records[0].message
        assert "reasoning" in caplog.records[0].message

    def test_emit_failure_swallowed(self, capsys, monkeypatch) -> None:  # noqa: ANN001
        emitter = LoggingTraceEmitter()
        event = TraceEvent(
            timestamp=1234.0,
            node_name="broken_node",
            operation_type="reasoning",
        )

        # Monkey-patch logger.debug to raise
        def _raise(*args, **kwargs):  # noqa: ANN002, ANN003
            raise RuntimeError("logging broken")

        monkeypatch.setattr(
            "agentic_devtools.orchestration.execution.tracing.logger.debug",
            _raise,
        )

        # Should NOT raise
        emitter.emit(event)

        # Should print warning to stderr
        captured = capsys.readouterr()
        assert "emit failed" in captured.err
        assert "broken_node" in captured.err

    def test_emit_failure_logs_only_exception_type_not_message(self, capsys, monkeypatch) -> None:  # noqa: ANN001
        """Stderr warning must contain only the exception type, never the message."""
        emitter = LoggingTraceEmitter()
        event = TraceEvent(
            timestamp=1234.0,
            node_name="secret_node",
            operation_type="reasoning",
        )

        sensitive_message = "token=super_secret_credential_abc123"

        def _raise(*args, **kwargs):  # noqa: ANN002, ANN003
            raise RuntimeError(sensitive_message)

        monkeypatch.setattr(
            "agentic_devtools.orchestration.execution.tracing.logger.debug",
            _raise,
        )

        emitter.emit(event)

        captured = capsys.readouterr()
        assert sensitive_message not in captured.err
        assert "RuntimeError" in captured.err

    def test_emit_multiple_events(self, caplog: pytest.LogCaptureFixture) -> None:
        emitter = LoggingTraceEmitter()
        with caplog.at_level(logging.DEBUG, logger="agentic_devtools.orchestration.execution.tracing"):
            for i in range(3):
                emitter.emit(
                    TraceEvent(
                        timestamp=float(i),
                        node_name=f"node_{i}",
                        operation_type="tool_invocation",
                    )
                )
        assert len(caplog.records) == 3
