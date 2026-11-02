"""Tests for the parse_pr_observation symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control import PRObservation
from agentic_devtools.cli.ci.supervision_control_command import parse_pr_observation


def _observation(number: int, head: str, *labels: str) -> PRObservation:
    return PRObservation(number, head, frozenset(labels))


def test_parse_pr_observation_accepts_valid_payload() -> None:
    observation = parse_pr_observation(
        {"number": 7, "headRefOid": "head-7", "labels": [{"name": "ai-pr-loop-supervised"}]}
    )
    assert observation == _observation(7, "head-7", "ai-pr-loop-supervised")


@pytest.mark.parametrize(
    "raw",
    [
        "not-a-dict",
        {"number": 0, "headRefOid": "head", "labels": []},
        {"number": True, "headRefOid": "head", "labels": []},
        {"number": 7, "headRefOid": "", "labels": []},
        {"number": 7, "headRefOid": "head", "labels": "not-a-list"},
        {"number": 7, "headRefOid": "head", "labels": [{"name": 1}]},
        {"number": 7, "headRefOid": "head", "labels": ["not-a-dict"]},
    ],
)
def test_parse_pr_observation_rejects_malformed_payloads(raw: object) -> None:
    with pytest.raises(ValueError):
        parse_pr_observation(raw)
