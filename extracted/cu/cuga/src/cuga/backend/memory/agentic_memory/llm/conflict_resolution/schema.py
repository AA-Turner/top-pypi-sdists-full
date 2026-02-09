from cuga.backend.memory.agentic_memory.schema import RecordedFact
from pydantic import BaseModel, Field
from typing import Literal


class SimpleMemory(BaseModel):
    """Derived from either a `Fact` or `RecordedFact`. Optimized for LLM-based conflict resolution."""

    id: str = Field(description='The unique ID of a fact.')
    content: str = Field(description='The content of the memory.')

    @staticmethod
    def from_recorded_facts(facts: list[RecordedFact]) -> list['SimpleMemory']:
        return [SimpleMemory(id=fact.id, content=fact.content) for fact in facts]


class MemoryEvent(BaseModel):
    """Produced by the LLM, to be processed by a memory backend."""

    id: str = Field(description='The unique ID of a fact.')
    content: str = Field(description='The content of the memory.')
    event: Literal['ADD', 'UPDATE', 'DELETE', 'NONE'] = Field(
        description='The type of update operation to perform.'
    )
    old_memory: str | None = Field(default=None, description='The memory before it was updated.')
    metadata: dict | None = Field(
        default=None, description='Arbitrary metadata which is related to the fact.'
    )
