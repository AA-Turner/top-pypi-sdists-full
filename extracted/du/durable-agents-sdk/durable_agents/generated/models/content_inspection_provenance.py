from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .content_inspection_provenance_source import ContentInspectionProvenance_source

@dataclass
class ContentInspectionProvenance(Parsable):
    # The reused_existing_data property
    reused_existing_data: Optional[bool] = None
    # The source property
    source: Optional[ContentInspectionProvenance_source] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ContentInspectionProvenance:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ContentInspectionProvenance
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ContentInspectionProvenance()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .content_inspection_provenance_source import ContentInspectionProvenance_source

        from .content_inspection_provenance_source import ContentInspectionProvenance_source

        fields: dict[str, Callable[[Any], None]] = {
            "reused_existing_data": lambda n : setattr(self, 'reused_existing_data', n.get_bool_value()),
            "source": lambda n : setattr(self, 'source', n.get_enum_value(ContentInspectionProvenance_source)),
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
        writer.write_bool_value("reused_existing_data", self.reused_existing_data)
        writer.write_enum_value("source", self.source)
    

