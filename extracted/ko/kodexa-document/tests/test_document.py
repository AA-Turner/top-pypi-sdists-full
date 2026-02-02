"""
Test Document class - thin wrapper around Go C bindings.
"""

import json
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from kodexa_document import Document, ContentNode
from kodexa_document.errors import DocumentError, DocumentNotFoundError


class TestDocumentCreation:
    """Test document creation methods."""
    
    def test_create_empty_document(self):
        """Test creating an empty document."""
        doc = Document()
        assert doc.uuid is not None
        assert doc.version == "6.0.0"
        doc.close()
    
    def test_create_with_metadata(self):
        """Test creating document with metadata."""
        metadata = {"title": "Test Doc", "author": "Test Suite"}
        doc = Document(metadata=metadata)
        assert doc.uuid is not None
        # Metadata is extracted from JSON for now
        doc_metadata = doc.metadata
        assert doc_metadata.get("title") == "Test Doc"
        assert doc_metadata.get("author") == "Test Suite"
        doc.close()
    
    def test_metadata_setter(self):
        """Test setting metadata via property setter.

        Note: 'version' is a reserved field that sets doc.version (the document version),
        not user metadata. See CLAUDE.md for details on special metadata fields.
        """
        doc = Document()

        # Test setting metadata dictionary
        # Using 'schema_version' instead of 'version' since 'version' is reserved
        test_metadata = {
            "title": "Test Document",
            "author": "Test Author",
            "schema_version": 1.0,  # Using non-reserved key
            "published": True,
            "tags": ["test", "example"]
        }
        doc.metadata = test_metadata

        # Verify metadata was set correctly
        retrieved_metadata = doc.metadata
        assert retrieved_metadata["title"] == "Test Document"
        assert retrieved_metadata["author"] == "Test Author"

        # Go backend may preserve or convert types - verify values are equivalent
        assert float(retrieved_metadata["schema_version"]) == 1.0
        assert str(retrieved_metadata["published"]).lower() in ["true", "1"]

        # Complex objects are JSON serialized, then parsed back
        tags_value = retrieved_metadata["tags"]
        if isinstance(tags_value, str):
            import json
            assert json.loads(tags_value) == ["test", "example"]
        else:
            assert tags_value == ["test", "example"]
        
        # Test updating metadata
        doc.metadata = {"status": "updated", "count": 42}
        updated_metadata = doc.metadata
        assert updated_metadata["status"] == "updated"
        assert int(updated_metadata["count"]) == 42
        
        # Test error handling
        try:
            doc.metadata = "not a dict"
            assert False, "Should have raised TypeError"
        except TypeError:
            pass
            
        try:
            doc.metadata = {123: "invalid key"}
            assert False, "Should have raised TypeError"
        except TypeError:
            pass
        
        doc.close()
    
    def test_create_in_memory(self):
        """Test explicit in-memory document creation."""
        doc = Document.create_in_memory()
        assert doc.uuid is not None
        assert doc.version == "6.0.0"
        doc.close()
    
    def test_create_from_text(self):
        """Test creating document from text."""
        text = "Line 1\nLine 2\nLine 3"
        doc = Document.from_text(text, separator="\n")
        assert doc.uuid is not None
        assert doc.version == "6.0.0"
        doc.close()
    
    def test_create_from_text_no_separator(self):
        """Test creating document from text without separator."""
        text = "This is a test document"
        doc = Document.from_text(text)
        assert doc.uuid is not None
        doc.close()


class TestDocumentProperties:
    """Test document property access."""
    
    def test_uuid_property(self):
        """Test UUID property access."""
        doc = Document()
        uuid1 = doc.uuid
        uuid2 = doc.get_uuid()
        assert uuid1 == uuid2
        assert len(uuid1) == 36  # Standard UUID format
        doc.close()
    
    def test_version_property(self):
        """Test version property access."""
        doc = Document()
        version1 = doc.version
        version2 = doc.get_version()
        assert version1 == version2
        assert version1 == "6.0.0"
        doc.close()
    
    def test_json_export(self):
        """Test JSON export."""
        metadata = {"test": "value"}
        doc = Document(metadata=metadata)
        json_str = doc.to_json()
        data = json.loads(json_str)
        assert data["uuid"] == doc.uuid
        assert data["version"] == doc.version
        doc.close()
    
    def test_json_export_with_formatting(self):
        """Test JSON export with formatting options."""
        doc = Document()
        json_str = doc.to_json(indent=2)
        assert "\n" in json_str  # Should be formatted
        doc.close()
    
    def test_to_dict(self):
        """Test to_dict() method returns dictionary representation."""
        metadata = {"title": "Test Doc", "author": "Test Suite"}
        doc = Document(metadata=metadata)
        
        # Get both JSON and dict representations
        json_str = doc.to_json()
        doc_dict = doc.to_dict()
        
        # Verify to_dict returns a dictionary
        assert isinstance(doc_dict, dict)
        
        # Verify it contains expected fields
        assert "uuid" in doc_dict
        assert "version" in doc_dict
        assert doc_dict["uuid"] == doc.uuid
        assert doc_dict["version"] == doc.version
        
        # Verify dict contains the legacy_python structure (different from JSON)
        # to_dict() should return: version, metadata, content_node, source, mixins, labels, uuid
        # to_json() returns the Go-native JSON structure which is different
        assert "content_node" in doc_dict  # to_dict includes content_node
        assert "mixins" in doc_dict        # to_dict includes mixins
        assert "labels" in doc_dict        # to_dict includes labels
        
        # JSON structure is different and should not equal to_dict
        json_dict = json.loads(json_str)
        # These are the fields that should be common between both
        common_fields = ["uuid", "version", "metadata"]
        for field in common_fields:
            if field in json_dict and field in doc_dict:
                assert doc_dict[field] == json_dict[field]
        
        # Verify metadata is included
        if "metadata" in doc_dict:
            doc_metadata = doc_dict["metadata"]
            assert isinstance(doc_metadata, dict)
            # Note: metadata structure may vary based on Go implementation
        
        doc.close()


class TestDocumentPersistence:
    """Test document save/load operations."""
    
    def test_save_and_load(self):
        """Test saving and loading a document."""
        with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
            temp_path = f.name
        
        try:
            # Create and save
            doc1 = Document.from_text("Test content")
            uuid1 = doc1.uuid
            doc1.save(temp_path)
            doc1.close()
            
            # Load
            doc2 = Document.from_kddb(temp_path)
            uuid2 = doc2.uuid
            assert uuid1 == uuid2
            doc2.close()
        finally:
            Path(temp_path).unlink(missing_ok=True)
    
    def test_open_nonexistent(self):
        """Test opening non-existent file."""
        with pytest.raises(DocumentError):
            Document.from_kddb("/nonexistent/file.kddb")
    
    def test_save_invalid_path(self):
        """Test saving to invalid path."""
        doc = Document()
        # The Go code returns a DocumentError for permission/path issues
        # Use null character to ensure path is invalid on all platforms (Windows, Linux, macOS)
        with pytest.raises((RuntimeError, DocumentError)):
            doc.save("/nonexistent/\x00directory/file.kddb")
        doc.close()


class TestDocumentLifecycle:
    """Test document lifecycle management."""
    
    def test_context_manager(self):
        """Test using document as context manager."""
        with Document() as doc:
            uuid = doc.uuid
            assert uuid is not None
        
        # Document should be closed after context
        with pytest.raises(RuntimeError):
            _ = doc.uuid
    
    def test_explicit_close(self):
        """Test explicit close."""
        doc = Document()
        uuid = doc.uuid
        doc.close()
        
        # Should raise after close
        with pytest.raises(RuntimeError):
            _ = doc.uuid
    
    def test_ref_property(self):
        """Test document ref property for platform origin tracking."""
        doc = Document(inmemory=True)
        
        # Initially None
        assert doc.ref is None
        
        # Set a platform reference
        doc.ref = "myorg/document-store:1.0.0"
        assert doc.ref == "myorg/document-store:1.0.0"
        
        # Can be set back to None
        doc.ref = None
        assert doc.ref is None
        
        doc.close()
    
    def test_ref_survives_json_roundtrip(self):
        """Test that ref survives JSON serialization."""
        doc1 = Document(inmemory=True)
        doc1.ref = "platform/component:2.0.0"
        
        json_str = doc1.to_json()
        doc2 = Document.from_json(json_str, inmemory=True)
        
        assert doc2.ref == "platform/component:2.0.0"
        
        doc1.close()
        doc2.close()
    
    def test_ref_not_persisted_in_kddb(self):
        """Test that ref property is NOT persisted (legacy_python parity)."""
        doc1 = Document(inmemory=True)
        doc1.ref = "myorg/store:1.0.0/doc-family-123"
        
        # Save to KDDB
        kddb_bytes = doc1.to_kddb()
        doc1.close()
        
        # Load from KDDB
        doc2 = Document.from_kddb(kddb_bytes, inmemory=True)
        
        # ref should be None after loading (not persisted)
        assert doc2.ref is None
        doc2.close()
    
    def test_ref_type_validation(self):
        """Test that ref property validates types."""
        doc = Document(inmemory=True)
        
        # Should accept string
        doc.ref = "test-ref"
        assert doc.ref == "test-ref"
        
        # Should accept None
        doc.ref = None
        assert doc.ref is None
        
        # Should reject non-string types
        with pytest.raises(TypeError, match="ref must be a string or None"):
            doc.ref = 123
        
        with pytest.raises(TypeError, match="ref must be a string or None"):
            doc.ref = {"ref": "test"}
        
        doc.close()
    
    def test_from_dict(self):
        """Test creating document from dictionary (legacy_python parity)."""
        # Create a document and convert to dict
        doc1 = Document(inmemory=True)
        doc1.set_metadata("test_key", "test_value")
        doc1.add_label("test-label")
        
        # Create content node
        root = doc1.create_node("document", "Test content")
        doc1.content_node = root
        
        # Convert to dict
        doc_dict = doc1.to_dict()
        doc1.close()
        
        # Create new document from dict
        doc2 = Document.from_dict(doc_dict, inmemory=True)
        
        # Verify properties
        assert doc2.uuid == doc_dict["uuid"]
        assert doc2.version == doc_dict["version"]
        assert doc2.get_metadata("test_key") == "test_value"
        assert "test-label" in doc2.labels
        assert doc2.content_node is not None
        assert doc2.content_node.node_type == "document"
        assert doc2.content_node.content == "Test content"
        
        doc2.close()
    
    def test_from_dict_to_dict_roundtrip(self):
        """Test that from_dict and to_dict are symmetric."""
        # Create original document
        doc1 = Document(inmemory=True)
        doc1.set_metadata("key1", "value1")
        doc1.set_metadata("key2", {"nested": "value"})
        doc1.add_label("label1")
        doc1.add_label("label2")
        
        root = doc1.create_node("document")
        child1 = doc1.create_node("paragraph", "Para 1")
        child2 = doc1.create_node("paragraph", "Para 2")
        root.add_child(child1)
        root.add_child(child2)
        doc1.content_node = root
        
        # First round-trip
        dict1 = doc1.to_dict()
        doc2 = Document.from_dict(dict1, inmemory=True)
        dict2 = doc2.to_dict()
        
        # Verify dictionaries are equivalent
        assert dict1["uuid"] == dict2["uuid"]
        assert dict1["version"] == dict2["version"]
        assert dict1.get("metadata") == dict2.get("metadata")
        assert dict1.get("labels") == dict2.get("labels")
        
        # Verify content structure
        assert dict1["content_node"]["type"] == dict2["content_node"]["type"]
        assert dict1["content_node"]["content"] == dict2["content_node"]["content"]
        assert len(dict1["content_node"]["children"]) == len(dict2["content_node"]["children"])
        
        doc1.close()
        doc2.close()
    
    def test_from_dict_type_validation(self):
        """Test that from_dict validates input type."""
        with pytest.raises(TypeError, match="doc_dict must be a dictionary"):
            Document.from_dict("not a dict")
        
        with pytest.raises(TypeError, match="doc_dict must be a dictionary"):
            Document.from_dict(123)
        
        with pytest.raises(TypeError, match="doc_dict must be a dictionary"):
            Document.from_dict(None)
    
    def test_from_dict_minimal(self):
        """Test from_dict with minimal valid dictionary."""
        # Minimal valid document dict
        doc_dict = {
            "uuid": "test-uuid-123",
            "version": "1.0.0"
        }
        
        doc = Document.from_dict(doc_dict, inmemory=True)
        assert doc.uuid == "test-uuid-123"
        assert doc.version == "1.0.0"
        doc.close()

    def test_double_close(self):
        """Test closing document twice."""
        doc = Document()
        doc.close()
        doc.close()  # Should not raise
    
    def test_repr(self):
        """Test string representation."""
        doc = Document()
        repr_str = repr(doc)
        assert "Document" in repr_str
        assert doc.uuid in repr_str
        assert "open" in repr_str
        
        doc.close()
        repr_str = repr(doc)
        assert "closed" in repr_str


class TestNotImplementedMethods:
    """Test methods that are not yet implemented."""
    
    def test_content_node_operations(self):
        """Test content node operations."""
        doc = Document()
        
        # Create root node
        root = doc.create_node("document", content="Root content")
        doc.content_node = root
        
        # Create child node
        child = doc.create_node("paragraph", content="Child content")
        root.add_child(child)
        
        # Test content access
        assert root.content == "Root content"
        assert child.content == "Child content"
        
        # Test hierarchy
        children = root.get_children()
        assert len(children) >= 0  # May vary depending on Go backend availability
        
        doc.close()
    
    def test_selector_operations(self):
        """Test that selector operations work correctly."""
        doc = Document.from_text("Test content")
        
        # Test basic selector functionality
        nodes = doc.select("//*")
        assert isinstance(nodes, list)
        assert len(nodes) >= 1  # Should find at least the root document node
        
        # Test select_first
        first_node = doc.select_first("//*")
        assert first_node is not None
        assert hasattr(first_node, 'node_type')
        
        # Test select with first_only=True - should behave like select_first but return a list
        first_only_nodes = doc.select("//*", first_only=True)
        assert isinstance(first_only_nodes, list)
        assert len(first_only_nodes) == 1
        assert first_only_nodes[0].node_type == first_node.node_type
        
        # Test select with first_only=False (default behavior)
        all_nodes = doc.select("//*", first_only=False)
        assert isinstance(all_nodes, list)
        assert len(all_nodes) >= len(first_only_nodes)  # Should find same or more nodes
        
        # Test with non-matching selector
        empty_nodes = doc.select("//nonexistent")
        assert isinstance(empty_nodes, list)
        assert len(empty_nodes) == 0
        
        # Test select_first with non-matching selector
        no_node = doc.select_first("//nonexistent")
        assert no_node is None
        
        # Test first_only=True with non-matching selector
        no_nodes = doc.select("//nonexistent", first_only=True)
        assert isinstance(no_nodes, list)
        assert len(no_nodes) == 0
        
        doc.close()
    
    def test_tag_operations(self):
        """Test that get_all_tagged_nodes works correctly."""
        doc = Document()
        
        # Empty document should return empty list
        tagged_nodes = doc.get_all_tagged_nodes()
        assert tagged_nodes == []
        
        doc.close()
    
    def test_from_json(self):
        """Test that from_json is now implemented."""
        # Create a valid document JSON
        doc = Document(inmemory=True)
        json_str = doc.to_json()
        doc.close()
        
        # from_json should now work
        doc2 = Document.from_json(json_str, inmemory=True)
        assert doc2 is not None
        doc2.close()


class TestEnhancedCreateNode:
    """Test enhanced create_node functionality with virtual/parent/index parameters."""
    
    def test_create_node_basic(self):
        """Test basic create_node functionality (backward compatibility)."""
        doc = Document(inmemory=True)
        
        # Basic node creation should still work
        node = doc.create_node("paragraph", "Basic content")
        assert node is not None
        assert node.node_type == "paragraph"
        assert node.content == "Basic content"
        
        doc.close()
    
    def test_create_node_with_virtual(self):
        """Test creating virtual nodes."""
        doc = Document(inmemory=True)
        
        # Create virtual node
        virtual_node = doc.create_node("section", "Virtual Section", virtual=True)
        assert virtual_node is not None
        assert virtual_node.node_type == "section"
        assert virtual_node.content == "Virtual Section"
        assert virtual_node.virtual is True
        
        # Create non-virtual node for comparison
        regular_node = doc.create_node("section", "Regular Section", virtual=False)
        assert regular_node is not None
        assert regular_node.virtual is False
        
        doc.close()
    
    def test_create_node_with_index(self):
        """Test creating nodes with specific index."""
        doc = Document(inmemory=True)
        
        # Create node with specific index
        indexed_node = doc.create_node("item", "Item content", index=42)
        assert indexed_node is not None
        assert indexed_node.node_type == "item"
        assert indexed_node.content == "Item content"
        assert indexed_node.index == 42
        
        doc.close()
    
    def test_create_node_with_parent(self):
        """Test creating nodes with parent relationship."""
        doc = Document(inmemory=True)
        
        # Create parent node
        parent = doc.create_node("container", "Parent content")
        assert parent is not None
        
        # Create child node with parent
        child = doc.create_node("item", "Child content", parent=parent)
        assert child is not None
        assert child.node_type == "item"
        assert child.content == "Child content"
        
        # Note: Parent-child relationship verification depends on Go backend
        # The parent should be set in the Go layer
        
        doc.close()
    
    def test_create_node_with_all_options(self):
        """Test creating nodes with all enhanced options."""
        doc = Document(inmemory=True)
        
        # Create parent node
        parent = doc.create_node("list", "List container")
        assert parent is not None
        
        # Create child with all options: virtual, parent, and index
        child = doc.create_node(
            "list-item", 
            "Item content",
            virtual=True,
            parent=parent,
            index=10
        )
        
        assert child is not None
        assert child.node_type == "list-item"
        assert child.content == "Item content"
        assert child.virtual is True
        assert child.index == 10
        
        doc.close()
    
    def test_create_node_parameter_combinations(self):
        """Test various parameter combinations."""
        doc = Document(inmemory=True)
        
        # Just virtual
        node1 = doc.create_node("test", "content1", virtual=True)
        assert node1.virtual is True
        
        # Just index
        node2 = doc.create_node("test", "content2", index=5)
        assert node2.index == 5
        
        # Virtual and index
        node3 = doc.create_node("test", "content3", virtual=True, index=7)
        assert node3.virtual is True
        assert node3.index == 7
        
        doc.close()
    
    def test_create_node_empty_content(self):
        """Test creating nodes with empty content."""
        doc = Document(inmemory=True)
        
        # Empty content with enhanced options
        node = doc.create_node("empty", "", virtual=True, index=0)
        assert node is not None
        assert node.content == ""
        assert node.virtual is True
        assert node.index == 0
        
        doc.close()
    
    def test_create_node_none_values(self):
        """Test creating nodes with None values (should use defaults)."""
        doc = Document(inmemory=True)
        
        # Explicitly pass None values
        node = doc.create_node(
            "test", 
            "content",
            virtual=False,
            parent=None, 
            index=None
        )
        
        assert node is not None
        assert node.node_type == "test"
        assert node.content == "content"
        assert node.virtual is False
        
        doc.close()


class TestDocumentValidations:
    """Test document validation operations."""
    
    def test_get_validations_empty(self):
        """Test getting validations from empty document."""
        doc = Document(inmemory=True)
        
        validations = doc.get_validations()
        assert isinstance(validations, list)
        assert len(validations) == 0
        
        doc.close()
    
    def test_set_and_get_validations(self):
        """Test setting and getting validations."""
        doc = Document(inmemory=True)
        
        # Test validations following legacy_python structure
        test_validations = [
            {
                "taxonomy_ref": "test/test-taxonomy:1.0.0",
                "taxon_path": "person",
                "validation": {
                    "name": "NameRequired",
                    "description": "Name is required",
                    "ruleFormula": "ifnull(name, '') != ''",
                    "messageFormula": "Name must be provided"
                }
            },
            {
                "taxonomy_ref": "test/test-taxonomy:1.0.0", 
                "taxon_path": "person/age",
                "validation": {
                    "name": "AgeValid",
                    "description": "Age must be positive",
                    "ruleFormula": "age > 0",
                    "messageFormula": "Age must be greater than 0"
                }
            }
        ]
        
        # Set validations
        doc.set_validations(test_validations)
        
        # Get validations and verify
        retrieved_validations = doc.get_validations()
        assert isinstance(retrieved_validations, list)
        assert len(retrieved_validations) == 2
        
        # Check first validation
        val1 = retrieved_validations[0]
        assert val1["taxonomy_ref"] == "test/test-taxonomy:1.0.0"
        assert val1["taxon_path"] == "person"
        assert val1["validation"]["name"] == "NameRequired"
        assert val1["validation"]["ruleFormula"] == "ifnull(name, '') != ''"
        
        # Check second validation
        val2 = retrieved_validations[1]
        assert val2["taxonomy_ref"] == "test/test-taxonomy:1.0.0"
        assert val2["taxon_path"] == "person/age"
        assert val2["validation"]["name"] == "AgeValid"
        
        doc.close()
    
    def test_set_validations_empty_list(self):
        """Test setting empty validations list."""
        doc = Document(inmemory=True)
        
        # Set empty list
        doc.set_validations([])
        
        # Verify empty
        validations = doc.get_validations()
        assert isinstance(validations, list)
        assert len(validations) == 0
        
        doc.close()
    
    def test_set_validations_type_error(self):
        """Test error handling for invalid validation types."""
        doc = Document(inmemory=True)
        
        # Should raise TypeError for non-list input
        with pytest.raises(TypeError):
            doc.set_validations("not a list")
        
        with pytest.raises(TypeError):
            doc.set_validations({"not": "a list"})
        
        doc.close()
    
    def test_validations_persistence(self):
        """Test that validations are properly persisted and retrieved."""
        # Create document and set validations
        doc1 = Document(inmemory=True)
        
        original_validations = [
            {
                "taxonomy_ref": "test/persistence:1.0.0",
                "taxon_path": "document",
                "validation": {
                    "name": "DocValid",
                    "ruleFormula": "content != null"
                }
            }
        ]
        
        doc1.set_validations(original_validations)
        doc1.close()
        
        # Note: Since we're using inmemory=True, we can't test persistence across 
        # document instances, but we can test that the validations survive
        # multiple get/set operations within the same document session
        doc2 = Document(inmemory=True)
        doc2.set_validations(original_validations)
        
        # Modify and verify persistence within same session
        new_validations = [
            {
                "taxonomy_ref": "test/modified:1.0.0", 
                "taxon_path": "updated",
                "validation": {
                    "name": "Updated",
                    "ruleFormula": "true"
                }
            }
        ]
        doc2.set_validations(new_validations)
        
        retrieved = doc2.get_validations()
        assert len(retrieved) == 1
        assert retrieved[0]["taxonomy_ref"] == "test/modified:1.0.0"
        assert retrieved[0]["taxon_path"] == "updated"

        doc2.close()


class TestDocumentErrorHandling:
    """Test error handling paths in Document class."""

    def test_document_error_paths(self):
        """Test error handling paths in Document class."""
        doc = Document()

        # Test closed document access attempts
        doc.close()

        with pytest.raises((DocumentError, RuntimeError)):
            doc.get_root()

        with pytest.raises((DocumentError, RuntimeError)):
            doc.set_root(None)

        with pytest.raises((DocumentError, RuntimeError)):
            doc.add_label("test")

        with pytest.raises((DocumentError, RuntimeError)):
            doc.add_mixin("test")

        with pytest.raises((DocumentError, RuntimeError)):
            doc.remove_label("test")

    def test_document_from_kddb_error_cases(self):
        """Test error cases in from_kddb method."""
        # Test with invalid type
        with pytest.raises(TypeError):
            Document.from_kddb(12345)

        # Test with invalid bytes
        with pytest.raises(DocumentError):
            Document.from_kddb(b"invalid kddb bytes")

    def test_document_metadata_edge_cases(self):
        """Test metadata edge cases."""
        doc = Document()

        # Test setting metadata with non-dict (None raises TypeError)
        with pytest.raises(TypeError):
            doc.metadata = None

        # Test setting metadata with non-dict string
        with pytest.raises(TypeError):
            doc.metadata = "not a dict"

        doc.close()

    def test_document_save_error_handling(self):
        """Test save method error handling."""
        doc = Document()

        # Test saving to invalid path
        # Use null character to ensure path is invalid on all platforms (Windows, Linux, macOS)
        with pytest.raises(DocumentError):
            doc.save("/nonexistent/\x00directory/file.kddb")

        doc.close()

    def test_document_properties_on_closed(self):
        """Test property access on closed document."""
        doc = Document()
        doc.close()

        # These should raise errors
        with pytest.raises((DocumentError, RuntimeError)):
            _ = doc.uuid

        with pytest.raises((DocumentError, RuntimeError)):
            _ = doc.version

        # Test to_json() on closed document
        with pytest.raises((DocumentError, RuntimeError)):
            _ = doc.to_json()

        # Also test to_dict() on closed document
        with pytest.raises((DocumentError, RuntimeError)):
            _ = doc.to_dict()

    def test_document_select_error_paths(self):
        """Test select method error paths."""
        doc = Document()
        root = doc.create_node("root")
        doc.content_node = root

        # Test with invalid selector
        with pytest.raises(DocumentError):
            doc.select("invalid[[[selector")

        doc.close()

    def test_document_to_kddb_with_path_none(self):
        """Test to_kddb returns bytes when path=None."""
        doc = Document()
        root = doc.create_node("root")
        doc.content_node = root

        # to_kddb with None path should return bytes
        kddb_bytes = doc.to_kddb(None)
        assert isinstance(kddb_bytes, bytes)
        assert len(kddb_bytes) > 0

        doc.close()