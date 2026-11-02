import asyncio
import logging
import time
from datetime import UTC, datetime, timedelta
from typing import Any, NoReturn
from uuid import UUID

from httpx import AsyncClient, Client, HTTPStatusError, codes
from tenacity import (
    before_sleep_log,
    retry,
    stop_after_attempt,
    wait_exponential,
)

from edison_client.models.chat import (
    ChatConversationList,
    ChatDispatchStatus,
    ChatMessagePayload,
    ChatMessageResponse,
    ChatRecoverPayload,
    ChatRecoverResponse,
    ChatSandboxClaimResponse,
    ConversationDetail,
    QueueMessagePayload,
    QueueMessageResponse,
    StoreMessagePayload,
)
from edison_client.utils.general import (
    _BASE_CONNECTION_ERRORS,
    _PRE_REQUEST_CONNECTION_ERRORS,
    AMBIGUOUS_HTTP_STATUS_CODES,
    RETRYABLE_HTTP_STATUS_CODES,
    retry_if_connection_error,
    retry_if_connection_error_not_idempotent,
)

logger = logging.getLogger(__name__)


class ChatError(Exception):
    """Base exception for chat operations."""


class ChatFetchError(ChatError):
    """Raised when there's an error fetching chat data."""


_DELIVERY_CHECK_ATTEMPTS = 3
_DELIVERY_CHECK_WAIT_S = 10.0


_MAX_CONVERSATION_PAGE_LIMIT = 1000


class _ConversationFetch:
    def __init__(self, session_id: UUID, limit: int | None, offset: int) -> None:
        self.session_id = session_id
        self.fetch_all = limit is None
        self.page_limit = _MAX_CONVERSATION_PAGE_LIMIT if limit is None else limit
        self.offset = offset
        self.pages: list[ConversationDetail] = []
        self.page: ConversationDetail | None = None
        self.result: ConversationDetail | None = None
        self.load_more = True

    @property
    def params(self) -> dict[str, int | str]:
        if self.page is not None and self.page.continuation_cursor is not None:
            cursor = self.page.continuation_cursor
            return {
                "continuation_message_id": str(cursor.message_id),
                "continuation_block_index": cursor.block_index,
            }

        params: dict[str, int | str] = {"limit": self.page_limit}
        if self.offset:
            params["offset"] = self.offset
        return params

    def _prepend_conversation_continuation(
        self,
        continuation: ConversationDetail,
    ) -> None:
        """
        When a single message is too large, we receive the message content in chunks.

        This function prepends the older content to the current message content.
        """
        if (
            self.page is None
            or not self.page.messages
            or len(continuation.messages) != 1
        ):
            raise ChatFetchError("Invalid conversation continuation response")
        current = self.page.messages[0]
        older = continuation.messages[0]
        if not isinstance(current.content, list) or not isinstance(older.content, list):
            raise ChatFetchError("Conversation continuations require block content")
        current.content = [*older.content, *current.content]
        current.content_block_start = older.content_block_start
        self.page.has_more = self.page.has_more or continuation.has_more
        self.page.continuation_cursor = continuation.continuation_cursor

    def add_page(self, page: ConversationDetail) -> None:
        if self.page is None:
            self.page = page
        else:
            self._prepend_conversation_continuation(page)

        if self.page.continuation_cursor is not None:
            return

        if not self.fetch_all:
            self.result = self.page
            self.load_more = False
            return

        self.pages.append(self.page)
        if not self.page.has_more:
            self.result = ConversationDetail(
                messages=[
                    message
                    for page in reversed(self.pages)
                    for message in page.messages
                ],
                session_id=self.session_id,
                has_more=False,
            )
            self.load_more = False
            return

        self.offset += len(self.page.messages)
        self.page = None


def _chat_message_info(
    *,
    channel: str,
    data_storage_ids: list[str | UUID] | None,
) -> dict[str, Any]:
    info: dict[str, Any] = {"channel": channel}
    if data_storage_ids:
        info["data_storage_ids"] = [
            _normalize_data_storage_id(entry_id) for entry_id in data_storage_ids
        ]
    return info


def _normalize_data_storage_id(entry_id: str | UUID) -> str:
    if isinstance(entry_id, UUID):
        return str(entry_id)
    return entry_id.removeprefix("data_entry:")


class ChatMethods:
    """Chat and conversation methods for RestClient.

    This class contains methods for interacting with the chat and conversation
    API endpoints.
    """

    @property
    def client(self) -> Client:
        raise NotImplementedError("client property must be implemented by subclass")

    @property
    def async_client(self) -> AsyncClient:
        raise NotImplementedError(
            "async_client property must be implemented by subclass"
        )

    def _handle_chat_http_errors(  # noqa: PLR6301
        self,
        e: HTTPStatusError,
        operation: str,
        exc_class: type[ChatError] = ChatError,
    ) -> NoReturn:
        """Handle common HTTP errors for chat operations."""
        if e.response.status_code in RETRYABLE_HTTP_STATUS_CODES:
            raise e
        if e.response.status_code == codes.FORBIDDEN:
            raise exc_class(
                f"Error {operation}: {e.response.status_code} - {e.response.text}"
            ) from e
        if e.response.status_code == codes.UNPROCESSABLE_ENTITY:
            raise exc_class(f"Invalid request payload: {e.response.text}") from e
        raise exc_class(
            f"Error {operation}: {e.response.status_code} - {e.response.text}"
        ) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error_not_idempotent,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def send_chat_message(
        self,
        project_id: UUID,
        message: str,
        *,
        session_id: UUID | None = None,
        ttl_seconds: int | None = None,
        timeout: int | None = None,
        job_name: str | None = None,
        channel: str = "app",
        data_storage_ids: list[str | UUID] | None = None,
    ) -> ChatMessageResponse:
        """Send a chat message.

        Args:
            project_id: Project to chat within.
            message: User message content.
            session_id: Existing session ID, or None for a new session.
            ttl_seconds: Optional sandbox TTL override in seconds (60-86400).
            timeout: Optional execution timeout override in seconds per chat turn (30-172800).
            job_name: Job name identifying which agent to chat with.
            channel: Channel identifier for the message (default: "app").
            data_storage_ids: Optional DSS entry IDs (bare UUID or `data_entry:` URI
                stem) to attach to the user message.

        Returns:
            ChatMessageResponse with session_id and dispatch status.

        Raises:
            ChatError: If there's an error sending the message.
        """
        sent_at = datetime.now(UTC)
        try:
            payload = ChatMessagePayload(
                project_id=project_id,
                message=message,
                info=_chat_message_info(
                    channel=channel, data_storage_ids=data_storage_ids
                ),
                session_id=session_id,
                ttl_seconds=ttl_seconds,
                timeout=timeout,
                job_name=job_name,
            )
            response = self.client.post(
                "/v0.1/chat",
                json=payload.model_dump(mode="json", exclude_none=True),
            )
            response.raise_for_status()
            return ChatMessageResponse.model_validate(response.json())
        except ChatError:
            raise
        except Exception as e:
            if isinstance(e, HTTPStatusError):
                if e.response.status_code not in AMBIGUOUS_HTTP_STATUS_CODES:
                    self._handle_chat_http_errors(e, "sending chat message")
            elif not isinstance(e, _BASE_CONNECTION_ERRORS):
                raise ChatError(f"An unexpected error occurred: {e!r}") from e
            elif isinstance(e, _PRE_REQUEST_CONNECTION_ERRORS):
                raise
            if session_id is None:
                raise
            try:
                if self._chat_message_delivered(session_id, message, since=sent_at):
                    logger.warning(
                        "Sending to session %s failed with %r but the message was delivered",
                        session_id,
                        e,
                    )
                    return ChatMessageResponse(
                        session_id=session_id, status=ChatDispatchStatus.PENDING
                    )
            except Exception as check_error:
                logger.warning(
                    "An unexpected error occurred while checking if the message was delivered: %r",
                    check_error,
                )
            raise

    def _chat_message_delivered(
        self, session_id: UUID, content: str, *, since: datetime
    ) -> bool:
        for attempt in range(_DELIVERY_CHECK_ATTEMPTS):
            if attempt:
                time.sleep(_DELIVERY_CHECK_WAIT_S)
            if self._chat_message_queued(session_id, content) or _is_delivered(
                self.get_conversation(session_id), content, since=since
            ):
                return True
        return False

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
    )
    def _chat_message_queued(self, session_id: UUID, content: str) -> bool:
        response = self.client.get(f"/v0.1/conversations/queue/{session_id}/messages")
        response.raise_for_status()
        return any(row["message"].get("content") == content for row in response.json())

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error_not_idempotent,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def asend_chat_message(
        self,
        project_id: UUID,
        message: str,
        *,
        session_id: UUID | None = None,
        ttl_seconds: int | None = None,
        timeout: int | None = None,
        job_name: str | None = None,
        channel: str = "app",
        data_storage_ids: list[str | UUID] | None = None,
    ) -> ChatMessageResponse:
        """Send a chat message (async).

        Args:
            project_id: Project to chat within.
            message: User message content.
            session_id: Existing session ID, or None for a new session.
            ttl_seconds: Optional sandbox TTL override in seconds (60-86400).
            timeout: Optional execution timeout override in seconds per chat turn (30-172800).
            job_name: Job name identifying which agent to chat with.
            channel: Channel identifier for the message (default: "app").
            data_storage_ids: Optional DSS entry IDs (bare UUID or `data_entry:` URI
                stem) to attach to the user message.

        Returns:
            ChatMessageResponse with session_id and dispatch status.

        Raises:
            ChatError: If there's an error sending the message.
        """
        sent_at = datetime.now(UTC)
        try:
            payload = ChatMessagePayload(
                project_id=project_id,
                message=message,
                info=_chat_message_info(
                    channel=channel, data_storage_ids=data_storage_ids
                ),
                session_id=session_id,
                ttl_seconds=ttl_seconds,
                timeout=timeout,
                job_name=job_name,
            )
            response = await self.async_client.post(
                "/v0.1/chat",
                json=payload.model_dump(mode="json", exclude_none=True),
            )
            response.raise_for_status()
            return ChatMessageResponse.model_validate(response.json())
        except ChatError:
            raise
        except Exception as e:
            if isinstance(e, HTTPStatusError):
                if e.response.status_code not in AMBIGUOUS_HTTP_STATUS_CODES:
                    self._handle_chat_http_errors(e, "sending chat message")
            elif not isinstance(e, _BASE_CONNECTION_ERRORS):
                raise ChatError(f"An unexpected error occurred: {e!r}") from e
            elif isinstance(e, _PRE_REQUEST_CONNECTION_ERRORS):
                raise
            if session_id is None:
                raise
            try:
                if await self._achat_message_delivered(
                    session_id, message, since=sent_at
                ):
                    logger.warning(
                        "Sending to session %s failed with %r but the message was delivered",
                        session_id,
                        e,
                    )
                    return ChatMessageResponse(
                        session_id=session_id, status=ChatDispatchStatus.PENDING
                    )
            except Exception as check_error:
                logger.warning(
                    "An unexpected error occurred while checking if the message was delivered: %r",
                    check_error,
                )
            raise

    async def _achat_message_delivered(
        self, session_id: UUID, content: str, *, since: datetime
    ) -> bool:
        for attempt in range(_DELIVERY_CHECK_ATTEMPTS):
            if attempt:
                await asyncio.sleep(_DELIVERY_CHECK_WAIT_S)
            if await self._achat_message_queued(session_id, content) or _is_delivered(
                await self.aget_conversation(session_id), content, since=since
            ):
                return True
        return False

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
    )
    async def _achat_message_queued(self, session_id: UUID, content: str) -> bool:
        response = await self.async_client.get(
            f"/v0.1/conversations/queue/{session_id}/messages"
        )
        response.raise_for_status()
        return any(row["message"].get("content") == content for row in response.json())

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def recover_chat_session(
        self,
        session_id: UUID,
        project_id: UUID,
        *,
        job_name: str | None = None,
    ) -> ChatRecoverResponse:
        """Recover a chat session.

        Args:
            session_id: Session ID to recover.
            project_id: Project ID for recovery.
            job_name: Job name for the agent.

        Returns:
            ChatRecoverResponse with session status.

        Raises:
            ChatError: If there's an error recovering the session.
        """
        try:
            payload = ChatRecoverPayload(
                project_id=project_id,
                job_name=job_name,
            )
            response = self.client.post(
                f"/v0.1/chat/{session_id}/recover",
                json=payload.model_dump(mode="json", exclude_none=True),
            )
            response.raise_for_status()
            return ChatRecoverResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_chat_http_errors(e, "recovering chat session")
        except ChatError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise ChatError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def arecover_chat_session(
        self,
        session_id: UUID,
        project_id: UUID,
        *,
        job_name: str | None = None,
    ) -> ChatRecoverResponse:
        """Recover a chat session (async).

        Args:
            session_id: Session ID to recover.
            project_id: Project ID for recovery.
            job_name: Job name for the agent.

        Returns:
            ChatRecoverResponse with session status.

        Raises:
            ChatError: If there's an error recovering the session.
        """
        try:
            payload = ChatRecoverPayload(
                project_id=project_id,
                job_name=job_name,
            )
            response = await self.async_client.post(
                f"/v0.1/chat/{session_id}/recover",
                json=payload.model_dump(mode="json", exclude_none=True),
            )
            response.raise_for_status()
            return ChatRecoverResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_chat_http_errors(e, "recovering chat session")
        except ChatError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise ChatError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def get_conversations(
        self,
        *,
        session_id: UUID | None = None,
        limit: int = 25,
        offset: int = 0,
    ) -> ChatConversationList:
        """List conversations.

        Args:
            session_id: Optional filter by session ID.
            limit: Maximum number of conversations (default 25, max 200).
            offset: Number of conversations to skip.

        Returns:
            ChatConversationList with list of conversations.

        Raises:
            ChatFetchError: If there's an error fetching conversations.
        """
        try:
            params: dict[str, Any] = {"limit": limit, "offset": offset}
            if session_id is not None:
                params["session_id"] = str(session_id)
            response = self.client.get("/v0.1/conversations", params=params)
            response.raise_for_status()
            return ChatConversationList.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_chat_http_errors(e, "fetching conversations", ChatFetchError)
        except ChatError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise ChatFetchError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aget_conversations(
        self,
        *,
        session_id: UUID | None = None,
        limit: int = 25,
        offset: int = 0,
    ) -> ChatConversationList:
        """List conversations (async).

        Args:
            session_id: Optional filter by session ID.
            limit: Maximum number of conversations (default 25, max 200).
            offset: Number of conversations to skip.

        Returns:
            ChatConversationList with list of conversations.

        Raises:
            ChatFetchError: If there's an error fetching conversations.
        """
        try:
            params: dict[str, Any] = {"limit": limit, "offset": offset}
            if session_id is not None:
                params["session_id"] = str(session_id)
            response = await self.async_client.get("/v0.1/conversations", params=params)
            response.raise_for_status()
            return ChatConversationList.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_chat_http_errors(e, "fetching conversations", ChatFetchError)
        except ChatError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise ChatFetchError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def get_conversation(
        self,
        session_id: UUID,
        *,
        limit: int | None = 50,
        offset: int = 0,
    ) -> ConversationDetail:
        """Get a conversation by session ID.

        Args:
            session_id: Session ID to look up.
            limit: Maximum number of messages to return (most recent by
                sort_order). Pass ``None`` to fetch all messages.
            offset: Number of messages to skip from the end.

        Returns:
            ConversationDetail with messages and session_id.

        Raises:
            ValueError: If offset is set without limit.
            ChatFetchError: If there's an error fetching the conversation.
        """
        if limit is None and offset:
            raise ValueError("offset requires limit to be set")
        fetch = _ConversationFetch(session_id, limit, offset)
        try:
            while fetch.load_more:
                response = self.client.get(
                    f"/v0.1/conversations/{session_id}",
                    params=fetch.params,
                )
                response.raise_for_status()
                fetch.add_page(ConversationDetail.model_validate(response.json()))
        except HTTPStatusError as e:
            self._handle_chat_http_errors(e, "fetching conversation", ChatFetchError)
        except ChatError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise ChatFetchError(f"An unexpected error occurred: {e!r}") from e
        if fetch.result is None:
            raise ChatFetchError("Conversation fetch completed without a result")
        return fetch.result

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aget_conversation(
        self,
        session_id: UUID,
        *,
        limit: int | None = 50,
        offset: int = 0,
    ) -> ConversationDetail:
        """Get a conversation by session ID (async).

        Args:
            session_id: Session ID to look up.
            limit: Maximum number of messages to return (most recent by
                sort_order). Pass ``None`` to fetch all messages.
            offset: Number of messages to skip from the end.

        Returns:
            ConversationDetail with messages and session_id.

        Raises:
            ValueError: If offset is set without limit.
            ChatFetchError: If there's an error fetching the conversation.
        """
        if limit is None and offset:
            raise ValueError("offset requires limit to be set")
        fetch = _ConversationFetch(session_id, limit, offset)
        try:
            while fetch.load_more:
                response = await self.async_client.get(
                    f"/v0.1/conversations/{session_id}",
                    params=fetch.params,
                )
                response.raise_for_status()
                fetch.add_page(ConversationDetail.model_validate(response.json()))
        except HTTPStatusError as e:
            self._handle_chat_http_errors(e, "fetching conversation", ChatFetchError)
        except ChatError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise ChatFetchError(f"An unexpected error occurred: {e!r}") from e
        if fetch.result is None:
            raise ChatFetchError("Conversation fetch completed without a result")
        return fetch.result

    # ── store_conversation_message ─────────────────────────────────────

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def store_conversation_message(
        self,
        session_id: UUID,
        message: dict,
        *,
        metadata: dict | None = None,
    ) -> None:
        """Store a conversation message.

        Args:
            session_id: Session ID to store the message in.
            message: Message JSON (aviary Message format).
            metadata: Optional metadata to attach to the message.

        Raises:
            ChatError: If there's an error storing the message.
        """
        try:
            payload = StoreMessagePayload(
                message=message,
                metadata=metadata,
            )
            response = self.client.post(
                f"/v0.1/conversations/{session_id}/messages",
                json=payload.model_dump(mode="json", exclude_none=True),
            )
            response.raise_for_status()
        except HTTPStatusError as e:
            self._handle_chat_http_errors(e, "storing conversation message")
        except ChatError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise ChatError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def astore_conversation_message(
        self,
        session_id: UUID,
        message: dict,
        *,
        metadata: dict | None = None,
    ) -> None:
        """Store a conversation message (async).

        Args:
            session_id: Session ID to store the message in.
            message: Message JSON (aviary Message format).
            metadata: Optional metadata to attach to the message.

        Raises:
            ChatError: If there's an error storing the message.
        """
        try:
            payload = StoreMessagePayload(
                message=message,
                metadata=metadata,
            )
            response = await self.async_client.post(
                f"/v0.1/conversations/{session_id}/messages",
                json=payload.model_dump(mode="json", exclude_none=True),
            )
            response.raise_for_status()
        except HTTPStatusError as e:
            self._handle_chat_http_errors(e, "storing conversation message")
        except ChatError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise ChatError(f"An unexpected error occurred: {e!r}") from e

    # ── queue_chat_message ─────────────────────────────────────────────

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def queue_chat_message(
        self,
        session_id: UUID,
        project_id: UUID,
        message: str,
    ) -> QueueMessageResponse:
        """Queue a message for injection into a running chat session.

        The message is placed in the pending queue and picked up by the
        rollout's ``before_transition`` hook on its next step.

        Args:
            session_id: Target chat session ID.
            project_id: Project the session belongs to.
            message: User message content.

        Returns:
            QueueMessageResponse with the pending message ID and target ID.

        Raises:
            ChatError: If there's an error queueing the message.
        """
        try:
            payload = QueueMessagePayload(
                target_id=session_id,
                project_id=project_id,
                message=message,
            )
            response = self.client.post(
                "/v0.1/conversations/queue",
                json=payload.model_dump(mode="json"),
            )
            response.raise_for_status()
            return QueueMessageResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_chat_http_errors(e, "queueing chat message")
        except ChatError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise ChatError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aqueue_chat_message(
        self,
        session_id: UUID,
        project_id: UUID,
        message: str,
    ) -> QueueMessageResponse:
        """Queue a message for injection into a running chat session (async).

        The message is placed in the pending queue and picked up by the
        rollout's ``before_transition`` hook on its next step.

        Args:
            session_id: Target chat session ID.
            project_id: Project the session belongs to.
            message: User message content.

        Returns:
            QueueMessageResponse with the pending message ID and target ID.

        Raises:
            ChatError: If there's an error queueing the message.
        """
        try:
            payload = QueueMessagePayload(
                target_id=session_id,
                project_id=project_id,
                message=message,
            )
            response = await self.async_client.post(
                "/v0.1/conversations/queue",
                json=payload.model_dump(mode="json"),
            )
            response.raise_for_status()
            return QueueMessageResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_chat_http_errors(e, "queueing chat message")
        except ChatError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise ChatError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def get_chat_sandbox_claim(self, session_id: UUID) -> ChatSandboxClaimResponse:
        """Read the recorded sandbox claim for a chat session."""
        try:
            response = self.client.get(f"/v0.1/chat/{session_id}/sandbox-claim")
            return self._parse_chat_sandbox_claim(response)
        except HTTPStatusError as e:
            self._handle_chat_http_errors(
                e, "fetching chat sandbox claim", ChatFetchError
            )
        except ChatError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise ChatFetchError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aget_chat_sandbox_claim(
        self, session_id: UUID
    ) -> ChatSandboxClaimResponse:
        """Read the recorded sandbox claim for a chat session."""
        try:
            response = await self.async_client.get(
                f"/v0.1/chat/{session_id}/sandbox-claim"
            )
            return self._parse_chat_sandbox_claim(response)
        except HTTPStatusError as e:
            self._handle_chat_http_errors(
                e, "fetching chat sandbox claim", ChatFetchError
            )
        except ChatError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise ChatFetchError(f"An unexpected error occurred: {e!r}") from e

    @staticmethod
    def _parse_chat_sandbox_claim(response: Any) -> ChatSandboxClaimResponse:
        response.raise_for_status()
        return ChatSandboxClaimResponse.model_validate(response.json())


def _is_delivered(
    conversation: ConversationDetail, content: str, *, since: datetime
) -> bool:
    cutoff = since - timedelta(seconds=30)  # max skew between client and server
    return any(
        m.role == "user" and m.content == content and m.created_at >= cutoff
        for m in conversation.messages
    )
