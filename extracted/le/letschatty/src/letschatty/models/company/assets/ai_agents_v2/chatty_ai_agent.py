from pydantic import Field, field_validator, BaseModel
from typing import List, Any, Optional, ClassVar

from letschatty.models.utils.definitions import Environment
from ....base_models import CompanyAssetModel
from ....base_models.chatty_asset_model import ChattyAssetPreview
from .chatty_ai_mode import ChattyAIMode
from ....utils.types.identifier import StrObjectId
from enum import StrEnum

class N8NWorkspaceAgentType(StrEnum):
    """AI agent type"""
    CALENDAR_SCHEDULER = "calendar_scheduler"
    TOKKO_BROKER = "tokko_broker"
    DEFAULT = "default"
    CUSTOM = "custom"

    @staticmethod
    def get_n8n_webhook_url_follow_up(agent_type: 'N8NWorkspaceAgentType', environment: Environment) -> str:
        base_url = "https://n8n.letschatty.com/webhook"
        def path(agent_type: N8NWorkspaceAgentType) -> str:
            return {
                N8NWorkspaceAgentType.CALENDAR_SCHEDULER: "calendar_scheduler/follow_up",
                N8NWorkspaceAgentType.TOKKO_BROKER: "tokko_broker/follow_up",
                N8NWorkspaceAgentType.DEFAULT: "default/follow_up",
            }[agent_type]
        if environment == Environment.PRODUCTION:
            return f"{base_url}/{path(agent_type)}"
        else:
            return f"{base_url}/demo/{path(agent_type)}"

class N8NWorkspaceAgentTypeParameters(BaseModel):
    """Parameters for the N8N workspace agent type"""
    calendars: Optional[List[str]] = Field(default=None, description="List of emails to be used as calendars")
    tokko_broker_api_key: Optional[str] = Field(default=None, description="The API key for the Tokko broker")

class Tool(StrEnum):
    """Tool model"""
    CALENDAR_SCHEDULER = "calendar_scheduler"

class ChattyAIAgentPreview(ChattyAssetPreview):
    """Preview of the Chatty AI Agent"""
    general_objective: str = Field(..., description="General objective of the AI agent")
    n8n_workspace_agent_type: N8NWorkspaceAgentType = Field(description="The type of agent to redirect the message to")

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        return super().get_projection() | {"general_objective": 1, "n8n_workspace_agent_type": 1}

    @classmethod
    def from_asset(cls, asset: 'ChattyAIAgent') -> 'ChattyAIAgentPreview':
        return cls(
            _id=asset.id,
            name=asset.name,
            company_id=asset.company_id,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            general_objective=asset.general_objective,
            n8n_workspace_agent_type=asset.n8n_workspace_agent_type
        )

class ChattyAIAgent(CompanyAssetModel):
    """AI Agent configuration model"""
    # Basic Information
    mode: ChattyAIMode = Field(default=ChattyAIMode.OFF)
    name: str = Field(..., description="Name of the AI agent")
    personality: str = Field(..., description="Detailed personality description of the agent")
    general_objective: str = Field(..., description="General objective/goal of the agent")
    unbreakable_rules: List[str] = Field(default_factory=list, description="List of unbreakable rules")
    control_triggers: List[str] = Field(default_factory=list, description="Triggers for human handoff")
    test_source_id: Optional[StrObjectId] = Field(default=None, description="Test source id")
    n8n_workspace_agent_type: N8NWorkspaceAgentType = Field(default=N8NWorkspaceAgentType.DEFAULT, description="The type of agent to redirect the message to")
    n8n_workspace_agent_type_parameteres : N8NWorkspaceAgentTypeParameters = Field(default=N8NWorkspaceAgentTypeParameters(), description="The parameters for the N8N workspace agent type")

    preview_class: ClassVar[type[ChattyAIAgentPreview]] = ChattyAIAgentPreview
    # Configuration
    follow_up_strategies: List[StrObjectId] = Field(default_factory=list, description="List of follow-up strategy ids")
    contexts: List[StrObjectId] = Field(default_factory=list, description="List of context items")
    faqs: List[StrObjectId] = Field(default_factory=list, description="Frequently asked questions")
    examples: List[StrObjectId] = Field(default_factory=list, description="Training examples")

    """json example:
    {
        "name": "Chatty AI Agent 1",
        "personality": "You are a helpful assistant",
        "mode": "autonomous",
        "unbreakable_rules": ["You cannot break the law"],
        "control_triggers": ["You cannot break the law"],
        "n8n_webhook_url": "https://n8n.com/webhook",
        "general_objective": "You are a helpful assistant",
        "tools": ["calendar_scheduler"],
        "calendars": ["test@test.com"],
        "follow_up_strategies": ["507f1f77bcf86cd799439011"],
        "contexts": ["507f1f77bcf86cd799439011", "507f1f77bcf86cd799439012"],
        "faqs": ["507f1f77bcf86cd799439011", "507f1f77bcf86cd799439012"],
        "examples": ["507f1f77bcf86cd799439011", "507f1f77bcf86cd799439012"]
    }
    """

    @field_validator('personality')
    @classmethod
    def validate_personality_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Personality cannot be empty")
        return v.strip()

    @field_validator('general_objective')
    @classmethod
    def validate_objective_not_empty(cls, v):
        if not v.strip():
            raise ValueError("General objective cannot be empty")
        return v.strip()

    @property
    def test_trigger(self) -> str:
        """Get the test trigger"""
        return f"Hola! Quiero testear al Chatty AI Agent {self.name} {self.id}"