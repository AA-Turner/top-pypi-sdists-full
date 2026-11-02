"""Tests for the parse_pr_list symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control import PRObservation
from agentic_devtools.cli.ci.supervision_control_command import parse_pr_list


def _observation(number: int, head: str, *labels: str) -> PRObservation:
    return PRObservation(number, head, frozenset(labels))


def test_parse_pr_list_accepts_valid_array() -> None:
    observations = parse_pr_list([{"number": 7, "headRefOid": "head-7", "labels": []}])
    assert observations == [_observation(7, "head-7")]


def test_parse_pr_list_rejects_non_array() -> None:
    with pytest.raises(ValueError, match="array"):
        parse_pr_list({"not": "a list"})
