from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .email_message_attachment import EmailMessageAttachment
    from .email_message_headers import EmailMessage_headers
    from .email_message_summary import EmailMessageSummary

from .email_message_summary import EmailMessageSummary

@dataclass
class EmailMessage(EmailMessageSummary, AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The attachments property
    attachments: Optional[list[EmailMessageAttachment]] = None
    # The extracted_html property
    extracted_html: Optional[str] = None
    # The extracted_text property
    extracted_text: Optional[str] = None
    # The headers property
    headers: Optional[EmailMessage_headers] = None
    # The html property
    html: Optional[str] = None
    # The text property
    text: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> EmailMessage:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: EmailMessage
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return EmailMessage()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .email_message_attachment import EmailMessageAttachment
        from .email_message_headers import EmailMessage_headers
        from .email_message_summary import EmailMessageSummary

        from .email_message_attachment import EmailMessageAttachment
        from .email_message_headers import EmailMessage_headers
        from .email_message_summary import EmailMessageSummary

        fields: dict[str, Callable[[Any], None]] = {
            "attachments": lambda n : setattr(self, 'attachments', n.get_collection_of_object_values(EmailMessageAttachment)),
            "extracted_html": lambda n : setattr(self, 'extracted_html', n.get_str_value()),
            "extracted_text": lambda n : setattr(self, 'extracted_text', n.get_str_value()),
            "headers": lambda n : setattr(self, 'headers', n.get_object_value(EmailMessage_headers)),
            "html": lambda n : setattr(self, 'html', n.get_str_value()),
            "text": lambda n : setattr(self, 'text', n.get_str_value()),
        }
        super_fields = super().get_field_deserializers()
        fields.update(super_fields)
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if writer is None:
            raise TypeError("writer cannot be null.")
        super().serialize(writer)
        writer.write_collection_of_object_values("attachments", self.attachments)
        writer.write_str_value("extracted_html", self.extracted_html)
        writer.write_str_value("extracted_text", self.extracted_text)
        writer.write_object_value("headers", self.headers)
        writer.write_str_value("html", self.html)
        writer.write_str_value("text", self.text)
        writer.write_additional_data_value(self.additional_data)
    

