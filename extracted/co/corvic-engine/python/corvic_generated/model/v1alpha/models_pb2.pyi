from corvic_generated.orm.v1 import agent_pb2 as _agent_pb2
from corvic_generated.orm.v1 import common_pb2 as _common_pb2
from corvic_generated.orm.v1 import feature_view_pb2 as _feature_view_pb2
from corvic_generated.orm.v1 import space_pb2 as _space_pb2
from corvic_generated.orm.v1 import table_pb2 as _table_pb2
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

class Resource(_message.Message):
    __slots__ = ("id", "name", "description", "mime_type", "url", "size", "md5", "original_path", "room_id", "source_ids", "org_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    MD5_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_PATH_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_IDS_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    mime_type: str
    url: str
    size: int
    md5: str
    original_path: str
    room_id: str
    source_ids: _containers.RepeatedScalarFieldContainer[str]
    org_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., mime_type: _Optional[str] = ..., url: _Optional[str] = ..., size: _Optional[int] = ..., md5: _Optional[str] = ..., original_path: _Optional[str] = ..., room_id: _Optional[str] = ..., source_ids: _Optional[_Iterable[str]] = ..., org_id: _Optional[str] = ...) -> None: ...

class Source(_message.Message):
    __slots__ = ("id", "name", "table_op_graph", "room_id", "resource_id", "org_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TABLE_OP_GRAPH_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    table_op_graph: _table_pb2.TableComputeOp
    room_id: str
    resource_id: str
    org_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., table_op_graph: _Optional[_Union[_table_pb2.TableComputeOp, _Mapping]] = ..., room_id: _Optional[str] = ..., resource_id: _Optional[str] = ..., org_id: _Optional[str] = ...) -> None: ...

class FeatureViewSource(_message.Message):
    __slots__ = ("id", "source_id", "table_op_graph", "drop_disconnected", "org_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    TABLE_OP_GRAPH_FIELD_NUMBER: _ClassVar[int]
    DROP_DISCONNECTED_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    source_id: str
    table_op_graph: _table_pb2.TableComputeOp
    drop_disconnected: bool
    org_id: str
    def __init__(self, id: _Optional[str] = ..., source_id: _Optional[str] = ..., table_op_graph: _Optional[_Union[_table_pb2.TableComputeOp, _Mapping]] = ..., drop_disconnected: bool = ..., org_id: _Optional[str] = ...) -> None: ...

class FeatureView(_message.Message):
    __slots__ = ("id", "name", "description", "room_id", "feature_view_output", "feature_view_sources", "space_ids", "org_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_SOURCES_FIELD_NUMBER: _ClassVar[int]
    SPACE_IDS_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    room_id: str
    feature_view_output: _feature_view_pb2.FeatureViewOutput
    feature_view_sources: _containers.RepeatedCompositeFieldContainer[FeatureViewSource]
    space_ids: _containers.RepeatedScalarFieldContainer[str]
    org_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., room_id: _Optional[str] = ..., feature_view_output: _Optional[_Union[_feature_view_pb2.FeatureViewOutput, _Mapping]] = ..., feature_view_sources: _Optional[_Iterable[_Union[FeatureViewSource, _Mapping]]] = ..., space_ids: _Optional[_Iterable[str]] = ..., org_id: _Optional[str] = ...) -> None: ...

class Space(_message.Message):
    __slots__ = ("id", "name", "description", "room_id", "space_parameters", "feature_view_id", "org_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    SPACE_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    room_id: str
    space_parameters: _space_pb2.SpaceParameters
    feature_view_id: str
    org_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., room_id: _Optional[str] = ..., space_parameters: _Optional[_Union[_space_pb2.SpaceParameters, _Mapping]] = ..., feature_view_id: _Optional[str] = ..., org_id: _Optional[str] = ...) -> None: ...

class UserMessage(_message.Message):
    __slots__ = ("id", "message")
    ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    id: str
    message: str
    def __init__(self, id: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class AgentMessage(_message.Message):
    __slots__ = ("id", "message", "policy", "context", "message_reaction", "user_message_id", "retrieved_entities")
    ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_REACTION_FIELD_NUMBER: _ClassVar[int]
    USER_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    RETRIEVED_ENTITIES_FIELD_NUMBER: _ClassVar[int]
    id: str
    message: str
    policy: _struct_pb2.Struct
    context: str
    message_reaction: MessageReaction
    user_message_id: str
    retrieved_entities: _common_pb2.RetrievedEntities
    def __init__(self, id: _Optional[str] = ..., message: _Optional[str] = ..., policy: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., context: _Optional[str] = ..., message_reaction: _Optional[_Union[MessageReaction, str]] = ..., user_message_id: _Optional[str] = ..., retrieved_entities: _Optional[_Union[_common_pb2.RetrievedEntities, _Mapping]] = ...) -> None: ...

class MessageEntry(_message.Message):
    __slots__ = ("id", "user_message", "agent_message")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    AGENT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_message: UserMessage
    agent_message: AgentMessage
    def __init__(self, id: _Optional[str] = ..., user_message: _Optional[_Union[UserMessage, _Mapping]] = ..., agent_message: _Optional[_Union[AgentMessage, _Mapping]] = ...) -> None: ...

class Agent(_message.Message):
    __slots__ = ("id", "name", "room_id", "agent_parameters", "org_id", "messages")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    AGENT_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    room_id: str
    agent_parameters: _agent_pb2.AgentParameters
    org_id: str
    messages: _containers.RepeatedCompositeFieldContainer[MessageEntry]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., room_id: _Optional[str] = ..., agent_parameters: _Optional[_Union[_agent_pb2.AgentParameters, _Mapping]] = ..., org_id: _Optional[str] = ..., messages: _Optional[_Iterable[_Union[MessageEntry, _Mapping]]] = ...) -> None: ...
