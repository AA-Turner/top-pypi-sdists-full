"""Tests for agentic_devtools.adapters.jira_adapter.JiraAdapter."""

from __future__ import annotations

from typing import Any, cast
from unittest.mock import MagicMock

import pytest

from agentic_devtools.adapters.jira_adapter import JiraAdapter
from agentic_devtools.adapters.types import Comment
from agentic_devtools.tools.jira import JiraConfig


def _make_config(mock_requests: MagicMock | None = None, base_url: str = "https://jira.example.com") -> JiraConfig:
    """Build a JiraConfig with an injectable mock requests module."""
    return JiraConfig(
        base_url=base_url,
        headers={"Authorization": "Basic xxx"},
        ssl_verify=False,
        requests_module=mock_requests or MagicMock(),
    )


class TestJiraAdapter:
    """Tests for the JiraAdapter concrete implementation."""

    def test_constructor_raises_on_empty_project_key(self) -> None:
        """Raises ValueError when project_key is empty and create_issue is called."""
        adapter = JiraAdapter(config=_make_config(), project_key="")
        with pytest.raises(ValueError, match="project_key"):
            adapter.create_issue("Title", "Desc")

    def test_constructor_accepts_none_project_key(self) -> None:
        """Constructor accepts None project_key but create_issue still raises."""
        adapter = JiraAdapter(config=_make_config(), project_key=None)
        with pytest.raises(ValueError, match="project_key"):
            adapter.create_issue("T", "D")

    def test_create_issue_raises_without_project_key(self) -> None:
        """create_issue raises ValueError when project_key was not provided."""
        adapter = JiraAdapter(config=_make_config())
        with pytest.raises(ValueError, match="project_key"):
            adapter.create_issue("Title", "Desc")

    def test_get_issue_works_without_project_key(self) -> None:
        """get_issue works even when project_key is not set."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "fields": {"summary": "Issue"},
        }
        mock_requests.get.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests))
        detail = adapter.get_issue("PROJ-1")
        assert detail["title"] == "Issue"

    def test_add_comment_works_without_project_key(self) -> None:
        """add_comment works even when project_key is not set."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "555"}
        mock_requests.post.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests))
        result = adapter.add_comment("PROJ-1", "Hello")
        assert result["comment_id"] == "555"

    def test_create_issue_delegates_and_maps_result(self) -> None:
        """create_issue calls jira.create_issue and maps to IssueResult."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "PROJ-42"}
        mock_requests.post.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ")
        result = adapter.create_issue("My title", "My description", labels=["bug"])

        assert result["issue_id"] == "PROJ-42"
        assert result["url"] == "https://jira.example.com/browse/PROJ-42"

    def test_create_issue_without_labels(self) -> None:
        """create_issue passes empty list when labels is None."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "PROJ-1"}
        mock_requests.post.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ")
        result = adapter.create_issue("Title", "Desc")

        assert result["issue_id"] == "PROJ-1"
        call_kwargs = mock_requests.post.call_args[1]
        assert call_kwargs["json"]["fields"]["labels"] == []

    def test_get_issue_maps_fields(self) -> None:
        """get_issue maps Jira fields to IssueDetail."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "fields": {
                "summary": "Test issue",
                "description": "A description",
                "labels": ["bug", "urgent"],
                "status": {"name": "Open"},
                "issuetype": {"subtask": False},
                "comment": {
                    "comments": [
                        {"id": "100", "body": "First comment", "created": "2026-01-01T00:00:00Z"},
                    ],
                },
            },
        }
        mock_requests.get.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ")
        detail = adapter.get_issue("PROJ-42")

        assert detail["issue_id"] == "PROJ-42"
        assert detail["title"] == "Test issue"
        assert detail["description"] == "A description"
        assert detail["labels"] == ["bug", "urgent"]
        assert detail["status"] == "Open"
        assert detail["url"] == "https://jira.example.com/browse/PROJ-42"
        assert len(detail["comments"]) == 1
        assert detail["comments"][0]["comment_id"] == "100"
        assert detail["comments"][0]["body"] == "First comment"

    def test_get_issue_handles_missing_optional_fields(self) -> None:
        """get_issue defaults gracefully when optional fields are absent."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "fields": {
                "summary": "Minimal issue",
            },
        }
        mock_requests.get.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ")
        detail = adapter.get_issue("PROJ-99")

        assert detail["title"] == "Minimal issue"
        assert detail["description"] == ""
        assert detail["labels"] == []
        assert detail["status"] == ""
        assert detail["comments"] == []

    def test_get_issue_handles_none_description(self) -> None:
        """get_issue converts None description to empty string."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "fields": {
                "summary": "Issue",
                "description": None,
            },
        }
        mock_requests.get.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ")
        detail = adapter.get_issue("PROJ-1")
        assert detail["description"] == ""

    def test_get_issue_coerces_adf_description_to_string(self) -> None:
        """get_issue coerces non-string description (e.g. ADF dict) to str."""
        adf_doc = {
            "type": "doc",
            "version": 1,
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Hello"}]}],
        }
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "fields": {
                "summary": "Issue",
                "description": adf_doc,
            },
        }
        mock_requests.get.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ")
        detail = adapter.get_issue("PROJ-1")
        assert isinstance(detail["description"], str)
        assert detail["description"] != ""

    def test_get_issue_handles_non_dict_status(self) -> None:
        """get_issue handles non-dict status field gracefully."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "fields": {
                "summary": "Issue",
                "status": "not-a-dict",
            },
        }
        mock_requests.get.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ")
        detail = adapter.get_issue("PROJ-1")
        assert detail["status"] == ""

    def test_get_issue_handles_non_dict_comment(self) -> None:
        """get_issue handles non-dict comment field gracefully."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "fields": {
                "summary": "Issue",
                "comment": "not-a-dict",
            },
        }
        mock_requests.get.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ")
        detail = adapter.get_issue("PROJ-1")
        assert detail["comments"] == []

    def test_get_issue_handles_null_comments_inside_comment_dict(self) -> None:
        """get_issue normalizes null comments list to empty."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "fields": {
                "summary": "Issue",
                "comment": {"comments": None},
            },
        }
        mock_requests.get.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ")
        detail = adapter.get_issue("PROJ-1")
        assert detail["comments"] == []

    def test_get_issue_skips_non_dict_comment_entries(self) -> None:
        """get_issue skips non-dict entries in the comments list."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "fields": {
                "summary": "Issue",
                "comment": {
                    "comments": [
                        {"id": "100", "body": "Good", "created": "2026-01-01"},
                        "bad-entry",
                        {"id": "200", "body": "Also good", "created": "2026-01-02"},
                    ],
                },
            },
        }
        mock_requests.get.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ")
        detail = adapter.get_issue("PROJ-1")
        assert len(detail["comments"]) == 2
        assert detail["comments"][0]["comment_id"] == "100"
        assert detail["comments"][1]["comment_id"] == "200"

    def test_get_issue_coerces_non_string_comment_body(self) -> None:
        """get_issue coerces non-string comment body (e.g. ADF dict) to str."""
        adf_body = {"type": "doc", "content": []}
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "fields": {
                "summary": "Issue",
                "comment": {
                    "comments": [
                        {"id": "100", "body": adf_body, "created": "2026-01-01"},
                        {"id": "200", "body": None, "created": "2026-01-02"},
                    ],
                },
            },
        }
        mock_requests.get.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ")
        detail = adapter.get_issue("PROJ-1")
        assert len(detail["comments"]) == 2
        # ADF dict coerced to str representation
        assert isinstance(detail["comments"][0]["body"], str)
        assert detail["comments"][0]["body"] != ""
        # None coerced to empty string
        assert detail["comments"][1]["body"] == ""

    def test_get_issue_coerces_non_string_comment_created(self) -> None:
        """get_issue coerces non-string created timestamp to str."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "fields": {
                "summary": "Issue",
                "comment": {
                    "comments": [
                        {"id": "100", "body": "Hi", "created": 12345},
                        {"id": "200", "body": "Hi", "created": None},
                    ],
                },
            },
        }
        mock_requests.get.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ")
        detail = adapter.get_issue("PROJ-1")
        assert detail["comments"][0]["created_at"] == "12345"
        assert detail["comments"][1]["created_at"] == ""

    def test_get_issue_handles_null_labels(self) -> None:
        """get_issue normalizes null labels to empty list."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "fields": {
                "summary": "Issue",
                "labels": None,
            },
        }
        mock_requests.get.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ")
        detail = adapter.get_issue("PROJ-1")
        assert detail["labels"] == []

    def test_get_issue_filters_non_string_labels(self) -> None:
        """get_issue filters out non-string entries from labels list."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "fields": {
                "summary": "Issue",
                "labels": ["bug", 42, "feature", None],
            },
        }
        mock_requests.get.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ")
        detail = adapter.get_issue("PROJ-1")
        assert detail["labels"] == ["bug", "feature"]

    def test_get_issue_handles_null_fields(self) -> None:
        """get_issue returns empty defaults when Jira returns {"fields": null}."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"fields": None}
        mock_requests.get.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ")
        detail = adapter.get_issue("PROJ-1")

        assert detail["title"] == ""
        assert detail["description"] == ""
        assert detail["labels"] == []
        assert detail["status"] == ""
        assert detail["comments"] == []

    def test_get_issue_handles_null_summary_and_status_name(self) -> None:
        """get_issue normalizes null summary/status.name to empty strings."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "fields": {
                "summary": None,
                "status": {"name": None},
            },
        }
        mock_requests.get.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ")
        detail = adapter.get_issue("PROJ-1")

        assert detail["title"] == ""
        assert detail["status"] == ""

    def test_get_issue_coerces_non_string_summary_and_status_name(self) -> None:
        """get_issue coerces non-string summary/status.name to strings."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "fields": {
                "summary": 123,
                "status": {"name": 456},
            },
        }
        mock_requests.get.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ")
        detail = adapter.get_issue("PROJ-1")

        assert detail["title"] == "123"
        assert detail["status"] == "456"

    def test_get_issue_handles_non_dict_response_body(self) -> None:
        """get_issue returns empty defaults when Jira returns a non-dict body (normalized by fetch_issue_context)."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = ["unexpected", "list"]
        mock_requests.get.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ")
        detail = adapter.get_issue("PROJ-1")

        assert detail["title"] == ""
        assert detail["description"] == ""
        assert detail["labels"] == []
        assert detail["status"] == ""
        assert detail["comments"] == []

    def test_add_comment_delegates_and_maps_result(self) -> None:
        """add_comment calls jira.add_comment and maps to CommentResult."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "555"}
        mock_requests.post.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ")
        result = adapter.add_comment("PROJ-42", "Hello world")

        assert result["comment_id"] == "555"

    def test_list_issues_raises_not_implemented(self) -> None:
        """list_issues raises NotImplementedError."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        with pytest.raises(NotImplementedError, match="not yet implemented"):
            adapter.list_issues()

    def test_custom_issue_type(self) -> None:
        """Constructor accepts a custom issue_type."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "PROJ-1"}
        mock_requests.post.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ", issue_type="Bug")
        adapter.create_issue("Bug title", "Bug desc")

        call_kwargs = mock_requests.post.call_args[1]
        assert call_kwargs["json"]["fields"]["issuetype"]["name"] == "Bug"

    def test_normalize_happy_path_all_fields(self) -> None:
        """normalize() returns valid NormalizedIssue with correct mappings."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "Test Issue",
                "description": "A description",
                "status": "Open",
                "labels": ["bug", "critical"],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [{"comment_id": "c1", "body": "hello", "created_at": "2024-01-01"}],
                "raw": {
                    "fields": {
                        "status": {"name": "In Progress"},
                        "description": "Raw description",
                        "created": "2024-01-01T00:00:00Z",
                        "updated": "2024-01-02T00:00:00Z",
                        "issuetype": {"name": "Bug", "subtask": False},
                        "priority": {"name": "High"},
                        "components": [{"name": "Backend"}],
                    }
                },
            }
        )
        assert result.issue_id == "PROJ-1"
        assert result.title == "Test Issue"
        assert result.url == "https://jira.example.com/browse/PROJ-1"
        assert result.provider == "jira"
        assert result.status == "in progress"
        assert result.description == "A description"
        assert result.labels == ["bug", "critical"]
        assert result.comments == [{"comment_id": "c1", "body": "hello", "created_at": "2024-01-01"}]
        assert result.created_at == "2024-01-01T00:00:00Z"
        assert result.updated_at == "2024-01-02T00:00:00Z"
        assert result.raw["fields"]["priority"]["name"] == "High"
        # FR-005: nested Jira issue type copied to top-level raw["issue_type"].
        assert result.raw["issue_type"] == "Bug"

    def test_normalize_copies_nested_issue_type_without_mutating_original(self) -> None:
        """normalize() copies nested issuetype name to top-level and does not mutate caller raw (FR-005/T017)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        original_raw: dict[str, object] = {
            "fields": {"status": {"name": "Open"}, "issuetype": {"name": "Story", "subtask": False}},
        }
        result = adapter.normalize(
            {
                "issue_id": "PROJ-2",
                "title": "Story Issue",
                "description": "desc",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-2",
                "comments": [],
                "raw": original_raw,
            }
        )
        # Top-level key populated on the normalized copy.
        assert result.raw["issue_type"] == "Story"
        # Nested payload preserved.
        assert result.raw["fields"]["issuetype"]["name"] == "Story"
        # Caller's original raw is NOT mutated.
        assert "issue_type" not in original_raw

    def test_normalize_omits_issue_type_when_no_nested_issuetype(self) -> None:
        """No top-level issue_type is added when the nested issuetype is absent (FR-005)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        original_raw: dict[str, object] = {"fields": {"status": {"name": "Open"}}}
        result = adapter.normalize(
            {
                "issue_id": "PROJ-3",
                "title": "No Type",
                "description": "desc",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-3",
                "comments": [],
                "raw": original_raw,
            }
        )
        assert "issue_type" not in result.raw
        assert "issue_type" not in original_raw

    def test_normalize_omits_issue_type_when_nested_name_blank(self) -> None:
        """A whitespace-only nested issuetype name does not populate top-level issue_type (FR-005)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-4",
                "title": "Blank Type",
                "description": "desc",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-4",
                "comments": [],
                "raw": {"fields": {"issuetype": {"name": "   "}}},
            }
        )
        assert "issue_type" not in result.raw

        """Status extracted from raw["fields"]["status"]["name"] (FR-002 step 1)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "typed-status",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {"status": {"name": "Done"}}},
            }
        )
        assert result.status == "done"

    def test_normalize_status_from_plain_string(self) -> None:
        """Status extracted from plain string in raw["fields"]["status"] (FR-002 step 2)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "typed-status",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {"status": "Closed"}},
            }
        )
        assert result.status == "closed"

    def test_normalize_status_fallback_to_typed_field(self) -> None:
        """Status falls back to IssueDetailWithRaw.status typed field (FR-002 step 3)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Backlog",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {}},
            }
        )
        assert result.status == "backlog"

    def test_normalize_status_defaults_to_unknown(self) -> None:
        """Status defaults to 'unknown' when all sources absent (FR-002 step 4)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {}},
            }
        )
        assert result.status == "unknown"

    def test_normalize_whitespace_status_coerced_to_unknown(self) -> None:
        """Empty/whitespace-only status coerced to 'unknown' (FR-002 whitespace)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "   ",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {"status": "  "}},
            }
        )
        assert result.status == "unknown"

    def test_normalize_status_dict_with_whitespace_name_falls_through(self) -> None:
        """When raw status is a dict with whitespace-only name, falls through to typed field."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Fallback",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {"status": {"name": "   "}}},
            }
        )
        assert result.status == "fallback"

    def test_normalize_status_dict_name_with_surrounding_whitespace_is_stripped(self) -> None:
        """Status name with surrounding whitespace is stripped (FR-002 step 1)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "typed",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {"status": {"name": "  In Progress  "}}},
            }
        )
        assert result.status == "in progress"

    def test_normalize_status_plain_string_with_surrounding_whitespace_is_stripped(self) -> None:
        """Plain string status with surrounding whitespace is stripped (FR-002 step 2)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "typed",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {"status": "  Closed  "}},
            }
        )
        assert result.status == "closed"

    def test_normalize_status_typed_field_with_surrounding_whitespace_is_stripped(self) -> None:
        """Typed status field with surrounding whitespace is stripped (FR-002 step 3)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "  Backlog  ",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {}},
            }
        )
        assert result.status == "backlog"

    def test_normalize_dates_from_raw_fields(self) -> None:
        """created_at and updated_at populated from raw fields (FR-009)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {"status": {"name": "Open"}, "created": "2024-06-01", "updated": "2024-06-02"}},
            }
        )
        assert result.created_at == "2024-06-01"
        assert result.updated_at == "2024-06-02"

    def test_normalize_dates_default_to_empty_when_absent(self) -> None:
        """Dates default to '' when absent from raw fields (FR-009)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {"status": {"name": "Open"}}},
            }
        )
        assert result.created_at == ""
        assert result.updated_at == ""

    def test_normalize_description_from_typed_field(self) -> None:
        """Description extracted from typed field when non-whitespace (FR-010 step 1)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "Typed description",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {"status": {"name": "Open"}, "description": "Raw description"}},
            }
        )
        assert result.description == "Typed description"

    def test_normalize_description_fallback_to_raw(self) -> None:
        """Description falls back to raw when typed field is whitespace-only (FR-010 step 2)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "   ",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {"status": {"name": "Open"}, "description": "Raw fallback"}},
            }
        )
        assert result.description == "Raw fallback"

    def test_normalize_adf_description_coerced(self) -> None:
        """ADF dict description coerced via str(), whitespace-only → '' (FR-010 edge)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        adf_doc = {"type": "doc", "content": [{"type": "paragraph"}]}
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {"status": {"name": "Open"}, "description": adf_doc}},
            }
        )
        assert isinstance(result.description, str)
        assert result.description != ""  # str(adf_doc) is non-whitespace

    def test_normalize_labels_valid_list(self) -> None:
        """Labels extracted from typed field as-is when valid list (FR-007)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Open",
                "labels": ["bug", "feature"],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {"status": {"name": "Open"}}},
            }
        )
        assert result.labels == ["bug", "feature"]

    def test_normalize_labels_non_list_coerced(self) -> None:
        """Labels coerced to [] when typed field is non-list (FR-007 defensive)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Open",
                "labels": "not-a-list",  # type: ignore[typeddict-item]
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {"status": {"name": "Open"}}},
            }
        )
        assert result.labels == []

    def test_normalize_comments_valid_list(self) -> None:
        """Comments extracted from typed field as-is when valid list (FR-008)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        comments = cast(list[Comment], [{"comment_id": "c1", "body": "hi", "created_at": "2024-01-01"}])
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": comments,
                "raw": {"fields": {"status": {"name": "Open"}}},
            }
        )
        assert result.comments == comments

    def test_normalize_comments_non_list_coerced(self) -> None:
        """Comments coerced to [] when typed field is non-list (FR-008 defensive)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": "not-a-list",  # type: ignore[typeddict-item]
                "raw": {"fields": {"status": {"name": "Open"}}},
            }
        )
        assert result.comments == []

    def test_normalize_comments_skips_non_dict_entries(self) -> None:
        """Non-dict entries in the comments list are silently skipped (FR-008)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        mixed: list[Any] = [
            "not-a-dict",
            {"comment_id": "c1", "body": "hello", "created_at": "2024-01-01"},
            None,
        ]
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": mixed,  # type: ignore[typeddict-item]
                "raw": {"fields": {"status": {"name": "Open"}}},
            }
        )
        assert len(result.comments) == 1
        assert result.comments[0]["comment_id"] == "c1"

    def test_normalize_comments_positional_fallback_when_id_empty(self) -> None:
        """comment_id falls back to positional c{n} when dict has empty/missing id (FR-008)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        incomplete: list[Any] = [
            {"comment_id": "   ", "body": "first", "created_at": ""},
            {"body": "second", "created_at": ""},
        ]
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": incomplete,  # type: ignore[typeddict-item]
                "raw": {"fields": {"status": {"name": "Open"}}},
            }
        )
        assert result.comments[0]["comment_id"] == "c1"
        assert result.comments[1]["comment_id"] == "c2"

    def test_normalize_comments_preserves_zero_comment_id(self) -> None:
        """A falsey non-None ``comment_id`` (e.g. ``0``) is preserved and stringified."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        comments: list[Any] = [
            {"comment_id": 0, "id": 999, "body": "first", "created_at": ""},
        ]
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": comments,  # type: ignore[typeddict-item]
                "raw": {"fields": {"status": {"name": "Open"}}},
            }
        )
        assert result.comments[0]["comment_id"] == "0"

    def test_normalize_comments_created_key_fallback(self) -> None:
        """created_at falls back to raw Jira "created" key when "created_at" is absent (FR-008)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        raw_jira_comments: list[Any] = [
            {"id": "101", "body": "msg", "created": "2026-06-01T10:00:00Z"},
        ]
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": raw_jira_comments,  # type: ignore[typeddict-item]
                "raw": {"fields": {"status": {"name": "Open"}}},
            }
        )
        assert len(result.comments) == 1
        assert result.comments[0]["comment_id"] == "101"
        assert result.comments[0]["created_at"] == "2026-06-01T10:00:00Z"

    def test_normalize_comments_created_at_takes_precedence_over_created(self) -> None:
        """created_at takes precedence over "created" when both keys are present (FR-008)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        both_keys: list[Any] = [
            {"comment_id": "c1", "body": "msg", "created_at": "2026-05-01", "created": "2026-01-01"},
        ]
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": both_keys,  # type: ignore[typeddict-item]
                "raw": {"fields": {"status": {"name": "Open"}}},
            }
        )
        assert result.comments[0]["created_at"] == "2026-05-01"

    def test_normalize_labels_filters_none_items(self) -> None:
        """None items in the labels list are dropped; other items are coerced to str (FR-007)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Open",
                "labels": ["bug", None, "feature"],  # type: ignore[list-item]
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {"status": {"name": "Open"}}},
            }
        )
        assert result.labels == ["bug", "feature"]

    def test_normalize_labels_coerces_non_string_items(self) -> None:
        """Non-string, non-None label items are coerced to str (FR-007)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Open",
                "labels": ["bug", 42, True],  # type: ignore[list-item]
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {"status": {"name": "Open"}}},
            }
        )
        assert result.labels == ["bug", "42", "True"]

    def test_normalize_propagates_validation_error(self) -> None:
        """AdapterValidationError propagated when identity fields invalid (FR-006)."""
        from agentic_devtools.adapters.exceptions import AdapterValidationError

        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        with pytest.raises(AdapterValidationError):
            adapter.normalize(
                {
                    "issue_id": "",
                    "title": "T",
                    "description": "",
                    "status": "Open",
                    "labels": [],
                    "url": "https://jira.example.com/browse/PROJ-1",
                    "comments": [],
                    "raw": {"fields": {"status": {"name": "Open"}}},
                }
            )

    def test_normalize_null_issuetype_priority_components(self) -> None:
        """None values for issuetype, priority, components do not raise (FR-003)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {
                    "fields": {
                        "status": {"name": "Open"},
                        "issuetype": None,
                        "priority": None,
                        "components": None,
                    }
                },
            }
        )
        assert result.issue_id == "PROJ-1"
        assert result.raw["fields"]["issuetype"] is None
        assert result.raw["fields"]["priority"] is None
        assert result.raw["fields"]["components"] is None

    def test_normalize_none_status_defaults_to_unknown(self) -> None:
        """None status in raw and typed field defaults to 'unknown' (FR-003 + FR-002)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {"status": None}},
            }
        )
        assert result.status == "unknown"

    def test_normalize_none_description_defaults_to_empty(self) -> None:
        """None description in both typed and raw fields defaults to '' (FR-003 + FR-010)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {"status": {"name": "Open"}, "description": None}},
            }
        )
        assert result.description == ""

    def test_normalize_non_dict_raw_fields_fallback(self) -> None:
        """Non-dict raw["fields"] silently falls back to typed fields only (edge case)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "Typed desc",
                "status": "Open",
                "labels": ["a"],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": "not-a-dict"},
            }
        )
        assert result.description == "Typed desc"
        assert result.status == "open"
        assert result.labels == ["a"]

    def test_normalize_preserves_custom_fields_in_raw(self) -> None:
        """NormalizedIssue.raw contains all custom fields including customfield_* (FR-004)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        raw_payload = {
            "fields": {
                "status": {"name": "Open"},
                "customfield_10001": "Sprint 1",
                "customfield_10002": 42,
                "customfield_10003": {"value": "Option A"},
                "customfield_10004": None,
                "customfield_10005": [{"value": "v1"}, {"value": "v2"}],
            }
        }
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": raw_payload,
            }
        )
        assert result.raw["fields"]["customfield_10001"] == "Sprint 1"
        assert result.raw["fields"]["customfield_10002"] == 42
        assert result.raw["fields"]["customfield_10003"] == {"value": "Option A"}
        assert result.raw["fields"]["customfield_10004"] is None
        assert result.raw["fields"]["customfield_10005"] == [{"value": "v1"}, {"value": "v2"}]

    def test_normalize_absent_raw_key_defaults_to_empty_dict(self) -> None:
        """Absent raw key in IssueDetailWithRaw defaults to empty dict {} in output (FR-004)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "D",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
            }
        )
        assert result.raw == {}

    def test_normalize_deeply_nested_custom_field_preserved(self) -> None:
        """Deeply nested custom field (cascading select) preserved in raw (FR-004, US-4)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        cascading = {"value": "Parent", "child": {"value": "Child"}}
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {"status": {"name": "Open"}, "customfield_10050": cascading}},
            }
        )
        assert result.raw["fields"]["customfield_10050"] == cascading

    def test_normalize_custom_field_empty_list(self) -> None:
        """Custom field with empty list value normalizes without error (FR-004, US-4)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {"status": {"name": "Open"}, "customfield_10060": []}},
            }
        )
        assert result.raw["fields"]["customfield_10060"] == []

    def test_normalize_custom_field_none_value(self) -> None:
        """Custom field with None value does not cause exception (FR-004, US-4)."""
        adapter = JiraAdapter(config=_make_config(), project_key="PROJ")
        result = adapter.normalize(
            {
                "issue_id": "PROJ-1",
                "title": "T",
                "description": "",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-1",
                "comments": [],
                "raw": {"fields": {"status": {"name": "Open"}, "customfield_10070": None}},
            }
        )
        assert result.raw["fields"]["customfield_10070"] is None

    def test_get_issue_returns_raw_key(self) -> None:
        """get_issue() return includes raw key with full API response (FR-011)."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "key": "PROJ-1",
            "fields": {
                "summary": "Test",
                "status": {"name": "Open"},
                "issuetype": {"subtask": False},
                "customfield_10001": "custom-value",
            },
        }
        mock_requests.get.return_value = mock_response

        adapter = JiraAdapter(config=_make_config(mock_requests), project_key="PROJ")
        detail = adapter.get_issue("PROJ-1")
        assert "raw" in detail
        assert detail["raw"]["fields"]["customfield_10001"] == "custom-value"
        assert detail["raw"]["key"] == "PROJ-1"

    def test_require_project_key_generic_message(self) -> None:
        """_require_project_key() raises ValueError with generic message."""
        adapter = JiraAdapter(config=_make_config(), project_key="")
        with pytest.raises(ValueError, match="JiraAdapter requires a Jira project_key"):
            adapter._require_project_key()
