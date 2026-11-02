from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field
from ..utils.types import StrObjectId
from .message_summary import MessageSummary
# Re-exportado: api-chatty lo importa desde acá.
from letschatty.services.messages_helpers import MessageTextOrCaptionOrPreview  # noqa: F401
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from .time_left import TimeLeft
from .seguimiento_estado import EstadoDelSeguimiento
from .scheduled_messages import ScheduledMessageStatus
from ..company.assets.tag import TagPreview
from typing import List, Optional
from .time_left import TimeLeft
from ...models.utils.definitions import Area, AreaTolerante
from ..utils.types.message_types import MessageType
import json
import logging
from enum import StrEnum

logger = logging.getLogger("ChatPreviewModel")

class ChattyAiAgentStatus(StrEnum):
    ASSIGNED = "assigned"
    ESCALATED = "escalated"


class ChattyAiAgentStatusPreview(BaseModel):
    """Compact AI-agent status returned in chat previews.

    Presence (not None) means an AI agent is assigned.
    ``status`` distinguishes plain assignment from escalation.
    ``ai_agent_id`` and ``name`` allow the UI to show the agent without extra lookups.
    ``escalation_reason`` is the raw ``human_intervention.reason`` token, so the UI
    can tell a genuine escalation (``control_trigger`` / ``something_went_wrong``)
    apart from a pending AI draft (``suggested_messages``) — both set
    ``status = ESCALATED``, but only the former is a problem. None when not escalated.
    """

    status: ChattyAiAgentStatus
    ai_agent_id: str
    name: Optional[str] = Field(default=None)
    escalation_reason: Optional[str] = Field(default=None)
    #: ``human_intervention.cintia_type`` — which kind of execution escalated, so a
    #: pending draft can be labelled "sugerencia de seguimiento" vs "de respuesta".
    #: None on chats escalated before the field existed; render the generic label.
    escalation_cintia_type: Optional[str] = Field(default=None)


class ClientPreview(BaseModel):
    name: str
    phone_number: str
    #: Alias de WhatsApp del contacto (`Client.username`) — display-only y mutable.
    #: NO es identidad: la identidad estable es el BSUID (`Client.user_id`), que no
    #: viaja en la preview. Es None en la enorme mayoría de los chats (sólo lo tienen
    #: los contactos que adoptaron username), así que el que lo consuma tiene que
    #: tolerar la ausencia y seguir mostrando `name`.
    username: Optional[str] = Field(default=None)

class AgentPreview(BaseModel):
    name: str
    email: Optional[str] = Field(default=None)
    id: StrObjectId
    photo_url: Optional[str] = Field(default=None)

class ChatPreview(BaseModel):
    chat_id: StrObjectId
    account_id: Optional[StrObjectId] = Field(default=None, description="The WhatsApp account of the chat (multi-account): the inbox shows its badge and filters by it")
    area_status : AreaTolerante
    agent : Optional[AgentPreview] = Field(default=None)
    client : ClientPreview
    last_message : Optional[MessageSummary] = Field(default=None, description="El resumen guardado en `chats.last_message`")
    is_read_status : bool
    free_conversation_expire_date : Optional[datetime] = Field(default=None, description="Vacío = ventana cerrada")
    free_template_window_expire_date : Optional[datetime] = Field(default=None, description="Vacío = ventana cerrada")
    starred : bool
    created_at : datetime
    scheduled_message : Optional[ScheduledMessageStatus] = Field(default=None)
    tags : Optional[List[TagPreview]] = Field(default=[])
    chatty_ai_agent_in_chat_status: Optional[ChattyAiAgentStatusPreview] = Field(default=None)
    proximo_recordatorio_at: Optional[datetime] = Field(default=None, description="Vencimiento del recordatorio sin resolver mas cercano del chat. El frontend compara contra su propio reloj para decidir si va badge y de que color: el backend no decide que es hoy, porque el huso que importa es el del agente.")
    seguimientos_total: int = Field(default=0)
    seguimientos_consecutivos: int = Field(default=0)
    ultimo_seguimiento_at: Optional[datetime] = Field(default=None)
    seguimiento_estado: Optional[EstadoDelSeguimiento] = Field(default=None, description="Espejo de Chat.seguimiento_estado para el chip y el filtro de la bandeja. None = activa.")
    @property
    def assigned_agent_id(self) -> Optional[StrObjectId]:
        if self.area_status != Area.WITH_AGENT:
            raise ValueError(f"Chat is not assigned to an agent: {self.chat_id} client: {self.client.name}")
        if self.agent is None:
            raise ValueError(f"Agent is not assigned to this chat: {self.chat_id} client: {self.client.name}")
        return self.agent.id

    def last_message_old_format(self) -> dict:
        """La forma que leen la web y la app: `{is_incoming, type, content, datetime, status}`."""
        if self.last_message is None:
            return {
                "is_incoming": False,
                "type": "text",
                "content": "No hay mensajes",
                "datetime": self.created_at.isoformat(),
                "status": None,
            }
        return self.last_message.old_format()

    @staticmethod
    def _closed_window_if_missing(expire_date: Optional[datetime]) -> datetime:
        """Las ventanas vacías se devuelven como hoy: vencidas hace una hora (la UI exige una fecha)."""
        if expire_date is None:
            return datetime.now(tz=ZoneInfo("UTC")) - timedelta(hours=1)
        return expire_date.replace(tzinfo=ZoneInfo("UTC")) if expire_date.tzinfo is None else expire_date

    def model_dump(self) -> dict:
        dump = json.loads(super().model_dump_json())
        dump["last_message"] = self.last_message_old_format()
        free_conversation = self._closed_window_if_missing(self.free_conversation_expire_date)
        free_template_window = self._closed_window_if_missing(self.free_template_window_expire_date)
        dump["free_conversation_expire_date"] = free_conversation.isoformat()
        dump["free_template_window_expire_date"] = free_template_window.isoformat()
        logger.debug(f"self.free_conversation_expire_date: {self.free_conversation_expire_date}")
        logger.debug(f"self.free_template_window_expire_date: {self.free_template_window_expire_date}")
        dump["time_left"] = TimeLeft.get_time_left(
            time_left_for_free_conversation_seconds=(free_conversation - datetime.now(tz=ZoneInfo("UTC"))).total_seconds(),
            time_left_for_free_template_window_seconds=(free_template_window - datetime.now(tz=ZoneInfo("UTC"))).total_seconds()
        ).model_dump()
        logger.debug(f"dump['time_left']: {dump['time_left']}")
        return dump

