from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsCredentials(_message.Message):
    __slots__ = ["access_key_id", "expiration", "secret_access_key", "session_token"]
    ACCESS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    SECRET_ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    SESSION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_key_id: str
    expiration: _timestamp_pb2.Timestamp
    secret_access_key: str
    session_token: str
    def __init__(self, access_key_id: _Optional[str] = ..., secret_access_key: _Optional[str] = ..., session_token: _Optional[str] = ..., expiration: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class AwsIamRole(_message.Message):
    __slots__ = ["external_id", "intermediate_role", "role_arn"]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    INTERMEDIATE_ROLE_FIELD_NUMBER: _ClassVar[int]
    ROLE_ARN_FIELD_NUMBER: _ClassVar[int]
    external_id: str
    intermediate_role: AwsIamRole
    role_arn: str
    def __init__(self, role_arn: _Optional[str] = ..., intermediate_role: _Optional[_Union[AwsIamRole, _Mapping]] = ..., external_id: _Optional[str] = ...) -> None: ...
