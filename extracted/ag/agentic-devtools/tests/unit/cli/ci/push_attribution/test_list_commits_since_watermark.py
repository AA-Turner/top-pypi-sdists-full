"""Tests for list_commits_since_watermark()."""

from __future__ import annotations

import json
from typing import Any

import pytest

from agentic_devtools.cli.ci.push_attribution import list_commits_since_watermark


def test_returns_empty_list_when_no_commits(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.push_attribution._gh_api",
        lambda _endpoint: json.dumps([]),
    )

    assert list_commits_since_watermark("owner/repo", "") == []


def test_stops_at_watermark_sha(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.push_attribution._gh_api",
        lambda _endpoint: json.dumps(
            [
                {"sha": "newest"},
                {"sha": "watermark"},
                {"sha": "older"},
            ]
        ),
    )

    assert list_commits_since_watermark("owner/repo", "watermark") == [{"sha": "newest"}]


def test_handles_pagination_and_returns_oldest_first(monkeypatch: pytest.MonkeyPatch) -> None:
    responses = {
        "/repos/owner/repo/commits?per_page=2&page=1": json.dumps(
            [
                {"sha": "c4"},
                {"sha": "c3"},
            ]
        ),
        "/repos/owner/repo/commits?per_page=2&page=2": json.dumps(
            [
                {"sha": "c2"},
                {"sha": "c1"},
            ]
        ),
        "/repos/owner/repo/commits?per_page=2&page=3": json.dumps([]),
    }

    def _fake_gh_api(endpoint: str) -> str:
        return responses[endpoint]

    monkeypatch.setattr("agentic_devtools.cli.ci.push_attribution._gh_api", _fake_gh_api)

    assert list_commits_since_watermark("owner/repo", "", per_page=2, max_pages=3) == [
        {"sha": "c1"},
        {"sha": "c2"},
        {"sha": "c3"},
        {"sha": "c4"},
    ]


def test_stops_after_max_pages_without_watermark(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.push_attribution._gh_api",
        lambda _endpoint: json.dumps([{"sha": "newer"}, {"sha": "older"}]),
    )

    assert list_commits_since_watermark("owner/repo", "missing", per_page=2, max_pages=1) == [
        {"sha": "older"},
        {"sha": "newer"},
    ]


def test_warns_when_max_pages_exhausted_with_nonempty_watermark(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """A warning is emitted when max_pages is exhausted and the watermark was never found."""
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.push_attribution._gh_api",
        lambda _endpoint: json.dumps([{"sha": "newer"}, {"sha": "older"}]),
    )

    import logging

    with caplog.at_level(logging.WARNING, logger="agentic_devtools.cli.ci.push_attribution"):
        result = list_commits_since_watermark("owner/repo", "missing-sha", per_page=2, max_pages=1)

    assert result == [{"sha": "older"}, {"sha": "newer"}]
    assert any("missing-sha" in r.message for r in caplog.records), "Expected warning mentioning the watermark"


def test_no_warning_when_max_pages_exhausted_with_empty_watermark(monkeypatch: pytest.MonkeyPatch) -> None:
    """When max_pages is exhausted and watermark is empty, commits are returned silently."""
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.push_attribution._gh_api",
        lambda _endpoint: json.dumps([{"sha": "a"}, {"sha": "b"}]),
    )

    result = list_commits_since_watermark("owner/repo", "", per_page=2, max_pages=1)

    assert result == [{"sha": "b"}, {"sha": "a"}]


def test_stops_when_page_is_short(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.push_attribution._gh_api",
        lambda _endpoint: json.dumps([{"sha": "only-commit"}]),
    )

    assert list_commits_since_watermark("owner/repo", "", per_page=2) == [{"sha": "only-commit"}]


def test_scopes_history_to_pull_request(monkeypatch: pytest.MonkeyPatch) -> None:
    endpoints: list[str] = []

    def _fake_gh_api(endpoint: str) -> str:
        endpoints.append(endpoint)
        return json.dumps([])

    monkeypatch.setattr(
        "agentic_devtools.cli.ci.push_attribution._gh_api",
        _fake_gh_api,
    )

    list_commits_since_watermark("owner/repo", "", pr_number=42)

    assert endpoints == ["/repos/owner/repo/pulls/42/commits?per_page=30&page=1"]


def test_pull_request_history_returns_commits_after_watermark_across_pages(monkeypatch: pytest.MonkeyPatch) -> None:
    responses = {
        "/repos/owner/repo/pulls/42/commits?per_page=2&page=1": json.dumps(
            [
                {"sha": "old-1"},
                {"sha": "watermark"},
            ]
        ),
        "/repos/owner/repo/pulls/42/commits?per_page=2&page=2": json.dumps(
            [
                {"sha": "new-1"},
                {"sha": "new-2"},
            ]
        ),
        "/repos/owner/repo/pulls/42/commits?per_page=2&page=3": json.dumps([]),
    }

    monkeypatch.setattr("agentic_devtools.cli.ci.push_attribution._gh_api", lambda endpoint: responses[endpoint])

    assert list_commits_since_watermark("owner/repo", "watermark", pr_number=42, per_page=2, max_pages=3) == [
        {"sha": "new-1"},
        {"sha": "new-2"},
    ]


def test_pull_request_history_without_watermark_keeps_oldest_first(monkeypatch: pytest.MonkeyPatch) -> None:
    responses = {
        "/repos/owner/repo/pulls/42/commits?per_page=2&page=1": json.dumps(
            [
                {"sha": "c1"},
                {"sha": "c2"},
            ]
        ),
        "/repos/owner/repo/pulls/42/commits?per_page=2&page=2": json.dumps(
            [
                {"sha": "c3"},
            ]
        ),
    }

    monkeypatch.setattr("agentic_devtools.cli.ci.push_attribution._gh_api", lambda endpoint: responses[endpoint])

    assert list_commits_since_watermark("owner/repo", "", pr_number=42, per_page=2, max_pages=2) == [
        {"sha": "c1"},
        {"sha": "c2"},
        {"sha": "c3"},
    ]


def test_pull_request_history_raises_when_page_contains_non_object(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.push_attribution._gh_api",
        lambda _endpoint: json.dumps(["not-an-object"]),
    )

    with pytest.raises(ValueError, match="contain objects"):
        list_commits_since_watermark("owner/repo", "", pr_number=42)


def test_pull_request_history_stops_when_watermark_found_on_short_page(monkeypatch: pytest.MonkeyPatch) -> None:
    endpoints: list[str] = []
    responses = {
        "/repos/owner/repo/pulls/42/commits?per_page=2&page=1": json.dumps(
            [
                {"sha": "watermark"},
            ]
        ),
    }

    def _fake_gh_api(endpoint: str) -> str:
        endpoints.append(endpoint)
        return responses[endpoint]

    monkeypatch.setattr("agentic_devtools.cli.ci.push_attribution._gh_api", _fake_gh_api)

    assert list_commits_since_watermark("owner/repo", "watermark", pr_number=42, per_page=2, max_pages=3) == []
    assert endpoints == ["/repos/owner/repo/pulls/42/commits?per_page=2&page=1"]


def test_pull_request_history_skips_pages_before_watermark(monkeypatch: pytest.MonkeyPatch) -> None:
    responses = {
        "/repos/owner/repo/pulls/42/commits?per_page=2&page=1": json.dumps(
            [
                {"sha": "old-1"},
                {"sha": "old-2"},
            ]
        ),
        "/repos/owner/repo/pulls/42/commits?per_page=2&page=2": json.dumps(
            [
                {"sha": "watermark"},
                {"sha": "new-1"},
            ]
        ),
        "/repos/owner/repo/pulls/42/commits?per_page=2&page=3": json.dumps(
            [
                {"sha": "new-2"},
            ]
        ),
    }

    monkeypatch.setattr("agentic_devtools.cli.ci.push_attribution._gh_api", lambda endpoint: responses[endpoint])

    assert list_commits_since_watermark("owner/repo", "watermark", pr_number=42, per_page=2, max_pages=3) == [
        {"sha": "new-1"},
        {"sha": "new-2"},
    ]


@pytest.mark.parametrize("pr_number", [True, 0])
def test_rejects_invalid_pull_request_number(pr_number: int, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.push_attribution._gh_api",
        lambda _endpoint: json.dumps([]),
    )

    with pytest.raises(ValueError, match="positive integer"):
        list_commits_since_watermark("owner/repo", "", pr_number=pr_number)


def test_raises_when_api_returns_non_list(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.push_attribution._gh_api",
        lambda _endpoint: json.dumps({"sha": "not-a-list"}),
    )

    with pytest.raises(ValueError, match="must be a list"):
        list_commits_since_watermark("owner/repo", "")


def test_raises_when_commit_page_contains_non_object(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.push_attribution._gh_api",
        lambda _endpoint: json.dumps(["not-an-object"]),
    )

    with pytest.raises(ValueError, match="contain objects"):
        list_commits_since_watermark("owner/repo", "")


@pytest.mark.parametrize(
    ("kwargs", "match"),
    [
        ({"per_page": 0}, "between 1 and 100"),
        ({"per_page": 101}, "between 1 and 100"),
        ({"max_pages": 0}, "max_pages must be >= 1"),
    ],
)
def test_validates_pagination_bounds(kwargs: dict[str, Any], match: str) -> None:
    with pytest.raises(ValueError, match=match):
        list_commits_since_watermark("owner/repo", "", **kwargs)


def test_scan_state_reports_watermark_progress(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.push_attribution._gh_api",
        lambda _endpoint: json.dumps([{"sha": "new"}, {"sha": "old"}]),
    )

    scan_state: dict[str, bool] = {}
    result = list_commits_since_watermark("owner/repo", "missing", per_page=2, max_pages=1, scan_state=scan_state)

    assert result == [{"sha": "old"}, {"sha": "new"}]
    assert scan_state == {"watermark_found": False, "scan_complete": False}
