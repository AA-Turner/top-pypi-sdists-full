"""Tests for retrieve_node."""

from unittest.mock import patch

from agentic_devtools.orchestration.nodes.retrieve import (
    _error_result,
    _retrieve_github,
    _retrieve_jira,
    retrieve_node,
)


class TestRetrieveNode:
    def test_dispatches_to_jira(self):
        with patch(
            "agentic_devtools.orchestration.nodes.retrieve._retrieve_jira",
            return_value={"step": "retrieve", "issue_retrieved": True},
        ):
            result = retrieve_node({"issue_key": "TEST-1", "issue_provider": "jira"})
            assert result["issue_retrieved"] is True

    def test_dispatches_to_github(self):
        with patch(
            "agentic_devtools.orchestration.nodes.retrieve._retrieve_github",
            return_value={"step": "retrieve", "issue_retrieved": True},
        ):
            result = retrieve_node({"issue_key": "42", "issue_provider": "github"})
            assert result["issue_retrieved"] is True

    def test_derives_jira_provider_from_issue_key_when_missing(self):
        with patch(
            "agentic_devtools.orchestration.nodes.retrieve._retrieve_jira",
            return_value={"step": "retrieve", "issue_retrieved": True},
        ) as mock_jira:
            retrieve_node({"issue_key": "TEST-1"})
            mock_jira.assert_called_once_with("TEST-1")

    def test_strips_issue_key_before_provider_detection_and_dispatch(self):
        with patch(
            "agentic_devtools.orchestration.nodes.retrieve._retrieve_jira",
            return_value={"step": "retrieve", "issue_retrieved": True},
        ) as mock_jira:
            retrieve_node({"issue_key": "  TEST-1 \n"})
            mock_jira.assert_called_once_with("TEST-1")

    def test_derives_github_provider_from_issue_key_when_missing(self):
        with patch(
            "agentic_devtools.orchestration.nodes.retrieve._retrieve_github",
            return_value={"step": "retrieve", "issue_retrieved": True},
        ) as mock_github:
            retrieve_node({"issue_key": "#42"})
            mock_github.assert_called_once_with("#42")

    def test_derives_provider_when_issue_provider_is_invalid(self):
        with patch(
            "agentic_devtools.orchestration.nodes.retrieve._retrieve_github",
            return_value={"step": "retrieve", "issue_retrieved": True},
        ) as mock_github:
            retrieve_node({"issue_key": "42", "issue_provider": "unknown"})
            mock_github.assert_called_once_with("42")

    def test_derives_provider_when_issue_provider_is_unhashable(self):
        """An unhashable issue_provider (dict/list) must not raise TypeError — fall back to detection."""
        with patch(
            "agentic_devtools.orchestration.nodes.retrieve._retrieve_github",
            return_value={"step": "retrieve", "issue_retrieved": True},
        ) as mock_github:
            for bad_value in [{"corrupted": True}, ["jira"], [42]]:
                mock_github.reset_mock()
                result = retrieve_node({"issue_key": "42", "issue_provider": bad_value})
                assert result["issue_retrieved"] is True, bad_value
                mock_github.assert_called_once(), bad_value

    def test_fails_fast_when_issue_key_missing(self):
        """Missing issue_key must return retrieve_failed without attempting Jira/GitHub calls."""
        result = retrieve_node({})
        assert result["error"] is not None
        assert "issue_key" in result["error"]
        assert result["events"][0]["event"] == "retrieve_failed"

    def test_fails_fast_when_issue_key_blank(self):
        """Blank (whitespace-only) issue_key must return retrieve_failed."""
        result = retrieve_node({"issue_key": "   "})
        assert result["error"] is not None
        assert result["events"][0]["event"] == "retrieve_failed"

    def test_fails_fast_when_issue_key_not_a_string(self):
        """Non-string issue_key (e.g. int from corrupted checkpoint) must return retrieve_failed."""
        result = retrieve_node({"issue_key": 99})
        assert result["error"] is not None
        assert result["events"][0]["event"] == "retrieve_failed"

    def test_fails_fast_when_issue_key_empty_string(self):
        """Empty-string issue_key must return retrieve_failed."""
        result = retrieve_node({"issue_key": ""})
        assert result["error"] is not None
        assert result["events"][0]["event"] == "retrieve_failed"

    def test_writes_back_jira_provider_to_state(self):
        """Derived issue_provider must be written into the returned state dict."""
        with patch(
            "agentic_devtools.orchestration.nodes.retrieve._retrieve_jira",
            return_value={"step": "retrieve", "issue_retrieved": True},
        ):
            result = retrieve_node({"issue_key": "TEST-1"})
            assert result["issue_provider"] == "jira"

    def test_writes_back_github_provider_to_state(self):
        """Derived issue_provider must be written into the returned state dict."""
        with patch(
            "agentic_devtools.orchestration.nodes.retrieve._retrieve_github",
            return_value={"step": "retrieve", "issue_retrieved": True},
        ):
            result = retrieve_node({"issue_key": "#42"})
            assert result["issue_provider"] == "github"

    def test_writes_back_provider_even_when_already_set(self):
        """Explicitly-set issue_provider must still appear in the returned state."""
        with patch(
            "agentic_devtools.orchestration.nodes.retrieve._retrieve_github",
            return_value={"step": "retrieve", "issue_retrieved": True},
        ):
            result = retrieve_node({"issue_key": "42", "issue_provider": "github"})
            assert result["issue_provider"] == "github"


class TestRetrieveJira:
    def test_returns_error_on_credential_failure(self):
        with patch(
            "agentic_devtools.orchestration.nodes.retrieve.fetch_jira_issue_data",
            side_effect=ValueError("Failed to construct Jira configuration: missing PAT"),
        ):
            result = _retrieve_jira("TEST-1")
            assert result["error"] is not None
            assert "credential" in result["error"].lower()

    def test_returns_error_on_runtime_failure(self):
        with patch(
            "agentic_devtools.orchestration.nodes.retrieve.fetch_jira_issue_data",
            side_effect=RuntimeError("HTTP 404 Not Found"),
        ):
            result = _retrieve_jira("TEST-1")
            assert result["error"] is not None
            assert "retrieval failed" in result["error"].lower()

    def test_returns_error_on_unexpected_exception(self):
        with patch(
            "agentic_devtools.orchestration.nodes.retrieve.fetch_jira_issue_data",
            side_effect=ImportError("optional dependency missing"),
        ):
            result = _retrieve_jira("TEST-1")
            assert result["error"] is not None
            assert "unexpected error" in result["error"].lower()
            assert result["issue_retrieved"] is False

    def test_success_returns_normalized_data(self):
        normalized = {
            "key": "TEST-1",
            "provider": "jira",
            "summary": "Fix bug",
            "description": "Details",
            "status": "Open",
            "issue_type": "Bug",
            "labels": ["urgent"],
            "comments": [],
            "parent_key": None,
            "parent_summary": None,
            "epic_key": None,
            "epic_summary": None,
            "acceptance_criteria": None,
        }
        with patch(
            "agentic_devtools.orchestration.nodes.retrieve.fetch_jira_issue_data",
            return_value=normalized,
        ):
            result = _retrieve_jira("TEST-1")
            assert result["issue_retrieved"] is True
            assert result["issue_data"]["summary"] == "Fix bug"
            assert result["issue_data"]["provider"] == "jira"


class TestRetrieveGithub:
    def test_returns_error_on_runtime_failure(self):
        with patch(
            "agentic_devtools.orchestration.nodes.retrieve.fetch_github_issue_data",
            side_effect=RuntimeError("Cannot resolve GitHub repository"),
        ):
            result = _retrieve_github("42")
            assert result["error"] is not None
            assert "Cannot resolve" in result["error"]

    def test_returns_error_on_unexpected_exception(self):
        with patch(
            "agentic_devtools.orchestration.nodes.retrieve.fetch_github_issue_data",
            side_effect=ValueError("unexpected non-runtime error"),
        ):
            result = _retrieve_github("42")
            assert result["error"] is not None
            assert "unexpected error" in result["error"].lower()
            assert result["issue_retrieved"] is False

    def test_success_returns_normalized_data(self):
        normalized = {
            "key": "42",
            "provider": "github",
            "summary": "Add feature",
            "description": "Description here",
            "status": "open",
            "issue_type": None,
            "labels": ["enhancement"],
            "comments": [],
            "parent_key": None,
            "parent_summary": None,
            "epic_key": None,
            "epic_summary": None,
            "acceptance_criteria": None,
        }
        with patch(
            "agentic_devtools.orchestration.nodes.retrieve.fetch_github_issue_data",
            return_value=normalized,
        ):
            result = _retrieve_github("#42")
            assert result["issue_retrieved"] is True
            assert result["issue_data"]["summary"] == "Add feature"
            assert result["issue_data"]["provider"] == "github"


class TestRetrieveGithubStateDir:
    def test_passes_state_dir_to_fetch(self):
        """The GitHub path resolves state_dir and passes it to fetch_github_issue_data."""
        normalized = {"key": "42", "provider": "github", "summary": "S", "description": "D"}
        with (
            patch(
                "agentic_devtools.orchestration.nodes.retrieve.fetch_github_issue_data", return_value=normalized
            ) as mock_fetch,
            patch("agentic_devtools.state.get_state_dir", return_value="/tmp/test-state"),
        ):
            result = _retrieve_github("42")
            assert result["issue_retrieved"] is True
            call_kwargs = mock_fetch.call_args
            assert call_kwargs.kwargs.get("state_dir") is not None

    def test_state_dir_failure_still_works_and_logs_debug(self, caplog) -> None:
        """When get_state_dir raises, state_dir is None, retrieval still works, and a debug message is logged."""
        import logging

        normalized = {"key": "42", "provider": "github", "summary": "S", "description": "D"}
        with (
            patch(
                "agentic_devtools.orchestration.nodes.retrieve.fetch_github_issue_data",
                return_value=normalized,
            ) as mock_fetch,
            patch(
                "agentic_devtools.state.get_state_dir",
                side_effect=RuntimeError("no state dir"),
            ),
            caplog.at_level(logging.DEBUG, logger="agentic_devtools.orchestration.nodes.retrieve"),
        ):
            result = _retrieve_github("42")
            assert result["issue_retrieved"] is True
            call_kwargs = mock_fetch.call_args
            assert call_kwargs.kwargs.get("state_dir") is None
            assert any("get_state_dir() failed" in record.message for record in caplog.records)


class TestErrorResult:
    def test_structure(self):
        result = _error_result("something broke")
        assert result["step"] == "retrieve"
        assert result["error"] == "something broke"
        assert result["issue_retrieved"] is False
        assert result["issue_data"] == {}
        assert result["events"][0]["event"] == "retrieve_failed"


class TestRetrieveJiraStateDir:
    def test_passes_state_dir_to_fetch(self):
        """The Jira path resolves state_dir and passes it to fetch_jira_issue_data."""
        normalized = {"key": "T-1", "provider": "jira", "summary": "S", "description": "D"}
        with (
            patch(
                "agentic_devtools.orchestration.nodes.retrieve.fetch_jira_issue_data", return_value=normalized
            ) as mock_fetch,
            patch("agentic_devtools.state.get_state_dir", return_value="/tmp/test-state"),
        ):
            result = _retrieve_jira("T-1")
            assert result["issue_retrieved"] is True
            # Verify state_dir was passed
            call_kwargs = mock_fetch.call_args
            assert call_kwargs.kwargs.get("state_dir") is not None


class TestRetrieveJiraStateDirFailure:
    """When get_state_dir raises, state_dir is None but retrieval still works."""

    def test_state_dir_import_failure_still_works(self) -> None:
        normalized = {"key": "T-1", "provider": "jira", "summary": "S", "description": "D"}
        with (
            patch(
                "agentic_devtools.orchestration.nodes.retrieve.fetch_jira_issue_data",
                return_value=normalized,
            ) as mock_fetch,
            patch(
                "agentic_devtools.state.get_state_dir",
                side_effect=RuntimeError("no state dir"),
            ),
        ):
            result = _retrieve_jira("T-1")
            assert result["issue_retrieved"] is True
            call_kwargs = mock_fetch.call_args
            assert call_kwargs.kwargs.get("state_dir") is None

    def test_state_dir_failure_logs_debug(self, caplog) -> None:
        """When get_state_dir raises, a debug-level message is logged."""
        import logging

        normalized = {"key": "T-1", "provider": "jira", "summary": "S", "description": "D"}
        with (
            patch(
                "agentic_devtools.orchestration.nodes.retrieve.fetch_jira_issue_data",
                return_value=normalized,
            ),
            patch(
                "agentic_devtools.state.get_state_dir",
                side_effect=RuntimeError("no state dir"),
            ),
            caplog.at_level(logging.DEBUG, logger="agentic_devtools.orchestration.nodes.retrieve"),
        ):
            _retrieve_jira("T-1")
            assert any("get_state_dir() failed" in record.message for record in caplog.records)
