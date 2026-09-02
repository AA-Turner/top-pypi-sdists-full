"""TRK-M1-03 A6: strict patch-key rejection on every connector egress path.

N1 (TRK-M1-01 draft matrix): an unknown patch key must be rejected with
``IssuePayloadContractError(kind="patch", field_path=<key>, reason="PK-001")``
before any write is issued -- no connector may silently drop or guess at an
unrecognized key.
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
    ExternalRef,
    InMemoryConnector,
    IssuePayloadContractError,
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


async def test_in_memory_connector_rejects_unknown_patch_key() -> None:
    connector = InMemoryConnector(name="jira", workspace="demo")
    ref = ExternalRef(system="jira", workspace="demo", id="DEMO-1")
    await connector.create_issue(
        CanonicalIssue(
            ref=ref,
            title="First",
            body=None,
            status=CanonicalStatus.TODO,
            issue_type=CanonicalIssueType.TASK,
        )
    )

    with pytest.raises(IssuePayloadContractError) as excinfo:
        await connector.update_issue(ref, {"severity": 1}, idempotency_key=None)

    assert excinfo.value.kind == "patch"
    assert excinfo.value.field_path == "severity"
    assert excinfo.value.reason == "PK-001"


async def test_beads_connector_rejects_unknown_patch_key_before_any_command() -> None:
    runner = ScriptedRunner(script=[])
    connector = BeadsConnector(config=BeadsConnectorConfig(workspace="demo"), runner=runner)
    ref = ExternalRef(system="beads", workspace="demo", id="bd-1")

    with pytest.raises(IssuePayloadContractError) as excinfo:
        await connector.update_issue(ref, {"severity": 1}, idempotency_key=None)

    assert excinfo.value.kind == "patch"
    assert excinfo.value.field_path == "severity"
    assert excinfo.value.reason == "PK-001"
    assert runner.commands == [], "no bd command should be issued for a rejected patch"
