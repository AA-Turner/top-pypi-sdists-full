"""A2A (agent-to-agent) models (protocol v1.0)."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class AgentProvider(BaseModel):
    """Provider information for an A2A agent card."""

    model_config = ConfigDict(extra="ignore")

    organization: str | None = None
    url: str | None = None


class AgentInterface(BaseModel):
    """A transport interface the agent exposes."""

    model_config = ConfigDict(extra="ignore")

    url: str
    protocolBinding: str | None = None
    protocolVersion: str | None = None


class AgentCapabilities(BaseModel):
    """Capabilities advertised by an A2A agent card."""

    model_config = ConfigDict(extra="ignore")

    streaming: bool = False
    pushNotifications: bool = False
    extendedAgentCard: bool = False


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
    supportedInterfaces: list[AgentInterface]
    provider: AgentProvider | None = None
    version: str
    documentationUrl: str | None = None
    capabilities: AgentCapabilities
    securitySchemes: dict[str, dict[str, Any]] | None = None
    securityRequirements: list[dict[str, Any]] | None = None
    defaultInputModes: list[str] = []
    defaultOutputModes: list[str] = []
    skills: list[AgentSkill]

    @property
    def protocol_version(self) -> str | None:
        """Protocol version of the first advertised interface."""
        if self.supportedInterfaces:
            return self.supportedInterfaces[0].protocolVersion
        return None
