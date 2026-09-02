from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Callable

from spec_kitty_tracker import (
    BeadsConnector,
    BeadsConnectorConfig,
    CanonicalIssue,
    CanonicalIssueType,
    CanonicalLink,
    CanonicalStatus,
    ExternalRef,
    FPConnector,
    FPConnectorConfig,
    LinkType,
)

Matcher = Callable[[Sequence[str]], bool]


@dataclass
class ScriptedRunner:
    script: list[tuple[Matcher, str]]

    def __post_init__(self) -> None:
        self.commands: list[list[str]] = []

    def run(self, command: Sequence[str], *, cwd: str | None = None) -> str:
        del cwd
        cmd = list(command)
        self.commands.append(cmd)
        for matcher, output in self.script:
            if matcher(cmd):
                return output
        raise AssertionError(f"Unexpected command: {' '.join(cmd)}")


def _starts_with(*parts: str) -> Matcher:
    return lambda cmd: len(cmd) >= len(parts) and list(cmd[: len(parts)]) == list(parts)


async def test_beads_connector_list_and_create_flow() -> None:
    runner = ScriptedRunner(
        script=[
            (
                _starts_with("bd", "--json", "list"),
                """
                [
                  {
                    "id": "bd-1",
                    "title": "Fix auth",
                    "description": "Use OAuth",
                    "status": "in_progress",
                    "priority": 1,
                    "issue_type": "bug",
                    "labels": ["backend"],
                    "created_at": "2026-02-26T10:00:00Z",
                    "updated_at": "2026-02-26T11:00:00Z"
                  }
                ]
                """,
            ),
            (
                _starts_with("bd", "--json", "create"),
                '{"id": "bd-101"}',
            ),
            (
                _starts_with("bd", "--json", "show", "bd-101"),
                """
                {
                  "issue": {
                    "id": "bd-101",
                    "title": "New item",
                    "description": "desc",
                    "status": "open",
                    "priority": 2,
                    "issue_type": "task",
                    "created_at": "2026-02-26T10:00:00Z",
                    "updated_at": "2026-02-26T10:01:00Z"
                  },
                  "comments": []
                }
                """,
            ),
            (
                _starts_with("bd", "--json", "comments", "add", "bd-101"),
                "{}",
            ),
            (
                _starts_with("bd", "--json", "dep", "add", "bd-101", "bd-200"),
                "{}",
            ),
        ]
    )

    connector = BeadsConnector(
        config=BeadsConnectorConfig(workspace="demo"),
        runner=runner,
    )

    page = await connector.list_issues(
        updated_since=None,
        cursor=None,
        limit=50,
        filters=None,
    )
    assert len(page.items) == 1
    assert page.items[0].status == CanonicalStatus.IN_PROGRESS
    assert page.items[0].issue_type == CanonicalIssueType.BUG

    created = await connector.create_issue(
        CanonicalIssue(
            ref=ExternalRef(system="beads", workspace="demo", id="tmp"),
            title="New item",
            body="desc",
            status=CanonicalStatus.TODO,
            issue_type=CanonicalIssueType.TASK,
        )
    )
    assert created.ref.id == "bd-101"

    await connector.add_comment(created.ref, "working on it")
    await connector.upsert_link(
        created.ref,
        CanonicalLink(
            type=LinkType.BLOCKED_BY,
            target=ExternalRef(system="beads", workspace="demo", id="bd-200"),
        ),
    )

    flat = [" ".join(command) for command in runner.commands]
    assert any(cmd.startswith("bd --json create") for cmd in flat)
    assert any("bd --json comments add bd-101" in cmd for cmd in flat)
    assert any("bd --json dep add bd-101 bd-200 --type blocks" in cmd for cmd in flat)


async def test_fp_connector_list_get_create_and_update() -> None:
    runner = ScriptedRunner(
        script=[
            (
                _starts_with("fp", "issue", "list"),
                """
                FP-abcd [todo] [high] Build auth flow
                FP-efgh [in-progress] [medium] Implement callback handler
                """,
            ),
            (
                _starts_with("fp", "issue", "show", "FP-abcd"),
                "FP-abcd [todo] [high] Build auth flow",
            ),
            (
                _starts_with("fp", "context", "FP-abcd"),
                "Issue context for FP-abcd",
            ),
            (
                _starts_with("fp", "issue", "create"),
                "Created issue FP-ijkl",
            ),
            (
                _starts_with("fp", "issue", "show", "FP-ijkl"),
                "FP-ijkl [todo] [medium] New fp issue",
            ),
            (
                _starts_with("fp", "context", "FP-ijkl"),
                "Issue context for FP-ijkl",
            ),
            (
                _starts_with("fp", "issue", "update", "--status", "in-progress", "FP-ijkl"),
                "Updated FP-ijkl",
            ),
            (
                _starts_with("fp", "comment", "FP-ijkl"),
                "Comment added",
            ),
            (
                _starts_with("fp", "issue", "update", "--depends", "FP-9999", "FP-ijkl"),
                "Updated dependencies",
            ),
        ]
    )

    connector = FPConnector(
        config=FPConnectorConfig(workspace="demo"),
        runner=runner,
    )

    page = await connector.list_issues(
        updated_since=None,
        cursor=None,
        limit=20,
        filters=None,
    )
    assert len(page.items) == 2
    assert page.items[0].ref.id == "FP-abcd"
    assert page.items[0].status == CanonicalStatus.TODO

    issue = await connector.get_issue(ExternalRef(system="fp", workspace="demo", id="FP-abcd"))
    assert issue.title == "Build auth flow"
    assert issue.body == "Issue context for FP-abcd"

    created = await connector.create_issue(
        CanonicalIssue(
            ref=ExternalRef(system="fp", workspace="demo", id="tmp"),
            title="New fp issue",
            body="context",
            status=CanonicalStatus.TODO,
            issue_type=CanonicalIssueType.TASK,
        )
    )
    assert created.ref.id == "FP-ijkl"

    moved = await connector.transition_issue(created.ref, CanonicalStatus.IN_PROGRESS)
    assert moved.status == CanonicalStatus.TODO  # parsed from scripted show output

    await connector.add_comment(created.ref, "progress")
    await connector.upsert_link(
        created.ref,
        CanonicalLink(
            type=LinkType.BLOCKED_BY,
            target=ExternalRef(system="fp", workspace="demo", id="FP-9999"),
        ),
    )

    flat = [" ".join(command) for command in runner.commands]
    assert any(cmd.startswith("fp issue create --title New fp issue") for cmd in flat)
    assert any(cmd.startswith("fp issue update --status in-progress FP-ijkl") for cmd in flat)
    assert any(cmd.startswith("fp comment FP-ijkl progress") for cmd in flat)
    assert any(cmd.startswith("fp issue update --depends FP-9999 FP-ijkl") for cmd in flat)
