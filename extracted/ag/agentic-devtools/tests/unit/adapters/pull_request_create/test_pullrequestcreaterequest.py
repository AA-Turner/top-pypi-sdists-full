from typing import Any

import pytest

from agentic_devtools.adapters.pull_request_create import PullRequestCreateRequest


def test_pull_request_create_request_validates_provider_and_required_fields() -> None:
    request = PullRequestCreateRequest(
        provider="github",
        source_branch="feature/change",
        title="Change",
        body="Details",
        target_branch="main",
        draft=True,
        reviewers=("octocat",),
    )

    assert request.provider == "github"
    assert request.reviewers == ("octocat",)


def test_pull_request_create_request_normalizes_padded_whitespace() -> None:
    request = PullRequestCreateRequest(
        provider="github",
        source_branch=" feature/change ",
        title=" Change ",
        target_branch=" main ",
        reviewers=(" octocat ", "hubot "),
    )

    assert request.source_branch == "feature/change"
    assert request.title == "Change"
    assert request.target_branch == "main"
    assert request.reviewers == ("octocat", "hubot")


@pytest.mark.parametrize(
    "kwargs",
    [
        {"provider": "gitlab", "source_branch": "feature", "title": "Title"},
        {"provider": "github", "source_branch": "", "title": "Title"},
        {"provider": "github", "source_branch": "feature", "title": ""},
        {"provider": "github", "source_branch": "feature", "title": "Title", "draft": "yes"},
        {"provider": "github", "source_branch": "feature", "title": "Title", "body": None},
        {"provider": "github", "source_branch": "feature", "title": "Title", "target_branch": ""},
        {"provider": "github", "source_branch": "feature", "title": "Title", "draft": "yes"},
        {"provider": "github", "source_branch": "feature", "title": "Title", "reviewers": ("",)},
        {"provider": "github", "source_branch": "feature", "title": "Title", "dry_run": "yes"},
        {"provider": "github", "source_branch": "feature", "title": "Title", "body_is_explicit": "yes"},
    ],
)
def test_pull_request_create_request_rejects_invalid_values(kwargs: dict[str, Any]) -> None:
    with pytest.raises(ValueError):
        PullRequestCreateRequest(**kwargs)


def test_pull_request_create_request_normalizes_padded_fields() -> None:
    request = PullRequestCreateRequest(
        provider="github",
        source_branch=" feature ",
        title=" Title ",
        body=" Body with padding ",
        target_branch=" main ",
        reviewers=(" alice ", "bob "),
    )

    assert request.source_branch == "feature"
    assert request.title == "Title"
    assert request.target_branch == "main"
    assert request.reviewers == ("alice", "bob")
    # The body is user-facing content, not an identifier, so it is left untouched.
    assert request.body == " Body with padding "


def test_pull_request_create_request_allows_empty_reviewers_for_azure_devops() -> None:
    request = PullRequestCreateRequest(
        provider="azure_devops",
        source_branch="feature",
        title="Title",
        reviewers=(),
    )

    assert request.reviewers == ()
