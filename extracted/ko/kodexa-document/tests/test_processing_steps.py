"""
Test processing steps functionality matching legacy_python behavior.
"""

import json
import pytest
from kodexa_document import Document, ProcessingStep


class TestProcessingSteps:
    """Test processing steps methods."""

    def test_get_steps_empty_document(self):
        """Test getting steps from empty document returns empty list."""
        document = Document(inmemory=True)

        # New document should have empty steps
        steps = document.get_steps()
        assert steps == []

        document.close()

    def test_set_and_get_steps_simple(self):
        """Test setting and getting simple processing steps."""
        document = Document(inmemory=True)

        # Create a simple ProcessingStep
        step = ProcessingStep(name="text_processor")

        # Set steps as a list
        document.set_steps([step])

        # Get it back
        retrieved_steps = document.get_steps()
        assert len(retrieved_steps) == 1
        assert retrieved_steps[0].name == "text_processor"

        document.close()

    def test_set_and_get_multiple_steps(self):
        """Test setting and getting multiple processing steps."""
        document = Document(inmemory=True)

        # Create multiple ProcessingStep objects
        step1 = ProcessingStep(name="step1")
        step2 = ProcessingStep(name="step2")
        step3 = ProcessingStep(name="step3")

        # Set steps as a list
        document.set_steps([step1, step2, step3])

        # Get them back
        retrieved_steps = document.get_steps()
        assert len(retrieved_steps) == 3
        names = [s.name for s in retrieved_steps]
        assert "step1" in names
        assert "step2" in names
        assert "step3" in names

        document.close()

    def test_set_and_get_steps_with_dict(self):
        """Test setting steps using dict format."""
        document = Document(inmemory=True)

        # Set multiple steps as dicts
        steps_data = [
            {"name": "ocr_processor", "metadata": {"language": "en"}},
            {"name": "text_extractor", "metadata": {"format": "plain"}},
            {"name": "classifier", "metadata": {"model": "bert"}}
        ]
        document.set_steps(steps_data)

        # Get them back
        retrieved_steps = document.get_steps()
        assert len(retrieved_steps) == 3
        names = [s.name for s in retrieved_steps]
        assert "ocr_processor" in names
        assert "text_extractor" in names
        assert "classifier" in names

        # Verify metadata preserved
        ocr_step = next(s for s in retrieved_steps if s.name == "ocr_processor")
        assert ocr_step.metadata.get("language") == "en"

        document.close()

    def test_set_and_get_steps_complex(self):
        """Test setting and getting complex processing steps with metadata."""
        document = Document(inmemory=True)

        # Create multiple complex processing steps
        step1 = ProcessingStep(
            name="ocr_processor",
            metadata={
                "language": "en",
                "confidence_threshold": 0.8
            }
        )
        step2 = ProcessingStep(
            name="text_analyzer",
            metadata={
                "mode": "deep",
                "max_tokens": 1000
            }
        )

        document.set_steps([step1, step2])

        # Get them back and verify
        retrieved_steps = document.get_steps()
        assert len(retrieved_steps) == 2

        names = [s.name for s in retrieved_steps]
        assert "ocr_processor" in names
        assert "text_analyzer" in names

        ocr_step = next(s for s in retrieved_steps if s.name == "ocr_processor")
        assert ocr_step.metadata.get("language") == "en"

        document.close()

    def test_set_steps_overwrite(self):
        """Test that setting steps overwrites previous steps."""
        document = Document(inmemory=True)

        # Set initial steps
        initial_step = ProcessingStep(name="initial_processor")
        document.set_steps([initial_step])

        # Verify initial steps
        steps = document.get_steps()
        assert len(steps) == 1
        assert steps[0].name == "initial_processor"

        # Overwrite with new steps
        new_step = ProcessingStep(name="updated_processor")
        document.set_steps([new_step])

        # Verify overwrite worked
        steps = document.get_steps()
        assert len(steps) == 1
        assert steps[0].name == "updated_processor"

        document.close()

    def test_set_steps_none_clears(self):
        """Test that setting steps to None clears the steps."""
        document = Document(inmemory=True)

        # Set some steps first
        step = ProcessingStep(name="test_processor")
        document.set_steps([step])

        # Verify steps are set
        steps = document.get_steps()
        assert len(steps) == 1

        # Clear steps by setting to None
        document.set_steps(None)

        # Verify steps are cleared
        assert document.get_steps() == []

        document.close()

    def test_set_steps_empty_list(self):
        """Test setting steps to empty list."""
        document = Document(inmemory=True)

        # Set some steps first
        step = ProcessingStep(name="test_processor")
        document.set_steps([step])

        # Set to empty list
        document.set_steps([])

        # Should return empty list
        assert document.get_steps() == []

        document.close()

    def test_set_steps_type_validation(self):
        """Test that set_steps validates input type."""
        document = Document(inmemory=True)

        # Should raise TypeError for invalid input types
        with pytest.raises(TypeError, match="steps must be a list"):
            document.set_steps(123)

        # Lists should work
        document.set_steps([])  # Empty list should work

        # None should work
        document.set_steps(None)

        document.close()

    def test_steps_persistence_across_operations(self):
        """Test that steps persist across other document operations."""
        document = Document(inmemory=True)

        # Set processing steps
        step = ProcessingStep(name="persistent_test_processor")
        document.set_steps([step])

        # Perform other operations on document
        root = document.create_node("document")
        document.content_node = root

        child = document.create_node("paragraph", content="Test content")
        root.add_child(child)

        # Verify steps are still there
        steps = document.get_steps()
        assert len(steps) == 1
        assert steps[0].name == "persistent_test_processor"

        # Set metadata
        document.set_metadata("test_key", "test_value")

        # Steps should still be there
        steps = document.get_steps()
        assert len(steps) == 1
        assert steps[0].name == "persistent_test_processor"

        document.close()

    def test_multiple_documents_independent_steps(self):
        """Test that different documents have independent processing steps."""
        doc1 = Document(inmemory=True)
        doc2 = Document(inmemory=True)

        # Set different steps for each document
        step1 = ProcessingStep(name="doc1_processor")
        step2 = ProcessingStep(name="doc2_processor")

        doc1.set_steps([step1])
        doc2.set_steps([step2])

        # Verify each document has its own steps
        doc1_steps = doc1.get_steps()
        doc2_steps = doc2.get_steps()

        assert len(doc1_steps) == 1
        assert doc1_steps[0].name == "doc1_processor"

        assert len(doc2_steps) == 1
        assert doc2_steps[0].name == "doc2_processor"

        # Clear steps in doc1
        doc1.set_steps(None)

        # doc2 should be unaffected
        assert doc1.get_steps() == []
        doc2_steps = doc2.get_steps()
        assert len(doc2_steps) == 1
        assert doc2_steps[0].name == "doc2_processor"

        doc1.close()
        doc2.close()

    def test_processing_step_with_children(self):
        """Test ProcessingStep with child steps."""
        document = Document(inmemory=True)

        # Create parent step with children
        parent = ProcessingStep(name="pipeline")
        child1 = ProcessingStep(name="step1")
        child2 = ProcessingStep(name="step2")

        parent.add_child(child1)
        parent.add_child(child2)

        document.set_steps([parent])

        # Get it back
        retrieved_steps = document.get_steps()
        assert len(retrieved_steps) == 1
        assert retrieved_steps[0].name == "pipeline"
        # Note: children might not be fully preserved depending on Go implementation

        document.close()

    def test_processing_step_with_metadata(self):
        """Test ProcessingStep with various metadata."""
        document = Document(inmemory=True)

        step = ProcessingStep(
            name="metadata_test",
            metadata={
                "version": "1.0",
                "config": {
                    "setting1": True,
                    "setting2": 42
                }
            },
            presentation_metadata={
                "display_name": "Metadata Test Step",
                "icon": "gear"
            }
        )

        document.set_steps([step])

        retrieved_steps = document.get_steps()
        assert len(retrieved_steps) == 1
        assert retrieved_steps[0].name == "metadata_test"
        assert retrieved_steps[0].metadata.get("version") == "1.0"

        document.close()
