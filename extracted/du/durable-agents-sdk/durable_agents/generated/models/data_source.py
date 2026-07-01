from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .data_source_account import DataSource_account
    from .data_source_read_count import DataSource_read_count
    from .data_source_read_limit import DataSource_read_limit
    from .data_source_resource import DataSourceResource
    from .data_source_schedule import DataSourceSchedule
    from .data_source_status import DataSourceStatus
    from .data_source_type import DataSourceType

@dataclass
class DataSource(Parsable):
    # The account property
    account: Optional[DataSource_account] = None
    # The created_at property
    created_at: Optional[datetime.datetime] = None
    # The id property
    id: Optional[str] = None
    # The name property
    name: Optional[str] = None
    # The read_count property
    read_count: Optional[DataSource_read_count] = None
    # The read_limit property
    read_limit: Optional[DataSource_read_limit] = None
    # The resource property
    resource: Optional[DataSourceResource] = None
    # The schedule property
    schedule: Optional[DataSourceSchedule] = None
    # The status property
    status: Optional[DataSourceStatus] = None
    # The type property
    type: Optional[DataSourceType] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> DataSource:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DataSource
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return DataSource()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .data_source_account import DataSource_account
        from .data_source_read_count import DataSource_read_count
        from .data_source_read_limit import DataSource_read_limit
        from .data_source_resource import DataSourceResource
        from .data_source_schedule import DataSourceSchedule
        from .data_source_status import DataSourceStatus
        from .data_source_type import DataSourceType

        from .data_source_account import DataSource_account
        from .data_source_read_count import DataSource_read_count
        from .data_source_read_limit import DataSource_read_limit
        from .data_source_resource import DataSourceResource
        from .data_source_schedule import DataSourceSchedule
        from .data_source_status import DataSourceStatus
        from .data_source_type import DataSourceType

        fields: dict[str, Callable[[Any], None]] = {
            "account": lambda n : setattr(self, 'account', n.get_object_value(DataSource_account)),
            "created_at": lambda n : setattr(self, 'created_at', n.get_datetime_value()),
            "id": lambda n : setattr(self, 'id', n.get_str_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "read_count": lambda n : setattr(self, 'read_count', n.get_object_value(DataSource_read_count)),
            "read_limit": lambda n : setattr(self, 'read_limit', n.get_object_value(DataSource_read_limit)),
            "resource": lambda n : setattr(self, 'resource', n.get_object_value(DataSourceResource)),
            "schedule": lambda n : setattr(self, 'schedule', n.get_enum_value(DataSourceSchedule)),
            "status": lambda n : setattr(self, 'status', n.get_enum_value(DataSourceStatus)),
            "type": lambda n : setattr(self, 'type', n.get_enum_value(DataSourceType)),
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
        writer.write_object_value("account", self.account)
        writer.write_datetime_value("created_at", self.created_at)
        writer.write_str_value("id", self.id)
        writer.write_str_value("name", self.name)
        writer.write_object_value("read_count", self.read_count)
        writer.write_object_value("read_limit", self.read_limit)
        writer.write_object_value("resource", self.resource)
        writer.write_enum_value("schedule", self.schedule)
        writer.write_enum_value("status", self.status)
        writer.write_enum_value("type", self.type)
    

