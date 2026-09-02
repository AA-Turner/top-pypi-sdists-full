"""Tests for agentic_devtools.tools.jira.fetch_issue_context."""

from unittest.mock import MagicMock

import pytest

from agentic_devtools.tools.jira import JiraConfig, fetch_issue_context


class TestFetchIssueContext:
    """Tests for the fetch_issue_context tool function."""

    def _make_config(self, mock_requests=None, base_url="https://jira.example.com"):
        return JiraConfig(
            base_url=base_url,
            headers={"Authorization": "Basic xxx"},
            ssl_verify=False,
            requests_module=mock_requests or MagicMock(),
        )

    def _make_issue_response(self, issue_key="PROJ-1", is_subtask=False, epic_link=None, parent_key=None):
        fields = {
            "summary": "Test issue",
            "description": "Description",
            "comment": {"comments": []},
            "labels": [],
            "issuetype": {
                "name": "Sub-task" if is_subtask else "Task",
                "subtask": is_subtask,
            },
            "customfield_10008": epic_link,
        }
        if parent_key and is_subtask:
            fields["parent"] = {"key": parent_key}
        return {"key": issue_key, "fields": fields}

    def test_returns_issue_data(self):
        mock_requests = MagicMock()
        issue_data = self._make_issue_response("PROJ-1")
        mock_response = MagicMock()
        mock_response.json.return_value = issue_data
        mock_requests.get.return_value = mock_response

        config = self._make_config(mock_requests)
        result = fetch_issue_context(config=config, issue_key="PROJ-1")

        assert result["issue"]["key"] == "PROJ-1"
        assert result["parent_issue"] is None
        assert result["epic_issue"] is None
        assert result["remote_links"] == []

    def test_uses_full_field_fetch(self):
        """HTTP request uses full-field fetch (*all) rather than a hard-coded allowlist."""
        mock_requests = MagicMock()
        issue_data = self._make_issue_response("PROJ-1")
        mock_response = MagicMock()
        mock_response.json.return_value = issue_data
        mock_requests.get.return_value = mock_response

        config = self._make_config(mock_requests)
        fetch_issue_context(config=config, issue_key="PROJ-1")

        # First GET call is the issue fetch
        first_call = mock_requests.get.call_args_list[0]
        url = first_call[0][0] if first_call[0] else first_call[1].get("url", "")
        assert "fields=*all" in url

    def test_url_encodes_issue_key(self):
        """Issue key is URL-escaped for both issue and remotelink request paths."""
        mock_requests = MagicMock()
        issue_data = self._make_issue_response("PROJ-1")
        mock_response = MagicMock()
        mock_response.json.return_value = issue_data
        mock_requests.get.return_value = mock_response

        config = self._make_config(mock_requests)
        fetch_issue_context(config=config, issue_key="PROJ-1/abc?x=1#frag")

        encoded_key = "PROJ-1%2Fabc%3Fx%3D1%23frag"

        first_call = mock_requests.get.call_args_list[0]
        first_url = first_call[0][0] if first_call[0] else first_call[1].get("url", "")
        assert f"/rest/api/2/issue/{encoded_key}?" in first_url

        second_call = mock_requests.get.call_args_list[1]
        second_url = second_call[0][0] if second_call[0] else second_call[1].get("url", "")
        assert second_url.endswith(f"/rest/api/2/issue/{encoded_key}/remotelink")

    def test_raises_value_error_on_empty_base_url(self):
        config = self._make_config(base_url="")

        with pytest.raises(ValueError, match="base_url is required"):
            fetch_issue_context(config=config, issue_key="PROJ-1")

    def test_fetches_parent_for_subtask(self):
        mock_requests = MagicMock()
        issue_data = self._make_issue_response("PROJ-2", is_subtask=True, parent_key="PROJ-1")
        parent_data = {"key": "PROJ-1", "fields": {"summary": "Parent Issue"}}

        def get_side_effect(url, **kwargs):
            resp = MagicMock()
            if "PROJ-2" in url and "remotelink" not in url:
                resp.json.return_value = issue_data
            elif "PROJ-1" in url:
                resp.json.return_value = parent_data
            else:
                resp.json.return_value = []
            return resp

        mock_requests.get.side_effect = get_side_effect
        config = self._make_config(mock_requests)

        result = fetch_issue_context(config=config, issue_key="PROJ-2")

        assert result["parent_issue"] is not None
        assert result["parent_issue"]["key"] == "PROJ-1"

    def test_subtask_without_parent_key_skips_parent_fetch(self):
        """Subtask with no parent key in fields skips parent fetch."""
        mock_requests = MagicMock()
        issue_data = self._make_issue_response("PROJ-7", is_subtask=True)
        mock_response = MagicMock()
        mock_response.json.return_value = issue_data
        mock_requests.get.return_value = mock_response

        config = self._make_config(mock_requests)
        result = fetch_issue_context(config=config, issue_key="PROJ-7")

        assert result["parent_issue"] is None
        # Two GET calls: main issue + remotelinks; no parent fetch
        assert mock_requests.get.call_count == 2

    def test_fetches_epic_for_linked_issue(self):
        mock_requests = MagicMock()
        issue_data = self._make_issue_response("PROJ-3", epic_link="PROJ-100")
        epic_data = {"key": "PROJ-100", "fields": {"summary": "My Epic"}}

        def get_side_effect(url, **kwargs):
            resp = MagicMock()
            if "PROJ-3" in url and "remotelink" not in url:
                resp.json.return_value = issue_data
            elif "PROJ-100" in url:
                resp.json.return_value = epic_data
            else:
                resp.json.return_value = []
            return resp

        mock_requests.get.side_effect = get_side_effect
        config = self._make_config(mock_requests)

        result = fetch_issue_context(config=config, issue_key="PROJ-3")

        assert result["epic_issue"] is not None
        assert result["epic_issue"]["key"] == "PROJ-100"

    def test_no_epic_fetch_for_subtask(self):
        """Subtasks should not trigger an epic fetch even if customfield_10008 is set."""
        mock_requests = MagicMock()
        issue_data = self._make_issue_response("PROJ-4", is_subtask=True, parent_key="PROJ-3", epic_link="PROJ-100")

        def get_side_effect(url, **kwargs):
            resp = MagicMock()
            if "PROJ-4" in url and "remotelink" not in url:
                resp.json.return_value = issue_data
            elif "PROJ-3" in url:
                resp.json.return_value = {"key": "PROJ-3", "fields": {"summary": "Parent"}}
            else:
                resp.json.return_value = []
            return resp

        mock_requests.get.side_effect = get_side_effect
        config = self._make_config(mock_requests)

        result = fetch_issue_context(config=config, issue_key="PROJ-4")

        assert result["epic_issue"] is None

    def test_no_epic_fetch_for_epic_itself(self):
        """Epics themselves should not trigger a recursive epic fetch."""
        mock_requests = MagicMock()
        issue_data = {
            "key": "PROJ-100",
            "fields": {
                "summary": "An Epic",
                "description": "",
                "comment": {"comments": []},
                "labels": [],
                "issuetype": {"name": "Epic", "subtask": False},
                "customfield_10008": "PROJ-200",
            },
        }

        def get_side_effect(url, **kwargs):
            resp = MagicMock()
            if "PROJ-100" in url and "remotelink" not in url:
                resp.json.return_value = issue_data
            else:
                resp.json.return_value = []
            return resp

        mock_requests.get.side_effect = get_side_effect
        config = self._make_config(mock_requests)

        result = fetch_issue_context(config=config, issue_key="PROJ-100")

        assert result["epic_issue"] is None

    def test_remote_links_returned(self):
        mock_requests = MagicMock()
        issue_data = self._make_issue_response("PROJ-5")
        links = [{"object": {"title": "PR #1"}}]

        def get_side_effect(url, **kwargs):
            resp = MagicMock()
            if "remotelink" in url:
                resp.json.return_value = links
            else:
                resp.json.return_value = issue_data
            return resp

        mock_requests.get.side_effect = get_side_effect
        config = self._make_config(mock_requests)

        result = fetch_issue_context(config=config, issue_key="PROJ-5")

        assert len(result["remote_links"]) == 1
        assert result["remote_links"][0]["object"]["title"] == "PR #1"

    def test_handles_fetch_failure_gracefully(self):
        """Parent/epic fetch failures should not crash the function."""
        mock_requests = MagicMock()
        issue_data = self._make_issue_response("PROJ-6", is_subtask=True, parent_key="PROJ-5")

        call_count = 0

        def get_side_effect(url, **kwargs):
            nonlocal call_count
            call_count += 1
            resp = MagicMock()
            if "PROJ-6" in url and "remotelink" not in url:
                resp.json.return_value = issue_data
            elif "PROJ-5" in url:
                raise Exception("Connection refused")
            else:
                resp.json.return_value = []
            return resp

        mock_requests.get.side_effect = get_side_effect
        config = self._make_config(mock_requests)

        result = fetch_issue_context(config=config, issue_key="PROJ-6")

        assert result["parent_issue"] is None  # Fetch failed gracefully

    def test_calls_raise_for_status_on_main_issue(self):
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("HTTP 404")
        mock_requests.get.return_value = mock_response
        config = self._make_config(mock_requests)

        with pytest.raises(Exception, match="HTTP 404"):
            fetch_issue_context(config=config, issue_key="PROJ-1")

    def test_handles_null_fields_in_response(self):
        """Jira can return {"fields": null}; should not crash."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "PROJ-1", "fields": None}
        mock_requests.get.return_value = mock_response

        config = self._make_config(mock_requests)
        result = fetch_issue_context(config=config, issue_key="PROJ-1")

        assert result["issue"] == {"key": "PROJ-1", "fields": None}
        assert result["parent_issue"] is None
        assert result["epic_issue"] is None

    def test_handles_non_dict_response_body(self):
        """response.json() returning None or a list should not crash."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = None  # Unexpected Jira API shape
        mock_requests.get.return_value = mock_response

        config = self._make_config(mock_requests)
        result = fetch_issue_context(config=config, issue_key="PROJ-1")

        # Non-dict body is normalised to {} so that the typed result field
        # (issue: dict) is always a dict.
        assert result["issue"] == {}
        assert result["parent_issue"] is None
        assert result["epic_issue"] is None

    def test_handles_null_issuetype_in_fields(self):
        """fields.issuetype == null should not crash and should be treated as a non-subtask/non-epic."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "key": "PROJ-1",
            "fields": {"issuetype": None, "customfield_10008": None},
        }
        mock_requests.get.return_value = mock_response

        config = self._make_config(mock_requests)
        result = fetch_issue_context(config=config, issue_key="PROJ-1")

        assert result["parent_issue"] is None
        assert result["epic_issue"] is None

    def test_handles_non_string_issuetype_name(self):
        """fields.issuetype.name == null should not crash and still allow epic fetch for non-subtasks."""
        mock_requests = MagicMock()
        issue_data = {
            "key": "PROJ-1",
            "fields": {
                "issuetype": {"name": None, "subtask": False},
                "customfield_10008": "PROJ-100",
            },
        }
        epic_data = {"key": "PROJ-100", "fields": {"summary": "Epic"}}

        def get_side_effect(url, **kwargs):
            resp = MagicMock()
            if "PROJ-100" in url:
                resp.json.return_value = epic_data
            elif "remotelink" in url:
                resp.json.return_value = []
            else:
                resp.json.return_value = issue_data
            return resp

        mock_requests.get.side_effect = get_side_effect

        config = self._make_config(mock_requests)
        result = fetch_issue_context(config=config, issue_key="PROJ-1")

        assert result["parent_issue"] is None
        assert result["epic_issue"] == epic_data

    def test_handles_null_parent_in_subtask_fields(self):
        """fields.parent == null on a subtask should not crash; no parent fetch attempted."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "key": "PROJ-2",
            "fields": {
                "issuetype": {"name": "Sub-task", "subtask": True},
                "parent": None,
                "customfield_10008": None,
            },
        }
        mock_requests.get.return_value = mock_response

        config = self._make_config(mock_requests)
        result = fetch_issue_context(config=config, issue_key="PROJ-2")

        assert result["parent_issue"] is None
        # Only two GET calls: main issue + remotelinks; no parent fetch
        assert mock_requests.get.call_count == 2

    def test_url_encodes_related_issue_key(self):
        """Parent and epic keys are URL-encoded when fetched via _fetch_related_issue."""
        mock_requests = MagicMock()
        parent_key = "PROJ-1/x?q=1"
        issue_data = {
            "key": "PROJ-2",
            "fields": {
                "summary": "Sub",
                "description": "",
                "comment": {"comments": []},
                "labels": [],
                "issuetype": {"name": "Sub-task", "subtask": True},
                "customfield_10008": None,
                "parent": {"key": parent_key},
            },
        }
        parent_data = {"key": parent_key, "fields": {"summary": "Parent"}}

        def get_side_effect(url, **kwargs):
            resp = MagicMock()
            if "PROJ-2" in url and "remotelink" not in url:
                resp.json.return_value = issue_data
            elif "PROJ-1%2Fx%3Fq%3D1" in url:
                resp.json.return_value = parent_data
            else:
                resp.json.return_value = []
            return resp

        mock_requests.get.side_effect = get_side_effect
        config = self._make_config(mock_requests)

        result = fetch_issue_context(config=config, issue_key="PROJ-2")

        # Verify the parent was fetched via URL-encoded key
        urls = [call[0][0] for call in mock_requests.get.call_args_list]
        assert any("PROJ-1%2Fx%3Fq%3D1" in url for url in urls)
        assert result["parent_issue"] is not None

    def test_non_string_epic_link_skips_epic_fetch(self):
        """customfield_10008 with a non-string value must not crash; epic fetch is skipped."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "key": "PROJ-3",
            "fields": {
                "summary": "Task",
                "description": "",
                "comment": {"comments": []},
                "labels": [],
                "issuetype": {"name": "Task", "subtask": False},
                # Non-string epic link — unexpected Jira/custom-field shape
                "customfield_10008": {"id": "10001", "key": "PROJ-1"},
            },
        }
        mock_requests.get.return_value = mock_response

        config = self._make_config(mock_requests)
        result = fetch_issue_context(config=config, issue_key="PROJ-3")

        assert result["epic_issue"] is None
        # Only two GET calls: main issue + remotelinks; no epic fetch attempted
        assert mock_requests.get.call_count == 2

    def test_non_dict_parent_response_is_normalized_to_none(self):
        """Related parent issue fetch returning non-dict JSON should be ignored."""
        mock_requests = MagicMock()
        issue_data = self._make_issue_response("PROJ-2", is_subtask=True, parent_key="PROJ-1")

        def get_side_effect(url, **kwargs):
            resp = MagicMock()
            if "PROJ-2" in url and "remotelink" not in url:
                resp.json.return_value = issue_data
            elif "PROJ-1" in url:
                resp.json.return_value = ["unexpected", "shape"]
            else:
                resp.json.return_value = []
            return resp

        mock_requests.get.side_effect = get_side_effect
        config = self._make_config(mock_requests)

        result = fetch_issue_context(config=config, issue_key="PROJ-2")

        assert result["parent_issue"] is None

    def test_non_dict_epic_response_is_normalized_to_none(self):
        """Related epic fetch returning non-dict JSON should be ignored."""
        mock_requests = MagicMock()
        issue_data = self._make_issue_response("PROJ-3", epic_link="PROJ-100")

        def get_side_effect(url, **kwargs):
            resp = MagicMock()
            if "PROJ-3" in url and "remotelink" not in url:
                resp.json.return_value = issue_data
            elif "PROJ-100" in url:
                resp.json.return_value = None
            else:
                resp.json.return_value = []
            return resp

        mock_requests.get.side_effect = get_side_effect
        config = self._make_config(mock_requests)

        result = fetch_issue_context(config=config, issue_key="PROJ-3")

        assert result["epic_issue"] is None
