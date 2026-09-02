"""Tests for read_audit_entries() — FR-010."""

from __future__ import annotations

import json
import logging
import logging.handlers

from agentic_devtools.orchestration.safety.query import read_audit_entries


class TestReadAuditEntries:
    """Tests for audit entry reading."""

    def test_no_handler_returns_unavailable(self) -> None:
        result = read_audit_entries(logger_name="test.nonexistent.logger")
        assert result["available"] is False
        assert result["entries"] == []
        assert "message" in result

    def test_handler_with_buffer_returns_entries(self) -> None:
        """When a handler with a buffer attribute exists, entries are returned."""
        logger_name = "test.audit.buffer_handler_test"
        audit_logger = logging.getLogger(logger_name)
        audit_logger.handlers.clear()

        handler = logging.handlers.MemoryHandler(capacity=100)
        audit_logger.addHandler(handler)
        audit_logger.setLevel(logging.DEBUG)
        try:
            entry1 = {"tool": "test_tool", "status": "completed"}
            entry2 = {"tool": "other_tool", "status": "failed"}
            audit_logger.info(json.dumps(entry1))
            audit_logger.info(json.dumps(entry2))

            result = read_audit_entries(logger_name=logger_name)
            assert result["available"] is True
            assert len(result["entries"]) == 2
            assert result["entries"][0]["tool"] == "test_tool"
            assert result["entries"][1]["tool"] == "other_tool"
            assert result["message"] == ""
        finally:
            audit_logger.removeHandler(handler)
            handler.close()

    def test_handler_with_buffer_applies_limit(self) -> None:
        """Limit parameter restricts entries returned from buffer."""
        logger_name = "test.audit.buffer_limit_test"
        audit_logger = logging.getLogger(logger_name)
        audit_logger.handlers.clear()

        handler = logging.handlers.MemoryHandler(capacity=100)
        audit_logger.addHandler(handler)
        audit_logger.setLevel(logging.DEBUG)
        try:
            for i in range(5):
                audit_logger.info(json.dumps({"index": i}))

            result = read_audit_entries(logger_name=logger_name, limit=2)
            assert result["available"] is True
            assert len(result["entries"]) == 2
        finally:
            audit_logger.removeHandler(handler)
            handler.close()

    def test_handler_without_buffer_returns_unavailable(self) -> None:
        """When handlers exist but none have a buffer, returns unavailable."""
        logger_name = "test.audit.no_buffer_handler_test"
        audit_logger = logging.getLogger(logger_name)
        audit_logger.handlers.clear()

        handler = logging.StreamHandler()
        audit_logger.addHandler(handler)
        try:
            result = read_audit_entries(logger_name=logger_name)
            assert result["available"] is False
            assert result["entries"] == []
            assert "message" in result
        finally:
            audit_logger.removeHandler(handler)
            handler.close()

    def test_handler_with_buffer_skips_non_json(self) -> None:
        """Non-JSON entries in the buffer are skipped without error."""
        logger_name = "test.audit.buffer_nonjson_test"
        audit_logger = logging.getLogger(logger_name)
        audit_logger.handlers.clear()

        handler = logging.handlers.MemoryHandler(capacity=100)
        audit_logger.addHandler(handler)
        audit_logger.setLevel(logging.DEBUG)
        try:
            audit_logger.info("not valid json")
            audit_logger.info(json.dumps({"valid": True}))

            result = read_audit_entries(logger_name=logger_name)
            assert result["available"] is True
            assert len(result["entries"]) == 1
            assert result["entries"][0]["valid"] is True
        finally:
            audit_logger.removeHandler(handler)
            handler.close()
