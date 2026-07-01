from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .ref import Ref

@dataclass
class WebhookAck(Parsable):
    # The accepted property
    accepted: Optional[bool] = None
    # The run property
    run: Optional[Ref] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> WebhookAck:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: WebhookAck
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return WebhookAck()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .ref import Ref

        from .ref import Ref

        fields: dict[str, Callable[[Any], None]] = {
            "accepted": lambda n : setattr(self, 'accepted', n.get_bool_value()),
            "run": lambda n : setattr(self, 'run', n.get_object_value(Ref)),
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
        writer.write_bool_value("accepted", self.accepted)
        writer.write_object_value("run", self.run)
    

