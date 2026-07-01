from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .email_inbox_status import EmailInbox_status

@dataclass
class EmailInbox(Parsable):
    # The created_at property
    created_at: Optional[datetime.datetime] = None
    # The email property
    email: Optional[str] = None
    # The id property
    id: Optional[str] = None
    # The status property
    status: Optional[EmailInbox_status] = None
    # The username property
    username: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> EmailInbox:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: EmailInbox
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return EmailInbox()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .email_inbox_status import EmailInbox_status

        from .email_inbox_status import EmailInbox_status

        fields: dict[str, Callable[[Any], None]] = {
            "created_at": lambda n : setattr(self, 'created_at', n.get_datetime_value()),
            "email": lambda n : setattr(self, 'email', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_str_value()),
            "status": lambda n : setattr(self, 'status', n.get_enum_value(EmailInbox_status)),
            "username": lambda n : setattr(self, 'username', n.get_str_value()),
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
        writer.write_datetime_value("created_at", self.created_at)
        writer.write_str_value("email", self.email)
        writer.write_str_value("id", self.id)
        writer.write_enum_value("status", self.status)
        writer.write_str_value("username", self.username)
    

