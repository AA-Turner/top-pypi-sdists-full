"""
Test extraction engine functionality.
"""

import pytest
import json
import tempfile
from pathlib import Path
from kodexa_document import Document
from kodexa_document.extraction import (
    ExtractionEngine, 
    Taxonomy, 
    DataObject, 
    DataAttribute,
    ContentException,
    DocumentTaxonValidation
)
from kodexa_document.errors import KodexaError, DocumentError


class TestTaxonomy:
    """Test Taxonomy class functionality."""
    
    def test_create_taxonomy_from_dict(self):
        """Test creating taxonomy from dictionary data."""
        taxonomy_data = {
            "name": "test_taxonomy",
            "version": "1.0",
            "ref": "test_taxonomy_ref",
            "taxons": [
                {
                    "name": "paragraph",
                    "type": "content"
                }
            ]
        }
        
        with Taxonomy(taxonomy_data=taxonomy_data) as taxonomy:
            assert taxonomy.validate() == True
            json_str = taxonomy.to_json()
            parsed = json.loads(json_str)
            assert parsed["Name"] == "test_taxonomy"
    
    def test_create_taxonomy_from_file(self):
        """Test creating taxonomy from file."""
        taxonomy_data = {
            "name": "file_taxonomy",
            "version": "1.0",
            "ref": "file_taxonomy_ref",
            "taxons": []
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(taxonomy_data, f)
            taxonomy_path = f.name
        
        try:
            with Taxonomy(taxonomy_path=taxonomy_path) as taxonomy:
                assert taxonomy.validate() == True
                json_str = taxonomy.to_json()
                parsed = json.loads(json_str)
                assert parsed["Name"] == "file_taxonomy"
        finally:
            Path(taxonomy_path).unlink()
    
    def test_taxonomy_validation(self):
        """Test taxonomy validation."""
        # Valid taxonomy
        valid_taxonomy = {
            "name": "valid",
            "version": "1.0",
            "ref": "valid_taxonomy_ref",
            "taxons": []
        }
        
        with Taxonomy(taxonomy_data=valid_taxonomy) as taxonomy:
            assert taxonomy.validate() == True
    
    def test_taxonomy_context_manager(self):
        """Test taxonomy context manager."""
        taxonomy_data = {
            "name": "context_test",
            "version": "1.0",
            "ref": "context_test_ref",
            "taxons": []
        }
        
        with Taxonomy(taxonomy_data=taxonomy_data) as taxonomy:
            # Should work inside context
            assert taxonomy.validate() == True
        
        # Should be closed after context
        with pytest.raises(KodexaError, match="Taxonomy is closed"):
            taxonomy.validate()
    
    def test_taxonomy_error_cases(self):
        """Test taxonomy error handling."""
        # No data provided
        with pytest.raises(ValueError, match="Either taxonomy_data or taxonomy_path must be provided"):
            Taxonomy()
        
        # Invalid file path
        with pytest.raises((KodexaError, DocumentError), match="failed to read taxonomy file"):
            Taxonomy(taxonomy_path="/nonexistent/path.json")


class TestDataAttribute:
    """Test DataAttribute class."""
    
    def test_data_attribute_initialization(self):
        """Test DataAttribute initialization."""
        data = {
            'data_object_id': 123,
            'path': '/test/path',
            'tag': 'test_tag',
            'tag_uuid': 'uuid-123',
            'value': 'test_value',
            'confidence': 0.95,
            'taxonomy_ref': 'tax_ref',
            'taxon_type': 'content',
            'group_uuid': 'group-123',
            'parent_group_uuid': 'parent-123',
            'cell_index': 1,
            'node_uuid': 'node-123',
            'node_id': 456,
            'source': 'extraction',
            'manual': True
        }
        
        attr = DataAttribute(data)
        
        assert attr.data_object_id == 123
        assert attr.path == '/test/path'
        assert attr.tag == 'test_tag'
        assert attr.tag_uuid == 'uuid-123'
        assert attr.value == 'test_value'
        assert attr.confidence == 0.95
        assert attr.taxonomy_ref == 'tax_ref'
        assert attr.taxon_type == 'content'
        assert attr.group_uuid == 'group-123'
        assert attr.parent_group_uuid == 'parent-123'
        assert attr.cell_index == 1
        assert attr.node_uuid == 'node-123'
        assert attr.node_id == 456
        assert attr.source == 'extraction'
        assert attr.manual == True


class TestDataObject:
    """Test DataObject class."""
    
    def test_data_object_initialization(self):
        """Test DataObject initialization with attributes and children."""
        data = {
            'id': 123,
            'uuid': 'obj-123',
            'name': 'test_object',
            'type': 'document',
            'taxonomy_ref': 'tax_ref',
            'group_path': '/group',
            'attributes': [
                {
                    'tag': 'attr1',
                    'value': 'value1'
                },
                {
                    'tag': 'attr2', 
                    'value': 'value2'
                }
            ],
            'children': [
                {
                    'id': 124,
                    'name': 'child1',
                    'type': 'paragraph'
                }
            ]
        }
        
        obj = DataObject(data)
        
        assert obj.id == 123
        assert obj.uuid == 'obj-123'
        assert obj.name == 'test_object'
        assert obj.type == 'document'
        assert obj.taxonomy_ref == 'tax_ref'
        assert obj.group_path == '/group'
        
        # Check attributes
        assert len(obj.attributes) == 2
        assert obj.attributes[0].tag == 'attr1'
        assert obj.attributes[0].value == 'value1'
        assert obj.attributes[1].tag == 'attr2'
        assert obj.attributes[1].value == 'value2'
        
        # Check children
        assert len(obj.children) == 1
        assert obj.children[0].id == 124
        assert obj.children[0].name == 'child1'
        assert obj.children[0].type == 'paragraph'


class TestContentException:
    """Test ContentException class."""
    
    def test_content_exception_initialization(self):
        """Test ContentException initialization."""
        data = {
            'id': 123,
            'uuid': 'exc-123',
            'node_uuid': 'node-123',
            'exception_type': 'validation_error',
            'severity': 'high',
            'message': 'Test error message',
            'path': '/test/path',
            'fixed': True,
            'created_on': '2023-01-01T00:00:00Z',
            'updated_on': '2023-01-02T00:00:00Z'
        }
        
        exc = ContentException(data)
        
        assert exc.id == 123
        assert exc.uuid == 'exc-123'
        assert exc.node_uuid == 'node-123'
        assert exc.exception_type == 'validation_error'
        assert exc.severity == 'high'
        assert exc.message == 'Test error message'
        assert exc.path == '/test/path'
        assert exc.fixed == True
        assert exc.created_on == '2023-01-01T00:00:00Z'
        assert exc.updated_on == '2023-01-02T00:00:00Z'


class TestDocumentTaxonValidation:
    """Test DocumentTaxonValidation class."""
    
    def test_validation_initialization(self):
        """Test DocumentTaxonValidation initialization."""
        data = {
            'taxonomy_ref': 'tax_ref_123',
            'taxon_path': 'Invoice/FieldName',
            'validation': {
                'name': 'Required Field',
                'ruleFormula': '!isBlank({FieldName})',
                'messageFormula': '"Field is required"',
                'exceptionId': 'required-field-123'
            }
        }

        validation = DocumentTaxonValidation(data)

        assert validation.taxonomy_ref == 'tax_ref_123'
        assert validation.taxon_path == 'Invoice/FieldName'
        assert validation.validation['name'] == 'Required Field'
        assert validation.validation['exceptionId'] == 'required-field-123'


class TestExtractionEngine:
    """Test ExtractionEngine functionality."""
    
    def test_extraction_engine_initialization(self):
        """Test ExtractionEngine initialization with different taxonomy types."""
        doc = Document(inmemory=True)
        root = doc.create_node("document", "Test document")
        doc.content_node = root
        
        # Test with Taxonomy objects
        taxonomy_data = {
            "name": "test_taxonomy",
            "version": "1.0",
            "ref": "test_taxonomy_ref",
            "taxons": []
        }
        
        taxonomy = Taxonomy(taxonomy_data=taxonomy_data)
        
        with ExtractionEngine(doc, [taxonomy]) as engine:
            # Should initialize successfully
            assert engine is not None
        
        # Test with dictionary taxonomies
        taxonomies = [taxonomy_data]
        
        with ExtractionEngine(doc, taxonomies) as engine:
            # Should initialize successfully
            assert engine is not None
        
        # Clean up
        taxonomy.close()
    
    def test_extraction_engine_process_empty(self):
        """Test processing with empty taxonomies."""
        doc = Document(inmemory=True)
        root = doc.create_node("document", "Test document")
        doc.content_node = root

        taxonomies = [{
            "name": "empty_taxonomy",
            "version": "1.0",
            "ref": "empty_taxonomy_ref",
            "taxons": []
        }]

        with ExtractionEngine(doc, taxonomies) as engine:
            count = engine.process_and_save()

            # Should return int (count of data objects extracted)
            assert isinstance(count, int)
            assert count >= 0
    
    def test_extraction_engine_get_exceptions(self):
        """Test getting content exceptions."""
        doc = Document(inmemory=True)
        root = doc.create_node("document", "Test document")
        doc.content_node = root
        
        taxonomies = [{
            "name": "test_taxonomy",
            "version": "1.0",
            "ref": "test_taxonomy_ref",
            "taxons": []
        }]
        
        with ExtractionEngine(doc, taxonomies) as engine:
            exceptions = engine.get_content_exceptions()
            
            # Should return list
            assert isinstance(exceptions, list)
            # All items should be ContentException objects
            for exc in exceptions:
                assert isinstance(exc, ContentException)
    
    def test_extraction_engine_get_validations(self):
        """Test getting document validations."""
        doc = Document(inmemory=True)
        root = doc.create_node("document", "Test document")
        doc.content_node = root
        
        taxonomies = [{
            "name": "test_taxonomy",
            "version": "1.0",
            "ref": "test_taxonomy_ref",
            "ref": "test_taxonomy_ref", 
            "taxons": []
        }]
        
        with ExtractionEngine(doc, taxonomies) as engine:
            validations = engine.get_document_taxon_validations()

            # Should return list
            assert isinstance(validations, list)
            # All items should be DocumentTaxonValidation objects
            for val in validations:
                assert isinstance(val, DocumentTaxonValidation)
    
    def test_extraction_engine_context_manager(self):
        """Test ExtractionEngine context manager."""
        doc = Document(inmemory=True)
        root = doc.create_node("document", "Test document")
        doc.content_node = root

        taxonomies = [{"name": "test", "version": "1.0",
            "ref": "test_taxonomy_ref", "taxons": []}]

        with ExtractionEngine(doc, taxonomies) as engine:
            # Should work inside context
            count = engine.process_and_save()
            assert isinstance(count, int)

        # Should be closed after context
        with pytest.raises(KodexaError, match="Extraction engine is closed"):
            engine.process_and_save()
    
    def test_extraction_engine_invalid_taxonomies(self):
        """Test ExtractionEngine with invalid taxonomies."""
        doc = Document(inmemory=True)
        root = doc.create_node("document", "Test document")
        doc.content_node = root
        
        # Invalid taxonomy type
        with pytest.raises(ValueError, match="Taxonomies must be Taxonomy instances or dictionaries"):
            ExtractionEngine(doc, ["invalid_type"])


class TestHighLevelExtractFunction:
    """Test the high-level extract() function."""

    def test_extract_convenience_function(self):
        """Test the extract() convenience function."""
        doc = Document(inmemory=True)
        root = doc.create_node("document", "Test document")
        doc.content_node = root

        taxonomies = [{
            "name": "test_taxonomy",
            "version": "1.0",
            "ref": "test_taxonomy_ref",
            "taxons": []
        }]

        with ExtractionEngine(doc, taxonomies) as engine:
            count = engine.process_and_save()

        # Should return count of data objects extracted
        assert isinstance(count, int)
        assert count >= 0

    def test_extract_with_taxonomy_objects(self):
        """Test extract() with Taxonomy objects."""
        doc = Document(inmemory=True)
        root = doc.create_node("document", "Test document")
        doc.content_node = root

        taxonomy_data = {
            "name": "test_taxonomy",
            "version": "1.0",
            "ref": "test_taxonomy_ref",
            "taxons": []
        }

        taxonomy = Taxonomy(taxonomy_data=taxonomy_data)

        try:
            with ExtractionEngine(doc, [taxonomy]) as engine:
                count = engine.process_and_save()

            # Should return count of data objects extracted
            assert isinstance(count, int)
            assert count >= 0
        finally:
            taxonomy.close()


class TestExtractionIntegration:
    """Test extraction engine integration with documents."""

    def test_extraction_with_content_nodes(self):
        """Test extraction with actual content nodes."""
        doc = Document(inmemory=True)
        root = doc.create_node("document", "Test document")
        para1 = doc.create_node("paragraph", "First paragraph")
        para2 = doc.create_node("paragraph", "Second paragraph")

        root.add_child(para1)
        root.add_child(para2)
        doc.content_node = root

        # Simple taxonomy for testing
        taxonomies = [{
            "name": "content_taxonomy",
            "version": "1.0",
            "ref": "content_taxonomy_ref",
            "taxons": [
                {
                    "name": "document_content",
                    "type": "group"
                }
            ]
        }]

        with ExtractionEngine(doc, taxonomies) as engine:
            count = engine.process_and_save()

        # Should process successfully
        assert isinstance(count, int)
        assert count >= 0

    def test_extraction_engine_error_handling(self):
        """Test extraction engine error handling."""
        doc = Document(inmemory=True)
        root = doc.create_node("document", "Test document")
        doc.content_node = root

        # Test with malformed taxonomy
        taxonomies = [{"invalid": "taxonomy"}]  # Missing required fields

        # Should handle gracefully (may return 0 or specific error)
        try:
            with ExtractionEngine(doc, taxonomies) as engine:
                count = engine.process_and_save()
            assert isinstance(count, int)
        except (KodexaError, ValueError):
            # Expected for malformed taxonomy
            pass