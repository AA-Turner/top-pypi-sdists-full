from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.azure_devops.helpers import _find_existing_thread_by_marker


def test_returns_matching_thread_id_and_status() -> None:
    requests = MagicMock()
    response = MagicMock()
    response.json.return_value = {
        "value": [
            {
                "id": 41,
                "status": "closed",
                "comments": [
                    {
                        "id": 7,
                        "author": {"id": "user-1"},
                        "content": "<!-- agdt-approval:idempotency-key:key-1 -->\nLGTM",
                    }
                ],
            }
        ]
    }
    requests.get.return_value = response
    config = MagicMock()
    config.build_api_url.return_value = "https://example.com/threads"

    result = _find_existing_thread_by_marker(requests, {}, config, "repo-1", 42, "key-1", "user-1")

    assert result == (41, "closed", 7, "LGTM")


def test_returns_none_when_threads_do_not_match_marker() -> None:
    requests = MagicMock()
    response = MagicMock()
    response.json.return_value = {"value": [{"id": 41, "status": "closed", "comments": [{"content": "LGTM"}]}]}
    requests.get.return_value = response
    config = MagicMock()
    config.build_api_url.return_value = "https://example.com/threads"

    result = _find_existing_thread_by_marker(requests, {}, config, "repo-1", 42, "key-1", "user-1")

    assert result is None


def test_returns_matching_thread_from_continuation_page() -> None:
    requests = MagicMock()
    first_response = MagicMock()
    first_response.json.return_value = {"value": [{"id": 41, "status": "closed", "comments": []}]}
    first_response.headers = {"x-ms-continuationtoken": "next/page"}
    second_response = MagicMock()
    second_response.json.return_value = {
        "value": [
            {
                "id": 42,
                "status": "active",
                "comments": [
                    {
                        "id": 9,
                        "author": {"id": "user-1"},
                        "content": "<!-- agdt-approval:idempotency-key:key-1 -->",
                    }
                ],
            }
        ]
    }
    second_response.headers = {}
    requests.get.side_effect = [first_response, second_response]
    config = MagicMock()
    config.build_api_url.return_value = "https://example.com/threads"

    result = _find_existing_thread_by_marker(requests, {}, config, "repo-1", 42, "key-1", "user-1")

    assert result == (42, "active", 9, "")
    assert requests.get.call_args_list[1].args[0] == ("https://example.com/threads&continuationToken=next%2Fpage")


@pytest.mark.parametrize("continuation_tokens", [("repeat", "repeat"), ("a", "b", "a")])
def test_rejects_repeated_continuation_tokens(continuation_tokens: tuple[str, ...]) -> None:
    requests = MagicMock()
    responses = []
    for token in continuation_tokens:
        response = MagicMock()
        response.json.return_value = {"value": []}
        response.headers = {"x-ms-continuationtoken": token}
        responses.append(response)
    requests.get.side_effect = responses
    config = MagicMock()
    config.build_api_url.return_value = "https://example.com/threads"

    with pytest.raises(RuntimeError, match="repeated continuation token"):
        _find_existing_thread_by_marker(requests, {}, config, "repo-1", 42, "key-1", "user-1")

    assert requests.get.call_count == len(continuation_tokens)


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        (["not an object"], "Azure DevOps thread list response must be a JSON object"),
        ({"value": "not a list"}, "Azure DevOps thread list response must contain a list 'value'"),
    ],
)
def test_rejects_invalid_thread_list_response(payload: object, message: str) -> None:
    requests = MagicMock()
    response = MagicMock()
    response.json.return_value = payload
    requests.get.return_value = response
    config = MagicMock()
    config.build_api_url.return_value = "https://example.com/threads"

    with pytest.raises(RuntimeError, match=message):
        _find_existing_thread_by_marker(requests, {}, config, "repo-1", 42, "key-1", "user-1")


def test_skips_non_mapping_thread_entries() -> None:
    requests = MagicMock()
    response = MagicMock()
    response.json.return_value = {"value": ["not a thread"]}
    response.headers = {}
    requests.get.return_value = response
    config = MagicMock()
    config.build_api_url.return_value = "https://example.com/threads"

    result = _find_existing_thread_by_marker(requests, {}, config, "repo-1", 42, "key-1", "user-1")

    assert result is None


def test_rejects_boolean_thread_id() -> None:
    requests = MagicMock()
    response = MagicMock()
    response.json.return_value = {
        "value": [
            {
                "id": True,
                "status": "active",
                "comments": [
                    {
                        "author": {"id": "user-1"},
                        "content": "<!-- agdt-approval:idempotency-key:key-1 -->\nLGTM",
                    }
                ],
            }
        ]
    }
    response.headers = {}
    requests.get.return_value = response
    config = MagicMock()
    config.build_api_url.return_value = "https://example.com/threads"

    result = _find_existing_thread_by_marker(requests, {}, config, "repo-1", 42, "key-1", "user-1")

    assert result is None


def test_returns_none_comment_id_when_comment_lacks_a_valid_id() -> None:
    requests = MagicMock()
    response = MagicMock()
    response.json.return_value = {
        "value": [
            {
                "id": 41,
                "status": "closed",
                "comments": [
                    {
                        "author": {"id": "user-1"},
                        "content": "<!-- agdt-approval:idempotency-key:key-1 -->\nLGTM",
                    }
                ],
            }
        ]
    }
    requests.get.return_value = response
    config = MagicMock()
    config.build_api_url.return_value = "https://example.com/threads"

    result = _find_existing_thread_by_marker(requests, {}, config, "repo-1", 42, "key-1", "user-1")

    assert result == (41, "closed", None, "LGTM")


@pytest.mark.parametrize("comment_id", [True, 0, -1])
def test_returns_none_comment_id_for_non_positive_or_boolean_id(comment_id: object) -> None:
    """Malformed comment IDs are rejected before they can be used in a PATCH URL."""
    requests = MagicMock()
    response = MagicMock()
    response.json.return_value = {
        "value": [
            {
                "id": 41,
                "status": "closed",
                "comments": [
                    {
                        "id": comment_id,
                        "author": {"id": "user-1"},
                        "content": "<!-- agdt-approval:idempotency-key:key-1 -->\nLGTM",
                    }
                ],
            }
        ]
    }
    requests.get.return_value = response
    config = MagicMock()
    config.build_api_url.return_value = "https://example.com/threads"

    result = _find_existing_thread_by_marker(requests, {}, config, "repo-1", 42, "key-1", "user-1")

    assert result == (41, "closed", None, "LGTM")


@pytest.mark.parametrize(
    "content",
    [
        "Discussion:\n<!-- agdt-approval:idempotency-key:key-1 -->\nQuoted text",
        "```markdown\n<!-- agdt-approval:idempotency-key:key-1 -->\n```",
        "<!-- agdt-approval:idempotency-key:key-1 --> trailing text",
    ],
)
def test_ignores_quoted_or_noncanonical_marker(content: str) -> None:
    """Only a canonical leading marker identifies an approval thread."""
    requests = MagicMock()
    response = MagicMock()
    response.json.return_value = {
        "value": [{"id": 41, "status": "closed", "comments": [{"content": content, "author": {"id": "user-1"}}]}]
    }
    requests.get.return_value = response
    config = MagicMock()
    config.build_api_url.return_value = "https://example.com/threads"

    assert _find_existing_thread_by_marker(requests, {}, config, "repo-1", 42, "key-1", "user-1") is None


def test_does_not_reuse_marker_thread_from_another_author() -> None:
    """A matching marker from another approver does not identify the current user's thread."""
    requests = MagicMock()
    response = MagicMock()
    response.json.return_value = {
        "value": [
            {
                "id": 41,
                "status": "closed",
                "comments": [
                    {
                        "id": 7,
                        "author": {"id": "other-user"},
                        "content": "<!-- agdt-approval:idempotency-key:key-1 -->\nLGTM",
                    }
                ],
            }
        ]
    }
    requests.get.return_value = response
    config = MagicMock()
    config.build_api_url.return_value = "https://example.com/threads"

    assert _find_existing_thread_by_marker(requests, {}, config, "repo-1", 42, "key-1", "user-1") is None


@pytest.mark.parametrize(
    "thread",
    [
        {
            "id": 41,
            "isDeleted": True,
            "status": "closed",
            "comments": [
                {
                    "id": 7,
                    "author": {"id": "user-1"},
                    "content": "<!-- agdt-approval:idempotency-key:key-1 -->\nLGTM",
                }
            ],
        },
        {
            "id": 41,
            "status": "closed",
            "comments": [
                {
                    "id": 7,
                    "isDeleted": True,
                    "author": {"id": "user-1"},
                    "content": "<!-- agdt-approval:idempotency-key:key-1 -->\nLGTM",
                }
            ],
        },
    ],
)
def test_does_not_reuse_deleted_marker_thread_or_comment(thread: dict) -> None:
    """Deleted approval threads or first comments are not treated as existing approvals."""
    requests = MagicMock()
    response = MagicMock()
    response.json.return_value = {"value": [thread]}
    response.headers = {}
    requests.get.return_value = response
    config = MagicMock()
    config.build_api_url.return_value = "https://example.com/threads"

    assert _find_existing_thread_by_marker(requests, {}, config, "repo-1", 42, "key-1", "user-1") is None
