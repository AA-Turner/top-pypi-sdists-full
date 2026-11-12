"""Chat Collection — la colección `chats`: la conversación y la preview de la bandeja.

Desde el rediseño, `chats` no guarda mensajes ni estados de workflow. Esta colección escribe:

- el chat entero al crearlo (`insert`), y sin los campos con dueño al guardarlo (`update`);
- el resumen de los mensajes (`apply_message`, `apply_status`, `refresh_last_message`), que
  llama `ChatAssetService` después de escribir el mensaje en `chat_messages`.

La preview de la persona la escribe `ClientCollection` (fan-out) y `flow_ids` lo escribe
`ChatFlowStateCollection`.
"""

from typing import Collection, Optional
from bson import ObjectId
from datetime import datetime
from zoneinfo import ZoneInfo

from ....models.data_base.asset_collection import AssetCollection
from .chat_summary_pipeline import summary_update_pipeline
from ....models.chat.chat import Chat
from ....models.chat.chat_summary import ChatSummary
from ....models.chat.message_summary import MessageSummary
from ....models.base_models import ChattyAssetPreview
from ....models.data_base.mongo_connection import MongoConnection
from ....services.factories.chats.chat_factory import ChatFactory
from ....models.messages.chatty_messages import ChattyMessage
from ....models.utils import Status
from ....models.utils.types.identifier import StrObjectId
from ....models.utils.custom_exceptions.custom_exceptions import NotFoundError
from ....models.messages.meta_message_model.meta_status_json import ErrorDetail


def _now() -> datetime:
    return datetime.now(ZoneInfo("UTC"))


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

    async def update(self, asset: Chat) -> StrObjectId:
        """Guardado entero del chat SIN los campos con dueño (`Chat.WRITER_OWNED_FIELDS`).

        Un flujo que tiene el chat en memoria desde hace un rato no puede revertir el resumen
        de un mensaje que entró mientras tanto, ni la persona, ni los workflows.
        """
        if not isinstance(asset, Chat):
            raise ValueError(f"Asset must be of type {Chat.__name__}")
        asset.update_now()
        result = await self.collection.update_one({"_id": ObjectId(asset.id)}, {"$set": asset.to_update_document()})
        if result.matched_count == 0:
            raise NotFoundError(f"No document found with id {asset.id}")
        return asset.id

    async def update_fields(self, asset: Chat, fields: Collection[str]) -> StrObjectId:
        """`$set` de SOLO `fields`, y nunca un campo con dueño (`Chat.WRITER_OWNED_FIELDS`): el `update`
        de un servicio de assets no puede revertir el resumen, la persona ni los workflows de un chat."""
        if not isinstance(asset, Chat):
            raise ValueError(f"Asset must be of type {Chat.__name__}")
        asset.update_now()
        keys = {Chat.model_fields[name].alias or name for name in fields if name in Chat.model_fields}
        keys.add("updated_at")
        document = {key: value for key, value in asset.to_update_document().items() if key in keys}
        result = await self.collection.update_one({"_id": ObjectId(asset.id)}, {"$set": document})
        if result.matched_count == 0:
            raise NotFoundError(f"No document found with id {asset.id}")
        return asset.id

    # ── Resumen de los mensajes ──

    async def apply_message(self, chat_id: StrObjectId, message: ChattyMessage) -> None:
        """Aplica un mensaje ya guardado en `chat_messages` al resumen, sin hacerlo retroceder."""
        result = await self.collection.update_one({"_id": ObjectId(chat_id)}, summary_update_pipeline(message, _now()))
        if result.matched_count == 0:
            raise NotFoundError(f"No chat {chat_id} to apply message {message.id}", chat_id=chat_id)

    async def apply_status(self, chat_id: StrObjectId, message_id: str, status: Status, error_details: Optional[ErrorDetail] = None, *, confirmed_by_provider: bool) -> None:
        """Lleva el ✓✓ al resumen si el mensaje es el último o el último saliente.

        Con la misma condición que el mensaje: un estado que llega tarde no retrocede el resumen.
        """
        superseded = [s.value for s in status.superseded_statuses(confirmed_by_provider=confirmed_by_provider)] + [None]
        for field in ("last_message", "last_outgoing_message"):
            fields = {f"{field}.status": status.value}
            if error_details and field == "last_message":
                fields[f"{field}.error_details"] = error_details.model_dump(mode="json")
            await self.collection.update_one(
                {"_id": ObjectId(chat_id), f"{field}.id": message_id, f"{field}.status": {"$in": superseded}},
                {"$set": fields},
            )

    async def refresh_last_message(self, chat_id: StrObjectId, message: ChattyMessage) -> None:
        """Rehace la preview del último mensaje cuando ese mensaje se edita o se revoca."""
        summary = MessageSummary.from_message(message).to_document()
        await self.collection.update_one(
            {"_id": ObjectId(chat_id), "last_message.id": message.id},
            {"$set": {"last_message.preview": summary["preview"], "updated_at": _now()}},
        )

    async def write_summary(self, chat_id: StrObjectId, summary: ChatSummary) -> None:
        """Reemplaza el resumen entero. Para repararlo desde los bloques (`ChatSummary.from_messages`)."""
        await self.collection.update_one({"_id": ObjectId(chat_id)}, {"$set": {**summary.to_document(), "updated_at": _now()}})
