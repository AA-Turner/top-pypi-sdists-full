from chalk._gen.chalk.kubernetes.v1 import resourcequantities_pb2 as _resourcequantities_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KubernetesResourceQuotaStatus(_message.Message):
    __slots__ = ("hard_limits", "used")
    HARD_LIMITS_FIELD_NUMBER: _ClassVar[int]
    USED_FIELD_NUMBER: _ClassVar[int]
    hard_limits: _resourcequantities_pb2.KubernetesResourceQuantities
    used: _resourcequantities_pb2.KubernetesResourceQuantities
    def __init__(
        self,
        hard_limits: _Optional[_Union[_resourcequantities_pb2.KubernetesResourceQuantities, _Mapping]] = ...,
        used: _Optional[_Union[_resourcequantities_pb2.KubernetesResourceQuantities, _Mapping]] = ...,
    ) -> None: ...

class KubernetesResourceQuotaSpec(_message.Message):
    __slots__ = ("hard_limits",)
    HARD_LIMITS_FIELD_NUMBER: _ClassVar[int]
    hard_limits: _resourcequantities_pb2.KubernetesResourceQuantities
    def __init__(
        self, hard_limits: _Optional[_Union[_resourcequantities_pb2.KubernetesResourceQuantities, _Mapping]] = ...
    ) -> None: ...

class KubernetesResourceQuotaData(_message.Message):
    __slots__ = ("spec", "status")
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    spec: KubernetesResourceQuotaSpec
    status: KubernetesResourceQuotaStatus
    def __init__(
        self,
        spec: _Optional[_Union[KubernetesResourceQuotaSpec, _Mapping]] = ...,
        status: _Optional[_Union[KubernetesResourceQuotaStatus, _Mapping]] = ...,
    ) -> None: ...
