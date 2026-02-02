"""
Tests for ProcessingStep class for legacy_python compatibility.
"""
import json
import pytest
from kodexa_document import ProcessingStep


class TestProcessingStepBasic:
    """Test basic ProcessingStep functionality"""
    
    def test_step_creation_basic(self):
        """Test creating a basic ProcessingStep"""
        step = ProcessingStep(name="Test Step")
        
        assert step.name == "Test Step"
        assert step.id is not None
        assert len(step.id) == 36  # UUID length
        assert step.metadata == {}
        assert step.presentation_metadata == {}
        assert step.children == []
        assert step.parents == []
    
    def test_step_creation_with_metadata(self):
        """Test creating a ProcessingStep with metadata"""
        metadata = {"key1": "value1", "key2": 42}
        presentation_metadata = {"ui": "config"}
        
        step = ProcessingStep(
            name="Test Step",
            metadata=metadata,
            presentation_metadata=presentation_metadata
        )
        
        assert step.name == "Test Step"
        assert step.metadata == metadata
        assert step.presentation_metadata == presentation_metadata
    
    def test_step_creation_with_alias(self):
        """Test creating a ProcessingStep using presentationMetadata alias"""
        step = ProcessingStep(
            name="Test Step",
            presentationMetadata={"ui": "config"}
        )
        
        assert step.presentation_metadata == {"ui": "config"}
    
    def test_step_id_uniqueness(self):
        """Test that step IDs are unique"""
        step1 = ProcessingStep(name="Step 1")
        step2 = ProcessingStep(name="Step 2")
        
        assert step1.id != step2.id


class TestProcessingStepRelationships:
    """Test ProcessingStep parent-child relationships"""
    
    def test_add_child_basic(self):
        """Test adding a child to a step"""
        parent = ProcessingStep(name="Parent")
        child = ProcessingStep(name="Child")
        
        parent.add_child(child)
        
        assert child in parent.children
        assert parent in child.parents
    
    def test_add_child_prevents_duplicates(self):
        """Test that adding the same child twice doesn't create duplicates"""
        parent = ProcessingStep(name="Parent")
        child = ProcessingStep(name="Child")
        
        parent.add_child(child)
        parent.add_child(child)  # Add again
        
        assert len(parent.children) == 1
        assert len(child.parents) == 1
    
    def test_complex_hierarchy(self):
        """Test creating a complex step hierarchy"""
        step1 = ProcessingStep(name="Step 1")
        step2 = ProcessingStep(name="Step 2")
        step3 = ProcessingStep(name="Step 3")
        
        step1.add_child(step2)
        step2.add_child(step3)
        
        # Check forward relationships
        assert step2 in step1.children
        assert step3 in step2.children
        
        # Check backward relationships
        assert step1 in step2.parents
        assert step2 in step3.parents
        
        # Check that step1 and step3 are not directly connected
        assert step3 not in step1.children
        assert step1 not in step3.parents
    
    def test_multiple_parents_children(self):
        """Test a step with multiple parents and children"""
        parent1 = ProcessingStep(name="Parent 1")
        parent2 = ProcessingStep(name="Parent 2")
        middle = ProcessingStep(name="Middle")
        child1 = ProcessingStep(name="Child 1")
        child2 = ProcessingStep(name="Child 2")
        
        parent1.add_child(middle)
        parent2.add_child(middle)
        middle.add_child(child1)
        middle.add_child(child2)
        
        assert len(middle.parents) == 2
        assert len(middle.children) == 2
        assert parent1 in middle.parents
        assert parent2 in middle.parents
        assert child1 in middle.children
        assert child2 in middle.children


class TestProcessingStepMerge:
    """Test ProcessingStep merge functionality"""
    
    def test_merge_with_basic(self):
        """Test merging two steps"""
        step1 = ProcessingStep(name="Step 1")
        step2 = ProcessingStep(name="Step 2")
        
        merged = ProcessingStep.merge_with(step1, step2)
        
        assert merged.name == "Merged(Step 1, Step 2)"
        assert len(merged.parents) == 2
        assert step1 in merged.parents
        assert step2 in merged.parents
        assert merged in step1.children
        assert merged in step2.children
    
    def test_merge_with_multiple_steps(self):
        """Test merging multiple steps"""
        step1 = ProcessingStep(name="Step 1")
        step2 = ProcessingStep(name="Step 2")
        step3 = ProcessingStep(name="Step 3")
        
        merged = ProcessingStep.merge_with(step1, step2, step3)
        
        assert merged.name == "Merged(Step 1, Step 2, Step 3)"
        assert len(merged.parents) == 3
        assert all(step in merged.parents for step in [step1, step2, step3])
        assert all(merged in step.children for step in [step1, step2, step3])
    
    def test_merge_with_single_step(self):
        """Test merging with a single step"""
        step1 = ProcessingStep(name="Step 1")
        
        merged = ProcessingStep.merge_with(step1)
        
        assert merged.name == "Merged(Step 1)"
        assert len(merged.parents) == 1
        assert step1 in merged.parents
        assert merged in step1.children


class TestProcessingStepSerialization:
    """Test ProcessingStep serialization and deserialization"""
    
    def test_to_dict_basic(self):
        """Test converting a simple step to dict"""
        step = ProcessingStep(
            name="Test Step",
            metadata={"key": "value"},
            presentation_metadata={"ui": "config"}
        )
        
        result = step.to_dict()
        
        assert result["name"] == "Test Step"
        assert result["uuid"] == step.id
        assert result["metadata"] == {"key": "value"}
        assert result["presentationMetadata"] == {"ui": "config"}
        assert result["children"] == []
        assert result["parents"] == []
    
    def test_to_dict_with_relationships(self):
        """Test converting steps with relationships to dict"""
        parent = ProcessingStep(name="Parent")
        child = ProcessingStep(name="Child")
        parent.add_child(child)
        
        parent_dict = parent.to_dict()
        child_dict = child.to_dict()
        
        # Parent should have full child info
        assert len(parent_dict["children"]) == 1
        assert parent_dict["children"][0]["name"] == "Child"
        assert parent_dict["children"][0]["uuid"] == child.id

        # Child should have minimal parent info (to avoid circular refs)
        assert len(child_dict["parents"]) == 1
        assert child_dict["parents"][0]["name"] == "Parent"
        assert child_dict["parents"][0]["uuid"] == parent.id
    
    def test_to_dict_circular_reference_handling(self):
        """Test that to_dict handles circular references properly"""
        step1 = ProcessingStep(name="Step 1")
        step2 = ProcessingStep(name="Step 2")
        step1.add_child(step2)
        step2.add_child(step1)  # Create circular reference
        
        # This should not cause infinite recursion
        result = step1.to_dict()
        
        assert result["name"] == "Step 1"
        assert len(result["children"]) == 1
        assert result["children"][0]["name"] == "Step 2"
    
    def test_to_json_basic(self):
        """Test converting a step to JSON"""
        step = ProcessingStep(name="Test Step", metadata={"key": "value"})
        
        json_str = step.to_json()
        parsed = json.loads(json_str)
        
        assert parsed["name"] == "Test Step"
        assert parsed["metadata"] == {"key": "value"}
    
    def test_from_dict_basic(self):
        """Test creating a step from dict"""
        data = {
            "id": "test-id",
            "name": "Test Step",
            "metadata": {"key": "value"},
            "presentationMetadata": {"ui": "config"}
        }
        
        step = ProcessingStep.from_dict(data)
        
        assert step.id == "test-id"
        assert step.name == "Test Step"
        assert step.metadata == {"key": "value"}
        assert step.presentation_metadata == {"ui": "config"}
    
    def test_from_dict_with_children(self):
        """Test creating steps with children from dict"""
        data = {
            "id": "parent-id",
            "name": "Parent",
            "children": [
                {
                    "id": "child-id",
                    "name": "Child",
                    "metadata": {"child": "data"}
                }
            ]
        }
        
        parent = ProcessingStep.from_dict(data)
        
        assert parent.name == "Parent"
        assert len(parent.children) == 1
        assert parent.children[0].name == "Child"
        assert parent.children[0].metadata == {"child": "data"}
        assert parent in parent.children[0].parents
    
    def test_from_json_basic(self):
        """Test creating a step from JSON"""
        data = {
            "name": "Test Step",
            "metadata": {"key": "value"}
        }
        json_str = json.dumps(data)
        
        step = ProcessingStep.from_json(json_str)
        
        assert step.name == "Test Step"
        assert step.metadata == {"key": "value"}
    
    def test_round_trip_serialization(self):
        """Test that serialization and deserialization are consistent"""
        original = ProcessingStep(
            name="Test Step",
            metadata={"key": "value"},
            presentation_metadata={"ui": "config"}
        )
        child = ProcessingStep(name="Child Step")
        original.add_child(child)
        
        # Convert to dict and back
        data = original.to_dict()
        reconstructed = ProcessingStep.from_dict(data)
        
        assert reconstructed.name == original.name
        assert reconstructed.metadata == original.metadata
        assert reconstructed.presentation_metadata == original.presentation_metadata
        assert len(reconstructed.children) == len(original.children)
        assert reconstructed.children[0].name == original.children[0].name


class TestProcessingStepEquality:
    """Test ProcessingStep equality and hashing"""
    
    def test_equality_by_id(self):
        """Test that steps are equal if they have the same ID"""
        step1 = ProcessingStep(name="Step 1", id="same-id")
        step2 = ProcessingStep(name="Step 2", id="same-id")  # Different name, same ID
        
        assert step1 == step2
    
    def test_inequality_by_id(self):
        """Test that steps are not equal if they have different IDs"""
        step1 = ProcessingStep(name="Step 1")
        step2 = ProcessingStep(name="Step 1")  # Same name, different ID
        
        assert step1 != step2
    
    def test_hash_by_id(self):
        """Test that step hash is based on ID"""
        step1 = ProcessingStep(name="Step 1", id="test-id")
        step2 = ProcessingStep(name="Step 2", id="test-id")
        
        assert hash(step1) == hash(step2)
    
    def test_use_in_set(self):
        """Test that steps can be used in sets properly"""
        step1 = ProcessingStep(name="Step 1", id="id1")
        step2 = ProcessingStep(name="Step 2", id="id2")
        step3 = ProcessingStep(name="Step 3", id="id1")  # Same ID as step1
        
        step_set = {step1, step2, step3}
        
        assert len(step_set) == 2  # step1 and step3 should be considered the same
    
    def test_repr(self):
        """Test string representation of ProcessingStep"""
        step = ProcessingStep(name="Test Step", id="test-id")
        
        repr_str = repr(step)
        
        assert "Step(id=test-id, name=Test Step)" == repr_str