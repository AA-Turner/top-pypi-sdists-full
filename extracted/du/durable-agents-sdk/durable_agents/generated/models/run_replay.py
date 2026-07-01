from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .run import Run
    from .run_event import RunEvent

@dataclass
class RunReplay(Parsable):
    # The events property
    events: Optional[list[RunEvent]] = None
    # The run property
    run: Optional[Run] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> RunReplay:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: RunReplay
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return RunReplay()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .run import Run
        from .run_event import RunEvent

        from .run import Run
        from .run_event import RunEvent

        fields: dict[str, Callable[[Any], None]] = {
            "events": lambda n : setattr(self, 'events', n.get_collection_of_object_values(RunEvent)),
            "run": lambda n : setattr(self, 'run', n.get_object_value(Run)),
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
        writer.write_collection_of_object_values("events", self.events)
        writer.write_object_value("run", self.run)
    

