from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .data_source import DataSource

@dataclass
class DataSourceCreateResult(Parsable):
    # The created property
    created: Optional[bool] = None
    # The source property
    source: Optional[DataSource] = None
    # The sources property
    sources: Optional[list[DataSource]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> DataSourceCreateResult:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DataSourceCreateResult
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return DataSourceCreateResult()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .data_source import DataSource

        from .data_source import DataSource

        fields: dict[str, Callable[[Any], None]] = {
            "created": lambda n : setattr(self, 'created', n.get_bool_value()),
            "source": lambda n : setattr(self, 'source', n.get_object_value(DataSource)),
            "sources": lambda n : setattr(self, 'sources', n.get_collection_of_object_values(DataSource)),
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
        writer.write_bool_value("created", self.created)
        writer.write_object_value("source", self.source)
        writer.write_collection_of_object_values("sources", self.sources)
    

