"""
Processing step model for tracking document processing history.
"""
import json
import uuid
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict, model_serializer

from kodexa_document.model.base import StandardDateTime
from kodexa_document.model.objects import KnowledgeItem


class ProcessingStep(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    start_timestamp: Optional[StandardDateTime] = Field(None, alias="startTimestamp")
    duration: Optional[int] = Field(None, alias="duration")
    metadata: dict = Field(default_factory=lambda: {})
    applied_knowledge_items: List[KnowledgeItem] = Field(default_factory=list, alias="knowledgeItems")
    presentation_metadata: dict = Field(default_factory=lambda: {}, alias='presentationMetadata')
    children: List['ProcessingStep'] = Field(default_factory=list)
    parents: List['ProcessingStep'] = Field(default_factory=list)
    internal_steps: List['ProcessingStep'] = Field(default_factory=list, alias='internalSteps')

    def add_child(self, child_step: 'ProcessingStep'):
        self.children.append(child_step)
        child_step.parents.append(self)

    @staticmethod
    def merge_with(*other_steps: 'ProcessingStep') -> 'ProcessingStep':
        merged_step = ProcessingStep(name=f"Merged({', '.join(step.name for step in other_steps)})")
        for step in other_steps:
            step.children.append(merged_step)
            merged_step.parents.append(step)
        return merged_step

    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    @model_serializer(mode='plain')
    def _serialize(self):
        return self.to_dict()

    def to_dict(self, seen=None):
        if seen is None:
            seen = set()

        # Avoid circular references by skipping already seen objects
        if self.id in seen:
            return {'id': self.id, 'name': self.name}

        seen.add(self.id)

        knowledge_items = []
        if self.applied_knowledge_items:
            for knowledge_item in self.applied_knowledge_items:
                # Use model_dump() if it's a pydantic model
                if hasattr(knowledge_item, "model_dump") and callable(getattr(knowledge_item, "model_dump")):
                    knowledge_items.append(knowledge_item.model_dump())
                # If it's already a dict, accept as is
                elif isinstance(knowledge_item, dict):
                    knowledge_items.append(knowledge_item)
                else:
                    raise TypeError(
                        f"Item in applied_knowledge_items must be a Pydantic model or dict, got {type(knowledge_item)}"
                    )

        return {
            'id': self.id,
            'name': self.name,
            'metadata': self.metadata,
            'knowledgeItems': knowledge_items,
            'startTimestamp': self.start_timestamp.isoformat() if self.start_timestamp else None,
            'duration': self.duration,
            'presentationMetadata': self.presentation_metadata,
            'internalSteps': [step.to_dict(seen) for step in self.internal_steps],
            'children': [child.to_dict(seen) for child in self.children],
            'parents': [{'id': parent.id, 'name': parent.name} for parent in self.parents],
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def __repr__(self):
        return f"Step(id={self.id}, name={self.name})"
