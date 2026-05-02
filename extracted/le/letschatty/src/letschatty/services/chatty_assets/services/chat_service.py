"""Chat Service - Pre-configured AssetService for Chats"""

from typing import Optional
import logging

from ..asset_service import AssetService, CacheConfig
from ..collections import ChatCollection
from ....models.cache import CacheProtocol
from ....models.chat.chat import Chat
from ....models.base_models import ChattyAssetPreview
from ....models.data_base.mongo_connection import MongoConnection
from ....models.messages.chatty_messages import ChattyMessage
from ....models.utils import Status
from ....models.utils.types import MessageType
from ....models.messages.meta_message_model.meta_status_json import ErrorDetail
from ....models.execution.execution import ExecutionContext

logger = logging.getLogger("ChatAssetService")


class ChatAssetService(AssetService[Chat, ChattyAssetPreview]):
    """
    Pre-configured service for Chat assets with sensible defaults.

    Note: No event configuration - Chat events are handled by ChatsEditor, not AssetService.

    Partial-update methods (push_message, update_message_status) avoid loading and
    replacing the full Chat document, which is expensive when messages accumulate.
    """

    def __init__(self,
                 connection: MongoConnection,
                 cache_config: CacheConfig = CacheConfig.default(),
                 cache: Optional[CacheProtocol] = None):
        collection = ChatCollection(connection)
        super().__init__(
            collection=collection,
            cache_config=cache_config,
            cache=cache,
        )

    @property
    def _chat_collection(self) -> ChatCollection:
        return self.collection  # type: ignore[return-value]

    async def push_message(
        self,
        chat_id: str,
        message: ChattyMessage,
        execution_context: ExecutionContext,
    ) -> None:
        """Appends a message without loading or replacing the full Chat document."""
        update_last_message = message.type != MessageType.CENTRAL
        logger.info(
            "[push_message] chat_id=%s message_id=%s type=%s update_last_message=%s",
            chat_id, message.id, message.type, update_last_message,
        )
        await self._chat_collection.push_message(chat_id, message, update_last_message=update_last_message)
        logger.info("[push_message] done chat_id=%s message_id=%s", chat_id, message.id)
        execution_context.set_event_time(message.created_at)
        await self.cache.delete(self._item_key(chat_id))

    async def update_message_status(
        self,
        chat_id: str,
        message_id: str,
        status: Status,
        execution_context: ExecutionContext,
        error_details: Optional[ErrorDetail] = None,
    ) -> None:
        """Updates delivery status of one message by message_id."""
        await self._chat_collection.update_message_status(chat_id, message_id, status, error_details)
        await self.cache.delete(self._item_key(chat_id))
