import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ToolCallStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TOOL_CALL_STATUS_UNSPECIFIED: _ClassVar[ToolCallStatus]
    TOOL_CALL_STATUS_APPROVED: _ClassVar[ToolCallStatus]
    TOOL_CALL_STATUS_DENIED: _ClassVar[ToolCallStatus]
    TOOL_CALL_STATUS_AWAITING_APPROVAL: _ClassVar[ToolCallStatus]
TOOL_CALL_STATUS_UNSPECIFIED: ToolCallStatus
TOOL_CALL_STATUS_APPROVED: ToolCallStatus
TOOL_CALL_STATUS_DENIED: ToolCallStatus
TOOL_CALL_STATUS_AWAITING_APPROVAL: ToolCallStatus

class GetSnapshotRidByUserMessageIdRequest(_message.Message):
    __slots__ = ("conversation_rid", "message_id")
    CONVERSATION_RID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    conversation_rid: str
    message_id: str
    def __init__(self, conversation_rid: _Optional[str] = ..., message_id: _Optional[str] = ...) -> None: ...

class GetSnapshotRidByUserMessageIdResponse(_message.Message):
    __slots__ = ("snapshot_rid",)
    SNAPSHOT_RID_FIELD_NUMBER: _ClassVar[int]
    snapshot_rid: str
    def __init__(self, snapshot_rid: _Optional[str] = ...) -> None: ...

class ReadOnlyMode(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class EditMode(_message.Message):
    __slots__ = ("auto_accept",)
    AUTO_ACCEPT_FIELD_NUMBER: _ClassVar[int]
    auto_accept: bool
    def __init__(self, auto_accept: bool = ...) -> None: ...

class ConversationMode(_message.Message):
    __slots__ = ("read_only", "edit")
    READ_ONLY_FIELD_NUMBER: _ClassVar[int]
    EDIT_FIELD_NUMBER: _ClassVar[int]
    read_only: ReadOnlyMode
    edit: EditMode
    def __init__(self, read_only: _Optional[_Union[ReadOnlyMode, _Mapping]] = ..., edit: _Optional[_Union[EditMode, _Mapping]] = ...) -> None: ...

class ToolApprovalResult(_message.Message):
    __slots__ = ("tool_call_id", "approved", "denied")
    TOOL_CALL_ID_FIELD_NUMBER: _ClassVar[int]
    APPROVED_FIELD_NUMBER: _ClassVar[int]
    DENIED_FIELD_NUMBER: _ClassVar[int]
    tool_call_id: str
    approved: ToolApprovedResponse
    denied: ToolDeniedResponse
    def __init__(self, tool_call_id: _Optional[str] = ..., approved: _Optional[_Union[ToolApprovedResponse, _Mapping]] = ..., denied: _Optional[_Union[ToolDeniedResponse, _Mapping]] = ...) -> None: ...

class ToolApprovedResponse(_message.Message):
    __slots__ = ("override_args",)
    OVERRIDE_ARGS_FIELD_NUMBER: _ClassVar[int]
    override_args: str
    def __init__(self, override_args: _Optional[str] = ...) -> None: ...

class ToolDeniedResponse(_message.Message):
    __slots__ = ("denial_reason",)
    DENIAL_REASON_FIELD_NUMBER: _ClassVar[int]
    denial_reason: str
    def __init__(self, denial_reason: _Optional[str] = ...) -> None: ...

class RetryRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UserPromptRequest(_message.Message):
    __slots__ = ("message", "images")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    message: UserModelMessage
    images: _containers.RepeatedCompositeFieldContainer[ImagePart]
    def __init__(self, message: _Optional[_Union[UserModelMessage, _Mapping]] = ..., images: _Optional[_Iterable[_Union[ImagePart, _Mapping]]] = ...) -> None: ...

class ToolApprovalRequest(_message.Message):
    __slots__ = ("tool_approvals",)
    TOOL_APPROVALS_FIELD_NUMBER: _ClassVar[int]
    tool_approvals: _containers.RepeatedCompositeFieldContainer[ToolApprovalResult]
    def __init__(self, tool_approvals: _Optional[_Iterable[_Union[ToolApprovalResult, _Mapping]]] = ...) -> None: ...

class StreamChatRequest(_message.Message):
    __slots__ = ("conversation_rid", "message", "images", "tool_approvals", "retry", "user_prompt", "tool_approval", "workbook")
    CONVERSATION_RID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    TOOL_APPROVALS_FIELD_NUMBER: _ClassVar[int]
    RETRY_FIELD_NUMBER: _ClassVar[int]
    USER_PROMPT_FIELD_NUMBER: _ClassVar[int]
    TOOL_APPROVAL_FIELD_NUMBER: _ClassVar[int]
    WORKBOOK_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_FIELD_NUMBER: _ClassVar[int]
    conversation_rid: str
    message: UserModelMessage
    images: _containers.RepeatedCompositeFieldContainer[ImagePart]
    tool_approvals: _containers.RepeatedCompositeFieldContainer[ToolApprovalResult]
    retry: RetryRequest
    user_prompt: UserPromptRequest
    tool_approval: ToolApprovalRequest
    workbook: WorkbookContext
    def __init__(self, conversation_rid: _Optional[str] = ..., message: _Optional[_Union[UserModelMessage, _Mapping]] = ..., images: _Optional[_Iterable[_Union[ImagePart, _Mapping]]] = ..., tool_approvals: _Optional[_Iterable[_Union[ToolApprovalResult, _Mapping]]] = ..., retry: _Optional[_Union[RetryRequest, _Mapping]] = ..., user_prompt: _Optional[_Union[UserPromptRequest, _Mapping]] = ..., tool_approval: _Optional[_Union[ToolApprovalRequest, _Mapping]] = ..., workbook: _Optional[_Union[WorkbookContext, _Mapping]] = ..., **kwargs) -> None: ...

class WorkbookContext(_message.Message):
    __slots__ = ("workbook_rid", "user_presence")
    WORKBOOK_RID_FIELD_NUMBER: _ClassVar[int]
    USER_PRESENCE_FIELD_NUMBER: _ClassVar[int]
    workbook_rid: str
    user_presence: WorkbookUserPresence
    def __init__(self, workbook_rid: _Optional[str] = ..., user_presence: _Optional[_Union[WorkbookUserPresence, _Mapping]] = ...) -> None: ...

class GlobalContext(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class WorkbookUserPresence(_message.Message):
    __slots__ = ("tab_index", "range")
    TAB_INDEX_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    tab_index: int
    range: TimeRange
    def __init__(self, tab_index: _Optional[int] = ..., range: _Optional[_Union[TimeRange, _Mapping]] = ...) -> None: ...

class CreateConversationRequest(_message.Message):
    __slots__ = ("title", "workspace_rid", "old_conversation_rid", "previous_message_id", "conversation_mode")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    OLD_CONVERSATION_RID_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_MODE_FIELD_NUMBER: _ClassVar[int]
    title: str
    workspace_rid: str
    old_conversation_rid: str
    previous_message_id: str
    conversation_mode: ConversationMode
    def __init__(self, title: _Optional[str] = ..., workspace_rid: _Optional[str] = ..., old_conversation_rid: _Optional[str] = ..., previous_message_id: _Optional[str] = ..., conversation_mode: _Optional[_Union[ConversationMode, _Mapping]] = ...) -> None: ...

class CreateConversationResponse(_message.Message):
    __slots__ = ("new_conversation_rid",)
    NEW_CONVERSATION_RID_FIELD_NUMBER: _ClassVar[int]
    new_conversation_rid: str
    def __init__(self, new_conversation_rid: _Optional[str] = ...) -> None: ...

class UpdateConversationMetadataRequest(_message.Message):
    __slots__ = ("title", "conversation_rid", "conversation_mode")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_RID_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_MODE_FIELD_NUMBER: _ClassVar[int]
    title: str
    conversation_rid: str
    conversation_mode: ConversationMode
    def __init__(self, title: _Optional[str] = ..., conversation_rid: _Optional[str] = ..., conversation_mode: _Optional[_Union[ConversationMode, _Mapping]] = ...) -> None: ...

class UpdateConversationMetadataResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteConversationRequest(_message.Message):
    __slots__ = ("conversation_rid",)
    CONVERSATION_RID_FIELD_NUMBER: _ClassVar[int]
    conversation_rid: str
    def __init__(self, conversation_rid: _Optional[str] = ...) -> None: ...

class DeleteConversationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetConversationRequest(_message.Message):
    __slots__ = ("conversation_rid", "page_start_message_id", "max_message_count")
    CONVERSATION_RID_FIELD_NUMBER: _ClassVar[int]
    PAGE_START_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    MAX_MESSAGE_COUNT_FIELD_NUMBER: _ClassVar[int]
    conversation_rid: str
    page_start_message_id: str
    max_message_count: int
    def __init__(self, conversation_rid: _Optional[str] = ..., page_start_message_id: _Optional[str] = ..., max_message_count: _Optional[int] = ...) -> None: ...

class ModelMessageWithId(_message.Message):
    __slots__ = ("message", "tool_action", "message_id", "snapshot_rid", "tool_approval_requests")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TOOL_ACTION_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_RID_FIELD_NUMBER: _ClassVar[int]
    TOOL_APPROVAL_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    message: ModelMessage
    tool_action: ToolAction
    message_id: str
    snapshot_rid: str
    tool_approval_requests: _containers.RepeatedCompositeFieldContainer[ToolCallDescription]
    def __init__(self, message: _Optional[_Union[ModelMessage, _Mapping]] = ..., tool_action: _Optional[_Union[ToolAction, _Mapping]] = ..., message_id: _Optional[str] = ..., snapshot_rid: _Optional[str] = ..., tool_approval_requests: _Optional[_Iterable[_Union[ToolCallDescription, _Mapping]]] = ...) -> None: ...

class GetConversationResponse(_message.Message):
    __slots__ = ("ordered_messages", "conversation_metadata")
    ORDERED_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_METADATA_FIELD_NUMBER: _ClassVar[int]
    ordered_messages: _containers.RepeatedCompositeFieldContainer[ModelMessageWithId]
    conversation_metadata: ConversationMetadata
    def __init__(self, ordered_messages: _Optional[_Iterable[_Union[ModelMessageWithId, _Mapping]]] = ..., conversation_metadata: _Optional[_Union[ConversationMetadata, _Mapping]] = ...) -> None: ...

class ListConversationsRequest(_message.Message):
    __slots__ = ("workspace_rid", "next_page_token", "page_size")
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    workspace_rid: str
    next_page_token: str
    page_size: int
    def __init__(self, workspace_rid: _Optional[str] = ..., next_page_token: _Optional[str] = ..., page_size: _Optional[int] = ...) -> None: ...

class ConversationMetadata(_message.Message):
    __slots__ = ("conversation_rid", "title", "created_at", "last_updated_at", "mode")
    CONVERSATION_RID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    conversation_rid: str
    title: str
    created_at: _timestamp_pb2.Timestamp
    last_updated_at: _timestamp_pb2.Timestamp
    mode: ConversationMode
    def __init__(self, conversation_rid: _Optional[str] = ..., title: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., mode: _Optional[_Union[ConversationMode, _Mapping]] = ...) -> None: ...

class ListConversationsResponse(_message.Message):
    __slots__ = ("conversations", "next_page_token")
    CONVERSATIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    conversations: _containers.RepeatedCompositeFieldContainer[ConversationMetadata]
    next_page_token: str
    def __init__(self, conversations: _Optional[_Iterable[_Union[ConversationMetadata, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class TimeRange(_message.Message):
    __slots__ = ("range_start", "range_end")
    RANGE_START_FIELD_NUMBER: _ClassVar[int]
    RANGE_END_FIELD_NUMBER: _ClassVar[int]
    range_start: Timestamp
    range_end: Timestamp
    def __init__(self, range_start: _Optional[_Union[Timestamp, _Mapping]] = ..., range_end: _Optional[_Union[Timestamp, _Mapping]] = ...) -> None: ...

class Timestamp(_message.Message):
    __slots__ = ("seconds", "nanoseconds")
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    NANOSECONDS_FIELD_NUMBER: _ClassVar[int]
    seconds: int
    nanoseconds: int
    def __init__(self, seconds: _Optional[int] = ..., nanoseconds: _Optional[int] = ...) -> None: ...

class ModelMessage(_message.Message):
    __slots__ = ("user", "assistant")
    USER_FIELD_NUMBER: _ClassVar[int]
    ASSISTANT_FIELD_NUMBER: _ClassVar[int]
    user: UserModelMessage
    assistant: AssistantModelMessage
    def __init__(self, user: _Optional[_Union[UserModelMessage, _Mapping]] = ..., assistant: _Optional[_Union[AssistantModelMessage, _Mapping]] = ...) -> None: ...

class UserModelMessage(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: _containers.RepeatedCompositeFieldContainer[UserContentPart]
    def __init__(self, text: _Optional[_Iterable[_Union[UserContentPart, _Mapping]]] = ...) -> None: ...

class AssistantModelMessage(_message.Message):
    __slots__ = ("content_parts",)
    CONTENT_PARTS_FIELD_NUMBER: _ClassVar[int]
    content_parts: _containers.RepeatedCompositeFieldContainer[AssistantContentPart]
    def __init__(self, content_parts: _Optional[_Iterable[_Union[AssistantContentPart, _Mapping]]] = ...) -> None: ...

class UserContentPart(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: TextPart
    def __init__(self, text: _Optional[_Union[TextPart, _Mapping]] = ...) -> None: ...

class AssistantContentPart(_message.Message):
    __slots__ = ("text", "reasoning")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    REASONING_FIELD_NUMBER: _ClassVar[int]
    text: TextPart
    reasoning: ReasoningPart
    def __init__(self, text: _Optional[_Union[TextPart, _Mapping]] = ..., reasoning: _Optional[_Union[ReasoningPart, _Mapping]] = ...) -> None: ...

class TextPart(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...

class ImagePart(_message.Message):
    __slots__ = ("data", "media_type", "filename")
    DATA_FIELD_NUMBER: _ClassVar[int]
    MEDIA_TYPE_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    media_type: str
    filename: str
    def __init__(self, data: _Optional[bytes] = ..., media_type: _Optional[str] = ..., filename: _Optional[str] = ...) -> None: ...

class ReasoningPart(_message.Message):
    __slots__ = ("reasoning",)
    REASONING_FIELD_NUMBER: _ClassVar[int]
    reasoning: str
    def __init__(self, reasoning: _Optional[str] = ...) -> None: ...

class StreamChatResponse(_message.Message):
    __slots__ = ("finish", "error", "text_start", "text_delta", "text_end", "reasoning_start", "reasoning_delta", "reasoning_end", "tool_action")
    FINISH_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TEXT_START_FIELD_NUMBER: _ClassVar[int]
    TEXT_DELTA_FIELD_NUMBER: _ClassVar[int]
    TEXT_END_FIELD_NUMBER: _ClassVar[int]
    REASONING_START_FIELD_NUMBER: _ClassVar[int]
    REASONING_DELTA_FIELD_NUMBER: _ClassVar[int]
    REASONING_END_FIELD_NUMBER: _ClassVar[int]
    TOOL_ACTION_FIELD_NUMBER: _ClassVar[int]
    finish: Finish
    error: Error
    text_start: TextStart
    text_delta: TextDelta
    text_end: TextEnd
    reasoning_start: ReasoningStart
    reasoning_delta: ReasoningDelta
    reasoning_end: ReasoningEnd
    tool_action: ToolAction
    def __init__(self, finish: _Optional[_Union[Finish, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ..., text_start: _Optional[_Union[TextStart, _Mapping]] = ..., text_delta: _Optional[_Union[TextDelta, _Mapping]] = ..., text_end: _Optional[_Union[TextEnd, _Mapping]] = ..., reasoning_start: _Optional[_Union[ReasoningStart, _Mapping]] = ..., reasoning_delta: _Optional[_Union[ReasoningDelta, _Mapping]] = ..., reasoning_end: _Optional[_Union[ReasoningEnd, _Mapping]] = ..., tool_action: _Optional[_Union[ToolAction, _Mapping]] = ...) -> None: ...

class ToolCallDescription(_message.Message):
    __slots__ = ("tool_call_id", "tool_name", "tool_args_json_string", "status")
    TOOL_CALL_ID_FIELD_NUMBER: _ClassVar[int]
    TOOL_NAME_FIELD_NUMBER: _ClassVar[int]
    TOOL_ARGS_JSON_STRING_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    tool_call_id: str
    tool_name: str
    tool_args_json_string: str
    status: ToolCallStatus
    def __init__(self, tool_call_id: _Optional[str] = ..., tool_name: _Optional[str] = ..., tool_args_json_string: _Optional[str] = ..., status: _Optional[_Union[ToolCallStatus, str]] = ...) -> None: ...

class Finish(_message.Message):
    __slots__ = ("ordered_message_ids", "new_title", "tool_approval_requests")
    ORDERED_MESSAGE_IDS_FIELD_NUMBER: _ClassVar[int]
    NEW_TITLE_FIELD_NUMBER: _ClassVar[int]
    TOOL_APPROVAL_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    ordered_message_ids: _containers.RepeatedScalarFieldContainer[str]
    new_title: str
    tool_approval_requests: _containers.RepeatedCompositeFieldContainer[ToolCallDescription]
    def __init__(self, ordered_message_ids: _Optional[_Iterable[str]] = ..., new_title: _Optional[str] = ..., tool_approval_requests: _Optional[_Iterable[_Union[ToolCallDescription, _Mapping]]] = ...) -> None: ...

class Error(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class TextStart(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class TextDelta(_message.Message):
    __slots__ = ("id", "delta")
    ID_FIELD_NUMBER: _ClassVar[int]
    DELTA_FIELD_NUMBER: _ClassVar[int]
    id: str
    delta: str
    def __init__(self, id: _Optional[str] = ..., delta: _Optional[str] = ...) -> None: ...

class TextEnd(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ReasoningStart(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ReasoningDelta(_message.Message):
    __slots__ = ("id", "delta")
    ID_FIELD_NUMBER: _ClassVar[int]
    DELTA_FIELD_NUMBER: _ClassVar[int]
    id: str
    delta: str
    def __init__(self, id: _Optional[str] = ..., delta: _Optional[str] = ...) -> None: ...

class ReasoningEnd(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ToolAction(_message.Message):
    __slots__ = ("id", "tool_action_verb", "tool_target")
    ID_FIELD_NUMBER: _ClassVar[int]
    TOOL_ACTION_VERB_FIELD_NUMBER: _ClassVar[int]
    TOOL_TARGET_FIELD_NUMBER: _ClassVar[int]
    id: str
    tool_action_verb: str
    tool_target: str
    def __init__(self, id: _Optional[str] = ..., tool_action_verb: _Optional[str] = ..., tool_target: _Optional[str] = ...) -> None: ...
