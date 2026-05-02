from pydantic import Field, BaseModel, model_validator
from typing import Optional, List
from ...utils.types import StrObjectId
from letschatty.models.company.assets.ai_agents_v2.chatty_ai_agent_config_for_automation import ChattyAIConfigForAutomation
from letschatty.models.utils.definitions import Area
from letschatty.models.chat.quality_scoring import QualityScore

class Automation(BaseModel):
    tags: List[StrObjectId] = Field(default_factory=list)
    products: List[StrObjectId] = Field(default_factory=list)
    flow: List[StrObjectId] = Field(default_factory=list)
    highlight_description: Optional[str] = Field(default=None)
    quality_score: Optional[QualityScore] = Field(default=None)
    chatty_ai_agent_config: Optional[ChattyAIConfigForAutomation] = Field(default=None)
    area: Optional[Area] = Field(default=None)
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
    # client_info: Optional[ClientInfo] = Field(default=None) me gustaría que levante el mail y/o otros atributos

    @model_validator(mode='after')
    def check_agent_id(self):
        if self.area == Area.WITH_AGENT and not self.agent_id:
            raise ValueError("Agent id is required when area is with agent")
        return self