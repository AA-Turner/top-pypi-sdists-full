from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from nominal_api_protos.nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal_api_protos.nominal.types.time import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DatasetRetentionExemption(_message.Message):
    __slots__ = ("dataset_rid", "source_id", "bounds", "description")
    DATASET_RID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    BOUNDS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    dataset_rid: str
    source_id: str
    bounds: _time_pb2.Range
    description: str
    def __init__(self, dataset_rid: _Optional[str] = ..., source_id: _Optional[str] = ..., bounds: _Optional[_Union[_time_pb2.Range, _Mapping]] = ..., description: _Optional[str] = ...) -> None: ...

class UpsertDatasetRetentionExemptionRequest(_message.Message):
    __slots__ = ("dataset_rid", "source_id", "bounds", "description")
    DATASET_RID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    BOUNDS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    dataset_rid: str
    source_id: str
    bounds: _time_pb2.Range
    description: str
    def __init__(self, dataset_rid: _Optional[str] = ..., source_id: _Optional[str] = ..., bounds: _Optional[_Union[_time_pb2.Range, _Mapping]] = ..., description: _Optional[str] = ...) -> None: ...

class UpsertDatasetRetentionExemptionResponse(_message.Message):
    __slots__ = ("exemption",)
    EXEMPTION_FIELD_NUMBER: _ClassVar[int]
    exemption: DatasetRetentionExemption
    def __init__(self, exemption: _Optional[_Union[DatasetRetentionExemption, _Mapping]] = ...) -> None: ...

class DeleteDatasetRetentionExemptionRequest(_message.Message):
    __slots__ = ("dataset_rid", "source_id")
    DATASET_RID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    dataset_rid: str
    source_id: str
    def __init__(self, dataset_rid: _Optional[str] = ..., source_id: _Optional[str] = ...) -> None: ...

class DeleteDatasetRetentionExemptionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListDatasetRetentionExemptionsRequest(_message.Message):
    __slots__ = ("dataset_rid", "bounds", "page_size", "next_page_token")
    DATASET_RID_FIELD_NUMBER: _ClassVar[int]
    BOUNDS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    dataset_rid: str
    bounds: _time_pb2.Range
    page_size: int
    next_page_token: str
    def __init__(self, dataset_rid: _Optional[str] = ..., bounds: _Optional[_Union[_time_pb2.Range, _Mapping]] = ..., page_size: _Optional[int] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class ListDatasetRetentionExemptionsResponse(_message.Message):
    __slots__ = ("exemptions", "next_page_token")
    EXEMPTIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    exemptions: _containers.RepeatedCompositeFieldContainer[DatasetRetentionExemption]
    next_page_token: str
    def __init__(self, exemptions: _Optional[_Iterable[_Union[DatasetRetentionExemption, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class KeepForever(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class KeepUntilExpiry(_message.Message):
    __slots__ = ("expiry_days",)
    EXPIRY_DAYS_FIELD_NUMBER: _ClassVar[int]
    expiry_days: int
    def __init__(self, expiry_days: _Optional[int] = ...) -> None: ...

class RetentionPolicy(_message.Message):
    __slots__ = ("keep_forever", "keep_until_expiry")
    KEEP_FOREVER_FIELD_NUMBER: _ClassVar[int]
    KEEP_UNTIL_EXPIRY_FIELD_NUMBER: _ClassVar[int]
    keep_forever: KeepForever
    keep_until_expiry: KeepUntilExpiry
    def __init__(self, keep_forever: _Optional[_Union[KeepForever, _Mapping]] = ..., keep_until_expiry: _Optional[_Union[KeepUntilExpiry, _Mapping]] = ...) -> None: ...

class UpdateRetentionPolicyRequest(_message.Message):
    __slots__ = ("dataset_rid", "retention_policy")
    DATASET_RID_FIELD_NUMBER: _ClassVar[int]
    RETENTION_POLICY_FIELD_NUMBER: _ClassVar[int]
    dataset_rid: str
    retention_policy: RetentionPolicy
    def __init__(self, dataset_rid: _Optional[str] = ..., retention_policy: _Optional[_Union[RetentionPolicy, _Mapping]] = ...) -> None: ...

class UpdateRetentionPolicyResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
