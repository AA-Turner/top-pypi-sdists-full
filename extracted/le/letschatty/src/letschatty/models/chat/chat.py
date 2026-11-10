from __future__ import annotations
import bisect
from typing import ClassVar, Optional, Dict, Any, List, Tuple, TYPE_CHECKING
from datetime import datetime, timedelta
from pydantic import Field, ConfigDict, PrivateAttr, field_validator
from zoneinfo import ZoneInfo
from .chat_client_preview import ChatClientPreview
from .chat_summary import ChatSummary, SUMMARY_FIELDS
from .message_summary import MessageSummary, IncomingMessageSummary, OutgoingMessageSummary
from .quality_scoring import QualityScore
from .highlight import Highlight
from ..utils.types.serializer_type import SerializerType
from ..messages.chatty_messages import ChattyMessage
from ..utils.types.message_types import MessageSubtype, MessageType
from ..base_models.chatty_asset_model import CompanyAssetModel
from ..utils.types.identifier import StrObjectId
from ..utils.definitions import Area, AreaTolerante
from ..utils.custom_exceptions.custom_exceptions import MessagesNotLoaded, FlowStatesNotLoaded, PersonNotLoaded
from ..company.assets.chat_assets import AssignedAssetToChat, SaleAssignedToChat, ContactPointAssignedToChat
from .continuous_conversation import ContinuousConversation
from .scheduled_messages import ScheduledMessages
from .seguimiento import Seguimiento
from .motivo_en_chat import MotivoEnChat
from .seguimiento_estado import EstadoDelSeguimiento
from ..company.assets.ai_agents_v2.chatty_ai_agent_in_chat import ChattyAiAgentInChatStatus
from ..messages.chatty_messages.base.message_draft import MessageDraft
from .time_left import TimeLeft
from .reply_window import is_free_window_open
from ..company.conversation_topic import TopicTimelineEntry
from ..company.CRM.funnel import ActiveFunnel
import logging
logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .flow_link_state import FlowStateAssignedToChat
    from .client import Client

_UTC = ZoneInfo("UTC")


class Chat(CompanyAssetModel):
    """Una conversación y todo lo que muestra la bandeja: un documento de `chats` (~3 KB).

    Lo que NO guarda, y por qué:

    - **Los mensajes** viven en `chat_messages`, de a 50 por bloque. `messages` está vacío salvo
      que el cargador los pida, y leerlo sin cargarlos lanza `MessagesNotLoaded` en vez de
      devolver vacío en silencio. Lo que antes se calculaba recorriéndolos (último mensaje,
      último entrante, ventanas, si alguna vez respondimos) es un campo guardado: ver
      `ChatSummary`.
    - **Los estados de workflow** viven en `chat_flow_states`; el chat guarda sólo `flow_ids`
      para el filtro de la bandeja.
    - **La persona completa** vive en `clients`; el chat guarda `client_id` y la preview que
      muestra la bandeja (`client`).

    Los mensajes nuevos que agrega la lógica en memoria (las notas del sistema de
    `ChatService`) quedan en `pending_messages`, y el guardado los escribe en los bloques.
    """
    client_id: StrObjectId = Field(description="La persona del chat, en `clients`")
    client: ChatClientPreview = Field(description="Copia de lo que la bandeja muestra de la persona. La escribe `ClientCollection`")
    channel_id: str = Field(description="El número de la empresa por el que ocurre el chat: `whatsapp_<phone_number_id>`. Legacy: lo exige letschatty <= 0.5.x; el chat se resuelve por `account_id`")
    account_id: Optional[StrObjectId] = Field(default=None, description="The WhatsApp account (`whatsapp_accounts`) the chat belongs to. Everything sent in this chat goes out through it")
    bsuid: Optional[str] = Field(default=None, description="The person's BSUID in the portfolio of this chat's account: the only one this chat's number can message")
    legacy_duplicate_key: Optional[str] = Field(default=None, description="Set only on chats that duplicated another live chat of the same person and account before uniqueness was enforced (2026-10). Chats are never merged; this keeps them out of `uniq_live_chat_per_account`")
    agent_id: Optional[StrObjectId] = Field(default=None, description="The id of the agents that's handling the chat if assigned")
    area: AreaTolerante = Field(default=Area.WAITING_AGENT, description="Each Area represents a stage of the chat, it's an old naming that should eventually be renamed to status or StatusArea")
    is_read_status: bool = Field(default=False)
    starred: bool = Field(default=False)
    lead_quality: QualityScore = Field(default=QualityScore.NEUTRAL, description="Calidad del chat. Era `client.lead_quality`: es de la conversación (eventos `chat.quality_score.*`)")
    tags: List[AssignedAssetToChat] = Field(default_factory=list)
    products: List[AssignedAssetToChat] = Field(default_factory=list)
    sales: List[SaleAssignedToChat] = Field(default_factory=list, description="Preview de las ventas: id, productos y fecha de venta. La venta entera vive en `sales`")
    contact_points: List[ContactPointAssignedToChat] = Field(default_factory=list, description="Preview de los touchpoints: id y fuente. El touchpoint entero vive en `contact_points`")
    highlights: List[Highlight] = Field(default_factory=list)
    continuous_conversations: List[ContinuousConversation] = Field(default_factory=list)
    scheduled_messages: List[ScheduledMessages] = Field(default_factory=list)
    flow_ids: List[StrObjectId] = Field(default_factory=list, description="Ids de los workflows con estado en `chat_flow_states`. Sólo para el filtro de la bandeja; lo escribe `ChatFlowStateCollection`")
    chatty_ai_agent_in_chat_status: Optional[ChattyAiAgentInChatStatus] = Field(
        default=None, description="Present when an AI agent is assigned; human_intervention set when escalated"
    )
    suggested_messages: List[MessageDraft] = Field(default_factory=list)
    topics_timeline: List[TopicTimelineEntry] = Field(default_factory=list, description="Timeline of conversation topics throughout the conversation")
    active_funnel: Optional[ActiveFunnel] = Field(default=None, description="Current active funnel for this chat")

    # ── Resumen de los mensajes. Lo escribe sólo el escritor de mensajes (ver ChatSummary). ──
    last_message: Optional[MessageSummary] = Field(default=None)
    last_message_timestamp: Optional[datetime] = Field(default=None)
    last_incoming_message: Optional[IncomingMessageSummary] = Field(default=None)
    last_incoming_message_timestamp: Optional[datetime] = Field(default=None)
    last_outgoing_message: Optional[OutgoingMessageSummary] = Field(default=None)
    first_outgoing_message_at: Optional[datetime] = Field(default=None, description="Vacío = nunca salió un mensaje real")
    free_conversation_expire_date: Optional[datetime] = Field(default=None, description="24 h desde el último entrante. Vacío = ventana cerrada")
    free_template_window_expire_date: Optional[datetime] = Field(default=None, description="7 días desde el último entrante que llegó desde un anuncio. Vacío = cerrada")

    proximo_recordatorio_at: Optional[datetime] = Field(default=None, frozen=True, description="FROZEN A PROPOSITO: lo escribe SOLO el $set del recalculo, nunca un save del chat. Sin frozen, cualquier guardado de documento completo (`update` mergea {**actuales, **entrantes}) lo pisaria con el valor que tuviera en memoria ese flujo, que puede ser anterior al recalculo — el badge desapareceria sin que nadie toque un recordatorio. Vencimiento del recordatorio SIN RESOLVER mas cercano de este chat, o None si no hay ninguno. Espejo del minimo sobre la coleccion `recordatorios`, para que la bandeja pueda mostrar el badge, filtrar y ordenar sin un join contra otra coleccion. Es una FECHA y no un booleano a proposito: 'vencido' se evalua al momento de la query (`<= ahora`), asi que el que se mueve es el reloj y no el dato, y no hace falta ningun barrido que lo actualice.")
    seguimientos: List[Seguimiento] = Field(default_factory=list, description="Los seguimientos del chat, embebidos. LA LISTA ES LA VERDAD: los tres campos de abajo se recalculan desde ella en cada escritura del SeguimientosEditor (api-chatty) y nunca se incrementan a mano. Ver models/chat/seguimiento.py.")
    seguimientos_total: int = Field(default=0, frozen=True, description="FROZEN A PROPOSITO, por lo mismo que proximo_recordatorio_at: lo escribe SOLO el $set del recalculo. Cantidad de seguimientos no anulados.")
    seguimientos_consecutivos: int = Field(default=0, frozen=True, description="FROZEN A PROPOSITO. Seguimientos no anulados desde el ultimo mensaje del cliente; cualquier entrante lo vuelve a cero. `>= 1` es «le hice seguimiento y no respondio».")
    ultimo_seguimiento_at: Optional[datetime] = Field(default=None, frozen=True, description="FROZEN A PROPOSITO. `at` del ultimo seguimiento no anulado, o None. Es una FECHA y no un booleano para que «sin seguimiento hace N dias» lo evalue el reloj en la query.")
    motivo: Optional[MotivoEnChat] = Field(default=None, frozen=True, description="FROZEN A PROPOSITO, por lo mismo que proximo_recordatorio_at: lo escribe SOLO el $set de api-chatty (camino de atencion de la entrada), nunca un save del chat. El motivo de consulta aplicado en la ultima entrada del chat (chat nuevo o vuelta despues de dias_para_reclasificar), cuando y como se decidio. None = el chat nunca paso por el flujo de atencion. Ver models/chat/motivo_en_chat.py.")
    seguimiento_estado: Optional[EstadoDelSeguimiento] = Field(default=None, frozen=True, description="FROZEN A PROPOSITO, por lo mismo que motivo: lo escribe SOLO el $set de api-chatty (al arrancar los seguimientos, al terminar sin respuesta y al entrar un mensaje del cliente), nunca un save del chat. activa / en_seguimiento / sin_respuesta, desde cuando, y al caer la etapa del funnel. None = nunca paso por los seguimientos del flujo: se lee como activa. Ver models/chat/seguimiento_estado.py.")

    _messages: Optional[List[ChattyMessage]] = PrivateAttr(default=None)
    _pending_messages: List[ChattyMessage] = PrivateAttr(default_factory=list)
    _flow_states: Optional[List["FlowStateAssignedToChat"]] = PrivateAttr(default=None)
    _person: Optional["Client"] = PrivateAttr(default=None)
    _pending_person_fields: Dict[str, Any] = PrivateAttr(default_factory=dict)
    _total_visible_messages: Optional[int] = PrivateAttr(default=None)

    model_config = ConfigDict(extra="ignore")

    #: Fechas que tienen que llegar a Mongo como fecha y no como texto.
    database_datetime_fields: ClassVar[set[str]] = {
        "last_message_timestamp", "last_incoming_message_timestamp", "first_outgoing_message_at",
        "free_conversation_expire_date", "free_template_window_expire_date",
        "proximo_recordatorio_at", "ultimo_seguimiento_at",
    }

    #: Campos que el guardado entero del chat (`update`) NO escribe: cada uno tiene su escritor.
    #: Si los escribiera, un chat viejo en memoria revertiría lo que otro escritor puso.
    WRITER_OWNED_FIELDS: ClassVar[Tuple[str, ...]] = SUMMARY_FIELDS + (
        "client", "client_id", "flow_ids",
        "proximo_recordatorio_at", "seguimientos_total", "seguimientos_consecutivos", "ultimo_seguimiento_at", "motivo",
        "seguimiento_estado",
    )

    _ASSIGNED_ARRAYS: ClassVar[Tuple[str, ...]] = ("products", "tags", "sales", "contact_points")

    @field_validator(
        "last_message_timestamp", "last_incoming_message_timestamp", "first_outgoing_message_at",
        "free_conversation_expire_date", "free_template_window_expire_date",
        "proximo_recordatorio_at", "ultimo_seguimiento_at", mode="after",
    )
    @classmethod
    def _dates_in_utc(cls, value: Optional[datetime]) -> Optional[datetime]:
        """Mongo devuelve las fechas sin zona: se leen como UTC. Sin esto, restar una fecha
        leída de la base a «ahora» explota (la lección de `funnels-chat-funnel-integrity`)."""
        if value is None:
            return None
        return value.replace(tzinfo=_UTC) if value.tzinfo is None else value.astimezone(_UTC)

    # ── Mensajes: cargados a pedido ──

    @property
    def messages_loaded(self) -> bool:
        return self._messages is not None

    @property
    def messages(self) -> List[ChattyMessage]:
        """Los mensajes que cargó el cargador, en orden cronológico. Sin cargar, lanza."""
        if self._messages is None:
            raise MessagesNotLoaded(chat_id=self.id)
        return self._messages

    @messages.setter
    def messages(self, messages: List[ChattyMessage]) -> None:
        self.load_messages(messages)

    def load_messages(self, messages: List[ChattyMessage]) -> None:
        self._messages = sorted(messages, key=lambda m: m.created_at)

    @property
    def pending_messages(self) -> List[ChattyMessage]:
        """Mensajes agregados en memoria que todavía no se guardaron en `chat_messages`."""
        return list(self._pending_messages)

    def add_pending_message(self, message: ChattyMessage) -> None:
        self._pending_messages.append(message)
        if self._messages is not None:
            bisect.insort(self._messages, message)

    def mark_message_saved(self, message: ChattyMessage) -> None:
        """El mensaje ya está en `chat_messages`: deja de estar pendiente y, si hay mensajes
        cargados, queda en la lista (aunque no haya pasado por `add_pending_message`)."""
        self._pending_messages = [m for m in self._pending_messages if m.id != message.id]
        if self._messages is not None and all(m.id != message.id for m in self._messages):
            bisect.insort(self._messages, message)

    def take_pending_messages(self) -> List[ChattyMessage]:
        """Los mensajes pendientes, y vacía la lista. Lo llama el guardado."""
        pending, self._pending_messages = self._pending_messages, []
        return pending

    # ── Estados de workflow: cargados a pedido ──

    @property
    def flow_states_loaded(self) -> bool:
        return self._flow_states is not None

    @property
    def flow_states(self) -> List["FlowStateAssignedToChat"]:
        if self._flow_states is None:
            raise FlowStatesNotLoaded(chat_id=self.id)
        return self._flow_states

    @flow_states.setter
    def flow_states(self, states: List["FlowStateAssignedToChat"]) -> None:
        self.load_flow_states(states)

    def load_flow_states(self, states: List["FlowStateAssignedToChat"]) -> None:
        self._flow_states = list(states)

    # ── La persona completa: cargada a pedido ──

    @property
    def person_loaded(self) -> bool:
        return self._person is not None

    @property
    def person(self) -> "Client":
        """La persona completa de `clients` (email, documento, formularios). Sin cargar, lanza:
        un evento que la necesita no puede salir con esos campos en null sin que nadie se entere."""
        if self._person is None:
            raise PersonNotLoaded(chat_id=self.id)
        return self._person

    def load_person(self, person: "Client") -> None:
        if person.id != self.client_id:
            raise ValueError(f"La persona {person.id} no es la del chat {self.id} ({self.client_id})")
        self._person = person

    def attach_person(self, person: "Client") -> None:
        """Apunta el chat a esta persona: la que ya estaba en `clients` o la recién dada de alta."""
        self.client_id = person.id
        self.client = person.preview()
        self._person = person

    def set_person_field(self, name: str, value: Any) -> None:
        """Cambia un dato de la persona en memoria y lo deja pendiente para `clients`.

        Si el dato es de la preview, la preview del chat se actualiza también (el guardado hace
        el fan-out a los otros chats de la persona).
        """
        setattr(self.person, name, value)
        self._pending_person_fields[name] = value
        if name in ChatClientPreview.FIELDS:
            setattr(self.client, name, value)

    def set_person_form_value(self, key: str, value: Any) -> None:
        """Un valor de `lead_form_data`, sin pisar las otras claves (en `clients`, `$set` por clave)."""
        self.person.lead_form_data[key] = value
        self._pending_person_fields[f"lead_form_data.{key}"] = value

    def take_pending_person_fields(self) -> Dict[str, Any]:
        """Los cambios de la persona pendientes, y vacía la lista. Lo llama el guardado."""
        pending, self._pending_person_fields = self._pending_person_fields, {}
        return pending

    @property
    def total_visible_messages(self) -> Optional[int]:
        """Cuántos mensajes visibles tiene el chat entero, cuando se cargó una ventana (paginación)."""
        return self._total_visible_messages

    def set_total_visible_messages(self, total: int) -> None:
        self._total_visible_messages = total

    # ── Resumen ──

    @property
    def summary(self) -> ChatSummary:
        return ChatSummary(**{field: getattr(self, field) for field in SUMMARY_FIELDS})

    def apply_summary(self, summary: ChatSummary) -> None:
        """Deja en memoria el resumen que el escritor guardó."""
        for field in SUMMARY_FIELDS:
            object.__setattr__(self, field, getattr(summary, field))

    @property
    def has_active_cc(self) -> bool:
        """
        Check if a chat has an active continuous conversation.
        """
        return any(cc.active for cc in self.continuous_conversations)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Chat):
            return False
        return self.id == other.id

    def __ne__(self, other: Any) -> bool:
        if not isinstance(other, Chat):
            return False
        return self.id != other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def _ordering_timestamp(self) -> datetime:
        return self.last_message_timestamp or self.created_at

    def __gt__(self, other: Any) -> bool:
        """Compare two chats by the last message timestamp; without one, by created_at"""
        if not isinstance(other, Chat):
            return False
        return self._ordering_timestamp() > other._ordering_timestamp()

    def __lt__(self, other: Any) -> bool:
        """Compare two chats by the last message timestamp; without one, by created_at"""
        if not isinstance(other, Chat):
            return False
        return self._ordering_timestamp() < other._ordering_timestamp()

    @property
    def identifier(self) -> StrObjectId:
        return self.id

    # ── Ventanas de Meta ──

    @staticmethod
    def _seconds_until(expire_date: Optional[datetime]) -> float:
        """Segundos hasta el vencimiento. Sin fecha, la ventana está cerrada (como hoy: «hace 1 h»)."""
        now = datetime.now(tz=_UTC)
        if expire_date is None:
            return -3600.0
        expire_date = expire_date.replace(tzinfo=_UTC) if expire_date.tzinfo is None else expire_date
        return (expire_date - now).total_seconds()

    @property
    def recipient_identity(self) -> Optional[str]:
        """Who this chat's number writes to: the phone if there is one, else the person's BSUID
        in the portfolio of this chat's account (`bsuid`). The legacy scalar `client.user_id` is
        the default account's BSUID, so it is only the last resort (pre-migration chats)."""
        return self.client.waid or self.bsuid or self.client.user_id

    @property
    def is_free_conversation_active(self) -> bool:
        """Check if the free conversation is active (the rule is `models/chat/reply_window.py`, ENG-340)"""
        return is_free_window_open(self.free_conversation_expire_date, datetime.now(tz=_UTC))

    @property
    def time_left_for_free_conversation(self) -> float:
        """Get the time left for the free conversation in seconds"""
        return self._seconds_until(self.free_conversation_expire_date)

    @property
    def is_free_template_window_active(self) -> bool:
        """Check if the free template window is active"""
        return self._seconds_until(self.free_template_window_expire_date) > 0

    @property
    def time_left_for_free_template_window(self) -> float:
        """Get the time left for the free template window in seconds"""
        return self._seconds_until(self.free_template_window_expire_date)

    @property
    def time_left(self) -> TimeLeft:
        """Get the time left for the free conversation and the free template window"""
        return TimeLeft.get_time_left(
            time_left_for_free_conversation_seconds=self.time_left_for_free_conversation,
            time_left_for_free_template_window_seconds=self.time_left_for_free_template_window
        )

    def is_chat_assigned_to_agent(self, agent_id: StrObjectId) -> bool:
        """Check if the chat is assigned to the AI agent"""
        return self.area == Area.WITH_AGENT and self.agent_id == agent_id

    def is_chat_assigned_to_another_agent(self, agent_id: StrObjectId) -> bool:
        """Check if the chat is assigned to another agent"""
        return self.area == Area.WITH_AGENT and self.agent_id != agent_id

    @property
    def chat_has_ai_agent_assigned(self) -> bool:
        """Check if the chat has an AI agent assigned"""
        return self.chatty_ai_agent_in_chat_status is not None

    # ── Lo que sale del resumen guardado ──

    @property
    def is_first_message(self) -> bool:
        """Si todavía nunca salió un mensaje real nuestro (todos los mensajes reales son del cliente)."""
        return self.first_outgoing_message_at is None

    @property
    def last_outgoing_message_timestamp(self) -> Optional[datetime]:
        return self.last_outgoing_message.created_at if self.last_outgoing_message else None

    # ── Lo que necesita el historial: lanza si no se cargó ──

    @property
    def sent_fast_answers_ids(self) -> List[StrObjectId]:
        """Load fast answers that have been sent in this chat"""
        return [m.context.response_id for m in self.messages if m.subtype == MessageSubtype.CHATTY_FAST_ANSWER]

    @property
    def sent_templates(self) -> List[ChattyMessage]:
        """Load templates names that have been sent in this chat"""
        return [m for m in self.messages if m.is_template_message]

    @property
    def get_sent_templates_names(self) -> List[str]:
        """Load templates names that have been sent in this chat"""
        return [template.context.template_name for template in self.sent_templates]  # type: ignore

    @property
    def real_messages(self) -> List[ChattyMessage]:
        """Get the real messages in the chat"""
        return [m for m in self.messages if m.type != MessageType.CENTRAL]

    @property
    def get_last_referal_incoming_message(self) -> Optional[ChattyMessage]:
        """Get the last referal incoming message in the chat (no historial importado)."""
        for message in reversed(self.messages):
            if message.is_incoming_message and not message.referral.is_default and message.subtype != MessageSubtype.COEXISTENCE_IMPORT:
                return message
        return None

    @property
    def get_last_template_message_sent(self) -> Optional[ChattyMessage]:
        """Get the last template message sent in the chat"""
        for message in reversed(self.messages):
            if not message.is_incoming_message and message.context.template_name:
                return message
        return None

    def was_template_sent_to_chat(self, template_name: str) -> bool:
        """Check if a template was sent to the chat"""
        return template_name in self.get_sent_templates_names

    def get_templates_sent_to_chat(self) -> List[ChattyMessage]:
        """Get all templates sent to the chat"""
        return self.sent_templates

    def get_message_by_id(self, message_id: str) -> Optional[ChattyMessage]:
        """Get a message by its id"""
        for message in self.messages:
            if message.id == message_id:
                return message
        return None

    def get_time_delta_between_an_incoming_message_and_its_previous(self, message: ChattyMessage) -> Optional[timedelta]:
        """Get the time delta between an incoming message and its previous message"""
        for m in reversed(self.messages):
            if m.is_incoming_message and m.id != message.id:
                return message.created_at - m.created_at
        return None

    # ── Conversación ──

    @property
    def active_topics(self) -> List[str]:
        """Get currently active conversation topics (last timeline entry)."""
        if not self.topics_timeline:
            return []
        return self.topics_timeline[-1].topics

    @property
    def is_starred(self) -> bool:
        """Check if the chat is starred"""
        return self.starred

    @property
    def bought_product_ids(self) -> List[StrObjectId]:
        """Los productos que compró el cliente: todos los de cada venta, sin las ventas sin productos."""
        return [product_id for sale in self.sales for product_id in sale.productos_vendidos()]

    @property
    def assigned_product_ids(self) -> List[StrObjectId]:
        """Get all product ids in the chat"""
        return [product.asset_id for product in self.products]

    @property
    def assigned_tag_ids(self) -> List[StrObjectId]:
        """Get all tag ids in the chat"""
        return [tag.asset_id for tag in self.tags]

    @property
    def assigned_source_ids(self) -> List[StrObjectId]:
        """Get all source ids in the chat"""
        return [contact_point.source_id for contact_point in self.contact_points]

    def get_all_tags(self) -> List[AssignedAssetToChat]:
        return self.tags

    def get_all_highlights(self) -> List[Highlight]:
        return self.highlights

    def get_all_contact_points(self) -> List[ContactPointAssignedToChat]:
        return self.contact_points

    def get_area(self) -> Area:
        """Get the area of the chat"""
        return self.area

    def is_read(self) -> bool:
        """Check if the chat is read"""
        return self.is_read_status

    def get_agent_id(self) -> Optional[StrObjectId]:
        """Get the agent id of the chat"""
        return self.agent_id

    # ── Serialización ──

    def model_dump_json(self, *args, **kwargs) -> Dict[str, Any]:
        dump = super().model_dump_json(*args, **kwargs)
        serializer = kwargs.get('serializer', SerializerType.API)
        if serializer == SerializerType.DATABASE:
            # El resumen, con las fechas como fecha y las claves siempre presentes.
            dump.update(self.summary.to_document())
            # Los arrays de assets: sin re-dumpear cada elemento, `assigned_at` llega a Mongo
            # como texto y los filtros por fecha de la bandeja no lo ven.
            for name in self._ASSIGNED_ARRAYS:
                dump[name] = self.database_array(name)
            dump["seguimientos"] = [s.model_dump_json(serializer=SerializerType.DATABASE) for s in self.seguimientos]
            # El motivo: la fecha como fecha, y un None NO se escribe (lo pone el $set de api-chatty).
            if self.motivo is None:
                dump.pop("motivo", None)
            else:
                dump["motivo"] = self.motivo.model_dump()
            # El estado del seguimiento: igual que el motivo (fecha como fecha, un None no se escribe).
            if self.seguimiento_estado is None:
                dump.pop("seguimiento_estado", None)
            else:
                dump["seguimiento_estado"] = self.seguimiento_estado.model_dump()
            dump["client"] = self.client.to_document()
            # Never write a null account: a full save must not erase what the migration set.
            for name in ("account_id", "bsuid", "legacy_duplicate_key"):
                if getattr(self, name) is None:
                    dump.pop(name, None)
        return dump

    def database_array(self, name: str) -> List[Dict[str, Any]]:
        """Un array de assets (`tags`, `contact_points`...) como va a Mongo en un `$set`: cada
        elemento con su serializador de base, así `assigned_at` queda como fecha y no como texto."""
        if name not in self._ASSIGNED_ARRAYS:
            raise ValueError(f"{name} no es un array de assets del chat")
        return [e.model_dump_json(serializer=SerializerType.DATABASE) for e in getattr(self, name)]

    def to_update_document(self) -> Dict[str, Any]:
        """El documento para el guardado entero (`update`): sin `_id` ni los campos con dueño."""
        document = self.model_dump_json(serializer=SerializerType.DATABASE)
        document.pop("_id", None)
        for field in self.WRITER_OWNED_FIELDS:
            document.pop(field, None)
        return document
