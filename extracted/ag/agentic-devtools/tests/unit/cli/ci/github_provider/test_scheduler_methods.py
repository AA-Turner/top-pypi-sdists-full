"""Tests for GitHubActionsProvider scheduler-related methods."""

import json
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.exceptions import VariableWriteError
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.retry import ProviderRateLimitError, RetryableError


@pytest.fixture()
def provider() -> GitHubActionsProvider:
    """Create a GitHubActionsProvider with a test repo."""
    return GitHubActionsProvider(repo="owner/test-repo")


class TestGetVariable:
    """Tests for GitHubActionsProvider.get_variable."""

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_value_when_found(self, mock_api, provider) -> None:
        mock_api.return_value = json.dumps({"name": "MY_VAR", "value": "42"})
        result = provider.get_variable("MY_VAR")
        assert result == "42"

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_none_on_not_found(self, mock_api, provider) -> None:
        mock_api.side_effect = RuntimeError("404 Not Found")
        result = provider.get_variable("MISSING_VAR")
        assert result is None

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_raises_on_permission_denied(self, mock_api, provider) -> None:
        mock_api.side_effect = RuntimeError("403 Forbidden")
        with pytest.raises(RuntimeError, match="403 Forbidden"):
            provider.get_variable("FORBIDDEN_VAR")

    @patch.dict("os.environ", {"REPO_VARIABLE_WRITER_PAT": "ghp_writer"})
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_uses_writer_token_when_requested(self, mock_api, provider) -> None:
        mock_api.return_value = json.dumps({"name": "MY_VAR", "value": "42"})

        result = provider.get_variable("MY_VAR", use_writer_token=True)

        assert result == "42"
        assert mock_api.call_args.kwargs["token"] == "ghp_writer"

    @patch.dict("os.environ", {}, clear=True)
    def test_raises_when_writer_token_requested_but_missing(self, provider) -> None:
        with pytest.raises(VariableWriteError, match="not configured"):
            provider.get_variable("MY_VAR", use_writer_token=True)

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_retries_transient_error(self, mock_api, mock_sleep, provider) -> None:
        mock_api.side_effect = [
            RetryableError("rate limit"),
            json.dumps({"name": "MY_VAR", "value": "42"}),
        ]
        result = provider.get_variable("MY_VAR")
        assert result == "42"
        assert mock_api.call_count == 2


class TestSetVariable:
    """Tests for GitHubActionsProvider.set_variable."""

    @patch.dict("os.environ", {"REPO_VARIABLE_WRITER_PAT": "ghp_test123"})
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_updates_existing_variable(self, mock_api, provider) -> None:
        mock_api.return_value = ""
        provider.set_variable("MY_VAR", "new_value")
        mock_api.assert_called_once()
        call_kwargs = mock_api.call_args[1]
        assert call_kwargs["method"] == "PATCH"
        assert call_kwargs["body"]["value"] == "new_value"

    @patch.dict("os.environ", {"REPO_VARIABLE_WRITER_PAT": "ghp_test123"})
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_creates_new_variable_on_404(self, mock_api, provider) -> None:
        # First call (PATCH) fails with 404, second call (POST) succeeds
        mock_api.side_effect = [RuntimeError("404 Not Found"), ""]
        provider.set_variable("NEW_VAR", "value")
        assert mock_api.call_count == 2
        second_call_kwargs = mock_api.call_args_list[1][1]
        assert second_call_kwargs["method"] == "POST"

    @patch.dict("os.environ", {"REPO_VARIABLE_WRITER_PAT": ""})
    def test_raises_when_token_missing(self, provider) -> None:
        with pytest.raises(VariableWriteError, match="not configured"):
            provider.set_variable("MY_VAR", "value")

    @patch.dict("os.environ", {"REPO_VARIABLE_WRITER_PAT": "ghp_test123"})
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_raises_on_permission_denied(self, mock_api, provider) -> None:
        mock_api.side_effect = RuntimeError("403 Forbidden")
        with pytest.raises(VariableWriteError, match="Failed to set variable"):
            provider.set_variable("MY_VAR", "value")


class TestValidateVariableToken:
    """Tests for GitHubActionsProvider.validate_variable_token."""

    @patch.dict("os.environ", {"REPO_VARIABLE_WRITER_PAT": "ghp_valid"})
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_true_when_valid(self, mock_api, provider) -> None:
        mock_api.return_value = json.dumps({"variables": []})
        assert provider.validate_variable_token() is True

    @patch.dict("os.environ", {"REPO_VARIABLE_WRITER_PAT": ""})
    def test_returns_false_when_missing(self, provider) -> None:
        assert provider.validate_variable_token() is False

    @patch.dict("os.environ", {"REPO_VARIABLE_WRITER_PAT": "ghp_expired"})
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_false_when_expired(self, mock_api, provider) -> None:
        mock_api.side_effect = RuntimeError("401 Unauthorized")
        assert provider.validate_variable_token() is False

    @patch.dict("os.environ", {"REPO_VARIABLE_WRITER_PAT": "ghp_valid"})
    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_retries_transient_error(self, mock_api, mock_sleep, provider) -> None:
        mock_api.side_effect = [RetryableError("rate limit"), json.dumps({"variables": []})]
        assert provider.validate_variable_token() is True
        assert mock_api.call_count == 2


class TestDispatchWorkflow:
    """Tests for GitHubActionsProvider.dispatch_workflow."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_dispatches_successfully(self, mock_run, provider) -> None:
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        provider.dispatch_workflow("ai-pr-loop.yml", {"pr_number": "2020"})
        cmd = mock_run.call_args[0][0]
        assert "gh" in cmd
        assert "workflow" in cmd
        assert "run" in cmd
        assert "ai-pr-loop.yml" in cmd
        assert "--field" in cmd
        assert "pr_number=2020" in cmd

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_on_failure(self, mock_run, provider) -> None:
        mock_run.return_value = MagicMock(returncode=1, stderr="dispatch error")
        with pytest.raises(RuntimeError, match="dispatch error"):
            provider.dispatch_workflow("ai-pr-loop.yml", {"pr_number": "2020"})

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_provider_rate_limit_error_on_rate_limit_stderr(self, mock_run, provider) -> None:
        from agentic_devtools.cli.ci.retry import ProviderRateLimitError

        mock_run.return_value = MagicMock(returncode=1, stderr="GraphQL: rate limit exceeded")
        with pytest.raises(ProviderRateLimitError) as exc_info:
            provider.dispatch_workflow("ai-pr-loop.yml", {"pr_number": "2020"})
        assert exc_info.value.source == "dispatch-stderr"
        assert exc_info.value.provider == "github"

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_provider_rate_limit_error_on_secondary_rate_limit_stderr(self, mock_run, provider) -> None:
        from agentic_devtools.cli.ci.retry import ProviderRateLimitError

        mock_run.return_value = MagicMock(returncode=1, stderr="secondary rate limit triggered")
        with pytest.raises(ProviderRateLimitError):
            provider.dispatch_workflow("ai-pr-loop.yml", {"pr_number": "2020"})

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_provider_rate_limit_error_on_http_429_stderr(self, mock_run, provider) -> None:
        from agentic_devtools.cli.ci.retry import ProviderRateLimitError

        mock_run.return_value = MagicMock(returncode=1, stderr="HTTP 429: Too Many Requests")
        with pytest.raises(ProviderRateLimitError):
            provider.dispatch_workflow("ai-pr-loop.yml", {"pr_number": "2020"})


class TestListEligiblePrs:
    """Tests for GitHubActionsProvider.list_eligible_prs."""

    @patch("agentic_devtools.cli.ci.github_provider._raise_for_graphql_errors")
    @patch("agentic_devtools.cli.ci.scheduler.filter_eligible_prs")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_passes_response_metadata_to_graphql_error_handler(
        self,
        mock_api,
        mock_filter,
        mock_raise_for_graphql_errors,
        provider,
    ) -> None:
        def api_side_effect(*_args, **kwargs):
            kwargs["response_metadata"].update(retry_after=120.0, reset_timestamp=1500.0, remaining=0)
            return json.dumps(
                {
                    "data": {
                        "repository": {
                            "pullRequests": {"nodes": [], "pageInfo": {"hasNextPage": False, "endCursor": None}}
                        }
                    }
                }
            )

        mock_api.side_effect = api_side_effect
        mock_filter.return_value = []

        provider.list_eligible_prs()

        mock_raise_for_graphql_errors.assert_called_once()
        kwargs = mock_raise_for_graphql_errors.call_args.kwargs
        assert kwargs["retry_after"] == 120.0
        assert kwargs["reset_timestamp"] == 1500.0
        assert kwargs["remaining"] == 0

    @patch("agentic_devtools.cli.ci.scheduler.filter_eligible_prs")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_delegates_filtering_to_scheduler_helper(self, mock_api, mock_filter, provider) -> None:
        from agentic_devtools.cli.ci.scheduler import EligiblePR

        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefName": "feature/test-2020",
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": [{"name": "ai-auto-merge-allowed"}]},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        mock_api.return_value = graphql_response
        mock_filter.return_value = [EligiblePR(number=2020, created_at="2024-01-01T00:00:00Z")]

        result = provider.list_eligible_prs()

        mock_filter.assert_called_once()
        page_prs = mock_filter.call_args.args[0]
        assert page_prs == [
            {
                "number": 2020,
                "createdAt": "2024-01-01T00:00:00Z",
                "isCrossRepository": False,
                "headRefName": "feature/test-2020",
                "head_ref": "feature/test-2020",
                "labels": [{"name": "ai-auto-merge-allowed"}],
                "is_human_blocked": False,
                "touches_audit_agent_output": False,
                "labels_to_propagate": [],
            },
        ]
        assert result == mock_filter.return_value

    @patch("agentic_devtools.cli.ci.scheduler.filter_eligible_prs")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_enriches_agent_output_only_for_copilot_heads(self, mock_api, mock_filter, provider) -> None:
        from agentic_devtools.cli.ci.scheduler import EligiblePR

        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefName": "copilot/auditbatch-abc",
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": [{"name": "ai-auto-merge-allowed"}]},
                                },
                                {
                                    "number": 2021,
                                    "createdAt": "2024-01-02T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefName": "feature/plain-branch",
                                    "headRefOid": "def456",
                                    "labels": {"nodes": [{"name": "ai-auto-merge-allowed"}]},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        files_response = json.dumps(
            [
                {"filename": "audit-batches/batch-1/agent-output/result.md"},
            ]
        )
        mock_api.side_effect = [graphql_response, files_response]
        mock_filter.side_effect = [
            [EligiblePR(number=2020, created_at="2024-01-01T00:00:00Z")],
            [EligiblePR(number=2021, created_at="2024-01-02T00:00:00Z")],
        ]

        result = provider.list_eligible_prs()

        assert [pr.number for pr in result] == [2020, 2021]
        # GraphQL + one files call (only for copilot branch)
        assert mock_api.call_count == 2
        first_candidate = mock_filter.call_args_list[0].args[0][0]
        second_candidate = mock_filter.call_args_list[1].args[0][0]
        assert first_candidate["touches_audit_agent_output"] is True
        assert second_candidate["touches_audit_agent_output"] is False

    @patch("agentic_devtools.cli.ci.scheduler.filter_eligible_prs")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_agent_output_enrichment_failures_are_fail_safe(self, mock_api, mock_filter, provider) -> None:
        from agentic_devtools.cli.ci.scheduler import EligiblePR

        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefName": "copilot/auditbatch-abc",
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": [{"name": "ai-auto-merge-allowed"}]},
                                }
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        mock_api.side_effect = [graphql_response, RuntimeError("files lookup failed")]
        mock_filter.return_value = [EligiblePR(number=2020, created_at="2024-01-01T00:00:00Z")]

        result = provider.list_eligible_prs()

        assert [pr.number for pr in result] == [2020]
        candidate = mock_filter.call_args.args[0][0]
        assert candidate["touches_audit_agent_output"] is False

    @patch.object(GitHubActionsProvider, "_touches_audit_agent_output")
    @patch("agentic_devtools.cli.ci.scheduler.filter_eligible_prs")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_agent_output_enrichment_rate_limit_is_propagated(
        self, mock_api, mock_filter, mock_touches, provider
    ) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefName": "copilot/auditbatch-abc",
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": [{"name": "ai-auto-merge-allowed"}]},
                                }
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        mock_api.return_value = graphql_response
        mock_filter.return_value = []
        mock_touches.side_effect = ProviderRateLimitError(provider="github", is_rate_limit=True)

        with patch("agentic_devtools.cli.ci.retry.time.sleep"):
            with pytest.raises(ProviderRateLimitError):
                provider.list_eligible_prs()

    @patch.object(GitHubActionsProvider, "_is_human_blocked")
    @patch("agentic_devtools.cli.ci.scheduler.filter_eligible_prs")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_human_blocked_enrichment_rate_limit_is_propagated(
        self, mock_api, mock_filter, mock_human_blocked, provider
    ) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefName": "feature/test",
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                }
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        mock_api.return_value = graphql_response
        mock_filter.return_value = []
        mock_human_blocked.side_effect = ProviderRateLimitError(provider="github", is_rate_limit=True)

        with patch("agentic_devtools.cli.ci.retry.time.sleep"):
            with pytest.raises(ProviderRateLimitError):
                provider.list_eligible_prs()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_eligible_prs(self, mock_api, provider) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                },
                                {
                                    "number": 2021,
                                    "createdAt": "2024-01-02T00:00:00Z",
                                    "isCrossRepository": True,  # Fork — should be excluded
                                    "headRefOid": "def456",
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        # GraphQL call, then reviews for human-blocked check on PR 2020 only.
        # Fork PR 2021 is short-circuited before the expensive REST call.
        mock_api.side_effect = [
            graphql_response,
            # For PR 2020 — reviews
            json.dumps([]),
        ]

        result = provider.list_eligible_prs()

        # Only 2020 should be eligible (2021 is a fork)
        assert len(result) == 1
        assert result[0].number == 2020
        # Exactly 2 API calls: 1 GraphQL + 1 reviews for 2020 (fork 2021 skipped)
        assert mock_api.call_count == 2

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_skips_non_dict_nodes(self, mock_api, provider) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                "not-a-dict",
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        mock_api.side_effect = [graphql_response, json.dumps([])]

        result = provider.list_eligible_prs()

        assert [pr.number for pr in result] == [2020]
        # Only one eligible dict node should trigger the human-blocked REST call.
        assert mock_api.call_count == 2

    @patch("agentic_devtools.cli.ci.scheduler.filter_eligible_prs")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_handles_null_label_nodes(self, mock_api, mock_filter, provider) -> None:
        from agentic_devtools.cli.ci.scheduler import EligiblePR

        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": None},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        mock_api.return_value = graphql_response
        mock_filter.return_value = [EligiblePR(number=2020, created_at="2024-01-01T00:00:00Z")]

        result = provider.list_eligible_prs()

        assert result == mock_filter.return_value
        page_prs = mock_filter.call_args.args[0]
        assert page_prs[0]["labels"] == []

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_filters_ignored_label(self, mock_api, provider) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": [{"name": "ai-pr-loop-ignore"}]},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        mock_api.return_value = graphql_response

        result = provider.list_eligible_prs()
        assert len(result) == 0
        # Only 1 API call: the GraphQL query. Ignore-label PR short-circuited before REST calls.
        assert mock_api.call_count == 1

    @patch.object(GitHubActionsProvider, "_touches_audit_agent_output")
    @patch.object(GitHubActionsProvider, "_is_human_blocked")
    @patch("agentic_devtools.cli.ci.scheduler.filter_eligible_prs")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_list_supervisor_prs_uses_supervisor_only_filters(
        self,
        mock_api,
        mock_filter,
        mock_human_blocked,
        mock_touches,
        provider,
    ) -> None:
        from agentic_devtools.cli.ci.scheduler import EligiblePR

        mock_api.return_value = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefName": "copilot/auditbatch-abc",
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                }
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        mock_filter.return_value = [EligiblePR(number=2020, created_at="2024-01-01T00:00:00Z")]

        result = provider.list_supervisor_prs(max_prs=5)

        assert result == mock_filter.return_value
        mock_human_blocked.assert_not_called()
        mock_touches.assert_not_called()
        assert mock_filter.call_args.kwargs == {
            "exclude_human_blocked": False,
            "exclude_audit_handoff": False,
        }

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_cheap_filters_short_circuit_before_human_blocked_check(self, mock_api, provider) -> None:
        """Fork and ignore-label PRs must not trigger _is_human_blocked REST calls."""
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": True,  # Fork
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                },
                                {
                                    "number": 2021,
                                    "createdAt": "2024-01-02T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "def456",
                                    "labels": {"nodes": [{"name": "ai-pr-loop-ignore"}]},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        # Only the GraphQL call should be made — both PRs are ineligible via cheap filters.
        mock_api.return_value = graphql_response

        result = provider.list_eligible_prs()

        assert result == []
        assert mock_api.call_count == 1

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_skips_non_positive_pr_numbers(self, mock_api, provider) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 0,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        mock_api.return_value = graphql_response

        result = provider.list_eligible_prs()
        assert result == []

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_pagination_with_cursor(self, mock_api, provider) -> None:
        page1 = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": True, "endCursor": "cursor1"},
                        }
                    }
                }
            }
        )
        page2 = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2021,
                                    "createdAt": "2024-01-02T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "def456",
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        # Page 1 GraphQL, reviews for PR 2020, page 2 GraphQL, reviews for PR 2021
        mock_api.side_effect = [page1, json.dumps([]), page2, json.dumps([])]

        result = provider.list_eligible_prs()
        assert len(result) == 2
        assert result[0].number == 2020
        assert result[1].number == 2021

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_pagination_breaks_when_end_cursor_none(self, mock_api, provider) -> None:
        page1 = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": True, "endCursor": None},
                        }
                    }
                }
            }
        )
        mock_api.side_effect = [page1, json.dumps([])]

        result = provider.list_eligible_prs()
        assert len(result) == 1

    @patch("agentic_devtools.cli.ci.github_provider._MAX_PR_PAGES", 2)
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_pagination_exhausts_max_pages(self, mock_api, provider) -> None:
        def make_page(number, has_next=True):
            return json.dumps(
                {
                    "data": {
                        "repository": {
                            "pullRequests": {
                                "nodes": [
                                    {
                                        "number": number,
                                        "createdAt": f"2024-01-0{number}T00:00:00Z",
                                        "isCrossRepository": False,
                                        "headRefOid": f"sha{number}",
                                        "labels": {"nodes": []},
                                    },
                                ],
                                "pageInfo": {"hasNextPage": has_next, "endCursor": f"cursor{number}"},
                            }
                        }
                    }
                }
            )

        # Both pages have hasNextPage=True, but we exhaust _MAX_PR_PAGES (2)
        mock_api.side_effect = [
            make_page(1, has_next=True),
            # Reviews for PR 1 (not approved)
            json.dumps([]),
            make_page(2, has_next=True),
            # Reviews for PR 2 (not approved)
            json.dumps([]),
        ]

        result = provider.list_eligible_prs()
        assert len(result) == 2

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_raises_on_graphql_errors(self, mock_api, provider) -> None:
        mock_api.return_value = json.dumps(
            {
                "errors": [
                    {
                        "message": "Resource not accessible by integration",
                    }
                ]
            }
        )

        with pytest.raises(RuntimeError, match="Eligible PR GraphQL query failed"):
            provider.list_eligible_prs()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_raises_on_graphql_errors_without_messages(self, mock_api, provider) -> None:
        mock_api.return_value = json.dumps({"errors": [None]})

        with pytest.raises(RuntimeError, match="Unknown GraphQL error"):
            provider.list_eligible_prs()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_skips_pr_with_auto_merge_label(self, mock_api, provider) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": [{"name": "ai-auto-merge-allowed"}]},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        mock_api.return_value = graphql_response

        result = provider.list_eligible_prs()
        # PR has auto-merge label so it's not human-blocked, still eligible
        assert len(result) == 1
        assert result[0].number == 2020

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_skips_enrichment_when_empty_head_sha(self, mock_api, provider) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "",
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        mock_api.return_value = graphql_response

        result = provider.list_eligible_prs()
        assert len(result) == 1
        assert result[0].number == 2020

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_human_blocked_check_exception_is_safe(self, mock_api, provider) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        # GraphQL, then reviews API throws unexpected exception
        mock_api.side_effect = [graphql_response, Exception("unexpected")]

        result = provider.list_eligible_prs()
        assert len(result) == 1
        assert result[0].number == 2020

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_human_blocked_reviews_api_failure(self, mock_api, provider) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        # GraphQL call succeeds, reviews API fails with RuntimeError
        mock_api.side_effect = [graphql_response, RuntimeError("API timeout")]

        result = provider.list_eligible_prs()
        assert len(result) == 1
        assert result[0].number == 2020

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_human_blocked_true_when_approved_and_ci_passing(self, mock_api, provider) -> None:
        pr_number = 2020
        head_sha = "abc123"
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": pr_number,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": head_sha,
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        reviews_response = json.dumps([{"state": "APPROVED", "user": {"login": "reviewer"}}])
        status_response = json.dumps({"state": "success", "total_count": 1})
        checks_response = json.dumps({"check_runs": [{"status": "completed", "conclusion": "success"}]})
        mock_api.side_effect = [graphql_response, reviews_response, status_response, checks_response]

        result = provider.list_eligible_prs()
        # Human-blocked PRs are EXCLUDED from the result
        assert len(result) == 0
        review_calls = [
            call for call in mock_api.call_args_list if call.args and f"/pulls/{pr_number}/reviews" in call.args[0]
        ]
        check_run_calls = [
            call for call in mock_api.call_args_list if call.args and f"/commits/{head_sha}/check-runs" in call.args[0]
        ]
        assert len(review_calls) == 1
        assert len(check_run_calls) == 1
        assert f"/pulls/{pr_number}/reviews" in review_calls[0].args[0]
        assert f"/commits/{head_sha}/check-runs" in check_run_calls[0].args[0]
        assert review_calls[0].kwargs.get("paginate") is True
        assert check_run_calls[0].kwargs.get("paginate") is True

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_human_blocked_false_when_not_approved(self, mock_api, provider) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        reviews_response = json.dumps([{"state": "CHANGES_REQUESTED"}])
        mock_api.side_effect = [graphql_response, reviews_response]

        result = provider.list_eligible_prs()
        assert len(result) == 1
        assert result[0].number == 2020

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_human_blocked_false_when_reviews_payload_not_list(self, mock_api, provider, caplog) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        # Unexpected object payload from reviews endpoint
        reviews_response = json.dumps({"unexpected": "shape"})
        mock_api.side_effect = [graphql_response, reviews_response]

        with caplog.at_level("WARNING"):
            result = provider.list_eligible_prs()

        assert len(result) == 1
        assert "Unexpected reviews payload type" in caplog.text

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_human_blocked_warns_when_checks_payload_not_dict(self, mock_api, provider, caplog) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        reviews_response = json.dumps([{"state": "APPROVED", "user": {"login": "reviewer"}}])
        status_response = json.dumps({"state": "success", "total_count": 1})
        # Unexpected array payload from check-runs endpoint
        checks_response = json.dumps([])
        mock_api.side_effect = [graphql_response, reviews_response, status_response, checks_response]

        with caplog.at_level("WARNING"):
            result = provider.list_eligible_prs()

        # Unexpected payload shape should fail-safe and keep PR eligible.
        assert len(result) == 1
        assert result[0].number == 2020
        assert "Unexpected check-runs payload type" in caplog.text

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_human_blocked_false_when_changes_requested_after_approval(self, mock_api, provider) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        reviews_response = json.dumps(
            [
                {"state": "APPROVED", "user": {"login": "reviewer"}},
                {"state": "CHANGES_REQUESTED", "user": {"login": "reviewer"}},
            ]
        )
        mock_api.side_effect = [graphql_response, reviews_response]

        result = provider.list_eligible_prs()
        assert len(result) == 1
        assert result[0].number == 2020

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_human_blocked_false_when_approval_is_dismissed(self, mock_api, provider) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        reviews_response = json.dumps(
            [
                {
                    "id": 1,
                    "state": "APPROVED",
                    "submitted_at": "2024-01-01T00:00:00Z",
                    "user": {"login": "reviewer"},
                },
                {
                    "id": 2,
                    "state": "DISMISSED",
                    "submitted_at": "2024-01-02T00:00:00Z",
                    "user": {"login": "reviewer"},
                },
                {
                    "id": 3,
                    "state": "COMMENTED",
                    "submitted_at": "2024-01-03T00:00:00Z",
                    "user": {"login": "reviewer"},
                },
            ]
        )
        mock_api.side_effect = [graphql_response, reviews_response]

        result = provider.list_eligible_prs()

        assert len(result) == 1
        assert result[0].number == 2020

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_human_blocked_true_when_approval_after_changes_requested(self, mock_api, provider) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        reviews_response = json.dumps(
            [
                {
                    "id": 2,
                    "state": "APPROVED",
                    "submitted_at": "2024-01-02T00:00:00Z",
                    "user": {"login": "reviewer"},
                },
                {
                    "id": 1,
                    "state": "CHANGES_REQUESTED",
                    "submitted_at": "2024-01-01T00:00:00Z",
                    "user": {"login": "reviewer"},
                },
            ]
        )
        status_response = json.dumps({"state": "success", "total_count": 1})
        checks_response = json.dumps({"check_runs": [{"status": "completed", "conclusion": "success"}]})
        mock_api.side_effect = [graphql_response, reviews_response, status_response, checks_response]

        result = provider.list_eligible_prs()
        assert len(result) == 0

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_human_blocked_false_when_status_api_fails(self, mock_api, provider) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        reviews_response = json.dumps([{"state": "APPROVED", "user": {"login": "reviewer"}}])
        # Status API fails
        mock_api.side_effect = [graphql_response, reviews_response, RuntimeError("timeout")]

        result = provider.list_eligible_prs()
        assert len(result) == 1
        assert result[0].number == 2020

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_human_blocked_false_when_checks_api_fails(self, mock_api, provider) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        reviews_response = json.dumps([{"state": "APPROVED", "user": {"login": "reviewer"}}])
        status_response = json.dumps({"state": "success", "total_count": 1})
        # Check-runs API fails
        mock_api.side_effect = [graphql_response, reviews_response, status_response, RuntimeError("err")]

        result = provider.list_eligible_prs()
        assert len(result) == 1
        assert result[0].number == 2020

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_human_blocked_false_when_ci_failing(self, mock_api, provider) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        reviews_response = json.dumps([{"state": "APPROVED"}])
        status_response = json.dumps({"state": "failure", "total_count": 1})
        checks_response = json.dumps({"check_runs": [{"status": "completed", "conclusion": "failure"}]})
        mock_api.side_effect = [graphql_response, reviews_response, status_response, checks_response]

        result = provider.list_eligible_prs()
        assert len(result) == 1
        assert result[0].number == 2020

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_honors_max_prs_limit(self, mock_api, provider) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "sha-2020",
                                    "labels": {"nodes": []},
                                },
                                {
                                    "number": 2021,
                                    "createdAt": "2024-01-02T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "sha-2021",
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": True, "endCursor": "cursor1"},
                        }
                    }
                }
            }
        )
        # GraphQL page + reviews for the first PR only (short-circuit before PR 2021 enrichment/page 2 fetch)
        mock_api.side_effect = [graphql_response, json.dumps([])]

        result = provider.list_eligible_prs(max_prs=1)

        assert [pr.number for pr in result] == [2020]
        assert mock_api.call_count == 2

    def test_graphql_queries_request_linked_issue_labels(self) -> None:
        from agentic_devtools.cli.ci.github_provider import (
            _ELIGIBLE_PRS_QUERY,
            _ELIGIBLE_PRS_QUERY_WITH_CURSOR,
        )

        for query in (_ELIGIBLE_PRS_QUERY, _ELIGIBLE_PRS_QUERY_WITH_CURSOR):
            assert "closingIssuesReferences" in query

    @patch("agentic_devtools.cli.ci.scheduler.filter_eligible_prs")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_enriches_allowlisted_labels_from_linked_issues(self, mock_api, mock_filter, provider) -> None:
        from agentic_devtools.cli.ci.scheduler import EligiblePR

        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefName": "feature/fix-2020",
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": [{"name": "suppressed-comment-follow-up"}]},
                                    "closingIssuesReferences": {
                                        "nodes": [
                                            {
                                                "labels": {
                                                    "nodes": [
                                                        {"name": "ai-auto-merge-allowed"},
                                                        {"name": "suppressed-comment-follow-up"},
                                                        {"name": "Subtask"},
                                                    ]
                                                }
                                            }
                                        ]
                                    },
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        mock_api.return_value = graphql_response
        mock_filter.return_value = [EligiblePR(number=2020, created_at="2024-01-01T00:00:00Z")]

        provider.list_eligible_prs()

        candidate = mock_filter.call_args.args[0][0]
        # Allowlist only: "Subtask" is never copied; the label the PR already has is skipped.
        assert candidate["labels_to_propagate"] == ["ai-auto-merge-allowed"]

    @patch("agentic_devtools.cli.ci.scheduler.filter_eligible_prs")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_pr_without_linked_issue_has_nothing_to_propagate(self, mock_api, mock_filter, provider) -> None:
        from agentic_devtools.cli.ci.scheduler import EligiblePR

        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefName": "feature/plain",
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": [{"name": "ai-auto-merge-allowed"}]},
                                    "closingIssuesReferences": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        mock_api.return_value = graphql_response
        mock_filter.return_value = [EligiblePR(number=2020, created_at="2024-01-01T00:00:00Z")]

        provider.list_eligible_prs()

        assert mock_filter.call_args.args[0][0]["labels_to_propagate"] == []

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_inherited_auto_merge_label_skips_human_blocked_check(self, mock_api, provider) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefName": "feature/fix-2020",
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                    "closingIssuesReferences": {
                                        "nodes": [{"labels": {"nodes": [{"name": "ai-auto-merge-allowed"}]}}]
                                    },
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        mock_api.return_value = graphql_response

        result = provider.list_eligible_prs()

        assert [pr.number for pr in result] == [2020]
        assert result[0].labels_to_propagate == ("ai-auto-merge-allowed",)
        # Only the GraphQL call — the human-blocked reviews lookup is short-circuited.
        assert mock_api.call_count == 1


class TestGetRecentDispatchHistory:
    """Tests for GitHubActionsProvider.get_recent_dispatch_history."""

    # --- Existing tests updated to mock _gh_api for the per-run detail fetch ---

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.object(GitHubActionsProvider, "list_workflow_runs")
    def test_returns_dispatch_events(self, mock_list_runs, mock_gh_api, provider) -> None:
        """Secondary fallback: pr_number from pull_requests[] used for non-dispatch runs."""
        run_mock = MagicMock()
        run_mock.id = 12345
        run_mock.event = "push"
        run_mock.pr_number = 2020
        run_mock.name = "AI PR Loop"
        run_mock.created_at = "2024-06-01T10:00:00Z"
        mock_list_runs.return_value = [run_mock]

        result = provider.get_recent_dispatch_history("ai-pr-loop.yml")
        assert len(result) == 1
        assert result[0].pr_number == 2020
        mock_gh_api.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.object(GitHubActionsProvider, "list_workflow_runs")
    def test_extracts_pr_number_from_run_name(self, mock_list_runs, mock_gh_api, provider) -> None:
        """Tertiary fallback: run-name regex used for non-dispatch runs with no pr_number."""
        run_mock = MagicMock()
        run_mock.id = 12345
        run_mock.event = "push"
        run_mock.pr_number = 0
        run_mock.name = "AI PR Loop (PR #2021)"
        run_mock.created_at = "2024-06-01T10:00:00Z"
        mock_list_runs.return_value = [run_mock]

        result = provider.get_recent_dispatch_history("ai-pr-loop.yml")
        assert len(result) == 1
        assert result[0].pr_number == 2021
        mock_gh_api.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.object(GitHubActionsProvider, "list_workflow_runs")
    def test_skips_runs_without_pr_number(self, mock_list_runs, mock_gh_api, provider) -> None:
        """Run with no PR number from any source is skipped (non-dispatch event)."""
        run_mock = MagicMock()
        run_mock.id = 12345
        run_mock.event = "push"
        run_mock.pr_number = 0
        run_mock.name = "AI PR Loop"
        run_mock.created_at = "2024-06-01T10:00:00Z"
        mock_list_runs.return_value = [run_mock]

        result = provider.get_recent_dispatch_history("ai-pr-loop.yml")
        assert len(result) == 0
        mock_gh_api.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.object(GitHubActionsProvider, "list_workflow_runs")
    def test_returns_empty_when_no_runs(self, mock_list_runs, mock_gh_api, provider) -> None:
        """Empty run list produces empty result without calling _gh_api."""
        mock_list_runs.return_value = []

        result = provider.get_recent_dispatch_history("ai-pr-loop.yml")
        assert len(result) == 0
        mock_gh_api.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider._MAX_DISPATCH_HISTORY_EVENTS", 2)
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.object(GitHubActionsProvider, "list_workflow_runs")
    def test_stops_at_max_events_limit(self, mock_list_runs, mock_gh_api, provider) -> None:
        """Collection stops once _MAX_DISPATCH_HISTORY_EVENTS events are gathered."""
        runs = []
        for i in range(5):
            run_mock = MagicMock()
            run_mock.id = 10000 + i
            run_mock.event = "push"
            run_mock.pr_number = 2020 + i
            run_mock.name = "AI PR Loop"
            run_mock.created_at = f"2024-06-0{i + 1}T10:00:00Z"
            runs.append(run_mock)
        mock_list_runs.return_value = runs

        result = provider.get_recent_dispatch_history("ai-pr-loop.yml")
        # Should stop after collecting 2 events (_MAX_DISPATCH_HISTORY_EVENTS=2)
        assert len(result) == 2
        mock_gh_api.assert_not_called()

    # --- New tests for inputs.pr_number primary source (Fix A) ---

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.object(GitHubActionsProvider, "list_workflow_runs")
    def test_sources_pr_number_from_inputs_primary(self, mock_list_runs, mock_gh_api, provider) -> None:
        """inputs.pr_number from run detail is the primary PR number source."""
        run_mock = MagicMock()
        run_mock.id = 99999
        run_mock.event = "workflow_dispatch"
        run_mock.pr_number = 0  # pull_requests[] empty — typical for workflow_dispatch
        run_mock.name = "AI PR Loop"  # no PR # token in name
        run_mock.created_at = "2024-06-01T10:00:00Z"
        mock_list_runs.return_value = [run_mock]
        mock_gh_api.return_value = json.dumps({"inputs": {"pr_number": "2236"}})

        result = provider.get_recent_dispatch_history("ai-pr-loop.yml")
        assert len(result) == 1
        assert result[0].pr_number == 2236

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.object(GitHubActionsProvider, "list_workflow_runs")
    def test_parses_quoted_inputs_pr_number(self, mock_list_runs, mock_gh_api, provider) -> None:
        """inputs.pr_number enclosed in double-quotes is parsed correctly."""
        run_mock = MagicMock()
        run_mock.id = 11111
        run_mock.event = "workflow_dispatch"
        run_mock.pr_number = 0
        run_mock.name = "AI PR Loop"
        run_mock.created_at = "2024-06-01T10:00:00Z"
        mock_list_runs.return_value = [run_mock]
        mock_gh_api.return_value = json.dumps({"inputs": {"pr_number": '"2236"'}})

        result = provider.get_recent_dispatch_history("ai-pr-loop.yml")
        assert len(result) == 1
        assert result[0].pr_number == 2236

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.object(GitHubActionsProvider, "list_workflow_runs")
    def test_parses_whitespace_padded_inputs_pr_number(self, mock_list_runs, mock_gh_api, provider) -> None:
        """inputs.pr_number with surrounding whitespace is stripped and parsed."""
        run_mock = MagicMock()
        run_mock.id = 66666
        run_mock.event = "workflow_dispatch"
        run_mock.pr_number = 0
        run_mock.name = "AI PR Loop"
        run_mock.created_at = "2024-06-01T10:00:00Z"
        mock_list_runs.return_value = [run_mock]
        mock_gh_api.return_value = json.dumps({"inputs": {"pr_number": "  2236  "}})

        result = provider.get_recent_dispatch_history("ai-pr-loop.yml")
        assert len(result) == 1
        assert result[0].pr_number == 2236

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.object(GitHubActionsProvider, "list_workflow_runs")
    def test_skips_run_with_missing_inputs(self, mock_list_runs, mock_gh_api, provider) -> None:
        """Run whose detail has no 'inputs' key and no other signal is skipped."""
        run_mock = MagicMock()
        run_mock.id = 22222
        run_mock.event = "workflow_dispatch"
        run_mock.pr_number = 0
        run_mock.name = "AI PR Loop"
        run_mock.created_at = "2024-06-01T10:00:00Z"
        mock_list_runs.return_value = [run_mock]
        mock_gh_api.return_value = json.dumps({})  # no 'inputs' key at all

        result = provider.get_recent_dispatch_history("ai-pr-loop.yml")
        assert len(result) == 0

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.object(GitHubActionsProvider, "list_workflow_runs")
    def test_skips_run_with_non_numeric_inputs_pr_number(self, mock_list_runs, mock_gh_api, provider) -> None:
        """Run with non-numeric inputs.pr_number and no other signal is skipped."""
        run_mock = MagicMock()
        run_mock.id = 33333
        run_mock.event = "workflow_dispatch"
        run_mock.pr_number = 0
        run_mock.name = "AI PR Loop"
        run_mock.created_at = "2024-06-01T10:00:00Z"
        mock_list_runs.return_value = [run_mock]
        mock_gh_api.return_value = json.dumps({"inputs": {"pr_number": "not-a-number"}})

        result = provider.get_recent_dispatch_history("ai-pr-loop.yml")
        assert len(result) == 0

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.object(GitHubActionsProvider, "list_workflow_runs")
    def test_skips_run_with_zero_inputs_pr_number(self, mock_list_runs, mock_gh_api, provider) -> None:
        """Run with inputs.pr_number == '0' and no other signal is skipped."""
        run_mock = MagicMock()
        run_mock.id = 34444
        run_mock.event = "workflow_dispatch"
        run_mock.pr_number = 0
        run_mock.name = "AI PR Loop"
        run_mock.created_at = "2024-06-01T10:00:00Z"
        mock_list_runs.return_value = [run_mock]
        mock_gh_api.return_value = json.dumps({"inputs": {"pr_number": "0"}})

        result = provider.get_recent_dispatch_history("ai-pr-loop.yml")
        assert len(result) == 0

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.object(GitHubActionsProvider, "list_workflow_runs")
    def test_skips_run_when_detail_fetch_raises(self, mock_list_runs, mock_gh_api, provider) -> None:
        """Per-run detail fetch exception is silenced; other runs still produce events."""
        run_a = MagicMock()
        run_a.id = 44444
        run_a.event = "workflow_dispatch"
        run_a.pr_number = 0
        run_a.name = "AI PR Loop"
        run_a.created_at = "2024-06-01T11:00:00Z"  # newer

        run_b = MagicMock()
        run_b.id = 55555
        run_b.event = "workflow_dispatch"
        run_b.pr_number = 0
        run_b.name = "AI PR Loop"
        run_b.created_at = "2024-06-01T10:00:00Z"  # older

        mock_list_runs.return_value = [run_a, run_b]

        def api_side_effect(endpoint, **kwargs):
            if "44444" in endpoint:
                raise RuntimeError("403 Forbidden")
            return json.dumps({"inputs": {"pr_number": "2237"}})

        mock_gh_api.side_effect = api_side_effect

        result = provider.get_recent_dispatch_history("ai-pr-loop.yml")
        # run_a detail fetch failed (skipped); run_b resolved to PR #2237
        assert len(result) == 1
        assert result[0].pr_number == 2237

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.object(GitHubActionsProvider, "list_workflow_runs")
    def test_retryable_error_breaks_loop(self, mock_list_runs, mock_gh_api, provider) -> None:
        """RetryableError from per-run detail fetch breaks the loop immediately."""
        run_a = MagicMock()
        run_a.id = 44444
        run_a.event = "workflow_dispatch"
        run_a.pr_number = 0
        run_a.name = "AI PR Loop"
        run_a.created_at = "2024-06-01T11:00:00Z"  # newer

        run_b = MagicMock()
        run_b.id = 55555
        run_b.event = "workflow_dispatch"
        run_b.pr_number = 0
        run_b.name = "AI PR Loop"
        run_b.created_at = "2024-06-01T10:00:00Z"  # older

        mock_list_runs.return_value = [run_a, run_b]
        mock_gh_api.side_effect = RetryableError("rate limited")

        result = provider.get_recent_dispatch_history("ai-pr-loop.yml")
        # Loop stopped after first RetryableError — run_b never fetched
        assert len(result) == 0
        assert mock_gh_api.call_count == 1

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.object(GitHubActionsProvider, "list_workflow_runs")
    def test_retryable_error_mid_loop_preserves_prior_result(self, mock_list_runs, mock_gh_api, provider) -> None:
        """RetryableError on second run still returns first run's collected result."""
        run_a = MagicMock()
        run_a.id = 44444
        run_a.event = "workflow_dispatch"
        run_a.pr_number = 0
        run_a.name = "AI PR Loop"
        run_a.created_at = "2024-06-01T11:00:00Z"  # newer — processed first

        run_b = MagicMock()
        run_b.id = 55555
        run_b.event = "workflow_dispatch"
        run_b.pr_number = 0
        run_b.name = "AI PR Loop"
        run_b.created_at = "2024-06-01T10:00:00Z"  # older — triggers RetryableError

        mock_list_runs.return_value = [run_a, run_b]

        def api_side_effect(endpoint, **kwargs):
            if "44444" in endpoint:
                return json.dumps({"inputs": {"pr_number": "2236"}})
            raise RetryableError("rate limited")

        mock_gh_api.side_effect = api_side_effect

        result = provider.get_recent_dispatch_history("ai-pr-loop.yml")
        # run_a result preserved; loop stopped at run_b's RetryableError
        assert len(result) == 1
        assert result[0].pr_number == 2236
        assert mock_gh_api.call_count == 2

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.object(GitHubActionsProvider, "list_workflow_runs")
    def test_rate_limited_run_detail_propagates_provider_error(self, mock_list_runs, mock_gh_api, provider) -> None:
        run_mock = MagicMock()
        run_mock.id = 44444
        run_mock.event = "workflow_dispatch"
        run_mock.pr_number = 0
        run_mock.name = "AI PR Loop"
        run_mock.created_at = "2024-06-01T11:00:00Z"
        mock_list_runs.return_value = [run_mock]
        mock_gh_api.side_effect = RetryableError("rate limited", provider="github", is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError) as exc_info:
            provider.get_recent_dispatch_history("ai-pr-loop.yml")

        assert exc_info.value.is_rate_limit is True

    @patch.object(GitHubActionsProvider, "list_workflow_runs")
    def test_calls_list_workflow_runs_without_status_filter(self, mock_list_runs, provider) -> None:
        """list_workflow_runs is called with status=None to include in-progress runs (Fix B)."""
        mock_list_runs.return_value = []

        provider.get_recent_dispatch_history("ai-pr-loop.yml")

        mock_list_runs.assert_called_once_with("ai-pr-loop.yml", window_hours=24, status=None)

    @patch("agentic_devtools.cli.ci.github_provider._MAX_DISPATCH_HISTORY_RUNS", 2)
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.object(GitHubActionsProvider, "list_workflow_runs")
    def test_run_detail_fetch_count_bounded_by_max_runs(self, mock_list_runs, mock_gh_api, provider) -> None:
        """Run-detail fetches are bounded by _MAX_DISPATCH_HISTORY_RUNS."""
        runs = []
        for i in range(5):
            run_mock = MagicMock()
            run_mock.id = 10000 + i
            run_mock.event = "workflow_dispatch"
            run_mock.pr_number = 0
            run_mock.name = "AI PR Loop"
            run_mock.created_at = f"2024-06-0{i + 1}T10:00:00Z"
            runs.append(run_mock)
        mock_list_runs.return_value = runs
        # No valid pr_number from any source
        mock_gh_api.return_value = json.dumps({"inputs": {}})

        provider.get_recent_dispatch_history("ai-pr-loop.yml")

        # Only _MAX_DISPATCH_HISTORY_RUNS=2 detail fetches should be made
        assert mock_gh_api.call_count == 2

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch.object(GitHubActionsProvider, "list_workflow_runs")
    def test_results_ordered_most_recent_first(self, mock_list_runs, mock_gh_api, provider) -> None:
        """Results are sorted most-recent-first regardless of list_workflow_runs order."""
        run_older = MagicMock()
        run_older.id = 77777
        run_older.event = "workflow_dispatch"
        run_older.pr_number = 0
        run_older.name = "AI PR Loop"
        run_older.created_at = "2024-06-01T08:00:00Z"

        run_newer = MagicMock()
        run_newer.id = 88888
        run_newer.event = "workflow_dispatch"
        run_newer.pr_number = 0
        run_newer.name = "AI PR Loop"
        run_newer.created_at = "2024-06-01T12:00:00Z"

        # Deliberately return older run first to verify sorting
        mock_list_runs.return_value = [run_older, run_newer]

        def api_side_effect(endpoint, **kwargs):
            if "77777" in endpoint:
                return json.dumps({"inputs": {"pr_number": "2236"}})
            return json.dumps({"inputs": {"pr_number": "2237"}})

        mock_gh_api.side_effect = api_side_effect

        result = provider.get_recent_dispatch_history("ai-pr-loop.yml")
        assert len(result) == 2
        # Newer run (2237) should come first
        assert result[0].pr_number == 2237
        assert result[1].pr_number == 2236


class TestSetVariableCreateFailure:
    """Tests for set_variable when POST creation also fails."""

    @patch.dict("os.environ", {"REPO_VARIABLE_WRITER_PAT": "ghp_test123"})
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_raises_when_create_also_fails(self, mock_api, provider) -> None:
        # PATCH fails with 404, then POST also fails
        mock_api.side_effect = [
            RuntimeError("404 Not Found"),
            RuntimeError("500 Internal Server Error"),
        ]
        with pytest.raises(VariableWriteError, match="Failed to create variable"):
            provider.set_variable("MY_VAR", "value")


class TestRetryableSchedulerMethods:
    """Tests retry behavior for scheduler-related provider methods."""

    @patch.dict("os.environ", {"REPO_VARIABLE_WRITER_PAT": "ghp_test123"})
    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_set_variable_retries_transient_error(self, mock_api, mock_sleep, provider) -> None:
        mock_api.side_effect = [RetryableError("rate limit"), ""]
        provider.set_variable("MY_VAR", "value")
        assert mock_api.call_count == 2

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_list_eligible_prs_retries_transient_error(self, mock_api, mock_sleep, provider) -> None:
        graphql_response = json.dumps(
            {
                "data": {
                    "repository": {
                        "pullRequests": {
                            "nodes": [
                                {
                                    "number": 2020,
                                    "createdAt": "2024-01-01T00:00:00Z",
                                    "isCrossRepository": False,
                                    "headRefOid": "abc123",
                                    "labels": {"nodes": []},
                                },
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        )
        mock_api.side_effect = [
            RetryableError("rate limit"),
            graphql_response,
            json.dumps([]),
        ]

        result = provider.list_eligible_prs()

        assert [pr.number for pr in result] == [2020]
        assert mock_api.call_count == 3


class TestTouchesAuditAgentOutput:
    """Tests for GitHubActionsProvider._touches_audit_agent_output."""

    def test_returns_false_when_no_changed_files(self, provider) -> None:
        with patch.object(provider, "list_pr_files", return_value=[]):
            assert provider._touches_audit_agent_output(2020) is False

    def test_returns_true_when_later_file_matches(self, provider) -> None:
        with patch.object(
            provider,
            "list_pr_files",
            return_value=[
                "docs/readme.md",
                "audit-batches/batch-1/agent-output/result.md",
            ],
        ):
            assert provider._touches_audit_agent_output(2020) is True
