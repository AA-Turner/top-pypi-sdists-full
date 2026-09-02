"""Unit tests for LogEntry model (T037)."""

import pytest

from novita_sandbox.artifact_hosting.models.log_entry import LogEntry


class TestLogEntry:
    """T037: Test LogEntry model."""
    
    def test_from_dict_basic(self):
        """Should parse basic log entry data with 'line' field."""
        data = {"line": "Building image..."}
        
        log_entry = LogEntry.from_dict(data)
        
        assert log_entry.message == "Building image..."
    
    def test_from_dict_with_line_field(self):
        """Should parse API response that uses 'line' field."""
        data = {"line": "Step 1/7 : FROM ubuntu:22.04"}
        
        log_entry = LogEntry.from_dict(data)
        
        assert log_entry.message == "Step 1/7 : FROM ubuntu:22.04"
    
    def test_from_dict_with_message_field(self):
        """Should also accept 'message' field for backwards compatibility."""
        data = {"message": "Some log message"}
        
        log_entry = LogEntry.from_dict(data)
        
        assert log_entry.message == "Some log message"
    
    def test_from_dict_empty_data(self):
        """Should handle empty data gracefully."""
        data = {}
        
        log_entry = LogEntry.from_dict(data)
        
        assert log_entry.message == ""
    
    def test_to_dict_uses_line_field(self):
        """to_dict should use 'line' to match API format."""
        log_entry = LogEntry(message="Building image...")
        
        result = log_entry.to_dict()
        
        assert result["line"] == "Building image..."
        assert "message" not in result  # API uses 'line', not 'message'
    
    def test_str_representation(self):
        """Should have meaningful string representation."""
        log_entry = LogEntry(message="Starting nginx...")
        
        string_repr = str(log_entry)
        
        assert string_repr == "Starting nginx..."
    
    def test_str_representation_multiline(self):
        """String representation should handle multiline messages."""
        log_entry = LogEntry(message="Line 1\nLine 2")
        
        string_repr = str(log_entry)
        
        assert "Line 1" in string_repr
        assert "Line 2" in string_repr
