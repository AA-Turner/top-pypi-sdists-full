"""Tests for aroom unpack command."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from anteroom.unpack import _bundled_root, unpack


@pytest.fixture
def dest_dir(tmp_path: Path) -> Path:
    return tmp_path / "unpacked"


@pytest.fixture
def fake_bundled(tmp_path: Path) -> Path:
    """Create a minimal fake _bundled directory."""
    bundled = tmp_path / "_bundled"
    bundled.mkdir()
    (bundled / "__init__.py").touch()

    tests = bundled / "tests"
    tests.mkdir()
    (tests / "__init__.py").touch()
    unit = tests / "unit"
    unit.mkdir()
    (unit / "__init__.py").touch()
    (unit / "test_example.py").write_text("def test_one(): pass\n")

    docs = bundled / "docs"
    docs.mkdir()
    (docs / "index.md").write_text("# Docs\n")

    scripts = bundled / "scripts"
    scripts.mkdir()
    (scripts / "run.sh").write_text("#!/bin/bash\necho hi\n")

    (bundled / "pyproject.toml").write_text("[project]\nname = 'anteroom'\n")
    (bundled / "README.md").write_text("# Anteroom\n")
    (bundled / "LICENSE").write_text("Apache-2.0\n")

    return bundled


class TestBundledRoot:
    def test_returns_path_relative_to_module(self) -> None:
        root = _bundled_root()
        assert root.name == "_bundled"
        assert root.parent.name == "anteroom"


class TestUnpack:
    def test_unpacks_to_dest(self, fake_bundled: Path, dest_dir: Path) -> None:
        with patch("anteroom.unpack._bundled_root", return_value=fake_bundled):
            unpack(dest_dir)

        assert (dest_dir / "tests" / "unit" / "test_example.py").exists()
        assert (dest_dir / "docs" / "index.md").exists()
        assert (dest_dir / "scripts" / "run.sh").exists()
        assert (dest_dir / "pyproject.toml").exists()
        assert (dest_dir / "README.md").exists()
        assert (dest_dir / "LICENSE").exists()

    def test_creates_src_copy(self, fake_bundled: Path, dest_dir: Path) -> None:
        with patch("anteroom.unpack._bundled_root", return_value=fake_bundled):
            unpack(dest_dir)

        src_dir = dest_dir / "src" / "anteroom"
        assert src_dir.is_dir()
        assert not src_dir.is_symlink()

    def test_refuses_existing_dest_without_force(self, fake_bundled: Path, dest_dir: Path) -> None:
        dest_dir.mkdir(parents=True)
        with patch("anteroom.unpack._bundled_root", return_value=fake_bundled):
            with pytest.raises(SystemExit):
                unpack(dest_dir)

    def test_overwrites_with_force(self, fake_bundled: Path, dest_dir: Path) -> None:
        dest_dir.mkdir(parents=True)
        (dest_dir / "old_file.txt").write_text("stale")

        with patch("anteroom.unpack._bundled_root", return_value=fake_bundled):
            unpack(dest_dir, force=True)

        assert (dest_dir / "tests" / "unit" / "test_example.py").exists()
        assert (dest_dir / "old_file.txt").exists()

    def test_missing_bundled_dir_exits(self, tmp_path: Path, dest_dir: Path) -> None:
        missing = tmp_path / "nonexistent"
        with patch("anteroom.unpack._bundled_root", return_value=missing):
            with pytest.raises(SystemExit):
                unpack(dest_dir)

    def test_skips_missing_items(self, fake_bundled: Path, dest_dir: Path) -> None:
        """Items listed in _BUNDLED_ITEMS but not present are silently skipped."""
        with patch("anteroom.unpack._bundled_root", return_value=fake_bundled):
            unpack(dest_dir)

        assert not (dest_dir / "evals").exists()
        assert not (dest_dir / "demos").exists()

    def test_skips_symlinks_escaping_bundled_root(self, fake_bundled: Path, dest_dir: Path, tmp_path: Path) -> None:
        """Symlinks pointing outside the bundled root are not copied."""
        outside = tmp_path / "outside"
        outside.mkdir()
        secret = outside / "secret.txt"
        secret.write_text("sensitive data")

        escape_link = fake_bundled / "tests" / "unit" / "escape"
        escape_link.symlink_to(outside)

        with patch("anteroom.unpack._bundled_root", return_value=fake_bundled):
            unpack(dest_dir)

        assert not (dest_dir / "tests" / "unit" / "escape").exists()

    def test_skips_symlinks_to_same_prefix_sibling(self, tmp_path: Path, dest_dir: Path) -> None:
        """Symlinks to a same-prefix sibling dir (e.g. _bundled_evil) are blocked."""
        bundled = tmp_path / "_bundled"
        bundled.mkdir()
        (bundled / "__init__.py").touch()

        sibling = tmp_path / "_bundled_evil"
        sibling.mkdir()
        (sibling / "pwned.txt").write_text("gotcha")

        tests = bundled / "tests"
        tests.mkdir()
        (tests / "__init__.py").touch()
        escape = tests / "sibling_escape"
        escape.symlink_to(sibling)

        with patch("anteroom.unpack._bundled_root", return_value=bundled):
            unpack(dest_dir)

        assert not (dest_dir / "tests" / "sibling_escape").exists()
