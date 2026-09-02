"""Tests for derive_issue_key in speckit/phase0/helpers.py (FR-010)."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.phase0.helpers import derive_issue_key


class TestDeriveIssueKey:
    """Tests for the derive_issue_key function."""

    def test_integer_reference(self) -> None:
        assert derive_issue_key(1799) == "1799"

    def test_plain_string_reference(self) -> None:
        assert derive_issue_key("1799") == "1799"

    def test_hash_prefixed_string_reference(self) -> None:
        assert derive_issue_key("#1799") == "1799"

    def test_whitespace_is_stripped(self) -> None:
        assert derive_issue_key("  #1799  ") == "1799"

    def test_hash_with_inner_whitespace(self) -> None:
        assert derive_issue_key("# 1799") == "1799"

    def test_leading_zeros_are_normalized(self) -> None:
        assert derive_issue_key("01799") == "1799"

    def test_bool_is_rejected(self) -> None:
        with pytest.raises(ValueError):
            derive_issue_key(True)

    def test_zero_is_rejected(self) -> None:
        with pytest.raises(ValueError):
            derive_issue_key(0)

    def test_negative_integer_is_rejected(self) -> None:
        with pytest.raises(ValueError):
            derive_issue_key(-5)

    def test_empty_string_is_rejected(self) -> None:
        with pytest.raises(ValueError):
            derive_issue_key("   ")

    def test_non_numeric_string_is_rejected(self) -> None:
        with pytest.raises(ValueError):
            derive_issue_key("abc")

    def test_hash_only_string_is_rejected(self) -> None:
        with pytest.raises(ValueError):
            derive_issue_key("#")
