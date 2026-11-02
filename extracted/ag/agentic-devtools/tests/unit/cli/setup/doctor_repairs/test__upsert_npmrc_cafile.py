"""Tests for _upsert_npmrc_cafile — idempotent, atomic npmrc upsert."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.setup.doctor_repairs import _upsert_npmrc_cafile


class TestUpsertNpmrcCafile:
    """_upsert_npmrc_cafile performs key-level idempotent upsert with atomic write."""

    def test_creates_new_file_when_missing(self, tmp_path: Path) -> None:
        """Creates ~/.agdt/npmrc with cafile= line when file does not exist."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        ca_path = "/path/to/bundle.pem"

        with patch("agentic_devtools.cli.setup.doctor_repairs.Path.home", return_value=fake_home):
            result = _upsert_npmrc_cafile(ca_path)

        assert result == fake_home / ".agdt" / "npmrc"
        content = result.read_text(encoding="utf-8")
        assert content == f"cafile={ca_path}\n"

    def test_replaces_existing_cafile_line(self, tmp_path: Path) -> None:
        """Replaces an existing cafile= line, preserving other lines."""
        fake_home = tmp_path / "home"
        npmrc = fake_home / ".agdt" / "npmrc"
        npmrc.parent.mkdir(parents=True)
        npmrc.write_text("registry=https://registry.npmjs.org\ncafile=/old/path.pem\nstrict-ssl=true\n")
        new_ca = "/new/bundle.pem"

        with patch("agentic_devtools.cli.setup.doctor_repairs.Path.home", return_value=fake_home):
            result = _upsert_npmrc_cafile(new_ca)

        content = result.read_text(encoding="utf-8")
        assert f"cafile={new_ca}" in content
        assert "cafile=/old/path.pem" not in content
        assert "registry=https://registry.npmjs.org" in content
        assert "strict-ssl=true" in content

    def test_appends_when_no_cafile_line_exists(self, tmp_path: Path) -> None:
        """Appends cafile= when no existing cafile= line is present."""
        fake_home = tmp_path / "home"
        npmrc = fake_home / ".agdt" / "npmrc"
        npmrc.parent.mkdir(parents=True)
        npmrc.write_text("registry=https://registry.npmjs.org\nstrict-ssl=true\n")
        new_ca = "/new/bundle.pem"

        with patch("agentic_devtools.cli.setup.doctor_repairs.Path.home", return_value=fake_home):
            result = _upsert_npmrc_cafile(new_ca)

        content = result.read_text(encoding="utf-8")
        lines = content.splitlines()
        assert lines[0] == "registry=https://registry.npmjs.org"
        assert lines[1] == "strict-ssl=true"
        assert lines[2] == f"cafile={new_ca}"

    def test_preserves_all_other_lines_verbatim(self, tmp_path: Path) -> None:
        """All non-cafile lines are preserved exactly as they were."""
        fake_home = tmp_path / "home"
        npmrc = fake_home / ".agdt" / "npmrc"
        npmrc.parent.mkdir(parents=True)
        original = "# comment\nregistry=foo\n  spaces  \n"
        npmrc.write_text(original)

        with patch("agentic_devtools.cli.setup.doctor_repairs.Path.home", return_value=fake_home):
            _upsert_npmrc_cafile("/ca.pem")

        content = (fake_home / ".agdt" / "npmrc").read_text(encoding="utf-8")
        assert "# comment\n" in content
        assert "registry=foo\n" in content
        assert "  spaces  \n" in content

    def test_idempotent_same_path(self, tmp_path: Path) -> None:
        """Running twice with the same ca_path produces the same result."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        ca_path = "/path/to/bundle.pem"

        with patch("agentic_devtools.cli.setup.doctor_repairs.Path.home", return_value=fake_home):
            _upsert_npmrc_cafile(ca_path)
            _upsert_npmrc_cafile(ca_path)

        content = (fake_home / ".agdt" / "npmrc").read_text(encoding="utf-8")
        assert content.count("cafile=") == 1

    def test_temp_file_cleaned_up_on_rename_failure(self, tmp_path: Path) -> None:
        """Temp file is cleaned up when os.replace fails."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()

        with (
            patch("agentic_devtools.cli.setup.doctor_repairs.Path.home", return_value=fake_home),
            patch("os.replace", side_effect=OSError("rename failed")),
        ):
            try:
                _upsert_npmrc_cafile("/ca.pem")
            except OSError:
                pass

        # No temp files should remain.
        agdt_dir = fake_home / ".agdt"
        if agdt_dir.exists():
            remaining = [f for f in agdt_dir.iterdir() if f.name.startswith(".npmrc_") and f.name.endswith(".tmp")]
            assert remaining == []

    def test_temp_cleanup_ignores_unlink_oserror(self, tmp_path: Path) -> None:
        """When both os.replace and os.unlink fail, no exception leaks from cleanup."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()

        with (
            patch("agentic_devtools.cli.setup.doctor_repairs.Path.home", return_value=fake_home),
            patch("os.replace", side_effect=OSError("rename failed")),
            patch("os.unlink", side_effect=OSError("unlink failed")),
        ):
            with pytest.raises(OSError, match="rename failed"):
                _upsert_npmrc_cafile("/ca.pem")

    def test_fd_closed_on_write_failure(self, tmp_path: Path) -> None:
        """File descriptor is closed when os.write raises."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()

        with (
            patch("agentic_devtools.cli.setup.doctor_repairs.Path.home", return_value=fake_home),
            patch("os.write", side_effect=OSError("write failed")),
        ):
            with pytest.raises(OSError, match="write failed"):
                _upsert_npmrc_cafile("/ca.pem")

    def test_creates_parent_directory_if_missing(self, tmp_path: Path) -> None:
        """Creates ~/.agdt/ directory if it does not exist."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        assert not (fake_home / ".agdt").exists()

        with patch("agentic_devtools.cli.setup.doctor_repairs.Path.home", return_value=fake_home):
            result = _upsert_npmrc_cafile("/ca.pem")

        assert result.exists()
        assert (fake_home / ".agdt").is_dir()

    def test_accepts_path_object(self, tmp_path: Path) -> None:
        """Accepts Path object as ca_path argument."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()

        with patch("agentic_devtools.cli.setup.doctor_repairs.Path.home", return_value=fake_home):
            result = _upsert_npmrc_cafile(Path("/some/path/bundle.pem"))

        content = result.read_text(encoding="utf-8")
        assert "cafile=/some/path/bundle.pem" in content

    def test_appends_correctly_when_last_line_has_no_trailing_newline(self, tmp_path: Path) -> None:
        """cafile= starts on its own line even when existing content lacks a trailing newline."""
        fake_home = tmp_path / "home"
        npmrc = fake_home / ".agdt" / "npmrc"
        npmrc.parent.mkdir(parents=True)
        # Deliberately omit trailing newline on the last line.
        npmrc.write_bytes(b"registry=https://registry.npmjs.org")

        with patch("agentic_devtools.cli.setup.doctor_repairs.Path.home", return_value=fake_home):
            result = _upsert_npmrc_cafile("/ca.pem")

        lines = result.read_text(encoding="utf-8").splitlines()
        assert lines[0] == "registry=https://registry.npmjs.org"
        assert lines[1] == "cafile=/ca.pem"
        assert len(lines) == 2

    def test_multiple_cafile_lines_collapsed_to_single_entry(self, tmp_path: Path) -> None:
        """Multiple existing cafile= lines are collapsed to a single updated entry."""
        fake_home = tmp_path / "home"
        npmrc = fake_home / ".agdt" / "npmrc"
        npmrc.parent.mkdir(parents=True)
        npmrc.write_text("registry=https://registry.npmjs.org\ncafile=/old1.pem\nstrict-ssl=true\ncafile=/old2.pem\n")

        with patch("agentic_devtools.cli.setup.doctor_repairs.Path.home", return_value=fake_home):
            result = _upsert_npmrc_cafile("/new.pem")

        content = result.read_text(encoding="utf-8")
        assert content.count("cafile=") == 1
        assert "cafile=/new.pem" in content
        assert "cafile=/old1.pem" not in content
        assert "cafile=/old2.pem" not in content
        assert "registry=https://registry.npmjs.org" in content
        assert "strict-ssl=true" in content

    def test_preserves_non_utf8_bytes_when_upserting(self, tmp_path: Path) -> None:
        """Non-UTF8 npmrc bytes are preserved while inserting the ASCII cafile= line."""
        fake_home = tmp_path / "home"
        npmrc = fake_home / ".agdt" / "npmrc"
        npmrc.parent.mkdir(parents=True)
        npmrc.write_bytes(b"prefix=\xff\n")

        with patch("agentic_devtools.cli.setup.doctor_repairs.Path.home", return_value=fake_home):
            result = _upsert_npmrc_cafile("/ca.pem")

        assert result.read_bytes() == b"prefix=\xff\ncafile=/ca.pem\n"

    def test_write_zero_raises_oserror(self, tmp_path: Path) -> None:
        """Raises OSError when os.write returns 0 (disk full / bad fd) to prevent infinite loop."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()

        with (
            patch("agentic_devtools.cli.setup.doctor_repairs.Path.home", return_value=fake_home),
            patch("os.write", return_value=0),
        ):
            with pytest.raises(OSError, match="os.write returned 0"):
                _upsert_npmrc_cafile("/ca.pem")

    def test_fsync_called_before_rename(self, tmp_path: Path) -> None:
        """os.fsync is called on the temp fd before os.replace to ensure durability."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()

        with (
            patch("agentic_devtools.cli.setup.doctor_repairs.Path.home", return_value=fake_home),
            patch("os.fsync") as mock_fsync,
        ):
            _upsert_npmrc_cafile("/ca.pem")

        mock_fsync.assert_called_once()
