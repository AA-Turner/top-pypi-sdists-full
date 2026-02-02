from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StoreType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STORE_TYPE_UNSPECIFIED: _ClassVar[StoreType]
    STORE_TYPE_DATA_ROOM: _ClassVar[StoreType]
    STORE_TYPE_KNOWLEDGE_BASE: _ClassVar[StoreType]
STORE_TYPE_UNSPECIFIED: StoreType
STORE_TYPE_DATA_ROOM: StoreType
STORE_TYPE_KNOWLEDGE_BASE: StoreType

class StoreEntry(_message.Message):
    __slots__ = ("id", "name", "type")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    type: StoreType
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., type: _Optional[_Union[StoreType, str]] = ...) -> None: ...

class DocumentChunk(_message.Message):
    __slots__ = ("blob",)
    BLOB_FIELD_NUMBER: _ClassVar[int]
    blob: bytes
    def __init__(self, blob: _Optional[bytes] = ...) -> None: ...

class DocumentMetadata(_message.Message):
    __slots__ = ("name", "mime_type", "store_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    MIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    STORE_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    mime_type: str
    store_id: int
    def __init__(self, name: _Optional[str] = ..., mime_type: _Optional[str] = ..., store_id: _Optional[int] = ...) -> None: ...

class DocumentEntry(_message.Message):
    __slots__ = ("id", "name", "mime_type", "url", "crc32", "store_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    CRC32_FIELD_NUMBER: _ClassVar[int]
    STORE_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    mime_type: str
    url: str
    crc32: str
    store_id: int
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., mime_type: _Optional[str] = ..., url: _Optional[str] = ..., crc32: _Optional[str] = ..., store_id: _Optional[int] = ...) -> None: ...

class CreateStoreRequest(_message.Message):
    __slots__ = ("name", "type")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: StoreType
    def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[StoreType, str]] = ...) -> None: ...

class CreateStoreResponse(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: StoreEntry
    def __init__(self, entry: _Optional[_Union[StoreEntry, _Mapping]] = ...) -> None: ...

class DeleteStoreRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class DeleteStoreResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetStoreRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class GetStoreResponse(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: StoreEntry
    def __init__(self, entry: _Optional[_Union[StoreEntry, _Mapping]] = ...) -> None: ...

class ListStoresRequest(_message.Message):
    __slots__ = ("name", "type")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: StoreType
    def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[StoreType, str]] = ...) -> None: ...

class ListStoresResponse(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: StoreEntry
    def __init__(self, entry: _Optional[_Union[StoreEntry, _Mapping]] = ...) -> None: ...

class UploadDocumentRequest(_message.Message):
    __slots__ = ("metadata", "data")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    metadata: DocumentMetadata
    data: DocumentChunk
    def __init__(self, metadata: _Optional[_Union[DocumentMetadata, _Mapping]] = ..., data: _Optional[_Union[DocumentChunk, _Mapping]] = ...) -> None: ...

class UploadDocumentResponse(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: DocumentEntry
    def __init__(self, entry: _Optional[_Union[DocumentEntry, _Mapping]] = ...) -> None: ...

class CreateUploadURLRequest(_message.Message):
    __slots__ = ("metadata", "origin")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    metadata: DocumentMetadata
    origin: str
    def __init__(self, metadata: _Optional[_Union[DocumentMetadata, _Mapping]] = ..., origin: _Optional[str] = ...) -> None: ...

class CreateUploadURLResponse(_message.Message):
    __slots__ = ("url", "token")
    URL_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    url: str
    token: str
    def __init__(self, url: _Optional[str] = ..., token: _Optional[str] = ...) -> None: ...

class UploadURLTokenPayload(_message.Message):
    __slots__ = ("metadata", "filename")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    metadata: DocumentMetadata
    filename: str
    def __init__(self, metadata: _Optional[_Union[DocumentMetadata, _Mapping]] = ..., filename: _Optional[str] = ...) -> None: ...

class FinalizeUploadURLRequest(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class FinalizeUploadURLResponse(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: DocumentEntry
    def __init__(self, entry: _Optional[_Union[DocumentEntry, _Mapping]] = ...) -> None: ...

class DeleteDocumentRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class DeleteDocumentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetDocumentRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class GetDocumentResponse(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: DocumentEntry
    def __init__(self, entry: _Optional[_Union[DocumentEntry, _Mapping]] = ...) -> None: ...

class ListDocumentsOfStoreRequest(_message.Message):
    __slots__ = ("store_id",)
    STORE_ID_FIELD_NUMBER: _ClassVar[int]
    store_id: int
    def __init__(self, store_id: _Optional[int] = ...) -> None: ...

class ListDocumentsOfStoreResponse(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: DocumentEntry
    def __init__(self, entry: _Optional[_Union[DocumentEntry, _Mapping]] = ...) -> None: ...

class CreateStructuredUploadURLRequest(_message.Message):
    __slots__ = ("metadata", "origin")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    metadata: DocumentMetadata
    origin: str
    def __init__(self, metadata: _Optional[_Union[DocumentMetadata, _Mapping]] = ..., origin: _Optional[str] = ...) -> None: ...

class CreateStructuredUploadURLResponse(_message.Message):
    __slots__ = ("url", "token")
    URL_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    url: str
    token: str
    def __init__(self, url: _Optional[str] = ..., token: _Optional[str] = ...) -> None: ...

class FinalizeStructuredUploadURLRequest(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class FinalizeStructuredUploadURLResponse(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: DocumentEntry
    def __init__(self, entry: _Optional[_Union[DocumentEntry, _Mapping]] = ...) -> None: ...
