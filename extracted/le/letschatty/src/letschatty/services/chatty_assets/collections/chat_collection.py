"""Chat Collection - Pre-configured AssetCollection for Chats"""

from typing import Optional
from bson import ObjectId
from datetime import datetime
from zoneinfo import ZoneInfo

from ..asset_service import AssetCollection
from ....models.chat.chat import Chat
from ....models.base_models import ChattyAssetPreview
from ....models.data_base.mongo_connection import MongoConnection
from ....services.factories.chats.chat_factory import ChatFactory
from ....models.messages.chatty_messages import ChattyMessage
from ....models.utils import Status
from ....models.messages.meta_message_model.meta_status_json import ErrorDetail


class ChatCollection(AssetCollection[Chat, ChattyAssetPreview]):
    """Pre-configured collection for Chat assets"""

    def __init__(self, connection: MongoConnection):
        super().__init__(
            collection="chats",
            asset_type=Chat,
            connection=connection,
            create_instance_method=ChatFactory.from_json,
            preview_type=None
        )

    async def push_message(self, chat_id: str, message: ChattyMessage, update_last_message: bool = True) -> str:
        """Appends a single message to the messages array without loading the full chat."""
        import logging as _logging
        _logger = _logging.getLogger(__name__)
        msg_doc = message.model_dump(by_alias=True, mode='json')
        set_fields: dict = {"updated_at": datetime.now(ZoneInfo("UTC"))}
        if update_last_message:
            set_fields["last_message"] = msg_doc
            set_fields["last_message_timestamp"] = message.created_at
        result = await self.collection.update_one(
            {"_id": ObjectId(chat_id)},
            {"$push": {"messages": msg_doc}, "$set": set_fields},
        )
        _logger.info("[push_message] chat_id=%s message_id=%s matched=%d modified=%d", chat_id, message.id, result.matched_count, result.modified_count)
        if result.matched_count == 0:
            _logger.error("[push_message] CHAT NOT FOUND in DB — message was NOT saved! chat_id=%s message_id=%s", chat_id, message.id)
        return chat_id

    async def update_message_status(
        self,
        chat_id: str,
        message_id: str,
        status: Status,
        error_details: Optional[ErrorDetail] = None,
    ) -> str:
        """Updates status of one message using the positional operator."""
        set_fields: dict = {
            "messages.$.status": status.value,
            "updated_at": datetime.now(ZoneInfo("UTC")),
        }
        if error_details:
            set_fields["messages.$.error_details"] = error_details.model_dump(mode='json')
        await self.collection.update_one(
            {"_id": ObjectId(chat_id), "messages.id": message_id},
            {"$set": set_fields}
        )
        return chat_id
