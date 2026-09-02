"""TRK-M1-03 A5: Beads write denial.

N4 (TRK-M1-01 draft matrix): the Beads connector must never assign or
close/cancel a Bead, and must never silently drop a patch key it cannot
carry (``custom_fields``, ``links``). Every denial is a typed
``CapabilityNotSupportedError`` raised before any ``bd`` command is issued.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import pytest

from spec_kitty_tracker import (
    BeadsConnector,
    BeadsConnectorConfig,
    CanonicalIssue,
    CanonicalIssueType,
    CanonicalStatus,
    CapabilityNotSupportedError,
    ExternalRef,
)

Matcher = Callable[[Sequence[str]], bool]


@dataclass
class ScriptedRunner:
    script: list[tuple[Matcher, str]]

    def __post_init__(self) -> None:
        self.commands: list[list[str]] = []

    def run(self, command: Sequence[str], *, cwd: str | None = None, context: object = None) -> str:
        del cwd, context
        cmd = list(command)
        self.commands.append(cmd)
        for matcher, output in self.script:
            if matcher(cmd):
                return output
        raise AssertionError(f"Unexpected command: {' '.join(cmd)}")


def _starts_with(*parts: str) -> Matcher:
    return lambda cmd: len(cmd) >= len(parts) and list(cmd[: len(parts)]) == list(parts)


def _connector(
    script: list[tuple[Matcher, str]] | None = None,
) -> tuple[BeadsConnector, ScriptedRunner]:
    runner = ScriptedRunner(script=script or [])
    connector = BeadsConnector(config=BeadsConnectorConfig(workspace="demo"), runner=runner)
    return connector, runner


async def test_update_issue_denies_assignees() -> None:
    connector, runner = _connector()
    ref = ExternalRef(system="beads", workspace="demo", id="bd-1")

    with pytest.raises(CapabilityNotSupportedError):
        await connector.update_issue(ref, {"assignees": ["ivan"]}, idempotency_key=None)

    assert runner.commands == []


async def test_update_issue_denies_terminal_status_done() -> None:
    connector, runner = _connector()
    ref = ExternalRef(system="beads", workspace="demo", id="bd-1")

    with pytest.raises(CapabilityNotSupportedError):
        await connector.update_issue(ref, {"status": CanonicalStatus.DONE}, idempotency_key=None)

    assert runner.commands == []


async def test_update_issue_denies_terminal_status_canceled() -> None:
    connector, runner = _connector()
    ref = ExternalRef(system="beads", workspace="demo", id="bd-1")

    with pytest.raises(CapabilityNotSupportedError):
        await connector.update_issue(
            ref, {"status": CanonicalStatus.CANCELED}, idempotency_key=None
        )

    assert runner.commands == []


async def test_transition_issue_denies_terminal_status() -> None:
    connector, runner = _connector()
    ref = ExternalRef(system="beads", workspace="demo", id="bd-1")

    with pytest.raises(CapabilityNotSupportedError):
        await connector.transition_issue(ref, CanonicalStatus.DONE)

    assert runner.commands == []


async def test_update_issue_non_terminal_status_still_allowed() -> None:
    connector, _runner = _connector(
        script=[
            (_starts_with("bd", "--json", "update", "bd-1"), "{}"),
            (
                _starts_with("bd", "--json", "show", "bd-1"),
                '{"id": "bd-1", "title": "T", "status": "in_progress"}',
            ),
        ]
    )
    ref = ExternalRef(system="beads", workspace="demo", id="bd-1")

    result = await connector.update_issue(
        ref, {"status": CanonicalStatus.IN_PROGRESS}, idempotency_key=None
    )
    assert result.status == CanonicalStatus.IN_PROGRESS


async def test_update_issue_denies_custom_fields_no_silent_drop() -> None:
    connector, runner = _connector()
    ref = ExternalRef(system="beads", workspace="demo", id="bd-1")

    with pytest.raises(CapabilityNotSupportedError):
        await connector.update_issue(ref, {"custom_fields": {"x": 1}}, idempotency_key=None)

    assert runner.commands == []


async def test_update_issue_denies_links_no_silent_drop() -> None:
    connector, runner = _connector()
    ref = ExternalRef(system="beads", workspace="demo", id="bd-1")

    with pytest.raises(CapabilityNotSupportedError):
        await connector.update_issue(ref, {"links": []}, idempotency_key=None)

    assert runner.commands == []


async def test_create_issue_never_emits_assignee_flag() -> None:
    connector, runner = _connector(
        script=[
            (_starts_with("bd", "--json", "create"), '{"id": "bd-101"}'),
            (
                _starts_with("bd", "--json", "show", "bd-101"),
                '{"id": "bd-101", "title": "New item", "status": "open"}',
            ),
        ]
    )

    await connector.create_issue(
        CanonicalIssue(
            ref=ExternalRef(system="beads", workspace="demo", id="tmp"),
            title="New item",
            body=None,
            status=CanonicalStatus.TODO,
            issue_type=CanonicalIssueType.TASK,
            assignees=["ivan"],
        )
    )

    create_cmd = next(cmd for cmd in runner.commands if cmd[2] == "create")
    assert "--assignee" not in create_cmd
