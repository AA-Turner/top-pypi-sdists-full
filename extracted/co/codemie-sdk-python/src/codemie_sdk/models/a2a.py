"""A2A (agent-to-agent) models."""

from pydantic import BaseModel, ConfigDict


class AgentProvider(BaseModel):
    """Provider information for an A2A agent card."""

    model_config = ConfigDict(extra="ignore")

    organization: str
    url: str | None = None


class AgentCapabilities(BaseModel):
    """Capabilities advertised by an A2A agent card."""

    model_config = ConfigDict(extra="ignore")

    streaming: bool = False
    pushNotifications: bool = False
    stateTransitionHistory: bool = False


class AgentAuthentication(BaseModel):
    """Authentication schemes advertised by an A2A agent card."""

    model_config = ConfigDict(extra="ignore")

    schemes: list[str]
    credentials: str | None = None


class AgentSkill(BaseModel):
    """A single skill exposed by an A2A agent card."""

    model_config = ConfigDict(extra="ignore")

    id: str
    name: str
    description: str | None = None
    tags: list[str] | None = None
    examples: list[str] | None = None
    inputModes: list[str] | None = None
    outputModes: list[str] | None = None


class AgentCard(BaseModel):
    """A2A agent card describing an assistant for agent discovery."""

    model_config = ConfigDict(extra="ignore")

    name: str
    description: str | None = None
    url: str
    provider: AgentProvider | None = None
    version: str
    documentationUrl: str | None = None
    capabilities: AgentCapabilities
    authentication: AgentAuthentication | None = None
    defaultInputModes: list[str] = ["text"]
    defaultOutputModes: list[str] = ["text"]
    skills: list[AgentSkill]
