from tecton_proto.args import user_defined_function__client_pb2 as _user_defined_function__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import secret__client_pb2 as _secret__client_pb2
from tecton_proto.data import fco_metadata__client_pb2 as _fco_metadata__client_pb2
from tecton_proto.validation import validator__client_pb2 as _validator__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ResourceProvider(_message.Message):
    __slots__ = ["fco_metadata", "function", "resource_provider_id", "secrets", "validation_args"]
    class SecretsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _secret__client_pb2.SecretReference
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_secret__client_pb2.SecretReference, _Mapping]] = ...) -> None: ...
    FCO_METADATA_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_PROVIDER_ID_FIELD_NUMBER: _ClassVar[int]
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_ARGS_FIELD_NUMBER: _ClassVar[int]
    fco_metadata: _fco_metadata__client_pb2.FcoMetadata
    function: _user_defined_function__client_pb2.UserDefinedFunction
    resource_provider_id: _id__client_pb2.Id
    secrets: _containers.MessageMap[str, _secret__client_pb2.SecretReference]
    validation_args: _validator__client_pb2.ResourceProviderArgs
    def __init__(self, resource_provider_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., fco_metadata: _Optional[_Union[_fco_metadata__client_pb2.FcoMetadata, _Mapping]] = ..., secrets: _Optional[_Mapping[str, _secret__client_pb2.SecretReference]] = ..., function: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ..., validation_args: _Optional[_Union[_validator__client_pb2.ResourceProviderArgs, _Mapping]] = ...) -> None: ...
