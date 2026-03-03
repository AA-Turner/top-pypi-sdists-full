"""Data models for Plato worlds."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class WorkspaceSnapshot(BaseModel):
    """Snapshot of a workspace's state at save time."""

    name: str
    path: str
    tracked: bool = False
    repo_name: str = ""
    s3_bucket: str = ""
    s3_prefix: str = ""
    head_hash: str | None = None
    steps: list[str] = Field(default_factory=list)


class StateHistoryEntry(BaseModel):
    """A single entry in the state history log."""

    step: int
    timestamp: str = ""
    workspaces: dict[str, WorkspaceSnapshot] = Field(default_factory=dict)


class WorldState(BaseModel):
    """Base state model for all worlds.

    World-specific state models should extend this::

        class MyState(WorldState):
            current_step: int = 0
            scores: list[float] = []
    """

    workspaces: dict[str, WorkspaceSnapshot] = Field(default_factory=dict)
    state_history: list[StateHistoryEntry] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class Observation(BaseModel):
    """Observation returned from reset/step."""

    data: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "allow"}


class StepResult(BaseModel):
    """Result of a step."""

    observation: Observation
    done: bool = False
    info: dict[str, Any] = Field(default_factory=dict)
