from letschatty.models.utils.types import StrObjectId
from letschatty.models.execution.execution import ExecutionContext
from pydantic import BaseModel, Field
from letschatty.models.utils.definitions import Area, AreaTolerante
from letschatty.models.chat.quality_scoring import QualityScore
from datetime import datetime, timedelta
import logging
from enum import StrEnum
from typing import Optional
logger = logging.getLogger("FilterParameters")

class ChattyAiAgentStatusFilterParam(StrEnum):
    ASSIGNED = "assigned"
    NOT_SET = "not_set"
    #: Genuine escalations only — EXCLUDES the SUGGESTED_* reasons below.
    ESCALATED = "escalated"
    #: Any chat holding an AI draft for human review (responder OR follow-up).
    #: A suggestion is normal AI flow, not a problem, so it is filterable apart
    #: from a real escalation.
    SUGGESTED = "suggested"
    #: A responder answered the client and the reply is awaiting review.
    SUGGESTED_RESPONSE = "suggested_response"
    #: A smart follow-up wants to reach out proactively on a silent chat.
    SUGGESTED_FOLLOW_UP = "suggested_follow_up"
    ALL = "all"

class FilterParameters(BaseModel):
    area_status: list[AreaTolerante] = Field(default=[])
    previews_per_page: int = Field(default=10, ge=1)
    order_desc: int = Field(default=1, ge=0, le=1)
    page_number: int = Field(default=1, ge=1)
    unread: int = Field(default=0, ge=0, le=1)
    starred: int = Field(default=0, ge=0, le=1)
    time_left_order: int = Field(default=0, ge=0, le=1)
    products: list[StrObjectId] = Field(default=[])
    sales_products: list[StrObjectId] = Field(default=[])
    tags: list[StrObjectId] = Field(default=[])
    search_like: str = Field(default="")
    agents: list[StrObjectId] = Field(default=[])
    #: Multi-account: only chats of these WhatsApp accounts. Empty = every account.
    accounts: list[StrObjectId] = Field(default=[])
    funnels: list[StrObjectId] = Field(default=[])
    funnel_stages: list[StrObjectId] = Field(default=[])
    time_since_last_message_hours: int = Field(default=0, ge=0)
    sources: list[StrObjectId] = Field(default=[])
    quality_score: list[QualityScore] = Field(default=[])
    search_in_chat: str = Field(default="")
    workflows: list[StrObjectId] = Field(default=[])
    last_message_date_range: Optional[tuple[datetime, datetime]] = Field(default=None)
    sales_date_range: Optional[tuple[datetime, datetime]] = Field(default=None)
    sources_date_range: Optional[tuple[datetime, datetime]] = Field(default=None)
    executor_user_id: StrObjectId
    chatty_ai_agent_status : ChattyAiAgentStatusFilterParam = Field(default=ChattyAiAgentStatusFilterParam.ALL)
    #: Sólo los chats de MIS pendientes, ordenados por vencimiento.
    #:
    #: Es un filtro y no un valor de `Area` a propósito: `Area` son las colas que el chat
    #: tiene guardadas, y esto es una vista que las cruza a todas. El precedente es
    #: `is_my_chats`, que la barra lateral muestra como un área más pero que acá también
    #: es una combinación de filtros.
    #:
    #: El conjunto NO sale del espejo `proximo_recordatorio_at` —que es del chat y no sabe
    #: de responsable ni de alcance— sino de la agenda, que ya aplica visibilidad. Así el
    #: área, la campana y la agenda no pueden diferir: es la misma fuente.
    solo_pendientes: int = Field(default=0, ge=0, le=1)
    #: «Le hice seguimiento y no respondió»: seguimientos_consecutivos >= 1.
    con_seguimiento_sin_respuesta: int = Field(default=0, ge=0, le=1)
    #: «Sin seguimiento hace N días»: ultimo_seguimiento_at anterior a hoy-N, O nunca. 0 = apagado.
    sin_seguimiento_hace_dias: int = Field(default=0, ge=0)
    #: «Lleva al menos N seguimientos»: seguimientos_total >= N. 0 = apagado.
    seguimientos_min: int = Field(default=0, ge=0)

    @property
    def is_my_chats(self) -> bool:
        return len(self.agents) == 1 and self.agents[0] == self.executor_user_id and len(self.area_status) == 0

    @property
    def is_direct(self) -> bool:
        if not self.search_in_chat and not self.search_like and not self.products and not self.sales_products and not self.tags and not self.funnels and not self.funnel_stages and not self.time_since_last_message_hours and not self.sources and not self.quality_score and not self.workflows and not self.last_message_date_range and not self.sales_date_range and not self.sources_date_range and not self.solo_pendientes and not self.con_seguimiento_sin_respuesta and not self.sin_seguimiento_hace_dias and not self.seguimientos_min and len(self.area_status) <= 1 and (len(self.agents) <= 1 or self.is_my_chats):
            return True
        return False

    @classmethod
    def from_query_params(cls, query_params: dict, execution_context: ExecutionContext) -> "FilterParameters":
        logger.debug(f"Query params: {query_params}")
        processed_params = {}
        processed_params["executor_user_id"] = execution_context.executor.id

        # Handle all list fields
        list_fields = {
            "products": StrObjectId,
            "sales_products": StrObjectId,
            "tags": StrObjectId,
            "agents": StrObjectId,
            "accounts": StrObjectId,
            "funnels": StrObjectId,
            "funnel_stages": StrObjectId,
            "area_status": Area,
            "sources": StrObjectId,
            "quality_score": QualityScore,
            "workflows": StrObjectId,
        }

        for field_name, field_type in list_fields.items():
            value = query_params.get(field_name)
            if not value:
                processed_params[field_name] = []
            elif "," in value:
                processed_params[field_name] = [field_type(item) for item in value.split(",")]
            else:
                processed_params[field_name] = [field_type(value)]

        # Process all other fields from query params
        for key, value in query_params.items():
            if key not in list_fields and value:  # Only process if value is not empty
                processed_params[key] = value
        logger.debug(f"Processed params: {processed_params}")
        return cls(**processed_params)