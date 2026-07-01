from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class EmailMessageSummary(Parsable):
    # The attachments_count property
    attachments_count: Optional[int] = None
    # The bcc property
    bcc: Optional[list[str]] = None
    # The cc property
    cc: Optional[list[str]] = None
    # The created_at property
    created_at: Optional[datetime.datetime] = None
    # The from property
    from_: Optional[str] = None
    # The id property
    id: Optional[str] = None
    # The in_reply_to property
    in_reply_to: Optional[str] = None
    # The inbox_id property
    inbox_id: Optional[str] = None
    # The labels property
    labels: Optional[list[str]] = None
    # The preview property
    preview: Optional[str] = None
    # The references property
    references: Optional[list[str]] = None
    # The reply_to property
    reply_to: Optional[list[str]] = None
    # The size property
    size: Optional[int] = None
    # The subject property
    subject: Optional[str] = None
    # The thread_id property
    thread_id: Optional[str] = None
    # The timestamp property
    timestamp: Optional[datetime.datetime] = None
    # The to property
    to: Optional[list[str]] = None
    # The updated_at property
    updated_at: Optional[datetime.datetime] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> EmailMessageSummary:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: EmailMessageSummary
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return EmailMessageSummary()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "attachments_count": lambda n : setattr(self, 'attachments_count', n.get_int_value()),
            "bcc": lambda n : setattr(self, 'bcc', n.get_collection_of_primitive_values(str)),
            "cc": lambda n : setattr(self, 'cc', n.get_collection_of_primitive_values(str)),
            "created_at": lambda n : setattr(self, 'created_at', n.get_datetime_value()),
            "from": lambda n : setattr(self, 'from_', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_str_value()),
            "in_reply_to": lambda n : setattr(self, 'in_reply_to', n.get_str_value()),
            "inbox_id": lambda n : setattr(self, 'inbox_id', n.get_str_value()),
            "labels": lambda n : setattr(self, 'labels', n.get_collection_of_primitive_values(str)),
            "preview": lambda n : setattr(self, 'preview', n.get_str_value()),
            "references": lambda n : setattr(self, 'references', n.get_collection_of_primitive_values(str)),
            "reply_to": lambda n : setattr(self, 'reply_to', n.get_collection_of_primitive_values(str)),
            "size": lambda n : setattr(self, 'size', n.get_int_value()),
            "subject": lambda n : setattr(self, 'subject', n.get_str_value()),
            "thread_id": lambda n : setattr(self, 'thread_id', n.get_str_value()),
            "timestamp": lambda n : setattr(self, 'timestamp', n.get_datetime_value()),
            "to": lambda n : setattr(self, 'to', n.get_collection_of_primitive_values(str)),
            "updated_at": lambda n : setattr(self, 'updated_at', n.get_datetime_value()),
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
        writer.write_int_value("attachments_count", self.attachments_count)
        writer.write_collection_of_primitive_values("bcc", self.bcc)
        writer.write_collection_of_primitive_values("cc", self.cc)
        writer.write_datetime_value("created_at", self.created_at)
        writer.write_str_value("from", self.from_)
        writer.write_str_value("id", self.id)
        writer.write_str_value("in_reply_to", self.in_reply_to)
        writer.write_str_value("inbox_id", self.inbox_id)
        writer.write_collection_of_primitive_values("labels", self.labels)
        writer.write_str_value("preview", self.preview)
        writer.write_collection_of_primitive_values("references", self.references)
        writer.write_collection_of_primitive_values("reply_to", self.reply_to)
        writer.write_int_value("size", self.size)
        writer.write_str_value("subject", self.subject)
        writer.write_str_value("thread_id", self.thread_id)
        writer.write_datetime_value("timestamp", self.timestamp)
        writer.write_collection_of_primitive_values("to", self.to)
        writer.write_datetime_value("updated_at", self.updated_at)
    

