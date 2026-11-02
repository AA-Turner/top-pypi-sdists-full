from __future__ import annotations

import pytest

from agentic_devtools.adapters.pull_request_draft import PullRequestDraftRequest


def test_accepts_valid_request() -> None:
    request = PullRequestDraftRequest("github", "owner/repo", 42)
    assert request.provider == "github"
    assert request.dry_run is False


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"provider": "jira"}, "provider"),
        ({"provider": ["github"]}, "provider"),
        ({"provider": {"name": "github"}}, "provider"),
        ({"repository": ""}, "repository"),
        ({"repository": "owner/repo/extra"}, "repository"),
        ({"pull_request_id": 0}, "pull_request_id"),
        ({"pull_request_id": True}, "pull_request_id"),
        ({"dry_run": "true"}, "dry_run"),
        ({"organization": ""}, "organization"),
        ({"project": ""}, "project"),
    ],
)
def test_rejects_invalid_values(kwargs: dict[str, object], message: str) -> None:
    values: dict[str, object] = {
        "provider": "github",
        "repository": "owner/repo",
        "pull_request_id": 42,
    }
    values.update(kwargs)
    with pytest.raises(ValueError, match=message):
        PullRequestDraftRequest(**values)  # type: ignore[arg-type]
