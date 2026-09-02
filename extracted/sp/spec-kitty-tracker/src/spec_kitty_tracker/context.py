"""Local execution context for local/native tracker connectors.

TRK-M1-02 A3 (see TRK-M1-01 contract-freeze draft §3.2). Local/native
connectors (Beads, FP) receive a caller-supplied :class:`LocalExecutionContext`
so calls can be attributed to an actor and preserve the caller's current
task/team/repository scope, per docs/TRACKER_ARCH_ROLE.md:43 ("Local/native
connectors receive a caller-supplied local execution context and must
preserve current task/team/repository scope").

This module owns the type only. How a host constructs and threads a context
through :class:`~spec_kitty_tracker.connectors.cli_runner.CommandRunner` is
covered by TRK-M1-02 A4 (``context.py`` + ``cli_runner.py`` +
``connectors/beads.py`` + ``connectors/fp.py``); how a host maps a program
gateway binding onto this type is host territory (TRK-M1-04, spec-kitty
repo) — Tracker must not import control-plane code or know intent formats
(TRK-M1-01 draft D2).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LocalExecutionContext:
    actor: str
    repository: str
    team: str | None = None
    mission_id: str | None = None
    task_id: str | None = None

    def __post_init__(self) -> None:
        if not self.actor.strip():
            raise ValueError("LocalExecutionContext.actor must not be empty")
        if not self.repository.strip():
            raise ValueError("LocalExecutionContext.repository must not be empty")
