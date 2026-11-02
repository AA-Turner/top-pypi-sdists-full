from unittest.mock import patch

import pytest

from agentic_devtools.adapters.pull_request_details import _github_details


@pytest.mark.parametrize(
    ("raw_login", "expected_login"),
    [("octocat", "octocat"), (None, ""), (123, ""), ({"name": "octocat"}, "")],
)
@pytest.mark.parametrize(
    ("thread_id", "expected_github_thread_node_id"),
    [("thread-1", "thread-1"), ("__agdt-thread-1", None)],
)
def test_github_details_normalizes_files_threads_and_commit_shape(
    raw_login, expected_login, thread_id, expected_github_thread_node_id
) -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [
                type(
                    "Comment",
                    (),
                    {
                        "id": 10,
                        "body": "body",
                        "path": "src/x.py",
                        "line": 7,
                        "start_line": 7,
                        "commit_id": "headsha",
                        "original_commit_id": "basesha",
                        "author_login": "octocat",
                        "html_url": "https://github.com/owner/repo/pull/4#discussion_r10",
                        "in_reply_to_id": 9,
                        "created_at": "2026-10-07T15:00:00Z",
                    },
                )()
            ],
            "list_issue_comments": lambda self, number: [
                type(
                    "IssueComment",
                    (),
                    {
                        "id": 12,
                        "body": "conversation comment",
                        "author": "reviewer",
                        "created_at": "2026-10-07T16:00:00Z",
                        "html_url": "https://github.com/owner/repo/pull/4#issuecomment-12",
                    },
                )()
            ],
            "list_review_threads_by_thread_id": lambda self, number: {thread_id: (False, (10,))},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[
                {
                    "number": 4,
                    "title": "Example",
                    "draft": True,
                    "state": "open",
                    "html_url": "https://github.com/owner/repo/pull/4",
                    "head": {"ref": "feature", "sha": "headsha"},
                    "base": {"ref": "main", "sha": "basesha"},
                    "user": {"login": raw_login},
                },
                [{"sha": "headsha"}],
                [
                    {
                        "filename": "src/x.py",
                        "status": "renamed",
                        "additions": 3,
                        "deletions": 1,
                        "previous_filename": "src/old.py",
                    }
                ],
                {"head": {"sha": "headsha"}},
            ],
        ),
    ):
        payload = _github_details(4, "owner/repo")

    assert payload["pullRequest"]["lastMergeSourceCommit"] == {"commitId": "headsha"}
    assert payload["pullRequest"]["lastMergeTargetCommit"] == {"commitId": "basesha"}
    assert payload["pullRequest"]["url"] == "https://github.com/owner/repo/pull/4"
    assert payload["comparison"] == {
        "baseRef": "basesha",
        "compareRef": "headsha",
        "baseCommit": "basesha",
        "compareCommit": "headsha",
        "baseBranch": "main",
        "compareBranch": "feature",
    }
    assert payload["pullRequest"]["createdBy"] == {
        "displayName": expected_login,
        "uniqueName": expected_login,
    }
    assert payload["files"][0]["path"] == "src/x.py"
    assert payload["files"][0]["originalPath"] == "src/old.py"
    assert payload["files"][0]["changeType"] == "rename"
    assert payload["threads"][0]["comments"][0]["content"] == "body"
    assert payload["threads"][0]["comments"][0]["htmlUrl"] == ("https://github.com/owner/repo/pull/4#discussion_r10")
    assert payload["threads"][0]["comments"][0]["inReplyToId"] == 9
    assert payload["threads"][0]["comments"][0]["createdAt"] == "2026-10-07T15:00:00Z"
    assert payload["threads"][0]["id"] == thread_id
    if expected_github_thread_node_id is None:
        assert "githubThreadNodeId" not in payload["threads"][0]
    else:
        assert payload["threads"][0]["githubThreadNodeId"] == expected_github_thread_node_id
    assert payload["threads"][0]["threadContext"] == {"filePath": "src/x.py"}
    assert payload["threads"][0]["pullRequestThreadContext"] == {"filePath": "src/x.py"}
    assert payload["threads"][1]["comments"][0]["createdAt"] == "2026-10-07T16:00:00Z"
    assert payload["threads"][1]["comments"][0]["htmlUrl"] == ("https://github.com/owner/repo/pull/4#issuecomment-12")
    assert payload["schemaVersion"] == 1
    assert payload["repository"] == {
        "id": "owner/repo",
        "name": "repo",
        "project": {"name": "owner"},
    }
    assert payload["providerData"] == {"repository": "owner/repo"}
    assert payload["iterations"] == {"status": "unsupported", "items": []}
    assert payload["reviewer"]["reviewedFiles"] == {"status": "unsupported", "files": []}
    assert payload["capabilities"]["iterations"] == "unsupported"
    assert payload["capabilities"]["reviewedFiles"] == "unsupported"
    assert len(payload["warnings"]) == 2
    assert payload["diff"] == "diff"
    assert payload["diffComplete"] is True


@pytest.mark.parametrize(
    ("latest_metadata", "expected_message"),
    [
        ({"head": {"sha": "new-head"}}, "head changed while collecting details"),
        ({}, "did not return a valid head SHA"),
        ({"head": {"sha": ""}}, "did not return a valid head SHA"),
        ([], "did not return a valid head SHA"),
    ],
)
def test_github_details_rejects_inconsistent_head_during_collection(latest_metadata, expected_message) -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    metadata = {
        "number": 4,
        "state": "open",
        "head": {"ref": "feature", "sha": "old-head"},
        "base": {"ref": "main", "sha": "base"},
    }
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[metadata, [], [], latest_metadata],
        ),
        pytest.raises(RuntimeError, match=expected_message),
    ):
        _github_details(4, "owner/repo")


@pytest.mark.parametrize("head", [{}, {"sha": None}, {"sha": 123}])
def test_github_details_marks_missing_head_sha_as_partial_data(head) -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: pytest.fail("diff must not be fetched without a head SHA"),
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[
                {"number": 4, "state": "open", "head": head, "base": {"ref": "main", "sha": "base"}},
                [],
                [],
            ],
        ),
    ):
        payload = _github_details(4, "owner/repo")

    assert payload["comparison"]["compareRef"] == ""
    assert payload["comparison"]["compareCommit"] == ""
    assert payload["pullRequest"]["lastMergeSourceCommit"] == {"commitId": ""}
    assert payload["diff"] is None
    assert payload["diffComplete"] is False
    assert any(warning["capability"] == "head" for warning in payload["warnings"])


def test_github_details_skips_unmapped_comments_and_normalizes_added_removed_files() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {"thread-1": (True, (99,))},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[
                {
                    "number": 5,
                    "state": "closed",
                    "merged": True,
                    "merged_at": "2026-09-16T00:00:00Z",
                    "head": {"ref": "feature", "sha": "headsha"},
                    "base": {"ref": "main", "sha": "basesha"},
                },
                [{"sha": "headsha"}],
                [
                    {"filename": "src/added.py", "status": "added", "additions": 2, "deletions": 0},
                    {"filename": "src/removed.py", "status": "removed", "additions": 0, "deletions": 4},
                    {"filename": "src/malformed.py", "status": {"unexpected": "value"}},
                ],
                {"head": {"sha": "headsha"}},
            ],
        ),
    ):
        payload = _github_details(5, "owner/repo")

    assert payload["pullRequest"]["status"] == "completed"
    assert payload["threads"] == []
    assert payload["files"][0]["changeType"] == "add"
    assert payload["files"][1]["changeType"] == "delete"
    assert payload["files"][2]["status"] == ""
    assert payload["files"][2]["changeType"] == "edit"


@pytest.mark.parametrize("file_detail", [None, {}, {"filename": None}, {"filename": 42}])
def test_github_details_rejects_malformed_file_entries(file_detail) -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[
                {"number": 13, "state": "open", "changed_files": 1, "head": {}, "base": {}},
                [],
                [file_detail],
            ],
        ),
        pytest.raises(RuntimeError, match="malformed file entry"),
    ):
        _github_details(13, "owner/repo")


def test_github_details_keeps_comments_without_thread_context_when_path_missing() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [
                type(
                    "Comment",
                    (),
                    {
                        "id": 11,
                        "body": "general",
                        "path": "",
                        "line": None,
                        "start_line": None,
                        "commit_id": "headsha",
                        "original_commit_id": "basesha",
                        "author_login": "octocat",
                    },
                )()
            ],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {"thread-1": (True, (11,))},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[{"number": 5, "state": "open", "head": {}, "base": {}}, [], []],
        ),
    ):
        payload = _github_details(5, "owner/repo")

    assert len(payload["threads"]) == 1
    assert "threadContext" not in payload["threads"][0]["comments"][0]
    assert "threadContext" not in payload["threads"][0]


def test_github_details_maps_closed_unmerged_pull_requests_to_abandoned() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[
                {"number": 6, "state": "closed", "merged": False, "head": {}, "base": {}},
                [],
                [],
            ],
        ),
    ):
        payload = _github_details(6, "owner/repo")

    assert payload["pullRequest"]["status"] == "abandoned"


def test_github_details_requests_commits_and_files_paginated() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[
                {"number": 6, "state": "open", "head": {}, "base": {}},
                [{"sha": "headsha"}],
                [],
            ],
        ) as api_json,
    ):
        payload = _github_details(6, "owner/repo")

    assert payload["commits"] == [{"sha": "headsha"}]
    assert api_json.call_args_list[1].kwargs == {"paginate": True}
    assert api_json.call_args_list[2].kwargs == {"paginate": True}


def test_github_details_propagates_paginated_errors_without_retrying() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[
                {"number": 6, "state": "open", "head": {}, "base": {}},
                RuntimeError("boom"),
            ],
        ) as api_json,
    ):
        with pytest.raises(RuntimeError, match="boom"):
            _github_details(6, "owner/repo")

    assert api_json.call_count == 2


def test_github_details_does_not_treat_merged_at_as_merged_state() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[
                {"number": 7, "state": "closed", "merged_at": "2026-09-16T00:00:00Z", "head": {}, "base": {}},
                [],
                [],
            ],
        ),
    ):
        payload = _github_details(7, "owner/repo")

    assert payload["pullRequest"]["status"] == "abandoned"


def test_github_details_rejects_unknown_pull_request_states() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[{"number": 8, "state": "merged", "head": {}, "base": {}}, [], []],
        ),
    ):
        with pytest.raises(RuntimeError, match="unsupported pull request state"):
            _github_details(8, "owner/repo")


def test_github_details_falls_back_to_requested_pr_number_for_invalid_metadata_number() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[{"number": "6", "state": "open", "head": {}, "base": {}}, [], []],
        ),
    ):
        payload = _github_details(6, "owner/repo")

    assert payload["pullRequest"]["pullRequestId"] == 6
    assert payload["pullRequest"]["number"] == 6
    assert payload["pullRequest"]["createdBy"] == {"displayName": "", "uniqueName": ""}


def test_github_details_rejects_missing_pull_request_state() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[{"number": 9, "head": {}, "base": {}}, [], []],
        ),
    ):
        with pytest.raises(RuntimeError, match="unsupported pull request state"):
            _github_details(9, "owner/repo")


def test_github_details_emits_fallback_thread_for_unthreaded_comment() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [
                type(
                    "Comment",
                    (),
                    {
                        "id": 21,
                        "body": "loose comment",
                        "path": "src/file.py",
                        "line": 4,
                        "start_line": 4,
                        "commit_id": "headsha",
                        "original_commit_id": "basesha",
                        "author_login": "octocat",
                    },
                )()
            ],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[{"number": 10, "state": "open", "head": {}, "base": {}}, [], []],
        ),
    ):
        payload = _github_details(10, "owner/repo")

    assert payload["threads"][0]["id"] == "comment-21"
    assert payload["threads"][0]["comments"][0]["content"] == "loose comment"
    assert payload["threads"][0]["threadContext"] == {"filePath": "src/file.py"}
    assert payload["threads"][0]["pullRequestThreadContext"] == {"filePath": "src/file.py"}


def test_github_details_emits_fallback_thread_without_thread_context_for_pathless_comment() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [
                type(
                    "Comment",
                    (),
                    {
                        "id": 22,
                        "body": "pathless",
                        "path": "",
                        "line": None,
                        "start_line": None,
                        "commit_id": "headsha",
                        "original_commit_id": "basesha",
                        "author_login": "octocat",
                    },
                )()
            ],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[{"number": 11, "state": "open", "head": {}, "base": {}}, [], []],
        ),
    ):
        payload = _github_details(11, "owner/repo")

    assert payload["threads"][0]["id"] == "comment-22"
    assert "threadContext" not in payload["threads"][0]["comments"][0]
    assert "threadContext" not in payload["threads"][0]


def test_github_details_leaves_isbinary_unset_when_patch_absent_and_false_when_present() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[
                {"number": 12, "state": "open", "head": {}, "base": {}},
                [],
                [
                    {"filename": "assets/logo.png", "status": "modified", "additions": 0, "deletions": 0},
                    {"filename": "src/x.py", "status": "modified", "additions": 2, "deletions": 1, "patch": "@@"},
                ],
            ],
        ),
    ):
        payload = _github_details(12, "owner/repo")

    assert payload["files"][0]["path"] == "assets/logo.png"
    assert "isBinary" not in payload["files"][0]
    assert payload["files"][1]["path"] == "src/x.py"
    assert payload["files"][1]["isBinary"] is False


def test_github_details_rejects_non_list_api_responses() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[{"state": "open", "head": {}, "base": {}}, {}, {}],
        ),
    ):
        with pytest.raises(RuntimeError, match="invalid commits response"):
            _github_details(1, "o/r")

    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[{"state": "open", "head": {}, "base": {}}, [], {}],
        ),
    ):
        with pytest.raises(RuntimeError, match="invalid files response"):
            _github_details(1, "o/r")

    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[[], [], []],
        ),
    ):
        with pytest.raises(RuntimeError, match="unsupported pull request state"):
            _github_details(1, "o/r")


def test_github_details_maps_body_to_normalized_description() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[
                {"number": 13, "state": "open", "head": {}, "base": {}, "body": "PR description text"},
                [],
                [],
            ],
        ),
    ):
        payload = _github_details(13, "owner/repo")

    assert payload["pullRequest"]["description"] == "PR description text"


def test_github_details_defaults_description_to_empty_string_when_body_missing() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[{"number": 14, "title": None, "state": "open", "head": {}, "base": {}}, [], []],
        ),
    ):
        payload = _github_details(14, "owner/repo")

    assert payload["pullRequest"]["title"] == ""
    assert payload["pullRequest"]["description"] == ""


def test_github_details_populates_added_and_removed_lines_from_patch() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[
                {"number": 15, "state": "open", "head": {}, "base": {}},
                [],
                [
                    {
                        "filename": "src/y.py",
                        "status": "modified",
                        "additions": 1,
                        "deletions": 1,
                        "patch": "@@ -1,2 +1,2 @@\n context\n-old line\n+new line",
                    }
                ],
            ],
        ),
    ):
        payload = _github_details(15, "owner/repo")

    file_detail = payload["files"][0]
    assert file_detail["addedLines"] == [{"line": 2, "content": "new line"}]
    assert file_detail["removedLines"] == [{"line": 2, "content": "old line"}]


def test_github_details_omits_line_anchors_for_truncated_patch() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[
                {"number": 16, "state": "open", "head": {}, "base": {}},
                [],
                [
                    {
                        "filename": "src/y.py",
                        "status": "modified",
                        "additions": 1,
                        "deletions": 0,
                        "patch": "@@ -1 +1 @@\n+new\n...",
                    }
                ],
            ],
        ),
    ):
        payload = _github_details(16, "owner/repo")

    assert "addedLines" not in payload["files"][0]
    assert "removedLines" not in payload["files"][0]


@pytest.mark.parametrize(
    ("additions", "deletions", "patch_content"),
    [
        (2, 1, "@@ -1 +1,2 @@\n-old\n+new"),
        (1, 2, "@@ -1,2 +1 @@\n-old\n+new"),
    ],
)
def test_github_details_omits_line_anchors_when_patch_counts_do_not_match(
    additions: int, deletions: int, patch_content: str
) -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[
                {"number": 18, "state": "open", "head": {}, "base": {}},
                [],
                [
                    {
                        "filename": "src/y.py",
                        "status": "modified",
                        "additions": additions,
                        "deletions": deletions,
                        "patch": patch_content,
                    }
                ],
            ],
        ),
    ):
        payload = _github_details(18, "owner/repo")

    file_detail = payload["files"][0]
    assert file_detail["addedLineCount"] == additions
    assert file_detail["removedLineCount"] == deletions
    assert "addedLines" not in file_detail
    assert "removedLines" not in file_detail


def test_github_details_rejects_malformed_line_counts() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[
                {"number": 17, "state": "open", "head": {}, "base": {}},
                [],
                [
                    {
                        "filename": "src/y.py",
                        "status": "modified",
                        "additions": "1",
                        "deletions": 0,
                    }
                ],
            ],
        ),
    ):
        with pytest.raises(RuntimeError, match="invalid additions/deletions"):
            _github_details(17, "owner/repo")


def test_github_details_includes_issue_comments_as_pathless_threads() -> None:
    issue_comment = type(
        "IssueComment",
        (),
        {"id": 555, "author": "reviewer", "body": "general feedback", "created_at": "2026-01-01T00:00:00Z"},
    )()
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [issue_comment],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[
                {"number": 21, "state": "open", "head": {}, "base": {}},
                [],
                [],
            ],
        ),
    ):
        payload = _github_details(21, "owner/repo")

    assert payload["threads"] == [
        {
            "id": "issue-comment-555",
            "isDeleted": False,
            "status": "active",
            "comments": [
                {
                    "id": 555,
                    "content": "general feedback",
                    "isDeleted": False,
                    "path": None,
                    "createdAt": "2026-01-01T00:00:00Z",
                    "htmlUrl": "",
                    "author": {"displayName": "reviewer", "uniqueName": "reviewer"},
                }
            ],
        }
    ]


def test_github_details_rejects_incomplete_file_list_from_capped_endpoint() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[
                {"number": 30, "state": "open", "head": {}, "base": {}, "changed_files": 3001},
                [],
                [{"filename": f"src/f{i}.py", "status": "modified"} for i in range(3000)],
            ],
        ),
        pytest.raises(RuntimeError, match="refusing to persist an incomplete file list"),
    ):
        _github_details(30, "owner/repo")


def test_github_details_marks_diff_incomplete_when_file_limit_exceeded() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: pytest.fail("must not fetch a capped diff"),
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[
                {"number": 32, "state": "open", "head": {}, "base": {}, "changed_files": 301},
                [],
                [{"filename": f"src/f{i}.py", "status": "modified"} for i in range(301)],
            ],
        ),
    ):
        payload = _github_details(32, "owner/repo")

    assert payload["diff"] is None
    assert payload["diffComplete"] is False


def test_github_details_rejects_incomplete_commit_list_from_capped_endpoint() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with (
        patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider),
        patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[
                {"number": 31, "state": "open", "head": {}, "base": {}, "commits": 251},
                [{"sha": "headsha"}] * 250,
                [],
            ],
        ),
        pytest.raises(RuntimeError, match="incomplete commit list"),
    ):
        _github_details(31, "owner/repo")
