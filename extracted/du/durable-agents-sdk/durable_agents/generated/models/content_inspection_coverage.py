from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .content_inspection_coverage_source_kind import ContentInspectionCoverage_source_kind
    from .content_inspection_coverage_status import ContentInspectionCoverage_status

@dataclass
class ContentInspectionCoverage(Parsable):
    # The full_text_available property
    full_text_available: Optional[bool] = None
    # The returned_chars property
    returned_chars: Optional[int] = None
    # The source_kind property
    source_kind: Optional[ContentInspectionCoverage_source_kind] = None
    # The status property
    status: Optional[ContentInspectionCoverage_status] = None
    # The total_chars property
    total_chars: Optional[int] = None
    # The truncation_reason property
    truncation_reason: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ContentInspectionCoverage:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ContentInspectionCoverage
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ContentInspectionCoverage()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .content_inspection_coverage_source_kind import ContentInspectionCoverage_source_kind
        from .content_inspection_coverage_status import ContentInspectionCoverage_status

        from .content_inspection_coverage_source_kind import ContentInspectionCoverage_source_kind
        from .content_inspection_coverage_status import ContentInspectionCoverage_status

        fields: dict[str, Callable[[Any], None]] = {
            "full_text_available": lambda n : setattr(self, 'full_text_available', n.get_bool_value()),
            "returned_chars": lambda n : setattr(self, 'returned_chars', n.get_int_value()),
            "source_kind": lambda n : setattr(self, 'source_kind', n.get_enum_value(ContentInspectionCoverage_source_kind)),
            "status": lambda n : setattr(self, 'status', n.get_enum_value(ContentInspectionCoverage_status)),
            "total_chars": lambda n : setattr(self, 'total_chars', n.get_int_value()),
            "truncation_reason": lambda n : setattr(self, 'truncation_reason', n.get_str_value()),
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
        writer.write_bool_value("full_text_available", self.full_text_available)
        writer.write_int_value("returned_chars", self.returned_chars)
        writer.write_enum_value("source_kind", self.source_kind)
        writer.write_enum_value("status", self.status)
        writer.write_int_value("total_chars", self.total_chars)
        writer.write_str_value("truncation_reason", self.truncation_reason)
    

