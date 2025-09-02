from __future__ import annotations
from typing import List, TYPE_CHECKING, Optional
from datetime import datetime
from pydantic import BaseModel, Field, model_validator, computed_field

from letschatty.models.company.assets.ai_agents_v2.chatty_ai_agent_config_for_automation import ChattyAIConfigForAutomation
from ...utils.definitions import Area
from ...utils.types.identifier import StrObjectId
from zoneinfo import ZoneInfo
from enum import StrEnum
import logging

if TYPE_CHECKING:
    from .required_for_frontend_templates import RequiredTemplateParameter

logger = logging.getLogger("RecipientOfTemplateCampaign")

class TemplateOrigin(StrEnum):
    FROM_CHAT = "from_chat"
    FROM_CAMPAIGN = "from_campaign"
    FROM_WORKFLOW = "from_workflow"
    FROM_CONTINUOUS_CONVERSATION = "from_continuous_conversation"
    FROM_TEMPLATES_MANAGER = "from_templates_manager"
    FROM_SCHEDULED_MESSAGES = "from_scheduled_messages"


class FilledRecipientParameter(BaseModel):
    id: str
    text: str

    @classmethod
    def from_required_template_parameters_and_recipient_dict(cls, required_template_parameters: List[RequiredTemplateParameter], recipient_dict: dict) -> List[FilledRecipientParameter]:
        logger.debug(f"Required template parameters: {required_template_parameters}")
        logger.debug(f"Recipient dict: {recipient_dict}")
        try:
            return [FilledRecipientParameter(id=parameter.id, text=recipient_dict[parameter.id]) for parameter in required_template_parameters]
        except KeyError as e:
            logger.error(f"Error in campaign creation: Missing parameter: {e} in recipient with phone number: {recipient_dict['phone_number']}")
            raise ValueError(f"Error in campaign creation: Missing parameter: {e} in recipient with phone number: {recipient_dict['phone_number']}")

class FilledTemplateData(BaseModel):
    template_name: str
    fast_answer_id: Optional[StrObjectId] = None
    area: Optional[Area]
    assign_to_agent: Optional[StrObjectId] = Field(default=None)
    phone_number: str | None = None
    new_contact_name: str | None = None
    parameters: List[FilledRecipientParameter] = Field(default_factory=list)
    tags: List[StrObjectId] = Field(default_factory=list)
    products: List[StrObjectId] = Field(default_factory=list)
    flow: List[StrObjectId] = Field(default_factory=list)
    chatty_ai_agent_config: Optional[ChattyAIConfigForAutomation] = Field(default=None)
    description: str | None = None
    forced_send: bool = False
    lenguage: str | None = None
    campaign_name: str | None = None
    campaign_id: StrObjectId | None = None
    body: str | None = None
    origin : TemplateOrigin
    scheduled_at : Optional[datetime] = None
    scheduled_messages_id : Optional[StrObjectId] = None
    continuous_conversation_id : Optional[StrObjectId] = None

    @property
    def recipient_name(self) -> str:
        if self.new_contact_name:
            return self.new_contact_name
        return self.recipient_phone_number

    @property
    def recipient_phone_number(self) -> str:
        if not self.phone_number:
            raise ValueError("Template data does not have a phone number, can't be used as recipient")
        return self.phone_number

    @property
    def completed_body(self) -> str:
        if not self.body:
            raise ValueError("Body is empty")
        return self.body

    @model_validator(mode='before')
    def assign_to_agent_if_area_is_with_agent(cls, data: dict) -> dict:
        if not data.get("area") == Area.WITH_AGENT:
            data["assign_to_agent"] = None
        return data

    @model_validator(mode='after') #type: ignore
    def validate_template_data(self) -> dict:

        if self.area == Area.WITH_AGENT and not self.assign_to_agent:
            # TEMPORARY FIX FOR AGENT ASSIGNMENT: IF IT'S NOT SPECIFIED, ASSIGN TO THE AGENT EMAIL
            raise ValueError("Agent assignment must be specified for WITH AGENT area")

        if not self.phone_number:
            logger.warning("Phone number must be specified for single recipient")
            raise ValueError("Phone number must be specified for single recipient")

        self.phone_number = str(self.phone_number)

        if not self.new_contact_name:
            self.new_contact_name = self.phone_number

        return self #type: ignore

    @model_validator(mode='after')
    def validate_scheduled_at(self):
        if self.scheduled_at and self.scheduled_at < datetime.now(ZoneInfo("UTC")):
            raise ValueError("Scheduled at must be in the future")
        return self
