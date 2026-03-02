from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KnowledgeBaseType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    KNOWLEDGE_BASE_TYPE_UNSPECIFIED: _ClassVar[KnowledgeBaseType]
    KNOWLEDGE_BASE_TYPE_PROMPT: _ClassVar[KnowledgeBaseType]
    KNOWLEDGE_BASE_TYPE_EMBEDDING: _ClassVar[KnowledgeBaseType]
KNOWLEDGE_BASE_TYPE_UNSPECIFIED: KnowledgeBaseType
KNOWLEDGE_BASE_TYPE_PROMPT: KnowledgeBaseType
KNOWLEDGE_BASE_TYPE_EMBEDDING: KnowledgeBaseType

class CreateOrUpdateKnowledgeBaseRequest(_message.Message):
    __slots__ = ("attachment_rid", "summary_description", "type")
    ATTACHMENT_RID_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    attachment_rid: str
    summary_description: str
    type: KnowledgeBaseType
    def __init__(self, attachment_rid: _Optional[str] = ..., summary_description: _Optional[str] = ..., type: _Optional[_Union[KnowledgeBaseType, str]] = ...) -> None: ...

class CreateOrUpdateKnowledgeBaseResponse(_message.Message):
    __slots__ = ("knowledge_base_rid",)
    KNOWLEDGE_BASE_RID_FIELD_NUMBER: _ClassVar[int]
    knowledge_base_rid: str
    def __init__(self, knowledge_base_rid: _Optional[str] = ...) -> None: ...

class KnowledgeBase(_message.Message):
    __slots__ = ("knowledge_base_rid", "attachment_rid", "workspace_rid", "summary_description", "type", "version")
    KNOWLEDGE_BASE_RID_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENT_RID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    knowledge_base_rid: str
    attachment_rid: str
    workspace_rid: str
    summary_description: str
    type: KnowledgeBaseType
    version: int
    def __init__(self, knowledge_base_rid: _Optional[str] = ..., attachment_rid: _Optional[str] = ..., workspace_rid: _Optional[str] = ..., summary_description: _Optional[str] = ..., type: _Optional[_Union[KnowledgeBaseType, str]] = ..., version: _Optional[int] = ...) -> None: ...

class ListRequest(_message.Message):
    __slots__ = ("workspace_rid",)
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    workspace_rid: str
    def __init__(self, workspace_rid: _Optional[str] = ...) -> None: ...

class ListResponse(_message.Message):
    __slots__ = ("knowledge_bases",)
    KNOWLEDGE_BASES_FIELD_NUMBER: _ClassVar[int]
    knowledge_bases: _containers.RepeatedCompositeFieldContainer[KnowledgeBase]
    def __init__(self, knowledge_bases: _Optional[_Iterable[_Union[KnowledgeBase, _Mapping]]] = ...) -> None: ...

class DeleteRequest(_message.Message):
    __slots__ = ("knowledge_base_rid",)
    KNOWLEDGE_BASE_RID_FIELD_NUMBER: _ClassVar[int]
    knowledge_base_rid: str
    def __init__(self, knowledge_base_rid: _Optional[str] = ...) -> None: ...

class DeleteResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class GetBatchRequest(_message.Message):
    __slots__ = ("knowledge_base_rids",)
    KNOWLEDGE_BASE_RIDS_FIELD_NUMBER: _ClassVar[int]
    knowledge_base_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, knowledge_base_rids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetBatchResponse(_message.Message):
    __slots__ = ("knowledge_bases",)
    KNOWLEDGE_BASES_FIELD_NUMBER: _ClassVar[int]
    knowledge_bases: _containers.RepeatedCompositeFieldContainer[KnowledgeBase]
    def __init__(self, knowledge_bases: _Optional[_Iterable[_Union[KnowledgeBase, _Mapping]]] = ...) -> None: ...

class GenerateSummaryDescriptionRequest(_message.Message):
    __slots__ = ("attachment_rid",)
    ATTACHMENT_RID_FIELD_NUMBER: _ClassVar[int]
    attachment_rid: str
    def __init__(self, attachment_rid: _Optional[str] = ...) -> None: ...

class GenerateSummaryDescriptionResponse(_message.Message):
    __slots__ = ("summary_description",)
    SUMMARY_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    summary_description: str
    def __init__(self, summary_description: _Optional[str] = ...) -> None: ...
