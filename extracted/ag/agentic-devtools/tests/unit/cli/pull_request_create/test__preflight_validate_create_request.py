from unittest.mock import patch

import pytest

from agentic_devtools.cli import pull_request_create


def _state(source_branch: object = "feature", title: object = "Title") -> dict:
    return {"source_branch": source_branch, "title": title}


def test_preflight_accepts_valid_explicit_fields() -> None:
    with patch.object(pull_request_create, "resolve_create_provider") as resolve_provider:
        pull_request_create._preflight_validate_create_request(
            provider="github",
            source_branch="feature",
            title="Title",
            body="Body",
            target_branch="main",
            draft=True,
            reviewers=["alice"],
            dry_run=False,
        )

    resolve_provider.assert_called_once_with("github")


def test_preflight_does_not_render_body_template() -> None:
    """Body template rendering must not happen during preflight validation."""
    with (
        patch.object(pull_request_create, "resolve_create_provider"),
        patch.object(pull_request_create, "resolve_pr_body") as resolve_body,
    ):
        pull_request_create._preflight_validate_create_request(source_branch="feature", title="Title")

    resolve_body.assert_not_called()


def test_preflight_falls_back_to_state_for_source_branch_and_title() -> None:
    with (
        patch.object(pull_request_create, "resolve_create_provider"),
        patch.object(pull_request_create, "get_value", side_effect=lambda key: _state().get(key)),
    ):
        pull_request_create._preflight_validate_create_request()


def test_preflight_rejects_invalid_provider() -> None:
    with pytest.raises(ValueError, match="--provider"):
        pull_request_create._preflight_validate_create_request(provider="gitlab", source_branch="feature", title="T")


@pytest.mark.parametrize("source_branch", [None, "", "   "])
def test_preflight_requires_source_branch(source_branch: object) -> None:
    with (
        patch.object(pull_request_create, "resolve_create_provider"),
        patch.object(pull_request_create, "get_value", return_value=None),
    ):
        with pytest.raises(ValueError, match="source_branch is required"):
            pull_request_create._preflight_validate_create_request(
                source_branch=source_branch,  # type: ignore[arg-type]
                title="Title",
            )


@pytest.mark.parametrize("title", [None, "", "   "])
def test_preflight_requires_title(title: object) -> None:
    with (
        patch.object(pull_request_create, "resolve_create_provider"),
        patch.object(pull_request_create, "get_value", return_value=None),
    ):
        with pytest.raises(ValueError, match="title is required"):
            pull_request_create._preflight_validate_create_request(
                source_branch="feature",
                title=title,  # type: ignore[arg-type]
            )


def test_preflight_rejects_non_string_body() -> None:
    with patch.object(pull_request_create, "resolve_create_provider"):
        with pytest.raises(ValueError, match="body must be a string"):
            pull_request_create._preflight_validate_create_request(
                source_branch="feature",
                title="Title",
                body=123,  # type: ignore[arg-type]
            )


@pytest.mark.parametrize("target_branch", ["", "   ", 5])
def test_preflight_rejects_invalid_target_branch(target_branch: object) -> None:
    with patch.object(pull_request_create, "resolve_create_provider"):
        with pytest.raises(ValueError, match="target_branch is required"):
            pull_request_create._preflight_validate_create_request(
                source_branch="feature",
                title="Title",
                target_branch=target_branch,  # type: ignore[arg-type]
            )


def test_preflight_accepts_empty_target_branch_from_state() -> None:
    state = {"source_branch": "feature", "title": "Title", "target_branch": ""}
    with (
        patch.object(pull_request_create, "resolve_create_provider"),
        patch.object(pull_request_create, "get_value", side_effect=lambda key: state.get(key)),
    ):
        pull_request_create._preflight_validate_create_request()


def test_preflight_rejects_non_bool_draft() -> None:
    with patch.object(pull_request_create, "resolve_create_provider"):
        with pytest.raises(ValueError, match="draft must be a boolean"):
            pull_request_create._preflight_validate_create_request(
                source_branch="feature",
                title="Title",
                draft="yes",  # type: ignore[arg-type]
            )


@pytest.mark.parametrize("reviewers", [1, 1.5, {"a"}])
def test_preflight_rejects_invalid_reviewers_type(reviewers: object) -> None:
    with patch.object(pull_request_create, "resolve_create_provider"):
        with pytest.raises(
            ValueError, match="reviewers must be a comma-separated string or a list/tuple of non-empty strings"
        ):
            pull_request_create._preflight_validate_create_request(
                source_branch="feature",
                title="Title",
                reviewers=reviewers,  # type: ignore[arg-type]
            )


@pytest.mark.parametrize("reviewers", [",", " , , ", [], [","]])
def test_preflight_rejects_reviewers_without_names(reviewers: object) -> None:
    with patch.object(pull_request_create, "resolve_create_provider"):
        with pytest.raises(ValueError, match="reviewers must include at least one non-empty name"):
            pull_request_create._preflight_validate_create_request(
                source_branch="feature",
                title="Title",
                reviewers=reviewers,  # type: ignore[arg-type]
            )


def test_preflight_rejects_non_string_body_from_state() -> None:
    """An invalid `description` already in state must be caught here, not just an explicit override."""
    state = {"source_branch": "feature", "title": "Title", "description": 123}
    with (
        patch.object(pull_request_create, "resolve_create_provider"),
        patch.object(pull_request_create, "get_value", side_effect=lambda key: state.get(key)),
    ):
        with pytest.raises(ValueError, match="body must be a string"):
            pull_request_create._preflight_validate_create_request()


@pytest.mark.parametrize("target_branch", ["   ", 5])
def test_preflight_rejects_invalid_target_branch_from_state(target_branch: object) -> None:
    """An invalid `target_branch` already in state must be caught here, not just an explicit override."""
    state = {"source_branch": "feature", "title": "Title", "target_branch": target_branch}
    with (
        patch.object(pull_request_create, "resolve_create_provider"),
        patch.object(pull_request_create, "get_value", side_effect=lambda key: state.get(key)),
    ):
        with pytest.raises(ValueError, match="target_branch is required"):
            pull_request_create._preflight_validate_create_request()


@pytest.mark.parametrize("reviewers", [1, 1.5, {"a"}])
def test_preflight_rejects_invalid_reviewers_type_from_state(reviewers: object) -> None:
    """Invalid `reviewers` already in state must be caught here, not just an explicit override."""
    state = {"source_branch": "feature", "title": "Title", "reviewers": reviewers}
    with (
        patch.object(pull_request_create, "resolve_create_provider"),
        patch.object(pull_request_create, "get_value", side_effect=lambda key: state.get(key)),
    ):
        with pytest.raises(
            ValueError, match="reviewers must be a comma-separated string or a list/tuple of non-empty strings"
        ):
            pull_request_create._preflight_validate_create_request()


@pytest.mark.parametrize("reviewers", [(1,), ("",), ("   ",), ("alice", 2)])
def test_preflight_rejects_invalid_reviewers_tuple_members(reviewers: object) -> None:
    """A tuple with non-string/empty members must fail synchronously, not inside the background task."""
    with patch.object(pull_request_create, "resolve_create_provider"):
        with pytest.raises(ValueError, match="reviewers must be a list/tuple of non-empty strings"):
            pull_request_create._preflight_validate_create_request(
                source_branch="feature",
                title="Title",
                reviewers=reviewers,  # type: ignore[arg-type]
            )


@pytest.mark.parametrize("reviewers", [(1,), ("",), ("   ",)])
def test_preflight_rejects_invalid_reviewers_tuple_members_from_state(reviewers: object) -> None:
    """An invalid `reviewers` tuple already in state must be caught here, not just an explicit override."""
    state = {"source_branch": "feature", "title": "Title", "reviewers": reviewers}
    with (
        patch.object(pull_request_create, "resolve_create_provider"),
        patch.object(pull_request_create, "get_value", side_effect=lambda key: state.get(key)),
    ):
        with pytest.raises(ValueError, match="reviewers must be a list/tuple of non-empty strings"):
            pull_request_create._preflight_validate_create_request()


def test_preflight_rejects_non_bool_dry_run() -> None:
    with patch.object(pull_request_create, "resolve_create_provider"):
        with pytest.raises(ValueError, match="dry_run must be a boolean"):
            pull_request_create._preflight_validate_create_request(
                source_branch="feature",
                title="Title",
                dry_run="yes",  # type: ignore[arg-type]
            )
