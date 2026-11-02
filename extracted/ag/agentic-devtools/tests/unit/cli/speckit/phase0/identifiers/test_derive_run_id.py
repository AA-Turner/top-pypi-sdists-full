"""Tests for derive_run_id in speckit/phase0/identifiers.py (FR-001)."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.phase0.identifiers import derive_run_id


class TestDeriveRunId:
    """Tests for the derive_run_id function."""

    def test_valid_inputs(self) -> None:
        assert derive_run_id("owner/repo", 123456789, 1) == "gh:owner/repo:123456789:1"

    def test_second_attempt(self) -> None:
        assert derive_run_id("owner/repo", 42, 3) == "gh:owner/repo:42:3"

    def test_rejects_invalid_repository_slug(self) -> None:
        with pytest.raises(ValueError):
            derive_run_id("owner-repo", 1, 1)

    def test_rejects_repository_slug_with_extra_segment(self) -> None:
        with pytest.raises(ValueError):
            derive_run_id("owner/repo/extra", 1, 1)

    def test_rejects_repository_slug_with_whitespace(self) -> None:
        with pytest.raises(ValueError):
            derive_run_id("owner/bad repo", 1, 1)

    def test_rejects_non_positive_workflow_run_id(self) -> None:
        with pytest.raises(ValueError):
            derive_run_id("owner/repo", 0, 1)

    def test_rejects_non_positive_workflow_run_attempt(self) -> None:
        with pytest.raises(ValueError):
            derive_run_id("owner/repo", 1, -1)

    def test_rejects_non_integer_workflow_run_id(self) -> None:
        with pytest.raises(ValueError):
            derive_run_id("owner/repo", "1", 1)  # type: ignore[arg-type]
