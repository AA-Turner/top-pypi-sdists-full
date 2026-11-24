from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetCatalogRoutingTableRequest(_message.Message):
    __slots__ = ("function_version_ids",)
    FUNCTION_VERSION_IDS_FIELD_NUMBER: _ClassVar[int]
    function_version_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, function_version_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetCatalogRoutingTableResponse(_message.Message):
    __slots__ = ("model_endpoint_config_json",)
    MODEL_ENDPOINT_CONFIG_JSON_FIELD_NUMBER: _ClassVar[int]
    model_endpoint_config_json: str
    def __init__(self, model_endpoint_config_json: _Optional[str] = ...) -> None: ...
