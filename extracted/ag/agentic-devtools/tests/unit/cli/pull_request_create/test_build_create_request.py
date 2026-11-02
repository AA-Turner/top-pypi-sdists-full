from unittest.mock import patch

import pytest

from agentic_devtools.cli import pull_request_create


def test_build_create_request_reads_github_state() -> None:
    values = {
        "platform.code_hosting": "github",
        "source_branch": "feature",
        "title": "Title",
        "description": "Body",
        "target_branch": "develop",
        "draft": "false",
        "reviewers": "alice,bob",
    }
    with patch("agentic_devtools.cli.pull_request_create.get_value", side_effect=values.get):
        request = pull_request_create.build_create_request()

    assert request.provider == "github"
    assert request.body == "Body"
    assert request.draft is False
    assert request.reviewers == ("alice", "bob")


def test_build_create_request_supports_explicit_values_and_template_body() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template"),
        patch("agentic_devtools.cli.pull_request_create.is_dry_run", return_value=True),
    ):
        request = pull_request_create.build_create_request(
            provider="github",
            source_branch="feature",
            title="Title",
            target_branch="develop",
            reviewers=["alice"],
        )

    assert request.body == "Template"
    assert request.body_is_explicit is False
    assert request.target_branch == "develop"
    assert request.dry_run is True


def test_build_create_request_marks_explicit_body() -> None:
    with patch(
        "agentic_devtools.cli.pull_request_create.get_value",
        side_effect=lambda key: "github" if key == "platform.code_hosting" else None,
    ):
        request = pull_request_create.build_create_request(source_branch="feature", title="Title", body="Body")

    assert request.body == "Body"
    assert request.body_is_explicit is True


def test_build_create_request_defaults_reviewers_and_target() -> None:
    with patch(
        "agentic_devtools.cli.pull_request_create.get_value",
        side_effect=lambda key: "github" if key == "platform.code_hosting" else None,
    ):
        request = pull_request_create.build_create_request(source_branch="feature", title="Title")

    assert request.reviewers == ()
    assert request.target_branch == "main"


def test_build_create_request_rejects_invalid_reviewers() -> None:
    with patch(
        "agentic_devtools.cli.pull_request_create.get_value",
        side_effect=lambda key: "github" if key == "platform.code_hosting" else None,
    ):
        with pytest.raises(ValueError, match="reviewers"):
            pull_request_create.build_create_request(
                source_branch="feature",
                title="Title",
                reviewers={"alice"},  # type: ignore[arg-type]
            )


@pytest.mark.parametrize(
    ("description", "target_branch", "message"),
    [([], "main", "body must be a string"), ("Body", 7, "target_branch must be a string")],
)
def test_build_create_request_rejects_invalid_state_types(
    description: object,
    target_branch: object,
    message: str,
) -> None:
    values = {
        "platform.code_hosting": "github",
        "source_branch": "feature",
        "title": "Title",
        "description": description,
        "target_branch": target_branch,
    }
    with patch("agentic_devtools.cli.pull_request_create.get_value", side_effect=values.get):
        with pytest.raises(ValueError, match=message):
            pull_request_create.build_create_request()


def test_build_create_request_preserves_formatted_state_title() -> None:
    """A formatted state title remains final instead of being prefixed again."""
    values = {
        "platform.code_hosting": "github",
        "title": "feat(#42): add new feature",
    }
    with patch("agentic_devtools.cli.pull_request_create.get_value", side_effect=values.get):
        request = pull_request_create.build_create_request(source_branch="feature")

    assert request.title == "feat(#42): add new feature"


def test_build_create_request_preserves_explicit_formatted_title() -> None:
    """An explicit full PR title is not rendered as a title-template summary."""
    with patch(
        "agentic_devtools.cli.pull_request_create.get_value",
        side_effect=lambda key: "github" if key == "platform.code_hosting" else None,
    ):
        request = pull_request_create.build_create_request(
            source_branch="feature",
            title="feat(#42): add new feature",
        )

    assert request.title == "feat(#42): add new feature"


def test_build_create_request_strips_markdown_links_from_formatted_titles() -> None:
    """GitHub titles must be link-stripped like Azure DevOps."""
    raw_title = "feature([PROJECT-1234](https://jira.example/browse/PROJECT-1234)): add feature"
    with (
        patch(
            "agentic_devtools.cli.pull_request_create.get_value",
            side_effect=lambda key: "github" if key == "platform.code_hosting" else None,
        ),
    ):
        request = pull_request_create.build_create_request(source_branch="feature", title=raw_title)

    assert request.title == "feature(PROJECT-1234): add feature"


def test_build_create_request_rejects_blank_title() -> None:
    """An empty/whitespace title fails validation."""
    with patch(
        "agentic_devtools.cli.pull_request_create.get_value",
        side_effect=lambda key: "github" if key == "platform.code_hosting" else None,
    ):
        with pytest.raises(ValueError, match="title"):
            pull_request_create.build_create_request(source_branch="feature", title="   ")
