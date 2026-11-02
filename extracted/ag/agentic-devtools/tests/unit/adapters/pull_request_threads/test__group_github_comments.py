import pytest

from agentic_devtools.adapters.pull_request_threads import _group_github_comments


def test_groups_root_and_reply_and_uses_original_line() -> None:
    result = _group_github_comments(
        [{"id": 2, "path": "a.py", "original_line": 5, "body": "x"}],
        resolved_by_comment_id={2: False},
    )
    assert result[0].line == 5
    assert result[0].status == "active"


def test_normalizes_resolved_status_and_malformed_user_to_none() -> None:
    result = _group_github_comments(
        [{"id": 2, "path": "a.py", "line": 5, "body": None, "user": "reviewer"}],
        resolved_by_comment_id={2: True},
    )
    assert result[0].status == "resolved"
    assert result[0].comments == (
        {
            "id": 2,
            "author": None,
            "content": "",
            "pull_request_review_id": None,
            "in_reply_to_id": None,
            "diff_hunk": None,
        },
    )


def test_keeps_searching_for_status_when_root_comment_is_not_in_lookup() -> None:
    result = _group_github_comments(
        [
            {"id": 1, "path": "a.py", "line": 5, "body": "root"},
            {"id": 2, "in_reply_to_id": 1, "body": "reply"},
        ],
        resolved_by_comment_id={2: False},
    )
    assert result[0].status == "active"


def test_prefers_the_root_comment_id_for_thread_location() -> None:
    result = _group_github_comments(
        [
            {"id": 2, "in_reply_to_id": 1, "body": "reply"},
            {"id": 1, "path": "a.py", "line": 5, "body": "root"},
        ],
        resolved_by_comment_id={1: False},
    )
    assert result[0].file == "a.py"
    assert result[0].line == 5


def test_groups_nested_replies_under_the_root_comment() -> None:
    result = _group_github_comments(
        [
            {"id": 1, "path": "a.py", "line": 5, "body": "root"},
            {"id": 2, "in_reply_to_id": 1, "body": "reply"},
            {"id": 3, "in_reply_to_id": 2, "body": "nested reply"},
        ]
    )
    assert len(result) == 1
    assert result[0].id == "1"
    assert [comment["id"] for comment in result[0].comments] == [1, 2, 3]


def test_breaks_parent_cycles_without_hanging() -> None:
    result = _group_github_comments(
        [
            {"id": 1, "in_reply_to_id": 2, "body": "one"},
            {"id": 2, "in_reply_to_id": 1, "body": "two"},
        ]
    )
    assert len(result) == 2


def test_falls_back_to_reply_metadata_when_root_comment_is_missing() -> None:
    result = _group_github_comments(
        [{"id": 2, "in_reply_to_id": 1, "path": "a.py", "line": 5, "body": "reply"}],
        resolved_by_comment_id={2: False},
    )
    assert result[0].file == "a.py"
    assert result[0].line == 5


def test_uses_unknown_status_when_no_comment_has_resolution_state() -> None:
    result = _group_github_comments([{"id": 2, "path": "a.py", "line": 5, "body": "x"}], resolved_by_comment_id={})
    assert result[0].status == "unknown"


def test_rejects_comment_without_numeric_id() -> None:
    with pytest.raises(ValueError, match="malformed id"):
        _group_github_comments([{"id": "1"}])


def test_rejects_boolean_comment_id() -> None:
    with pytest.raises(ValueError, match="malformed id"):
        _group_github_comments([{"id": True}])


def test_rejects_boolean_parent_id() -> None:
    with pytest.raises(ValueError, match="parent id"):
        _group_github_comments([{"id": 1, "in_reply_to_id": True}])


def test_rejects_boolean_lines_and_preserves_review_metadata() -> None:
    result = _group_github_comments(
        [
            {
                "id": 1,
                "line": True,
                "original_line": True,
                "pull_request_review_id": 42,
                "diff_hunk": "@@ -1 +1 @@",
            }
        ]
    )
    assert result[0].line is None
    assert result[0].comments[0] == {
        "id": 1,
        "author": None,
        "content": "",
        "pull_request_review_id": 42,
        "in_reply_to_id": None,
        "diff_hunk": "@@ -1 +1 @@",
    }
