"""Los eventos de la capa de atribución inferida.

Se emiten SÓLO cuando hay algo que decir: cuando el texto coincide con una plantilla
conocida, cuando el recibo de Meta aporta y cuando una persona decide. El movimiento del
touchpoint NO tiene evento propio: es un cambio de estado real, así que viaja en el
`contact_point.updated` que ya se emite, con su `update_reason`. El caso aburrido —chat orgánico donde Meta dice que no y
nunca tuvimos una opinión— no se emite: es el residuo, y se calcula restando los chats
orgánicos de `mv_contact_points`.

Estos payloads NO extienden `CustomerEventData` a propósito. Esa base exige el WABA, el
phone_number_id y los snapshots de empresa y agente, que el factory arma leyendo el chat
con todos sus assets — una lectura extra por cada chat orgánico que matchee una plantilla,
en el camino caliente del webhook. Acá alcanza con el chat y el touchpoint.
"""
from enum import StrEnum
from typing import ClassVar, List, Optional

from pydantic import BaseModel, Field, field_validator

from ....utils.types.identifier import StrObjectId
from ..base import Event, EventData
from ..event_types import EventType


class InferredSuggestionState(StrEnum):
    """Por qué el chat terminó con sugerencia o sin ella.

    Los cuatro estados que no son `suggested` son el diagnóstico del cuello de botella:
    dicen si falta evidencia, si el texto quedó excluido por genérico, o si los anuncios
    vinculados dejaron de tener actividad."""
    SUGGESTED = "suggested"
    TEMPLATE_LEARNING = "template_learning"
    TEMPLATE_EXCLUDED = "template_excluded"
    CANDIDATES_STALE = "candidates_stale"


class InferredVerdict(StrEnum):
    """Lo que dijo el recibo de Meta sobre el origen de la conversación.

    `UNATTRIBUTED` significa «no pude rastrearlo», NO «no fue un anuncio»: la asimetría
    importa al leer la precisión, porque un `confirmed` valida la sugerencia y un
    `unattributed` no la refuta."""
    CONFIRMED = "confirmed"
    UNATTRIBUTED = "unattributed"


class InferredAdCandidateData(BaseModel):
    """Un candidato tal como se lo mostró a la persona, con su peso congelado."""
    source_id: StrObjectId
    ad_id: Optional[str] = Field(default=None)
    weight: float
    n: int


class InferredAdEventData(EventData):
    """Lo mínimo común: el chat y el touchpoint sobre los que se habla.

    `chat_id` llega a Redshift como columna propia (la ingesta lo lee de `data.chat_id`),
    así que los joins con chats y ventas funcionan sin tocar la tabla."""
    chat_id: StrObjectId
    contact_point_id: StrObjectId
    company_id: Optional[StrObjectId] = Field(default=None)
    account_id: Optional[StrObjectId] = Field(
        default=None, description="The WhatsApp account of the chat: the learning pool is per (company, account, text)"
    )

    @property
    def message_group_id(self) -> str:
        return f"chat-{self.chat_id}"


class InferredAdEvaluatedData(InferredAdEventData):
    state: InferredSuggestionState
    template_hash: str
    candidates: List[InferredAdCandidateData] = Field(default_factory=list)
    top_weight: Optional[float] = Field(default=None)
    n_candidates: int = Field(default=0)
    window_days: Optional[int] = Field(default=None)


class InferredAdVerdictData(InferredAdEventData):
    verdict: InferredVerdict
    had_suggestion: bool
    template_hash: Optional[str] = Field(default=None)
    top_weight: Optional[float] = Field(default=None)
    conversation_id: Optional[str] = Field(default=None)
    latency_seconds: Optional[int] = Field(
        default=None, description="Del alta del chat al recibo; dimensiona el TTL de la bandera"
    )
    blocked_by_invariant: bool = Field(
        default=False,
        description="Meta confirmó pero el touchpoint ya estaba atribuido y no se tocó: la métrica de riesgo",
    )


class InferredAdDecidedData(InferredAdEventData):
    action: str = Field(description="confirmed_ad | unknown_ad | rejected")
    chosen_source_id: Optional[StrObjectId] = Field(default=None)
    chose_top: Optional[bool] = Field(default=None)
    chosen_rank: Optional[int] = Field(default=None)
    chosen_weight: Optional[float] = Field(default=None)
    template_hash: Optional[str] = Field(default=None)
    seconds_since_suggestion: Optional[int] = Field(default=None)
    meta_backing_at_decision: Optional[str] = Field(
        default=None,
        description="El respaldo de Meta cuando la persona decidió: mide cuándo Meta se equivocó o no mandó nada",
    )
    decided_by: Optional[StrObjectId] = Field(default=None)


class InferredAdTemplateData(EventData):
    """Sobre la plantilla, no sobre un chat: es estado de la libreta de la empresa."""
    template_hash: str
    company_id: Optional[StrObjectId] = Field(default=None)
    account_id: Optional[StrObjectId] = Field(
        default=None, description="The account whose learning pool this template belongs to: the same text is a different template on each number"
    )
    linked_ads: int = Field(default=0)
    distinct_waids: Optional[int] = Field(default=None)
    orphan_share: Optional[float] = Field(default=None)
    reason: Optional[str] = Field(default=None, description="Por qué quedó excluida")

    @property
    def message_group_id(self) -> str:
        return f"template-{self.template_hash}"


def _validador_de_tipo(tipos: set):
    @field_validator("type")
    def validar(cls, value):
        if value not in tipos:
            raise ValueError(
                f"Invalid event type: {value}. Must be one of: {', '.join(str(t) for t in tipos)}"
            )
        return value
    return validar


class InferredAdEvaluatedEvent(Event):
    data: InferredAdEvaluatedData
    VALID_TYPES: ClassVar[set] = {EventType.INFERRED_AD_EVALUATED}
    _v = _validador_de_tipo(VALID_TYPES)


class InferredAdVerdictEvent(Event):
    data: InferredAdVerdictData
    VALID_TYPES: ClassVar[set] = {EventType.INFERRED_AD_VERDICT}
    _v = _validador_de_tipo(VALID_TYPES)


class InferredAdDecidedEvent(Event):
    data: InferredAdDecidedData
    VALID_TYPES: ClassVar[set] = {EventType.INFERRED_AD_DECIDED}
    _v = _validador_de_tipo(VALID_TYPES)


class InferredAdTemplateEvent(Event):
    data: InferredAdTemplateData
    VALID_TYPES: ClassVar[set] = {
        EventType.INFERRED_AD_TEMPLATE_ACTIVATED,
        EventType.INFERRED_AD_TEMPLATE_EXCLUDED,
    }
    _v = _validador_de_tipo(VALID_TYPES)
