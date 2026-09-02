"""Tests for detect_npm_footprint."""

import os
import sys
from pathlib import Path

import pytest

from agentic_devtools.cli.setup.npm_footprint import (
    NPM_INDICATOR_FILES,
    detect_npm_footprint,
)


class TestDetectNpmFootprint:
    """Tests for detect_npm_footprint."""

    def test_returns_true_when_package_json_exists(self, tmp_path: Path) -> None:
        """Returns True when package.json exists at the directory root."""
        (tmp_path / "package.json").write_text("{}", encoding="utf-8")
        assert detect_npm_footprint(tmp_path) is True

    def test_returns_true_when_yarn_lock_exists(self, tmp_path: Path) -> None:
        """Returns True when yarn.lock exists (non-first indicator)."""
        (tmp_path / "yarn.lock").write_text("", encoding="utf-8")
        assert detect_npm_footprint(tmp_path) is True

    def test_returns_true_when_nvmrc_exists(self, tmp_path: Path) -> None:
        """Returns True when .nvmrc exists."""
        (tmp_path / ".nvmrc").write_text("18", encoding="utf-8")
        assert detect_npm_footprint(tmp_path) is True

    def test_returns_true_when_pnpm_lock_exists(self, tmp_path: Path) -> None:
        """Returns True when pnpm-lock.yaml exists."""
        (tmp_path / "pnpm-lock.yaml").write_text("", encoding="utf-8")
        assert detect_npm_footprint(tmp_path) is True

    def test_returns_true_when_bun_lockb_exists(self, tmp_path: Path) -> None:
        """Returns True when bun.lockb exists."""
        (tmp_path / "bun.lockb").write_bytes(b"\x00")
        assert detect_npm_footprint(tmp_path) is True

    def test_returns_false_when_no_indicators_present(self, tmp_path: Path) -> None:
        """Returns False when no npm indicator files are present."""
        (tmp_path / "README.md").write_text("hello", encoding="utf-8")
        assert detect_npm_footprint(tmp_path) is False

    def test_returns_false_for_empty_directory(self, tmp_path: Path) -> None:
        """Returns False for a completely empty directory."""
        assert detect_npm_footprint(tmp_path) is False

    def test_short_circuits_on_first_match(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Short-circuits after first match — at most 8 is_file() calls per NFR-001."""
        # Place the first indicator so it matches immediately
        (tmp_path / "package.json").write_text("{}", encoding="utf-8")

        calls: list[str] = []
        original_is_file = Path.is_file

        def tracking_is_file(self: Path) -> bool:
            calls.append(str(self))
            return original_is_file(self)

        monkeypatch.setattr(Path, "is_file", tracking_is_file)
        result = detect_npm_footprint(tmp_path)

        assert result is True
        # Should have called is_file() exactly once (short-circuited on package.json)
        assert len(calls) == 1

    def test_returns_false_when_indicator_name_is_directory(self, tmp_path: Path) -> None:
        """Ignores directories named like indicator files."""
        (tmp_path / "package.json").mkdir()
        assert detect_npm_footprint(tmp_path) is False

    def test_does_not_scan_subdirectories(self, tmp_path: Path) -> None:
        """Does not detect indicators in subdirectories — only checks root."""
        subdir = tmp_path / "subproject"
        subdir.mkdir()
        (subdir / "package.json").write_text("{}", encoding="utf-8")
        assert detect_npm_footprint(tmp_path) is False

    @pytest.mark.skipif(
        sys.platform == "win32" and not os.environ.get("CI"),
        reason="Symlink creation may require elevated privileges on Windows",
    )
    def test_detects_symlink_indicator(self, tmp_path: Path) -> None:
        """Detects indicator file that is a symlink (target exists)."""
        real_file = tmp_path / "actual_package.json"
        real_file.write_text("{}", encoding="utf-8")
        (tmp_path / "package.json").symlink_to(real_file)
        assert detect_npm_footprint(tmp_path) is True

    def test_detects_empty_package_json(self, tmp_path: Path) -> None:
        """Detects package.json even when it's empty (existence-only check)."""
        (tmp_path / "package.json").write_text("", encoding="utf-8")
        assert detect_npm_footprint(tmp_path) is True

    def test_npm_indicator_files_has_eight_entries(self) -> None:
        """NPM_INDICATOR_FILES contains exactly eight indicator files."""
        assert len(NPM_INDICATOR_FILES) == 8

    def test_all_indicator_files_detected_individually(self, tmp_path: Path) -> None:
        """Each indicator file triggers detection when present alone."""
        for filename in NPM_INDICATOR_FILES:
            # Create a fresh subdirectory for each test
            test_dir = tmp_path / filename.replace(".", "_")
            test_dir.mkdir()
            (test_dir / filename).write_text("", encoding="utf-8")
            assert detect_npm_footprint(test_dir) is True, f"Failed for {filename}"
