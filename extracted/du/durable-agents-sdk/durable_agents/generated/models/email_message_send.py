from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class EmailMessageSend(Parsable):
    # The bcc property
    bcc: Optional[list[str]] = None
    # The cc property
    cc: Optional[list[str]] = None
    # The html property
    html: Optional[str] = None
    # The reply_to property
    reply_to: Optional[list[str]] = None
    # The subject property
    subject: Optional[str] = None
    # The text property
    text: Optional[str] = None
    # The to property
    to: Optional[list[str]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> EmailMessageSend:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: EmailMessageSend
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return EmailMessageSend()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "bcc": lambda n : setattr(self, 'bcc', n.get_collection_of_primitive_values(str)),
            "cc": lambda n : setattr(self, 'cc', n.get_collection_of_primitive_values(str)),
            "html": lambda n : setattr(self, 'html', n.get_str_value()),
            "reply_to": lambda n : setattr(self, 'reply_to', n.get_collection_of_primitive_values(str)),
            "subject": lambda n : setattr(self, 'subject', n.get_str_value()),
            "text": lambda n : setattr(self, 'text', n.get_str_value()),
            "to": lambda n : setattr(self, 'to', n.get_collection_of_primitive_values(str)),
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
        writer.write_collection_of_primitive_values("bcc", self.bcc)
        writer.write_collection_of_primitive_values("cc", self.cc)
        writer.write_str_value("html", self.html)
        writer.write_collection_of_primitive_values("reply_to", self.reply_to)
        writer.write_str_value("subject", self.subject)
        writer.write_str_value("text", self.text)
        writer.write_collection_of_primitive_values("to", self.to)
    

