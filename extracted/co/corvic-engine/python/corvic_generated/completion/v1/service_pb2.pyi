from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RetrieverType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RETRIEVER_TYPE_UNSPECIFIED: _ClassVar[RetrieverType]
    RETRIEVER_TYPE_SIMILARITY_SEARCH: _ClassVar[RetrieverType]
    RETRIEVER_TYPE_FAKE_SEARCH: _ClassVar[RetrieverType]

class EngineType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ENGINE_TYPE_UNSPECIFIED: _ClassVar[EngineType]
    ENGINE_TYPE_HUGGINGFACE_REMOTE: _ClassVar[EngineType]
    ENGINE_TYPE_HUGGINGFACE_LOCAL: _ClassVar[EngineType]
    ENGINE_TYPE_HUGGINGFACE_INFERENCE: _ClassVar[EngineType]
    ENGINE_TYPE_OPEN_AI: _ClassVar[EngineType]

class ChainType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHAIN_TYPE_UNSPECIFIED: _ClassVar[ChainType]
    CHAIN_TYPE_STUFF: _ClassVar[ChainType]
    CHAIN_TYPE_REFINE: _ClassVar[ChainType]
RETRIEVER_TYPE_UNSPECIFIED: RetrieverType
RETRIEVER_TYPE_SIMILARITY_SEARCH: RetrieverType
RETRIEVER_TYPE_FAKE_SEARCH: RetrieverType
ENGINE_TYPE_UNSPECIFIED: EngineType
ENGINE_TYPE_HUGGINGFACE_REMOTE: EngineType
ENGINE_TYPE_HUGGINGFACE_LOCAL: EngineType
ENGINE_TYPE_HUGGINGFACE_INFERENCE: EngineType
ENGINE_TYPE_OPEN_AI: EngineType
CHAIN_TYPE_UNSPECIFIED: ChainType
CHAIN_TYPE_STUFF: ChainType
CHAIN_TYPE_REFINE: ChainType

class CompleteResponse(_message.Message):
    __slots__ = ("text", "finish_reason", "created", "usage", "chunks")
    class Usage(_message.Message):
        __slots__ = ("prompt_tokens", "completion_tokens", "total_tokens", "context_tokens")
        PROMPT_TOKENS_FIELD_NUMBER: _ClassVar[int]
        COMPLETION_TOKENS_FIELD_NUMBER: _ClassVar[int]
        TOTAL_TOKENS_FIELD_NUMBER: _ClassVar[int]
        CONTEXT_TOKENS_FIELD_NUMBER: _ClassVar[int]
        prompt_tokens: int
        completion_tokens: int
        total_tokens: int
        context_tokens: int
        def __init__(self, prompt_tokens: _Optional[int] = ..., completion_tokens: _Optional[int] = ..., total_tokens: _Optional[int] = ..., context_tokens: _Optional[int] = ...) -> None: ...
    class Chunk(_message.Message):
        __slots__ = ("chunk_id", "document_id", "distance")
        CHUNK_ID_FIELD_NUMBER: _ClassVar[int]
        DOCUMENT_ID_FIELD_NUMBER: _ClassVar[int]
        DISTANCE_FIELD_NUMBER: _ClassVar[int]
        chunk_id: str
        document_id: str
        distance: float
        def __init__(self, chunk_id: _Optional[str] = ..., document_id: _Optional[str] = ..., distance: _Optional[float] = ...) -> None: ...
    TEXT_FIELD_NUMBER: _ClassVar[int]
    FINISH_REASON_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    CHUNKS_FIELD_NUMBER: _ClassVar[int]
    text: str
    finish_reason: str
    created: int
    usage: CompleteResponse.Usage
    chunks: _containers.RepeatedCompositeFieldContainer[CompleteResponse.Chunk]
    def __init__(self, text: _Optional[str] = ..., finish_reason: _Optional[str] = ..., created: _Optional[int] = ..., usage: _Optional[_Union[CompleteResponse.Usage, _Mapping]] = ..., chunks: _Optional[_Iterable[_Union[CompleteResponse.Chunk, _Mapping]]] = ...) -> None: ...

class CompleteRagResponse(_message.Message):
    __slots__ = ("text", "finish_reason", "created", "usage", "chunks")
    class Usage(_message.Message):
        __slots__ = ("prompt_tokens", "completion_tokens", "total_tokens", "context_tokens")
        PROMPT_TOKENS_FIELD_NUMBER: _ClassVar[int]
        COMPLETION_TOKENS_FIELD_NUMBER: _ClassVar[int]
        TOTAL_TOKENS_FIELD_NUMBER: _ClassVar[int]
        CONTEXT_TOKENS_FIELD_NUMBER: _ClassVar[int]
        prompt_tokens: int
        completion_tokens: int
        total_tokens: int
        context_tokens: int
        def __init__(self, prompt_tokens: _Optional[int] = ..., completion_tokens: _Optional[int] = ..., total_tokens: _Optional[int] = ..., context_tokens: _Optional[int] = ...) -> None: ...
    class Chunk(_message.Message):
        __slots__ = ("chunk_id", "document_id", "distance")
        CHUNK_ID_FIELD_NUMBER: _ClassVar[int]
        DOCUMENT_ID_FIELD_NUMBER: _ClassVar[int]
        DISTANCE_FIELD_NUMBER: _ClassVar[int]
        chunk_id: str
        document_id: str
        distance: float
        def __init__(self, chunk_id: _Optional[str] = ..., document_id: _Optional[str] = ..., distance: _Optional[float] = ...) -> None: ...
    TEXT_FIELD_NUMBER: _ClassVar[int]
    FINISH_REASON_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    CHUNKS_FIELD_NUMBER: _ClassVar[int]
    text: str
    finish_reason: str
    created: int
    usage: CompleteRagResponse.Usage
    chunks: _containers.RepeatedCompositeFieldContainer[CompleteRagResponse.Chunk]
    def __init__(self, text: _Optional[str] = ..., finish_reason: _Optional[str] = ..., created: _Optional[int] = ..., usage: _Optional[_Union[CompleteRagResponse.Usage, _Mapping]] = ..., chunks: _Optional[_Iterable[_Union[CompleteRagResponse.Chunk, _Mapping]]] = ...) -> None: ...

class GetDefaultResponse(_message.Message):
    __slots__ = ("sys_prompt", "max_chunks", "chain_type", "embed_engine", "embed_model_name", "workspace", "collection", "tag", "threshold", "retriever_type")
    SYS_PROMPT_FIELD_NUMBER: _ClassVar[int]
    MAX_CHUNKS_FIELD_NUMBER: _ClassVar[int]
    CHAIN_TYPE_FIELD_NUMBER: _ClassVar[int]
    EMBED_ENGINE_FIELD_NUMBER: _ClassVar[int]
    EMBED_MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    RETRIEVER_TYPE_FIELD_NUMBER: _ClassVar[int]
    sys_prompt: str
    max_chunks: int
    chain_type: ChainType
    embed_engine: EngineType
    embed_model_name: str
    workspace: str
    collection: str
    tag: str
    threshold: float
    retriever_type: RetrieverType
    def __init__(self, sys_prompt: _Optional[str] = ..., max_chunks: _Optional[int] = ..., chain_type: _Optional[_Union[ChainType, str]] = ..., embed_engine: _Optional[_Union[EngineType, str]] = ..., embed_model_name: _Optional[str] = ..., workspace: _Optional[str] = ..., collection: _Optional[str] = ..., tag: _Optional[str] = ..., threshold: _Optional[float] = ..., retriever_type: _Optional[_Union[RetrieverType, str]] = ...) -> None: ...

class CompleteRagRequest(_message.Message):
    __slots__ = ("model", "prompt", "room_id", "sys_prompt", "max_chunks", "chain_type", "embed_engine", "embed_model_name", "workspace", "collection", "tag", "threshold", "retriever_type")
    MODEL_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    SYS_PROMPT_FIELD_NUMBER: _ClassVar[int]
    MAX_CHUNKS_FIELD_NUMBER: _ClassVar[int]
    CHAIN_TYPE_FIELD_NUMBER: _ClassVar[int]
    EMBED_ENGINE_FIELD_NUMBER: _ClassVar[int]
    EMBED_MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    RETRIEVER_TYPE_FIELD_NUMBER: _ClassVar[int]
    model: str
    prompt: str
    room_id: int
    sys_prompt: str
    max_chunks: int
    chain_type: ChainType
    embed_engine: EngineType
    embed_model_name: str
    workspace: str
    collection: str
    tag: str
    threshold: float
    retriever_type: RetrieverType
    def __init__(self, model: _Optional[str] = ..., prompt: _Optional[str] = ..., room_id: _Optional[int] = ..., sys_prompt: _Optional[str] = ..., max_chunks: _Optional[int] = ..., chain_type: _Optional[_Union[ChainType, str]] = ..., embed_engine: _Optional[_Union[EngineType, str]] = ..., embed_model_name: _Optional[str] = ..., workspace: _Optional[str] = ..., collection: _Optional[str] = ..., tag: _Optional[str] = ..., threshold: _Optional[float] = ..., retriever_type: _Optional[_Union[RetrieverType, str]] = ...) -> None: ...

class CompleteRequest(_message.Message):
    __slots__ = ("model", "prompt", "sys_prompt")
    MODEL_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    SYS_PROMPT_FIELD_NUMBER: _ClassVar[int]
    model: str
    prompt: str
    sys_prompt: str
    def __init__(self, model: _Optional[str] = ..., prompt: _Optional[str] = ..., sys_prompt: _Optional[str] = ...) -> None: ...

class GetShaResponse(_message.Message):
    __slots__ = ("sha",)
    SHA_FIELD_NUMBER: _ClassVar[int]
    sha: str
    def __init__(self, sha: _Optional[str] = ...) -> None: ...

class GetShaRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetModelsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetDefaultRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Model(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetModelsResponse(_message.Message):
    __slots__ = ("names",)
    NAMES_FIELD_NUMBER: _ClassVar[int]
    names: _containers.RepeatedCompositeFieldContainer[Model]
    def __init__(self, names: _Optional[_Iterable[_Union[Model, _Mapping]]] = ...) -> None: ...
