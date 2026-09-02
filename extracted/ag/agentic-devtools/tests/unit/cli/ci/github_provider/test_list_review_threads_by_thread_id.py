"""Tests for GitHubActionsProvider.list_review_threads_by_thread_id()."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def _mock_run_safe_response(data):
    class _Result:
        returncode = 0
        stdout = json.dumps(data)
        stderr = ""

    return _Result()


def _threads_response(nodes, *, has_next_page=False, end_cursor=None):
    return {
        "data": {
            "repository": {
                "pullRequest": {
                    "reviewThreads": {
                        "pageInfo": {"hasNextPage": has_next_page, "endCursor": end_cursor},
                        "nodes": nodes,
                    }
                }
            }
        }
    }


class TestListReviewThreadsByThreadId:
    """Tests for the thread-keyed review thread projection."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_maps_thread_ids_to_state_and_comment_ids(self, mock_run_safe):
        mock_run_safe.return_value = _mock_run_safe_response(
            _threads_response(
                [
                    {
                        "id": "THREAD_A",
                        "isResolved": True,
                        "comments": {"nodes": [{"databaseId": 10}, {"databaseId": 11}]},
                    },
                    {
                        "id": "THREAD_B",
                        "isResolved": False,
                        "comments": {"nodes": [{"databaseId": 12}]},
                    },
                ]
            )
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.list_review_threads_by_thread_id(42)

        assert result == {
            "THREAD_A": (True, (10, 11)),
            "THREAD_B": (False, (12,)),
        }

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_comment_keyed_projection_is_unchanged(self, mock_run_safe):
        """The thread-keyed addition does not alter list_review_thread_states()."""
        mock_run_safe.return_value = _mock_run_safe_response(
            _threads_response(
                [
                    {
                        "id": "THREAD_A",
                        "isResolved": True,
                        "comments": {"nodes": [{"databaseId": 10}, {"databaseId": 11}]},
                    },
                    {
                        "id": "THREAD_B",
                        "isResolved": False,
                        "comments": {"nodes": [{"databaseId": 12}]},
                    },
                ]
            )
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        assert provider.list_review_thread_states(42) == {
            10: (True, True),
            11: (True, True),
            12: (False, False),
        }

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_distinguishes_one_multi_comment_thread_from_many_threads(self, mock_run_safe):
        mock_run_safe.return_value = _mock_run_safe_response(
            _threads_response(
                [
                    {
                        "id": "THREAD_A",
                        "isResolved": False,
                        "comments": {"nodes": [{"databaseId": 1}, {"databaseId": 2}, {"databaseId": 3}]},
                    }
                ]
            )
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.list_review_threads_by_thread_id(42)

        assert len(result) == 1
        assert result["THREAD_A"] == (False, (1, 2, 3))

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_uses_synthetic_key_when_thread_id_missing_or_invalid(self, mock_run_safe):
        mock_run_safe.return_value = _mock_run_safe_response(
            _threads_response(
                [
                    {"isResolved": False, "comments": {"nodes": [{"databaseId": 20}]}},
                    {"id": "", "isResolved": True, "comments": {"nodes": [{"databaseId": 21}]}},
                    {"id": 123, "isResolved": False, "comments": {"nodes": [{"databaseId": 22}]}},
                ]
            )
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.list_review_threads_by_thread_id(42)

        assert len(result) == 3
        assert sorted(result.values()) == [
            (False, (20,)),
            (False, (22,)),
            (True, (21,)),
        ]
        assert all(key.startswith("__agdt-thread-") for key in result)

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_omits_non_integer_comment_ids(self, mock_run_safe):
        mock_run_safe.return_value = _mock_run_safe_response(
            _threads_response(
                [
                    {
                        "id": "THREAD_A",
                        "isResolved": False,
                        "comments": {"nodes": [{"databaseId": "not-an-int"}, {"databaseId": 30}]},
                    }
                ]
            )
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.list_review_threads_by_thread_id(42)

        assert result == {"THREAD_A": (False, (30,))}

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_synthetic_keys_stay_unique_across_thread_pages(self, mock_run_safe):
        mock_run_safe.side_effect = [
            _mock_run_safe_response(
                _threads_response(
                    [{"isResolved": False, "comments": {"nodes": [{"databaseId": 40}]}}],
                    has_next_page=True,
                    end_cursor="cursor-1",
                )
            ),
            _mock_run_safe_response(
                _threads_response([{"isResolved": True, "comments": {"nodes": [{"databaseId": 41}]}}])
            ),
        ]
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.list_review_threads_by_thread_id(42)

        assert len(result) == 2
        assert all(key.startswith("__agdt-thread-") for key in result)
        assert mock_run_safe.call_count == 2

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_reuses_cached_fetch_without_extra_round_trip(self, mock_run_safe):
        mock_run_safe.return_value = _mock_run_safe_response(
            _threads_response([{"id": "THREAD_A", "isResolved": False, "comments": {"nodes": [{"databaseId": 50}]}}])
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        provider.list_review_thread_states(42)
        result = provider.list_review_threads_by_thread_id(42)

        assert result == {"THREAD_A": (False, (50,))}
        assert mock_run_safe.call_count == 1

    def test_returns_empty_mapping_when_identity_cache_not_populated(self):
        """A signals fetch that leaves no identity entry degrades to an empty map."""
        provider = GitHubActionsProvider(repo="owner/repo")

        with patch.object(GitHubActionsProvider, "_fetch_thread_signals_by_comment_id", return_value={}):
            assert provider.list_review_threads_by_thread_id(42) == {}

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returned_mapping_is_a_copy(self, mock_run_safe):
        mock_run_safe.return_value = _mock_run_safe_response(
            _threads_response([{"id": "THREAD_A", "isResolved": False, "comments": {"nodes": [{"databaseId": 60}]}}])
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.list_review_threads_by_thread_id(42)
        result.clear()

        assert provider.list_review_threads_by_thread_id(42) == {"THREAD_A": (False, (60,))}

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_provider_rate_limit_error_on_graphql_rate_limit_payload(self, mock_run_safe, _mock_sleep):
        class _Result:
            returncode = 0
            stdout = (
                "HTTP/2 200 OK\n"
                "Retry-After: 60\n"
                "X-RateLimit-Reset: 600\n"
                "X-RateLimit-Remaining: 0\n\n"
                '{"errors":[{"type":"RATE_LIMITED","message":"rate limit exceeded"}]}'
            )
            stderr = ""

        mock_run_safe.return_value = _Result()
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(ProviderRateLimitError) as exc_info:
            provider.list_review_threads_by_thread_id(42)
        assert exc_info.value.retry_after_seconds == 60
        assert exc_info.value.reset_timestamp == 600
        assert exc_info.value.remaining == 0

    @pytest.mark.parametrize(
        ("payload", "expected_message"),
        [
            ({"data": {}}, "missing data.repository"),
            ({"data": {"repository": {}}}, "missing data.repository.pullRequest"),
            (
                {"data": {"repository": {"pullRequest": {}}}},
                "missing data.repository.pullRequest.reviewThreads",
            ),
        ],
    )
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_runtime_error_when_thread_signals_graphql_shape_is_invalid(
        self, mock_run_safe, payload, expected_message
    ):
        mock_run_safe.return_value = _mock_run_safe_response(payload)
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match=expected_message):
            provider.list_review_threads_by_thread_id(42)
