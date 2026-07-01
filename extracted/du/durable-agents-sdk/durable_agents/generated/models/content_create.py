from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class ContentCreate(Parsable):
    """
    Create content from a URL or text body. Durable API validates the required fields for each ingest mode.
    """
    # Graphlit collection GUIDs or unique names to attach.
    collections: Optional[list[str]] = None
    # Graphlit labels to attach by name.
    labels: Optional[list[str]] = None
    # The name property
    name: Optional[str] = None
    # The text property
    text: Optional[str] = None
    # The url property
    url: Optional[str] = None
    # Wait for synchronous ingest before returning.
    wait: Optional[bool] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ContentCreate:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ContentCreate
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ContentCreate()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "collections": lambda n : setattr(self, 'collections', n.get_collection_of_primitive_values(str)),
            "labels": lambda n : setattr(self, 'labels', n.get_collection_of_primitive_values(str)),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "text": lambda n : setattr(self, 'text', n.get_str_value()),
            "url": lambda n : setattr(self, 'url', n.get_str_value()),
            "wait": lambda n : setattr(self, 'wait', n.get_bool_value()),
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
        writer.write_collection_of_primitive_values("collections", self.collections)
        writer.write_collection_of_primitive_values("labels", self.labels)
        writer.write_str_value("name", self.name)
        writer.write_str_value("text", self.text)
        writer.write_str_value("url", self.url)
        writer.write_bool_value("wait", self.wait)
    

