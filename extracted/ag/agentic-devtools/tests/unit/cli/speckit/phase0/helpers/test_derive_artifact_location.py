"""Tests for derive_artifact_location in speckit/phase0/helpers.py (FR-003)."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.phase0.helpers import derive_artifact_location


class TestDeriveArtifactLocation:
    """Tests for the derive_artifact_location function."""

    def test_integer_reference(self) -> None:
        assert derive_artifact_location(1799) == ".speckit/issues/1799/issue.md"

    def test_hash_prefixed_reference(self) -> None:
        assert derive_artifact_location("#1799") == ".speckit/issues/1799/issue.md"

    def test_invalid_reference_is_rejected(self) -> None:
        with pytest.raises(ValueError):
            derive_artifact_location("")
