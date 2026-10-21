from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetCatalogRoutingTableRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetCatalogRoutingTableResponse(_message.Message):
    __slots__ = ("model_endpoint_config_json",)
    MODEL_ENDPOINT_CONFIG_JSON_FIELD_NUMBER: _ClassVar[int]
    model_endpoint_config_json: str
    def __init__(self, model_endpoint_config_json: _Optional[str] = ...) -> None: ...
