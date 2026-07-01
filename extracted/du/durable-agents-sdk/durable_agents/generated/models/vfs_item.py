from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .content import Content
    from .vfs_body import VfsBody
    from .vfs_children import VfsChildren
    from .vfs_entry import VfsEntry

@dataclass
class VfsItem(Parsable):
    # The body property
    body: Optional[VfsBody] = None
    # The children property
    children: Optional[VfsChildren] = None
    # The content property
    content: Optional[Content] = None
    # Derived read-only Library VFS entry. Directory entries are synthesized from the navigation root, the flat contents view, Graphlit labels, collections, public kind values, mentions, and sources; they are not persisted Durable folders.
    entry: Optional[VfsEntry] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> VfsItem:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: VfsItem
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return VfsItem()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .content import Content
        from .vfs_body import VfsBody
        from .vfs_children import VfsChildren
        from .vfs_entry import VfsEntry

        from .content import Content
        from .vfs_body import VfsBody
        from .vfs_children import VfsChildren
        from .vfs_entry import VfsEntry

        fields: dict[str, Callable[[Any], None]] = {
            "body": lambda n : setattr(self, 'body', n.get_object_value(VfsBody)),
            "children": lambda n : setattr(self, 'children', n.get_object_value(VfsChildren)),
            "content": lambda n : setattr(self, 'content', n.get_object_value(Content)),
            "entry": lambda n : setattr(self, 'entry', n.get_object_value(VfsEntry)),
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
        writer.write_object_value("body", self.body)
        writer.write_object_value("children", self.children)
        writer.write_object_value("content", self.content)
        writer.write_object_value("entry", self.entry)
    

