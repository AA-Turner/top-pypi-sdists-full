"""
ProcessingStep class for legacy_python compatibility.

Provides a Pydantic-based model for tracking document processing history
with parent-child relationships between steps.
"""
import json
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any, Set
from pydantic import BaseModel, Field


class KnowledgeFeature(BaseModel):
    """Represents a feature associated with a knowledge item."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    feature_type_ref: Optional[str] = Field(None, alias='featureTypeRef')
    properties: Dict[str, Any] = Field(default_factory=dict)
    extended_properties: Dict[str, Any] = Field(default_factory=dict, alias='extendedProperties')
    slug: Optional[str] = None
    active: bool = True
    
    class Config:
        populate_by_name = True


class KnowledgeItem(BaseModel):
    """Represents a knowledge item associated with a processing step."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sequence_order: int = Field(0, alias='sequenceOrder')
    description: Optional[str] = None
    slug: Optional[str] = None
    title: Optional[str] = None
    knowledge_item_type_ref: Optional[str] = Field(None, alias='knowledgeItemTypeRef')
    properties: Dict[str, Any] = Field(default_factory=dict)
    features: List[KnowledgeFeature] = Field(default_factory=list)
    
    class Config:
        populate_by_name = True


class ProcessingStep(BaseModel):
    """
    Represents a step in document processing with parent-child relationships.
    
    This class provides compatibility with legacy_python's ProcessingStep,
    supporting hierarchical processing step tracking and merging operations.
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    start_timestamp: Optional[datetime] = Field(None, alias='startTimestamp')
    duration: Optional[int] = None  # Duration in milliseconds
    metadata: Dict[str, Any] = Field(default_factory=dict)
    presentation_metadata: Dict[str, Any] = Field(default_factory=dict, alias='presentationMetadata')
    children: List['ProcessingStep'] = Field(default_factory=list)
    parents: List['ProcessingStep'] = Field(default_factory=list)
    internal_steps: List['ProcessingStep'] = Field(default_factory=list, alias='internalSteps')
    knowledge_items: List[KnowledgeItem] = Field(default_factory=list, alias='knowledgeItems')
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True
        populate_by_name = True  # Allow both field name and alias
        json_encoders = {
            'ProcessingStep': lambda step: step.to_dict()
        }
    
    def add_child(self, child_step: 'ProcessingStep'):
        """
        Add a child step to this step.
        
        This creates a bidirectional parent-child relationship.
        
        Args:
            child_step: The ProcessingStep to add as a child.
        """
        if child_step not in self.children:
            self.children.append(child_step)
        if self not in child_step.parents:
            child_step.parents.append(self)
    
    @staticmethod
    def merge_with(*other_steps: 'ProcessingStep') -> 'ProcessingStep':
        """
        Create a new merged step from multiple parent steps.
        
        The merged step will have all provided steps as parents,
        and will be added as a child to each of them.
        
        Args:
            *other_steps: Variable number of ProcessingStep instances to merge.
            
        Returns:
            A new ProcessingStep that merges the provided steps.
        """
        merged_name = f"Merged({', '.join(step.name for step in other_steps)})"
        merged_step = ProcessingStep(name=merged_name)
        
        for step in other_steps:
            step.children.append(merged_step)
            merged_step.parents.append(step)
        
        return merged_step
    
    def to_dict(self, seen: Optional[Set[str]] = None) -> Dict[str, Any]:
        """
        Convert this ProcessingStep to a dictionary.

        Handles circular references by tracking already seen step IDs.

        Args:
            seen: Set of already processed step IDs to avoid circular references.

        Returns:
            Dictionary representation of this ProcessingStep.
        """
        if seen is None:
            seen = set()

        # Avoid circular references by returning minimal info for already seen objects
        if self.id in seen:
            return {'uuid': self.id, 'name': self.name}

        seen.add(self.id)

        result = {
            'uuid': self.id,  # Go struct expects 'uuid' field
            'name': self.name,
            'metadata': self.metadata,
            'presentationMetadata': self.presentation_metadata,
            'children': [child.to_dict(seen) for child in self.children],
            'parents': [{'uuid': parent.id, 'name': parent.name} for parent in self.parents],
        }
        
        # Add optional fields if they have values
        if self.start_timestamp is not None:
            result['startTimestamp'] = self.start_timestamp.isoformat()
        if self.duration is not None:
            result['duration'] = self.duration
        if self.internal_steps:
            result['internalSteps'] = [step.to_dict(seen) for step in self.internal_steps]
        if self.knowledge_items:
            result['knowledgeItems'] = [item.model_dump(by_alias=True) for item in self.knowledge_items]
        
        return result
    
    def to_json(self) -> str:
        """
        Convert this ProcessingStep to a JSON string.
        
        Returns:
            JSON string representation of this ProcessingStep.
        """
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], step_cache: Optional[Dict[str, 'ProcessingStep']] = None) -> 'ProcessingStep':
        """
        Create a ProcessingStep from a dictionary.
        
        This method reconstructs the step hierarchy, handling circular references
        through a step cache.
        
        Args:
            data: Dictionary containing step data.
            step_cache: Cache of already created steps to handle circular references.
            
        Returns:
            ProcessingStep instance reconstructed from the dictionary.
        """
        if step_cache is None:
            step_cache = {}

        # Check if this step already exists in cache
        # Support both 'uuid' (new Go format) and 'id' (legacy) fields
        step_id = data.get('uuid') or data.get('id')
        if step_id and step_id in step_cache:
            return step_cache[step_id]
        
        # Parse start_timestamp if present
        start_timestamp = None
        if 'startTimestamp' in data and data['startTimestamp']:
            ts_value = data['startTimestamp']
            if isinstance(ts_value, str):
                start_timestamp = datetime.fromisoformat(ts_value.replace('Z', '+00:00'))
            elif isinstance(ts_value, datetime):
                start_timestamp = ts_value
        
        # Parse knowledge items if present
        knowledge_items = []
        for ki_data in data.get('knowledgeItems', []):
            if isinstance(ki_data, dict):
                knowledge_items.append(KnowledgeItem(**ki_data))
        
        # Create the step without children/parents first
        # Support both 'uuid' (new Go format) and 'id' (legacy) fields
        step = cls(
            id=data.get('uuid') or data.get('id') or str(uuid.uuid4()),
            name=data['name'],
            start_timestamp=start_timestamp,
            duration=data.get('duration'),
            metadata=data.get('metadata', {}),
            presentation_metadata=data.get('presentationMetadata', {}),
            knowledge_items=knowledge_items
        )
        
        # Add to cache immediately to handle circular references
        if step_id:
            step_cache[step_id] = step
        
        # Process children if they are full objects (not just references)
        for child_data in data.get('children', []):
            if isinstance(child_data, dict) and 'name' in child_data:
                # Full child object, recursively create it
                if len(child_data) > 2:  # More than just id and name
                    child = cls.from_dict(child_data, step_cache)
                    if child not in step.children:
                        step.children.append(child)
                    if step not in child.parents:
                        child.parents.append(step)
        
        # Process internal steps
        for internal_data in data.get('internalSteps', []):
            if isinstance(internal_data, dict) and 'name' in internal_data:
                internal_step = cls.from_dict(internal_data, step_cache)
                if internal_step not in step.internal_steps:
                    step.internal_steps.append(internal_step)
        
        return step
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ProcessingStep':
        """
        Create a ProcessingStep from a JSON string.
        
        Args:
            json_str: JSON string containing step data.
            
        Returns:
            ProcessingStep instance reconstructed from the JSON.
        """
        return cls.from_dict(json.loads(json_str))
    
    def __repr__(self) -> str:
        """String representation of this ProcessingStep."""
        return f"Step(id={self.id}, name={self.name})"
    
    def __eq__(self, other) -> bool:
        """Check equality based on step ID."""
        if not isinstance(other, ProcessingStep):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash based on step ID for use in sets and dicts."""
        return hash(self.id)


# Make ProcessingStep available for forward references
ProcessingStep.model_rebuild()