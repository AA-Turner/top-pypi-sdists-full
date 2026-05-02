from pydantic import Field, BaseModel
from typing import Optional
from enum import StrEnum
from letschatty.models.company.assets.ai_agents_v2.chatty_ai_mode import ChattyAIMode

class ProductsInfoLevel(StrEnum):
    """Products info level"""
    NAME = "name"
    DESCRIPTION = "description"
    ALL = "all"

class MessagingSettings(BaseModel):
    """Messaging settings for the company"""
    good_quality_score_definition: Optional[str] = Field(default=None, description="The definition of a good quality score")
    products_info_level : ProductsInfoLevel = Field(default=ProductsInfoLevel.NAME, description="Whether to include all products info in the prompt or just the name / description")
    ai_god_mode : Optional[ChattyAIMode] = Field(default=None, description="The mode of the ai god - null if not active")
    whatsapp_apb_mode : bool = Field(default=False, description="Whether to use the whatsapp apb mode")
    home_config : Optional[dict[str, bool]] = Field(default=None, description="The config for the home page")
    tagger_instructions: Optional[str] = Field(default=None, description="The instructions for the tagger when using the tagger ai agent")
    allow_unconfigured_additional_fields: bool = Field(
        default=False,
        description="If true, tagger may collect and persist non-configured additional_fields keys"
    )
    tagger_funnel_assignment_enabled: bool = Field(
        default=False,
        description="If true, tagger will attempt to assign funnels to chats that have no funnel yet"
    )
