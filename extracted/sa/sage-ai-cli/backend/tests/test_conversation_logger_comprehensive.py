"""Comprehensive tests for backend/conversation_logger.py."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest


class TestEstimateTokens:
    """Tests for estimate_tokens function."""

    def test_import(self):
        """Function can be imported."""
        from backend.conversation_logger import estimate_tokens
        assert estimate_tokens is not None

    def test_empty_string(self):
        """Empty string returns 1."""
        from backend.conversation_logger import estimate_tokens

        result = estimate_tokens("")
        assert result == 1  # max(1, 0)

    def test_short_string(self):
        """Short string estimation."""
        from backend.conversation_logger import estimate_tokens

        result = estimate_tokens("test")  # 4 chars
        assert result == 1

    def test_longer_string(self):
        """Longer string estimation."""
        from backend.conversation_logger import estimate_tokens

        result = estimate_tokens("Hello, World!")  # 13 chars
        assert result == 3  # 13 // 4 = 3


class TestConversationLoggerConstants:
    """Tests for conversation logger constants."""

    def test_chars_per_token(self):
        """CHARS_PER_TOKEN is defined."""
        from backend.conversation_logger import CHARS_PER_TOKEN

        assert CHARS_PER_TOKEN == 4


class TestConversationLoggerInit:
    """Tests for ConversationLogger initialization."""

    def test_create_default(self):
        """Create with default path."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger()
        assert logger.base_dir is not None

    def test_create_custom_path(self, tmp_path):
        """Create with custom path."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)
        assert logger.base_dir == tmp_path
        assert logger.base_dir.exists()


class TestConversationLoggerLogInput:
    """Tests for log_input method."""

    def test_log_input(self, tmp_path):
        """Log user input."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)
        logger.log_input("conv-1", "Hello, AI!")

        inputs = logger.get_inputs("conv-1")
        assert len(inputs) == 1
        assert inputs[0]["content"] == "Hello, AI!"

    def test_log_input_with_timestamp(self, tmp_path):
        """Log input with custom timestamp."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)
        timestamp = "2024-01-01T12:00:00Z"
        logger.log_input("conv-1", "Test", timestamp=timestamp)

        inputs = logger.get_inputs("conv-1")
        assert inputs[0]["timestamp"] == timestamp

    def test_log_input_with_attachments(self, tmp_path):
        """Log input with attachments."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)
        attachments = [{"file_id": "f1", "filename": "test.txt"}]
        logger.log_input("conv-1", "Check this file", attachments=attachments)

        inputs = logger.get_inputs("conv-1")
        assert inputs[0]["attachments"] == attachments

    def test_log_multiple_inputs(self, tmp_path):
        """Log multiple inputs."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)
        logger.log_input("conv-1", "First")
        logger.log_input("conv-1", "Second")
        logger.log_input("conv-1", "Third")

        inputs = logger.get_inputs("conv-1")
        assert len(inputs) == 3


class TestConversationLoggerLogOutput:
    """Tests for log_output method."""

    def test_log_output(self, tmp_path):
        """Log AI output."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)
        logger.log_output("conv-1", "Hello! How can I help?", "llama-3b")

        outputs = logger.get_outputs("conv-1")
        assert len(outputs) == 1
        assert outputs[0]["content"] == "Hello! How can I help?"
        assert outputs[0]["model_id"] == "llama-3b"

    def test_log_output_with_metadata(self, tmp_path):
        """Log output with metadata."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)
        metadata = {"latency_ms": 150, "tokens_used": 50}
        logger.log_output("conv-1", "Response", "model-1", metadata=metadata)

        outputs = logger.get_outputs("conv-1")
        assert outputs[0]["metadata"] == metadata


class TestConversationLoggerGetMethods:
    """Tests for get_inputs and get_outputs methods."""

    def test_get_inputs_empty(self, tmp_path):
        """Get inputs for non-existent conversation."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)
        inputs = logger.get_inputs("nonexistent")
        assert inputs == []

    def test_get_outputs_empty(self, tmp_path):
        """Get outputs for non-existent conversation."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)
        outputs = logger.get_outputs("nonexistent")
        assert outputs == []

    def test_get_inputs_corrupt_file(self, tmp_path):
        """Get inputs with corrupt log file returns empty list."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)

        # Create corrupt log file
        corrupt_path = logger._inputs_path("conv-1")
        corrupt_path.write_text("invalid json")

        inputs = logger.get_inputs("conv-1")
        assert inputs == []


class TestConversationLoggerExport:
    """Tests for export method."""

    def test_export(self, tmp_path):
        """Export conversation."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)
        logger.log_input("conv-1", "Hello")
        logger.log_output("conv-1", "Hi!", "model-1")

        export = logger.export("conv-1")
        assert export["conversation_id"] == "conv-1"
        assert len(export["inputs"]) == 1
        assert len(export["outputs"]) == 1
        assert "exported_at" in export


class TestConversationLoggerGetContext:
    """Tests for get_context method."""

    def test_get_context_interleaved(self, tmp_path):
        """Get interleaved context."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)

        # Log inputs and outputs with different timestamps
        logger.log_input("conv-1", "Q1", timestamp="2024-01-01T12:00:00Z")
        logger.log_output("conv-1", "A1", "model", timestamp="2024-01-01T12:00:01Z")
        logger.log_input("conv-1", "Q2", timestamp="2024-01-01T12:00:02Z")
        logger.log_output("conv-1", "A2", "model", timestamp="2024-01-01T12:00:03Z")

        context = logger.get_context("conv-1")
        assert len(context) == 4
        assert context[0]["role"] == "user"
        assert context[1]["role"] == "assistant"

    def test_get_context_max_entries(self, tmp_path):
        """Get context respects max_entries."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)

        for i in range(20):
            logger.log_input("conv-1", f"Input {i}", timestamp=f"2024-01-01T{i:02d}:00:00Z")

        context = logger.get_context("conv-1", max_entries=5)
        assert len(context) == 5

    def test_get_context_sorted_by_timestamp(self, tmp_path):
        """Context is sorted by timestamp."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)

        # Add in reverse order
        logger.log_input("conv-1", "Second", timestamp="2024-01-01T12:01:00Z")
        logger.log_input("conv-1", "First", timestamp="2024-01-01T12:00:00Z")

        context = logger.get_context("conv-1")
        assert context[0]["content"] == "First"
        assert context[1]["content"] == "Second"


class TestConversationLoggerDelete:
    """Tests for delete method."""

    def test_delete_conversation(self, tmp_path):
        """Delete conversation logs."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)
        logger.log_input("conv-1", "Test")
        logger.log_output("conv-1", "Response", "model")

        inputs_path = logger._inputs_path("conv-1")
        outputs_path = logger._outputs_path("conv-1")

        assert inputs_path.exists()
        assert outputs_path.exists()

        logger.delete("conv-1")

        assert not inputs_path.exists()
        assert not outputs_path.exists()

    def test_delete_nonexistent_no_error(self, tmp_path):
        """Delete non-existent conversation doesn't raise."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)

        # Should not raise
        logger.delete("nonexistent")


class TestConversationLoggerGetStats:
    """Tests for get_stats method."""

    def test_get_stats(self, tmp_path):
        """Get conversation statistics."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)
        logger.log_input("conv-1", "Hello")
        logger.log_input("conv-1", "How are you?")
        logger.log_output("conv-1", "I'm fine, thanks!", "model")

        stats = logger.get_stats("conv-1")
        assert stats["conversation_id"] == "conv-1"
        assert stats["input_count"] == 2
        assert stats["output_count"] == 1
        assert stats["total_input_tokens"] > 0
        assert stats["total_output_tokens"] > 0
        assert stats["total_tokens"] == stats["total_input_tokens"] + stats["total_output_tokens"]

    def test_get_stats_empty_conversation(self, tmp_path):
        """Get stats for empty conversation."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)

        stats = logger.get_stats("nonexistent")
        assert stats["input_count"] == 0
        assert stats["output_count"] == 0
        assert stats["total_tokens"] == 0


class TestConversationLoggerPrivateMethods:
    """Tests for private methods."""

    def test_inputs_path(self, tmp_path):
        """_inputs_path returns correct path."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)
        path = logger._inputs_path("conv-1")

        assert path == tmp_path / "conv-1_inputs.json"

    def test_outputs_path(self, tmp_path):
        """_outputs_path returns correct path."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)
        path = logger._outputs_path("conv-1")

        assert path == tmp_path / "conv-1_outputs.json"

    def test_load_log_nonexistent(self, tmp_path):
        """_load_log returns empty list for non-existent file."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)
        result = logger._load_log(tmp_path / "nonexistent.json")

        assert result == []

    def test_save_log(self, tmp_path):
        """_save_log saves entries."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)
        path = tmp_path / "test.json"
        entries = [{"content": "test"}]

        logger._save_log(path, entries)

        assert path.exists()
        loaded = json.loads(path.read_text())
        assert loaded == entries


class TestGlobalConversationLogger:
    """Tests for global conversation_logger instance."""

    def test_global_instance_exists(self):
        """Global instance exists."""
        from backend.conversation_logger import conversation_logger

        assert conversation_logger is not None

    def test_global_instance_is_logger(self):
        """Global instance is ConversationLogger."""
        from backend.conversation_logger import conversation_logger, ConversationLogger

        assert isinstance(conversation_logger, ConversationLogger)
