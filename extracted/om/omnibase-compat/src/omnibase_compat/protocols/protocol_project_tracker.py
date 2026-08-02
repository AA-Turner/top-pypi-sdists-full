# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_spi.protocols.protocol_project_tracker
# COMPAT_REMOVAL_DATE: 2026-09-01

from __future__ import annotations

from abc import ABC, abstractmethod

from omnibase_compat.models.model_project_tracker import (
    ModelIssueStatus,
    ModelLabel,
    ModelTeam,
)


class ProtocolProjectTracker(ABC):
    """Abstract base for project tracker adapters (Linear, Jira, etc.)."""

    @abstractmethod
    def list_teams(self) -> list[ModelTeam]: ...

    @abstractmethod
    def list_issue_labels(self, team: str) -> list[ModelLabel]: ...

    @abstractmethod
    def list_issue_statuses(self, team: str) -> list[ModelIssueStatus]: ...


__all__: list[str] = [
    "ProtocolProjectTracker",
]
