from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .connector import Connector
    from .connector_mutation_result_authorize_url import ConnectorMutationResult_authorize_url

@dataclass
class ConnectorMutationResult(Parsable):
    # The authorization_required property
    authorization_required: Optional[bool] = None
    # The authorize_url property
    authorize_url: Optional[ConnectorMutationResult_authorize_url] = None
    # The connector property
    connector: Optional[Connector] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ConnectorMutationResult:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ConnectorMutationResult
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ConnectorMutationResult()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .connector import Connector
        from .connector_mutation_result_authorize_url import ConnectorMutationResult_authorize_url

        from .connector import Connector
        from .connector_mutation_result_authorize_url import ConnectorMutationResult_authorize_url

        fields: dict[str, Callable[[Any], None]] = {
            "authorization_required": lambda n : setattr(self, 'authorization_required', n.get_bool_value()),
            "authorize_url": lambda n : setattr(self, 'authorize_url', n.get_object_value(ConnectorMutationResult_authorize_url)),
            "connector": lambda n : setattr(self, 'connector', n.get_object_value(Connector)),
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
        writer.write_bool_value("authorization_required", self.authorization_required)
        writer.write_object_value("authorize_url", self.authorize_url)
        writer.write_object_value("connector", self.connector)
    

