from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class EmailMessageAttachment(Parsable):
    # The content_disposition property
    content_disposition: Optional[str] = None
    # The content_id property
    content_id: Optional[str] = None
    # The content_type property
    content_type: Optional[str] = None
    # The filename property
    filename: Optional[str] = None
    # The id property
    id: Optional[str] = None
    # The size property
    size: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> EmailMessageAttachment:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: EmailMessageAttachment
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return EmailMessageAttachment()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "content_disposition": lambda n : setattr(self, 'content_disposition', n.get_str_value()),
            "content_id": lambda n : setattr(self, 'content_id', n.get_str_value()),
            "content_type": lambda n : setattr(self, 'content_type', n.get_str_value()),
            "filename": lambda n : setattr(self, 'filename', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_str_value()),
            "size": lambda n : setattr(self, 'size', n.get_int_value()),
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
        writer.write_str_value("content_disposition", self.content_disposition)
        writer.write_str_value("content_id", self.content_id)
        writer.write_str_value("content_type", self.content_type)
        writer.write_str_value("filename", self.filename)
        writer.write_str_value("id", self.id)
        writer.write_int_value("size", self.size)
    

