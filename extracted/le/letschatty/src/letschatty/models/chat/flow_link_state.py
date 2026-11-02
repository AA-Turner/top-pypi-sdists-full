"""El estado de un workflow asignado a un chat: un documento de `chat_flow_states`.

Antes era un elemento de `chats.flow_states[]`. Dos cambios de fondo:

- **`flow_id` es el campo real.** Antes se llamaba `asset_id` con alias `flow_id`, y la mitad del
  código escribía una clave y la mitad la otra: el filtro de workflows de la bandeja consultaba
  `flow_id` y Mongo guardaba `asset_id`, así que devolvía cero. Al leer se acepta cualquiera de
  las dos; se guarda siempre `flow_id`. `asset_id` queda como propiedad para quien todavía lo lee.
- **El disparo por cambio es una marca explícita.** Antes copilot comparaba `chats.updated_at`
  con `last_call`. Ahora cada escritura de algo que una condición puede leer pone
  `next_call = ahora` en los estados `chat_update` y `first_of` del chat. Un estado que espera
  un cambio queda con `next_call` vacío (dormido): el scheduler sólo toma `next_call <= ahora`.
"""
from __future__ import annotations
from datetime import datetime
from enum import StrEnum
from typing import Optional, Self, Dict, Any, Iterable, List, TYPE_CHECKING
import logging

from bson import ObjectId
from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator
from zoneinfo import ZoneInfo

from letschatty.models.utils.types.identifier import StrObjectId
from letschatty.models.utils.types.serializer_type import SerializerType
from letschatty.models.copilot.links import LinkItem
from letschatty.models.company.assets.flow import FlowPreview
from letschatty.models.company.assets.chat_assets import ChatAssetType

logger = logging.getLogger("FlowStateAssignedToChat")

if TYPE_CHECKING:
    from letschatty.models.execution.execution import ExecutionContext

_UTC = ZoneInfo("UTC")

#: Campos de fecha del estado que van a Mongo como fecha.
_DATETIME_FIELDS = ("assigned_at", "next_call", "last_call")


class ExecutionResult(StrEnum):
    EXECUTED = "executed"
    FAILED = "failed"
    POSTPONED_FOR_LATER = "postponed_for_later"
    NOT_EXECUTED = "not_executed"


class StateTrigger(StrEnum):
    NEXT_CALL = "next_call"
    CHAT_UPDATE = "chat_update"
    FIRST_OF_NEXT_CALL_OR_CHAT_UPDATE = "first_of_next_call_or_chat_update"

    @property
    def wakes_on_chat_change(self) -> bool:
        """Si un cambio en el chat lo despierta. Los `next_call` no: adelantarlos haría salir
        mensajes demorados antes de tiempo y pisaría el timer de los seguimientos de IA."""
        return self in (StateTrigger.CHAT_UPDATE, StateTrigger.FIRST_OF_NEXT_CALL_OR_CHAT_UPDATE)


#: Los triggers que despierta la marca de cambio del chat.
TRIGGERS_WOKEN_BY_CHAT_CHANGE = tuple(t.value for t in StateTrigger if t.wakes_on_chat_change)


def _as_utc(value: Optional[datetime]) -> Optional[datetime]:
    if value is None:
        return None
    return value.replace(tzinfo=_UTC) if value.tzinfo is None else value.astimezone(_UTC)


class FlowStateAssignedToChat(BaseModel):
    id: StrObjectId = Field(default_factory=lambda: str(ObjectId()), validation_alias=AliasChoices("id", "_id"), description="El id del estado. Es el mismo que tenía en `chats.flow_states`: lo usan el evento `chat.workflow.assigned` y `POST /flows/run_state`")
    company_id: StrObjectId
    chat_id: StrObjectId
    flow_id: StrObjectId = Field(validation_alias=AliasChoices("flow_id", "asset_id"))
    asset_type: ChatAssetType = Field(default=ChatAssetType.WORKFLOW)
    assigned_at: datetime = Field(default_factory=lambda: datetime.now(_UTC))
    assigned_by: StrObjectId
    next_call: Optional[datetime] = Field(default_factory=lambda: datetime.now(_UTC), description="Cuándo tiene que correr. Vacío = dormido hasta que cambie el chat")
    last_call: Optional[datetime] = Field(default=None)
    description: str = Field(default="", description="Usefull for AI follow ups where we wanta a specific prompt for the follow up")
    executed_step: int = Field(default=0)
    repeat_step: int = Field(default=0)
    trigger: StateTrigger = Field(default=StateTrigger.NEXT_CALL)
    should_execute: bool = Field(default=True)
    execution_result: ExecutionResult = Field(default=ExecutionResult.NOT_EXECUTED)
    execution_time_seconds: Optional[float] = Field(default=None)
    error_message: Optional[str] = Field(default=None)
    last_incoming_message_id: Optional[str] = Field(default=None)
    is_smart_follow_up: bool = Field(default=False)
    total_followups_sent: int = Field(default=0)
    consecutive_count: int = Field(default=0)
    execution_attempts: int = Field(default=0)
    max_total_follow_ups_reached: bool = Field(default=False, description="If true, the total follow ups sent reached the maximum limit. This won't change once its set to true.")
    max_consecutive_follow_ups_reached: bool = Field(default=False, description="If true, the consecutive follow ups reached the maximum limit. This resets each time the user sends a message.")

    model_config = ConfigDict(arbitrary_types_allowed=True, validate_by_name=True, validate_by_alias=True)

    @field_validator(*_DATETIME_FIELDS, mode="after")
    @classmethod
    def _utc(cls, value: Optional[datetime]) -> Optional[datetime]:
        return _as_utc(value)

    @property
    def asset_id(self) -> StrObjectId:
        """El nombre viejo de `flow_id`. La web y la app siguen leyendo `asset_id`."""
        return self.flow_id

    def is_due(self, now: Optional[datetime] = None) -> bool:
        """Si el scheduler tiene que correrlo. Vale para los tres triggers: la marca de cambio ya
        dejó `next_call` en «ahora» a los que despierta un cambio, y uno dormido no tiene fecha."""
        if self.next_call is None:
            return False
        return self.next_call <= (now or datetime.now(_UTC))

    def sleep_until_chat_changes(self, now: Optional[datetime] = None) -> None:
        """Lo deja dormido hasta que cambie el chat: trigger `chat_update` y sin fecha. Lo despierta
        la marca de cambio (`ChatFlowStateCollection.mark_chat_changed`), no el reloj."""
        self.trigger = StateTrigger.CHAT_UPDATE
        self.next_call = None
        self.last_call = now or datetime.now(_UTC)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, FlowStateAssignedToChat):
            return False
        return self.flow_id == other.flow_id and self.chat_id == other.chat_id

    def __hash__(self) -> int:
        return hash((self.flow_id, self.chat_id))

    # ── Mongo ──

    def to_document(self) -> Dict[str, Any]:
        """El documento de `chat_flow_states`: `_id` = id del estado, fechas como fecha."""
        document = self.model_dump(mode="json", exclude={"id"})
        document["_id"] = ObjectId(self.id)
        for field in _DATETIME_FIELDS:
            document[field] = getattr(self, field)
        return document

    @classmethod
    def from_document(cls, document: Dict[str, Any]) -> "FlowStateAssignedToChat":
        data = dict(document)
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return cls(**data)

    @classmethod
    def from_documents(cls, documents: Iterable[Dict[str, Any]], now: Optional[datetime] = None) -> List["FlowStateAssignedToChat"]:
        """Los estados de un chat, con `should_execute` calculado para este instante."""
        now = now or datetime.now(_UTC)
        states = []
        for document in documents:
            state = cls.from_document(document)
            state.should_execute = state.is_due(now)
            states.append(state)
        return states

    def legacy_dict(self) -> Dict[str, Any]:
        """La forma que tenía dentro de `chats.flow_states`, que siguen leyendo la web y la app."""
        data = self.model_dump(mode="json")
        data["asset_id"] = data.pop("flow_id")
        return data

    def model_dump_json(self, *args, **kwargs) -> Dict[str, Any]:
        """Compatibilidad con quienes pedían el dump como dict (`serializer=DATABASE` → fechas como fecha)."""
        serializer = kwargs.pop("serializer", SerializerType.API)
        if serializer == SerializerType.DATABASE:
            return self.to_document()
        return self.model_dump(mode="json")

    # ── Construcción ──

    @staticmethod
    def from_link(link: LinkItem, execution_context: ExecutionContext, description: str, last_incoming_message_id: Optional[str] = None, next_call: Optional[datetime] = None, is_smart_follow_up: bool = False, trigger: Optional[StateTrigger] = None) -> FlowStateAssignedToChat:
        kwargs: Dict[str, Any] = dict(
            flow_id=link.flow_id,
            chat_id=link.chat_id,
            company_id=link.company_id,
            asset_type=ChatAssetType.WORKFLOW,
            assigned_by=execution_context.executor.id,
            description=description,
            last_incoming_message_id=last_incoming_message_id,
            next_call=next_call if next_call else datetime.now(_UTC),
            is_smart_follow_up=is_smart_follow_up,
        )
        if trigger is not None:
            kwargs["trigger"] = trigger
        return FlowStateAssignedToChat(**kwargs)

    @classmethod
    def from_json(cls, json: dict) -> FlowStateAssignedToChat:
        if isinstance(json, FlowStateAssignedToChat):
            return json
        return cls.from_document(json)


class FullState(FlowStateAssignedToChat):
    title: str = Field(default="")
    description: str = Field(default="")

    @staticmethod
    def from_state(state: FlowStateAssignedToChat, flow_preview: FlowPreview) -> FullState:
        data = state.model_dump()
        data.update(title=flow_preview.title, description=flow_preview.description or "")
        return FullState(**data)
