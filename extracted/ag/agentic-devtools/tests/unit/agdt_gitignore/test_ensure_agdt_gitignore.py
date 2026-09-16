"""Tests for agentic_devtools.agdt_gitignore.ensure_agdt_gitignore."""

from unittest.mock import patch

from agentic_devtools.agdt_gitignore import (
    AGDT_GITIGNORE_ENTRIES,
    AGDT_GITIGNORE_HEADER,
    ensure_agdt_gitignore,
)


class TestEnsureAgdtGitignore:
    """Tests for the ensure_agdt_gitignore function."""

    def test_creates_gitignore_with_correct_content(self, tmp_path):
        """Given a valid git_root, creates .agdt/.gitignore with header + entries."""
        result = ensure_agdt_gitignore(tmp_path)

        assert result is True
        gitignore_path = tmp_path / ".agdt" / ".gitignore"
        assert gitignore_path.exists()
        content = gitignore_path.read_text(encoding="utf-8")
        assert content.startswith(AGDT_GITIGNORE_HEADER)
        for entry in AGDT_GITIGNORE_ENTRIES:
            assert entry in content

    def test_creates_gitignore_with_native_newline(self, tmp_path):
        """Uses the platform-native newline when creating the file."""
        native_newline = "\r\n"
        with patch("agentic_devtools.agdt_gitignore.os.linesep", native_newline):
            assert ensure_agdt_gitignore(tmp_path) is True

        content = (tmp_path / ".agdt" / ".gitignore").read_bytes()
        assert content == (
            (AGDT_GITIGNORE_HEADER + "\n".join(AGDT_GITIGNORE_ENTRIES) + "\n")
            .replace("\n", native_newline)
            .encode("utf-8")
        )

    def test_overwrites_existing_gitignore(self, tmp_path):
        """Overwrites an existing .agdt/.gitignore with different content."""
        agdt_dir = tmp_path / ".agdt"
        agdt_dir.mkdir()
        gitignore_path = agdt_dir / ".gitignore"
        gitignore_path.write_text("old content\n", encoding="utf-8")

        result = ensure_agdt_gitignore(tmp_path)

        assert result is True
        content = gitignore_path.read_text(encoding="utf-8")
        assert "old content" not in content
        assert content.startswith(AGDT_GITIGNORE_HEADER)

    def test_returns_false_when_no_git_root(self):
        """Returns False when git_root is None."""
        assert ensure_agdt_gitignore(None) is False

    def test_creates_agdt_dir_if_missing(self, tmp_path):
        """Creates .agdt/ directory if it doesn't exist."""
        assert not (tmp_path / ".agdt").exists()

        result = ensure_agdt_gitignore(tmp_path)

        assert result is True
        assert (tmp_path / ".agdt").is_dir()

    def test_returns_false_on_write_error(self, tmp_path):
        """Returns False when write_bytes raises OSError."""
        with patch("pathlib.Path.write_bytes", side_effect=OSError("permission denied")):
            result = ensure_agdt_gitignore(tmp_path)

        assert result is False

    def test_returns_false_on_read_error_without_writing(self, tmp_path):
        """A non-missing-file read error returns False and leaves the file untouched."""
        ensure_agdt_gitignore(tmp_path)
        gitignore_path = tmp_path / ".agdt" / ".gitignore"
        gitignore_path.write_bytes(b"stale content\n")

        with patch("pathlib.Path.read_bytes", side_effect=PermissionError("permission denied")):
            with patch("pathlib.Path.write_bytes") as mock_write:
                result = ensure_agdt_gitignore(tmp_path)

        assert result is False
        mock_write.assert_not_called()
        assert gitignore_path.read_bytes() == b"stale content\n"

    def test_does_not_write_canonical_lf_content(self, tmp_path):
        """Canonical LF content remains byte-for-byte unchanged."""
        ensure_agdt_gitignore(tmp_path)
        gitignore_path = tmp_path / ".agdt" / ".gitignore"
        original = gitignore_path.read_bytes()

        with patch("pathlib.Path.write_bytes") as mock_write:
            assert ensure_agdt_gitignore(tmp_path) is True

        assert gitignore_path.read_bytes() == original
        mock_write.assert_not_called()

    def test_does_not_write_canonical_crlf_content(self, tmp_path):
        """Canonical CRLF content remains byte-for-byte unchanged."""
        ensure_agdt_gitignore(tmp_path)
        gitignore_path = tmp_path / ".agdt" / ".gitignore"
        gitignore_path.write_bytes(gitignore_path.read_bytes().replace(b"\n", b"\r\n"))
        original = gitignore_path.read_bytes()

        with patch("pathlib.Path.write_bytes") as mock_write:
            assert ensure_agdt_gitignore(tmp_path) is True

        assert gitignore_path.read_bytes() == original
        mock_write.assert_not_called()

    def test_corrects_content_using_existing_crlf(self, tmp_path):
        """Corrections preserve the existing CRLF newline convention."""
        gitignore_path = tmp_path / ".agdt" / ".gitignore"
        gitignore_path.parent.mkdir()
        gitignore_path.write_bytes(b"incorrect\r\ncontent\r\n")

        assert ensure_agdt_gitignore(tmp_path) is True
        content = gitignore_path.read_bytes()
        assert b"\r\n" in content
        assert b"\n" not in content.replace(b"\r\n", b"")

    def test_entries_constant_values(self):
        """AGDT_GITIGNORE_ENTRIES contains expected values."""
        assert "runtime-bootstrap.json" in AGDT_GITIGNORE_ENTRIES
        assert "identity.json" in AGDT_GITIGNORE_ENTRIES
        assert "workflows/" in AGDT_GITIGNORE_ENTRIES
        assert "cache/" in AGDT_GITIGNORE_ENTRIES

    def test_content_ends_with_newline(self, tmp_path):
        """The generated file content ends with a trailing newline."""
        ensure_agdt_gitignore(tmp_path)

        content = (tmp_path / ".agdt" / ".gitignore").read_text(encoding="utf-8")
        assert content.endswith("\n")
