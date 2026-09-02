"""Tests for _fetch_newest_jira_comments."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

from agentic_devtools.orchestration.nodes._issue_retrieval import _fetch_newest_jira_comments


def _make_config() -> MagicMock:
    cfg = MagicMock()
    cfg.base_url = "https://jira.example.com"
    cfg.headers = {"Authorization": "Basic x"}
    cfg.ssl_verify = True
    return cfg


class TestFetchNewestJiraComments:
    def test_returns_comments_list_on_success(self) -> None:
        cfg = _make_config()
        comments = [{"id": "9", "body": "newest", "created": "2024-06-01"}]
        response = MagicMock()
        response.json.return_value = {"comments": comments}
        requests = MagicMock()
        requests.get.return_value = response

        with patch(
            "agentic_devtools.tools.jira._requests",
            return_value=requests,
        ):
            result = _fetch_newest_jira_comments(cfg, "PROJECT-1", 30)

        assert result == comments
        # URL is ordered newest-first with the requested limit and an encoded key.
        called_url = requests.get.call_args.args[0]
        assert "orderBy=-created" in called_url
        assert "maxResults=30" in called_url
        assert "PROJECT-1" in called_url

    def test_encodes_issue_key(self) -> None:
        cfg = _make_config()
        response = MagicMock()
        response.json.return_value = {"comments": []}
        requests = MagicMock()
        requests.get.return_value = response

        with patch(
            "agentic_devtools.tools.jira._requests",
            return_value=requests,
        ):
            _fetch_newest_jira_comments(cfg, "PROJ/ECT 1", 5)

        called_url = requests.get.call_args.args[0]
        assert "PROJ%2FECT%201" in called_url

    def test_returns_none_on_request_exception(self) -> None:
        cfg = _make_config()
        requests = MagicMock()
        requests.get.side_effect = RuntimeError("boom")

        with patch(
            "agentic_devtools.tools.jira._requests",
            return_value=requests,
        ):
            result = _fetch_newest_jira_comments(cfg, "PROJECT-1", 30)

        assert result is None

    def test_returns_none_when_payload_not_dict(self) -> None:
        cfg = _make_config()
        response = MagicMock()
        response.json.return_value = ["unexpected", "list"]
        requests = MagicMock()
        requests.get.return_value = response

        with patch(
            "agentic_devtools.tools.jira._requests",
            return_value=requests,
        ):
            result = _fetch_newest_jira_comments(cfg, "PROJECT-1", 30)

        assert result is None

    def test_returns_none_when_comments_not_list(self) -> None:
        cfg = _make_config()
        response = MagicMock()
        response.json.return_value = {"comments": "not-a-list"}
        requests = MagicMock()
        requests.get.return_value = response

        with patch(
            "agentic_devtools.tools.jira._requests",
            return_value=requests,
        ):
            result: Any = _fetch_newest_jira_comments(cfg, "PROJECT-1", 30)

        assert result is None
