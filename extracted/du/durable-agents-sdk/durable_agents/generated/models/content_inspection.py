from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .content import Content
    from .content_inspection_coverage import ContentInspectionCoverage
    from .content_inspection_metadata import ContentInspection_metadata
    from .content_inspection_provenance import ContentInspectionProvenance
    from .content_inspection_ref import ContentInspectionRef
    from .content_inspection_resource_type import ContentInspection_resource_type

@dataclass
class ContentInspection(Parsable):
    # The children property
    children: Optional[list[ContentInspectionRef]] = None
    # The content property
    content: Optional[Content] = None
    # The coverage property
    coverage: Optional[ContentInspectionCoverage] = None
    # The description property
    description: Optional[str] = None
    # The markdown property
    markdown: Optional[str] = None
    # The metadata property
    metadata: Optional[ContentInspection_metadata] = None
    # The mime_type property
    mime_type: Optional[str] = None
    # The name property
    name: Optional[str] = None
    # The parent property
    parent: Optional[ContentInspectionRef] = None
    # The provenance property
    provenance: Optional[ContentInspectionProvenance] = None
    # The resource_type property
    resource_type: Optional[ContentInspection_resource_type] = None
    # The summary property
    summary: Optional[str] = None
    # Selected rendered text for terminal inspection. This field is not locally truncated by the Durable CLI/API.
    text: Optional[str] = None
    # The uri property
    uri: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ContentInspection:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ContentInspection
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ContentInspection()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .content import Content
        from .content_inspection_coverage import ContentInspectionCoverage
        from .content_inspection_metadata import ContentInspection_metadata
        from .content_inspection_provenance import ContentInspectionProvenance
        from .content_inspection_ref import ContentInspectionRef
        from .content_inspection_resource_type import ContentInspection_resource_type

        from .content import Content
        from .content_inspection_coverage import ContentInspectionCoverage
        from .content_inspection_metadata import ContentInspection_metadata
        from .content_inspection_provenance import ContentInspectionProvenance
        from .content_inspection_ref import ContentInspectionRef
        from .content_inspection_resource_type import ContentInspection_resource_type

        fields: dict[str, Callable[[Any], None]] = {
            "children": lambda n : setattr(self, 'children', n.get_collection_of_object_values(ContentInspectionRef)),
            "content": lambda n : setattr(self, 'content', n.get_object_value(Content)),
            "coverage": lambda n : setattr(self, 'coverage', n.get_object_value(ContentInspectionCoverage)),
            "description": lambda n : setattr(self, 'description', n.get_str_value()),
            "markdown": lambda n : setattr(self, 'markdown', n.get_str_value()),
            "metadata": lambda n : setattr(self, 'metadata', n.get_object_value(ContentInspection_metadata)),
            "mime_type": lambda n : setattr(self, 'mime_type', n.get_str_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "parent": lambda n : setattr(self, 'parent', n.get_object_value(ContentInspectionRef)),
            "provenance": lambda n : setattr(self, 'provenance', n.get_object_value(ContentInspectionProvenance)),
            "resource_type": lambda n : setattr(self, 'resource_type', n.get_enum_value(ContentInspection_resource_type)),
            "summary": lambda n : setattr(self, 'summary', n.get_str_value()),
            "text": lambda n : setattr(self, 'text', n.get_str_value()),
            "uri": lambda n : setattr(self, 'uri', n.get_str_value()),
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
        writer.write_collection_of_object_values("children", self.children)
        writer.write_object_value("content", self.content)
        writer.write_object_value("coverage", self.coverage)
        writer.write_str_value("description", self.description)
        writer.write_str_value("markdown", self.markdown)
        writer.write_object_value("metadata", self.metadata)
        writer.write_str_value("mime_type", self.mime_type)
        writer.write_str_value("name", self.name)
        writer.write_object_value("parent", self.parent)
        writer.write_object_value("provenance", self.provenance)
        writer.write_enum_value("resource_type", self.resource_type)
        writer.write_str_value("summary", self.summary)
        writer.write_str_value("text", self.text)
        writer.write_str_value("uri", self.uri)
    

