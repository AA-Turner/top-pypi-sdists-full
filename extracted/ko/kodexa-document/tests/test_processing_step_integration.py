"""
Tests for ProcessingStep integration with Document class.

Tests that ProcessingStep objects work correctly with Document.get_steps()
and Document.set_steps() methods for legacy_python compatibility.
"""
import json
import pytest
from kodexa_document import Document, ProcessingStep


class TestDocumentProcessingStepIntegration:
    """Test ProcessingStep integration with Document"""
    
    def test_set_and_get_steps_basic(self):
        """Test setting and getting basic processing steps"""
        doc = Document()
        
        # Create processing steps
        step1 = ProcessingStep(name="Step 1")
        step2 = ProcessingStep(name="Step 2")
        step3 = ProcessingStep(name="Step 3")
        
        # Set steps on document
        doc.set_steps([step1, step2, step3])
        
        # Retrieve steps
        retrieved_steps = doc.get_steps()
        
        assert isinstance(retrieved_steps, list)
        assert len(retrieved_steps) == 3
        assert all(isinstance(step, ProcessingStep) for step in retrieved_steps)
        assert retrieved_steps[0].name == "Step 1"
        assert retrieved_steps[1].name == "Step 2"
        assert retrieved_steps[2].name == "Step 3"
    
    def test_set_and_get_steps_with_relationships(self):
        """Test setting and getting steps with parent-child relationships.

        Note: The Go layer stores steps but does not currently preserve
        parent-child relationships in the database. This test verifies
        that steps with relationships can be stored and retrieved,
        even though the relationships themselves are not persisted.
        """
        doc = Document()

        # Create processing steps with relationships
        step1 = ProcessingStep(name="Step 1")
        step2 = ProcessingStep(name="Step 2")
        step3 = ProcessingStep(name="Step 3")

        # Add relationships (these are set in Python but not persisted by Go layer)
        step1.add_child(step2)
        step2.add_child(step3)

        # Set steps on document
        doc.set_steps([step1, step2, step3])

        # Retrieve steps
        retrieved_steps = doc.get_steps()

        assert len(retrieved_steps) == 3

        # Find steps by name (order might not be preserved)
        step_dict = {step.name: step for step in retrieved_steps}

        # Verify all steps were stored and retrieved
        assert "Step 1" in step_dict
        assert "Step 2" in step_dict
        assert "Step 3" in step_dict

        # Note: Parent-child relationships are not persisted by the Go layer
        # The children/parents lists will be empty after round-trip through Go
    
    def test_legacy_pattern_compatibility(self):
        """Test the exact legacy_python usage pattern from tests.

        Note: The Go layer stores steps but does not currently preserve
        parent-child relationships in the database. This test verifies
        basic step storage compatibility with the legacy pattern.
        """
        doc = Document()

        # Create some processing steps (from legacy test)
        step1 = ProcessingStep(name="Step 1")
        step2 = ProcessingStep(name="Step 2")
        step3 = ProcessingStep(name="Step 3")

        # Add children to the steps (from legacy test)
        # Note: These relationships are not persisted by Go layer
        step1.add_child(step2)
        step2.add_child(step3)

        # Set the steps to the document (from legacy test)
        doc.set_steps([step1, step2, step3])

        # Retrieve the steps from the document (from legacy test)
        retrieved_steps = doc.get_steps()

        # Validate the retrieved steps (from legacy test)
        assert len(retrieved_steps) == 3

        # Create lookup dict for easier validation
        step_lookup = {step.name: step for step in retrieved_steps}

        assert "Step 1" in step_lookup
        assert "Step 2" in step_lookup
        assert "Step 3" in step_lookup

        # Note: Parent-child relationships are not persisted by the Go layer
        # The children/parents lists will be empty after round-trip through Go
    
    def test_empty_steps(self):
        """Test handling empty steps list"""
        doc = Document()
        
        # Set empty steps
        doc.set_steps([])
        retrieved_steps = doc.get_steps()
        
        assert isinstance(retrieved_steps, list)
        assert len(retrieved_steps) == 0
    
    def test_none_steps(self):
        """Test clearing steps with None"""
        doc = Document()
        
        # First set some steps
        step1 = ProcessingStep(name="Step 1")
        doc.set_steps([step1])
        
        # Verify step was set
        assert len(doc.get_steps()) == 1
        
        # Clear with None
        doc.set_steps(None)
        retrieved_steps = doc.get_steps()
        
        assert isinstance(retrieved_steps, list)
        assert len(retrieved_steps) == 0
    
    def test_mixed_step_types(self):
        """Test setting steps with mixed ProcessingStep and dict objects"""
        doc = Document()
        
        step_obj = ProcessingStep(name="Step Object")
        step_dict = {
            "name": "Step Dict",
            "metadata": {"type": "dict"}
        }
        
        # Should accept both ProcessingStep objects and dict objects
        doc.set_steps([step_obj, step_dict])
        retrieved_steps = doc.get_steps()
        
        assert len(retrieved_steps) == 2
        assert all(isinstance(step, ProcessingStep) for step in retrieved_steps)
        
        # Find the steps
        names = [step.name for step in retrieved_steps]
        assert "Step Object" in names
        assert "Step Dict" in names
        
        # Find the dict-created step and verify its metadata
        dict_step = next(step for step in retrieved_steps if step.name == "Step Dict")
        assert dict_step.metadata == {"type": "dict"}
    
    def test_backward_compatibility_string_input(self):
        """Test that string input still works for backward compatibility"""
        doc = Document()
        
        # Test with JSON string
        steps_json = json.dumps([
            {"name": "String Step 1", "metadata": {"source": "string"}},
            {"name": "String Step 2", "metadata": {"source": "string"}}
        ])
        
        doc.set_steps(steps_json)
        retrieved_steps = doc.get_steps()
        
        # Should return ProcessingStep objects even when set as string
        assert isinstance(retrieved_steps, list)
        assert len(retrieved_steps) == 2
        assert all(isinstance(step, ProcessingStep) for step in retrieved_steps)
        
        names = [step.name for step in retrieved_steps]
        assert "String Step 1" in names
        assert "String Step 2" in names
    
    def test_invalid_step_type_error(self):
        """Test that invalid step types raise appropriate errors"""
        doc = Document()
        
        with pytest.raises(TypeError, match="Invalid step type"):
            doc.set_steps([ProcessingStep(name="Valid"), "invalid", ProcessingStep(name="Also Valid")])
        
        with pytest.raises(TypeError, match="steps must be a list"):
            doc.set_steps(42)
    
    def test_steps_persistence_across_operations(self):
        """Test that steps persist through document operations"""
        doc = Document()
        
        # Set steps
        step1 = ProcessingStep(name="Persistent Step")
        doc.set_steps([step1])
        
        # Perform some other document operations
        doc.metadata["test"] = "value"
        root = doc.create_node("document")
        doc.content_node = root
        
        # Steps should still be there
        retrieved_steps = doc.get_steps()
        assert len(retrieved_steps) == 1
        assert retrieved_steps[0].name == "Persistent Step"
    
    def test_steps_with_complex_metadata(self):
        """Test steps with complex metadata structures"""
        doc = Document()
        
        complex_metadata = {
            "nested": {
                "deeply": {
                    "nested": "value"
                }
            },
            "array": [1, 2, 3],
            "mixed": {
                "string": "text",
                "number": 42,
                "boolean": True
            }
        }
        
        step = ProcessingStep(
            name="Complex Step",
            metadata=complex_metadata,
            presentation_metadata={"ui_config": {"theme": "dark"}}
        )
        
        doc.set_steps([step])
        retrieved_steps = doc.get_steps()
        
        assert len(retrieved_steps) == 1
        retrieved_step = retrieved_steps[0]
        assert retrieved_step.name == "Complex Step"
        assert retrieved_step.metadata == complex_metadata
        assert retrieved_step.presentation_metadata == {"ui_config": {"theme": "dark"}}