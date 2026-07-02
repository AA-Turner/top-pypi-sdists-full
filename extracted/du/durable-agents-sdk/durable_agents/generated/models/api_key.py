from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .ref import Ref
    from .user_ref import UserRef
    from .workspace_ref import WorkspaceRef

@dataclass
class ApiKey(Parsable):
    # The created_at property
    created_at: Optional[datetime.datetime] = None
    # The id property
    id: Optional[str] = None
    # The last_seen_at property
    last_seen_at: Optional[datetime.datetime] = None
    # The name property
    name: Optional[str] = None
    # The revoked_at property
    revoked_at: Optional[datetime.datetime] = None
    # The scopes property
    scopes: Optional[list[str]] = None
    # The tenant property
    tenant: Optional[Ref] = None
    # The user property
    user: Optional[UserRef] = None
    # The workspace property
    workspace: Optional[WorkspaceRef] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ApiKey:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ApiKey
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ApiKey()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .ref import Ref
        from .user_ref import UserRef
        from .workspace_ref import WorkspaceRef

        from .ref import Ref
        from .user_ref import UserRef
        from .workspace_ref import WorkspaceRef

        fields: dict[str, Callable[[Any], None]] = {
            "created_at": lambda n : setattr(self, 'created_at', n.get_datetime_value()),
            "id": lambda n : setattr(self, 'id', n.get_str_value()),
            "last_seen_at": lambda n : setattr(self, 'last_seen_at', n.get_datetime_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "revoked_at": lambda n : setattr(self, 'revoked_at', n.get_datetime_value()),
            "scopes": lambda n : setattr(self, 'scopes', n.get_collection_of_primitive_values(str)),
            "tenant": lambda n : setattr(self, 'tenant', n.get_object_value(Ref)),
            "user": lambda n : setattr(self, 'user', n.get_object_value(UserRef)),
            "workspace": lambda n : setattr(self, 'workspace', n.get_object_value(WorkspaceRef)),
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
        writer.write_str_value("id", self.id)
        writer.write_datetime_value("last_seen_at", self.last_seen_at)
        writer.write_str_value("name", self.name)
        writer.write_datetime_value("revoked_at", self.revoked_at)
        writer.write_collection_of_primitive_values("scopes", self.scopes)
        writer.write_object_value("tenant", self.tenant)
        writer.write_object_value("user", self.user)
        writer.write_object_value("workspace", self.workspace)
    

