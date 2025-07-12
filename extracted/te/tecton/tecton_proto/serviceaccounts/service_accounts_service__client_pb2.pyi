from tecton_proto.auditlog import metadata__client_pb2 as _metadata__client_pb2
from tecton_proto.auth import service__client_pb2 as _service__client_pb2
from tecton_proto.data import service_account__client_pb2 as _service_account__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ActivateServiceAccountSecretRequest(_message.Message):
    __slots__ = ["secret_id", "service_account_id"]
    SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    secret_id: str
    service_account_id: str
    def __init__(self, service_account_id: _Optional[str] = ..., secret_id: _Optional[str] = ...) -> None: ...

class ActivateServiceAccountSecretResponse(_message.Message):
    __slots__ = ["secret"]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    secret: _service_account__client_pb2.MaskedClientSecret
    def __init__(self, secret: _Optional[_Union[_service_account__client_pb2.MaskedClientSecret, _Mapping]] = ...) -> None: ...

class CreateServiceAccountSecretRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class CreateServiceAccountSecretResponse(_message.Message):
    __slots__ = ["secret"]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    secret: _service_account__client_pb2.NewClientSecret
    def __init__(self, secret: _Optional[_Union[_service_account__client_pb2.NewClientSecret, _Mapping]] = ...) -> None: ...

class DeactivateServiceAccountSecretRequest(_message.Message):
    __slots__ = ["secret_id", "service_account_id"]
    SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    secret_id: str
    service_account_id: str
    def __init__(self, service_account_id: _Optional[str] = ..., secret_id: _Optional[str] = ...) -> None: ...

class DeactivateServiceAccountSecretResponse(_message.Message):
    __slots__ = ["secret"]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    secret: _service_account__client_pb2.MaskedClientSecret
    def __init__(self, secret: _Optional[_Union[_service_account__client_pb2.MaskedClientSecret, _Mapping]] = ...) -> None: ...

class DeleteServiceAccountSecretRequest(_message.Message):
    __slots__ = ["secret_id", "service_account_id"]
    SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    secret_id: str
    service_account_id: str
    def __init__(self, service_account_id: _Optional[str] = ..., secret_id: _Optional[str] = ...) -> None: ...

class DeleteServiceAccountSecretResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListServiceAccountSecretsRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ListServiceAccountSecretsResponse(_message.Message):
    __slots__ = ["client_secrets"]
    CLIENT_SECRETS_FIELD_NUMBER: _ClassVar[int]
    client_secrets: _containers.RepeatedCompositeFieldContainer[_service_account__client_pb2.MaskedClientSecret]
    def __init__(self, client_secrets: _Optional[_Iterable[_Union[_service_account__client_pb2.MaskedClientSecret, _Mapping]]] = ...) -> None: ...
