from unittest.mock import patch

import pytest

from agentic_devtools.cli import pull_request_create


def test_build_create_request_snapshot_resolves_state_backed_values() -> None:
    values = {
        "platform.code_hosting": "github",
        "source_branch": "feature",
        "title": "Title",
        "description": "Body",
        "target_branch": "develop",
        "draft": "false",
        "reviewers": "alice,bob",
    }
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", side_effect=values.get),
        patch("agentic_devtools.cli.pull_request_create.is_dry_run", return_value=True),
    ):
        snapshot = pull_request_create._build_create_request_snapshot()

    assert snapshot == {
        "provider": "github",
        "source_branch": "feature",
        "title": "Title",
        "body": "Body",
        "body_is_explicit": True,
        "target_branch": "develop",
        "draft": False,
        "reviewers": ("alice", "bob"),
        "dry_run": True,
    }


def test_build_create_request_snapshot_defaults_empty_state_target_branch_to_main() -> None:
    values = {
        "platform.code_hosting": "github",
        "source_branch": "feature",
        "title": "Title",
        "target_branch": "",
    }
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", side_effect=values.get),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Body"),
    ):
        snapshot = pull_request_create._build_create_request_snapshot()

    assert snapshot["target_branch"] == "main"


def test_build_create_request_snapshot_renders_template_body_when_state_body_missing() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template body"),
    ):
        snapshot = pull_request_create._build_create_request_snapshot(
            provider="github",
            source_branch="feature",
            title="Title",
        )

    assert snapshot["body"] == "Template body"


def test_build_create_request_snapshot_preserves_formatted_state_title() -> None:
    values = {
        "platform.code_hosting": "github",
        "title": "feat(#42): add new feature",
    }
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", side_effect=values.get),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template body"),
    ):
        snapshot = pull_request_create._build_create_request_snapshot(
            source_branch="feature",
        )

    assert snapshot["title"] == "feat(#42): add new feature"


def test_build_create_request_snapshot_preserves_explicit_formatted_title() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template body"),
    ):
        snapshot = pull_request_create._build_create_request_snapshot(
            provider="github",
            source_branch="feature",
            title="feat(#42): add new feature",
        )

    assert snapshot["title"] == "feat(#42): add new feature"


def test_build_create_request_snapshot_renders_azure_title_template() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.get_repo_root", return_value=None),
        patch(
            "agentic_devtools.cli.pull_request_create.load_platform_config",
            return_value={"code_hosting": "azure_devops"},
        ),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_title", return_value="Rendered title") as render,
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template body"),
    ):
        snapshot = pull_request_create._build_create_request_snapshot(
            provider="azure_devops",
            source_branch="feature",
            title="Input title",
        )

    render.assert_called_once_with("Input title")
    assert snapshot["title"] == "Rendered title"


def test_build_create_request_snapshot_defaults_other_to_azure_devops() -> None:
    values = {
        "platform.code_hosting": "other",
        "source_branch": "feature",
        "title": "Title",
    }
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", side_effect=values.get),
        patch("agentic_devtools.cli.pull_request_create.get_repo_root", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.load_platform_config", return_value={"code_hosting": "other"}),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template body"),
    ):
        snapshot = pull_request_create._build_create_request_snapshot()

    assert snapshot["provider"] == "azure_devops"


def test_build_create_request_snapshot_rejects_empty_list_reviewer() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template body"),
    ):
        with pytest.raises(ValueError, match="reviewers must be a list/tuple of non-empty strings"):
            pull_request_create._build_create_request_snapshot(
                provider="github",
                source_branch="feature",
                title="Title",
                reviewers=["alice", ""],
            )


@pytest.mark.parametrize("reviewers", [",", " , , ", [], [","]])
def test_build_create_request_snapshot_rejects_reviewers_without_names(reviewers: object) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template body"),
    ):
        with pytest.raises(ValueError, match="reviewers must include at least one non-empty name"):
            pull_request_create._build_create_request_snapshot(
                provider="github",
                source_branch="feature",
                title="Title",
                reviewers=reviewers,  # type: ignore[arg-type]
            )


def test_build_create_request_snapshot_rejects_non_string_list_reviewer() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template body"),
    ):
        with pytest.raises(
            ValueError, match="reviewers must be a comma-separated string or a list/tuple of non-empty strings"
        ):
            pull_request_create._build_create_request_snapshot(
                provider="github",
                source_branch="feature",
                title="Title",
                reviewers=["alice", 7],  # type: ignore[list-item]
            )


def test_build_create_request_snapshot_requires_source_branch() -> None:
    with patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None):
        with pytest.raises(ValueError, match="source_branch is required"):
            pull_request_create._build_create_request_snapshot(provider="github", title="Title")


def test_build_create_request_snapshot_rejects_non_bool_explicit_draft() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template body"),
    ):
        with pytest.raises(ValueError, match="draft must be a boolean"):
            pull_request_create._build_create_request_snapshot(
                provider="github",
                source_branch="feature",
                title="Title",
                draft="false",  # type: ignore[arg-type]
            )


def test_build_create_request_snapshot_accepts_bool_explicit_draft() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template body"),
    ):
        snapshot = pull_request_create._build_create_request_snapshot(
            provider="github",
            source_branch="feature",
            title="Title",
            draft=False,
        )

    assert snapshot["draft"] is False
