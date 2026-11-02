"""Tests for the find_control_issue_number symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control import CONTROL_MARKER, SUPERVISED_LABEL
from agentic_devtools.cli.ci.supervision_control_command import find_control_issue_number


def _issue(number: int, author: str, body: str, *labels: str) -> dict[str, object]:
    return {
        "number": number,
        "author": {"login": author},
        "body": body,
        "labels": [{"name": label} for label in labels],
    }


def test_find_control_issue_number_returns_none_when_absent() -> None:
    assert find_control_issue_number([], trusted_author="automation") is None


def test_find_control_issue_number_returns_matching_issue() -> None:
    raw = [
        _issue(42, "automation", CONTROL_MARKER, SUPERVISED_LABEL),
        _issue(5, "automation", "unrelated", SUPERVISED_LABEL),
    ]
    assert find_control_issue_number(raw, trusted_author="automation") == 42


def test_find_control_issue_number_ignores_untrusted_or_non_exact_markers() -> None:
    raw = [
        _issue(42, "attacker", CONTROL_MARKER, SUPERVISED_LABEL),
        _issue(44, "automation", f"prefix {CONTROL_MARKER}", SUPERVISED_LABEL),
    ]

    assert find_control_issue_number(raw, trusted_author="automation") is None


def test_find_control_issue_number_recovers_a_control_issue_without_its_label() -> None:
    assert find_control_issue_number([_issue(43, "automation", CONTROL_MARKER)], trusted_author="automation") == 43


def test_find_control_issue_number_rejects_multiple_matches() -> None:
    raw = [
        _issue(42, "automation", CONTROL_MARKER, SUPERVISED_LABEL),
        _issue(43, "automation", CONTROL_MARKER, SUPERVISED_LABEL),
    ]
    with pytest.raises(RuntimeError, match="multiple"):
        find_control_issue_number(raw, trusted_author="automation")


def test_find_control_issue_number_rejects_non_list() -> None:
    with pytest.raises(ValueError, match="invalid response"):
        find_control_issue_number({"not": "a list"}, trusted_author="automation")


def test_find_control_issue_number_requires_trusted_author() -> None:
    with pytest.raises(ValueError, match="trusted author"):
        find_control_issue_number([], trusted_author=" ")


@pytest.mark.parametrize(
    "raw",
    [
        [_issue(42, "automation", CONTROL_MARKER, SUPERVISED_LABEL) | {"number": "42"}],
        [_issue(42, "automation", CONTROL_MARKER, SUPERVISED_LABEL) | {"number": True}],
        [_issue(42, "automation", CONTROL_MARKER, SUPERVISED_LABEL) | {"number": 0}],
        [_issue(42, "automation", CONTROL_MARKER, SUPERVISED_LABEL) | {"body": None}],
        [_issue(42, "", CONTROL_MARKER, SUPERVISED_LABEL)],
        [_issue(42, "automation", CONTROL_MARKER) | {"labels": "invalid"}],
        ["not-an-issue"],
    ],
)
def test_find_control_issue_number_fails_closed_on_malformed_entries(raw: object) -> None:
    with pytest.raises(ValueError, match="issue entries"):
        find_control_issue_number(raw, trusted_author="automation")
