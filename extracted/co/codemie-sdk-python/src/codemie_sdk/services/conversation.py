"""Conversation service implementation."""

from __future__ import annotations

import requests

from ..models.conversation import (
    AdminConversationListResponse,
    Conversation,
    ConversationDetails,
    ConversationCreateRequest,
    ConversationFinishBulkRequest,
    ConversationFinishBulkResponse,
    ConversationFinishResponse,
    UpdateConversationRequest,
    ConversationFolder,
    UpdateConversationFolderRequest,
    UpdateHistoryByIndexRequest,
    UpsertHistoryRequest,
    UpsertHistoryResponse,
    BaseResponse,
    ConversationShareRequest,
    ConversationShareResponse,
    SharedConversationResponse,
    FeedbackCreateRequest,
    FeedbackCreateResponse,
    FeedbackDeleteRequest,
)
from ..models.assistant import AssistantChatRequest
from ..utils import ApiRequestHandler, TokenSource


class ConversationService:
    """Service for managing user conversations."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the conversation service.

        Args:
            api_domain: Base URL for the API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def list(self, is_finished: bool | None = None) -> list[Conversation]:
        """Get list of all conversations for the current user.

        Args:
            is_finished: Optional filter narrowing the list to finished (True)
                or unfinished (False) conversations only. Maps to the
                ``isFinished`` query parameter.

        Returns:
            List of all conversations for the current user.
        """
        params = {"isFinished": is_finished} if is_finished is not None else None
        return self._api.get("/v1/conversations", list[Conversation], params=params)

    def list_by_assistant_id(self, assistant_id: str) -> list[Conversation]:
        """Get list of all conversations for the current user that include the specified assistant.

        Args:
            assistant_id: Assistant ID

        Returns:
            List of conversations for the specified assistant.
        """
        return [
            conv
            for conv in self._api.get("/v1/conversations", list[Conversation])
            if assistant_id in conv.assistant_ids
        ]

    def get_conversation(self, conversation_id: str) -> ConversationDetails:
        """Get details for a specific conversation by its ID.

        Args:
            conversation_id: Conversation ID

        Returns:
            Conversation details
        """
        return self._api.get(
            f"/v1/conversations/{conversation_id}",
            ConversationDetails,
        )

    def create(self, request: ConversationCreateRequest) -> dict:
        """Create a new conversation.

        Args:
            request: Conversation creation request

        Returns:
            Created conversation details
        """
        return self._api.post(
            "/v1/conversations",
            dict,
            json_data=request.model_dump(exclude_none=True, by_alias=True),
        )

    def chat(
        self,
        conversation_id: str,
        request: AssistantChatRequest,
        headers: dict[str, str] | None = None,
    ) -> requests.Response | ConversationDetails:
        """Send a chat message to a conversation.

        This method is used for workflow chat mode where the workflow_id is set
        as the initial_assistant_id when creating the conversation.

        Args:
            conversation_id: Conversation ID to send message to
            request: Chat request details
            headers: Optional additional HTTP headers (e.g., X-* for MCP propagation)

        Returns:
            ConversationDetails with updated history or streaming response
        """
        response = self._api.put(
            f"/v1/conversations/{conversation_id}",
            ConversationDetails,
            json_data=request.model_dump(exclude_none=True, by_alias=True),
            stream=request.stream,
            extra_headers=headers,
        )
        return response

    def delete(self, conversation_id: str) -> dict:
        """Delete a specific conversation by its ID.

        Args:
            conversation_id: Conversation ID to delete

        Returns:
            Deletion confirmation
        """
        return self._api.delete(
            f"/v1/conversations/{conversation_id}",
            dict,
        )

    def update(
        self, conversation_id: str, request: UpdateConversationRequest
    ) -> ConversationDetails:
        """Update an existing conversation.

        Args:
            conversation_id: Conversation ID to update
            request: Update request with fields to modify

        Returns:
            Updated conversation details
        """
        return self._api.put(
            f"/v1/conversations/{conversation_id}",
            ConversationDetails,
            json_data=request.model_dump(exclude_none=True),
        )

    def delete_all(self) -> BaseResponse:
        """Delete all conversations for the current user.

        Returns:
            Deletion confirmation
        """
        return self._api.delete("/v1/conversations", BaseResponse)

    def get_files(self, conversation_id: str) -> list:
        """Get list of files attached to a conversation.

        Args:
            conversation_id: Conversation ID

        Returns:
            List of file names
        """
        response = self._api.get(
            f"/v1/conversations/{conversation_id}/files",
            dict,
            wrap_response=False,
        )
        # API returns list directly, not wrapped in 'data' field

        return response

    # Folder management methods

    def list_folders(self) -> list[ConversationFolder]:
        """Get list of all conversation folders for the current user.

        Returns:
            List of conversation folders
        """
        return self._api.get("/v1/conversations/folders/list", list[ConversationFolder])

    def create_folder(self, request: UpdateConversationFolderRequest) -> BaseResponse:
        """Create a new conversation folder.

        Args:
            request: Folder creation request with name

        Returns:
            Creation confirmation
        """
        return self._api.post(
            "/v1/conversations/folder",
            BaseResponse,
            json_data=request.model_dump(exclude_none=True),
        )

    def update_folder(
        self, folder: str, request: UpdateConversationFolderRequest
    ) -> BaseResponse:
        """Rename an existing conversation folder.

        Args:
            folder: Current folder name
            request: Update request with new name

        Returns:
            Update confirmation
        """
        return self._api.put(
            f"/v1/conversations/folder/{folder}",
            BaseResponse,
            json_data=request.model_dump(exclude_none=True),
        )

    def delete_folder(
        self, folder: str, remove_conversations: bool = False
    ) -> BaseResponse:
        """Delete a conversation folder.

        Args:
            folder: Folder name to delete
            remove_conversations: Whether to also delete conversations in the folder

        Returns:
            Deletion confirmation
        """
        endpoint = f"/v1/conversations/folder/{folder}"
        if remove_conversations:
            endpoint += "?remove_conversations=true"
        else:
            endpoint += "?remove_conversations=false"

        return self._api.delete(endpoint, BaseResponse)

    # History management methods

    def upsert_history(
        self, conversation_id: str, request: UpsertHistoryRequest
    ) -> UpsertHistoryResponse:
        """Create or update conversation with history (idempotent upsert).

        If conversation doesn't exist, creates it with custom ID and provided history.
        If conversation exists, appends only NEW messages not already present.

        Args:
            conversation_id: Conversation ID (will be created if doesn't exist)
            request: History upsert request with messages

        Returns:
            Upsert response with metadata about operation
        """
        return self._api.put(
            f"/v1/conversations/{conversation_id}/history",
            UpsertHistoryResponse,
            json_data=request.model_dump(mode="json", exclude_none=True),
        )

    def delete_history(self, conversation_id: str) -> ConversationDetails:
        """Clear all history from a conversation.

        Args:
            conversation_id: Conversation ID

        Returns:
            Updated conversation details with empty history
        """
        return self._api.delete(
            f"/v1/conversations/{conversation_id}/history",
            ConversationDetails,
        )

    def delete_history_by_index(
        self, conversation_id: str, history_index: int
    ) -> ConversationDetails:
        """Remove a specific history item by index.

        Args:
            conversation_id: Conversation ID
            history_index: Index of history item to delete

        Returns:
            Updated conversation details
        """
        return self._api.delete(
            f"/v1/conversations/{conversation_id}/history/{history_index}",
            ConversationDetails,
        )

    def update_history_by_index(
        self, conversation_id: str, request: UpdateHistoryByIndexRequest
    ) -> ConversationDetails:
        """Update an Assistant response in conversation history by index.

        Args:
            conversation_id: Conversation ID
            request: Update request with message index and new message content

        Returns:
            Updated conversation details
        """
        return self._api.put(
            f"/v1/conversations/{conversation_id}/history/{request.messageIndex}",
            ConversationDetails,
            json_data=request.model_dump(exclude_none=True),
        )

    def share_conversation(self, chat_id: str) -> ConversationShareResponse:
        """Create a share link for a conversation.

        Args:
            chat_id: Conversation ID to share

        Returns:
            Share response with token and metadata
        """
        request = ConversationShareRequest(chat_id=chat_id)
        return self._api.post(
            "/v1/share/conversations",
            ConversationShareResponse,
            json_data=request.model_dump(exclude_none=True),
        )

    def get_shared_conversation(self, token: str) -> SharedConversationResponse:
        """Get a shared conversation using its share token.

        Args:
            token: Share token

        Returns:
            Shared conversation details including history
        """
        return self._api.get(
            f"/v1/share/conversations/{token}",
            SharedConversationResponse,
        )

    # Feedback management methods (EPMCDME-14625)

    def create_feedback(self, request: FeedbackCreateRequest) -> FeedbackCreateResponse:
        """Submit like/dislike feedback on an assistant message.

        Args:
            request: Feedback creation request. ``response`` is required by the
                backend contract -- see ``FeedbackCreateRequest`` docstring.

        Returns:
            FeedbackCreateResponse with the id of the stored feedback entry
        """
        return self._api.post(
            "/v1/feedback",
            FeedbackCreateResponse,
            json_data=request.model_dump(by_alias=True, exclude_none=True),
        )

    def delete_feedback(self, request: FeedbackDeleteRequest) -> BaseResponse:
        """Delete a previously submitted feedback entry.

        Args:
            request: Feedback deletion request

        Returns:
            BaseResponse confirmation message
        """
        return self._api.delete(
            "/v1/feedback",
            BaseResponse,
            json_data=request.model_dump(by_alias=True, exclude_none=True),
        )

    # Conversation finishing (EPMCDME-11067)

    def finish(self, conversation_id: str) -> ConversationFinishResponse:
        """Mark a conversation as finished (owner-only).

        Not idempotent: a repeat call on an already-finished conversation
        raises HTTP 409 rather than returning success again.

        Args:
            conversation_id: Conversation ID to finish

        Returns:
            ConversationFinishResponse with the conversation ID and timestamp
        """
        return self._api.post(
            f"/v1/conversations/{conversation_id}/finish",
            ConversationFinishResponse,
        )

    def finish_bulk(
        self, conversation_ids: list[str]
    ) -> ConversationFinishBulkResponse:
        """Finish multiple conversations in one request (admin-only).

        Idempotent per ID: already-finished IDs are reported with
        already_finished=True instead of erroring. Unknown IDs are reported
        with error="not_found".

        Args:
            conversation_ids: List of conversation IDs to finish (1-500)

        Returns:
            ConversationFinishBulkResponse with per-ID results
        """
        request = ConversationFinishBulkRequest(conversation_ids=conversation_ids)
        return self._api.post(
            "/v1/admin/conversations/finish-bulk",
            ConversationFinishBulkResponse,
            json_data=request.model_dump(by_alias=True),
        )

    def list_admin(
        self,
        is_finished: bool | None = None,
        started_after: str | None = None,
        project: str | None = None,
        page: int = 0,
        per_page: int = 20,
    ) -> AdminConversationListResponse:
        """Paginated, cross-user conversation list for admin/scheduler use (admin-only).

        Args:
            is_finished: Optional filter (maps to ``isFinished``)
            started_after: Optional ISO datetime lower bound (maps to ``startedAt``)
            project: Optional project ID to scope the listing to one application
            page: Page number (0-based)
            per_page: Number of items per page (maps to ``perPage``)

        Returns:
            AdminConversationListResponse with items and pagination metadata
        """
        params: dict = {"page": page, "perPage": per_page}
        if is_finished is not None:
            params["isFinished"] = is_finished
        if started_after is not None:
            params["startedAt"] = started_after
        if project is not None:
            params["project"] = project

        return self._api.get(
            "/v1/admin/conversations",
            AdminConversationListResponse,
            params=params,
            wrap_response=False,
        )
