from __future__ import annotations

from unittest.mock import Mock

import pytest

from agentic_devtools.cli import pull_request_approval as commands


def test_builds_github_request_from_state(monkeypatch: pytest.MonkeyPatch) -> None:
    values = {
        "platform.code_hosting": "github",
        "github.pull_request_number": 7,
        "github.repo": "owner/repo",
        "content": "LGTM",
        "sourceCodeHostingPlatform.pullRequest.headSha": "a" * 40,
    }
    monkeypatch.setattr(commands, "load_state_locked", lambda: values)
    request = commands._build_approval_request()
    assert request.repository == "owner/repo"
    assert request.pull_request_id == 7


@pytest.mark.parametrize(
    ("stored_id", "github_id", "conflicts"),
    [(41, 42, True), (41, 41, False)],
)
def test_github_state_ids_must_not_conflict(
    monkeypatch: pytest.MonkeyPatch, stored_id: int, github_id: int, conflicts: bool
) -> None:
    values = {
        "platform.code_hosting": "github",
        "pull_request_id": stored_id,
        "github.pull_request_number": github_id,
        "github.repo": "owner/repo",
        "content": "LGTM",
        "sourceCodeHostingPlatform.pullRequest.headSha": "a" * 40,
    }
    monkeypatch.setattr(commands, "load_state_locked", lambda: values)

    if conflicts:
        with pytest.raises(ValueError, match="Conflicting pull-request IDs"):
            commands._build_approval_request()
    else:
        request = commands._build_approval_request()
        assert request.pull_request_id == stored_id


def test_canonical_github_head_takes_precedence_over_stale_alias(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    values = {
        "platform.code_hosting": "github",
        "github.pull_request_number": 7,
        "github.repo": "owner/repo",
        "content": "LGTM",
        "github.head_ref_oid": "b" * 40,
        "github.head_sha": "c" * 40,
        "sourceCodeHostingPlatform.pullRequest.headSha": "a" * 40,
    }
    monkeypatch.setattr(commands, "load_state_locked", lambda: values)
    request = commands._build_approval_request()
    assert request.expected_head == "a" * 40


def test_explicit_reviewed_head_overrides_live_head(monkeypatch: pytest.MonkeyPatch) -> None:
    values = {
        "platform.code_hosting": "github",
        "github.pull_request_number": 7,
        "github.repo": "owner/repo",
        "content": "LGTM",
        "github.head_ref_oid": "b" * 40,
    }
    monkeypatch.setattr(commands, "load_state_locked", lambda: values)
    request = commands._build_approval_request(expected_head="a" * 40)
    assert request.expected_head == "a" * 40


def test_builds_azure_request_from_explicit_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(commands, "load_state_locked", lambda: {})
    monkeypatch.setattr(commands, "resolve_approval_provider", lambda *_: "azure_devops")
    monkeypatch.setattr(
        commands,
        "AzureDevOpsConfig",
        type(
            "Config",
            (),
            {
                "from_state": staticmethod(
                    lambda state=None: type(
                        "C",
                        (),
                        {
                            "organization": "https://dev.azure.com/example",
                            "project": "project",
                            "repository": "repo",
                        },
                    )
                )
            },
        ),
    )
    request = commands._build_approval_request(pull_request_id=3, content="LGTM")
    assert request.provider == "azure_devops"
    assert request.repository == "repo"
    assert request.organization == "https://dev.azure.com/example"
    assert request.project == "project"


def test_builds_azure_request_from_config_snapshot(monkeypatch: pytest.MonkeyPatch) -> None:
    values = {
        "platform.code_hosting": "azure_devops",
        "pull_request_id": 3,
        "content": "LGTM",
        "repository": "stale-state-repo",
    }
    monkeypatch.setattr(commands, "load_state_locked", lambda: values)
    monkeypatch.setattr(commands, "resolve_approval_provider", lambda *_: "azure_devops")
    monkeypatch.setattr(
        commands,
        "AzureDevOpsConfig",
        type(
            "Config",
            (),
            {
                "from_state": staticmethod(
                    lambda state=None: type(
                        "C",
                        (),
                        {
                            "organization": "https://dev.azure.com/example",
                            "project": "project",
                            "repository": "snapshot-repo",
                        },
                    )
                )
            },
        ),
    )
    request = commands._build_approval_request()
    assert request.repository == "snapshot-repo"
    assert request.organization == "https://dev.azure.com/example"
    assert request.project == "project"


@pytest.mark.parametrize("kwargs", [{}, {"content": "x"}])
def test_requires_id_and_content(monkeypatch: pytest.MonkeyPatch, kwargs: dict[str, str]) -> None:
    monkeypatch.setattr(commands, "load_state_locked", lambda: {})
    monkeypatch.setattr(commands, "resolve_approval_provider", lambda *_: "azure_devops")
    with pytest.raises(ValueError):
        commands._build_approval_request(**kwargs)  # type: ignore[arg-type]


def test_state_or_and_explicit_optional_values(monkeypatch: pytest.MonkeyPatch) -> None:
    values = {"platform.code_hosting": "azure_devops", "repository": "repo"}
    monkeypatch.setattr(commands, "load_state_locked", lambda: values)
    request = commands._build_approval_request(pull_request_id=4, content="LGTM", dry_run=False)
    assert request.pull_request_id == 4
    assert request.dry_run is False


def test_rejects_non_string_head(monkeypatch: pytest.MonkeyPatch) -> None:
    values = {
        "platform.code_hosting": "github",
        "github.repo": "owner/repo",
        "sourceCodeHostingPlatform.pullRequest.headSha": 7,
    }
    monkeypatch.setattr(commands, "load_state_locked", lambda: values)
    with pytest.raises(ValueError, match="expected_head"):
        commands._build_approval_request(pull_request_id=1, content="LGTM")


def test_azure_request_ignores_github_pull_request_number_alias(monkeypatch: pytest.MonkeyPatch) -> None:
    values = {
        "platform.code_hosting": "azure_devops",
        "repository": "repo",
        "content": "LGTM",
        "github.pull_request_number": 99,
    }
    monkeypatch.setattr(commands, "load_state_locked", lambda: values)
    with pytest.raises(ValueError, match="pull_request_id"):
        commands._build_approval_request()


def test_falls_back_to_legacy_github_head_ref_oid_alias(monkeypatch: pytest.MonkeyPatch) -> None:
    values = {
        "platform.code_hosting": "github",
        "github.pull_request_number": 7,
        "github.repo": "owner/repo",
        "content": "LGTM",
        "github.head_ref_oid": "b" * 40,
    }
    monkeypatch.setattr(commands, "load_state_locked", lambda: values)
    request = commands._build_approval_request()
    assert request.expected_head == "b" * 40


def test_reviewed_github_head_sha_precedes_live_head_alias(monkeypatch: pytest.MonkeyPatch) -> None:
    values = {
        "platform.code_hosting": "github",
        "github.pull_request_number": 7,
        "github.repo": "owner/repo",
        "content": "LGTM",
        "github.head_sha": "a" * 40,
        "github.head_ref_oid": "b" * 40,
    }
    monkeypatch.setattr(commands, "load_state_locked", lambda: values)

    request = commands._build_approval_request()

    assert request.expected_head == "a" * 40


def test_azure_request_ignores_stray_head_sha_state(monkeypatch: pytest.MonkeyPatch) -> None:
    """Azure DevOps requests must not inherit a leftover provider-agnostic head-SHA state value."""
    values = {
        "platform.code_hosting": "azure_devops",
        "repository": "repo",
        "content": "LGTM",
        "sourceCodeHostingPlatform.pullRequest.headSha": "c" * 40,
    }
    monkeypatch.setattr(commands, "load_state_locked", lambda: values)
    request = commands._build_approval_request(pull_request_id=1)
    assert request.expected_head is None


def test_builds_request_from_one_locked_state_snapshot(monkeypatch: pytest.MonkeyPatch) -> None:
    state = {
        "platform": {"code_hosting": "github"},
        "github": {
            "pull_request_number": 17,
            "repo": "owner/repo",
            "head_ref_oid": "a" * 40,
        },
        "content": "LGTM",
        "dry_run": True,
    }
    load_snapshot = Mock(return_value=state)
    monkeypatch.setattr(commands, "load_state_locked", load_snapshot, raising=False)
    monkeypatch.setattr(commands, "get_value", lambda *_: pytest.fail("global state must not be reread"))

    request = commands._build_approval_request()

    load_snapshot.assert_called_once_with()
    assert request.provider == "github"
    assert request.repository == "owner/repo"
    assert request.pull_request_id == 17
    assert request.expected_head == "a" * 40
    assert request.content == "LGTM"
    assert request.dry_run is True


def test_parses_dry_run_string_from_state(monkeypatch: pytest.MonkeyPatch) -> None:
    state = {
        "platform.code_hosting": "github",
        "github.pull_request_number": 17,
        "github.repo": "owner/repo",
        "github.head_ref_oid": "a" * 40,
        "content": "LGTM",
        "dry_run": "yes",
    }
    monkeypatch.setattr(commands, "load_state_locked", lambda: state)

    request = commands._build_approval_request()

    assert request.dry_run is True
