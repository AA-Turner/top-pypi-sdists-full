"""Tests for ensure_placeholder_docs precondition helper."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.cli.checks.setup_drift import ensure_placeholder_docs


class TestEnsurePlaceholderDocs:
    """Tests for the ensure_placeholder_docs function (FR-008)."""

    def test_both_missing_creates_readme(self, tmp_path: Path) -> None:
        """Both placeholders missing → creates README.md stub."""
        docs_dir = tmp_path / "docs" / "setup-expectations"
        result = ensure_placeholder_docs(docs_dir)
        assert (docs_dir / "README.md").exists()
        content = (docs_dir / "README.md").read_text(encoding="utf-8")
        assert content.strip()  # non-empty
        assert "docs/setup-expectations/README.md" in result.created
        assert result.already_present == []

    def test_both_present_noop(self, tmp_path: Path) -> None:
        """Both files present and non-empty → no-op (SC-006)."""
        docs_dir = tmp_path / "docs" / "setup-expectations"
        docs_dir.mkdir(parents=True)
        (docs_dir / "README.md").write_text("# Readme\n", encoding="utf-8")
        (docs_dir / "agdt-setup.md").write_text("# Setup\n", encoding="utf-8")
        result = ensure_placeholder_docs(docs_dir)
        assert result.created == []
        assert len(result.already_present) == 2

    def test_one_present_one_missing_noop(self, tmp_path: Path) -> None:
        """One present non-empty, one missing → no-op (minimum met)."""
        docs_dir = tmp_path / "docs" / "setup-expectations"
        docs_dir.mkdir(parents=True)
        (docs_dir / "agdt-setup.md").write_text("# Setup\n", encoding="utf-8")
        result = ensure_placeholder_docs(docs_dir)
        assert result.created == []
        assert "docs/setup-expectations/agdt-setup.md" in result.already_present

    def test_one_empty_one_present_noop(self, tmp_path: Path) -> None:
        """One placeholder empty/whitespace, other present → no-op."""
        docs_dir = tmp_path / "docs" / "setup-expectations"
        docs_dir.mkdir(parents=True)
        (docs_dir / "README.md").write_text("   \n", encoding="utf-8")
        (docs_dir / "agdt-setup.md").write_text("# Setup\n", encoding="utf-8")
        result = ensure_placeholder_docs(docs_dir)
        assert result.created == []
        assert "docs/setup-expectations/agdt-setup.md" in result.already_present

    def test_deleted_path_other_present_noop(self, tmp_path: Path) -> None:
        """Placeholder in deleted_paths, other present → no-op."""
        docs_dir = tmp_path / "docs" / "setup-expectations"
        docs_dir.mkdir(parents=True)
        (docs_dir / "agdt-setup.md").write_text("# Setup\n", encoding="utf-8")
        result = ensure_placeholder_docs(
            docs_dir,
            deleted_paths=["docs/setup-expectations/README.md"],
        )
        assert result.created == []
        assert "docs/setup-expectations/agdt-setup.md" in result.already_present

    def test_all_deleted_raises_valueerror(self, tmp_path: Path) -> None:
        """All placeholders deleted → raises ValueError."""
        docs_dir = tmp_path / "docs" / "setup-expectations"
        docs_dir.mkdir(parents=True)
        with pytest.raises(ValueError, match="No non-empty placeholder doc"):
            ensure_placeholder_docs(
                docs_dir,
                deleted_paths=[
                    "docs/setup-expectations/README.md",
                    "docs/setup-expectations/agdt-setup.md",
                ],
            )

    def test_readme_deleted_other_missing_raises(self, tmp_path: Path) -> None:
        """README.md in deleted_paths, agdt-setup.md missing → raises ValueError."""
        docs_dir = tmp_path / "docs" / "setup-expectations"
        docs_dir.mkdir(parents=True)
        with pytest.raises(ValueError, match="auto-creation is blocked"):
            ensure_placeholder_docs(
                docs_dir,
                deleted_paths=["docs/setup-expectations/README.md"],
            )

    def test_both_empty_creates_readme(self, tmp_path: Path) -> None:
        """Both files empty → creates README.md."""
        docs_dir = tmp_path / "docs" / "setup-expectations"
        docs_dir.mkdir(parents=True)
        (docs_dir / "README.md").write_text("", encoding="utf-8")
        (docs_dir / "agdt-setup.md").write_text("  ", encoding="utf-8")
        result = ensure_placeholder_docs(docs_dir)
        assert "docs/setup-expectations/README.md" in result.created
        content = (docs_dir / "README.md").read_text(encoding="utf-8")
        assert content.strip()

    def test_no_deleted_paths_default_none(self, tmp_path: Path) -> None:
        """deleted_paths defaults to None, both missing → creates."""
        docs_dir = tmp_path / "docs" / "setup-expectations"
        result = ensure_placeholder_docs(docs_dir, deleted_paths=None)
        assert (docs_dir / "README.md").exists()
        assert result.created
