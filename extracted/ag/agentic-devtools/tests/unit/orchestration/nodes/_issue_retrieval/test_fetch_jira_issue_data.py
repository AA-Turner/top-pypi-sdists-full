"""Tests for fetch_jira_issue_data."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.orchestration.nodes._issue_retrieval import fetch_jira_issue_data


class TestFetchJiraIssueData:
    """Tests for Jira issue retrieval with parent/epic context."""

    def _make_config(self) -> MagicMock:
        config = MagicMock()
        config.base_url = "https://jira.example.com"
        config.headers = {"Authorization": "Basic abc123"}
        config.ssl_verify = True
        config.requests_module = MagicMock()
        return config

    def _make_issue(
        self,
        *,
        key: str = "PROJ-1",
        summary: str = "Test summary",
        description: str = "Test description",
        issue_type: str = "Story",
        is_subtask: bool = False,
        parent_key: str | None = None,
        epic_link: str | None = None,
        labels: list[str] | None = None,
    ) -> dict:
        fields: dict = {
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type, "subtask": is_subtask},
            "status": {"name": "In Progress"},
            "labels": labels or [],
            "comment": {"comments": [{"id": "1", "body": "A comment", "created": "2024-01-01"}]},
        }
        if parent_key:
            fields["parent"] = {"key": parent_key}
        if epic_link:
            fields["customfield_10008"] = epic_link
        return {"key": key, "fields": fields}

    def test_story_issue_returns_normalized_dict(self, tmp_path: Path) -> None:
        config = self._make_config()
        issue = self._make_issue(key="PROJ-10", labels=["backend"])
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": None, "epic_issue": None, "remote_links": []}

        with patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx):
            result = fetch_jira_issue_data("PROJ-10", config=config, state_dir=tmp_path)

        assert result["key"] == "PROJ-10"
        assert result["provider"] == "jira"
        assert result["summary"] == "Test summary"
        assert result["description"] == "Test description"
        assert result["labels"] == ["backend"]
        assert result["comments"] == [{"comment_id": "1", "body": "A comment", "created_at": "2024-01-01"}]
        assert result["parent_key"] is None
        assert result["parent_summary"] is None
        assert result["epic_key"] is None
        assert result["epic_summary"] is None

    def test_subtask_with_parent_and_epic(self, tmp_path: Path) -> None:
        config = self._make_config()
        issue = self._make_issue(key="PROJ-11", is_subtask=True, parent_key="PROJ-5")
        parent = {"key": "PROJ-5", "fields": {"summary": "Parent story", "customfield_10008": "PROJ-1"}}
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": parent, "epic_issue": None, "remote_links": []}
        epic_ctx: dict[str, Any] = {
            "issue": {"key": "PROJ-1", "fields": {"summary": "Epic summary"}},
            "parent_issue": None,
            "epic_issue": None,
            "remote_links": [],
        }

        with patch(
            "agentic_devtools.tools.jira.fetch_issue_context",
            side_effect=[ctx, epic_ctx],
        ):
            result = fetch_jira_issue_data("PROJ-11", config=config, state_dir=tmp_path)

        assert result["parent_key"] == "PROJ-5"
        assert result["parent_summary"] == "Parent story"
        assert result["epic_key"] == "PROJ-1"
        assert result["epic_summary"] == "Epic summary"

    def test_subtask_epic_fetch_failure_still_returns_epic_key(self, tmp_path: Path) -> None:
        """When fetching the epic for a subtask fails, epic_key is still set but epic_summary is None."""
        config = self._make_config()
        issue = self._make_issue(key="PROJ-12", is_subtask=True, parent_key="PROJ-5")
        parent = {"key": "PROJ-5", "fields": {"summary": "Parent story", "customfield_10008": "PROJ-1"}}
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": parent, "epic_issue": None, "remote_links": []}

        with patch(
            "agentic_devtools.tools.jira.fetch_issue_context",
            side_effect=[ctx, RuntimeError("epic fetch failed")],
        ):
            result = fetch_jira_issue_data("PROJ-12", config=config, state_dir=tmp_path)

        assert result["epic_key"] == "PROJ-1"
        assert result["epic_summary"] is None

    def test_story_with_epic(self, tmp_path: Path) -> None:
        config = self._make_config()
        issue = self._make_issue(key="PROJ-20", epic_link="PROJ-100")
        epic = {"key": "PROJ-100", "fields": {"summary": "Epic title"}}
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": None, "epic_issue": epic, "remote_links": []}

        with patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx):
            result = fetch_jira_issue_data("PROJ-20", config=config, state_dir=tmp_path)

        assert result["epic_key"] == "PROJ-100"
        assert result["epic_summary"] == "Epic title"

    def test_story_with_epic_link_and_missing_epic_context_preserves_epic_key(self, tmp_path: Path) -> None:
        config = self._make_config()
        issue = self._make_issue(key="PROJ-21", epic_link="PROJ-101")
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": None, "epic_issue": None, "remote_links": []}

        with patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx):
            result = fetch_jira_issue_data("PROJ-21", config=config, state_dir=tmp_path)

        assert result["epic_key"] == "PROJ-101"
        assert result["epic_summary"] is None

    def test_missing_description(self, tmp_path: Path) -> None:
        config = self._make_config()
        issue = self._make_issue(key="PROJ-30", description="")
        issue["fields"]["description"] = None
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": None, "epic_issue": None, "remote_links": []}

        with patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx):
            result = fetch_jira_issue_data("PROJ-30", config=config, state_dir=tmp_path)

        assert result["description"] == ""
        assert result["acceptance_criteria"] is None

    def test_adf_content_converted(self, tmp_path: Path) -> None:
        config = self._make_config()
        issue = self._make_issue(key="PROJ-40")
        # ADF dict for summary
        issue["fields"]["summary"] = {
            "type": "doc",
            "content": [{"type": "paragraph", "content": [{"text": "ADF Title"}]}],
        }
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": None, "epic_issue": None, "remote_links": []}

        with patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx):
            result = fetch_jira_issue_data("PROJ-40", config=config, state_dir=tmp_path)

        assert "ADF Title" in result["summary"]

    def test_credential_preflight_missing_pat(self) -> None:
        config = MagicMock()
        config.base_url = "https://jira.example.com"
        config.headers = {}

        with pytest.raises(ValueError, match="Authorization header is missing"):
            fetch_jira_issue_data("PROJ-1", config=config)

    def test_credential_preflight_empty_base_url(self) -> None:
        config = MagicMock()
        config.base_url = ""
        config.headers = {"Authorization": "Basic abc"}

        with pytest.raises(ValueError, match="base_url is empty"):
            fetch_jira_issue_data("PROJ-1", config=config)

    def test_http_401_raises_runtime_error(self, tmp_path: Path) -> None:
        config = self._make_config()
        with patch(
            "agentic_devtools.tools.jira.fetch_issue_context",
            side_effect=Exception("HTTP 401 Unauthorized"),
        ):
            with pytest.raises(RuntimeError, match="authentication failed"):
                fetch_jira_issue_data("PROJ-1", config=config, state_dir=tmp_path)

    def test_http_404_raises_runtime_error(self, tmp_path: Path) -> None:
        config = self._make_config()
        with patch(
            "agentic_devtools.tools.jira.fetch_issue_context",
            side_effect=Exception("HTTP 404 Not Found"),
        ):
            with pytest.raises(RuntimeError, match="not found"):
                fetch_jira_issue_data("PROJ-1", config=config, state_dir=tmp_path)

    def test_http_500_with_issue_key_suffix_401_is_not_auth_error(self, tmp_path: Path) -> None:
        config = self._make_config()
        with patch(
            "agentic_devtools.tools.jira.fetch_issue_context",
            side_effect=Exception("HTTP 500 for issue PROJ-401"),
        ):
            with pytest.raises(RuntimeError, match="Jira API error"):
                fetch_jira_issue_data("PROJ-401", config=config, state_dir=tmp_path)

    def test_http_500_with_issue_key_suffix_404_is_not_not_found_error(self, tmp_path: Path) -> None:
        config = self._make_config()
        with patch(
            "agentic_devtools.tools.jira.fetch_issue_context",
            side_effect=Exception("HTTP 500 for issue PROJ-404"),
        ):
            with pytest.raises(RuntimeError, match="Jira API error"):
                fetch_jira_issue_data("PROJ-404", config=config, state_dir=tmp_path)

    def test_status_code_from_exception_response_is_used(self, tmp_path: Path) -> None:
        config = self._make_config()
        exc = RuntimeError("request failed")
        setattr(exc, "response", SimpleNamespace(status_code=403))
        with patch("agentic_devtools.tools.jira.fetch_issue_context", side_effect=exc):
            with pytest.raises(RuntimeError, match="authentication failed"):
                fetch_jira_issue_data("PROJ-1", config=config, state_dir=tmp_path)

    def test_persists_response_files(self, tmp_path: Path) -> None:
        config = self._make_config()
        issue = self._make_issue(key="PROJ-50", is_subtask=True, parent_key="PROJ-49")
        parent = {"key": "PROJ-49", "fields": {"summary": "Parent"}}
        epic = {"key": "PROJ-1", "fields": {"summary": "Epic"}}
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": parent, "epic_issue": epic, "remote_links": []}

        with patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx):
            fetch_jira_issue_data("PROJ-50", config=config, state_dir=tmp_path)

        assert (tmp_path / "temp-get-issue-details-response.json").exists()
        assert (tmp_path / "temp-get-parent-issue-details-response.json").exists()
        # epic_issue from context is None in this case (subtask path uses parent's customfield)
        # but epic was returned in ctx, so it should be persisted
        assert (tmp_path / "temp-get-epic-details-response.json").exists()


class TestFetchJiraEdgeCases:
    """Additional edge case tests for fetch_jira_issue_data."""

    def _make_config(self) -> MagicMock:
        config = MagicMock()
        config.base_url = "https://jira.example.com"
        config.headers = {"Authorization": "Basic abc123"}
        config.ssl_verify = True
        config.requests_module = MagicMock()
        return config

    def test_subtask_without_parent_issue_resolved(self, tmp_path: Path) -> None:
        """Subtask where parent_issue is None still extracts parent_key from fields."""
        config = self._make_config()
        issue = {
            "key": "P-2",
            "fields": {
                "summary": "Sub",
                "description": "Desc",
                "issuetype": {"name": "Sub-task", "subtask": True},
                "status": {"name": "Open"},
                "labels": [],
                "comment": {"comments": []},
                "parent": {"key": "P-1"},
            },
        }
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": None, "epic_issue": None, "remote_links": []}

        with patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx):
            result = fetch_jira_issue_data("P-2", config=config, state_dir=tmp_path)

        assert result["parent_key"] == "P-1"
        assert result["parent_summary"] is None

    def test_generic_http_error_raises_runtime(self, tmp_path: Path) -> None:
        config = self._make_config()
        with patch(
            "agentic_devtools.tools.jira.fetch_issue_context",
            side_effect=Exception("Connection timeout"),
        ):
            with pytest.raises(RuntimeError, match="Jira API error"):
                fetch_jira_issue_data("P-1", config=config, state_dir=tmp_path)

    def test_fields_none_in_issue(self, tmp_path: Path) -> None:
        """Handle issue with fields=None gracefully."""
        config = self._make_config()
        issue = {"key": "P-1", "fields": None}
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": None, "epic_issue": None, "remote_links": []}

        with patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx):
            result = fetch_jira_issue_data("P-1", config=config, state_dir=tmp_path)

        assert result["summary"] == ""
        assert result["labels"] == []
        assert result["comments"] == []

    def test_acceptance_criteria_extracted(self, tmp_path: Path) -> None:
        config = self._make_config()
        issue = {
            "key": "P-3",
            "fields": {
                "summary": "Issue",
                "description": "## Acceptance Criteria\n- Criterion 1",
                "issuetype": {"name": "Story", "subtask": False},
                "status": {"name": "Open"},
                "labels": [],
                "comment": {"comments": []},
            },
        }
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": None, "epic_issue": None, "remote_links": []}

        with patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx):
            result = fetch_jira_issue_data("P-3", config=config, state_dir=tmp_path)

        assert result["acceptance_criteria"] is not None
        assert "Criterion 1" in result["acceptance_criteria"]


class TestFetchJiraIssueDataBranches:
    """Cover remaining branch conditions."""

    def _make_config(self) -> MagicMock:
        config = MagicMock()
        config.base_url = "https://jira.example.com"
        config.headers = {"Authorization": "Basic abc123"}
        config.ssl_verify = True
        config.requests_module = MagicMock()
        return config

    def test_labels_not_list_gives_empty(self, tmp_path: Path) -> None:
        config = self._make_config()
        issue = {
            "key": "P-1",
            "fields": {
                "summary": "X",
                "description": "D",
                "issuetype": {"name": "Story", "subtask": False},
                "status": {"name": "Open"},
                "labels": "not-a-list",
                "comment": {"comments": []},
            },
        }
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": None, "epic_issue": None, "remote_links": []}
        with patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx):
            result = fetch_jira_issue_data("P-1", config=config, state_dir=tmp_path)
        assert result["labels"] == []

    def test_config_none_calls_build(self, tmp_path: Path) -> None:
        """When config is None, _build_jira_config is called."""
        mock_config = MagicMock()
        mock_config.base_url = "https://jira.example.com"
        mock_config.headers = {"Authorization": "Basic x"}
        mock_config.ssl_verify = True
        mock_config.requests_module = MagicMock()
        issue = {
            "key": "P-1",
            "fields": {
                "summary": "X",
                "description": "D",
                "issuetype": {"name": "Story", "subtask": False},
                "status": {"name": "Open"},
                "labels": [],
                "comment": {"comments": []},
            },
        }
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": None, "epic_issue": None, "remote_links": []}
        with (
            patch("agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config", return_value=mock_config),
            patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx),
        ):
            result = fetch_jira_issue_data("P-1", config=None, state_dir=tmp_path)
        assert result["key"] == "P-1"

    def test_persist_oserror_logged(self, tmp_path: Path) -> None:
        """OSError during persist is logged but doesn't raise."""
        config = self._make_config()
        issue = {
            "key": "P-1",
            "fields": {
                "summary": "X",
                "description": "",
                "issuetype": {"name": "Story", "subtask": False},
                "status": {"name": "Open"},
                "labels": [],
                "comment": {"comments": []},
            },
        }
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": None, "epic_issue": None, "remote_links": []}
        # Use a path that doesn't allow writes
        with (
            patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx),
            patch("pathlib.Path.mkdir", side_effect=OSError("permission denied")),
        ):
            # Should not raise, just warn
            result = fetch_jira_issue_data("P-1", config=config, state_dir=tmp_path)
        assert result["key"] == "P-1"

    def test_subtask_with_parent_issue_none_and_no_parent_field(self, tmp_path: Path) -> None:
        """Subtask with parent_issue=None and no parent field -> no parent_key."""
        config = self._make_config()
        issue = {
            "key": "P-2",
            "fields": {
                "summary": "Sub",
                "description": "Desc",
                "issuetype": {"name": "Sub-task", "subtask": True},
                "status": {"name": "Open"},
                "labels": [],
                "comment": {"comments": []},
                # No 'parent' field
            },
        }
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": None, "epic_issue": None, "remote_links": []}
        with patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx):
            result = fetch_jira_issue_data("P-2", config=config, state_dir=tmp_path)
        assert result["parent_key"] is None


class TestParentIssueNoFields:
    """When parent_issue has no valid fields dict, fall back to issue's parent field."""

    def _make_config(self) -> MagicMock:
        config = MagicMock()
        config.base_url = "https://jira.example.com"
        config.headers = {"Authorization": "Basic abc123"}
        config.ssl_verify = True
        config.requests_module = MagicMock()
        return config

    def test_parent_issue_with_no_fields_extracts_from_issue_parent(self, tmp_path: Path) -> None:
        config = self._make_config()
        issue = {
            "key": "P-2",
            "fields": {
                "summary": "Sub",
                "description": "",
                "issuetype": {"name": "Sub-task", "subtask": True},
                "status": {"name": "Open"},
                "labels": [],
                "comment": {"comments": []},
                "parent": {"key": "P-1"},
            },
        }
        # parent_issue exists but fields is None/missing
        parent_issue = {"key": "P-1"}  # no "fields" key
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": parent_issue, "epic_issue": None, "remote_links": []}
        with patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx):
            result = fetch_jira_issue_data("P-2", config=config, state_dir=tmp_path)
        assert result["parent_key"] == "P-1"


class TestJiraBranchConditions:
    """Cover remaining branch conditions in fetch_jira_issue_data."""

    def _make_config(self) -> MagicMock:
        config = MagicMock()
        config.base_url = "https://jira.example.com"
        config.headers = {"Authorization": "Basic abc123"}
        config.ssl_verify = True
        config.requests_module = MagicMock()
        return config

    def test_state_dir_none_skips_persist(self) -> None:
        """When state_dir is None, no persistence happens."""
        config = self._make_config()
        issue = {
            "key": "P-1",
            "fields": {
                "summary": "X",
                "description": "",
                "issuetype": {"name": "Story", "subtask": False},
                "status": {"name": "Open"},
                "labels": [],
                "comment": {"comments": []},
            },
        }
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": None, "epic_issue": None, "remote_links": []}
        with patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx):
            result = fetch_jira_issue_data("P-1", config=config, state_dir=None)
        assert result["key"] == "P-1"

    def test_comment_non_dict_in_list_skipped(self) -> None:
        """Non-dict items in comments list are skipped."""
        config = self._make_config()
        issue = {
            "key": "P-1",
            "fields": {
                "summary": "X",
                "description": "",
                "issuetype": {"name": "Story", "subtask": False},
                "status": {"name": "Open"},
                "labels": [],
                "comment": {"comments": ["not-a-dict", {"id": "1", "body": "real", "created": "2024-01-01"}]},
            },
        }
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": None, "epic_issue": None, "remote_links": []}
        with patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx):
            result = fetch_jira_issue_data("P-1", config=config, state_dir=None)
        assert len(result["comments"]) == 1

    def test_raw_comments_not_list(self) -> None:
        """When comments.comments is not a list, return empty."""
        config = self._make_config()
        issue = {
            "key": "P-1",
            "fields": {
                "summary": "X",
                "description": "",
                "issuetype": {"name": "Story", "subtask": False},
                "status": {"name": "Open"},
                "labels": [],
                "comment": {"comments": "not-a-list"},
            },
        }
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": None, "epic_issue": None, "remote_links": []}
        with patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx):
            result = fetch_jira_issue_data("P-1", config=config, state_dir=None)
        assert result["comments"] == []

    def test_comments_truncated_to_30_newest_chronological(self) -> None:
        """More than 30 Jira comments are truncated to the 30 newest, chronological."""
        config = self._make_config()
        raw_comments = [{"id": str(i), "body": f"c{i}", "created": f"2024-01-{i:02d}"} for i in range(1, 36)]
        issue = {
            "key": "P-1",
            "fields": {
                "summary": "X",
                "description": "",
                "issuetype": {"name": "Story", "subtask": False},
                "status": {"name": "Open"},
                "labels": [],
                "comment": {"comments": raw_comments},
            },
        }
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": None, "epic_issue": None, "remote_links": []}
        with patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx):
            result = fetch_jira_issue_data("P-1", config=config, state_dir=None)
        assert len(result["comments"]) == 30
        # Keeps the 30 newest (6-35) in chronological order.
        assert result["comments"][0]["comment_id"] == "6"
        assert result["comments"][-1]["comment_id"] == "35"

    def test_parent_data_not_dict_no_parent_key(self, tmp_path: Path) -> None:
        """When parent data in fields is not a dict, parent_key stays None."""
        config = self._make_config()
        issue = {
            "key": "P-2",
            "fields": {
                "summary": "Sub",
                "description": "",
                "issuetype": {"name": "Sub-task", "subtask": True},
                "status": {"name": "Open"},
                "labels": [],
                "comment": {"comments": []},
                "parent": "not-a-dict",
            },
        }
        # parent_issue present but fields is not a dict
        parent_issue = {"key": "P-1", "fields": "broken"}
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": parent_issue, "epic_issue": None, "remote_links": []}
        with patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx):
            result = fetch_jira_issue_data("P-2", config=config, state_dir=tmp_path)
        # parent_data is "not-a-dict" so isinstance check fails
        assert result["parent_key"] is None

    def test_epic_issue_no_fields(self, tmp_path: Path) -> None:
        """Epic issue without fields dict falls back to issue epic link."""
        config = self._make_config()
        issue = {
            "key": "P-1",
            "fields": {
                "summary": "X",
                "description": "",
                "issuetype": {"name": "Story", "subtask": False},
                "status": {"name": "Open"},
                "labels": [],
                "comment": {"comments": []},
                "customfield_10008": "E-1",
            },
        }
        epic_issue = {"key": "E-1"}  # No "fields"
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": None, "epic_issue": epic_issue, "remote_links": []}
        with patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx):
            result = fetch_jira_issue_data("P-1", config=config, state_dir=tmp_path)
        assert result["epic_key"] == "E-1"

    def test_epic_link_empty_string(self, tmp_path: Path) -> None:
        """Parent's epic link field is empty string → no epic_key from link."""
        config = self._make_config()
        issue = {
            "key": "P-2",
            "fields": {
                "summary": "Sub",
                "description": "",
                "issuetype": {"name": "Sub-task", "subtask": True},
                "status": {"name": "Open"},
                "labels": [],
                "comment": {"comments": []},
                "parent": {"key": "P-1"},
            },
        }
        parent_issue = {"key": "P-1", "fields": {"summary": "Parent", "customfield_10008": ""}}
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": parent_issue, "epic_issue": None, "remote_links": []}
        with patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=ctx):
            result = fetch_jira_issue_data("P-2", config=config, state_dir=tmp_path)
        assert result["epic_key"] is None


class TestSubtaskEpicFetchBranches:
    """Branch coverage for epic fetch in subtask path (lines 252-264)."""

    def _make_config(self) -> Any:
        from unittest.mock import MagicMock

        from agentic_devtools.tools.jira import JiraConfig

        return JiraConfig(
            base_url="https://jira.example.com",
            headers={"Authorization": "******"},
            ssl_verify=True,
            requests_module=MagicMock(),
        )

    def _make_subtask_with_epic_link(self, key: str = "SUB-1", parent_key: str = "P-1") -> dict[str, Any]:
        issue = {
            "key": key,
            "fields": {
                "summary": "Subtask summary",
                "description": "Subtask description",
                "issuetype": {"name": "Sub-task", "subtask": True},
                "status": {"name": "Open"},
                "labels": [],
                "comment": {"comments": []},
                "parent": {"key": parent_key},
            },
        }
        parent = {"key": parent_key, "fields": {"summary": "Parent", "customfield_10008": "EPIC-1"}}
        ctx: dict[str, Any] = {"issue": issue, "parent_issue": parent, "epic_issue": None, "remote_links": []}
        return ctx

    def test_fetched_epic_not_dict_no_summary(self) -> None:
        """Branch 252->267: fetched_epic is not a dict → epic_summary stays None."""
        from unittest.mock import patch

        from agentic_devtools.orchestration.nodes._issue_retrieval import fetch_jira_issue_data

        config = self._make_config()
        ctx: dict[str, Any] = self._make_subtask_with_epic_link()
        epic_ctx: dict[str, Any] = {"issue": None, "parent_issue": None, "epic_issue": None, "remote_links": []}

        with patch("agentic_devtools.tools.jira.fetch_issue_context", side_effect=[ctx, epic_ctx]):
            result = fetch_jira_issue_data("SUB-1", config=config)

        assert result["epic_key"] == "EPIC-1"
        assert result["epic_summary"] is None

    def test_state_dir_none_skips_epic_persist(self) -> None:
        """Branch 253->255: state_dir is None → no persist, but summary still extracted."""
        from unittest.mock import patch

        from agentic_devtools.orchestration.nodes._issue_retrieval import fetch_jira_issue_data

        config = self._make_config()
        ctx: dict[str, Any] = self._make_subtask_with_epic_link()
        epic_ctx: dict[str, Any] = {
            "issue": {"key": "EPIC-1", "fields": {"summary": "Epic title"}},
            "parent_issue": None,
            "epic_issue": None,
            "remote_links": [],
        }

        with patch("agentic_devtools.tools.jira.fetch_issue_context", side_effect=[ctx, epic_ctx]):
            result = fetch_jira_issue_data("SUB-1", config=config, state_dir=None)

        assert result["epic_key"] == "EPIC-1"
        assert result["epic_summary"] == "Epic title"

    def test_epic_fields_not_dict_no_summary(self) -> None:
        """Branch 256->267: epic fields is not a dict → epic_summary stays None."""
        from unittest.mock import patch

        from agentic_devtools.orchestration.nodes._issue_retrieval import fetch_jira_issue_data

        config = self._make_config()
        ctx: dict[str, Any] = self._make_subtask_with_epic_link()
        epic_ctx: dict[str, Any] = {
            "issue": {"key": "EPIC-1", "fields": None},
            "parent_issue": None,
            "epic_issue": None,
            "remote_links": [],
        }

        with patch("agentic_devtools.tools.jira.fetch_issue_context", side_effect=[ctx, epic_ctx]):
            result = fetch_jira_issue_data("SUB-1", config=config)

        assert result["epic_key"] == "EPIC-1"
        assert result["epic_summary"] is None


class TestFetchJiraIssueDataCtxShape:
    """fetch_issue_context returning unexpected shape raises RuntimeError."""

    def _valid_config(self) -> Any:
        cfg = MagicMock()
        cfg.base_url = "https://jira.example.com"
        cfg.headers = {"Authorization": "Basic x"}
        return cfg

    def test_non_dict_ctx_raises_runtime_error(self) -> None:
        with (
            patch(
                "agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config",
                return_value=self._valid_config(),
            ),
            patch(
                "agentic_devtools.tools.jira.fetch_issue_context",
                return_value=["unexpected", "list"],
            ),
            pytest.raises(RuntimeError, match="unexpected shape"),
        ):
            fetch_jira_issue_data("PROJECT-1")

    def test_dict_ctx_missing_issue_key_raises_runtime_error(self) -> None:
        with (
            patch(
                "agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config",
                return_value=self._valid_config(),
            ),
            patch(
                "agentic_devtools.tools.jira.fetch_issue_context",
                return_value={"parent_issue": None, "epic_issue": None},
            ),
            pytest.raises(RuntimeError, match="unexpected shape"),
        ):
            fetch_jira_issue_data("PROJECT-1")

    def test_ctx_missing_optional_keys_uses_none(self) -> None:
        """parent_issue and epic_issue default to None when absent from ctx."""
        minimal_issue: dict[str, Any] = {
            "key": "PROJECT-1",
            "fields": {
                "summary": "Hello",
                "description": "Desc",
                "issuetype": {"name": "Task", "subtask": False},
                "status": {"name": "Open"},
                "labels": [],
                "comment": {},
            },
        }
        with (
            patch(
                "agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config",
                return_value=self._valid_config(),
            ),
            patch(
                "agentic_devtools.tools.jira.fetch_issue_context",
                return_value={"issue": minimal_issue},
            ),
        ):
            result = fetch_jira_issue_data("PROJECT-1")
        assert result["parent_key"] is None
        assert result["epic_key"] is None

    def test_empty_issue_dict_raises_runtime_error(self) -> None:
        """A malformed successful response (issue coerced to {}) is a retrieval error."""
        with (
            patch(
                "agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config",
                return_value=self._valid_config(),
            ),
            patch(
                "agentic_devtools.tools.jira.fetch_issue_context",
                return_value={"issue": {}},
            ),
            pytest.raises(RuntimeError, match="empty or malformed issue payload"),
        ):
            fetch_jira_issue_data("PROJECT-1")

    def test_non_dict_issue_raises_runtime_error(self) -> None:
        """A non-dict issue payload is a retrieval error, not an empty issue."""
        with (
            patch(
                "agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config",
                return_value=self._valid_config(),
            ),
            patch(
                "agentic_devtools.tools.jira.fetch_issue_context",
                return_value={"issue": "not-a-dict"},
            ),
            pytest.raises(RuntimeError, match="empty or malformed issue payload"),
        ):
            fetch_jira_issue_data("PROJECT-1")


class TestFetchJiraIssueDataNewestComments:
    """When the issue has more comments than the embedded page, fetch the newest page."""

    def _valid_config(self) -> Any:
        cfg = MagicMock()
        cfg.base_url = "https://jira.example.com"
        cfg.headers = {"Authorization": "Basic x"}
        return cfg

    def _issue_with_comment_total(self, total: int, embedded: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "key": "PROJECT-1",
            "fields": {
                "summary": "Hello",
                "description": "Desc",
                "issuetype": {"name": "Task", "subtask": False},
                "status": {"name": "Open"},
                "labels": [],
                "comment": {"comments": embedded, "total": total},
            },
        }

    def test_total_exceeds_page_fetches_newest(self) -> None:
        """total > embedded count triggers a newest-page fetch that replaces comments."""
        embedded = [{"id": "1", "body": "old", "created": "2024-01-01"}]
        newest = [{"id": "99", "body": "new", "created": "2024-06-01"}]
        with (
            patch(
                "agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config",
                return_value=self._valid_config(),
            ),
            patch(
                "agentic_devtools.tools.jira.fetch_issue_context",
                return_value={"issue": self._issue_with_comment_total(51, embedded)},
            ),
            patch(
                "agentic_devtools.orchestration.nodes._issue_retrieval._fetch_newest_jira_comments",
                return_value=newest,
            ) as mock_fetch,
        ):
            result = fetch_jira_issue_data("PROJECT-1")
        mock_fetch.assert_called_once()
        assert result["comments"] == [{"comment_id": "99", "body": "new", "created_at": "2024-06-01"}]

    def test_total_exceeds_page_but_fetch_fails_uses_embedded(self) -> None:
        """When the newest-page fetch returns None, the embedded comments are kept."""
        embedded = [{"id": "1", "body": "old", "created": "2024-01-01"}]
        with (
            patch(
                "agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config",
                return_value=self._valid_config(),
            ),
            patch(
                "agentic_devtools.tools.jira.fetch_issue_context",
                return_value={"issue": self._issue_with_comment_total(51, embedded)},
            ),
            patch(
                "agentic_devtools.orchestration.nodes._issue_retrieval._fetch_newest_jira_comments",
                return_value=None,
            ),
        ):
            result = fetch_jira_issue_data("PROJECT-1")
        assert result["comments"] == [{"comment_id": "1", "body": "old", "created_at": "2024-01-01"}]


class TestFetchJiraIssueDataFieldCoercion:
    """Non-string status/issue_type/comment-body values are coerced safely."""

    def _valid_config(self) -> Any:
        cfg = MagicMock()
        cfg.base_url = "https://jira.example.com"
        cfg.headers = {"Authorization": "Basic x"}
        return cfg

    def test_null_status_and_issue_type_coerced_to_empty(self) -> None:
        issue: dict[str, Any] = {
            "key": "PROJECT-1",
            "fields": {
                "summary": "Hello",
                "description": "Desc",
                "issuetype": {"name": None, "subtask": False},
                "status": {"name": None},
                "labels": [],
                "comment": {},
            },
        }
        with (
            patch(
                "agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config",
                return_value=self._valid_config(),
            ),
            patch(
                "agentic_devtools.tools.jira.fetch_issue_context",
                return_value={"issue": issue},
            ),
        ):
            result = fetch_jira_issue_data("PROJECT-1")
        assert result["status"] == ""
        assert result["issue_type"] == ""

    def test_adf_comment_body_converted_to_text(self) -> None:
        adf_body = {
            "type": "doc",
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Hello ADF"}]}],
        }
        issue: dict[str, Any] = {
            "key": "PROJECT-1",
            "fields": {
                "summary": "Hello",
                "description": "Desc",
                "issuetype": {"name": "Task", "subtask": False},
                "status": {"name": "Open"},
                "labels": [],
                "comment": {"comments": [{"id": "5", "body": adf_body, "created": "2024-01-01"}]},
            },
        }
        with (
            patch(
                "agentic_devtools.orchestration.nodes._issue_retrieval._build_jira_config",
                return_value=self._valid_config(),
            ),
            patch(
                "agentic_devtools.tools.jira.fetch_issue_context",
                return_value={"issue": issue},
            ),
        ):
            result = fetch_jira_issue_data("PROJECT-1")
        assert result["comments"][0]["body"].strip() == "Hello ADF"
