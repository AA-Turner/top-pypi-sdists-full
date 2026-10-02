"""Models for conversation-related data structures."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from codemie_sdk.models.assistant import ContextType


class Conversation(BaseModel):
    """
    Model for conversation summary data as returned from the list endpoint.
    """

    model_config = ConfigDict(extra="ignore")

    id: str
    name: str
    folder: str | None
    pinned: bool
    date: str
    assistant_ids: list[str]
    initial_assistant_id: str | None
    finished_at: datetime | None = None


class Mark(BaseModel):
    """Model for conversation review/mark data."""

    mark: str
    rating: int
    comments: str
    date: datetime
    operator: Operator | None = None


class Operator(BaseModel):
    """Represents an operator involved in marking a conversation."""

    user_id: str
    name: str


class Thought(BaseModel):
    """Model for reasoning or tool-invocation within a message's history."""

    id: str
    parent_id: str | None
    metadata: dict
    in_progress: bool
    input_text: str | None
    message: str | None
    author_type: str
    author_name: str
    output_format: str | None
    error: bool | None
    children: list[str]


class HistoryMark(BaseModel):
    """Model for conversation history review/mark data."""

    mark: str
    rating: int | None = None
    comments: str | None
    date: datetime
    type: str | None = None
    feedback_id: str | None = None


class HistoryItem(BaseModel):
    """Represents an individual message within a conversation's history."""

    role: str
    message: str
    historyIndex: int
    date: datetime
    responseTime: float | None = None
    inputTokens: int | None = None
    outputTokens: int | None = None
    cacheCreationInputTokens: int | None = None
    cacheReadInputTokens: int | None = None
    moneySpent: float | None = None
    userMark: HistoryMark | None = None
    operatorMark: HistoryMark | None = None
    messageRaw: str | None = None
    fileNames: list[str]
    assistantId: str | None = None
    thoughts: list[Thought] | None = Field(default_factory=list)
    workflowExecutionRef: str | bool | None = None
    executionId: str | None = None
    # WorkflowExecutionStatusEnum value, e.g. "In Progress" (EPMCDME-14075)
    executionStatus: str | None = None


class ContextItem(BaseModel):
    """Represents contextual settings for conversation."""

    context_type: ContextType | None
    name: str


class ToolItem(BaseModel):
    """Represents a tool used by an assistant, including configuration and description."""

    name: str
    label: str | None
    settings_config: bool | None
    description: str | None = None
    user_description: str | None


class AssistantDataItem(BaseModel):
    """Model represents details for an assistant included in a conversation."""

    assistant_id: str
    assistant_name: str
    assistant_icon: str | None
    assistant_type: str | None
    context: list[ContextItem | str] | None = None
    tools: list[ToolItem] | None = None
    conversation_starters: list[str] = []


class ConversationDetailsData(BaseModel):
    """Extended details about a conversation's configuration and context."""

    llm_model: str | None
    context: list[ContextItem]
    app_name: str | None
    repo_name: str | None
    index_type: str | None


class AssistantDetailsData(BaseModel):
    """Extended details about an assistant included in a conversation."""

    assistant_id: str
    assistant_name: str
    assistant_icon: str | None
    assistant_type: str | None
    context: list[ContextItem | str]
    tools: list[ToolItem]
    conversation_starters: list[str]


class ConversationCreateRequest(BaseModel):
    """Model for creating a new conversation."""

    initial_assistant_id: str | None = None
    folder: str | None = None
    mcp_server_single_usage: bool | None = False
    is_workflow_conversation: bool | None = Field(
        default=None, serialization_alias="is_workflow"
    )


class ConversationDetails(BaseModel):
    """Summary information for a user conversation as returned from list endpoints."""

    id: str
    date: datetime
    update_date: datetime
    conversation_id: str
    conversation_name: str
    llm_model: str | None
    folder: str | None
    pinned: bool
    history: list[HistoryItem]
    user_id: str
    user_name: str
    assistant_ids: list[str]
    assistant_data: list[AssistantDataItem]
    initial_assistant_id: str
    final_user_mark: Mark | None
    final_operator_mark: Mark | None
    project: str | None
    conversation_details: ConversationDetailsData | None
    assistant_details: AssistantDetailsData | None
    user_abilities: list[str] | None
    is_folder_migrated: bool
    is_workflow_conversation: bool | None = None
    category: str | None
    mcp_server_single_usage: bool | None = False
    finished_at: datetime | None = None


class ConversationShareRequest(BaseModel):
    """Model for creating share conversation request."""

    chat_id: str


class ConversationShareResponse(BaseModel):
    """Model for conversation share response."""

    share_id: str
    token: str
    created_at: str
    access_count: int


class SharedConversationResponse(BaseModel):
    """Model for shared conversation details response."""

    conversation: ConversationDetails
    shared_by: str
    created_at: str
    access_count: int


class BaseResponse(BaseModel):
    """Generic base response model with message field."""

    message: str


class UpdateConversationRequest(BaseModel):
    """Model for updating an existing conversation."""

    name: str | None = None
    folder: str | None = None
    pinned: bool | None = None


class ConversationFolder(BaseModel):
    """Model for conversation folder metadata."""

    id: str
    user_id: str
    folder_name: str
    date: str
    update_date: str
    user_abilities: list[str]


class UpdateConversationFolderRequest(BaseModel):
    """Model for creating or updating a folder name."""

    folder: str


class UpdateHistoryByIndexRequest(BaseModel):
    """Model for updating message content in conversation history by index."""

    messageIndex: int
    message: str


class UpsertHistoryRequest(BaseModel):
    """Model for upserting conversation history."""

    history: list[HistoryItem]
    assistant_id: str | None = None
    folder: str | None = None


class UpsertHistoryResponse(BaseModel):
    """Response model for conversation history upsert operation."""

    conversation_id: str
    new_messages: int
    total_messages: int
    created: bool


class ConversationFinishResponse(BaseModel):
    """Response for POST /conversations/{conversation_id}/finish (owner-only, not idempotent).

    Already-finished conversations cause the server to raise HTTP 409 rather
    than return this response again.
    """

    model_config = ConfigDict(populate_by_name=True)

    conversation_id: str = Field(alias="conversationId")
    finished_at: datetime = Field(alias="finishedAt")


class ConversationFinishResult(BaseModel):
    """Per-conversation-ID result entry within a bulk-finish response."""

    model_config = ConfigDict(populate_by_name=True)

    conversation_id: str = Field(alias="conversationId")
    already_finished: bool = Field(default=False, alias="alreadyFinished")
    finished_at: datetime | None = Field(default=None, alias="finishedAt")
    error: str | None = None


class ConversationFinishBulkRequest(BaseModel):
    """Request body for POST /admin/conversations/finish-bulk."""

    model_config = ConfigDict(populate_by_name=True)

    conversation_ids: list[str] = Field(alias="conversationIds")


class ConversationFinishBulkResponse(BaseModel):
    """Response for POST /admin/conversations/finish-bulk (admin-only, idempotent per ID)."""

    total: int
    results: list[ConversationFinishResult]


class ConversationPagination(BaseModel):
    """Pagination metadata for the admin conversation list endpoint."""

    page: int
    per_page: int
    total: int
    pages: int


class AdminConversationListResponse(BaseModel):
    """Paginated response for GET /admin/conversations (admin-only, cross-user)."""

    data: list[Conversation]
    pagination: ConversationPagination


# Feedback on assistant messages (EPMCDME-14625)


class FeedbackMark(str, Enum):
    """Sentiment recorded for a piece of feedback on an assistant message."""

    CORRECT = "correct"
    PARTIALLY_CORRECT = "partially correct"
    WRONG = "wrong"


class FeedbackAuthor(str, Enum):
    """Who a feedback entry is attributed to."""

    USER = "user"
    OPERATOR = "operator"


class FeedbackCreateRequest(BaseModel):
    """Model for submitting like/dislike feedback on an assistant message (POST /v1/feedback).

    ``response`` is required by the backend even though the client already has
    the text elsewhere: omitting it returns a 422 ``response: Field required``
    error. This was the root cause of EPMCDME-14625, where the frontend built
    the payload without it and negative feedback could never be submitted.
    Callers must always populate ``response`` -- an empty string is a valid
    value for incomplete, failed, or technical-error assistant responses.
    """

    model_config = ConfigDict(populate_by_name=True)

    conversation_id: str = Field(alias="conversationId")
    message_index: int = Field(alias="messageIndex")
    assistant_id: str
    request: str
    response: str
    mark: FeedbackMark
    author: FeedbackAuthor = FeedbackAuthor.USER
    comments: str | None = None
    type: str | None = None
    feedback_id: str | None = None


class FeedbackCreateResponse(BaseModel):
    """Response for POST /v1/feedback: the id of the stored feedback entry."""

    id: str


class FeedbackDeleteRequest(BaseModel):
    """Model for deleting a feedback entry on an assistant message (DELETE /v1/feedback)."""

    model_config = ConfigDict(populate_by_name=True)

    conversation_id: str = Field(alias="conversationId")
    feedback_id: str = Field(alias="feedbackId")
    message_index: int = Field(alias="messageIndex")
    assistant_id: str
    author: FeedbackAuthor = FeedbackAuthor.USER
