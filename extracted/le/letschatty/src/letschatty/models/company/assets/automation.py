from pydantic import Field, BaseModel, model_validator
from typing import Optional, List
from ...utils.types import StrObjectId
from letschatty.models.company.assets.ai_agents_v2.chatty_ai_agent_config_for_automation import ChattyAIConfigForAutomation
from letschatty.models.utils.definitions import Area, AreaOpcionalTolerante
from letschatty.models.chat.quality_scoring import QualityScore

class Automation(BaseModel):
    tags: List[StrObjectId] = Field(default_factory=list)
    products: List[StrObjectId] = Field(default_factory=list)
    flow: List[StrObjectId] = Field(default_factory=list)
    # Removal automations — asset IDs to REMOVE from the chat (mirror of tags/products/flow,
    # which add). Configuring the same id in both an add list and its remove list is
    # contradictory and unsupported. See docs/automation.md in api-chatty.
    tags_to_remove: List[StrObjectId] = Field(default_factory=list)
    products_to_remove: List[StrObjectId] = Field(default_factory=list)
    flows_to_remove: List[StrObjectId] = Field(default_factory=list)
    highlight_description: Optional[str] = Field(default=None)
    # Calidad del lead. Se escribe en `client.lead_quality` del chat (NO en
    # `client.quality_score`, que no existe en el documento).
    quality_score: Optional[QualityScore] = Field(default=None)
    # Desescalar: limpia `chatty_ai_agent_in_chat_status.human_intervention`, que es el
    # campo por el que se define un chat escalado. Booleano y no un enum porque la acción
    # no tiene parámetros: o se desescala o no se toca. No hay "escalar" acá a propósito
    # — escalar es una decisión de la IA con un motivo (HumanInterventionReason), no algo
    # que se configure en una automatización.
    deescalate: bool = Field(default=False)
    chatty_ai_agent_config: Optional[ChattyAIConfigForAutomation] = Field(default=None)
    area: AreaOpcionalTolerante = Field(default=None)
    agent_id: Optional[StrObjectId] = Field(default=None)
    chain_of_thought: Optional[str] = Field(default=None)
    # Funnel transition automations
    target_funnel_id: Optional[StrObjectId] = Field(
        default=None,
        description="Target funnel to move the chat to (for cross-funnel transitions)"
    )
    target_stage_id: Optional[StrObjectId] = Field(
        default=None,
        description="Target stage within the target funnel"
    )
    # Sacar del embudo: el inverso de target_funnel_id. No lleva id porque abandona el
    # embudo ACTIVO del chat, sea cual sea — igual que POST /{co}/chat/{id}/funnel/abandon.
    #
    # Si vienen los dos (mover a un embudo Y sacar del embudo), GANA EL MOVIMIENTO y el
    # abandono se saltea con un warning. El ejecutor de api-chatty es quien resuelve la
    # precedencia; acá no se valida ni se levanta excepción a propósito, porque un raise
    # tiraría abajo TODAS las acciones del chat por un par contradictorio.
    abandon_funnel: bool = Field(default=False)
    # client_info: Optional[ClientInfo] = Field(default=None) me gustaría que levante el mail y/o otros atributos

    @model_validator(mode='after')
    def check_agent_id(self):
        if self.area == Area.WITH_AGENT and not self.agent_id:
            raise ValueError("Agent id is required when area is with agent")
        return self