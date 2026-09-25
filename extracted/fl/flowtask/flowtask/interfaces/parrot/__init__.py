"""
Parrot-ai Interfaces for creating Chatbots and IA-Agents integrated with FlowTask.
"""
from .agent import AgentBase
from .config import (
    PODCAST_AGENT_ATTRIBUTES,
    AgentLLMConfig,
    NotificationChannel,
    NotificationConfig,
    NotificationOutcome,
    NotificationReport,
    ParrotAgentConfigMixin,
    PodcastConfig,
    SpeakerConfig,
    TeamsCardConfig,
    TeamsChannelRecipient,
    TeamsWebhookRecipient,
)

__all__ = (
    "AgentBase",
    "ParrotAgentConfigMixin",
    "PODCAST_AGENT_ATTRIBUTES",
    "AgentLLMConfig",
    "PodcastConfig",
    "SpeakerConfig",
    "NotificationChannel",
    "NotificationConfig",
    "NotificationOutcome",
    "NotificationReport",
    "TeamsCardConfig",
    "TeamsChannelRecipient",
    "TeamsWebhookRecipient",
)
