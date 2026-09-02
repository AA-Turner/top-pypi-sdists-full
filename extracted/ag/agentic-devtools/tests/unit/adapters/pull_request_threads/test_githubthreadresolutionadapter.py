from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest
import requests

from agentic_devtools.adapters.pull_request_threads import (
    GitHubThreadResolutionAdapter,
    ThreadResolutionRequest,
)


class _Response:
    def __init__(self, payload: dict[str, Any], status_code: int = 200) -> None:
        self.status_code = status_code
        self._payload = payload

    def json(self) -> dict[str, Any]:
        return self._payload


def test_resolves_comment_id_with_opaque_node_and_verifies() -> None:
    calls: list[dict[str, Any]] = []

    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        calls.append(kwargs)
        query = kwargs["json"]["query"]
        if "resolveReviewThread" in query:
            return _Response({"data": {"resolveReviewThread": {"thread": {"id": "PRRT_node", "isResolved": True}}}})
        return _Response(
            {
                "data": {
                    "repository": {
                        "pullRequest": {
                            "reviewThreads": {
                                "pageInfo": {"hasNextPage": False, "endCursor": None},
                                "nodes": [
                                    {
                                        "id": "PRRT_node",
                                        "isResolved": len(calls) > 1,
                                        "comments": {"nodes": [{"databaseId": 44}]},
                                    }
                                ],
                            }
                        }
                    }
                }
            }
        )

    request = ThreadResolutionRequest(
        provider="github",
        repository="owner/repo",
        pull_request_id=12,
        github_comment_id=44,
    )
    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(request)

    assert result.success is True
    assert result.status == "resolved"
    assert result.github_thread_node_id == "PRRT_node"
    assert "secret" not in str(result.as_dict())


def _github_request(node_id: str = "PRRT_node") -> ThreadResolutionRequest:
    return ThreadResolutionRequest(
        provider="github",
        repository="owner/repo",
        pull_request_id=12,
        github_thread_node_id=node_id,
    )


def test_already_resolved_thread_skips_mutation() -> None:
    calls: list[str] = []

    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        calls.append(kwargs["json"]["query"])
        return _Response(
            {
                "data": {
                    "repository": {
                        "pullRequest": {
                            "reviewThreads": {
                                "pageInfo": {"hasNextPage": False, "endCursor": None},
                                "nodes": [{"id": "PRRT_node", "isResolved": True, "comments": {"nodes": []}}],
                            }
                        }
                    }
                }
            }
        )

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request())

    assert result.success is True
    assert result.status == "already_resolved"
    assert len(calls) == 1
    assert "resolveReviewThread" not in calls[0]


def test_dry_run_does_not_call_github() -> None:
    def request_fn(*_args: Any, **_kwargs: Any) -> _Response:
        pytest.fail("dry-run must not contact GitHub")

    request = ThreadResolutionRequest(
        provider="github",
        repository="owner/repo",
        pull_request_id=12,
        github_thread_node_id="PRRT_node",
        dry_run=True,
    )

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(request)

    assert result.success is True
    assert result.status == "dry_run"
    assert result.github_thread_node_id is None
    assert result.github_comment_id is None
    payload = result.as_dict()
    assert payload["github_thread_node_id"] is None
    assert payload["github_comment_id"] is None


def test_non_boolean_is_resolved_maps_to_malformed_response() -> None:
    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        return _Response(
            {
                "data": {
                    "repository": {
                        "pullRequest": {
                            "reviewThreads": {
                                "pageInfo": {"hasNextPage": False, "endCursor": None},
                                "nodes": [{"id": "PRRT_node", "isResolved": "false", "comments": {"nodes": []}}],
                            }
                        }
                    }
                }
            }
        )

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request())

    assert result.success is False
    assert result.diagnostics == ("malformed_response",)


def test_transient_mutation_response_rechecks_thread_before_reporting_failure() -> None:
    calls: list[str] = []

    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        query = kwargs["json"]["query"]
        calls.append(query)
        if "resolveReviewThread" in query:
            return _Response({"message": "temporary failure"}, status_code=503)
        return _Response(
            {
                "data": {
                    "repository": {
                        "pullRequest": {
                            "reviewThreads": {
                                "pageInfo": {"hasNextPage": False, "endCursor": None},
                                "nodes": [
                                    {
                                        "id": "PRRT_node",
                                        "isResolved": len(calls) > 2,
                                        "comments": {"nodes": []},
                                    }
                                ],
                            }
                        }
                    }
                }
            }
        )

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request())

    assert result.success is True
    assert result.status == "resolved"
    assert sum("resolveReviewThread" in query for query in calls) == 1


def test_transient_mutation_response_preserves_original_diagnostic_when_reread_is_malformed() -> None:
    calls: list[str] = []

    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        query = kwargs["json"]["query"]
        calls.append(query)
        if "resolveReviewThread" in query:
            return _Response({"message": "temporary failure"}, status_code=503)
        if len(calls) == 1:
            return _Response(
                {
                    "data": {
                        "repository": {
                            "pullRequest": {
                                "reviewThreads": {
                                    "pageInfo": {"hasNextPage": False, "endCursor": None},
                                    "nodes": [{"id": "PRRT_node", "isResolved": False, "comments": {"nodes": []}}],
                                }
                            }
                        }
                    }
                }
            )
        return _Response(
            {
                "data": {
                    "repository": {
                        "pullRequest": {
                            "reviewThreads": {
                                "pageInfo": {"hasNextPage": False, "endCursor": None},
                                "nodes": [{"id": "PRRT_node", "isResolved": "nope", "comments": {"nodes": []}}],
                            }
                        }
                    }
                }
            }
        )

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request())

    assert result.success is False
    assert result.diagnostics == ("provider_unavailable",)


def test_transient_mutation_response_preserves_original_diagnostic_when_reread_missing_cursor() -> None:
    calls: list[str] = []

    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        query = kwargs["json"]["query"]
        calls.append(query)
        if "resolveReviewThread" in query:
            return _Response({"message": "temporary failure"}, status_code=503)
        return _Response(
            {
                "data": {
                    "repository": {
                        "pullRequest": {
                            "reviewThreads": {
                                "pageInfo": {"hasNextPage": True, "endCursor": None},
                                "nodes": [{"id": "PRRT_node", "isResolved": False, "comments": {"nodes": []}}],
                            }
                        }
                    }
                }
            }
        )

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request())

    assert result.success is False
    assert result.diagnostics == ("provider_unavailable",)


def test_connection_error_maps_to_provider_unavailable() -> None:
    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        raise requests.ConnectionError("connection reset by peer")

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request())

    assert result.success is False
    assert result.diagnostics == ("provider_unavailable",)


def test_mutation_timeout_rechecks_and_reports_success_if_resolved() -> None:
    calls: list[str] = []

    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        query = kwargs["json"]["query"]
        calls.append(query)
        if "resolveReviewThread" in query:
            raise requests.Timeout("timed out")
        return _Response(
            {
                "data": {
                    "repository": {
                        "pullRequest": {
                            "reviewThreads": {
                                "pageInfo": {"hasNextPage": False, "endCursor": None},
                                "nodes": [
                                    {
                                        "id": "PRRT_node",
                                        "isResolved": len(calls) > 2,
                                        "comments": {"nodes": []},
                                    }
                                ],
                            }
                        }
                    }
                }
            }
        )

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request())

    assert result.success is True
    assert result.status == "resolved"
    assert result.verification_status == "verified"


def test_mutation_timeout_preserves_diagnostic_when_thread_still_unresolved() -> None:
    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        query = kwargs["json"]["query"]
        if "resolveReviewThread" in query:
            raise requests.Timeout("timed out")
        return _Response(
            {
                "data": {
                    "repository": {
                        "pullRequest": {
                            "reviewThreads": {
                                "pageInfo": {"hasNextPage": False, "endCursor": None},
                                "nodes": [{"id": "PRRT_node", "isResolved": False, "comments": {"nodes": []}}],
                            }
                        }
                    }
                }
            }
        )

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request())

    assert result.success is False
    assert result.diagnostics == ("timeout",)


def test_mutation_connection_error_rechecks_and_reports_success_if_resolved() -> None:
    calls: list[str] = []

    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        query = kwargs["json"]["query"]
        calls.append(query)
        if "resolveReviewThread" in query:
            raise requests.ConnectionError("disconnected")
        return _Response(
            {
                "data": {
                    "repository": {
                        "pullRequest": {
                            "reviewThreads": {
                                "pageInfo": {"hasNextPage": False, "endCursor": None},
                                "nodes": [
                                    {
                                        "id": "PRRT_node",
                                        "isResolved": len(calls) > 2,
                                        "comments": {"nodes": []},
                                    }
                                ],
                            }
                        }
                    }
                }
            }
        )

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request())

    assert result.success is True
    assert result.status == "resolved"
    assert result.verification_status == "verified"


@pytest.mark.parametrize(
    ("error", "diagnostic"),
    [
        ({"type": "FORBIDDEN"}, "forbidden"),
        ({"type": "NOT_FOUND"}, "not_found"),
        ({"type": "RATE_LIMITED"}, "rate_limited"),
        ({"extensions": {"status": 409}}, "conflict"),
        ({"extensions": {"status": 422}}, "invalid_request"),
        ({"extensions": {"status": "403"}}, "forbidden"),
        ({"extensions": {"status": 418, "code": "CONFLICT"}}, "conflict"),
        ({"extensions": {"code": "BAD_USER_INPUT"}}, "invalid_request"),
        ({"extensions": {"status": 418}}, "graphql_error"),
        ({"type": 42}, "graphql_error"),
        ({"message": "other"}, "graphql_error"),
    ],
)
def test_graphql_errors_use_stable_diagnostics(error: dict[str, Any], diagnostic: str) -> None:
    def request_fn(_method: str, _url: str, **_kwargs: Any) -> _Response:
        return _Response({"errors": [error]})

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request())

    assert result.success is False
    assert result.diagnostics == (diagnostic,)


@pytest.mark.parametrize("payload", [{"errors": "invalid"}, {"errors": [None]}])
def test_malformed_graphql_errors_use_generic_diagnostic(payload: dict[str, Any]) -> None:
    def request_fn(_method: str, _url: str, **_kwargs: Any) -> _Response:
        return _Response(payload)

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request())

    assert result.diagnostics == ("graphql_error",)


def test_graphql_error_mapping_checks_all_errors() -> None:
    def request_fn(_method: str, _url: str, **_kwargs: Any) -> _Response:
        return _Response({"errors": [{"message": "other"}, {"type": "UNAUTHORIZED"}]})

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request())

    assert result.diagnostics == ("unauthorized",)


def test_graphql_error_mapping_skips_multiple_unrecognized_errors() -> None:
    def request_fn(_method: str, _url: str, **_kwargs: Any) -> _Response:
        return _Response({"errors": [{"type": "UNKNOWN_FIRST"}, {"type": "UNKNOWN_SECOND"}]})

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request())

    assert result.diagnostics == ("graphql_error",)


def test_rejects_malformed_thread_identity_from_github() -> None:
    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        return _Response(
            {
                "data": {
                    "repository": {
                        "pullRequest": {
                            "reviewThreads": {
                                "pageInfo": {"hasNextPage": False, "endCursor": None},
                                "nodes": [
                                    {
                                        "id": "numeric-id",
                                        "isResolved": False,
                                        "comments": {"nodes": [{"databaseId": 44}]},
                                    }
                                ],
                            }
                        }
                    }
                }
            }
        )

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(
        ThreadResolutionRequest(
            provider="github",
            repository="owner/repo",
            pull_request_id=12,
            github_comment_id=44,
        )
    )

    assert result.success is False
    assert result.diagnostics == ("malformed_response",)


def test_comment_found_on_second_page_of_thread_comments() -> None:
    """Target databaseId appears after the first 100 comments; _find_comment_in_thread paginates."""
    calls: list[dict[str, Any]] = []
    threads_query_count = [0]

    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        calls.append(kwargs)
        query = kwargs["json"]["query"]
        if "resolveReviewThread" in query:
            return _Response({"data": {"resolveReviewThread": {"thread": {"id": "PRRT_node", "isResolved": True}}}})
        if "node(id:" in query:
            # _THREAD_COMMENTS_QUERY — second comment page contains the target
            return _Response(
                {
                    "data": {
                        "node": {
                            "comments": {
                                "pageInfo": {"hasNextPage": False, "endCursor": None},
                                "nodes": [{"databaseId": 999}],
                            }
                        }
                    }
                }
            )
        # _THREADS_QUERY — first call for lookup, second for post-resolve verification
        threads_query_count[0] += 1
        is_verification = threads_query_count[0] > 1
        return _Response(
            {
                "data": {
                    "repository": {
                        "pullRequest": {
                            "reviewThreads": {
                                "pageInfo": {"hasNextPage": False, "endCursor": None},
                                "nodes": [
                                    {
                                        "id": "PRRT_node",
                                        "isResolved": is_verification,
                                        "comments": {
                                            "pageInfo": {"hasNextPage": True, "endCursor": "comment_cursor_1"},
                                            "nodes": [{"databaseId": 1}],
                                        },
                                    }
                                ],
                            }
                        }
                    }
                }
            }
        )

    request = ThreadResolutionRequest(
        provider="github",
        repository="owner/repo",
        pull_request_id=12,
        github_comment_id=999,
    )
    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(request)

    assert result.success is True
    assert result.status == "resolved"
    assert result.github_thread_node_id == "PRRT_node"
    # Verify _THREAD_COMMENTS_QUERY was issued for the second comment page
    thread_comment_queries = [c for c in calls if "node(id:" in c["json"]["query"]]
    assert len(thread_comment_queries) == 1
    assert thread_comment_queries[0]["json"]["variables"]["commentsCursor"] == "comment_cursor_1"


def test_missing_comment_pagination_cursor_raises_malformed_response() -> None:
    """Missing endCursor on a hasNextPage=True comment page surfaces as malformed_response."""

    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        query = kwargs["json"]["query"]
        if "node(id:" in query:
            # _THREAD_COMMENTS_QUERY — claims there is a next page but provides no cursor
            return _Response(
                {
                    "data": {
                        "node": {
                            "comments": {
                                "pageInfo": {"hasNextPage": True, "endCursor": None},
                                "nodes": [{"databaseId": 1}],
                            }
                        }
                    }
                }
            )
        # _THREADS_QUERY — first comment page has no match and claims a next page
        return _Response(
            {
                "data": {
                    "repository": {
                        "pullRequest": {
                            "reviewThreads": {
                                "pageInfo": {"hasNextPage": False, "endCursor": None},
                                "nodes": [
                                    {
                                        "id": "PRRT_node",
                                        "isResolved": False,
                                        "comments": {
                                            "pageInfo": {"hasNextPage": True, "endCursor": "comment_cursor_1"},
                                            "nodes": [{"databaseId": 1}],
                                        },
                                    }
                                ],
                            }
                        }
                    }
                }
            }
        )

    request = ThreadResolutionRequest(
        provider="github",
        repository="owner/repo",
        pull_request_id=12,
        github_comment_id=999,
    )
    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(request)

    assert result.success is False
    assert result.diagnostics == ("malformed_response",)


def test_attribute_error_in_graphql_response_maps_to_malformed_response() -> None:
    """Nodes that are not dicts trigger AttributeError during .get() traversal."""

    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        return _Response(
            {
                "data": {
                    "repository": {
                        "pullRequest": {
                            "reviewThreads": {
                                "pageInfo": {"hasNextPage": False, "endCursor": None},
                                "nodes": ["unexpected-string-node"],
                            }
                        }
                    }
                }
            }
        )

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(
        ThreadResolutionRequest(
            provider="github",
            repository="owner/repo",
            pull_request_id=12,
            github_thread_node_id="PRRT_node",
        )
    )

    assert result.success is False
    assert result.diagnostics == ("malformed_response",)


def test_graphql_rate_limit_429_is_retried_with_backoff() -> None:
    """A transient 429 response is retried with bounded backoff."""
    call_count = [0]

    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        call_count[0] += 1
        return _Response({}, status_code=429)

    with patch("agentic_devtools.adapters.pull_request_threads.time.sleep"):
        result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(
            ThreadResolutionRequest(
                provider="github",
                repository="owner/repo",
                pull_request_id=12,
                github_thread_node_id="PRRT_node",
            )
        )

    assert call_count[0] == 4
    assert result.success is False
    assert result.diagnostics == ("rate_limited",)


def _threads_response(node_id: str, is_resolved: bool) -> dict[str, Any]:
    return {
        "data": {
            "repository": {
                "pullRequest": {
                    "reviewThreads": {
                        "pageInfo": {"hasNextPage": False, "endCursor": None},
                        "nodes": [{"id": node_id, "isResolved": is_resolved, "comments": {"nodes": []}}],
                    }
                }
            }
        }
    }


def test_mutation_response_wrong_id_sets_verification_failed_status() -> None:
    """Mutation response returning a mismatched thread ID must report verification_status='failed'."""

    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        query = kwargs["json"]["query"]
        if "resolveReviewThread" in query:
            return _Response({"data": {"resolveReviewThread": {"thread": {"id": "PRRT_other", "isResolved": True}}}})
        return _Response(_threads_response("PRRT_node", False))

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request("PRRT_node"))

    assert result.success is False
    assert result.diagnostics == ("verification_failed",)
    assert result.verification_status == "failed"
    assert result.prior_state == "unresolved"


@pytest.mark.parametrize(
    "payload",
    [
        {"data": None},
        {"data": {"resolveReviewThread": None}},
    ],
)
def test_mutation_response_missing_container_maps_to_malformed_response(payload: dict[str, Any]) -> None:
    """A missing mutation container must preserve the malformed_response diagnostic."""

    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        query = kwargs["json"]["query"]
        if "resolveReviewThread" in query:
            return _Response(payload)
        return _Response(_threads_response("PRRT_node", False))

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request("PRRT_node"))

    assert result.success is False
    assert result.diagnostics == ("malformed_response",)


def test_mutation_response_missing_thread_maps_to_malformed_response() -> None:
    """A null mutation thread payload must preserve the malformed_response diagnostic."""

    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        query = kwargs["json"]["query"]
        if "resolveReviewThread" in query:
            return _Response({"data": {"resolveReviewThread": {"thread": None}}})
        return _Response(_threads_response("PRRT_node", False))

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request("PRRT_node"))

    assert result.success is False
    assert result.diagnostics == ("malformed_response",)


def test_mutation_response_non_string_id_maps_to_malformed_response() -> None:
    """A mutation thread id must be a non-empty string before identity verification runs."""

    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        query = kwargs["json"]["query"]
        if "resolveReviewThread" in query:
            return _Response({"data": {"resolveReviewThread": {"thread": {"id": 123, "isResolved": True}}}})
        return _Response(_threads_response("PRRT_node", False))

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request("PRRT_node"))

    assert result.success is False
    assert result.diagnostics == ("malformed_response",)


def test_mutation_response_not_resolved_sets_verification_failed_status() -> None:
    """Mutation response with isResolved=False must report verification_status='failed'."""

    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        query = kwargs["json"]["query"]
        if "resolveReviewThread" in query:
            return _Response({"data": {"resolveReviewThread": {"thread": {"id": "PRRT_node", "isResolved": False}}}})
        return _Response(_threads_response("PRRT_node", False))

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request("PRRT_node"))

    assert result.success is False
    assert result.diagnostics == ("verification_failed",)
    assert result.verification_status == "failed"
    assert result.prior_state == "unresolved"


def test_final_readback_still_unresolved_sets_verification_failed_status() -> None:
    """Final readback returning isResolved=False must report verification_status='failed'."""
    call_count = [0]

    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        query = kwargs["json"]["query"]
        if "resolveReviewThread" in query:
            return _Response({"data": {"resolveReviewThread": {"thread": {"id": "PRRT_node", "isResolved": True}}}})
        call_count[0] += 1
        # First call: lookup before mutation (returns unresolved); subsequent: readback still unresolved.
        return _Response(_threads_response("PRRT_node", False))

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request("PRRT_node"))

    assert result.success is False
    assert result.diagnostics == ("verification_failed",)
    assert result.verification_status == "failed"
    assert result.prior_state == "unresolved"


def test_null_repository_in_threads_query_maps_to_not_found() -> None:
    """A null repository in the reviewThreads query must produce not_found, not malformed_response."""

    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        return _Response({"data": {"repository": None}})

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request("PRRT_node"))

    assert result.success is False
    assert result.diagnostics == ("not_found",)


def test_null_pull_request_in_threads_query_maps_to_not_found() -> None:
    """A null pullRequest in the reviewThreads query must produce not_found, not malformed_response."""

    def request_fn(_method: str, _url: str, **kwargs: Any) -> _Response:
        return _Response({"data": {"repository": {"pullRequest": None}}})

    result = GitHubThreadResolutionAdapter(token="secret", request_fn=request_fn).resolve(_github_request("PRRT_node"))

    assert result.success is False
    assert result.diagnostics == ("not_found",)
