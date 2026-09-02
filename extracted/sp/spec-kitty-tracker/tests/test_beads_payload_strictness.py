"""TRK-M1-03 A8: Beads payload strictness.

N3 (TRK-M1-01 draft matrix): a malformed or out-of-vocabulary Beads
payload must fail closed with a typed IssuePayloadContractError -- never
default to a guessed value ("Untitled", TODO, TASK, BLOCKED_BY).
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import pytest

from spec_kitty_tracker import (
    BeadsConnector,
    BeadsConnectorConfig,
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


def _starts_with(*parts: str) -> Matcher:
    return lambda cmd: len(cmd) >= len(parts) and list(cmd[: len(parts)]) == list(parts)


def _connector(output: str) -> BeadsConnector:
    runner = ScriptedRunner(script=[(_starts_with("bd", "--json", "list"), output)])
    return BeadsConnector(config=BeadsConnectorConfig(workspace="demo"), runner=runner)


async def test_invalid_json_raises_bd_000() -> None:
    connector = _connector("{not json")

    with pytest.raises(IssuePayloadContractError) as excinfo:
        await connector.list_issues(updated_since=None, cursor=None, limit=50, filters=None)

    assert excinfo.value.reason == "BD-000"


async def test_missing_id_raises_bd_001() -> None:
    connector = _connector('[{"title": "x", "status": "open"}]')

    with pytest.raises(IssuePayloadContractError) as excinfo:
        await connector.list_issues(updated_since=None, cursor=None, limit=50, filters=None)

    assert excinfo.value.reason == "BD-001"
    assert excinfo.value.field_path == "id"


async def test_missing_title_raises_bd_002_never_untitled() -> None:
    connector = _connector('[{"id": "bd-1", "status": "open"}]')

    with pytest.raises(IssuePayloadContractError) as excinfo:
        await connector.list_issues(updated_since=None, cursor=None, limit=50, filters=None)

    assert excinfo.value.reason == "BD-002"
    assert excinfo.value.field_path == "title"


async def test_unknown_status_raises_bd_003_never_defaults_to_todo() -> None:
    connector = _connector('[{"id": "bd-1", "title": "x", "status": "weird"}]')

    with pytest.raises(IssuePayloadContractError) as excinfo:
        await connector.list_issues(updated_since=None, cursor=None, limit=50, filters=None)

    assert excinfo.value.reason == "BD-003"
    assert excinfo.value.field_path == "status"


async def test_unknown_issue_type_raises_bd_004_never_defaults_to_task() -> None:
    connector = _connector(
        '[{"id": "bd-1", "title": "x", "status": "open", "issue_type": "mystery"}]'
    )

    with pytest.raises(IssuePayloadContractError) as excinfo:
        await connector.list_issues(updated_since=None, cursor=None, limit=50, filters=None)

    assert excinfo.value.reason == "BD-004"
    assert excinfo.value.field_path == "issue_type"


async def test_unknown_dependency_type_raises_bd_005_never_defaults_to_blocked_by() -> None:
    connector = _connector(
        '[{"id": "bd-1", "title": "x", "status": "open", '
        '"dependencies": [{"id": "bd-2", "dependency_type": "mystery"}]}]'
    )

    with pytest.raises(IssuePayloadContractError) as excinfo:
        await connector.list_issues(updated_since=None, cursor=None, limit=50, filters=None)

    assert excinfo.value.reason == "BD-005"


async def test_known_beads_vocabulary_still_parses() -> None:
    connector = _connector(
        '[{"id": "bd-1", "title": "x", "status": "closed", "issue_type": "epic", '
        '"dependencies": [{"id": "bd-2", "dependency_type": "blocks"}]}]'
    )
    page = await connector.list_issues(updated_since=None, cursor=None, limit=50, filters=None)
    assert len(page.items) == 1
    assert page.items[0].title == "x"
