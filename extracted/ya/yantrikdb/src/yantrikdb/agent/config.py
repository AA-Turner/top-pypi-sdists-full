"""Configuration models for Yantrik Companion."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field


class PersonalityConfig(BaseModel):
    name: str = "Yantrik"
    system_prompt: str = (
        "You are Yantrik, a personal companion running on your user's phone. "
        "You remember everything they tell you. You are warm, thoughtful, "
        "and occasionally curious. You speak concisely — this is a phone, "
        "not an essay contest. When you notice patterns or have concerns, "
        "you bring them up naturally. You never fabricate memories — "
        "if you don't know, say so."
    )


class LLMConfig(BaseModel):
    base_url: str = "http://localhost:8081"
    model: str = "local"
    max_tokens: int = 512
    temperature: float = 0.7
    max_context_tokens: int = 2048


class ServerConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8340


class YantrikDBConfig(BaseModel):
    db_path: str = "/opt/yantrik/data/memory.db"
    embedding_dim: int = 384
    embedding_url: Optional[str] = "http://localhost:8082"


class ConversationConfig(BaseModel):
    max_history_turns: int = 10
    session_timeout_minutes: int = 30


class ToolsConfig(BaseModel):
    enabled: bool = True
    max_tool_rounds: int = 3


class CognitionConfig(BaseModel):
    think_interval_minutes: int = 15
    think_interval_active_minutes: int = 5
    idle_think_interval_minutes: int = 30
    proactive_urgency_threshold: float = 0.7


class InstinctSettings(BaseModel):
    check_in_enabled: bool = True
    check_in_hours: float = 8.0
    emotional_awareness_enabled: bool = True
    follow_up_enabled: bool = True
    follow_up_min_hours: float = 4.0
    reminder_enabled: bool = True
    pattern_surfacing_enabled: bool = True
    conflict_alerting_enabled: bool = True
    conflict_alert_threshold: int = 5


class UrgeConfig(BaseModel):
    expiry_hours: float = 48.0
    max_pending: int = 20
    boost_increment: float = 0.1
    cooldown_seconds: float = 3600.0


class LoggingConfig(BaseModel):
    level: str = "INFO"
    file: Optional[str] = None


class CompanionConfig(BaseModel):
    user_name: str = "User"
    personality: PersonalityConfig = PersonalityConfig()
    llm: LLMConfig = LLMConfig()
    server: ServerConfig = ServerConfig()
    yantrikdb: YantrikDBConfig = YantrikDBConfig()
    conversation: ConversationConfig = ConversationConfig()
    tools: ToolsConfig = ToolsConfig()
    cognition: CognitionConfig = CognitionConfig()
    instincts: InstinctSettings = InstinctSettings()
    urges: UrgeConfig = UrgeConfig()
    logging: LoggingConfig = LoggingConfig()

    @classmethod
    def from_yaml(cls, path: str | Path) -> CompanionConfig:
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        return cls(**data)
