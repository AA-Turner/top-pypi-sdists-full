"""Tests for the AgentTaskPrIdentity record."""

from dataclasses import FrozenInstanceError, fields
from typing import get_type_hints

import pytest

from agentic_devtools.cli.ci.agent_task_lifecycle import AgentTaskLifecycle
from agentic_devtools.cli.ci.agent_task_pr_identity import (
    AgentTaskPrIdentity,
    AgentTaskPrIdentityKind,
)


def test_record_has_typed_fields_and_immutable_default_values() -> None:
    identity = AgentTaskPrIdentity()

    identity_hints = get_type_hints(AgentTaskPrIdentity)
    assert identity.kind is AgentTaskPrIdentityKind.NONE
    assert identity.correlates is False
    assert identity.task_pr_number is None
    assert identity.task_branch == ""
    assert identity_hints["kind"] is AgentTaskPrIdentityKind
    assert identity_hints["correlates"] is bool
    assert identity_hints["task_pr_number"] == int | None
    assert identity_hints["task_branch"] is str
    assert [item.name for item in fields(AgentTaskPrIdentity)] == [
        "kind",
        "correlates",
        "task_pr_number",
        "task_branch",
    ]
    with pytest.raises(FrozenInstanceError):
        identity.correlates = True  # type: ignore[misc]


def test_existing_lifecycle_construction_uses_default_identity() -> None:
    lifecycle = AgentTaskLifecycle("task", "owner/repo", 42, "branch", "running", "created")

    assert get_type_hints(AgentTaskLifecycle)["pr_identity"] is AgentTaskPrIdentity
    assert lifecycle.pr_identity == AgentTaskPrIdentity()
