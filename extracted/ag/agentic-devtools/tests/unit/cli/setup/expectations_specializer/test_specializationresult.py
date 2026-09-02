"""Tests for the ``SpecializationResult`` dataclass."""

from __future__ import annotations

import dataclasses

import pytest

from agentic_devtools.cli.setup.expectations_specializer import (
    VALID_STATUSES,
    SpecializationResult,
)


class TestSpecializationResult:
    """Construction, defaults, discriminator, and frozenness contract."""

    def test_valid_status_values(self) -> None:
        """The recognised status discriminators are exported."""
        assert VALID_STATUSES == ("success", "skipped", "error")

    def test_success_construction(self) -> None:
        """A success result carries content and a ``None`` reason by default."""
        result = SpecializationResult(status="success", content="# doc")
        assert result.status == "success"
        assert result.content == "# doc"
        assert result.reason is None

    def test_skipped_construction(self) -> None:
        """A skipped result carries a reason and a ``None`` content by default."""
        result = SpecializationResult(status="skipped", reason="missing doc")
        assert result.status == "skipped"
        assert result.content is None
        assert result.reason == "missing doc"

    def test_error_construction(self) -> None:
        """An error result carries a reason."""
        result = SpecializationResult(status="error", reason="boom")
        assert result.status == "error"
        assert result.reason == "boom"

    def test_defaults(self) -> None:
        """``content`` and ``reason`` default to ``None``."""
        result = SpecializationResult(status="skipped")
        assert result.content is None
        assert result.reason is None

    def test_is_frozen(self) -> None:
        """The dataclass is frozen — attribute assignment raises."""
        result = SpecializationResult(status="success")
        with pytest.raises(dataclasses.FrozenInstanceError):
            result.status = "error"  # type: ignore[misc]
