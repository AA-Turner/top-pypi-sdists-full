import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal.data_connector.v1 import opc_ua_connector_pb2 as _opc_ua_connector_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal.gen.v1 import error_pb2 as _error_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataConnectorErrorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATA_CONNECTOR_ERROR_TYPE_UNSPECIFIED: _ClassVar[DataConnectorErrorType]
    DATA_CONNECTOR_ERROR_TYPE_CONNECTOR_NOT_FOUND: _ClassVar[DataConnectorErrorType]
    DATA_CONNECTOR_ERROR_TYPE_CONNECTOR_NOT_AUTHORIZED: _ClassVar[DataConnectorErrorType]
    DATA_CONNECTOR_ERROR_TYPE_TARGET_DATASET_NOT_IN_WORKSPACE: _ClassVar[DataConnectorErrorType]

class SortField(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SORT_FIELD_UNSPECIFIED: _ClassVar[SortField]
    SORT_FIELD_UPDATED_AT: _ClassVar[SortField]

class SortOrder(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SORT_ORDER_UNSPECIFIED: _ClassVar[SortOrder]
    SORT_ORDER_ASC: _ClassVar[SortOrder]
    SORT_ORDER_DESC: _ClassVar[SortOrder]

class ReplicaStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REPLICA_STATUS_UNSPECIFIED: _ClassVar[ReplicaStatus]
    REPLICA_STATUS_STARTING: _ClassVar[ReplicaStatus]
    REPLICA_STATUS_SUBSCRIBING: _ClassVar[ReplicaStatus]
    REPLICA_STATUS_RUNNING: _ClassVar[ReplicaStatus]
    REPLICA_STATUS_STOPPING: _ClassVar[ReplicaStatus]
    REPLICA_STATUS_STOPPED: _ClassVar[ReplicaStatus]
DATA_CONNECTOR_ERROR_TYPE_UNSPECIFIED: DataConnectorErrorType
DATA_CONNECTOR_ERROR_TYPE_CONNECTOR_NOT_FOUND: DataConnectorErrorType
DATA_CONNECTOR_ERROR_TYPE_CONNECTOR_NOT_AUTHORIZED: DataConnectorErrorType
DATA_CONNECTOR_ERROR_TYPE_TARGET_DATASET_NOT_IN_WORKSPACE: DataConnectorErrorType
SORT_FIELD_UNSPECIFIED: SortField
SORT_FIELD_UPDATED_AT: SortField
SORT_ORDER_UNSPECIFIED: SortOrder
SORT_ORDER_ASC: SortOrder
SORT_ORDER_DESC: SortOrder
REPLICA_STATUS_UNSPECIFIED: ReplicaStatus
REPLICA_STATUS_STARTING: ReplicaStatus
REPLICA_STATUS_SUBSCRIBING: ReplicaStatus
REPLICA_STATUS_RUNNING: ReplicaStatus
REPLICA_STATUS_STOPPING: ReplicaStatus
REPLICA_STATUS_STOPPED: ReplicaStatus

class CreateDataConnectorRequest(_message.Message):
    __slots__ = ("name", "description", "connection_details", "workspace_rid", "target_dataset_rid")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_DETAILS_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    TARGET_DATASET_RID_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    connection_details: DataConnectorDetails
    workspace_rid: str
    target_dataset_rid: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., connection_details: _Optional[_Union[DataConnectorDetails, _Mapping]] = ..., workspace_rid: _Optional[str] = ..., target_dataset_rid: _Optional[str] = ...) -> None: ...

class CreateDataConnectorResponse(_message.Message):
    __slots__ = ("data_connector",)
    DATA_CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    data_connector: DataConnector
    def __init__(self, data_connector: _Optional[_Union[DataConnector, _Mapping]] = ...) -> None: ...

class DataConnector(_message.Message):
    __slots__ = ("data_connector_rid", "name", "description", "connection_details", "workspace_rid", "target_dataset_rid", "created_at")
    DATA_CONNECTOR_RID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_DETAILS_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    TARGET_DATASET_RID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    data_connector_rid: str
    name: str
    description: str
    connection_details: DataConnectorDetailsSecrets
    workspace_rid: str
    target_dataset_rid: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, data_connector_rid: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., connection_details: _Optional[_Union[DataConnectorDetailsSecrets, _Mapping]] = ..., workspace_rid: _Optional[str] = ..., target_dataset_rid: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class DataConnectorDetails(_message.Message):
    __slots__ = ("opc_ua",)
    OPC_UA_FIELD_NUMBER: _ClassVar[int]
    opc_ua: _opc_ua_connector_pb2.OpcUaConnectorDetails
    def __init__(self, opc_ua: _Optional[_Union[_opc_ua_connector_pb2.OpcUaConnectorDetails, _Mapping]] = ...) -> None: ...

class DataConnectorDetailsUpdates(_message.Message):
    __slots__ = ("opc_ua",)
    OPC_UA_FIELD_NUMBER: _ClassVar[int]
    opc_ua: _opc_ua_connector_pb2.OpcUaConnectorDetailsUpdates
    def __init__(self, opc_ua: _Optional[_Union[_opc_ua_connector_pb2.OpcUaConnectorDetailsUpdates, _Mapping]] = ...) -> None: ...

class DataConnectorDetailsSecrets(_message.Message):
    __slots__ = ("opc_ua",)
    OPC_UA_FIELD_NUMBER: _ClassVar[int]
    opc_ua: _opc_ua_connector_pb2.OpcUaConnectorDetailsSecret
    def __init__(self, opc_ua: _Optional[_Union[_opc_ua_connector_pb2.OpcUaConnectorDetailsSecret, _Mapping]] = ...) -> None: ...

class UpdateDataConnectorRequest(_message.Message):
    __slots__ = ("data_connector_rid", "name", "description", "connection_details", "target_dataset_rid")
    DATA_CONNECTOR_RID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_DETAILS_FIELD_NUMBER: _ClassVar[int]
    TARGET_DATASET_RID_FIELD_NUMBER: _ClassVar[int]
    data_connector_rid: str
    name: str
    description: str
    connection_details: DataConnectorDetailsUpdates
    target_dataset_rid: str
    def __init__(self, data_connector_rid: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., connection_details: _Optional[_Union[DataConnectorDetailsUpdates, _Mapping]] = ..., target_dataset_rid: _Optional[str] = ...) -> None: ...

class UpdateDataConnectorResponse(_message.Message):
    __slots__ = ("data_connector",)
    DATA_CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    data_connector: DataConnector
    def __init__(self, data_connector: _Optional[_Union[DataConnector, _Mapping]] = ...) -> None: ...

class GetDataConnectorRequest(_message.Message):
    __slots__ = ("data_connector_rid",)
    DATA_CONNECTOR_RID_FIELD_NUMBER: _ClassVar[int]
    data_connector_rid: str
    def __init__(self, data_connector_rid: _Optional[str] = ...) -> None: ...

class GetDataConnectorResponse(_message.Message):
    __slots__ = ("data_connector",)
    DATA_CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    data_connector: DataConnector
    def __init__(self, data_connector: _Optional[_Union[DataConnector, _Mapping]] = ...) -> None: ...

class NameFilter(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DescriptionFilter(_message.Message):
    __slots__ = ("description",)
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    description: str
    def __init__(self, description: _Optional[str] = ...) -> None: ...

class TargetDatasetFilter(_message.Message):
    __slots__ = ("target_dataset_rid",)
    TARGET_DATASET_RID_FIELD_NUMBER: _ClassVar[int]
    target_dataset_rid: str
    def __init__(self, target_dataset_rid: _Optional[str] = ...) -> None: ...

class AndFilter(_message.Message):
    __slots__ = ("clauses",)
    CLAUSES_FIELD_NUMBER: _ClassVar[int]
    clauses: _containers.RepeatedCompositeFieldContainer[SearchFilter]
    def __init__(self, clauses: _Optional[_Iterable[_Union[SearchFilter, _Mapping]]] = ...) -> None: ...

class SortBy(_message.Message):
    __slots__ = ("field", "order")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    field: SortField
    order: SortOrder
    def __init__(self, field: _Optional[_Union[SortField, str]] = ..., order: _Optional[_Union[SortOrder, str]] = ...) -> None: ...

class SearchFilter(_message.Message):
    __slots__ = ("name", "description", "target_dataset")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TARGET_DATASET_FIELD_NUMBER: _ClassVar[int]
    AND_FIELD_NUMBER: _ClassVar[int]
    name: NameFilter
    description: DescriptionFilter
    target_dataset: TargetDatasetFilter
    def __init__(self, name: _Optional[_Union[NameFilter, _Mapping]] = ..., description: _Optional[_Union[DescriptionFilter, _Mapping]] = ..., target_dataset: _Optional[_Union[TargetDatasetFilter, _Mapping]] = ..., **kwargs) -> None: ...

class SearchRequest(_message.Message):
    __slots__ = ("workspace_rid", "filter", "page_size", "page_token", "sort_by")
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    SORT_BY_FIELD_NUMBER: _ClassVar[int]
    workspace_rid: str
    filter: SearchFilter
    page_size: int
    page_token: str
    sort_by: SortBy
    def __init__(self, workspace_rid: _Optional[str] = ..., filter: _Optional[_Union[SearchFilter, _Mapping]] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., sort_by: _Optional[_Union[SortBy, _Mapping]] = ...) -> None: ...

class SearchResponse(_message.Message):
    __slots__ = ("data_connectors", "page_token")
    DATA_CONNECTORS_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    data_connectors: _containers.RepeatedCompositeFieldContainer[DataConnector]
    page_token: str
    def __init__(self, data_connectors: _Optional[_Iterable[_Union[DataConnector, _Mapping]]] = ..., page_token: _Optional[str] = ...) -> None: ...

class StartSessionRequest(_message.Message):
    __slots__ = ("data_connector_rid",)
    DATA_CONNECTOR_RID_FIELD_NUMBER: _ClassVar[int]
    data_connector_rid: str
    def __init__(self, data_connector_rid: _Optional[str] = ...) -> None: ...

class StartSessionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StopSessionRequest(_message.Message):
    __slots__ = ("data_connector_rid",)
    DATA_CONNECTOR_RID_FIELD_NUMBER: _ClassVar[int]
    data_connector_rid: str
    def __init__(self, data_connector_rid: _Optional[str] = ...) -> None: ...

class StopSessionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetSessionStatusRequest(_message.Message):
    __slots__ = ("data_connector_rid",)
    DATA_CONNECTOR_RID_FIELD_NUMBER: _ClassVar[int]
    data_connector_rid: str
    def __init__(self, data_connector_rid: _Optional[str] = ...) -> None: ...

class ActiveSessionStatus(_message.Message):
    __slots__ = ("replica_status",)
    REPLICA_STATUS_FIELD_NUMBER: _ClassVar[int]
    replica_status: _containers.RepeatedScalarFieldContainer[ReplicaStatus]
    def __init__(self, replica_status: _Optional[_Iterable[_Union[ReplicaStatus, str]]] = ...) -> None: ...

class GetSessionStatusResponse(_message.Message):
    __slots__ = ("none", "active")
    NONE_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    none: _empty_pb2.Empty
    active: ActiveSessionStatus
    def __init__(self, none: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ..., active: _Optional[_Union[ActiveSessionStatus, _Mapping]] = ...) -> None: ...

class DeleteDataConnectorRequest(_message.Message):
    __slots__ = ("data_connector_rid",)
    DATA_CONNECTOR_RID_FIELD_NUMBER: _ClassVar[int]
    data_connector_rid: str
    def __init__(self, data_connector_rid: _Optional[str] = ...) -> None: ...

class DeleteDataConnectorResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
