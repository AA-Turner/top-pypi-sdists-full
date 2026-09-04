# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_spi.models.model_project_tracker
# COMPAT_REMOVAL_DATE: 2026-10-01
# COMPAT_RETENTION_NOTE: extended 2026-09-01 -> 2026-10-01 under OMN-16602.
# The original date expired mid-flight and hard-fails the required `validate`
# job for EVERY PR on this repo, so extending is the retention policy's own
# sanctioned action (see scripts/check_compat_retention.py: "migrate or extend
# the date"). Extended rather than removed on purpose: removal is a breaking
# API change to a published package and needs its own version bump and
# release, not a documentation PR. Live readiness measured 2026-09-02 and
# recorded on OMN-16602 — see that ticket before extending a second time.

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
