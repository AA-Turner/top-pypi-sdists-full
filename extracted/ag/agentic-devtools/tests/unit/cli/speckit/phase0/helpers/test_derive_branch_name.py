"""Tests for derive_branch_name in speckit/phase0/helpers.py (FR-010)."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.phase0.helpers import derive_branch_name


class TestDeriveBranchName:
    """Tests for the derive_branch_name function."""

    def test_integer_reference(self) -> None:
        assert derive_branch_name(1799) == "speckit/1799/phase-0-normalize"

    def test_hash_prefixed_reference(self) -> None:
        assert derive_branch_name("#1799") == "speckit/1799/phase-0-normalize"

    def test_invalid_reference_is_rejected(self) -> None:
        with pytest.raises(ValueError):
            derive_branch_name("not-a-number")
