"""Tests for the build_parser symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control_command import build_parser


def test_parser_exposes_bounded_operations() -> None:
    parser = build_parser()
    assert parser.parse_args(["status"]).operation == "status"
    assert parser.parse_args(["ensure-labels"]).operation == "ensure-labels"
    assert parser.parse_args(["quarantine", "--pr", "7=head"]).operation == "quarantine"
    assert parser.parse_args(["restore-prs", "--receipt", "{}"]).operation == "restore-prs"
    assert parser.parse_args(["hold"]).operation == "hold"
    assert parser.parse_args(["resume", "--receipt", "{}"]).operation == "resume"
    assert parser.parse_args(["checkpoint", "--run-id", "r1", "--payload", "{}"]).operation == "checkpoint"


def test_parser_no_longer_accepts_caller_supplied_states() -> None:
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["hold", "--states", "{}"])
    with pytest.raises(SystemExit):
        parser.parse_args(["resume", "--states", "{}", "--receipt", "{}"])
