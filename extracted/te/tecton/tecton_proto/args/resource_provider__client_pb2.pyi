from tecton_proto.args import basic_info__client_pb2 as _basic_info__client_pb2
from tecton_proto.args import diff_options__client_pb2 as _diff_options__client_pb2
from tecton_proto.args import user_defined_function__client_pb2 as _user_defined_function__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import secret__client_pb2 as _secret__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ResourceProviderArgs(_message.Message):
    __slots__ = ["function", "info", "prevent_destroy", "resource_provider_id", "secrets"]
    class SecretsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _secret__client_pb2.SecretReference
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_secret__client_pb2.SecretReference, _Mapping]] = ...) -> None: ...
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    PREVENT_DESTROY_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_PROVIDER_ID_FIELD_NUMBER: _ClassVar[int]
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    function: _user_defined_function__client_pb2.UserDefinedFunction
    info: _basic_info__client_pb2.BasicInfo
    prevent_destroy: bool
    resource_provider_id: _id__client_pb2.Id
    secrets: _containers.MessageMap[str, _secret__client_pb2.SecretReference]
    def __init__(self, resource_provider_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., info: _Optional[_Union[_basic_info__client_pb2.BasicInfo, _Mapping]] = ..., secrets: _Optional[_Mapping[str, _secret__client_pb2.SecretReference]] = ..., function: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ..., prevent_destroy: bool = ...) -> None: ...
