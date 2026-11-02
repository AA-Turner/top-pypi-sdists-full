"""Un solo lugar que arma un `Chat` desde sus cuatro colecciones, y la forma vieja para la UI.

`ChatLoader.load` lee `chats` y, sólo si se pide, los mensajes (una ventana o todo el
historial), la persona completa y los estados de workflow. Lo que no se pide no se carga, y
leerlo lanza en vez de devolver vacío.

`LegacyChatShape` rearma la forma que la web, la app y los demás servicios leen hoy: `client`
con la persona completa y las etiquetas, productos, ventas, touchpoints, highlights y calidad
adentro; `flow_states` con `asset_id`. Lo usan api-chatty (endpoints), cintia-reader y polls,
para que la forma vieja la arme un solo código y no diverja.
"""
from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, Literal, Optional, Union

from pydantic import BaseModel

from ..collections.client_collection import ClientCollection
from ..collections.chat_messages_collection import ChatMessagesCollection
from ..collections.chat_flow_state_collection import ChatFlowStateCollection
from ....models.chat.chat import Chat
from ....models.utils.types.identifier import StrObjectId
from .chat_service import ChatAssetService

#: Pedir todo el historial (para lo que de verdad lo necesita: replay, citas viejas, auditoría).
ALL_MESSAGES: Literal["all"] = "all"
MessagesToLoad = Union[None, int, Literal["all"]]


class ChatLoader:
    """Arma un `Chat` desde sus cuatro colecciones. Depende sólo de cómo leer cada parte, así lo
    usan igual api-chatty (con `ChatAssetService`) y los microservicios (con `AssetsCollections`)."""

    def __init__(
        self,
        get_chat: Callable[[StrObjectId], Awaitable[Chat]],
        messages: ChatMessagesCollection,
        clients: ClientCollection,
        flow_states: ChatFlowStateCollection,
    ):
        self._get_chat = get_chat
        self.messages = messages
        self.clients = clients
        self.flow_states = flow_states

    @classmethod
    def for_service(cls, chats: ChatAssetService) -> "ChatLoader":
        return cls(chats.get_by_id, chats.messages, chats.clients, chats.flow_states)

    async def load(
        self,
        chat_id: StrObjectId,
        *,
        messages: MessagesToLoad = None,
        person: bool = False,
        flow_states: bool = False,
    ) -> Chat:
        """El chat con lo que se pida.

        `messages`: `None` (no cargar), un número (los últimos bloques hasta juntar esa cantidad
        de mensajes visibles; deja `total_visible_messages` para la paginación) o `ALL_MESSAGES`.
        """
        return await self.fill(await self._get_chat(chat_id), messages=messages, person=person, flow_states=flow_states)

    async def fill(
        self,
        chat: Chat,
        *,
        messages: MessagesToLoad = None,
        person: bool = False,
        flow_states: bool = False,
    ) -> Chat:
        """Completa un chat ya leído con lo que se pida y todavía no tenga cargado."""
        if messages is not None and not chat.messages_loaded:
            await self._fill_messages(chat, messages)
        if person and not chat.person_loaded:
            chat.load_person(await self.clients.get_by_id(chat.client_id))
        if flow_states and not chat.flow_states_loaded:
            chat.load_flow_states(await self.flow_states.list_for_chat(chat.id))
        return chat

    async def _fill_messages(self, chat: Chat, messages: Union[int, Literal["all"]]) -> None:
        if messages == ALL_MESSAGES:
            chat.load_messages(await self.messages.all_messages(chat.id))
            return
        window = await self.messages.last_window(chat.id, visible=messages)
        chat.load_messages(window.messages)
        chat.set_total_visible_messages(window.total_visible)


class LegacyChatShape:
    """La forma de chat que leían todos antes del rediseño, armada desde el chat cargado."""

    #: Lo que era de `client` y pasó a la raíz del chat.
    MOVED_TO_ROOT = ("tags", "products", "sales", "contact_points", "highlights", "lead_quality")

    @classmethod
    def client(cls, chat: Chat) -> Dict[str, Any]:
        """El `client` de antes: la persona completa más lo que subió a la raíz.

        Las claves son un superconjunto de las de antes: `_id` e `id`, `DNI` y `document_id`
        (la web lee `DNI` con `document_id` de respaldo; la app lee `document_id`).
        """
        person = cls._person_dict(chat)
        for field in cls.MOVED_TO_ROOT:
            value = getattr(chat, field)
            person[field] = [cls._json(v) for v in value] if isinstance(value, list) else getattr(value, "value", value)
        person["DNI"] = person.get("document_id")
        person["business_area"] = None
        return person

    @classmethod
    def apply(cls, dump: Dict[str, Any], chat: Chat) -> Dict[str, Any]:
        """Lleva un dump del chat nuevo a la forma vieja (endpoints que no cambian de contrato)."""
        for field in cls.MOVED_TO_ROOT:
            dump.pop(field, None)
        dump.pop("client_id", None)
        dump.pop("flow_ids", None)
        dump["client"] = cls.client(chat)
        if chat.flow_states_loaded:
            dump["flow_states"] = [state.legacy_dict() for state in chat.flow_states]
        return dump

    @staticmethod
    def _person_dict(chat: Chat) -> Dict[str, Any]:
        person = chat.person
        data = BaseModel.model_dump(person, by_alias=True, mode="json")
        data["id"] = person.id
        return data

    @staticmethod
    def _json(value: Any) -> Any:
        """Como lo serializaba pydantic dentro del dump del chat: por alias y en JSON."""
        if isinstance(value, BaseModel):
            return BaseModel.model_dump(value, by_alias=True, mode="json")
        return value
