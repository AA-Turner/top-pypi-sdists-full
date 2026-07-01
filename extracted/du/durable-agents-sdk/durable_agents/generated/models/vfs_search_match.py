from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .content_type import ContentType
    from .file_type import FileType
    from .named_ref import NamedRef

@dataclass
class VfsSearchMatch(Parsable):
    """
    Search match returned from a Graphlit-derived VFS scope. Match paths are canonical content paths, not `/library/contents` or facet-owned nested paths.
    """
    # The collections property
    collections: Optional[list[NamedRef]] = None
    # The content_id property
    content_id: Optional[str] = None
    # Derived VFS scope that produced the match.
    directory_path: Optional[str] = None
    # The file_type property
    file_type: Optional[FileType] = None
    # The labels property
    labels: Optional[list[str]] = None
    # The mime_type property
    mime_type: Optional[str] = None
    # The name property
    name: Optional[str] = None
    # Canonical content path in `/library/<content-id>` form.
    path: Optional[str] = None
    # The score property
    score: Optional[float] = None
    # The snippet property
    snippet: Optional[str] = None
    # The type property
    type: Optional[ContentType] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> VfsSearchMatch:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: VfsSearchMatch
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return VfsSearchMatch()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .content_type import ContentType
        from .file_type import FileType
        from .named_ref import NamedRef

        from .content_type import ContentType
        from .file_type import FileType
        from .named_ref import NamedRef

        fields: dict[str, Callable[[Any], None]] = {
            "collections": lambda n : setattr(self, 'collections', n.get_collection_of_object_values(NamedRef)),
            "content_id": lambda n : setattr(self, 'content_id', n.get_str_value()),
            "directory_path": lambda n : setattr(self, 'directory_path', n.get_str_value()),
            "file_type": lambda n : setattr(self, 'file_type', n.get_enum_value(FileType)),
            "labels": lambda n : setattr(self, 'labels', n.get_collection_of_primitive_values(str)),
            "mime_type": lambda n : setattr(self, 'mime_type', n.get_str_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "path": lambda n : setattr(self, 'path', n.get_str_value()),
            "score": lambda n : setattr(self, 'score', n.get_float_value()),
            "snippet": lambda n : setattr(self, 'snippet', n.get_str_value()),
            "type": lambda n : setattr(self, 'type', n.get_enum_value(ContentType)),
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
        writer.write_str_value("content_id", self.content_id)
        writer.write_str_value("directory_path", self.directory_path)
        writer.write_enum_value("file_type", self.file_type)
        writer.write_collection_of_primitive_values("labels", self.labels)
        writer.write_str_value("mime_type", self.mime_type)
        writer.write_str_value("name", self.name)
        writer.write_str_value("path", self.path)
        writer.write_float_value("score", self.score)
        writer.write_str_value("snippet", self.snippet)
        writer.write_enum_value("type", self.type)
    

