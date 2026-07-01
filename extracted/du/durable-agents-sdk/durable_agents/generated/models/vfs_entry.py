from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .content_type import ContentType
    from .file_type import FileType
    from .named_ref import NamedRef
    from .vfs_entry_kind import VfsEntry_kind

@dataclass
class VfsEntry(Parsable):
    """
    Derived read-only Library VFS entry. Directory entries are synthesized from the navigation root, the flat contents view, Graphlit labels, collections, public kind values, mentions, and sources; they are not persisted Durable folders.
    """
    # Optional friendly alias paths, such as unique display-name paths for entity-backed folders.
    aliases: Optional[list[str]] = None
    # Canonical GUID-backed path when the entry was reached through a friendly name alias. For content entries this is `/library/<content-id>`.
    canonical_path: Optional[str] = None
    # The collections property
    collections: Optional[list[NamedRef]] = None
    # The content_id property
    content_id: Optional[str] = None
    # The created_at property
    created_at: Optional[datetime.datetime] = None
    # Parent derived VFS directory path.
    directory_path: Optional[str] = None
    # The file_type property
    file_type: Optional[FileType] = None
    # The kind property
    kind: Optional[VfsEntry_kind] = None
    # The labels property
    labels: Optional[list[str]] = None
    # The mime_type property
    mime_type: Optional[str] = None
    # The name property
    name: Optional[str] = None
    # Derived VFS path. Content entries use canonical `/library/<content-id>` paths even when listed under `/library/contents` or a facet folder.
    path: Optional[str] = None
    # Graphlit GUID for entity-backed directory entries such as labels, collections, sources, or mention entities.
    ref_id: Optional[str] = None
    # The type property
    type: Optional[ContentType] = None
    # The updated_at property
    updated_at: Optional[datetime.datetime] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> VfsEntry:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: VfsEntry
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return VfsEntry()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .content_type import ContentType
        from .file_type import FileType
        from .named_ref import NamedRef
        from .vfs_entry_kind import VfsEntry_kind

        from .content_type import ContentType
        from .file_type import FileType
        from .named_ref import NamedRef
        from .vfs_entry_kind import VfsEntry_kind

        fields: dict[str, Callable[[Any], None]] = {
            "aliases": lambda n : setattr(self, 'aliases', n.get_collection_of_primitive_values(str)),
            "canonical_path": lambda n : setattr(self, 'canonical_path', n.get_str_value()),
            "collections": lambda n : setattr(self, 'collections', n.get_collection_of_object_values(NamedRef)),
            "content_id": lambda n : setattr(self, 'content_id', n.get_str_value()),
            "created_at": lambda n : setattr(self, 'created_at', n.get_datetime_value()),
            "directory_path": lambda n : setattr(self, 'directory_path', n.get_str_value()),
            "file_type": lambda n : setattr(self, 'file_type', n.get_enum_value(FileType)),
            "kind": lambda n : setattr(self, 'kind', n.get_enum_value(VfsEntry_kind)),
            "labels": lambda n : setattr(self, 'labels', n.get_collection_of_primitive_values(str)),
            "mime_type": lambda n : setattr(self, 'mime_type', n.get_str_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "path": lambda n : setattr(self, 'path', n.get_str_value()),
            "ref_id": lambda n : setattr(self, 'ref_id', n.get_str_value()),
            "type": lambda n : setattr(self, 'type', n.get_enum_value(ContentType)),
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
        writer.write_collection_of_primitive_values("aliases", self.aliases)
        writer.write_str_value("canonical_path", self.canonical_path)
        writer.write_collection_of_object_values("collections", self.collections)
        writer.write_str_value("content_id", self.content_id)
        writer.write_datetime_value("created_at", self.created_at)
        writer.write_str_value("directory_path", self.directory_path)
        writer.write_enum_value("file_type", self.file_type)
        writer.write_enum_value("kind", self.kind)
        writer.write_collection_of_primitive_values("labels", self.labels)
        writer.write_str_value("mime_type", self.mime_type)
        writer.write_str_value("name", self.name)
        writer.write_str_value("path", self.path)
        writer.write_str_value("ref_id", self.ref_id)
        writer.write_enum_value("type", self.type)
        writer.write_datetime_value("updated_at", self.updated_at)
    

