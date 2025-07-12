from tecton_proto.auditlog import metadata__client_pb2 as _metadata__client_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ComputeIdentity(_message.Message):
    __slots__ = ["databricks_service_principal"]
    DATABRICKS_SERVICE_PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    databricks_service_principal: DatabricksServicePrincipal
    def __init__(self, databricks_service_principal: _Optional[_Union[DatabricksServicePrincipal, _Mapping]] = ...) -> None: ...

class DatabricksServicePrincipal(_message.Message):
    __slots__ = ["application_id"]
    APPLICATION_ID_FIELD_NUMBER: _ClassVar[int]
    application_id: str
    def __init__(self, application_id: _Optional[str] = ...) -> None: ...
