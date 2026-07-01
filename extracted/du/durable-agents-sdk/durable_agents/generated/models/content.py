from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .content_source_metadata import Content_source_metadata
    from .content_type import ContentType
    from .entity_state import EntityState
    from .file_type import FileType
    from .named_ref import NamedRef

@dataclass
class Content(Parsable):
    # Graphlit collection memberships associated with the content. Collections may be addressed in VFS as `/library/collections/<collection-ref>`.
    collections: Optional[list[NamedRef]] = None
    # Date the content was added to the Library. Used when filtering with `date_mode=added`.
    created_at: Optional[datetime.datetime] = None
    # The creation_date property
    creation_date: Optional[datetime.datetime] = None
    # The custom_summary property
    custom_summary: Optional[str] = None
    # The file_creation_date property
    file_creation_date: Optional[datetime.datetime] = None
    # The file_extension property
    file_extension: Optional[str] = None
    # The file_modified_date property
    file_modified_date: Optional[datetime.datetime] = None
    # The file_name property
    file_name: Optional[str] = None
    # The file_type property
    file_type: Optional[FileType] = None
    # The finished_date property
    finished_date: Optional[datetime.datetime] = None
    # The format property
    format: Optional[str] = None
    # The format_name property
    format_name: Optional[str] = None
    # The id property
    id: Optional[str] = None
    # The identifier property
    identifier: Optional[str] = None
    # Graphlit-owned labels associated with the content. Labels may be addressed in VFS as `/library/labels/<label-ref>`.
    labels: Optional[list[str]] = None
    # The mime_type property
    mime_type: Optional[str] = None
    # The modified_date property
    modified_date: Optional[datetime.datetime] = None
    # The name property
    name: Optional[str] = None
    # Original/authored metadata date for the content. Used when filtering with `date_mode=authored`.
    original_date: Optional[datetime.datetime] = None
    # Graphlit relevance score for search-backed content results. Null for non-search responses or when Graphlit does not provide a score.
    relevance: Optional[float] = None
    # The source property
    source: Optional[NamedRef] = None
    # The source_metadata property
    source_metadata: Optional[Content_source_metadata] = None
    # The state property
    state: Optional[EntityState] = None
    # The summary property
    summary: Optional[str] = None
    # The type property
    type: Optional[ContentType] = None
    # The updated_at property
    updated_at: Optional[datetime.datetime] = None
    # The uri property
    uri: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Content:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Content
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Content()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .content_source_metadata import Content_source_metadata
        from .content_type import ContentType
        from .entity_state import EntityState
        from .file_type import FileType
        from .named_ref import NamedRef

        from .content_source_metadata import Content_source_metadata
        from .content_type import ContentType
        from .entity_state import EntityState
        from .file_type import FileType
        from .named_ref import NamedRef

        fields: dict[str, Callable[[Any], None]] = {
            "collections": lambda n : setattr(self, 'collections', n.get_collection_of_object_values(NamedRef)),
            "created_at": lambda n : setattr(self, 'created_at', n.get_datetime_value()),
            "creation_date": lambda n : setattr(self, 'creation_date', n.get_datetime_value()),
            "custom_summary": lambda n : setattr(self, 'custom_summary', n.get_str_value()),
            "file_creation_date": lambda n : setattr(self, 'file_creation_date', n.get_datetime_value()),
            "file_extension": lambda n : setattr(self, 'file_extension', n.get_str_value()),
            "file_modified_date": lambda n : setattr(self, 'file_modified_date', n.get_datetime_value()),
            "file_name": lambda n : setattr(self, 'file_name', n.get_str_value()),
            "file_type": lambda n : setattr(self, 'file_type', n.get_enum_value(FileType)),
            "finished_date": lambda n : setattr(self, 'finished_date', n.get_datetime_value()),
            "format": lambda n : setattr(self, 'format', n.get_str_value()),
            "format_name": lambda n : setattr(self, 'format_name', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_str_value()),
            "identifier": lambda n : setattr(self, 'identifier', n.get_str_value()),
            "labels": lambda n : setattr(self, 'labels', n.get_collection_of_primitive_values(str)),
            "mime_type": lambda n : setattr(self, 'mime_type', n.get_str_value()),
            "modified_date": lambda n : setattr(self, 'modified_date', n.get_datetime_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "original_date": lambda n : setattr(self, 'original_date', n.get_datetime_value()),
            "relevance": lambda n : setattr(self, 'relevance', n.get_float_value()),
            "source": lambda n : setattr(self, 'source', n.get_object_value(NamedRef)),
            "source_metadata": lambda n : setattr(self, 'source_metadata', n.get_object_value(Content_source_metadata)),
            "state": lambda n : setattr(self, 'state', n.get_enum_value(EntityState)),
            "summary": lambda n : setattr(self, 'summary', n.get_str_value()),
            "type": lambda n : setattr(self, 'type', n.get_enum_value(ContentType)),
            "updated_at": lambda n : setattr(self, 'updated_at', n.get_datetime_value()),
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
        writer.write_collection_of_object_values("collections", self.collections)
        writer.write_datetime_value("created_at", self.created_at)
        writer.write_datetime_value("creation_date", self.creation_date)
        writer.write_datetime_value("file_creation_date", self.file_creation_date)
        writer.write_str_value("file_extension", self.file_extension)
        writer.write_datetime_value("file_modified_date", self.file_modified_date)
        writer.write_str_value("file_name", self.file_name)
        writer.write_enum_value("file_type", self.file_type)
        writer.write_datetime_value("finished_date", self.finished_date)
        writer.write_str_value("format", self.format)
        writer.write_str_value("format_name", self.format_name)
        writer.write_str_value("id", self.id)
        writer.write_str_value("identifier", self.identifier)
        writer.write_collection_of_primitive_values("labels", self.labels)
        writer.write_str_value("mime_type", self.mime_type)
        writer.write_datetime_value("modified_date", self.modified_date)
        writer.write_str_value("name", self.name)
        writer.write_datetime_value("original_date", self.original_date)
        writer.write_object_value("source", self.source)
        writer.write_object_value("source_metadata", self.source_metadata)
        writer.write_enum_value("state", self.state)
        writer.write_enum_value("type", self.type)
        writer.write_datetime_value("updated_at", self.updated_at)
        writer.write_str_value("uri", self.uri)
    

