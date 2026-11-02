"""Tests for _fetch_newest_github_comments."""

from __future__ import annotations

import json
import subprocess
from unittest.mock import MagicMock, patch

from agentic_devtools.orchestration.nodes._issue_retrieval import _fetch_newest_github_comments


def _completed(stdout: str = "", returncode: int = 0, stderr: str = "") -> subprocess.CompletedProcess:
    cp: subprocess.CompletedProcess = MagicMock(spec=subprocess.CompletedProcess)
    cp.stdout = stdout
    cp.returncode = returncode
    cp.stderr = stderr
    return cp


class TestFetchNewestGithubComments:
    def test_returns_normalized_comments_on_success(self) -> None:
        raw = [
            {"id": 101, "body": "newest comment", "created_at": "2024-06-01T00:00:00Z"},
            {"id": 100, "body": "older comment", "created_at": "2024-05-01T00:00:00Z"},
        ]
        cp = _completed(stdout=json.dumps(raw))

        with patch(
            "agentic_devtools.cli.subprocess_utils.run_safe",
            return_value=cp,
        ):
            result = _fetch_newest_github_comments("owner/repo", "42", 30)

        assert result is not None
        assert len(result) == 2
        assert result[0]["comment_id"] == "101"
        assert result[0]["body"] == "newest comment"
        assert result[0]["created_at"] == "2024-06-01T00:00:00Z"

    def test_url_contains_per_page_100_and_page_param(self) -> None:
        cp = _completed(stdout=json.dumps([]))

        with patch(
            "agentic_devtools.cli.subprocess_utils.run_safe",
            return_value=cp,
        ) as mock_run:
            _fetch_newest_github_comments("owner/repo", "99", 30)

        called_args = mock_run.call_args.args[0]
        endpoint = called_args[2]
        assert "direction=desc" not in endpoint
        assert "per_page=100" in endpoint
        assert "page=1" in endpoint
        assert "owner/repo" in endpoint
        assert "/99/" in endpoint

    def test_returns_none_on_nonzero_returncode(self) -> None:
        cp = _completed(returncode=1, stderr="gh: command failed")

        with patch(
            "agentic_devtools.cli.subprocess_utils.run_safe",
            return_value=cp,
        ):
            result = _fetch_newest_github_comments("owner/repo", "42", 30)

        assert result is None

    def test_returns_none_on_exception(self) -> None:
        with patch(
            "agentic_devtools.cli.subprocess_utils.run_safe",
            side_effect=FileNotFoundError("gh not found"),
        ):
            result = _fetch_newest_github_comments("owner/repo", "42", 30)

        assert result is None

    def test_returns_none_when_output_is_not_a_list(self) -> None:
        cp = _completed(stdout=json.dumps({"unexpected": "dict"}))

        with patch(
            "agentic_devtools.cli.subprocess_utils.run_safe",
            return_value=cp,
        ):
            result = _fetch_newest_github_comments("owner/repo", "42", 30)

        assert result is None

    def test_non_dict_entries_in_list_are_skipped(self) -> None:
        raw = [
            {"id": 5, "body": "good", "created_at": "2024-01-01T00:00:00Z"},
            "not-a-dict",
            None,
        ]
        cp = _completed(stdout=json.dumps(raw))

        with patch(
            "agentic_devtools.cli.subprocess_utils.run_safe",
            return_value=cp,
        ):
            result = _fetch_newest_github_comments("owner/repo", "42", 30)

        assert result is not None
        assert len(result) == 1
        assert result[0]["comment_id"] == "5"

    def test_null_id_becomes_empty_string(self) -> None:
        raw = [{"id": None, "body": "b", "created_at": "2024-01-01T00:00:00Z"}]
        cp = _completed(stdout=json.dumps(raw))

        with patch(
            "agentic_devtools.cli.subprocess_utils.run_safe",
            return_value=cp,
        ):
            result = _fetch_newest_github_comments("owner/repo", "42", 30)

        assert result is not None
        assert result[0]["comment_id"] == ""

    def test_non_string_body_becomes_empty_string(self) -> None:
        raw = [{"id": 1, "body": 42, "created_at": "2024-01-01T00:00:00Z"}]
        cp = _completed(stdout=json.dumps(raw))

        with patch(
            "agentic_devtools.cli.subprocess_utils.run_safe",
            return_value=cp,
        ):
            result = _fetch_newest_github_comments("owner/repo", "42", 30)

        assert result is not None
        assert result[0]["body"] == ""

    def test_paginates_when_first_page_full(self) -> None:
        """When page 1 returns 100 items, page 2 is fetched and the newest limit are kept."""
        page1 = [{"id": i, "body": f"b{i}", "created_at": f"2024-01-{i:02d}T00:00:00Z"} for i in range(1, 101)]
        page2 = [{"id": 200, "body": "newest", "created_at": "2024-12-01T00:00:00Z"}]
        pages = iter([_completed(stdout=json.dumps(page1)), _completed(stdout=json.dumps(page2))])

        with patch(
            "agentic_devtools.cli.subprocess_utils.run_safe",
            side_effect=lambda *a, **kw: next(pages),
        ):
            result = _fetch_newest_github_comments("owner/repo", "42", 5)

        assert result is not None
        # 101 total entries; newest 5 should be kept (ids 97-100 from page1 + 200 from page2)
        assert len(result) == 5
        assert result[-1]["comment_id"] == "200"

    def test_newest_limit_sliced_from_all_pages(self) -> None:
        """Only the last `limit` entries of all pages are returned."""
        page1 = [{"id": i, "body": f"b{i}", "created_at": f"2024-01-{i:02d}T00:00:00Z"} for i in range(1, 101)]
        page2 = [{"id": i, "body": f"b{i}", "created_at": f"2024-02-{i:02d}T00:00:00Z"} for i in range(101, 141)]
        pages = iter([_completed(stdout=json.dumps(page1)), _completed(stdout=json.dumps(page2))])

        with patch(
            "agentic_devtools.cli.subprocess_utils.run_safe",
            side_effect=lambda *a, **kw: next(pages),
        ):
            result = _fetch_newest_github_comments("owner/repo", "42", 30)

        assert result is not None
        assert len(result) == 30
        # Last 30 of 140 total = entries 111-140
        assert result[0]["comment_id"] == "111"
        assert result[-1]["comment_id"] == "140"
