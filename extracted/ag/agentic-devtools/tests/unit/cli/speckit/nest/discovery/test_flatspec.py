"""Tests for FlatSpec dataclass in nest/discovery.py."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.speckit.nest.discovery import FlatSpec


class TestFlatSpec:
    """Tests for the FlatSpec dataclass."""

    def test_stores_fields_correctly(self, tmp_path: Path) -> None:
        """Fields are accessible after construction."""
        spec = FlatSpec(issue_number=42, path=tmp_path / "42-slug", slug="slug")
        assert spec.issue_number == 42
        assert spec.path == tmp_path / "42-slug"
        assert spec.slug == "slug"

    def test_equality(self, tmp_path: Path) -> None:
        """Two FlatSpec instances with the same fields are equal."""
        p = tmp_path / "1-a"
        assert FlatSpec(issue_number=1, path=p, slug="a") == FlatSpec(issue_number=1, path=p, slug="a")
