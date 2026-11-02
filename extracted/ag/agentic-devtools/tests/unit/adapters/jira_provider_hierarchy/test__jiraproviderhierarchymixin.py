"""Tests for the JiraProvider hierarchy capability."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from agentic_devtools.adapters.jira_provider import JiraProvider
from agentic_devtools.adapters.retry import TransientError
from tests.unit.adapters.jira_provider._fixtures import _make_mock_session, _make_response

_SLEEP = "agentic_devtools.adapters.retry.time.sleep"


class TestJiraProviderLinkSubissue:
    """Tests for JiraProvider.link_subissue."""

    def test_link_empty_parent_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="parent_id must be non-empty"):
            provider.link_subissue("", "PROJ-2", dry_run=False)
        session.request.assert_not_called()

    def test_link_empty_child_raises(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="child_id must be non-empty"):
            provider.link_subissue("PROJ-1", "   ", dry_run=False)
        session.request.assert_not_called()

    def test_link_via_epic_link(self):
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        get_no_parent = _make_response(200, {"fields": {}})
        put_response = _make_response(204)
        session.request.side_effect = [field_response, get_no_parent, put_response]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)
        assert result.status == "linked"
        assert result.source_id == "PROJ-1"
        assert result.target_id == "PROJ-2"

    def test_link_dry_run(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.link_subissue("PROJ-1", "PROJ-2", dry_run=True)
        assert result.status == "dry-run"
        assert result.source_id == "PROJ-1"
        assert result.target_id == "PROJ-2"
        session.request.assert_not_called()

    def test_link_falls_back_to_parent_for_inapplicable_field(self):
        """link_subissue falls back to parent field when epic-link field is not applicable."""
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        get_no_parent = _make_response(200, {"fields": {}})
        epic_fail = _make_response(400, text='{"errors":{"customfield_10008":"Field not on the appropriate screen"}}')
        parent_response = _make_response(204)
        session.request.side_effect = [field_response, get_no_parent, epic_fail, parent_response]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)
        assert result.status == "linked"
        # Verify the fallback PUT used the correct parent payload
        fallback_call = session.request.call_args_list[3]
        fallback_payload = fallback_call.kwargs.get("json") or fallback_call[1].get("json")
        assert fallback_payload == {"fields": {"parent": {"key": "PROJ-1"}}}

    @pytest.mark.parametrize(
        "indicator_phrase",
        [
            "not applicable",
            "cannot be set",
            "does not exist",
        ],
    )
    def test_link_falls_back_for_other_inapplicable_indicators(self, indicator_phrase):
        """link_subissue falls back to parent for all recognised indicators."""
        session = _make_mock_session()
        field_response = _make_response(
            200,
            [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}],
        )
        get_no_parent = _make_response(200, {"fields": {}})
        epic_fail = _make_response(
            400,
            text=f'{{"errors":{{"customfield_10008":"Field {indicator_phrase}"}}}}',
        )
        parent_response = _make_response(204)
        session.request.side_effect = [field_response, get_no_parent, epic_fail, parent_response]

        provider = JiraProvider(
            project_key="PROJ",
            base_url="https://jira.example.com",
            session=session,
        )
        result = provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)
        assert result.status == "linked"

    def test_link_raises_on_non_inapplicable_400(self):
        """link_subissue surfaces non-field-inapplicable 400 errors."""
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        get_no_parent = _make_response(200, {"fields": {}})
        epic_fail = _make_response(400, text='{"errors":{"permission":"You do not have permission"}}')
        # find_existing_link: field_response + get_no_parent (returns None)
        # link_subissue: epic_fail on PUT
        session.request.side_effect = [field_response, get_no_parent, epic_fail]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(Exception, match="HTTP 400"):
            provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)

    def test_link_does_not_fallback_for_does_not_exist_error_on_other_field(self):
        """Fallback is skipped when the indicator is not tied to the epic-link field."""
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        get_no_parent = _make_response(200, {"fields": {}})
        epic_fail = _make_response(400, text='{"errors":{"summary":"Issue does not exist"}}')
        session.request.side_effect = [field_response, get_no_parent, epic_fail]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(Exception, match="HTTP 400"):
            provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)
        assert session.request.call_count == 3

    def test_link_not_found_raises_valueerror(self):
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        not_found = _make_response(404)
        # find_existing_link returns None on 404, then PUT also gets 404
        session.request.side_effect = [field_response, not_found, not_found]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="not found"):
            provider.link_subissue("PROJ-1", "PROJ-404", dry_run=False)
        assert session.request.call_count == 3

    def test_link_fallback_not_found_raises_valueerror(self):
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        get_no_parent = _make_response(200, {"fields": {}})
        epic_fail = _make_response(400, text='{"errors":{"customfield_10008":"Field not applicable"}}')
        fallback_not_found = _make_response(404)
        session.request.side_effect = [field_response, get_no_parent, epic_fail, fallback_not_found]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="not found"):
            provider.link_subissue("PROJ-1", "PROJ-404", dry_run=False)
        assert session.request.call_count == 4

    def test_link_raises_on_non_validation_error(self):
        """link_subissue surfaces non-validation epic-link failures."""
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        get_no_parent = _make_response(200, {"fields": {}})
        epic_fail = _make_response(401)
        session.request.side_effect = [field_response, get_no_parent, epic_fail]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(Exception):
            provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)
        assert session.request.call_count == 3

    def test_link_strips_whitespace_dry_run(self):
        """link_subissue strips surrounding whitespace from parent_id and child_id in dry-run."""
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.link_subissue("  PROJ-1  ", "  PROJ-2  ", dry_run=True)
        assert result.source_id == "PROJ-1"
        assert result.target_id == "PROJ-2"
        session.request.assert_not_called()

    def test_link_strips_whitespace_live(self):
        """link_subissue strips surrounding whitespace before constructing the API URL."""
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        get_no_parent = _make_response(200, {"fields": {}})
        put_response = _make_response(204)
        session.request.side_effect = [field_response, get_no_parent, put_response]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.link_subissue("  PROJ-1  ", "  PROJ-2  ", dry_run=False)
        assert result.source_id == "PROJ-1"
        assert result.target_id == "PROJ-2"
        # Verify the PUT URL used the stripped child_id
        put_call = session.request.call_args_list[2]
        put_url = put_call[0][1] if put_call[0] else put_call.kwargs.get("url", "")
        assert "PROJ-2" in put_url
        assert "  " not in put_url

    def test_link_already_linked_via_epic_field(self):
        """link_subissue returns already-linked when epic-link field already points to parent."""
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        get_linked = _make_response(200, {"fields": {"customfield_10008": "PROJ-1"}})
        session.request.side_effect = [field_response, get_linked]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)
        assert result.status == "already-linked"
        assert result.source_id == "PROJ-1"
        assert result.target_id == "PROJ-2"
        assert session.request.call_count == 2

    def test_link_already_linked_via_parent_field(self):
        """link_subissue returns already-linked when parent field already set to parent_id."""
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        get_linked = _make_response(
            200,
            {"fields": {"customfield_10008": None, "parent": {"key": "PROJ-1", "id": "10001"}}},
        )
        session.request.side_effect = [field_response, get_linked]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)
        assert result.status == "already-linked"
        assert result.source_id == "PROJ-1"
        assert result.target_id == "PROJ-2"
        assert session.request.call_count == 2

    def test_link_get_returns_non_dict_raises(self):
        """When GET response is non-dict, find_existing_link raises ValueError instead of proceeding."""
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        # GET returns a list instead of a dict (unexpected API shape).
        get_non_dict = _make_response(200, ["unexpected-list-response"])
        session.request.side_effect = [field_response, get_non_dict]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="find_existing_link: expected a JSON object from Jira"):
            provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)

    def test_link_get_fields_is_list_proceeds_to_put(self):
        """When GET response has `fields` as a list (non-dict), idempotency check is skipped."""
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        # GET returns a dict but with `fields` as a non-empty list â€” a truthy non-dict value.
        # Without an isinstance guard, `get_data.get("fields") or {}` would keep the list
        # and the subsequent `.get()` call would raise AttributeError.
        get_fields_list = _make_response(200, {"fields": ["unexpected", "list"]})
        put_response = _make_response(204)
        session.request.side_effect = [field_response, get_fields_list, put_response]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        result = provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)
        assert result.status == "linked"
        assert session.request.call_count == 3

    def test_link_put_returns_404_after_get_success_raises_valueerror(self):
        """When PUT returns 404 (issue deleted after GET), a ValueError is raised."""
        session = _make_mock_session()
        field_response = _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
        get_no_parent = _make_response(200, {"fields": {}})
        put_not_found = _make_response(404)
        session.request.side_effect = [field_response, get_no_parent, put_not_found]

        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="not found"):
            provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)
        assert session.request.call_count == 3


class TestJiraEpicHierarchyFlow:
    """End-to-end flow tests for epic hierarchy creation."""

    def test_create_epic_with_children(self):
        """Create 1 epic + 5 children with correct parent linking."""
        session = _make_mock_session()
        issue_counter = {"n": 0}

        def mock_request(method, url, **kwargs):
            if "/field" in url:
                return _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
            if method == "POST" and "/issue" in url:
                issue_counter["n"] += 1
                return _make_response(201, {"key": f"PROJ-{issue_counter['n']}", "id": str(10000 + issue_counter["n"])})
            if method == "PUT":
                return _make_response(204)
            return _make_response(200)

        session.request.side_effect = mock_request
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        parent_result = provider.create_issue("Epic Title", "Epic body", "epic", dry_run=False)
        assert parent_result.status == "created"
        parent_key = parent_result.identifier

        children = []
        for i in range(5):
            result = provider.create_issue(f"Feature {i}", f"Body {i}", "feature", parent_id=parent_key, dry_run=False)
            assert result.status == "created"
            children.append(result)

        assert len(children) == 5

    def test_epic_feature_subtask_hierarchy(self):
        """Create epic â†’ feature (parent_id=epic) â†’ subtask (parent_id=feature)."""
        session = _make_mock_session()
        issue_counter = {"n": 0}

        def mock_request(method, url, **kwargs):
            if "/field" in url:
                return _make_response(200, [{"id": "customfield_10008", "name": "Epic Link", "schema": {}}])
            if method == "POST" and "/issue" in url:
                issue_counter["n"] += 1
                return _make_response(201, {"key": f"PROJ-{issue_counter['n']}", "id": str(10000 + issue_counter["n"])})
            return _make_response(200)

        session.request.side_effect = mock_request
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        epic = provider.create_issue("Epic", "Body", "epic", dry_run=False)
        feature = provider.create_issue("Feature", "Body", "feature", parent_id=epic.identifier, dry_run=False)
        subtask = provider.create_issue("Subtask", "Body", "subtask", parent_id=feature.identifier, dry_run=False)

        assert epic.status == "created"
        assert feature.status == "created"
        assert subtask.status == "created"

        # Verify subtask has parent field set
        subtask_call = session.request.call_args_list[-1]
        subtask_payload = subtask_call.kwargs.get("json") or subtask_call[1].get("json")
        assert subtask_payload["fields"]["parent"] == {"key": feature.identifier}

    def test_blocking_dependencies(self):
        """Wire blocking dependencies between Jira issues."""
        session = _make_mock_session()
        issue_counter = {"n": 0}

        def mock_request(method, url, **kwargs):
            if method == "POST" and "/issue" in url and "Link" not in url:
                issue_counter["n"] += 1
                return _make_response(201, {"key": f"PROJ-{issue_counter['n']}", "id": str(10000 + issue_counter["n"])})
            if method == "POST" and "issueLink" in url:
                return _make_response(201)
            return _make_response(200)

        session.request.side_effect = mock_request
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        issues = []
        for i in range(3):
            result = provider.create_issue(f"Task {i}", f"Body {i}", "task", dry_run=False)
            issues.append(result)

        dep1 = provider.add_blocked_by(issues[1].identifier, issues[0].identifier, dry_run=False)
        assert dep1.status == "linked"
        dep2 = provider.add_blocked_by(issues[2].identifier, issues[1].identifier, dry_run=False)
        assert dep2.status == "linked"


class TestJiraProviderHierarchyContractGaps:
    """Jira-specific gap tests complementing the shared contract suite."""

    def test_link_subissue_transient_502_raises(self, monkeypatch):
        """link_subissue raises TransientError on a transient 502 (T018)."""
        monkeypatch.setattr(_SLEEP, lambda *a, **k: None)
        session = _make_mock_session()
        session.request.return_value = _make_response(502, text="bad gateway")
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        with pytest.raises(TransientError, match="502"):
            provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)

    def test_link_subissue_transient_503_raises(self, monkeypatch):
        """link_subissue raises TransientError on a transient 503 (T018)."""
        monkeypatch.setattr(_SLEEP, lambda *a, **k: None)
        session = _make_mock_session()
        session.request.return_value = _make_response(503, text="unavailable")
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        with pytest.raises(TransientError, match="503"):
            provider.link_subissue("PROJ-1", "PROJ-2", dry_run=False)


class TestJiraProviderExistingLink:
    """Tests for the JiraProvider existing-link query."""

    def test_find_existing_link_non_dict_response_raises(self):
        """find_existing_link raises ValueError when Jira returns a non-dict payload."""
        session = _make_mock_session()
        # field discovery
        field_resp = _make_response(
            200,
            [
                {
                    "id": "customfield_10014",
                    "name": "Epic Link",
                    "schema": {"custom": "com.pyxis.greenhopper.jira:gh-epic-link"},
                }
            ],
        )
        # issue GET returns a list instead of a dict
        issue_resp = MagicMock()
        issue_resp.status_code = 200
        issue_resp.raise_for_status = MagicMock()
        issue_resp.json.return_value = ["unexpected", "list"]
        session.request.side_effect = [field_resp, issue_resp]
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        with pytest.raises(ValueError, match="find_existing_link: expected a JSON object from Jira"):
            provider.find_existing_link("PROJ-1", "PROJ-2")
