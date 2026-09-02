"""Tests for spec_kitty_tracker.context.LocalExecutionContext (TRK-M1-02 A3).

``LocalExecutionContext`` is the caller-supplied local execution context that
local/native connectors carry so calls preserve current task/team/repository
scope and are attributable to an actor (docs/TRACKER_ARCH_ROLE.md:43;
TRK-M1-01 draft A3). This module defines the type only; wiring it through
connectors is exercised in test_command_runner_context.py.
"""

from __future__ import annotations

import pytest

from spec_kitty_tracker.context import LocalExecutionContext


def test_local_execution_context_minimal_construction() -> None:
    ctx = LocalExecutionContext(actor="ivan", repository="spec-kitty-tracker")

    assert ctx.actor == "ivan"
    assert ctx.repository == "spec-kitty-tracker"
    assert ctx.team is None
    assert ctx.mission_id is None
    assert ctx.task_id is None


def test_local_execution_context_full_construction() -> None:
    ctx = LocalExecutionContext(
        actor="ivan",
        repository="spec-kitty-tracker",
        team="team-kitty",
        mission_id="mission-01",
        task_id="TRK-M1-02",
    )

    assert ctx.team == "team-kitty"
    assert ctx.mission_id == "mission-01"
    assert ctx.task_id == "TRK-M1-02"


def test_local_execution_context_is_frozen() -> None:
    ctx = LocalExecutionContext(actor="ivan", repository="spec-kitty-tracker")

    with pytest.raises(AttributeError):
        ctx.actor = "someone-else"  # type: ignore[misc]


@pytest.mark.parametrize("actor,repository", [("", "repo"), ("   ", "repo")])
def test_local_execution_context_rejects_empty_actor(actor: str, repository: str) -> None:
    with pytest.raises(ValueError):
        LocalExecutionContext(actor=actor, repository=repository)


@pytest.mark.parametrize("actor,repository", [("ivan", ""), ("ivan", "   ")])
def test_local_execution_context_rejects_empty_repository(actor: str, repository: str) -> None:
    with pytest.raises(ValueError):
        LocalExecutionContext(actor=actor, repository=repository)
