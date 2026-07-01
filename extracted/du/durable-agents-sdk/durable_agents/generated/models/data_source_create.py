from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .data_source_resource_input import DataSourceResourceInput
    from .data_source_schedule import DataSourceSchedule
    from .data_source_type import DataSourceType

@dataclass
class DataSourceCreate(Parsable):
    # The access_key property
    access_key: Optional[str] = None
    # The account property
    account: Optional[str] = None
    # The account_name property
    account_name: Optional[str] = None
    # The api_key property
    api_key: Optional[str] = None
    # The auth_mode property
    auth_mode: Optional[str] = None
    # The branch property
    branch: Optional[str] = None
    # The bucket property
    bucket: Optional[str] = None
    # The client_id property
    client_id: Optional[str] = None
    # The client_secret property
    client_secret: Optional[str] = None
    # The container property
    container: Optional[str] = None
    # The endpoint property
    endpoint: Optional[str] = None
    # The filter property
    filter: Optional[str] = None
    # The include_attachments property
    include_attachments: Optional[bool] = None
    # The include_comments property
    include_comments: Optional[bool] = None
    # The include_files property
    include_files: Optional[bool] = None
    # The include_notes property
    include_notes: Optional[bool] = None
    # The is_sandbox property
    is_sandbox: Optional[bool] = None
    # The key property
    key: Optional[str] = None
    # The listing property
    listing: Optional[str] = None
    # The name property
    name: Optional[str] = None
    # The prefix property
    prefix: Optional[str] = None
    # The read_limit property
    read_limit: Optional[int] = None
    # The refresh_token property
    refresh_token: Optional[str] = None
    # The region property
    region: Optional[str] = None
    # The resource property
    resource: Optional[DataSourceResourceInput] = None
    # The schedule property
    schedule: Optional[DataSourceSchedule] = None
    # The secret_key property
    secret_key: Optional[str] = None
    # The state property
    state: Optional[str] = None
    # The storage_key property
    storage_key: Optional[str] = None
    # The subdomain property
    subdomain: Optional[str] = None
    # The token property
    token: Optional[str] = None
    # The type property
    type: Optional[DataSourceType] = None
    # The workspace property
    workspace: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> DataSourceCreate:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DataSourceCreate
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return DataSourceCreate()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .data_source_resource_input import DataSourceResourceInput
        from .data_source_schedule import DataSourceSchedule
        from .data_source_type import DataSourceType

        from .data_source_resource_input import DataSourceResourceInput
        from .data_source_schedule import DataSourceSchedule
        from .data_source_type import DataSourceType

        fields: dict[str, Callable[[Any], None]] = {
            "access_key": lambda n : setattr(self, 'access_key', n.get_str_value()),
            "account": lambda n : setattr(self, 'account', n.get_str_value()),
            "account_name": lambda n : setattr(self, 'account_name', n.get_str_value()),
            "api_key": lambda n : setattr(self, 'api_key', n.get_str_value()),
            "auth_mode": lambda n : setattr(self, 'auth_mode', n.get_str_value()),
            "branch": lambda n : setattr(self, 'branch', n.get_str_value()),
            "bucket": lambda n : setattr(self, 'bucket', n.get_str_value()),
            "client_id": lambda n : setattr(self, 'client_id', n.get_str_value()),
            "client_secret": lambda n : setattr(self, 'client_secret', n.get_str_value()),
            "container": lambda n : setattr(self, 'container', n.get_str_value()),
            "endpoint": lambda n : setattr(self, 'endpoint', n.get_str_value()),
            "filter": lambda n : setattr(self, 'filter', n.get_str_value()),
            "include_attachments": lambda n : setattr(self, 'include_attachments', n.get_bool_value()),
            "include_comments": lambda n : setattr(self, 'include_comments', n.get_bool_value()),
            "include_files": lambda n : setattr(self, 'include_files', n.get_bool_value()),
            "include_notes": lambda n : setattr(self, 'include_notes', n.get_bool_value()),
            "is_sandbox": lambda n : setattr(self, 'is_sandbox', n.get_bool_value()),
            "key": lambda n : setattr(self, 'key', n.get_str_value()),
            "listing": lambda n : setattr(self, 'listing', n.get_str_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "prefix": lambda n : setattr(self, 'prefix', n.get_str_value()),
            "read_limit": lambda n : setattr(self, 'read_limit', n.get_int_value()),
            "refresh_token": lambda n : setattr(self, 'refresh_token', n.get_str_value()),
            "region": lambda n : setattr(self, 'region', n.get_str_value()),
            "resource": lambda n : setattr(self, 'resource', n.get_object_value(DataSourceResourceInput)),
            "schedule": lambda n : setattr(self, 'schedule', n.get_enum_value(DataSourceSchedule)),
            "secret_key": lambda n : setattr(self, 'secret_key', n.get_str_value()),
            "state": lambda n : setattr(self, 'state', n.get_str_value()),
            "storage_key": lambda n : setattr(self, 'storage_key', n.get_str_value()),
            "subdomain": lambda n : setattr(self, 'subdomain', n.get_str_value()),
            "token": lambda n : setattr(self, 'token', n.get_str_value()),
            "type": lambda n : setattr(self, 'type', n.get_enum_value(DataSourceType)),
            "workspace": lambda n : setattr(self, 'workspace', n.get_str_value()),
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
        writer.write_str_value("access_key", self.access_key)
        writer.write_str_value("account", self.account)
        writer.write_str_value("account_name", self.account_name)
        writer.write_str_value("api_key", self.api_key)
        writer.write_str_value("auth_mode", self.auth_mode)
        writer.write_str_value("branch", self.branch)
        writer.write_str_value("bucket", self.bucket)
        writer.write_str_value("client_id", self.client_id)
        writer.write_str_value("client_secret", self.client_secret)
        writer.write_str_value("container", self.container)
        writer.write_str_value("endpoint", self.endpoint)
        writer.write_str_value("filter", self.filter)
        writer.write_bool_value("include_attachments", self.include_attachments)
        writer.write_bool_value("include_comments", self.include_comments)
        writer.write_bool_value("include_files", self.include_files)
        writer.write_bool_value("include_notes", self.include_notes)
        writer.write_bool_value("is_sandbox", self.is_sandbox)
        writer.write_str_value("key", self.key)
        writer.write_str_value("listing", self.listing)
        writer.write_str_value("name", self.name)
        writer.write_str_value("prefix", self.prefix)
        writer.write_int_value("read_limit", self.read_limit)
        writer.write_str_value("refresh_token", self.refresh_token)
        writer.write_str_value("region", self.region)
        writer.write_object_value("resource", self.resource)
        writer.write_enum_value("schedule", self.schedule)
        writer.write_str_value("secret_key", self.secret_key)
        writer.write_str_value("state", self.state)
        writer.write_str_value("storage_key", self.storage_key)
        writer.write_str_value("subdomain", self.subdomain)
        writer.write_str_value("token", self.token)
        writer.write_enum_value("type", self.type)
        writer.write_str_value("workspace", self.workspace)
    

