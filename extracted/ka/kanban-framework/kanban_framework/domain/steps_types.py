"""Shared types for step definitions."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StepDef:
    id: str
    description: str
    actions: list[str] = field(default_factory=list)
    agent_type: Optional[str] = None
    parallel: bool = False
    user_action: bool = False
    spawn_prompt: Optional[str] = None
    interactive: bool = False
    required_artifacts: list[str] = field(default_factory=list)
    after: list[str] = field(default_factory=list)
    type: str = "action"
    guard: dict | None = None
    gateway: dict | None = None
    knowledge: dict | None = None
