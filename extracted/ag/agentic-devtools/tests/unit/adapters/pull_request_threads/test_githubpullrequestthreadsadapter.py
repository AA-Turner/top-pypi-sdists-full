import subprocess
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

import pytest

from agentic_devtools.adapters.pull_request_threads import (
    GitHubPullRequestThreadsAdapter,
    PullRequestThreadsRequest,
)
from agentic_devtools.cli.ci.credential_roles import DEFAULT_CLASSIC_REPO_WORKFLOW_PAT


@pytest.fixture(autouse=True)
def default_github_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(DEFAULT_CLASSIC_REPO_WORKFLOW_PAT, "default-token")


def test_fetches_and_groups_paginated_comments(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(DEFAULT_CLASSIC_REPO_WORKFLOW_PAT, "default-token")
    calls: list[dict[str, Any]] = []
    commands: list[list[str]] = []
    responses = iter(
        [
            SimpleNamespace(
                returncode=0,
                stdout=(
                    '[[{"id": 9223372036854775808, "path": "a.py", "line": 3, "body": "root", '
                    '"user": {"login": "a"}}, '
                    '{"id": 9223372036854775809, "in_reply_to_id": 9223372036854775808, '
                    '"body": "reply", "user": {"login": "b"}}]]'
                ),
                stderr="",
            ),
            SimpleNamespace(
                returncode=0,
                stdout='{"data":{"repository":{"pullRequest":{"reviewThreads":{"pageInfo":{"hasNextPage":false,"endCursor":null},"nodes":[{"id":"PRRT_node","isResolved":true,"comments":{"pageInfo":{"hasNextPage":false,"endCursor":null},"nodes":[{"fullDatabaseId":"9223372036854775808"},{"fullDatabaseId":"9223372036854775809"}]}}]}}}}}',
                stderr="",
            ),
        ]
    )

    def run_command(*args, **kwargs):
        calls.append(kwargs)
        commands.append(args[0])
        return next(responses)

    result = GitHubPullRequestThreadsAdapter(run_command).list(PullRequestThreadsRequest("github", "owner/repo", 4))
    assert result[0].id == "9223372036854775808"
    assert len(result[0].comments) == 2
    assert result[0].status == "resolved"
    assert len(calls) == 2
    assert all(call["env"]["GH_TOKEN"] == "default-token" for call in calls)
    assert any("fullDatabaseId" in argument for argument in commands[1])


def test_fetches_additional_thread_comment_pages_for_status_mapping() -> None:
    responses = iter(
        [
            SimpleNamespace(
                returncode=0,
                stdout=(
                    '[[{"id": 1, "path": "a.py", "line": 3, "body": "root"}, '
                    '{"id": 2, "in_reply_to_id": 1, "body": "reply"}]]'
                ),
                stderr="",
            ),
            SimpleNamespace(
                returncode=0,
                stdout='{"data":{"repository":{"pullRequest":{"reviewThreads":{"pageInfo":{"hasNextPage":false,"endCursor":null},"nodes":[{"id":"PRRT_node","isResolved":false,"comments":{"pageInfo":{"hasNextPage":true,"endCursor":"cursor-1"},"nodes":[{"fullDatabaseId":1}]}}]}}}}}',
                stderr="",
            ),
            SimpleNamespace(
                returncode=0,
                stdout='{"data":{"node":{"comments":{"pageInfo":{"hasNextPage":false,"endCursor":null},"nodes":[{"fullDatabaseId":"2"}]}}}}',
                stderr="",
            ),
        ]
    )
    result = GitHubPullRequestThreadsAdapter(lambda *args, **kwargs: next(responses)).list(
        PullRequestThreadsRequest("github", "owner/repo", 4)
    )
    assert result[0].status == "active"


def test_reports_gh_failure() -> None:
    response = SimpleNamespace(returncode=1, stdout="", stderr="denied")
    with pytest.raises(RuntimeError, match="denied"):
        GitHubPullRequestThreadsAdapter(lambda *args, **kwargs: response).list(
            PullRequestThreadsRequest("github", "owner/repo", 4)
        )


def test_retries_rate_limited_gh_calls_using_retry_after() -> None:
    responses = iter(
        [
            SimpleNamespace(returncode=1, stdout="", stderr="HTTP 429: rate limited\nRetry-After: 2"),
            SimpleNamespace(returncode=0, stdout="[]", stderr=""),
        ]
    )
    calls = []

    def run_command(*args, **kwargs):
        calls.append(args)
        return next(responses)

    adapter = GitHubPullRequestThreadsAdapter(run_command)

    with patch("agentic_devtools.adapters.pull_request_threads.time.sleep") as sleep:
        result = adapter._run_gh(["gh", "api", "graphql"])

    assert result.returncode == 0
    assert len(calls) == 2
    sleep.assert_called_once_with(2.0)


def test_retries_bare_transient_gh_status_using_retry_after() -> None:
    responses = iter(
        [
            SimpleNamespace(returncode=1, stdout="", stderr="503 service unavailable\nRetry-After: 2"),
            SimpleNamespace(returncode=0, stdout="[]", stderr=""),
        ]
    )
    calls = []

    def run_command(*args, **kwargs):
        calls.append(args)
        return next(responses)

    adapter = GitHubPullRequestThreadsAdapter(run_command)

    with patch("agentic_devtools.adapters.pull_request_threads.time.sleep") as sleep:
        result = adapter._run_gh(["gh", "api", "graphql"])

    assert result.returncode == 0
    assert len(calls) == 2
    sleep.assert_called_once_with(2.0)


@pytest.mark.parametrize(
    "error",
    [
        "HTTP 500: internal server error",
        "HTTP/2.0 504: gateway timeout",
        "500 internal server error",
        "504 gateway timeout",
    ],
)
def test_retries_thread_listing_server_errors(error: str) -> None:
    responses = iter(
        [
            SimpleNamespace(returncode=1, stdout="", stderr=error),
            SimpleNamespace(returncode=0, stdout="[]", stderr=""),
        ]
    )
    adapter = GitHubPullRequestThreadsAdapter(lambda *args, **kwargs: next(responses))

    with patch("agentic_devtools.adapters.pull_request_threads.time.sleep") as sleep:
        result = adapter._run_gh(["gh", "api", "graphql"])

    assert result.returncode == 0
    sleep.assert_called_once_with(1.0)


def test_retries_timed_out_gh_calls_with_a_bounded_attempt_count() -> None:
    calls = []

    def run_command(*args, **kwargs):
        calls.append(args)
        if len(calls) == 1:
            raise subprocess.TimeoutExpired(args[0], timeout=kwargs["timeout"])
        return SimpleNamespace(returncode=0, stdout="[]", stderr="")

    adapter = GitHubPullRequestThreadsAdapter(run_command)
    with patch("agentic_devtools.adapters.pull_request_threads.time.sleep") as sleep:
        result = adapter._run_gh(["gh", "api", "graphql"])

    assert result.returncode == 0
    assert len(calls) == 2
    sleep.assert_called_once_with(1.0)


def test_reraises_timeout_after_retry_limit() -> None:
    calls = []

    def run_command(*args, **kwargs):
        calls.append(args)
        raise subprocess.TimeoutExpired(args[0], timeout=kwargs["timeout"])

    adapter = GitHubPullRequestThreadsAdapter(run_command)
    with (
        patch("agentic_devtools.adapters.pull_request_threads.time.sleep") as sleep,
        pytest.raises(subprocess.TimeoutExpired),
    ):
        adapter._run_gh(["gh", "api", "graphql"])

    assert len(calls) == 4
    assert [call.args[0] for call in sleep.call_args_list] == [1.0, 2.0, 4.0]


def test_reraises_timeout_when_retry_wait_budget_is_exhausted() -> None:
    calls = []

    def run_command(*args, **kwargs):
        calls.append(args)
        if len(calls) == 1:
            return SimpleNamespace(returncode=1, stdout="", stderr="HTTP 429: rate limited\nRetry-After: 15")
        raise subprocess.TimeoutExpired(args[0], timeout=kwargs["timeout"])

    adapter = GitHubPullRequestThreadsAdapter(run_command)
    with (
        patch("agentic_devtools.adapters.pull_request_threads.time.sleep") as sleep,
        pytest.raises(subprocess.TimeoutExpired),
    ):
        adapter._run_gh(["gh", "api", "graphql"])

    assert len(calls) == 2
    sleep.assert_called_once_with(15.0)


def test_uses_backoff_when_retry_after_header_is_invalid() -> None:
    responses = iter(
        [
            SimpleNamespace(returncode=1, stdout="", stderr="HTTP 503: unavailable\nRetry-After: invalid"),
            SimpleNamespace(returncode=0, stdout="[]", stderr=""),
        ]
    )
    adapter = GitHubPullRequestThreadsAdapter(lambda *args, **kwargs: next(responses))

    with patch("agentic_devtools.adapters.pull_request_threads.time.sleep") as sleep:
        result = adapter._run_gh(["gh", "api", "graphql"])

    assert result.returncode == 0
    sleep.assert_called_once_with(1.0)


def test_stops_retrying_when_retry_wait_budget_is_exhausted() -> None:
    responses = iter(
        [
            SimpleNamespace(returncode=1, stdout="", stderr="HTTP 429: rate limited\nRetry-After: 15"),
            SimpleNamespace(returncode=1, stdout="", stderr="HTTP 503: unavailable"),
        ]
    )
    calls = []

    def run_command(*args, **kwargs):
        calls.append(args)
        return next(responses)

    adapter = GitHubPullRequestThreadsAdapter(run_command)

    with patch("agentic_devtools.adapters.pull_request_threads.time.sleep") as sleep:
        result = adapter._run_gh(["gh", "api", "graphql"])

    assert result.returncode == 1
    assert len(calls) == 2
    sleep.assert_called_once_with(15.0)


def test_does_not_retry_non_transient_gh_failures() -> None:
    calls = []

    def run_command(*args, **kwargs):
        calls.append(args)
        return SimpleNamespace(returncode=1, stdout="", stderr="HTTP 403: forbidden")

    adapter = GitHubPullRequestThreadsAdapter(run_command)

    with patch("agentic_devtools.adapters.pull_request_threads.time.sleep") as sleep:
        result = adapter._run_gh(["gh", "api", "graphql"])

    assert result.returncode == 1
    assert len(calls) == 1
    sleep.assert_not_called()


def test_returns_last_gh_response_after_retry_limit() -> None:
    calls = []

    def run_command(*args, **kwargs):
        calls.append(args)
        return SimpleNamespace(returncode=1, stdout="", stderr="HTTP 503: unavailable")

    adapter = GitHubPullRequestThreadsAdapter(run_command)

    with patch("agentic_devtools.adapters.pull_request_threads.time.sleep") as sleep:
        result = adapter._run_gh(["gh", "api", "graphql"])

    assert result.returncode == 1
    assert len(calls) == 4
    assert [call.args[0] for call in sleep.call_args_list] == [1.0, 2.0, 4.0]


@pytest.mark.parametrize(
    "stdout",
    ["{}", "[1]", '[{"id": "bad"}]'],
)
def test_rejects_malformed_gh_payload(stdout: str) -> None:
    response = SimpleNamespace(returncode=0, stdout=stdout, stderr="")
    with pytest.raises(ValueError):
        GitHubPullRequestThreadsAdapter(lambda *args, **kwargs: response).list(
            PullRequestThreadsRequest("github", "owner/repo", 4)
        )


def test_rejects_malformed_review_thread_payload() -> None:
    responses = iter(
        [
            SimpleNamespace(
                returncode=0,
                stdout='[[{"id": 1, "path": "a.py", "line": 3, "body": "root"}]]',
                stderr="",
            ),
            SimpleNamespace(
                returncode=0,
                stdout='{"data":{"repository":{"pullRequest":{"reviewThreads":{"pageInfo":{"hasNextPage":false,"endCursor":null},"nodes":[{"id":"PRRT_node","isResolved":true,"comments":[]}]}}}}}',
                stderr="",
            ),
        ]
    )
    with pytest.raises(ValueError, match="reviewThreads"):
        GitHubPullRequestThreadsAdapter(lambda *args, **kwargs: next(responses)).list(
            PullRequestThreadsRequest("github", "owner/repo", 4)
        )


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ('{"data":{"repository":{"pullRequest":{"reviewThreads":{"nodes":{}}}}}}', "reviewThreads"),
        (
            '{"data":{"repository":{"pullRequest":{"reviewThreads":{"pageInfo":{"hasNextPage":false,"endCursor":null},"nodes":[null]}}}}}',
            "reviewThreads",
        ),
        (
            '{"data":{"repository":{"pullRequest":{"reviewThreads":{"pageInfo":{"hasNextPage":false,"endCursor":null},"nodes":[{"id":"PRRT_node","isResolved":"yes","comments":{"pageInfo":{"hasNextPage":false,"endCursor":null},"nodes":[]}}]}}}}}',
            "reviewThreads",
        ),
        (
            '{"data":{"repository":{"pullRequest":{"reviewThreads":{"pageInfo":{"hasNextPage":false,"endCursor":null},"nodes":[{"id":"PRRT_node","isResolved":true,"comments":[]}]}}}}}',
            "reviewThreads",
        ),
        ('{"data":{"repository":{"pullRequest":{"reviewThreads":{"pageInfo":[],"nodes":[]}}}}}', "reviewThreads"),
        (
            '{"data":{"repository":{"pullRequest":{"reviewThreads":{"pageInfo":{"hasNextPage":"yes","endCursor":null},"nodes":[]}}}}}',
            "reviewThreads",
        ),
        (
            '{"data":{"repository":{"pullRequest":{"reviewThreads":{"pageInfo":{"hasNextPage":true,"endCursor":null},"nodes":[]}}}}}',
            "pagination cursor",
        ),
    ],
)
def test_rejects_malformed_graphql_thread_pages(payload: str, message: str) -> None:
    responses = iter(
        [
            SimpleNamespace(returncode=0, stdout='[[{"id": 1, "path": "a.py", "line": 3, "body": "root"}]]', stderr=""),
            SimpleNamespace(returncode=0, stdout=payload, stderr=""),
        ]
    )
    with pytest.raises(ValueError, match=message):
        GitHubPullRequestThreadsAdapter(lambda *args, **kwargs: next(responses)).list(
            PullRequestThreadsRequest("github", "owner/repo", 4)
        )


def test_rejects_malformed_nested_comment_pages() -> None:
    responses = iter(
        [
            SimpleNamespace(returncode=0, stdout='[[{"id": 1, "path": "a.py", "line": 3, "body": "root"}]]', stderr=""),
            SimpleNamespace(
                returncode=0,
                stdout='{"data":{"repository":{"pullRequest":{"reviewThreads":{"pageInfo":{"hasNextPage":false,"endCursor":null},"nodes":[{"id":"PRRT_node","isResolved":true,"comments":{"pageInfo":{"hasNextPage":true,"endCursor":"cursor-1"},"nodes":[{"fullDatabaseId":1}]}}]}}}}}',
                stderr="",
            ),
            SimpleNamespace(
                returncode=0,
                stdout='{"data":{"node":{"comments":{"pageInfo":{"hasNextPage":"yes","endCursor":null},"nodes":[]}}}}',
                stderr="",
            ),
        ]
    )
    with pytest.raises(ValueError, match="reviewThreads"):
        GitHubPullRequestThreadsAdapter(lambda *args, **kwargs: next(responses)).list(
            PullRequestThreadsRequest("github", "owner/repo", 4)
        )


def test_reports_graphql_command_failure() -> None:
    adapter = GitHubPullRequestThreadsAdapter(
        lambda *args, **kwargs: SimpleNamespace(returncode=1, stdout="", stderr="boom")
    )
    with pytest.raises(RuntimeError, match="boom"):
        adapter._graphql("query {}", {"owner": "owner"})


def test_reports_graphql_errors_with_stable_diagnostic() -> None:
    adapter = GitHubPullRequestThreadsAdapter(
        lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout='{"errors":[{"type":"FORBIDDEN"}]}', stderr="")
    )
    with pytest.raises(RuntimeError, match="forbidden"):
        adapter._graphql("query {}", {"owner": "owner"})


@pytest.mark.parametrize(
    "error",
    [
        '{"type":"RATE_LIMITED"}',
        '{"extensions":{"status":503}}',
    ],
)
def test_retries_transient_graphql_errors(error: str) -> None:
    responses = iter(
        [
            SimpleNamespace(returncode=0, stdout=f'{{"errors":[{error}]}}', stderr=""),
            SimpleNamespace(returncode=0, stdout='{"data":{"ok":true}}', stderr=""),
        ]
    )
    calls = []

    def run_command(*args, **kwargs):
        calls.append(args)
        return next(responses)

    adapter = GitHubPullRequestThreadsAdapter(run_command)

    with patch("agentic_devtools.adapters.pull_request_threads.time.sleep") as sleep:
        payload = adapter._graphql("query {}", {"owner": "owner"})

    assert payload == {"data": {"ok": True}}
    assert len(calls) == 2
    sleep.assert_called_once_with(1.0)


def test_stops_retrying_transient_graphql_errors_after_bounded_attempts() -> None:
    calls = []

    def run_command(*args, **kwargs):
        calls.append(args)
        return SimpleNamespace(returncode=0, stdout='{"errors":[{"type":"RATE_LIMITED"}]}', stderr="")

    adapter = GitHubPullRequestThreadsAdapter(run_command)

    with (
        patch("agentic_devtools.adapters.pull_request_threads.time.sleep") as sleep,
        pytest.raises(RuntimeError, match="rate_limited"),
    ):
        adapter._graphql("query {}", {"owner": "owner"})

    assert len(calls) == 4
    assert [call.args[0] for call in sleep.call_args_list] == [1.0, 2.0, 4.0]


def test_stops_retrying_transient_graphql_errors_when_wait_budget_is_exhausted() -> None:
    calls = []

    def run_command(*args, **kwargs):
        calls.append(args)
        return SimpleNamespace(returncode=0, stdout='{"errors":[{"type":"RATE_LIMITED"}]}', stderr="")

    adapter = GitHubPullRequestThreadsAdapter(run_command)

    with (
        patch("agentic_devtools.adapters.pull_request_threads._GH_API_MAX_RETRY_WAIT_SECONDS", 0.0),
        patch("agentic_devtools.adapters.pull_request_threads.time.sleep") as sleep,
        pytest.raises(RuntimeError, match="rate_limited"),
    ):
        adapter._graphql("query {}", {"owner": "owner"})

    assert len(calls) == 1
    sleep.assert_not_called()


@pytest.mark.parametrize(
    ("stderr", "wait"),
    [
        ("HTTP 403: API rate limit exceeded\nRetry-After: 2", 2.0),
        ("HTTP 403: API rate limit exceeded\nX-RateLimit-Remaining: 0", 1.0),
        ("HTTP 403: API rate limit exceeded", 1.0),
    ],
)
def test_retries_rate_limited_403_responses(stderr: str, wait: float) -> None:
    responses = iter(
        [
            SimpleNamespace(returncode=1, stdout="", stderr=stderr),
            SimpleNamespace(returncode=0, stdout="[]", stderr=""),
        ]
    )
    calls = []

    def run_command(*args, **kwargs):
        calls.append(args)
        return next(responses)

    adapter = GitHubPullRequestThreadsAdapter(run_command)

    with patch("agentic_devtools.adapters.pull_request_threads.time.sleep") as sleep:
        result = adapter._run_gh(["gh", "api", "graphql"])

    assert result.returncode == 0
    assert len(calls) == 2
    sleep.assert_called_once_with(wait)


def test_follows_multiple_review_thread_pages() -> None:
    responses = iter(
        [
            SimpleNamespace(returncode=0, stdout='[[{"id": 1, "path": "a.py", "line": 3, "body": "root"}]]', stderr=""),
            SimpleNamespace(
                returncode=0,
                stdout='{"data":{"repository":{"pullRequest":{"reviewThreads":{"pageInfo":{"hasNextPage":true,"endCursor":"cursor-1"},"nodes":[{"id":"PRRT_node","isResolved":false,"comments":{"pageInfo":{"hasNextPage":false,"endCursor":null},"nodes":[{"fullDatabaseId":99}]}}]}}}}}',
                stderr="",
            ),
            SimpleNamespace(
                returncode=0,
                stdout='{"data":{"repository":{"pullRequest":{"reviewThreads":{"pageInfo":{"hasNextPage":false,"endCursor":null},"nodes":[{"id":"PRRT_node_2","isResolved":true,"comments":{"pageInfo":{"hasNextPage":false,"endCursor":null},"nodes":[{"fullDatabaseId":1}]}}]}}}}}',
                stderr="",
            ),
        ]
    )
    result = GitHubPullRequestThreadsAdapter(lambda *args, **kwargs: next(responses)).list(
        PullRequestThreadsRequest("github", "owner/repo", 4)
    )
    assert result[0].status == "resolved"


def test_rejects_missing_review_threads_connection() -> None:
    adapter = GitHubPullRequestThreadsAdapter()
    with patch.object(adapter, "_graphql", return_value={"data": {"repository": {"pullRequest": {}}}}):
        with pytest.raises(ValueError, match="reviewThreads"):
            adapter._threads_page("owner", "repo", 4, None)


def test_rejects_missing_nested_comments_connection() -> None:
    adapter = GitHubPullRequestThreadsAdapter()
    with patch.object(adapter, "_graphql", return_value={"data": {"node": {}}}):
        with pytest.raises(ValueError, match="reviewThreads"):
            adapter._thread_comments_page("PRRT_node", "cursor-1")


@pytest.mark.parametrize(
    ("comments_page", "message"),
    [
        ({"nodes": {}, "pageInfo": {"hasNextPage": False, "endCursor": None}}, "reviewThreads"),
        ({"nodes": [None], "pageInfo": {"hasNextPage": False, "endCursor": None}}, "reviewThreads"),
        ({"nodes": [{"fullDatabaseId": "bad"}], "pageInfo": {"hasNextPage": False, "endCursor": None}}, "comment id"),
        ({"nodes": [{"fullDatabaseId": True}], "pageInfo": {"hasNextPage": False, "endCursor": None}}, "comment id"),
        ({"nodes": [], "pageInfo": []}, "reviewThreads"),
        ({"nodes": [], "pageInfo": {"hasNextPage": "yes", "endCursor": None}}, "reviewThreads"),
        ({"nodes": [], "pageInfo": {"hasNextPage": True, "endCursor": None}}, "pagination cursor"),
    ],
)
def test_rejects_malformed_thread_comment_pages(comments_page: object, message: str) -> None:
    adapter = GitHubPullRequestThreadsAdapter()
    with pytest.raises(ValueError, match=message):
        adapter._thread_comment_ids("PRRT_node", comments_page)  # type: ignore[arg-type]


def test_rejects_invalid_thread_id_for_comment_pagination() -> None:
    adapter = GitHubPullRequestThreadsAdapter()
    with pytest.raises(ValueError, match="thread id"):
        adapter._thread_comment_ids(
            "bad",
            {"nodes": [], "pageInfo": {"hasNextPage": False, "endCursor": None}},
        )


def test_normalizes_large_full_database_id_strings() -> None:
    adapter = GitHubPullRequestThreadsAdapter()
    assert adapter._thread_comment_ids(
        "PRRT_node",
        {
            "nodes": [{"fullDatabaseId": "9223372036854775808"}],
            "pageInfo": {"hasNextPage": False, "endCursor": None},
        },
    ) == (9223372036854775808,)


def test_rejects_provider_mismatch() -> None:
    with pytest.raises(ValueError, match="provider mismatch"):
        GitHubPullRequestThreadsAdapter(lambda *args, **kwargs: None).list(
            PullRequestThreadsRequest("azure_devops", "repo", 4)
        )


def test_maps_the_discovered_default_role_token_to_gh_token(monkeypatch) -> None:
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "default-token")
    calls = []

    def run_command(*args, **kwargs):
        calls.append(kwargs)
        return SimpleNamespace(returncode=0)

    adapter = GitHubPullRequestThreadsAdapter(run_command)

    adapter._run_gh(["gh", "api", "graphql"])

    assert calls[0]["env"]["GH_TOKEN"] == "default-token"


def test_rejects_missing_default_role_token_before_running_gh(monkeypatch) -> None:
    monkeypatch.delenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", raising=False)
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("AI_PR_LOOP_CREDENTIAL_IDENTITY", raising=False)
    calls = []

    def run_command(*args, **kwargs):
        calls.append(kwargs)
        return SimpleNamespace(returncode=0)

    adapter = GitHubPullRequestThreadsAdapter(run_command)

    with pytest.raises(RuntimeError, match="default-role GitHub token is required"):
        adapter._run_gh(["gh", "api", "graphql"])

    assert calls == []
