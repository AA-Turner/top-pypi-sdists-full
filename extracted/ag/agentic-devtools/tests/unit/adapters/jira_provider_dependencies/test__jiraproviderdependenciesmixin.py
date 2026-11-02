"""Tests for the JiraProvider dependencies capability."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from agentic_devtools.adapters.jira_provider import JiraProvider
from agentic_devtools.adapters.retry import TransientError
from tests.unit.adapters.jira_provider._fixtures import _make_mock_session, _make_response

_SLEEP = "agentic_devtools.adapters.retry.time.sleep"


class TestJiraProviderAddBlockedBy:
    """Tests for JiraProvider.add_blocked_by."""

    def test_add_blocked_by_success(self):
        session = _make_mock_session()
        get_resp = _make_response(200, {"fields": {"issuelinks": []}})
        post_resp = _make_response(201)
        session.request.side_effect = [get_resp, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        assert result.status == "linked"
        assert result.source_id == "PROJ-1"
        assert result.target_id == "PROJ-2"

    def test_add_blocked_by_dry_run(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=True)
        assert result.status == "dry-run"
        session.request.assert_not_called()

    def test_add_blocked_by_payload_direction(self):
        """Verifies POST payload has outwardIssue=blocked_by_id and inwardIssue=issue_id."""
        session = _make_mock_session()
        get_resp = _make_response(200, {"fields": {"issuelinks": []}})
        post_resp = _make_response(201)
        session.request.side_effect = [get_resp, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)

        # call_args is the last call (the POST)
        call_kwargs = session.request.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert payload["outwardIssue"]["key"] == "PROJ-1"
        assert payload["inwardIssue"]["key"] == "PROJ-2"

    def test_add_blocked_by_already_linked_via_outward(self):
        """Returns already-linked when blocked_by_id appears as outwardIssue in existing links."""
        session = _make_mock_session()
        existing = {
            "fields": {
                "issuelinks": [
                    {
                        "type": {"name": "Blocks"},
                        "outwardIssue": {"key": "PROJ-1"},
                    }
                ]
            }
        }
        session.request.return_value = _make_response(200, existing)
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        assert result.status == "already-linked"
        assert result.source_id == "PROJ-1"
        assert result.target_id == "PROJ-2"
        # Only the GET was made â€” no POST
        assert session.request.call_count == 1

    def test_add_blocked_by_inward_issue_is_opposite_direction_not_idempotent(self):
        """inwardIssue=blocked_by_id represents the opposite edge (issue_id blocks blocked_by_id).

        This is NOT the same as "issue_id is blocked by blocked_by_id", so the method
        must NOT return already-linked and must proceed to POST the new link.
        """
        session = _make_mock_session()
        existing = {
            "fields": {
                "issuelinks": [
                    {
                        "type": {"name": "Blocks"},
                        "inwardIssue": {"key": "PROJ-1"},
                    }
                ]
            }
        }
        get_resp = _make_response(200, existing)
        post_resp = _make_response(201)
        session.request.side_effect = [get_resp, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        # The existing link is the wrong direction â€” a new link must be created
        assert result.status == "linked"
        # Both GET and POST were made
        assert session.request.call_count == 2

    def test_add_blocked_by_different_blocker_not_idempotent(self):
        """A different blocker in existing links does not trigger already-linked."""
        session = _make_mock_session()
        existing = {
            "fields": {
                "issuelinks": [
                    {
                        "type": {"name": "Blocks"},
                        "outwardIssue": {"key": "PROJ-99"},
                    }
                ]
            }
        }
        get_resp = _make_response(200, existing)
        post_resp = _make_response(201)
        session.request.side_effect = [get_resp, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        assert result.status == "linked"

    def test_add_blocked_by_empty_issue_id_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="issue_id must be a non-empty string"):
            provider.add_blocked_by("", "PROJ-1", dry_run=False)

    def test_add_blocked_by_empty_blocked_by_id_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="blocked_by_id must be a non-empty string"):
            provider.add_blocked_by("PROJ-2", "", dry_run=False)

    def test_add_blocked_by_self_blocking_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="Self-blocking is not allowed"):
            provider.add_blocked_by("PROJ-1", "PROJ-1", dry_run=False)

    def test_add_blocked_by_self_blocking_raises_in_dry_run(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="Self-blocking is not allowed"):
            provider.add_blocked_by("PROJ-1", "PROJ-1", dry_run=True)
        session.request.assert_not_called()

    def test_add_blocked_by_self_blocking_detected_after_strip(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="Self-blocking is not allowed"):
            provider.add_blocked_by("  PROJ-1", "PROJ-1  ", dry_run=False)
        session.request.assert_not_called()

    def test_add_blocked_by_issue_id_not_found_raises_valueerror(self):
        """GET 404 on issue_id during dependency check proceeds to POST which also 404s."""
        session = _make_mock_session()
        session.request.return_value = _make_response(404, text='{"errorMessages":["Issue does not exist"]}')
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(
            ValueError,
            match=r"issue_id='PROJ-2'.*blocked_by_id='PROJ-404'",
        ):
            provider.add_blocked_by("PROJ-2", "PROJ-404", dry_run=False)

    def test_add_blocked_by_post_not_found_raises_valueerror(self):
        """POST 404 raises ValueError that includes issue_id and blocked_by_id in the message."""
        session = _make_mock_session()
        get_resp = _make_response(200, {"fields": {"issuelinks": []}})
        post_resp = _make_response(404, text='{"errorMessages":["Issue does not exist"]}')
        session.request.side_effect = [get_resp, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(
            ValueError,
            match=r"issue_id='PROJ-2'.*blocked_by_id='PROJ-404'.*Issue does not exist",
        ):
            provider.add_blocked_by("PROJ-2", "PROJ-404", dry_run=False)

    def test_add_blocked_by_non_dict_link_entry_skipped(self):
        """Non-dict entries in issuelinks are skipped without error."""
        session = _make_mock_session()
        existing = {
            "fields": {
                "issuelinks": [
                    "not-a-dict",
                    {"type": {"name": "Blocks"}, "outwardIssue": {"key": "PROJ-1"}},
                ]
            }
        }
        session.request.return_value = _make_response(200, existing)
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        assert result.status == "already-linked"

    def test_add_blocked_by_non_dict_link_type_skipped(self):
        """Links with a non-dict type field are skipped without error."""
        session = _make_mock_session()
        existing = {
            "fields": {
                "issuelinks": [
                    {"type": "Blocks", "outwardIssue": {"key": "PROJ-1"}},
                ]
            }
        }
        get_resp = _make_response(200, existing)
        post_resp = _make_response(201)
        session.request.side_effect = [get_resp, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        # The malformed link is skipped; a new link is created
        assert result.status == "linked"

    def test_add_blocked_by_non_blocks_link_type_not_idempotent(self):
        """A different link type (e.g. Relates) is not treated as already-linked."""
        session = _make_mock_session()
        existing = {
            "fields": {
                "issuelinks": [
                    {"type": {"name": "Relates"}, "outwardIssue": {"key": "PROJ-1"}},
                ]
            }
        }
        get_resp = _make_response(200, existing)
        post_resp = _make_response(201)
        session.request.side_effect = [get_resp, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        assert result.status == "linked"

    def test_add_blocked_by_issuelinks_none_proceeds_to_post(self):
        """issuelinks=None in Jira response is treated as empty list; POST proceeds safely."""
        session = _make_mock_session()
        existing = {"fields": {"issuelinks": None}}
        get_resp = _make_response(200, existing)
        post_resp = _make_response(201)
        session.request.side_effect = [get_resp, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        assert result.status == "linked"
        call_kwargs = session.request.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert payload["outwardIssue"]["key"] == "PROJ-1"
        assert payload["inwardIssue"]["key"] == "PROJ-2"

    def test_add_blocked_by_type_name_none_skipped(self):
        """Link with type.name=None is skipped without AttributeError; POST proceeds safely."""
        session = _make_mock_session()
        existing = {
            "fields": {
                "issuelinks": [
                    {"type": {"name": None}, "outwardIssue": {"key": "PROJ-1"}},
                ]
            }
        }
        get_resp = _make_response(200, existing)
        post_resp = _make_response(201)
        session.request.side_effect = [get_resp, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        assert result.status == "linked"

    def test_add_blocked_by_get_returns_non_dict_raises(self):
        """When GET response is a non-dict (e.g. list), find_existing_dependency raises ValueError."""
        session = _make_mock_session()
        # GET returns a list instead of a dict (unexpected API shape).
        get_non_dict = _make_response(200, ["unexpected-list-response"])
        session.request.return_value = get_non_dict
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="find_existing_dependency: expected a JSON object from Jira"):
            provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)

    def test_add_blocked_by_get_fields_is_list_proceeds_to_post(self):
        """When GET response has `fields` as a list (non-dict), idempotency check is skipped and POST proceeds."""
        session = _make_mock_session()
        # GET returns a dict but with `fields` as a non-empty list â€” a truthy non-dict value.
        # Without the isinstance guard, fields.get("issuelinks") would raise AttributeError.
        get_fields_list = _make_response(200, {"fields": ["unexpected", "list"]})
        post_resp = _make_response(201)
        session.request.side_effect = [get_fields_list, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        assert result.status == "linked"
        assert session.request.call_count == 2

    def test_add_blocked_by_outward_issue_non_dict_skipped(self):
        """outwardIssue present but non-dict (e.g. string/list) does not raise and proceeds to POST."""
        session = _make_mock_session()
        # outwardIssue is a string â€” truthy, but not a dict. Without isinstance guard
        # the `or {}` default is skipped and .get("key") raises AttributeError.
        get_resp = _make_response(
            200,
            {
                "fields": {
                    "issuelinks": [
                        {
                            "type": {"name": "Blocks"},
                            "outwardIssue": "PROJ-1",  # string, not a dict
                        }
                    ]
                }
            },
        )
        post_resp = _make_response(201)
        session.request.side_effect = [get_resp, post_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.add_blocked_by("PROJ-2", "PROJ-1", dry_run=False)
        assert result.status == "linked"
        assert session.request.call_count == 2


class TestJiraProviderDependencyContractGaps:
    """Jira-specific gap tests complementing the shared contract suite."""

    def test_add_blocked_by_transient_502_raises(self, monkeypatch):
        """add_blocked_by raises TransientError on a transient 502 (T019)."""
        monkeypatch.setattr(_SLEEP, lambda *a, **k: None)
        session = _make_mock_session()
        session.request.return_value = _make_response(502, text="bad gateway")
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        with pytest.raises(TransientError, match="502"):
            provider.add_blocked_by("PROJ-1", "PROJ-2", dry_run=False)

    def test_add_blocked_by_transient_503_raises(self, monkeypatch):
        """add_blocked_by raises TransientError on a transient 503 (T019)."""
        monkeypatch.setattr(_SLEEP, lambda *a, **k: None)
        session = _make_mock_session()
        session.request.return_value = _make_response(503, text="unavailable")
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        with pytest.raises(TransientError, match="503"):
            provider.add_blocked_by("PROJ-1", "PROJ-2", dry_run=False)


class TestJiraProviderExistingDependency:
    """Tests for the JiraProvider existing-link query."""

    def test_find_existing_dependency_non_dict_response_raises(self):
        """find_existing_dependency raises ValueError when Jira returns a non-dict payload."""
        session = _make_mock_session()
        # issue GET returns a list instead of a dict
        issue_resp = MagicMock()
        issue_resp.status_code = 200
        issue_resp.raise_for_status = MagicMock()
        issue_resp.json.return_value = ["unexpected", "list"]
        session.request.return_value = issue_resp
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="find_existing_dependency: expected a JSON object from Jira"):
            provider.find_existing_dependency("PROJ-1", "PROJ-2")

    def test_find_existing_dependency_non_list_issuelinks_raises(self):
        """find_existing_dependency raises ValueError when fields.issuelinks is not a list."""
        session = _make_mock_session()
        issue_resp = MagicMock()
        issue_resp.status_code = 200
        issue_resp.raise_for_status = MagicMock()
        issue_resp.json.return_value = {"fields": {"issuelinks": {"unexpected": "shape"}}}
        session.request.return_value = issue_resp
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(
            ValueError,
            match=r"find_existing_dependency: expected fields\.issuelinks to be a list when present, got dict",
        ):
            provider.find_existing_dependency("PROJ-1", "PROJ-2")
