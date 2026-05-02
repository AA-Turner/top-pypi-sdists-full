from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserMessage(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...

class AgentMessage(_message.Message):
    __slots__ = ("agent_model", "text", "documents")
    class DocumentReference(_message.Message):
        __slots__ = ("document_id",)
        DOCUMENT_ID_FIELD_NUMBER: _ClassVar[int]
        document_id: int
        def __init__(self, document_id: _Optional[int] = ...) -> None: ...
    AGENT_MODEL_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    DOCUMENTS_FIELD_NUMBER: _ClassVar[int]
    agent_model: str
    text: str
    documents: _containers.RepeatedCompositeFieldContainer[AgentMessage.DocumentReference]
    def __init__(self, agent_model: _Optional[str] = ..., text: _Optional[str] = ..., documents: _Optional[_Iterable[_Union[AgentMessage.DocumentReference, _Mapping]]] = ...) -> None: ...

class MessageEntry(_message.Message):
    __slots__ = ("id", "thread_id", "store_id", "user_message", "agent_message")
    ID_FIELD_NUMBER: _ClassVar[int]
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    STORE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    AGENT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    id: int
    thread_id: int
    store_id: int
    user_message: UserMessage
    agent_message: AgentMessage
    def __init__(self, id: _Optional[int] = ..., thread_id: _Optional[int] = ..., store_id: _Optional[int] = ..., user_message: _Optional[_Union[UserMessage, _Mapping]] = ..., agent_message: _Optional[_Union[AgentMessage, _Mapping]] = ...) -> None: ...

class ThreadEntry(_message.Message):
    __slots__ = ("id", "store_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    STORE_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    store_id: int
    def __init__(self, id: _Optional[int] = ..., store_id: _Optional[int] = ...) -> None: ...

class CreateThreadRequest(_message.Message):
    __slots__ = ("store_id",)
    STORE_ID_FIELD_NUMBER: _ClassVar[int]
    store_id: int
    def __init__(self, store_id: _Optional[int] = ...) -> None: ...

class CreateThreadResponse(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: ThreadEntry
    def __init__(self, entry: _Optional[_Union[ThreadEntry, _Mapping]] = ...) -> None: ...

class DeleteThreadRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class DeleteThreadResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListThreadsRequest(_message.Message):
    __slots__ = ("store_id",)
    STORE_ID_FIELD_NUMBER: _ClassVar[int]
    store_id: int
    def __init__(self, store_id: _Optional[int] = ...) -> None: ...

class ListThreadsResponse(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: ThreadEntry
    def __init__(self, entry: _Optional[_Union[ThreadEntry, _Mapping]] = ...) -> None: ...

class AppendMessageRequest(_message.Message):
    __slots__ = ("text", "thread_id")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    text: str
    thread_id: int
    def __init__(self, text: _Optional[str] = ..., thread_id: _Optional[int] = ...) -> None: ...

class AppendMessageResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetMessagesCursor(_message.Message):
    __slots__ = ("thread_id", "store_id", "last_message_sent")
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    STORE_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_MESSAGE_SENT_FIELD_NUMBER: _ClassVar[int]
    thread_id: int
    store_id: int
    last_message_sent: int
    def __init__(self, thread_id: _Optional[int] = ..., store_id: _Optional[int] = ..., last_message_sent: _Optional[int] = ...) -> None: ...

class GetMessagesRequest(_message.Message):
    __slots__ = ("thread_id", "store_id", "cursor", "max_most_recent")
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    STORE_ID_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    MAX_MOST_RECENT_FIELD_NUMBER: _ClassVar[int]
    thread_id: int
    store_id: int
    cursor: str
    max_most_recent: int
    def __init__(self, thread_id: _Optional[int] = ..., store_id: _Optional[int] = ..., cursor: _Optional[str] = ..., max_most_recent: _Optional[int] = ...) -> None: ...

class UpToDateSentinel(_message.Message):
    __slots__ = ("cursor",)
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    def __init__(self, cursor: _Optional[str] = ...) -> None: ...

class GetMessagesResponse(_message.Message):
    __slots__ = ("cursor", "messages")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    messages: _containers.RepeatedCompositeFieldContainer[MessageEntry]
    def __init__(self, cursor: _Optional[str] = ..., messages: _Optional[_Iterable[_Union[MessageEntry, _Mapping]]] = ...) -> None: ...
