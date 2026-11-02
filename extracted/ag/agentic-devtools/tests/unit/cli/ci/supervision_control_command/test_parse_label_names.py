"""Tests for the parse_label_names symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control_command import parse_label_names


def test_parse_label_names_accepts_valid_array() -> None:
    assert parse_label_names([{"name": "a"}, {"name": "b"}]) == frozenset({"a", "b"})


@pytest.mark.parametrize("raw", ["not-a-list", [{"name": 1}], ["not-a-dict"]])
def test_parse_label_names_rejects_malformed_payloads(raw: object) -> None:
    with pytest.raises(ValueError, match="label list"):
        parse_label_names(raw)
