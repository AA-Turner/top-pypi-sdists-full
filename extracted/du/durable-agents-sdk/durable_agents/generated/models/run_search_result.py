from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .run_search_result_agent import RunSearchResult_agent

@dataclass
class RunSearchResult(Parsable):
    # The agent property
    agent: Optional[RunSearchResult_agent] = None
    # The completed_at property
    completed_at: Optional[datetime.datetime] = None
    # Conversation ID that backed the completed run memory search hit.
    conversation_id: Optional[str] = None
    # The created_at property
    created_at: Optional[datetime.datetime] = None
    # Created side effects when available from the run memory projection.
    created_side_effects: Optional[list[str]] = None
    # Search result identifier. For interactive agent runs, this is normally the conversation-backed run ID.
    id: Optional[str] = None
    # Concise answer/action summary when available. Currently projected from the run memory summary.
    output_summary: Optional[str] = None
    # Best available prompt-like text for display.
    prompt: Optional[str] = None
    # Relevance score for search-backed run-memory results.
    relevance: Optional[float] = None
    # Durable run ID. Recent run-control endpoints can use this ID while the recent run record is still retained.
    run_id: Optional[str] = None
    # Generated run memory summary when available.
    summary: Optional[str] = None
    # Conversation or run title when available.
    title: Optional[str] = None
    # Tool call count when available from run metadata.
    tool_calls: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> RunSearchResult:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: RunSearchResult
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return RunSearchResult()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .run_search_result_agent import RunSearchResult_agent

        from .run_search_result_agent import RunSearchResult_agent

        fields: dict[str, Callable[[Any], None]] = {
            "agent": lambda n : setattr(self, 'agent', n.get_object_value(RunSearchResult_agent)),
            "completed_at": lambda n : setattr(self, 'completed_at', n.get_datetime_value()),
            "conversation_id": lambda n : setattr(self, 'conversation_id', n.get_str_value()),
            "created_at": lambda n : setattr(self, 'created_at', n.get_datetime_value()),
            "created_side_effects": lambda n : setattr(self, 'created_side_effects', n.get_collection_of_primitive_values(str)),
            "id": lambda n : setattr(self, 'id', n.get_str_value()),
            "output_summary": lambda n : setattr(self, 'output_summary', n.get_str_value()),
            "prompt": lambda n : setattr(self, 'prompt', n.get_str_value()),
            "relevance": lambda n : setattr(self, 'relevance', n.get_float_value()),
            "run_id": lambda n : setattr(self, 'run_id', n.get_str_value()),
            "summary": lambda n : setattr(self, 'summary', n.get_str_value()),
            "title": lambda n : setattr(self, 'title', n.get_str_value()),
            "tool_calls": lambda n : setattr(self, 'tool_calls', n.get_int_value()),
        }
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if writer is None:
            raise TypeError("writer cannot be null.")
        writer.write_object_value("agent", self.agent)
        writer.write_datetime_value("completed_at", self.completed_at)
        writer.write_str_value("conversation_id", self.conversation_id)
        writer.write_datetime_value("created_at", self.created_at)
        writer.write_collection_of_primitive_values("created_side_effects", self.created_side_effects)
        writer.write_str_value("id", self.id)
        writer.write_str_value("output_summary", self.output_summary)
        writer.write_str_value("prompt", self.prompt)
        writer.write_str_value("run_id", self.run_id)
        writer.write_str_value("summary", self.summary)
        writer.write_str_value("title", self.title)
        writer.write_int_value("tool_calls", self.tool_calls)
    

