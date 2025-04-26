from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InstanceProfile(_message.Message):
    __slots__ = ["instance_profile_arn"]
    INSTANCE_PROFILE_ARN_FIELD_NUMBER: _ClassVar[int]
    instance_profile_arn: str
    def __init__(self, instance_profile_arn: _Optional[str] = ...) -> None: ...

class InstanceProfilesListResponse(_message.Message):
    __slots__ = ["instance_profiles"]
    INSTANCE_PROFILES_FIELD_NUMBER: _ClassVar[int]
    instance_profiles: _containers.RepeatedCompositeFieldContainer[InstanceProfile]
    def __init__(self, instance_profiles: _Optional[_Iterable[_Union[InstanceProfile, _Mapping]]] = ...) -> None: ...
