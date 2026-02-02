from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MessageReaction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MESSAGE_REACTION_UNSPECIFIED: _ClassVar[MessageReaction]
    MESSAGE_REACTION_THUMBS_UP: _ClassVar[MessageReaction]
    MESSAGE_REACTION_THUMBS_DOWN: _ClassVar[MessageReaction]
MESSAGE_REACTION_UNSPECIFIED: MessageReaction
MESSAGE_REACTION_THUMBS_UP: MessageReaction
MESSAGE_REACTION_THUMBS_DOWN: MessageReaction

class BlobUrlList(_message.Message):
    __slots__ = ("blob_urls",)
    BLOB_URLS_FIELD_NUMBER: _ClassVar[int]
    blob_urls: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, blob_urls: _Optional[_Iterable[str]] = ...) -> None: ...

class EmbeddingMetrics(_message.Message):
    __slots__ = ("ne_sum", "condition_number", "rcondition_number", "stable_rank")
    NE_SUM_FIELD_NUMBER: _ClassVar[int]
    CONDITION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    RCONDITION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    STABLE_RANK_FIELD_NUMBER: _ClassVar[int]
    ne_sum: float
    condition_number: float
    rcondition_number: float
    stable_rank: float
    def __init__(self, ne_sum: _Optional[float] = ..., condition_number: _Optional[float] = ..., rcondition_number: _Optional[float] = ..., stable_rank: _Optional[float] = ...) -> None: ...

class AgentMessageMetadata(_message.Message):
    __slots__ = ("message_reaction",)
    MESSAGE_REACTION_FIELD_NUMBER: _ClassVar[int]
    message_reaction: MessageReaction
    def __init__(self, message_reaction: _Optional[_Union[MessageReaction, str]] = ...) -> None: ...

class RetrievedEntityData(_message.Message):
    __slots__ = ("source_id", "row", "score")
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    ROW_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    source_id: str
    row: _struct_pb2.Struct
    score: float
    def __init__(self, source_id: _Optional[str] = ..., row: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., score: _Optional[float] = ...) -> None: ...

class RetrievedEntitiesData(_message.Message):
    __slots__ = ("retrieved_entities_data",)
    RETRIEVED_ENTITIES_DATA_FIELD_NUMBER: _ClassVar[int]
    retrieved_entities_data: _containers.RepeatedCompositeFieldContainer[RetrievedEntityData]
    def __init__(self, retrieved_entities_data: _Optional[_Iterable[_Union[RetrievedEntityData, _Mapping]]] = ...) -> None: ...

class RetrievedEntities(_message.Message):
    __slots__ = ("retrieved_entities",)
    class RetrievedEntitiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: RetrievedEntitiesData
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[RetrievedEntitiesData, _Mapping]] = ...) -> None: ...
    RETRIEVED_ENTITIES_FIELD_NUMBER: _ClassVar[int]
    retrieved_entities: _containers.MessageMap[str, RetrievedEntitiesData]
    def __init__(self, retrieved_entities: _Optional[_Mapping[str, RetrievedEntitiesData]] = ...) -> None: ...
