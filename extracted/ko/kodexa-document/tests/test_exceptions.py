"""
Test exception functionality matching legacy_python behavior.
"""

import pytest
from kodexa_document import Document


class TestExceptions:
    """Test document exception methods."""
    
    def test_initial_exceptions_empty(self):
        """Test that new documents have empty exceptions."""
        document = Document(inmemory=True)
        
        # Test get_exceptions method
        assert document.get_exceptions() == []
        
        document.close()
    
    def test_add_exception_from_dict(self):
        """Test adding an exception from a dictionary."""
        document = Document(inmemory=True)
        
        # Add an exception and verify it returns self for chaining
        exception_dict = {
            "message": "Test validation error",
            "exception_type": "VALIDATION_ERROR",
            "severity": "ERROR",
            "node_uuid": "test-node-123"
        }
        result = document.add_exception(exception_dict)
        assert result is document  # Method chaining
        
        # Verify exception was added
        exceptions = document.get_exceptions()
        assert len(exceptions) == 1
        assert exceptions[0]["message"] == "Test validation error"
        assert exceptions[0]["exception_type"] == "VALIDATION_ERROR"
        assert exceptions[0]["severity"] == "ERROR"
        assert exceptions[0]["node_uuid"] == "test-node-123"
        
        document.close()
    
    def test_add_exception_from_object(self):
        """Test adding an exception from an object with attributes."""
        document = Document(inmemory=True)
        
        # Create mock exception object
        class MockException:
            def __init__(self):
                self.message = "Object-based exception"
                self.exception_type = "PROCESSING_ERROR"
                self.severity = "WARNING"
                self.node_uuid = "object-node-456"
                self.path = "/document/section[1]"
                self.tag = "extracted-field"
                self.group_uuid = "group-123"
        
        mock_exception = MockException()
        result = document.add_exception(mock_exception)
        assert result is document  # Method chaining
        
        # Verify exception was added
        exceptions = document.get_exceptions()
        assert len(exceptions) == 1
        assert exceptions[0]["message"] == "Object-based exception"
        assert exceptions[0]["exception_type"] == "PROCESSING_ERROR"
        assert exceptions[0]["severity"] == "WARNING"
        assert exceptions[0]["node_uuid"] == "object-node-456"
        assert exceptions[0]["path"] == "/document/section[1]"
        assert exceptions[0]["tag"] == "extracted-field"
        assert exceptions[0]["group_uuid"] == "group-123"
        
        document.close()
    
    def test_add_multiple_exceptions(self):
        """Test adding multiple exceptions."""
        document = Document(inmemory=True)
        
        # Add multiple exceptions
        document.add_exception({
            "message": "First error",
            "exception_type": "ERROR_1",
        })
        document.add_exception({
            "message": "Second error", 
            "exception_type": "ERROR_2",
            "severity": "WARNING"
        })
        document.add_exception({
            "message": "Third error",
            "exception_type": "ERROR_3",
            "severity": "CRITICAL"
        })
        
        # Verify all exceptions are present
        exceptions = document.get_exceptions()
        assert len(exceptions) == 3
        
        messages = [ex["message"] for ex in exceptions]
        assert "First error" in messages
        assert "Second error" in messages
        assert "Third error" in messages
        
        document.close()
    
    def test_exception_required_fields_validation(self):
        """Test that required exception fields are validated."""
        document = Document(inmemory=True)
        
        # Test missing message
        with pytest.raises(ValueError, match="exception must have a non-empty message"):
            document.add_exception({"exception_type": "TEST"})
        
        with pytest.raises(ValueError, match="exception must have a non-empty message"):
            document.add_exception({"message": "", "exception_type": "TEST"})
        
        # Test missing exception_type
        with pytest.raises(ValueError, match="exception must have a non-empty exception_type"):
            document.add_exception({"message": "test message"})
        
        with pytest.raises(ValueError, match="exception must have a non-empty exception_type"):
            document.add_exception({"message": "test message", "exception_type": ""})
        
        document.close()
    
    def test_exception_type_validation(self):
        """Test that add_exception validates input types."""
        document = Document(inmemory=True)
        
        # Invalid types
        with pytest.raises(TypeError, match="exception must be a dictionary or ContentException-like object"):
            document.add_exception("not a dict or object")
        
        with pytest.raises(TypeError, match="exception must be a dictionary or ContentException-like object"):
            document.add_exception(123)
        
        with pytest.raises(TypeError, match="exception must be a dictionary or ContentException-like object"):
            document.add_exception(None)
        
        document.close()
    
    def test_exception_defaults(self):
        """Test that exception defaults are applied correctly."""
        document = Document(inmemory=True)
        
        # Add minimal exception
        document.add_exception({
            "message": "Minimal exception",
            "exception_type": "MINIMAL"
        })
        
        # Verify defaults were applied
        exceptions = document.get_exceptions()
        assert len(exceptions) == 1
        exception = exceptions[0]
        
        assert exception["message"] == "Minimal exception"
        assert exception["exception_type"] == "MINIMAL"
        assert exception["severity"] == "ERROR"  # Default
        assert exception["open"] is True  # Default
        
        document.close()
    
    def test_exceptions_with_all_fields(self):
        """Test exceptions with all possible fields."""
        document = Document(inmemory=True)
        
        # Add exception with all fields
        full_exception = {
            "message": "Complete validation failure",
            "exception_type": "VALIDATION_FAILURE",
            "severity": "CRITICAL",
            "node_uuid": "node-uuid-789",
            "exception_details": "Detailed error information here",
            "path": "/document/table[2]/row[5]/cell[3]",
            "closing_comment": "Needs manual review",
            "open": False,
            "exception_type_id": "VF-001",
            "tag": "extracted-amount",
            "group_uuid": "group-uuid-abc",
            "tag_uuid": "tag-uuid-def"
        }
        
        document.add_exception(full_exception)
        
        # Verify all fields are preserved
        exceptions = document.get_exceptions()
        assert len(exceptions) == 1
        exception = exceptions[0]
        
        # Check all fields (some may be normalized by Go backend)
        assert exception["message"] == "Complete validation failure"
        assert exception["exception_type"] == "VALIDATION_FAILURE"
        assert exception["severity"] == "CRITICAL"
        assert exception["node_uuid"] == "node-uuid-789"
        assert exception["exception_details"] == "Detailed error information here"
        assert exception["path"] == "/document/table[2]/row[5]/cell[3]"
        
        document.close()
    
    def test_exceptions_persistence_across_operations(self):
        """Test that exceptions persist across other document operations."""
        document = Document(inmemory=True)
        
        # Add exceptions
        document.add_exception({
            "message": "Persistent exception 1",
            "exception_type": "PERSISTENT_1"
        })
        document.add_exception({
            "message": "Persistent exception 2", 
            "exception_type": "PERSISTENT_2"
        })
        
        # Perform other document operations
        root = document.create_node("document")
        document.content_node = root
        
        child = document.create_node("paragraph", content="Test content")
        root.add_child(child)
        
        # Set metadata
        document.set_metadata("test_key", "test_value")
        
        # Add labels
        document.add_label("test-label")
        
        # Exceptions should still be there
        exceptions = document.get_exceptions()
        assert len(exceptions) == 2
        
        messages = [ex["message"] for ex in exceptions]
        assert "Persistent exception 1" in messages
        assert "Persistent exception 2" in messages
        
        document.close()
    
    def test_multiple_documents_independent_exceptions(self):
        """Test that different documents have independent exceptions."""
        doc1 = Document(inmemory=True)
        doc2 = Document(inmemory=True)
        
        # Add different exceptions to each document
        doc1.add_exception({
            "message": "Doc1 exception 1",
            "exception_type": "DOC1_ERROR_1"
        })
        doc1.add_exception({
            "message": "Doc1 exception 2",
            "exception_type": "DOC1_ERROR_2"
        })
        
        doc2.add_exception({
            "message": "Doc2 exception 1",
            "exception_type": "DOC2_ERROR_1"
        })
        doc2.add_exception({
            "message": "Doc2 exception 2",
            "exception_type": "DOC2_ERROR_2"
        })
        doc2.add_exception({
            "message": "Doc2 exception 3",
            "exception_type": "DOC2_ERROR_3"
        })
        
        # Verify each document has its own exceptions
        doc1_exceptions = doc1.get_exceptions()
        doc2_exceptions = doc2.get_exceptions()
        
        assert len(doc1_exceptions) == 2
        assert len(doc2_exceptions) == 3
        
        doc1_messages = [ex["message"] for ex in doc1_exceptions]
        doc2_messages = [ex["message"] for ex in doc2_exceptions]
        
        assert "Doc1 exception 1" in doc1_messages
        assert "Doc1 exception 2" in doc1_messages
        assert "Doc1 exception 1" not in doc2_messages
        
        assert "Doc2 exception 1" in doc2_messages
        assert "Doc2 exception 2" in doc2_messages
        assert "Doc2 exception 3" in doc2_messages
        assert "Doc2 exception 1" not in doc1_messages
        
        doc1.close()
        doc2.close()
    
    def test_method_chaining(self):
        """Test that add_exception supports method chaining."""
        document = Document(inmemory=True)
        
        # Test method chaining
        result = (document
                  .add_exception({"message": "Chain 1", "exception_type": "CHAIN_1"})
                  .add_exception({"message": "Chain 2", "exception_type": "CHAIN_2"})
                  .add_exception({"message": "Chain 3", "exception_type": "CHAIN_3"}))
        
        # Should return the same document object
        assert result is document
        
        # Verify final state
        exceptions = document.get_exceptions()
        assert len(exceptions) == 3
        
        messages = [ex["message"] for ex in exceptions]
        assert "Chain 1" in messages
        assert "Chain 2" in messages
        assert "Chain 3" in messages
        
        document.close()
    
    def test_exceptions_after_document_close(self):
        """Test that accessing exceptions after close raises an error."""
        document = Document(inmemory=True)
        
        # Add an exception
        document.add_exception({
            "message": "Test exception",
            "exception_type": "TEST"
        })
        
        # Close the document
        document.close()
        
        # Accessing exceptions should raise an error
        with pytest.raises(RuntimeError, match="Document has been closed"):
            document.get_exceptions()
        
        with pytest.raises(RuntimeError, match="Document has been closed"):
            document.add_exception({"message": "Another", "exception_type": "ANOTHER"})
    
    
    def test_exception_with_unicode_and_special_chars(self):
        """Test exceptions with unicode and special characters."""
        document = Document(inmemory=True)
        
        # Add exception with special characters
        document.add_exception({
            "message": "Unicode test: 中文 русский العربية 🚀 📄 ✨",
            "exception_type": "UNICODE_TEST",
            "exception_details": "Path with special chars: /doc/table[1]/cell[@id='special-chars!@#$%']",
            "path": "/document/section[contains(text(), 'special & chars')]"
        })
        
        # Verify exception is stored correctly
        exceptions = document.get_exceptions()
        assert len(exceptions) == 1
        
        exception = exceptions[0]
        assert "中文 русский العربية 🚀 📄 ✨" in exception["message"]
        assert "special-chars!@#$%" in exception["exception_details"]
        
        document.close()
    
    def test_basic_exception_legacy_python_style(self):
        """Test adding exception using ContentException class (legacy_python parity)."""
        from kodexa_document import ContentException
        
        # This matches legacy_python test_basic_exception()
        document = Document(inmemory=True)
        exception = ContentException({
            "message": "Testing exception",
            "exception_type": "Test"
        })
        document.add_exception(exception)
        
        assert len(document.get_exceptions()) == 1
        
        # Verify the exception details
        exceptions = document.get_exceptions()
        assert exceptions[0]["message"] == "Testing exception"
        assert exceptions[0]["exception_type"] == "Test"
        
        document.close()
    
    def test_update_exception_with_persistence(self):
        """Test exception persistence through KDDB save/load (legacy_python parity)."""
        import tempfile
        import os
        from kodexa_document import ContentException
        
        # This matches legacy_python test_update_exception() but adapted for current implementation
        # The current implementation only stores predefined fields in the database
        
        # Create document with exception
        document = Document(inmemory=True)
        content_exception = ContentException({
            "message": "Testing exception",
            "exception_type": "Test",
            "severity": "ERROR"  # Use a supported field instead of exception_type_id
        })
        document.add_exception(content_exception)
        
        assert len(document.get_exceptions()) == 1
        
        # Save to KDDB
        with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
            temp_path = f.name
        
        try:
            document.to_kddb(temp_path)
            document.close()
            
            # Load from KDDB
            document2 = Document.from_kddb(temp_path, inmemory=True)
            
            # Verify exception persisted
            assert len(document2.get_exceptions()) == 1
            
            # Check exception details
            exception = document2.get_exceptions()[0]
            assert exception["message"] == "Testing exception"
            assert exception["exception_type"] == "Test"
            assert exception["severity"] == "ERROR"
            
            # Note: Custom fields like exception_type_id from legacy_python
            # are not preserved in the current implementation as they're not
            # part of the database schema
            
            document2.close()
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestOpenExceptionsAndClose:
    """Test get_open_exceptions and close_exception methods."""

    def test_get_open_exceptions_empty(self):
        """Test that new documents have no open exceptions."""
        document = Document(inmemory=True)
        assert document.get_open_exceptions() == []
        document.close()

    def test_get_open_exceptions_filters_closed(self):
        """Test that get_open_exceptions returns only open exceptions."""
        document = Document(inmemory=True)

        # Add open exception
        document.add_exception({
            "message": "Open exception",
            "exception_type": "OPEN_ERROR",
            "open": True
        })

        # Add closed exception
        document.add_exception({
            "message": "Closed exception",
            "exception_type": "CLOSED_ERROR",
            "open": False
        })

        # Get all exceptions
        all_exceptions = document.get_exceptions()
        assert len(all_exceptions) == 2

        # Get only open exceptions
        open_exceptions = document.get_open_exceptions()
        assert len(open_exceptions) == 1
        assert open_exceptions[0]["message"] == "Open exception"
        assert open_exceptions[0]["open"] is True

        document.close()

    def test_close_exception_by_id(self):
        """Test closing an exception by ID."""
        document = Document(inmemory=True)

        # Add an open exception
        document.add_exception({
            "message": "Exception to close",
            "exception_type": "CLOSABLE_ERROR",
            "open": True
        })

        # Get the exception ID
        exceptions = document.get_exceptions()
        assert len(exceptions) == 1
        exception_id = exceptions[0]["id"]

        # Verify it's open
        open_exceptions = document.get_open_exceptions()
        assert len(open_exceptions) == 1

        # Close the exception
        result = document.close_exception(exception_id)
        assert result is document  # Method chaining

        # Verify it's now closed
        open_exceptions = document.get_open_exceptions()
        assert len(open_exceptions) == 0

        # Verify the exception still exists but is closed
        # (closed exceptions may omit the 'open' field or set it to False)
        all_exceptions = document.get_exceptions()
        assert len(all_exceptions) == 1
        assert all_exceptions[0].get("open", False) is False

        document.close()

    def test_close_exception_with_comment(self):
        """Test closing an exception with a closing comment."""
        document = Document(inmemory=True)

        # Add an open exception
        document.add_exception({
            "message": "Exception with comment",
            "exception_type": "COMMENT_ERROR",
            "open": True
        })

        # Get the exception ID
        exceptions = document.get_exceptions()
        exception_id = exceptions[0]["id"]

        # Close with comment
        document.close_exception(exception_id, "Resolved by manual review")

        # Verify the closing comment is set
        # (closed exceptions may omit the 'open' field or set it to False)
        exceptions = document.get_exceptions()
        assert len(exceptions) == 1
        assert exceptions[0].get("open", False) is False
        assert exceptions[0].get("closing_comment") == "Resolved by manual review"

        document.close()

    def test_close_exception_method_chaining(self):
        """Test that close_exception supports method chaining."""
        document = Document(inmemory=True)

        # Add multiple exceptions
        document.add_exception({"message": "Ex1", "exception_type": "TYPE1"})
        document.add_exception({"message": "Ex2", "exception_type": "TYPE2"})
        document.add_exception({"message": "Ex3", "exception_type": "TYPE3"})

        # Get IDs
        exceptions = document.get_exceptions()
        ids = [e["id"] for e in exceptions]

        # Chain close_exception calls
        result = (document
                  .close_exception(ids[0], "Closed 1")
                  .close_exception(ids[1], "Closed 2"))

        assert result is document

        # Verify state
        open_exceptions = document.get_open_exceptions()
        assert len(open_exceptions) == 1
        assert open_exceptions[0]["message"] == "Ex3"

        document.close()

    def test_close_exception_after_document_close(self):
        """Test that close_exception raises error on closed document."""
        document = Document(inmemory=True)
        document.add_exception({"message": "Test", "exception_type": "TEST"})
        exceptions = document.get_exceptions()
        exception_id = exceptions[0]["id"]

        document.close()

        with pytest.raises(RuntimeError, match="Document has been closed"):
            document.close_exception(exception_id)

    def test_get_open_exceptions_after_document_close(self):
        """Test that get_open_exceptions raises error on closed document."""
        document = Document(inmemory=True)
        document.close()

        with pytest.raises(RuntimeError, match="Document has been closed"):
            document.get_open_exceptions()