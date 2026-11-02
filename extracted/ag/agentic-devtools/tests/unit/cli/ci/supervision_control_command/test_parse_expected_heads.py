"""Tests for the parse_expected_heads symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control_command import parse_expected_heads


def test_parse_expected_heads_rejects_malformed_input() -> None:
    with pytest.raises(ValueError, match="number=head"):
        parse_expected_heads(["7", "x=head"])


def test_parse_expected_heads_rejects_non_positive_number() -> None:
    with pytest.raises(ValueError, match="number=head"):
        parse_expected_heads(["0=head"])


def test_parse_expected_heads_rejects_blank_head() -> None:
    with pytest.raises(ValueError, match="number=head"):
        parse_expected_heads(["7=  "])


@pytest.mark.parametrize("values", [["7=head-7", "7=head-7"], ["7=old", "7=new"]])
def test_parse_expected_heads_rejects_duplicate_numbers(values: list[str]) -> None:
    with pytest.raises(ValueError, match="duplicate PR number"):
        parse_expected_heads(values)


def test_parse_expected_heads_accepts_valid_entries() -> None:
    assert parse_expected_heads(["7=head-7", "8=head-8"]) == {7: "head-7", 8: "head-8"}
