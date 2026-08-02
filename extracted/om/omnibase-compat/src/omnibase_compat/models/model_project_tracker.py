# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_spi.models.model_project_tracker
# COMPAT_REMOVAL_DATE: 2026-09-01

from __future__ import annotations

from pydantic import BaseModel, Field


class ModelTeam(BaseModel, frozen=True):
    id: str
    name: str
    key: str


class ModelLabel(BaseModel, frozen=True):
    id: str
    name: str
    color: str | None = Field(default=None)
    team_id: str | None = Field(default=None)


class ModelIssueStatus(BaseModel, frozen=True):
    id: str
    name: str
    type: str
    team_id: str | None = Field(default=None)


__all__: list[str] = [
    "ModelTeam",
    "ModelLabel",
    "ModelIssueStatus",
]
