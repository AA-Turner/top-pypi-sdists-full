from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class DataSourceDiscoverRequest(Parsable):
    # The account property
    account: Optional[str] = None
    # The database property
    database: Optional[str] = None
    # The drive property
    drive: Optional[str] = None
    # The library property
    library: Optional[str] = None
    # The search property
    search: Optional[str] = None
    # The site property
    site: Optional[str] = None
    # The team property
    team: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> DataSourceDiscoverRequest:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DataSourceDiscoverRequest
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return DataSourceDiscoverRequest()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "account": lambda n : setattr(self, 'account', n.get_str_value()),
            "database": lambda n : setattr(self, 'database', n.get_str_value()),
            "drive": lambda n : setattr(self, 'drive', n.get_str_value()),
            "library": lambda n : setattr(self, 'library', n.get_str_value()),
            "search": lambda n : setattr(self, 'search', n.get_str_value()),
            "site": lambda n : setattr(self, 'site', n.get_str_value()),
            "team": lambda n : setattr(self, 'team', n.get_str_value()),
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
        writer.write_str_value("account", self.account)
        writer.write_str_value("database", self.database)
        writer.write_str_value("drive", self.drive)
        writer.write_str_value("library", self.library)
        writer.write_str_value("search", self.search)
        writer.write_str_value("site", self.site)
        writer.write_str_value("team", self.team)
    

