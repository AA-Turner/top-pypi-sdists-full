from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.common import fco_locator__client_pb2 as _fco_locator__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
FEATURE_VIEW_SIMILARITY_DUPLICATE: FeatureViewSimilarityType
FEATURE_VIEW_SIMILARITY_NEAR_DUPLICATE: FeatureViewSimilarityType
FEATURE_VIEW_SIMILARITY_UNKNOWN: FeatureViewSimilarityType

class FeatureSimilarityAnalysisResult(_message.Message):
    __slots__ = ["analysis_time", "fv_groups"]
    ANALYSIS_TIME_FIELD_NUMBER: _ClassVar[int]
    FV_GROUPS_FIELD_NUMBER: _ClassVar[int]
    analysis_time: _timestamp_pb2.Timestamp
    fv_groups: _containers.RepeatedCompositeFieldContainer[FeatureViewSimilarityGroup]
    def __init__(self, analysis_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., fv_groups: _Optional[_Iterable[_Union[FeatureViewSimilarityGroup, _Mapping]]] = ...) -> None: ...

class FeatureViewSimilarityGroup(_message.Message):
    __slots__ = ["fv_details_first", "fv_locator_first", "pairs", "workspace_state_id_first"]
    FV_DETAILS_FIRST_FIELD_NUMBER: _ClassVar[int]
    FV_LOCATOR_FIRST_FIELD_NUMBER: _ClassVar[int]
    PAIRS_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_STATE_ID_FIRST_FIELD_NUMBER: _ClassVar[int]
    fv_details_first: str
    fv_locator_first: _fco_locator__client_pb2.FcoLocator
    pairs: _containers.RepeatedCompositeFieldContainer[FeatureViewSimilarityPair]
    workspace_state_id_first: _id__client_pb2.Id
    def __init__(self, fv_locator_first: _Optional[_Union[_fco_locator__client_pb2.FcoLocator, _Mapping]] = ..., workspace_state_id_first: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., fv_details_first: _Optional[str] = ..., pairs: _Optional[_Iterable[_Union[FeatureViewSimilarityPair, _Mapping]]] = ...) -> None: ...

class FeatureViewSimilarityPair(_message.Message):
    __slots__ = ["fv_details_second", "fv_locator_second", "similarity", "similarity_description", "type", "workspace_state_id_second"]
    FV_DETAILS_SECOND_FIELD_NUMBER: _ClassVar[int]
    FV_LOCATOR_SECOND_FIELD_NUMBER: _ClassVar[int]
    SIMILARITY_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SIMILARITY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_STATE_ID_SECOND_FIELD_NUMBER: _ClassVar[int]
    fv_details_second: str
    fv_locator_second: _fco_locator__client_pb2.FcoLocator
    similarity: float
    similarity_description: str
    type: FeatureViewSimilarityType
    workspace_state_id_second: _id__client_pb2.Id
    def __init__(self, fv_locator_second: _Optional[_Union[_fco_locator__client_pb2.FcoLocator, _Mapping]] = ..., workspace_state_id_second: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., similarity: _Optional[float] = ..., type: _Optional[_Union[FeatureViewSimilarityType, str]] = ..., fv_details_second: _Optional[str] = ..., similarity_description: _Optional[str] = ...) -> None: ...

class FeatureViewSimilarityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
